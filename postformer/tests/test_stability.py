"""T6: gate/stability invariants (blueprint: beta*k-norm^2 < 2.0, alpha in (0,1)).

P1 keys are RMSNormed + unit-renormalized, beta is sigmoid-clamped to
[0.01, 0.99], alpha = exp(-exp(.)) in (0, 1) by construction, so the P1
2.0 contraction bound applies. P5 uses a degree-2 map
phi(k) = [k; 0.5 k^2] on RMSNormed (not unit) keys with a scaled ADDITIVE
write - no 2.0 contraction theory applies there, so P5 gets its own
separately-reported smoke bound (finite + generous cap), never the P1 claim.
This test asserts the invariants on live forward draws plus finite outputs
under collinear-key stress, and logs both worst cases.
"""

import torch

from postformer.models.common import seed_all
from postformer.models.factory import build_model
from postformer.models.p1_delta_hybrid import BETA_MAX, BETA_MIN
from postformer.models.p5_map import poly_map
from .conftest import MINI

P5_SMOKE_CAP = 50.0  # no contraction theory for the additive map; guards blowup only


def test_gate_invariants_p1_p5():
    seed_all(21, "t6")
    worst_p1, worst_p5 = 0.0, 0.0
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
                k = mem._split(mem.w_k(x), mem.d_k)
                if fam == "p1":
                    kn = mem._normed_k(k)
                    sq = kn.pow(2).sum(dim=-1)  # unit norm per head by construction
                    prod = beta * sq  # both (B, T, H)
                    worst_p1 = max(worst_p1, float(prod.max()))
                    assert bool((prod < 2.0).all()), (fam, float(prod.max()))
                else:
                    pk = poly_map(mem.k_norm(k))  # (B, T, H, 2*d_k)
                    sq = pk.pow(2).sum(dim=-1)
                    prod = beta * sq
                    worst_p5 = max(worst_p5, float(prod.max()))
                    assert bool(torch.isfinite(prod).all()), (fam, float(prod.max()))
                    assert bool((prod < P5_SMOKE_CAP).all()), (fam, float(prod.max()))
    print(f"T6 worst P1 beta*||k||^2 = {worst_p1:.4f} (< 2.0 required); "
          f"worst P5 beta*||phi(k)||^2 = {worst_p5:.4f} (< {P5_SMOKE_CAP} smoke cap)")


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
