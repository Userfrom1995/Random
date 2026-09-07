"""T1: chunked/forward vs recurrent step parity (rel err <= 1e-4, incl. C boundaries)."""

import torch

from postformer.models.common import seed_all
from postformer.models.factory import build_model
from .conftest import FAMILIES, MINI


def rel_err(a, b):
    return ((a - b).abs() / (1 + a.abs())).max().item()


def test_parity_random():
    seed_all(11, "t1")
    for fam in FAMILIES:
        m, _ = build_model(fam, "tiny", dict(MINI))
        m.eval()
        ids = torch.randint(0, MINI["vocab_size"], (2, 30))  # 30 > W=8, crosses C=4
        with torch.no_grad():
            full = m(ids)
            st = m.init_state(2, "cpu", torch.float32)
            outs = [m.step(ids[:, i:i + 1], st)[0] for i in range(30)]
        assert rel_err(full, torch.cat(outs, dim=1)) <= 1e-4, fam


def test_parity_collinear_keys():
    """Collinear (all-same-token) stress: erase path must stay finite and match."""
    seed_all(12, "t1-collinear")
    for fam in FAMILIES:
        m, _ = build_model(fam, "tiny", dict(MINI))
        m.eval()
        ids = torch.full((1, 20), 7, dtype=torch.long)
        with torch.no_grad():
            full = m(ids)
            assert torch.isfinite(full).all(), fam
            st = m.init_state(1, "cpu", torch.float32)
            outs = [m.step(ids[:, i:i + 1], st)[0] for i in range(20)]
        assert rel_err(full, torch.cat(outs, dim=1)) <= 1e-4, fam
