"""P1 Gated DeltaNet + sliding-window hybrid (Delta-Hybrid, top-ranked proposal).

Per layer: (i) gated delta-rule fast-weight memory
  S_t = alpha_t * (S_{t-1} + beta_t * k_t (v_t - r_t)^T),  r_t = S_{t-1}^T k_t,
with k RMSNormed to unit norm, beta = sigmoid clamped to [0.01, 0.99]
(bias init -2.0, start retentive), alpha = exp(-exp(.)) init ~0.97;
(ii) exact sliding-window attention (W = 128) for local induction;
(iii) learned per-token fusion gate; (iv) SwiGLU.

State per layer (batch 1): H*d_k*d_v (delta S) + 2*W*d_win (window KV) +
H scalars. No factor of T. Reference kernels: forward_chunk loops in chunks
of C (fp32 inter-chunk state); step() is the single-token form.
"""

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

from .common import KVWindowBuffer, RMSNorm, RotaryEmbedding, SwiGLU

BETA_MIN, BETA_MAX = 0.01, 0.99
BETA_BIAS_INIT = -2.0
ALPHA_BIAS_INIT = -3.5  # exp(-exp(-3.5)) ~= 0.97


class GatedDeltaMemory(nn.Module):
    """Multi-head key-structured fast-weight memory with shared beta/alpha projs."""

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
        self.w_beta = nn.Linear(d_model, heads, bias=True)
        self.w_alpha = nn.Linear(d_model, heads, bias=True)
        nn.init.constant_(self.w_beta.bias, BETA_BIAS_INIT)
        nn.init.constant_(self.w_alpha.bias, ALPHA_BIAS_INIT)

    def gates(self, x: torch.Tensor):
        beta = torch.sigmoid(self.w_beta(x)).clamp(BETA_MIN, BETA_MAX)
        alpha = torch.exp(-torch.exp(self.w_alpha(x)))
        return beta, alpha  # (..., H)

    def _normed_k(self, k: torch.Tensor) -> torch.Tensor:
        k = self.k_norm(k)
        return k / (k.norm(dim=-1, keepdim=True).clamp_min(1e-6))  # unit norm per head

    def _split(self, x: torch.Tensor, d: int) -> torch.Tensor:
        # (..., H*d) -> (..., H, d)
        return x.view(*x.shape[:-1], self.heads, d)

    def init_state(self, batch: int, device, dtype):
        return torch.zeros(batch, self.heads, self.d_k, self.d_v, device=device, dtype=dtype)

    def step(self, x_t: torch.Tensor, S: torch.Tensor):
        """x_t: (B, d). Returns (out (B, H*dv), S_new). O(H*d_k*d_v), no scan."""
        q = self._split(self.w_q(x_t), self.d_k)
        k = self._split(self.w_k(x_t), self.d_k)
        v = self._split(self.w_v(x_t), self.d_v)
        k = self._normed_k(k)
        beta, alpha = self.gates(x_t)  # (B, H)
        r = torch.einsum("bhki,bhk->bhi", S, k)          # retrieve (B,H,dv)
        err = (v - r).unsqueeze(-2)                       # (B,H,1,dv)
        kk = k.unsqueeze(-1)                              # (B,H,dk,1)
        S = alpha.view(-1, self.heads, 1, 1) * (
            S + beta.view(-1, self.heads, 1, 1) * (kk * err))
        o = torch.einsum("bhki,bhk->bhi", S, q)
        return self.w_o(o.reshape(x_t.shape[0], -1)), S

    def forward_chunk(self, x: torch.Tensor, S0: torch.Tensor, chunk: int):
        """Reference chunked forward: same math as step(), grouped in chunks of C."""
        b, t, _ = x.shape
        S = S0
        outs = []
        for s in range(0, t, chunk):
            e = min(s + chunk, t)
            for i in range(s, e):
                o, S = self.step(x[:, i, :], S)
                outs.append(o)
        return torch.stack(outs, dim=1), S


