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


def test_stability_collinear_stays_finite():
    seed_all(22, "t6-collinear")
    for fam in ("transformer", "p1", "p2", "p3", "p4", "p5"):
        m, _ = build_model(fam, "tiny", dict(MINI))
        m.eval()
        ids = torch.full((1, 24), 7, dtype=torch.long)
        with torch.no_grad():
            out = m(ids)
        assert torch.isfinite(out).all(), fam
        # Smoke bound (not an envelope claim): collinear stress must not explode.
        assert float(out.abs().max()) < 1e6, (fam, float(out.abs().max()))


def test_gate_invariants_p2_p3():
    """T6 (M3 arms): SSD decay gate a in (0, 1); P3 acc/selective betas in
    [0.01, 0.99], selective alpha in (0, 1); accumulator rescale hook fires
    (counter increments) rather than overflowing on a long constant stream."""
    from postformer.models.p1_delta_hybrid import BETA_MAX as _BMAX, BETA_MIN as _BMIN
    seed_all(23, "t6-p2p3")
    m2, _ = build_model("p2", "tiny", dict(MINI))
    m2.eval()
    x = torch.randn(2, 12, MINI["d_model"])
    with torch.no_grad():
        for blk in m2.blocks:
            a = torch.exp(-torch.exp(blk.ssd.w_a(x)))
            assert bool(((a > 0) & (a < 1)).all()), "p2 decay gate"
    m3, _ = build_model("p3", "tiny", dict(MINI))
    m3.eval()
    with torch.no_grad():
        for blk in m3.blocks:
            mem = blk.mem
            for proj in (mem.w_beta_acc, mem.w_beta_sel):
                b = torch.sigmoid(proj(x)).clamp(_BMIN, _BMAX)
                assert bool(((b >= _BMIN) & (b <= _BMAX)).all()), "p3 beta"
            al = torch.exp(-torch.exp(mem.w_alpha(x)))
            assert bool(((al > 0) & (al < 1)).all()), "p3 alpha"
        # Long constant stream: outputs finite, rescale counter is an int.
        ids = torch.full((1, 96), 5, dtype=torch.long)
        out = m3(ids)
        assert torch.isfinite(out).all()
        st = m3.init_state(1, "cpu", torch.float32)
        for i in range(96):
            tok = torch.full((1, 1), 5, dtype=torch.long)
            _, st = m3.step(tok, st)
        assert isinstance(st[0]["mem"]["rescales"], int)
