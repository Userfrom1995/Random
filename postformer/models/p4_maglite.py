"""P4 MAG-lite: surprise-gated fast-weight memory + exact window (M4 proposal).

Per block: (i) a surprise-gated delta memory

  r_t   = M_{t-1}^T k_t                       (retrieve)
  e_t   = v_t - r_t                           (reconstruction error)
  s_t   = sigmoid(w_s(x_t) + 0.25 * g * ||e_t||)  (surprise gate, per head)
  eta_t = beta_t * s_t                        (one gradient-step size)
  M_t   = alpha_t * (M_{t-1} + eta_t * k_t e_t^T)

with k RMSNormed to unit norm, beta = sigmoid clamped to [0.01, 0.99]
(bias init -2.0, start retentive), alpha = exp(-exp(.)) init ~0.97,
surprise = sigmoid clamped to [0.01, 0.99], eta = beta * surprise
in [0.0001, 0.9801],
and a small learned error-gain g (init 0.5, per head) mapping the
reconstruction-error norm into extra write strength (scaled by
surprise_scale = 0.25, so the effective init gain is 0.125). When the memory
already predicts v_t (small ||e_t||), s_t falls back to the input gate
and the write is small; when the prediction fails (large ||e_t||),
the write strengthens - a single associative-reconstruction gradient
step with surprise modulation (Titans MAG-lite family, honest
single-step reference kernel, no multi-step inner loop).

(ii) the exact sliding-window branch reused from P1 (local induction);
(iii) a learned 2-way fusion gate; (iv) SwiGLU.

H4 verdict rule (blueprint): P4 earns its keep only if it ties P1 on
MQAR N=64 while beating P1 on the 8x length-drift delta; if P4 trails
P1 on MQAR N=64 by more than 10 points at matched budget, the
gradient-compression fidelity hypothesis is recorded as rejected.

State per layer (batch 1): H*d_k*d_v (fast weights M) + 2*W*d_win
(window KV). No factor of T.
Reference kernel: forward_recurrent applies step() token-by-token;
chunk groups loop iterations only and has no mathematical effect.
"""

import torch
import torch.nn as nn

from .common import RMSNorm, SwiGLU
from .p1_delta_hybrid import FusionGate, SlidingWindowAttn
from .p1_delta_hybrid import BETA_MAX, BETA_MIN, BETA_BIAS_INIT, ALPHA_BIAS_INIT


class SurpriseDeltaMemory(nn.Module):
    """Fast-weight memory with surprise-modulated write strength."""

    def __init__(self, d_model: int, heads: int, d_k: int, d_v: int,
                 err_gain_init: float = 0.5):
        super().__init__()
        self.heads = heads
        self.d_k = d_k
        self.d_v = d_v
        self.w_q = nn.Linear(d_model, heads * d_k, bias=False)
        self.w_k = nn.Linear(d_model, heads * d_k, bias=False)
        self.w_v = nn.Linear(d_model, heads * d_v, bias=False)
        self.w_o = nn.Linear(heads * d_v, d_model, bias=False)
        self.k_norm = RMSNorm(d_k)
        self.w_beta = nn.Linear(d_model, heads, bias=True)
        self.w_alpha = nn.Linear(d_model, heads, bias=True)
        self.w_surprise = nn.Linear(d_model, heads, bias=True)
        # Per-head error gain: maps ||e|| into extra surprise logits.
        self.err_gain = nn.Parameter(torch.full((heads,), float(err_gain_init)))
        self.surprise_scale = 0.25
        nn.init.constant_(self.w_beta.bias, BETA_BIAS_INIT)
        nn.init.constant_(self.w_alpha.bias, ALPHA_BIAS_INIT)
        nn.init.zeros_(self.w_surprise.bias)

    def _split(self, x: torch.Tensor, d: int) -> torch.Tensor:
        return x.view(*x.shape[:-1], self.heads, d)

    def _normed_k(self, k: torch.Tensor) -> torch.Tensor:
        k = self.k_norm(k)
        return k / (k.norm(dim=-1, keepdim=True).clamp_min(1e-6))

    def gates(self, x: torch.Tensor):
        beta = torch.sigmoid(self.w_beta(x)).clamp(BETA_MIN, BETA_MAX)
        alpha = torch.exp(-torch.exp(self.w_alpha(x)))
        return beta, alpha

    def init_state(self, batch: int, device, dtype):
        return torch.zeros(batch, self.heads, self.d_k, self.d_v,
                           device=device, dtype=dtype)

    def step(self, x_t: torch.Tensor, M: torch.Tensor):
        """x_t: (B, d). Returns (out (B, d), M_new). O(H*d_k*d_v)."""
        q = self._split(self.w_q(x_t), self.d_k)
        k = self._split(self.w_k(x_t), self.d_k)
        v = self._split(self.w_v(x_t), self.d_v)
        k = self._normed_k(k)
        beta, alpha = self.gates(x_t)  # (B, H)
        r = torch.einsum("bhki,bhk->bhi", M, k)  # (B, H, dv)
        err = v - r  # (B, H, dv) reconstruction error
        err_norm = err.norm(dim=-1)  # (B, H)
        s_logit = (self.w_surprise(x_t)
                   + self.err_gain.view(1, -1) * err_norm * self.surprise_scale)
        surprise = torch.sigmoid(s_logit).clamp(0.01, 0.99)
        eta = beta * surprise
        M = alpha.view(-1, self.heads, 1, 1) * (
            M + eta.view(-1, self.heads, 1, 1)
            * (k.unsqueeze(-1) * err.unsqueeze(-2)))
        o = torch.einsum("bhki,bhk->bhi", M, q)
        return self.w_o(o.reshape(x_t.shape[0], -1)), M

    def forward_recurrent(self, x: torch.Tensor, M0: torch.Tensor, chunk: int):
        """Sequential reference forward: applies step() token-by-token; chunk
        groups loop iterations only and has no mathematical effect."""
        M = M0
        outs = []
        for s in range(0, x.shape[1], chunk):
            e = min(s + chunk, x.shape[1])
            for i in range(s, e):
                o, M = self.step(x[:, i, :], M)
                outs.append(o)
        return torch.stack(outs, dim=1), M


