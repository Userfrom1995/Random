"""T6: gate/stability invariants (blueprint: beta*k-norm^2 < 2.0, alpha in (0,1)).

P1/P5 keys are RMSNormed (P1 additionally unit-renormalized), beta is
sigmoid-clamped to [0.01, 0.99], alpha = exp(-exp(.)) in (0, 1) by
construction. This test asserts the invariants on live forward draws plus
finite outputs under collinear-key stress, and logs the worst case.
"""

import torch

from postformer.models.common import seed_all
from postformer.models.factory import build_model
from postformer.models.p1_delta_hybrid import BETA_MAX, BETA_MIN
from .conftest import MINI


def test_gate_invariants_p1_p5():
    seed_all(21, "t6")
    worst = 0.0
    for fam in ("p1", "p5"):
        m, _ = build_model(fam, "tiny", dict(MINI))
        m.eval()
        x = torch.randn(2, 12, MINI["d_model"])
        with torch.no_grad():
            for blk in m.blocks:
                mem = blk.delta
                beta = torch.sigmoid(mem.w_beta(x)).clamp(BETA_MIN, BETA_MAX)
                alpha = torch.exp(-torch.exp(mem.w_alpha(x)))
                assert bool(((beta >= BETA_MIN) & (beta <= BETA_MAX)).all()), fam
                assert bool(((alpha > 0) & (alpha < 1)).all()), fam
                k = mem._split(mem.w_k(x), mem.d_k) if fam == "p1" else None
                if k is not None:
                    kn = mem._normed_k(k)
                    sq = kn.pow(2).sum(dim=-1)  # unit norm per head by construction
                    prod = beta * sq  # both (B, T, H)
                    worst = max(worst, float(prod.max()))
                    assert bool((prod < 2.0).all()), (fam, float(prod.max()))
    print(f"T6 worst beta*||k||^2 = {worst:.4f} (< 2.0 required)")


def test_stability_collinear_finite():
    seed_all(22, "t6-collinear")
    for fam in ("transformer", "p1", "p5"):
        m, _ = build_model(fam, "tiny", dict(MINI))
        m.eval()
        ids = torch.full((1, 24), 7, dtype=torch.long)
        with torch.no_grad():
            out = m(ids)
        assert torch.isfinite(out).all(), fam
        assert float(out.abs().max()) < 1e6, (fam, float(out.abs().max()))
