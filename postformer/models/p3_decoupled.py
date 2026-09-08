"""P3 decoupled multi-scale memory (M3 proposal, A3 ablation target).

Three parallel branches per block, fused by an input-dependent 3-way gate:

(i) AccumulatorHead: decay-free additive write
      A_t = guard(A_{t-1} + beta_t * k_t v_t^T),  alpha fixed at 1.0,
  with a norm-guard rescale hook (if ||A||_F exceeds cap, rescale to cap;
  fire count accumulated on the state dict under "rescales"). Tests H3:
  the decay-free head extends copying without erase. A3 ablation:
  `use_accumulator=False` zeroes the branch (params unchanged, only the
  dynamics are removed, so the ablation is honest).

(ii) SelectiveHead: scalar-gated linear write (GLA-lite)
      S_t = alpha_t * S_{t-1} + beta_t * k_t v_t^T,
  k RMSNormed to unit norm, beta = sigmoid clamped to [0.01, 0.99],
  alpha = exp(-exp(.)) init ~0.97. Same dynamics family as the P5
  control but at feature dim d_k (not the degree-2 map), so A3 and A1
  vary one mechanism at a time.

Both recurrent branches share one QKV trunk (no duplicated projections);
each has its own output proj. (iii) exact sliding-window attention
(reused from P1) covers local induction. SwiGLU closes the block.

State per layer (batch 1): H*d_k*d_v (accumulator A, zeros when
disabled) + H*d_k*d_v (selective S) + 2*W*d_win (window KV). No
factor of T.
Reference kernel: forward_recurrent applies step() token-by-token; chunk
groups loop iterations only and has no mathematical effect.
"""

import torch
import torch.nn as nn

from .common import RMSNorm, SwiGLU
from .p1_delta_hybrid import SlidingWindowAttn
from .p1_delta_hybrid import BETA_MAX, BETA_MIN, BETA_BIAS_INIT, ALPHA_BIAS_INIT