class SlidingWindowAttn(nn.Module):
    """Exact causal attention over the last W keys. O(W*d) per step."""

    def __init__(self, d_model: int, heads: int, head_dim: int, window: int,
                 rope_base: float = 10000.0):
        super().__init__()
        self.heads = heads
        self.hd = head_dim
        self.window = window
        self.wd = heads * head_dim
        self.qkv = nn.Linear(d_model, 3 * self.wd, bias=False)
        self.proj = nn.Linear(self.wd, d_model, bias=False)
        self.rope = RotaryEmbedding(head_dim, base=rope_base)

    def _split(self, x: torch.Tensor):
        return x.view(*x.shape[:-1], self.heads, self.hd).transpose(-3, -2)
        # (..., H, L, hd)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        b, t, _ = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)
        q, k, v = self._split(q), self._split(k), self._split(v)
        cos, sin = self.rope.cos_sin(t, x.device, x.dtype)
        q = RotaryEmbedding.apply(q, cos, sin)
        k = RotaryEmbedding.apply(k, cos, sin)
        scores = q @ k.transpose(-2, -1) / math.sqrt(self.hd)
        causal = torch.triu(torch.ones(t, t, dtype=torch.bool, device=x.device), 1)
        local = (torch.arange(t, device=x.device).unsqueeze(1)
                 - torch.arange(t, device=x.device).unsqueeze(0)) >= self.window
        scores = scores.masked_fill((causal | local).unsqueeze(0).unsqueeze(0), float("-inf"))
        y = (torch.softmax(scores, dim=-1) @ v).transpose(-3, -2).reshape(b, t, self.wd)
        return self.proj(y)

    def init_state(self, batch: int, device, dtype):
        return {"k": KVWindowBuffer(batch, self.window, self.wd, device, dtype),
                "pos": 0}

    def step(self, x_t: torch.Tensor, state: dict):
        b = x_t.shape[0]
        q, k, v = self.qkv(x_t).chunk(3, dim=-1)
        pos = state["pos"]
        cos, sin = self.rope.cos_sin(pos + 1, x_t.device, x_t.dtype)
        # RoPE per head (must match forward()'s per-head rotation exactly).
        q = RotaryEmbedding.apply(
            q.view(b, self.heads, self.hd).unsqueeze(2),
            cos[pos:pos + 1], sin[pos:pos + 1]).squeeze(2).reshape(b, self.wd)
        k = RotaryEmbedding.apply(
            k.view(b, self.heads, self.hd).unsqueeze(2),
            cos[pos:pos + 1], sin[pos:pos + 1]).squeeze(2).reshape(b, self.wd)
        state["k"].append(k, v)
        state["pos"] = pos + 1
        kk, vv = state["k"].get()  # (B, m, wd)
        kk = kk.view(b, -1, self.heads, self.hd).transpose(1, 2)
        vv = vv.view(b, -1, self.heads, self.hd).transpose(1, 2)
        qq = q.view(b, 1, self.heads, self.hd).transpose(1, 2)
        scores = (qq @ kk.transpose(-2, -1)) / math.sqrt(self.hd)
        y = (torch.softmax(scores, dim=-1) @ vv).transpose(1, 2).reshape(b, self.wd)
        return self.proj(y), state


class FusionGate(nn.Module):
    def __init__(self, d_model: int):
        super().__init__()
        self.proj = nn.Linear(d_model, 2, bias=True)

    def forward(self, x: torch.Tensor, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        w = torch.softmax(self.proj(x), dim=-1)
        return w[..., 0:1] * a + w[..., 1:2] * b


class P1Block(nn.Module):
    def __init__(self, d_model: int, heads: int, d_k: int, d_v: int,
                 win_heads: int, win_hd: int, window: int, mlp_hid: int,
                 chunk: int, rope_base: float = 10000.0):
        super().__init__()
        self.n1 = RMSNorm(d_model)
        self.n2 = RMSNorm(d_model)
        self.delta = GatedDeltaMemory(d_model, heads, d_k, d_v)
        self.window = SlidingWindowAttn(d_model, win_heads, win_hd, window, rope_base)
        self.fusion = FusionGate(d_model)
        self.mlp = SwiGLU(d_model, mlp_hid)
        self.chunk = chunk

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.n1(x)
        b, t, _ = x.shape
        S = self.delta.init_state(b, x.device, x.dtype)
        d_out, _ = self.delta.forward_chunk(h, S, self.chunk)
        w_out = self.window(h)
        x = x + self.fusion(h, d_out, w_out)
        return x + self.mlp(self.n2(x))

    def init_state(self, batch: int, device, dtype):
        return {"S": self.delta.init_state(batch, device, dtype),
                "win": self.window.init_state(batch, device, dtype)}

    def step(self, x_t: torch.Tensor, state: dict):
        """Single-token update; x_t is (B, d). State is O(1) in T."""
        h = self.n1(x_t)
        d_out, state["S"] = self.delta.step(h, state["S"])
        w_out, _ = self.window.step(h, state["win"])
        y = x_t + self.fusion(h, d_out, w_out)
        return y + self.mlp(self.n2(y)), state

    def state_size(self, bpe: int = 4) -> int:
        H, dk, dv = self.delta.heads, self.delta.d_k, self.delta.d_v
        W, wd = self.window.window, self.window.wd
        return H * dk * dv * bpe + 2 * W * wd * bpe + H * bpe


class P1LM(nn.Module):
    def __init__(self, config: dict):
        super().__init__()
        self.cfg = dict(config)
        d = config["d_model"]
        self.tok_embed = nn.Embedding(config["vocab_size"], d)
        self.blocks = nn.ModuleList(
            [P1Block(d, config["heads"], config["d_k"], config["d_v"],
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

    def state_bytes(self, batch: int, length: int = 0, bpe: int = 4) -> int:
        # O(1) in length by construction; length accepted for API parity.
        return batch * sum(b.state_size(bpe) for b in self.blocks)
