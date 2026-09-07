"""P2 SSD backbone + bounded sparse global slots (M3 proposal, A4 target).

Per block: (i) an SSD-lite recurrent branch
      S_t = a_t * S_{t-1} + k_t v_t^T,  a_t = exp(-exp(w_a(x_t)))
  (scalar decay, no erase term: the pure-decay control against P1's
  key-structured removal); (ii) a global slot branch holding at most G
  exact (key, value) pairs written on a fixed stride (deterministic
  sparse long-range coverage, disjoint from the local W window); read is
  exact softmax attention over all stored slots, which is top-G
  selection by query-key match with no learned router and therefore no
  router-collapse mode (deviation from the blueprint's learned top-k is
  deliberate and documented here: zero router params, nothing to balance,
  eviction is oldest-first); (iii) the exact sliding-window branch
  reused from P1. A 3-way input-dependent gate fuses the three reads.
  SwiGLU closes the block.

A4 control: `slots=0` disables slot writes/reads (branch contributes
zeros, params unchanged) and must reproduce pure-SSD behaviour.

State per layer (batch 1): H*d_k*d_v (SSD S) + 2*G*H*(d_k+d_v) (slot K/V,
capped at G globally, oldest evicted) + 2*W*d_win (window KV) + H
scalars. No factor of T. Reference kernel: forward_recurrent applies
step() token-by-token; chunk groups loop iterations only.
"""

import math

import torch
import torch.nn as nn

from .common import RMSNorm, SwiGLU
from .p1_delta_hybrid import SlidingWindowAttn
from .p1_delta_hybrid import ALPHA_BIAS_INIT
from .p3_decoupled import FusionGate3


class SSDBranch(nn.Module):
    """Scalar-decay linear recurrence (SSD-lite, no erase term)."""

    def __init__(self, d_model: int, heads: int, d_k: int, d_v: int):
        super().__init__()
        self.heads = heads
        self.d_k = d_k
        self.d_v = d_v
        self.w_q = nn.Linear(d_model, heads * d_k, bias=False)
        self.w_k = nn.Linear(d_model, heads * d_k, bias=False)
        self.w_v = nn.Linear(d_model, heads * d_v, bias=False)
        self.w_o = nn.Linear(heads * d_v, d_model, bias=False)
        self.k_norm = RMSNorm(d_k)
        self.w_a = nn.Linear(d_model, heads, bias=True)
        nn.init.constant_(self.w_a.bias, ALPHA_BIAS_INIT)

    def _split(self, x: torch.Tensor, d: int) -> torch.Tensor:
        return x.view(*x.shape[:-1], self.heads, d)

    def _normed_k(self, k: torch.Tensor) -> torch.Tensor:
        k = self.k_norm(k)
        return k / (k.norm(dim=-1, keepdim=True).clamp_min(1e-6))

    def init_state(self, batch: int, device, dtype):
        return torch.zeros(batch, self.heads, self.d_k, self.d_v,
                           device=device, dtype=dtype)

    def step(self, x_t: torch.Tensor, S: torch.Tensor):
        """x_t: (B, d). Returns (out (B, d), S_new). O(H*d_k*d_v)."""
        q = self._split(self.w_q(x_t), self.d_k)
        k = self._split(self.w_k(x_t), self.d_k)
        v = self._split(self.w_v(x_t), self.d_v)
        k = self._normed_k(k)
        a = torch.exp(-torch.exp(self.w_a(x_t)))  # (B, H) in (0, 1)
        S = (a.view(-1, self.heads, 1, 1) * S
             + k.unsqueeze(-1) * v.unsqueeze(-2))
        o = torch.einsum("bhki,bhk->bhi", S, q)
        return self.w_o(o.reshape(x_t.shape[0], -1)), S

    def forward_recurrent(self, x: torch.Tensor, S0: torch.Tensor, chunk: int):
        """Sequential reference forward: applies step() token-by-token; chunk
        groups loop iterations only and has no mathematical effect."""
        S = S0
        outs = []
        for s in range(0, x.shape[1], chunk):
            e = min(s + chunk, x.shape[1])
            for i in range(s, e):
                o, S = self.step(x[:, i, :], S)
                outs.append(o)
        return torch.stack(outs, dim=1), S