class DecoupledMemory(nn.Module):
    """Shared-QKV accumulator + selective dual-state memory."""

    def __init__(self, d_model: int, heads: int, d_k: int, d_v: int,
                 use_accumulator: bool = True, rescale_cap: float = 1e4):
        super().__init__()
        self.heads = heads
        self.d_k = d_k
        self.d_v = d_v
        self.use_accumulator = use_accumulator
        self.rescale_cap = float(rescale_cap)
        self.w_q = nn.Linear(d_model, heads * d_k, bias=False)
        self.w_k = nn.Linear(d_model, heads * d_k, bias=False)
        self.w_v = nn.Linear(d_model, heads * d_v, bias=False)
        self.w_o_acc = nn.Linear(heads * d_v, d_model, bias=False)
        self.w_o_sel = nn.Linear(heads * d_v, d_model, bias=False)
        self.k_norm = RMSNorm(d_k)
        self.w_beta_acc = nn.Linear(d_model, heads, bias=True)
        self.w_beta_sel = nn.Linear(d_model, heads, bias=True)
        self.w_alpha = nn.Linear(d_model, heads, bias=True)
        nn.init.constant_(self.w_beta_acc.bias, BETA_BIAS_INIT)
        nn.init.constant_(self.w_beta_sel.bias, BETA_BIAS_INIT)
        nn.init.constant_(self.w_alpha.bias, ALPHA_BIAS_INIT)

    def _split(self, x: torch.Tensor, d: int) -> torch.Tensor:
        return x.view(*x.shape[:-1], self.heads, d)

    def _normed_k(self, k: torch.Tensor) -> torch.Tensor:
        k = self.k_norm(k)
        return k / (k.norm(dim=-1, keepdim=True).clamp_min(1e-6))

    def init_state(self, batch: int, device, dtype):
        return {"A": torch.zeros(batch, self.heads, self.d_k, self.d_v,
                                 device=device, dtype=dtype),
                "S": torch.zeros(batch, self.heads, self.d_k, self.d_v,
                                 device=device, dtype=dtype),
                "rescales": 0}

    def _guard(self, A: torch.Tensor, state: dict) -> torch.Tensor:
        # Norm-guard rescale hook: decay-free accumulation would otherwise
        # grow without bound on long streams. Rescale (not clip) preserves
        # the stored direction; the fire count is ledgered, never silent.
        # The scale is computed under no-grad but applied outside, so the
        # rescaled A keeps its autograd graph (a where() built inside
        # no-grad would detach trunk k/v/beta grads on every firing step).
        with torch.no_grad():
            n = A.norm(dim=(-2, -1), keepdim=True).clamp_min(1e-12)
            over = (n > self.rescale_cap)
            if bool(over.any()):
                state["rescales"] += int(over.sum().item())
                scale = torch.where(over, self.rescale_cap / n,
                                    torch.ones_like(n))
            else:
                return A
        return A * scale

    def step(self, x_t: torch.Tensor, state: dict):
        """x_t: (B, d). Returns (out (B, d), state). O(H*d_k*d_v)."""
        out, state, _q = self._step_core(x_t, state)
        return out, state

    def _step_core(self, x_t: torch.Tensor, state: dict):
        """Shared single-projection core: one w_q/w_k/w_v pass, returns (out, state, q)."""
        q = self._split(self.w_q(x_t), self.d_k)
        k = self._split(self.w_k(x_t), self.d_k)
        v = self._split(self.w_v(x_t), self.d_v)
        k = self._normed_k(k)
        beta_acc = torch.sigmoid(self.w_beta_acc(x_t)).clamp(BETA_MIN, BETA_MAX)
        beta_sel = torch.sigmoid(self.w_beta_sel(x_t)).clamp(BETA_MIN, BETA_MAX)
        alpha = torch.exp(-torch.exp(self.w_alpha(x_t)))
        if self.use_accumulator:
            A = state["A"] + beta_acc.view(-1, self.heads, 1, 1) * (
                k.unsqueeze(-1) * v.unsqueeze(-2))
            A = self._guard(A, state)
        else:
            A = state["A"]  # frozen zeros: A3 control removes the dynamics
        S = (alpha.view(-1, self.heads, 1, 1) * state["S"]
             + beta_sel.view(-1, self.heads, 1, 1) * (
                 k.unsqueeze(-1) * v.unsqueeze(-2)))
        state["A"], state["S"] = A, S
        o_acc = torch.einsum("bhki,bhk->bhi", A, q)
        o_sel = torch.einsum("bhki,bhk->bhi", S, q)
        out = (self.w_o_acc(o_acc.reshape(x_t.shape[0], -1))
               + self.w_o_sel(o_sel.reshape(x_t.shape[0], -1)))
        return out, state, q

    def step_split(self, x_t: torch.Tensor, state: dict):
        """Single-token update returning (recurrent_out, selective_out, state).

        selective_out is the selective-branch read from the post-step S
        with the current q; recurrent_out - selective_out is exactly the
        accumulator contribution (exact: both reads are linear in the
        post-step states, which evolve independently). Reuses the single
        w_q projection from the core (no doubled Q-proj cost)."""
        r_out, state, q = self._step_core(x_t, state)
        S = state["S"]
        o_sel = torch.einsum("bhki,bhk->bhi", S, q)
        s_out = self.w_o_sel(o_sel.reshape(x_t.shape[0], -1))
        return r_out, s_out, state

    def forward_recurrent(self, x: torch.Tensor, state: dict, chunk: int):
        """Sequential reference forward: applies step() token-by-token; chunk
        groups loop iterations only and has no mathematical effect (no
        parallel/chunkwise math, no fp32 cast)."""
        b, t, _ = x.shape
        outs = []
        for s in range(0, t, chunk):
            e = min(s + chunk, t)
            for i in range(s, e):
                o, state = self.step(x[:, i, :], state)
                outs.append(o)
        return torch.stack(outs, dim=1), state


