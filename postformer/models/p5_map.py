"""P5 higher-order feature-map baseline (ablation control, not a contender).

Gated linear attention with a parameter-free degree-2 polynomial map
  phi(k) = [k ; s * k^2]  (dim 2*d_k, s = 0.5)
and a SCALED ADDITIVE write (A1 counterpart to the P1 delta erase):
  S_t = alpha_t * S_{t-1} + beta_t * phi(k_t) v_t^T.
Projection shapes are identical to P1, so T2 param parity holds by
construction; A1 varies the write rule (erase vs additive); NOTE q/k
are both unit-normed here (differs from P1 raw-q, RMSNorm-only k), so
query scale differs via the degree-2 map - see docs/envelope-audit.md.
Same W-window branch, fusion, and SwiGLU shell as P1.
"""

import torch
import torch.nn as nn

from .common import RMSNorm
from .p1_delta_hybrid import P1Block
from .p1_delta_hybrid import BETA_MAX, BETA_MIN, BETA_BIAS_INIT, ALPHA_BIAS_INIT

MAP_SCALE = 0.5


def poly_map(k: torch.Tensor) -> torch.Tensor:
    """(..., H, d_k) -> (..., H, 2*d_k) degree-2 feature map, parameter-free."""
    return torch.cat([k, MAP_SCALE * k * k], dim=-1)


class GatedMapMemory(nn.Module):
    def __init__(self, d_model: int, heads: int, d_k: int, d_v: int):
        super().__init__()
        self.heads = heads
        self.d_k = d_k
        self.d_v = d_v
        self.d_phi = 2 * d_k
        self.w_q = nn.Linear(d_model, heads * d_k, bias=False)
        self.w_k = nn.Linear(d_model, heads * d_k, bias=False)
        self.w_v = nn.Linear(d_model, heads * d_v, bias=False)
        self.w_o = nn.Linear(heads * d_v, d_model, bias=False)
        self.k_norm = RMSNorm(d_k)
        self.w_beta = nn.Linear(d_model, heads, bias=True)
        self.w_alpha = nn.Linear(d_model, heads, bias=True)
        nn.init.constant_(self.w_beta.bias, BETA_BIAS_INIT)
        nn.init.constant_(self.w_alpha.bias, ALPHA_BIAS_INIT)

    def _split(self, x: torch.Tensor, d: int) -> torch.Tensor:
        return x.view(*x.shape[:-1], self.heads, d)

    def init_state(self, batch: int, device, dtype):
        return torch.zeros(batch, self.heads, self.d_phi, self.d_v,
                           device=device, dtype=dtype)

    def _normed_k(self, k: torch.Tensor) -> torch.Tensor:
        k = self.k_norm(k)
        return k / (k.norm(dim=-1, keepdim=True).clamp_min(1e-6))

    def step(self, x_t: torch.Tensor, S: torch.Tensor):
        q = self._split(self.w_q(x_t), self.d_k)
        k = self._split(self.w_k(x_t), self.d_k)
        v = self._split(self.w_v(x_t), self.d_v)
        q = self._normed_k(q)
        k = self._normed_k(k)
        beta = torch.sigmoid(self.w_beta(x_t)).clamp(BETA_MIN, BETA_MAX)
        alpha = torch.exp(-torch.exp(self.w_alpha(x_t)))
        pq, pk = poly_map(q), poly_map(k)
        S = (alpha.view(-1, self.heads, 1, 1) * S
             + beta.view(-1, self.heads, 1, 1) * (pk.unsqueeze(-1) * v.unsqueeze(-2)))
        o = torch.einsum("bhki,bhk->bhi", S, pq)
        return self.w_o(o.reshape(x_t.shape[0], -1)), S

    def forward_recurrent(self, x: torch.Tensor, S0: torch.Tensor, chunk: int):
        """Sequential reference forward: applies step() token-by-token; chunk
        groups loop iterations only and has no mathematical effect (no
        parallel/chunkwise math, no fp32 cast)."""
        b, t, _ = x.shape
        S = S0
        outs = []
        for s in range(0, t, chunk):
            e = min(s + chunk, t)
            for i in range(s, e):
                o, S = self.step(x[:, i, :], S)
                outs.append(o)
        return torch.stack(outs, dim=1), S


class P5Block(P1Block):
    """P1 shell with the delta memory swapped for the additive map memory."""

    def __init__(self, d_model: int, heads: int, d_k: int, d_v: int,
                 win_heads: int, win_hd: int, window: int, mlp_hid: int,
                 chunk: int, rope_base: float = 10000.0):
        super().__init__(d_model, heads, d_k, d_v, win_heads, win_hd,
                         window, mlp_hid, chunk, rope_base)
        self.delta = GatedMapMemory(d_model, heads, d_k, d_v)

    def state_size(self, bpe: int = 4) -> int:
        H, dp, dv = self.delta.heads, self.delta.d_phi, self.delta.d_v
        W, wd = self.window.window, self.window.wd
        win = 2 * W * wd * bpe if W > 0 else 0
        return H * dp * dv * bpe + win


class P5LM(nn.Module):
    def __init__(self, config: dict):
        super().__init__()
        if config.get("tie_embeddings", False):
            raise ValueError("tie_embeddings is baseline-only: P5 always "
                             "builds a separate lm_head")
        self.cfg = dict(config)
        d = config["d_model"]
        self.tok_embed = nn.Embedding(config["vocab_size"], d)
        self.blocks = nn.ModuleList(
            [P5Block(d, config["heads"], config["d_k"], config["d_v"],
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
        return batch * sum(b.state_size(bpe) for b in self.blocks)