class SlotBuffer:
    """Global exact slots: at most G (key, value) pairs per head.

    Writes happen on a fixed stride over positions (every `stride`-th
    token, position 0 always written when G > 0); when full, the oldest
    slot is evicted. Reads are exact softmax attention over every stored
    slot. All state is O(G*H*(d_k+d_v)), never O(T*d).
    """

    def __init__(self, batch: int, heads: int, d_k: int, d_v: int,
                 slots: int, stride: int, device, dtype):
        if slots < 0:
            raise ValueError(f"slots must be >= 0, got {slots!r}")
        if stride < 1:
            raise ValueError(f"slot stride must be >= 1, got {stride!r}")
        self.heads = heads
        self.d_k = d_k
        self.d_v = d_v
        self.slots = slots
        self.stride = stride
        self.keys = torch.zeros(batch, heads, slots, d_k, device=device, dtype=dtype)
        self.vals = torch.zeros(batch, heads, slots, d_v, device=device, dtype=dtype)
        self.n = 0          # slots currently filled (<= G)
        self.pos = 0        # total tokens seen (stride clock)
        self.writes = 0     # lifetime write count (ledger/debug)

    def append(self, k: torch.Tensor, v: torch.Tensor) -> None:
        """Consider (k, v) per-head pair for the current position."""
        if self.slots == 0:
            self.pos += 1
            return
        if self.pos % self.stride == 0 or self.pos == 0:
            if self.n < self.slots:
                self.keys[:, :, self.n, :] = k
                self.vals[:, :, self.n, :] = v
                self.n += 1
            else:
                self.keys[:, :, :-1, :] = self.keys[:, :, 1:, :].clone()
                self.vals[:, :, :-1, :] = self.vals[:, :, 1:, :].clone()
                self.keys[:, :, -1, :] = k
                self.vals[:, :, -1, :] = v
            self.writes += 1
        self.pos += 1

    def read(self, q: torch.Tensor) -> torch.Tensor | None:
        """Exact attention of q (B, H, d_k) over stored slots -> (B, H, d_v)."""
        if self.n == 0:
            return None
        kk = self.keys[:, :, :self.n, :]
        vv = self.vals[:, :, :self.n, :]
        scores = (q.unsqueeze(-2) @ kk.transpose(-2, -1)) / math.sqrt(self.d_k)
        return (torch.softmax(scores, dim=-1) @ vv).squeeze(-2)


