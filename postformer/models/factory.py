"""Model factory: build_model(name, scale, overrides) -> (model, config).

Names: transformer | p1 | p2 | p3 | p4 | p5  x  toy | tiny | small,
e.g. "p1-tiny". Pinned configs (non-embedding params; MLP hid trimmed so
each candidate lands within +-2% of its baseline arm - verified by
tests/test_params.py):

  transformer-tiny: 6L d512 8h mlp2048            (reference, 29366784, ~29.37M)
  p1/p5-tiny:       6L d512 4xh(dk128,dv128) W128 C64  win 4x64 mlp1704
  p2-tiny:          6L d512 4xh(dk128,dv128) W128 C64  win 4x64 mlp1704 G16
  p3-tiny:          6L d512 4xh(dk128,dv128) W128 C64  win 4x64 mlp1532
  p4-tiny:          6L d512 4xh(dk128,dv128) W128 C64  win 4x64 mlp1702
  transformer-small: 12L d768 12h mlp3072        (reference, 113462016, ~113.46M)
  p1/p5-small:      12L d768 6xh(dk128,dv128) W128 C128 win 4x64 mlp2726
  p2-small:         12L d768 6xh(dk128,dv128) W128 C128 win 4x64 mlp2726 G16
  p3-small:         12L d768 6xh(dk128,dv128) W128 C128 win 4x64 mlp2468
  p4-small:         12L d768 6xh(dk128,dv128) W128 C128 win 4x64 mlp2724

P2's stride router is parameter-free, so it shares P1's MLP hid; P3's
second output proj plus third gate proj costs one hid step (toy 274,
tiny 1532, small 2468 - measured, not estimated). P4 adds one
surprise proj (d_model x H) plus a per-head error gain (H params) over
P1, compensated by trimming 2 hid units (measured, see test_params.py).

tie_embeddings is baseline-only: P1/P2/P3/P4/P5 always build a separate
lm_head, so passing tie_embeddings for them is rejected to protect
param parity.
"""

from . import baseline as _b
from .common import param_count_no_embed
from .p1_delta_hybrid import P1LM
from .p2_slots import P2LM
from .p3_decoupled import P3LM
from .p4_maglite import P4LM
from .p5_map import P5LM


def _trunk_cfg(scale: str) -> dict:
    """Shared trunk dims (heads/state/window) for all recurrent candidates."""
    if scale == "toy":
        # CPU-trainable proxy (M2 falsification only): 2L d128, 2 delta heads
        # dk32/dv32, W16, C16, win 2x16 (-0.13% vs transformer-toy for P1/P5).
        return {"layers": 2, "d_model": 128, "heads": 2, "d_k": 32, "d_v": 32,
                "win_heads": 2, "win_hd": 16, "window": 16,
                "chunk": 16, "rope_base": 10000.0, "vocab_size": 66}
    if scale == "tiny":
        return {"layers": 6, "d_model": 512, "heads": 4, "d_k": 128, "d_v": 128,
                "win_heads": 4, "win_hd": 64, "window": 128,
                "chunk": 64, "rope_base": 10000.0, "vocab_size": 8192}
    if scale == "small":
        return {"layers": 12, "d_model": 768, "heads": 6, "d_k": 128, "d_v": 128,
                "win_heads": 4, "win_hd": 64, "window": 128,
                "chunk": 128, "rope_base": 10000.0, "vocab_size": 256}
    raise ValueError(f"unknown scale {scale!r}")


_MLP_HID = {
    # (family, scale) -> mlp_hid pin (measured parity, see test_params.py)
    ("p1", "toy"): 296, ("p1", "tiny"): 1704, ("p1", "small"): 2726,
    ("p5", "toy"): 296, ("p5", "tiny"): 1704, ("p5", "small"): 2726,
    ("p2", "toy"): 296, ("p2", "tiny"): 1704, ("p2", "small"): 2726,
    ("p3", "toy"): 274, ("p3", "tiny"): 1532, ("p3", "small"): 2468,
    ("p4", "toy"): 294, ("p4", "tiny"): 1702, ("p4", "small"): 2724,
}

_FAMILY_DEFAULTS = {
    # Per-family extra config keys beyond the trunk + mlp_hid.
    "p2": {"slots": 16, "slot_stride": 8},
    "p3": {"use_accumulator": True},
}


def _p1_cfg(scale: str) -> dict:
    cfg = _trunk_cfg(scale)
    cfg["mlp_hid"] = _MLP_HID[("p1", scale)]
    return cfg


def _candidate_cfg(family: str, scale: str) -> dict:
    if family not in ("p1", "p2", "p3", "p4", "p5"):
        raise ValueError(f"unknown candidate family {family!r}")
    cfg = _trunk_cfg(scale)
    cfg["mlp_hid"] = _MLP_HID[(family, scale)]
    cfg.update(_FAMILY_DEFAULTS.get(family, {}))
    return cfg


def build_model(name: str, scale: str, overrides: dict | None = None):
    family = name.split("-", 1)[0]
    if family == "transformer":
        cfg = dict(_b.SCALES[scale])
    elif family in ("p1", "p2", "p3", "p4", "p5"):
        cfg = _candidate_cfg(family, scale)
    else:
        raise ValueError(f"unknown family {family!r} in {name!r}")
    if overrides:
        if family in ("p1", "p2", "p3", "p4", "p5") and overrides.get("tie_embeddings"):
            raise ValueError("tie_embeddings is baseline-only: P1/P2/P3/P4/P5 always "
                             "build a separate lm_head; allowing the override "
                             "would silently break param parity")
        cfg.update({k: v for k, v in overrides.items() if v is not None})
    if family == "transformer":
        model = _b.DecoderLM(cfg)
    elif family == "p1":
        model = P1LM(cfg)
    elif family == "p2":
        model = P2LM(cfg)
    elif family == "p3":
        model = P3LM(cfg)
    elif family == "p4":
        model = P4LM(cfg)
    else:
        model = P5LM(cfg)
    return model, cfg


def count_params(name: str, scale: str, overrides: dict | None = None) -> tuple[int, dict]:
    import torch

    model, cfg = build_model(name, scale, overrides)
    with torch.no_grad():
        n = param_count_no_embed(model)
    return n, cfg