class P4Block(nn.Module):
    def __init__(self, d_model: int, heads: int, d_k: int, d_v: int,
                 win_heads: int, win_hd: int, window: int, mlp_hid: int,
                 chunk: int, rope_base: float = 10000.0):
        super().__init__()
        if chunk < 1:
            raise ValueError(f"chunk must be >= 1, got {chunk!r}")
        self.n1 = RMSNorm(d_model)
        self.n2 = RMSNorm(d_model)
        self.mem = SurpriseDeltaMemory(d_model, heads, d_k, d_v)
        self.window = SlidingWindowAttn(d_model, win_heads, win_hd, window,
                                        rope_base)
        self.fusion = FusionGate(d_model)
        self.mlp = SwiGLU(d_model, mlp_hid)
        self.chunk = chunk

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.n1(x)
        b, t, _ = x.shape
        M = self.mem.init_state(b, x.device, x.dtype)
        m_out, _ = self.mem.forward_recurrent(h, M, self.chunk)
        w_out = self.window(h)
        x = x + self.fusion(h, m_out, w_out)
        return x + self.mlp(self.n2(x))

    def init_state(self, batch: int, device, dtype):
        return {"M": self.mem.init_state(batch, device, dtype),
                "win": self.window.init_state(batch, device, dtype)}

    def step(self, x_t: torch.Tensor, state: dict):
        """Single-token update; x_t is (B, d). State is O(1) in T."""
        h = self.n1(x_t)
        m_out, state["M"] = self.mem.step(h, state["M"])
        w_out, _ = self.window.step(h, state["win"])
        y = x_t + self.fusion(h, m_out, w_out)
        return y + self.mlp(self.n2(y)), state

    def state_size(self, bpe: int = 4) -> int:
        H, dk, dv = self.mem.heads, self.mem.d_k, self.mem.d_v
        W, wd = self.window.window, self.window.wd
        win = 2 * W * wd * bpe if W > 0 else 0
        return H * dk * dv * bpe + win


class P4LM(nn.Module):
    def __init__(self, config: dict):
        super().__init__()
        if config.get("tie_embeddings", False):
            raise ValueError("tie_embeddings is baseline-only: P4 always "
                             "builds a separate lm_head")
        self.cfg = dict(config)
        d = config["d_model"]
        self.tok_embed = nn.Embedding(config["vocab_size"], d)
        self.blocks = nn.ModuleList(
            [P4Block(d, config["heads"], config["d_k"], config["d_v"],
                     config["win_heads"], config["win_hd"], config["window"],
                     config["mlp_hid"], config["chunk"],
                     config.get("rope_base", 10000.0))
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
