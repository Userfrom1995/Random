"""Model factory: build_model(name, scale, overrides) -> (model, config).

Names: transformer | p1 | p5  x  toy | tiny | small, e.g. "p1-tiny".
Pinned configs (non-embedding params; MLP hid trimmed so each candidate
lands within +-2% of its baseline arm - verified by tests/test_params.py):

  transformer-tiny: 6L d512 8h mlp2048            (reference, 29366784, ~29.37M)
  p1/p5-tiny:       6L d512 4xh(dk128,dv128) W128 C64  win 4x64 mlp1704
  transformer-small: 12L d768 12h mlp3072        (reference, 113462016, ~113.46M)
  p1/p5-small:      12L d768 6xh(dk128,dv128) W128 C128 win 4x64 mlp2726

tie_embeddings is baseline-only: P1/P5 always build a separate lm_head, so
passing tie_embeddings for p1/p5 is rejected to protect param parity.
"""

from . import baseline as _b
from .common import param_count_no_embed
from .p1_delta_hybrid import P1LM
from .p5_map import P5LM


def _p1_cfg(scale: str) -> dict:
    if scale == "toy":
        # CPU-trainable proxy (M2 falsification only): 2L d128, 2 delta heads
        # dk32/dv32, W16, C16, win 2x16, mlp296 (-0.13% vs transformer-toy).
        return {"layers": 2, "d_model": 128, "heads": 2, "d_k": 32, "d_v": 32,
                "win_heads": 2, "win_hd": 16, "window": 16, "mlp_hid": 296,
                "chunk": 16, "rope_base": 10000.0, "vocab_size": 66}
    if scale == "tiny":
        return {"layers": 6, "d_model": 512, "heads": 4, "d_k": 128, "d_v": 128,
                "win_heads": 4, "win_hd": 64, "window": 128, "mlp_hid": 1704,
                "chunk": 64, "rope_base": 10000.0, "vocab_size": 8192}
    if scale == "small":
        return {"layers": 12, "d_model": 768, "heads": 6, "d_k": 128, "d_v": 128,
                "win_heads": 4, "win_hd": 64, "window": 128, "mlp_hid": 2726,
                "chunk": 128, "rope_base": 10000.0, "vocab_size": 256}
    raise ValueError(f"unknown scale {scale!r}")


def build_model(name: str, scale: str, overrides: dict | None = None):
    family = name.split("-", 1)[0]
    if family == "transformer":
        cfg = dict(_b.SCALES[scale])
    elif family == "p1":
        cfg = _p1_cfg(scale)
    elif family == "p5":
        cfg = _p1_cfg(scale)
    else:
        raise ValueError(f"unknown family {family!r} in {name!r}")
    if overrides:
        if family in ("p1", "p5") and overrides.get("tie_embeddings"):
            raise ValueError("tie_embeddings is baseline-only: P1/P5 always build "
                             "a separate lm_head; allowing the override would silently "
                             "break param parity")
        cfg.update({k: v for k, v in overrides.items() if v is not None})
    if family == "transformer":
        model = _b.DecoderLM(cfg)
    elif family == "p1":
        model = P1LM(cfg)
    else:
        model = P5LM(cfg)
    return model, cfg


def count_params(name: str, scale: str, overrides: dict | None = None) -> tuple[int, dict]:
    import torch

    model, cfg = build_model(name, scale, overrides)
    with torch.no_grad():
        n = param_count_no_embed(model)
    return n, cfg
