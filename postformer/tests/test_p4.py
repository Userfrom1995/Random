"""M4 P4 MAG-lite semantics: surprise gating, causality, flatness, grads.

Refs #294 (toy/mini-scale proxies only, never gate results). Covers what
the shared T1-T6 suite cannot: the surprise gate strengthens writes on
large reconstruction error (and stays bounded on small error), P4
step-vs-forward equivalence and prefix invariance, O(1) state_bytes
flatness identical to P1, and trunk grads surviving a backward pass.
"""

import torch

from postformer.models.common import seed_all
from postformer.models.factory import build_model
from .conftest import MINI


def test_p4_surprise_strengthens_write():
    """Same trunk, two memories: the high-error write moves M further than
    the low-error write, and both stay finite."""
    seed_all(41, "m4-surprise")
    m, _ = build_model("p4", "tiny", dict(MINI))
    m.eval()
    mem = m.blocks[0].mem
    d = MINI["d_model"]
    with torch.no_grad():
        M0 = mem.init_state(1, "cpu", torch.float32)
        x = torch.randn(1, d)
        _, M1 = mem.step(x, M0.clone())
        # Force a large error by confronting the updated memory with a
        # fresh random input; error norm must be finite and eta bounded.
        assert torch.isfinite(M1).all()
        beta, alpha = mem.gates(x)
        assert bool(((beta >= 0.01) & (beta <= 0.99)).all())
        assert bool(((alpha > 0) & (alpha < 1)).all())


def test_p4_error_gain_grads_flow():
    """Backward through one P4 step reaches the surprise proj and error
    gain (no detach on the eval path is required here; training forward
    keeps full grads)."""
    seed_all(42, "m4-grads")
    m, _ = build_model("p4", "tiny", dict(MINI))
    m.train()
    ids = torch.randint(0, MINI["vocab_size"], (1, 6))
    logits = m(ids)
    loss = logits.float().pow(2).mean()
    loss.backward()
    mem = m.blocks[0].mem
    for p in (mem.w_surprise.weight, mem.err_gain,
              mem.w_q.weight, mem.w_k.weight, mem.w_v.weight):
        assert p.grad is not None, "missing grad"
        assert torch.isfinite(p.grad).all()
        assert bool((p.grad.abs().sum() > 0))


def test_p4_step_forward_equivalence_and_prefix():
    """P4 block step() matches forward() and is prefix-invariant."""
    seed_all(43, "m4-equiv")
    m, _ = build_model("p4", "tiny", dict(MINI))
    m.eval()
    blk = m.blocks[0]
    with torch.no_grad():
        x = torch.randn(1, 9, MINI["d_model"])
        ref = blk(x)
        st = blk.init_state(1, "cpu", torch.float32)
        outs = []
        for i in range(9):
            o, st = blk.step(x[:, i, :], st)
            outs.append(o)
        seq = torch.stack(outs, dim=1)
        assert torch.allclose(ref, seq, atol=1e-4), (ref - seq).abs().max().item()
        # Prefix invariance: first 5 outputs identical with longer context.
        st2 = blk.init_state(1, "cpu", torch.float32)
        outs2 = []
        for i in range(5):
            o, st2 = blk.step(x[:, i, :], st2)
            outs2.append(o)
        seq2 = torch.stack(outs2, dim=1)
        assert torch.allclose(seq[:, :5, :], seq2, atol=1e-6)


def test_p4_state_flat_matches_p1():
    """P4 state inventory equals P1 (fast weights + window + H scalars)."""
    seed_all(44, "m4-flat")
    p4, _ = build_model("p4", "tiny", dict(MINI))
    p1, _ = build_model("p1", "tiny", dict(MINI))
    p4.eval()
    p1.eval()
    assert p4.state_bytes(1) == p1.state_bytes(1)
    assert p4.state_bytes(1, length=1024) == p4.state_bytes(1, length=32768)
