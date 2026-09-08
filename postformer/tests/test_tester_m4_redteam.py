"""Tester M4a hostile suite: P4 window guard, surprise bounds, parity, causality.

Refs #294 (toy/mini proxies only, never gate results). Durable regression
for the two M4a review findings plus P4 excellence gates.
"""

import torch

from postformer.models.common import seed_all
from postformer.models.factory import build_model, count_params
from .conftest import MINI


def test_p4_window_flag_accepted_and_rejected_for_transformer(tmp_path):
    # CLI-level check: --window must route for p4, reject for transformer.
    import pytest
    import postformer.harness.synthetic_recall as sr
    with pytest.raises(SystemExit):
        sr.main(["--model", "transformer-toy", "--task", "mqar",
                 "--window", "16", "--vocab", "64", "--episodes", "1",
                 "--n-pairs", "8", "--out", str(tmp_path / "rej")])
    # 1-episode p4 probe must NOT fail the family guard (writes under tmp).
    sr.main(["--model", "p4-toy", "--task", "mqar",
             "--window", "8", "--vocab", "64", "--episodes", "1",
             "--n-pairs", "8", "--out", str(tmp_path / "p4")])


def test_p4_parity_within_2pct_all_scales():
    for scale in ("toy", "tiny", "small"):
        base, _ = count_params("transformer", scale)
        cand, _ = count_params("p4", scale)
        drift = (cand - base) / base
        assert abs(drift) <= 0.02, (scale, base, cand, drift)


def test_p4_eta_bounded_and_surprise_monotone_same_base():
    """Same base M, same trunk x up to error scale: bigger error -> bigger move."""
    seed_all(101, "tester-m4-eta")
    m, _ = build_model("p4", "tiny", dict(MINI))
    m.eval()
    mem = m.blocks[0].mem
    d = MINI["d_model"]
    with torch.no_grad():
        M0 = mem.init_state(1, "cpu", torch.float32)
        x = torch.randn(1, d)
        # Grab internals manually to check eta bounds.
        q = mem._split(mem.w_q(x), mem.d_k)
        k = mem._split(mem.w_k(x), mem.d_k)
        v = mem._split(mem.w_v(x), mem.d_v)
        k = mem._normed_k(k)
        beta, alpha = mem.gates(x)
        assert bool(((beta >= 0.01) & (beta <= 0.99)).all())
        r = torch.einsum("bhki,bhk->bhi", M0, k)
        err = v - r
        err_norm = err.norm(dim=-1)
        s_logit = (mem.w_surprise(x) + mem.err_gain.view(1, -1) * err_norm * mem.surprise_scale)
        surprise = torch.sigmoid(s_logit).clamp(0.01, 0.99)
        eta = beta * surprise
        assert bool(((eta >= 0.0001) & (eta <= 0.9801)).all()), eta
        # Monotonicity: scale the error artificially, surprise must rise.
        s_big = torch.sigmoid(mem.w_surprise(x) + mem.err_gain.view(1, -1) * (err_norm * 5.0) * mem.surprise_scale)
        # err_gain is init +0.5 but could train negative; assert only finiteness here,
        # and monotonic direction conditional on positive gain.
        assert torch.isfinite(s_big).all()
        if bool((mem.err_gain > 0).all()):
            assert bool(((s_big >= surprise).all())), "surprise must not fall with bigger error when gain>0"


def test_p4_step_forward_equivalence_long_and_t1():
    seed_all(102, "tester-m4-equiv")
    m, _ = build_model("p4", "tiny", dict(MINI))
    m.eval()
    blk = m.blocks[0]
    with torch.no_grad():
        # T=1 degenerate.
        x1 = torch.randn(1, 1, MINI["d_model"])
        ref1 = blk(x1)
        st = blk.init_state(1, "cpu", torch.float32)
        o, _ = blk.step(x1[:, 0, :], st)
        assert torch.allclose(ref1[:, 0, :], o, atol=1e-4)
        # Longer incl. W boundary (W=8 in MINI).
        x = torch.randn(1, 20, MINI["d_model"])
        ref = blk(x)
        st = blk.init_state(1, "cpu", torch.float32)
        outs = []
        for i in range(20):
            o, st = blk.step(x[:, i, :], st)
            outs.append(o)
        seq = torch.stack(outs, dim=1)
        assert torch.allclose(ref, seq, atol=1e-4), (ref - seq).abs().max().item()


def test_p4_state_flat_and_matches_p1_mini():
    seed_all(103, "tester-m4-flat")
    p4, _ = build_model("p4", "tiny", dict(MINI))
    p1, _ = build_model("p1", "tiny", dict(MINI))
    assert p4.state_bytes(1, 1024) == p1.state_bytes(1, 1024)
    assert p4.state_bytes(1, length=1024) == p4.state_bytes(1, length=32768)


def test_p4_tie_embeddings_rejected():
    import pytest
    with pytest.raises(ValueError):
        build_model("p4", "tiny", dict(dict(MINI), tie_embeddings=True))


def test_p4_deterministic_rerun():
    seed_all(104, "tester-m4-det")
    m, _ = build_model("p4", "tiny", dict(MINI))
    m.eval()
    with torch.no_grad():
        ids = torch.randint(0, MINI["vocab_size"], (1, 7))
        a = m(ids)
        b = m(ids)
        assert torch.equal(a, b)


def test_p4_grads_reach_surprise_params():
    seed_all(105, "tester-m4-grad")
    m, _ = build_model("p4", "tiny", dict(MINI))
    m.train()
    ids = torch.randint(0, MINI["vocab_size"], (1, 6))
    loss = m(ids).float().pow(2).mean()
    loss.backward()
    mem = m.blocks[0].mem
    for p in (mem.w_surprise.weight, mem.err_gain, mem.w_beta.weight):
        assert p.grad is not None and torch.isfinite(p.grad).all()
        assert bool((p.grad.abs().sum() > 0))
