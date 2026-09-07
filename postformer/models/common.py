"""Shared domain primitives (torch only, no viewer/HTML imports, deterministic)."""

import hashlib
import random

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def seed_all(master: int, purpose: str = "default") -> int:
    """Seed random/numpy/torch (+cuda) from sha256(master/purpose). Returns subseed."""
    digest = hashlib.sha256(f"{master}/{purpose}".encode("utf-8")).digest()
    sub = int.from_bytes(digest[:8], "big") % (2**31 - 1)
    random.seed(sub)
    np.random.seed(sub % (2**32 - 1))
    torch.manual_seed(sub)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(sub)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    return sub


class RMSNorm(nn.Module):
    def __init__(self, d: int, eps: float = 1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(d))
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        var = x.float().pow(2).mean(dim=-1, keepdim=True)
        x = x.float() * torch.rsqrt(var + self.eps)
        return (self.weight.float() * x).to(x.dtype)


class SwiGLU(nn.Module):
    """SwiGLU MLP: down(silu(gate(x)) * up(x)). Params = 3 * d_in * d_hid."""

    def __init__(self, d_in: int, d_hid: int):
        super().__init__()
        self.gate = nn.Linear(d_in, d_hid, bias=False)
        self.up = nn.Linear(d_in, d_hid, bias=False)
        self.down = nn.Linear(d_hid, d_in, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.down(F.silu(self.gate(x)) * self.up(x))


class RotaryEmbedding(nn.Module):
    """RoPE with cached cos/sin; O(d) per token, no learned params."""

    def __init__(self, dim: int, base: float = 10000.0, max_len: int = 65536):
        super().__init__()
        inv = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv, persistent=False)
        self.max_len = max_len

    def cos_sin(self, seq_len: int, device, dtype):
        t = torch.arange(seq_len, device=device, dtype=torch.float32)
        freqs = torch.outer(t, self.inv_freq.to(device))
        emb = torch.cat([freqs, freqs], dim=-1)
        return emb.cos().to(dtype), emb.sin().to(dtype)

    def row(self, pos: int, device, dtype):
        """Single-position cos/sin row: O(d), identical values to cos_sin(pos+1)[pos].

        The recurrent step() path must use this (never the full table) so
        per-token latency stays O(1) in T (G4 flatness).
        """
        t = torch.tensor([float(pos)], device=device, dtype=torch.float32)
        freqs = torch.outer(t, self.inv_freq.to(device))
        emb = torch.cat([freqs, freqs], dim=-1)
        return emb.cos().to(dtype), emb.sin().to(dtype)

    @staticmethod
    def apply(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
        # x: (..., L, dim); cos/sin: (L, dim)
        half = x.shape[-1] // 2
        x1, x2 = x[..., :half], x[..., half:]
        c = cos[..., :half]
        s = sin[..., :half]
        return torch.cat([x1 * c - x2 * s, x1 * s + x2 * c], dim=-1)


class KVWindowBuffer:
    """Fixed-capacity ring buffer of (K, V) rows; state is O(B*W*d), never O(T*d)."""

    def __init__(self, batch: int, max_len: int, d: int, device, dtype):
        self.max_len = max_len
        self.buf_k = torch.zeros(batch, max_len, d, device=device, dtype=dtype)
        self.buf_v = torch.zeros(batch, max_len, d, device=device, dtype=dtype)
        self.n = 0  # total tokens ever appended (monotone clock for causality)

    def append(self, k: torch.Tensor, v: torch.Tensor) -> None:
        # k, v: (B, d) single-token rows. Keeps the most recent max_len rows.
        if self.n < self.max_len:
            self.buf_k[:, self.n, :] = k
            self.buf_v[:, self.n, :] = v
        else:
            self.buf_k[:, :-1, :] = self.buf_k[:, 1:, :].clone()
            self.buf_v[:, :-1, :] = self.buf_v[:, 1:, :].clone()
            self.buf_k[:, -1, :] = k
            self.buf_v[:, -1, :] = v
        self.n += 1

    def get(self):
        m = min(self.n, self.max_len)
        return self.buf_k[:, :m, :], self.buf_v[:, :m, :]

    def state_bytes(self) -> int:
        return self.buf_k.numel() * self.buf_k.element_size() + self.buf_v.numel() * self.buf_v.element_size()


def param_count_no_embed(model: nn.Module) -> int:
    """Binding counter: all params except token embedding (named '*tok_embed*')."""
    total = 0
    for name, p in model.named_parameters():
        if "tok_embed" in name:
            continue
        total += p.numel()
    return total


def causal_mask(length: int, device) -> torch.Tensor:
    """Boolean (L, L) mask, True where j > i (future) must be hidden."""
    return torch.triu(torch.ones(length, length, dtype=torch.bool, device=device), diagonal=1)