class P2Block(nn.Module):
    def __init__(self, d_model: int, heads: int, d_k: int, d_v: int,
                 win_heads: int, win_hd: int, window: int, mlp_hid: int,
                 chunk: int, rope_base: float = 10000.0,
                 slots: int = 16, slot_stride: int = 8):
        super().__init__()
        self.d_model = d_model
        self.n1 = RMSNorm(d_model)
        self.n2 = RMSNorm(d_model)
        self.ssd = SSDBranch(d_model, heads, d_k, d_v)
        self.slots = slots
        self.slot_stride = slot_stride
        self.window = SlidingWindowAttn(d_model, win_heads, win_hd, window,
                                        rope_base)
        self.fusion = FusionGate3(d_model)
        self.mlp = SwiGLU(d_model, mlp_hid)
        self.chunk = chunk

    def _slot_state(self, batch: int, device, dtype):
        return SlotBuffer(batch, self.ssd.heads, self.ssd.d_k, self.ssd.d_v,
                          self.slots, self.slot_stride, device, dtype)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Single-pass reference: one SSD trajectory feeds both the dense
        # read and the slot writer. Slot reads are exact attention over the
        # strided prefix (positions j <= i with j % stride == 0, last G),
        # stacked fresh per position: values are identical to step()'s
        # incremental buffer, but no in-place op touches the graph, so
        # training backward stays valid AND slot-path grads reach the
        # trunk k/v projs (step() detaches instead: eval-only, no grad).
        h = self.n1(x)
        b, t, _ = h.shape
        S = self.ssd.init_state(b, h.device, h.dtype)
        r_seq, q_seq, k_seq, v_seq = [], [], [], []
        for s in range(0, t, self.chunk):
            e = min(s + self.chunk, t)
            for i in range(s, e):
                hi = h[:, i, :]
                o, S = self.ssd.step(hi, S)
                r_seq.append(o)
                q_seq.append(self.ssd._split(self.ssd.w_q(hi), self.ssd.d_k))
                k_seq.append(self.ssd._normed_k(
                    self.ssd._split(self.ssd.w_k(hi), self.ssd.d_k)))
                v_seq.append(self.ssd._split(self.ssd.w_v(hi), self.ssd.d_v))
        r_out = torch.stack(r_seq, dim=1)
        if self.slots == 0:
            g_out = torch.zeros_like(r_out)  # A4 pure-SSD control
        else:
            g_seq = []
            for i in range(t):
                # j = 0 always qualifies (0 % stride == 0): idx never empty.
                idx = [j for j in range(i + 1)
                       if j % self.slot_stride == 0][-self.slots:]
                kk = torch.stack([k_seq[j] for j in idx], dim=2)
                vv = torch.stack([v_seq[j] for j in idx], dim=2)
                scores = ((q_seq[i].unsqueeze(-2) @ kk.transpose(-2, -1))
                          / math.sqrt(self.ssd.d_k))
                rd = (torch.softmax(scores, dim=-1) @ vv).squeeze(-2)
                g_seq.append(self._slot_proj(rd))
            g_out = torch.stack(g_seq, dim=1)
        w_out = self.window(h)
        x = x + self.fusion(h, r_out, g_out, w_out)
        return x + self.mlp(self.n2(x))

    def _slot_proj(self, rd: torch.Tensor) -> torch.Tensor:
        # Slot reads live in the SSD value space by construction (slot values
        # are trunk v's), so the SSD output proj is the honest projector.
        b = rd.shape[0]
        return self.ssd.w_o(rd.reshape(b, self.ssd.heads * self.ssd.d_v))

    def init_state(self, batch: int, device, dtype):
        return {"S": self.ssd.init_state(batch, device, dtype),
                "buf": self._slot_state(batch, device, dtype),
                "win": self.window.init_state(batch, device, dtype)}

    def step(self, x_t: torch.Tensor, state: dict):
        """Single-token update; x_t is (B, d). State is O(1) in T."""
        h = self.n1(x_t)
        b = x_t.shape[0]
        r_out, state["S"] = self.ssd.step(h, state["S"])
        # Slots observe the same trunk k/v the SSD just consumed.
        q = self.ssd._split(self.ssd.w_q(h), self.ssd.d_k)
        k = self.ssd._normed_k(
            self.ssd._split(self.ssd.w_k(h), self.ssd.d_k))
        v = self.ssd._split(self.ssd.w_v(h), self.ssd.d_v)
        buf = state["buf"]
        buf.append(k.detach(), v.detach())
        rd = buf.read(q)
        g_out = (torch.zeros_like(r_out) if rd is None
                 else self._slot_proj(rd))
        w_out, _ = self.window.step(h, state["win"])
        y = x_t + self.fusion(h, r_out, g_out, w_out)
        return y + self.mlp(self.n2(y)), state

    def state_size(self, bpe: int = 4) -> int:
        H, dk, dv = self.ssd.heads, self.ssd.d_k, self.ssd.d_v
        W, wd = self.window.window, self.window.wd
        win = 2 * W * wd * bpe if W > 0 else 0
        slots = 2 * self.slots * H * (dk + dv) * bpe
        return H * dk * dv * bpe + slots + win + H * bpe


class P2LM(nn.Module):
    def __init__(self, config: dict):
        super().__init__()
        self.cfg = dict(config)
        d = config["d_model"]
        self.tok_embed = nn.Embedding(config["vocab_size"], d)
        self.blocks = nn.ModuleList(
            [P2Block(d, config["heads"], config["d_k"], config["d_v"],
                     config["win_heads"], config["win_hd"], config["window"],
                     config["mlp_hid"], config["chunk"],
                     config.get("rope_base", 10000.0),
                     config.get("slots", 16),
                     config.get("slot_stride", 8))
             for _ in range(config["layers"])])
        self.norm_f = RMSNorm(d)
        self.lm_head = nn.Linear(d, config["vocab_size"], bias=False)

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        x = self.tok_embed(ids)
        for blk in self.blocks:
            x = blk(x)
        return self.lm_head(self.norm_f(x))

    def init_state(self, batch: int, device, dtype):
        return [blk.init_state(batch, device, dtype) for blk in self.blocks]

    def step(self, tok: torch.Tensor, states: list) -> tuple:
        x = self.tok_embed(tok)[:, 0, :]
        for blk, st in zip(self.blocks, states):
            x, _ = blk.step(x, st)
        return self.lm_head(self.norm_f(x)).unsqueeze(1), states

    def state_bytes(self, batch: int, length: int = 0, bpe: int = 4) -> int:
        # O(1) in length by construction; length accepted for API parity.
        return batch * sum(b.state_size(bpe) for b in self.blocks)
