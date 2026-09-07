"""Causal decoder-only Transformer baseline (G4 control: KV cache is O(T*d)).

Pinned scales (non-embedding params = all but input tok_embed; output head counts):
  S-tiny : 6 layers, d_model 512, 8 heads, SwiGLU hid 2048  (29366784)
  S-small: 12 layers, d_model 768, 12 heads, SwiGLU hid 3072 (113462016)
Pre-norm RMSNorm, RoPE, no bias. Deterministic init via seed_all.
"""

import math

import torch
import torch.nn as nn

from .common import RMSNorm, RotaryEmbedding, SwiGLU, causal_mask

TINY = {"layers": 6, "d_model": 512, "heads": 8, "mlp_hid": 2048,
        "rope_base": 10000.0, "vocab_size": 8192, "tie_embeddings": False}
SMALL = {"layers": 12, "d_model": 768, "heads": 12, "mlp_hid": 3072,
         "rope_base": 10000.0, "vocab_size": 256, "tie_embeddings": False}

SCALES = {"tiny": TINY, "small": SMALL,
          # TOY: CPU-trainable proxy for M2 falsification (matched-budget MQAR
          # training on the runner; NOT a gate scale - S-tiny/S-small gates
          # remain binding). Pinned: 2L d128 4h mlp256.
          "toy": {"layers": 2, "d_model": 128, "heads": 4, "mlp_hid": 256,
                  "rope_base": 10000.0, "vocab_size": 66, "tie_embeddings": False}}


class TransformerBlock(nn.Module):
    def __init__(self, d_model: int, heads: int, mlp_hid: int, rope_base: float = 10000.0):
        super().__init__()
        assert d_model % heads == 0
        self.d_model = d_model
        self.heads = heads
        self.hd = d_model // heads
        self.n1 = RMSNorm(d_model)
        self.n2 = RMSNorm(d_model)
        self.qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.proj = nn.Linear(d_model, d_model, bias=False)
        self.mlp = SwiGLU(d_model, mlp_hid)
        self.rope = RotaryEmbedding(self.hd, base=rope_base)

    def _split(self, x: torch.Tensor) -> torch.Tensor:
        # (B, L, d) -> (B, H, L, hd)
        b, l, _ = x.shape
        return x.view(b, l, self.heads, self.hd).transpose(1, 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.n1(x)
        q, k, v = self.qkv(h).chunk(3, dim=-1)
        q, k, v = self._split(q), self._split(k), self._split(v)
        cos, sin = self.rope.cos_sin(x.shape[1], x.device, x.dtype)
        q = RotaryEmbedding.apply(q, cos, sin)
        k = RotaryEmbedding.apply(k, cos, sin)
        attn = torch.softmax(
            q @ k.transpose(-2, -1) / math.sqrt(self.hd)
            + causal_mask(x.shape[1], x.device).float().masked_fill(
                causal_mask(x.shape[1], x.device), float("-inf")).unsqueeze(0).unsqueeze(0),
            dim=-1)
        y = (attn @ v).transpose(1, 2).reshape(x.shape)
        x = x + self.proj(y)
        return x + self.mlp(self.n2(x))

    def init_state(self, batch: int, device, dtype):
        return {"k": [], "v": [], "pos": 0}

    def step(self, x_t: torch.Tensor, state: dict) -> tuple:
        """Single-token update; cache grows O(T*d) (the control that must grow)."""
        h = self.n1(x_t)
        q, k, v = self.qkv(h).chunk(3, dim=-1)
        q = q.view(-1, self.heads, self.hd)
        k = k.view(-1, self.heads, self.hd)
        v = v.view(-1, self.heads, self.hd)
        pos = state["pos"]
        cos, sin = self.rope.row(pos, x_t.device, x_t.dtype)
        q = RotaryEmbedding.apply(q.unsqueeze(2), cos, sin).squeeze(2)
        k = RotaryEmbedding.apply(k.unsqueeze(2), cos, sin).squeeze(2)
        state["k"].append(k.detach())
        state["v"].append(v.detach())
        state["pos"] = pos + 1
        kk = torch.stack(state["k"], dim=2)  # (B, H, T, hd), RoPE baked in at append
        vv = torch.stack(state["v"], dim=2)
        scores = (q.unsqueeze(2) @ kk.transpose(-2, -1)) / math.sqrt(self.hd)
        attn = torch.softmax(scores, dim=-1)
        y = (attn @ vv).reshape(x_t.shape[0], self.d_model)
        x_t = x_t + self.proj(y)
        return x_t + self.mlp(self.n2(x_t)), state

    def state_bytes(self, batch: int, length: int, bpe: int = 4) -> int:
        return 2 * batch * length * self.d_model * bpe


class DecoderLM(nn.Module):
    def __init__(self, config: dict):
        super().__init__()
        self.cfg = dict(config)
        d = config["d_model"]
        self.tok_embed = nn.Embedding(config["vocab_size"], d)
        self.blocks = nn.ModuleList(
            [TransformerBlock(d, config["heads"], config["mlp_hid"],
                              config.get("rope_base", 10000.0))
             for _ in range(config["layers"])])
        self.norm_f = RMSNorm(d)
        if config.get("tie_embeddings", False):
            self.lm_head = None
        else:
            self.lm_head = nn.Linear(d, config["vocab_size"], bias=False)

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        x = self.tok_embed(ids)
        for blk in self.blocks:
            x = blk(x)
        x = self.norm_f(x)
        return x @ self.tok_embed.weight.T if self.lm_head is None else self.lm_head(x)

    def init_state(self, batch: int, device, dtype):
        return [blk.init_state(batch, device, dtype) for blk in self.blocks]

    def step(self, tok: torch.Tensor, states: list) -> tuple:
        x = self.tok_embed(tok)[:, 0, :]
        for blk, st in zip(self.blocks, states):
            x, _ = blk.step(x, st)
        x = self.norm_f(x)
        logits = (x @ self.tok_embed.weight.T if self.lm_head is None
                  else self.lm_head(x))
        return logits.unsqueeze(1), states

    def state_bytes(self, batch: int, length: int, bpe: int = 4) -> int:
        return sum(b.state_bytes(batch, length, bpe) for b in self.blocks)


def build_decoder_lm(scale: str, overrides: dict | None = None) -> DecoderLM:
    cfg = dict(SCALES[scale])
    if overrides:
        cfg.update({k: v for k, v in overrides.items() if v is not None})
    return DecoderLM(cfg)