class FusionGate3(nn.Module):
    """Input-dependent 3-way blend over (accumulator, selective, window)."""

    def __init__(self, d_model: int):
        super().__init__()
        self.proj = nn.Linear(d_model, 3, bias=True)

    def forward(self, x: torch.Tensor, a: torch.Tensor,
                b: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        w = torch.softmax(self.proj(x), dim=-1)
        return (w[..., 0:1] * a + w[..., 1:2] * b + w[..., 2:3] * c)


class P3Block(nn.Module):
    def __init__(self, d_model: int, heads: int, d_k: int, d_v: int,
                 win_heads: int, win_hd: int, window: int, mlp_hid: int,
                 chunk: int, rope_base: float = 10000.0,
                 use_accumulator: bool = True):
        super().__init__()
        if chunk < 1:
            raise ValueError(f"chunk must be >= 1, got {chunk!r}")
        self.n1 = RMSNorm(d_model)
        self.n2 = RMSNorm(d_model)
        self.mem = DecoupledMemory(d_model, heads, d_k, d_v,
                                   use_accumulator=use_accumulator)
        self.window = SlidingWindowAttn(d_model, win_heads, win_hd, window,
                                        rope_base)
        self.fusion = FusionGate3(d_model)
        self.mlp = SwiGLU(d_model, mlp_hid)
        self.chunk = chunk

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.n1(x)
        # Single-pass split loop: per-token (recurrent, selective) pairs
        # from one trajectory (states A/S evolve independently, so the
        # accumulator contribution r - s is exact, no shadow pass).
        st = self.mem.init_state(h.shape[0], x.device, x.dtype)
        r_seq, s_seq = [], []
        for s in range(0, h.shape[1], self.chunk):
            e = min(s + self.chunk, h.shape[1])
            for i in range(s, e):
                r, sv, st = self.mem.step_split(h[:, i, :], st)
                r_seq.append(r)
                s_seq.append(sv)
        r_out = torch.stack(r_seq, dim=1)
        s_out = torch.stack(s_seq, dim=1)
        w_out = self.window(h)
        a_out = r_out - s_out  # accumulator contribution by difference
        x = x + self.fusion(h, a_out, s_out, w_out)
        return x + self.mlp(self.n2(x))

    def init_state(self, batch: int, device, dtype):
        return {"mem": self.mem.init_state(batch, device, dtype),
                "win": self.window.init_state(batch, device, dtype)}

    def step(self, x_t: torch.Tensor, state: dict):
        """Single-token update; x_t is (B, d). State is O(1) in T."""
        h = self.n1(x_t)
        r_out, s_out, _ = self.mem.step_split(h, state["mem"])
        w_out, _ = self.window.step(h, state["win"])
        a_out = r_out - s_out
        y = x_t + self.fusion(h, a_out, s_out, w_out)
        return y + self.mlp(self.n2(y)), state

    def state_size(self, bpe: int = 4) -> int:
        H, dk, dv = self.mem.heads, self.mem.d_k, self.mem.d_v
        W, wd = self.window.window, self.window.wd
        win = 2 * W * wd * bpe if W > 0 else 0
        # A stays resident (zeros when use_accumulator=False), so the
        # inventory always counts both A and S.
        return 2 * H * dk * dv * bpe + win


class P3LM(nn.Module):
    def __init__(self, config: dict):
        super().__init__()
        if config.get("tie_embeddings", False):
            raise ValueError("tie_embeddings is baseline-only: P3 always "
                             "builds a separate lm_head")
        self.cfg = dict(config)
        d = config["d_model"]
        self.tok_embed = nn.Embedding(config["vocab_size"], d)
        self.blocks = nn.ModuleList(
            [P3Block(d, config["heads"], config["d_k"], config["d_v"],
                     config["win_heads"], config["win_hd"], config["window"],
                     config["mlp_hid"], config["chunk"],
                     config.get("rope_base", 10000.0),
                     config.get("use_accumulator", True))
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

    def state_bytes(self, batch: int, length: int, bpe: int = 4) -> int:
        # O(1) in length by construction; length accepted for API parity.
        return batch * sum(b.state_size(bpe) for b in self.blocks)
