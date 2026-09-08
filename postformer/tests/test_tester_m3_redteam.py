"""Tester M3 hostile regression suite (PR #295 M3, issue #294).

Durable checks owned by the Tester for the M3 delta (P2 slots + P3
decoupled + loader inheritance fix) on top of the M1+M2-toy suite.
All CPU-fast (toy scale only).

Covers:
- P3 rescale guard preserves trunk grads when it fires (the M3 finding-1
  detach bug must stay fixed).
- P2/P3 state_size exactness vs the proof-g4 inventory (finding-2/3
  overcount/phantom bugs must stay fixed) + proof numbers match code.
- P2/P3 step-vs-forward equivalence and prefix invariance (slot reads
  must stay causal, j<=i only).
- P2/P3 param parity within 2% at all scales; A3/A4 controls keep
  identical params (honest ablations).
- P2 slot determinism + slots=0 pure-SSD control finite.
- Loader ablation inheritance: checkpoint window/slots/use_accumulator
  inherited, mismatch rejected.

Refs #294 (never Closes: G1+G2+G3+G4 at pinned S-tiny/S-small pending).
"""

import os

import pytest
import torch

from postformer.models.common import seed_all
from postformer.models.factory import build_model, count_params

REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
PFDIR = os.path.join(os.path.dirname(__file__), "..")
PROOF = os.path.join(PFDIR, "docs", "proof-g4.md")


# --- Finding 1: P3 _guard must not detach trunk grads when it fires ---

def test_p3_guard_preserves_grads_on_fire():
    from postformer.models.p3_decoupled import DecoupledMemory
    seed_all(7, "tester-m3-guard")
    mem = DecoupledMemory(d_model=32, heads=2, d_k=8, d_v=8)
    mem.train()
    # Force the guard to fire every step with a tiny cap.
    mem.rescale_cap = 1e-9
    state = mem.init_state(2, "cpu", torch.float32)
    outs = []
    for _ in range(6):
        o, state = mem.step(torch.randn(2, 32), state)
        outs.append(o)
    assert state["rescales"] > 0, "guard never fired; test is vacuous"
    loss = torch.stack(outs, dim=1).pow(2).mean()
    loss.backward()
    # Trunk projections feeding A must still carry grads (detach bug = None).
    for mod, name in ((mem.w_k, "w_k"), (mem.w_v, "w_v"),
                      (mem.w_beta_acc, "w_beta_acc")):
        assert mod.weight.grad is not None, f"{name} grad detached by _guard"
        assert torch.isfinite(mod.weight.grad).all(), f"{name} grad non-finite"
        assert mod.weight.grad.abs().sum().item() > 0, \
            f"{name} grad silently zero"


def test_p3_guard_no_fire_passthrough_keeps_graph():
    from postformer.models.p3_decoupled import DecoupledMemory
    seed_all(8, "tester-m3-guard-idle")
    mem = DecoupledMemory(d_model=32, heads=2, d_k=8, d_v=8)
    mem.train()
    state = mem.init_state(1, "cpu", torch.float32)
    outs = []
    for _ in range(4):
        o, state = mem.step(torch.randn(1, 32), state)
        outs.append(o)
    assert state["rescales"] == 0
    torch.stack(outs, dim=1).pow(2).mean().backward()
    assert mem.w_k.weight.grad is not None


# --- Findings 2/3: state_size exactness + proof agreement ---

def _tiny_cfg(fam):
    _, cfg = build_model(fam, "tiny")
    return cfg


def test_p2_state_size_exact_tiny():
    m, cfg = build_model("p2", "tiny")
    blk = m.blocks[0]
    H, dk, dv = cfg["heads"], cfg["d_k"], cfg["d_v"]
    W, wd = cfg["window"], cfg["win_heads"] * cfg["win_hd"]
    G = cfg["slots"]
    expected = H * dk * dv * 4 + G * H * (dk + dv) * 4 + 2 * W * wd * 4
    got = blk.state_size(4)
    assert got == expected, (got, expected)
    # Regression tripwire for the old 2x-slots + phantom-H bug:
    buggy = 2 * G * H * (dk + dv) * 4 + H * dk * dv * 4 + H * 4 + 2 * W * wd * 4
    assert got != buggy, "state_size still carries the 2x/phantom terms"
    assert got < buggy


def test_p3_state_size_accumulator_on_off():
    m_on, cfg = build_model("p3", "tiny")
    H, dk, dv = cfg["heads"], cfg["d_k"], cfg["d_v"]
    W, wd = cfg["window"], cfg["win_heads"] * cfg["win_hd"]
    win = 2 * W * wd * 4
    assert m_on.blocks[0].state_size(4) == 2 * H * dk * dv * 4 + win
    m_off, _ = build_model("p3", "tiny", {"use_accumulator": False})
    # A stays resident (zeros when disabled), so off reports the same 2x.
    assert m_off.blocks[0].state_size(4) == 2 * H * dk * dv * 4 + win


def test_proof_g4_m3_numbers_match_code():
    m2, _ = build_model("p2", "tiny")
    m3, _ = build_model("p3", "tiny")
    # 6 tiny layers; proof claims P2 589824/layer = 3538944, P3 786432 = 4718592.
    p2_total = sum(b.state_size(4) for b in m2.blocks)
    p3_total = sum(b.state_size(4) for b in m3.blocks)
    assert p2_total == 3538944, p2_total
    assert p3_total == 4718592, p3_total
    with open(PROOF) as f:
        src = f.read()
    assert "3538944" in src and "4718592" in src


# --- P2/P3 causality: step == forward, prefix invariance ---

def test_p2_p3_step_matches_forward_and_prefix_invariant():
    seed_all(21, "tester-m3-causal")
    for fam in ("p2", "p3"):
        m, _ = build_model(fam, "toy")
        m.eval()
        x = torch.randint(0, 66, (1, 32))
        with torch.no_grad():
            full = m(x)
            st = m.init_state(1, "cpu", torch.float32)
            outs = [m.step(x[:, i:i + 1], st)[0] for i in range(32)]
        diff = (torch.cat(outs, dim=1) - full).abs().max().item()
        assert diff <= 1e-4, (fam, diff)
        with torch.no_grad():
            a = torch.randint(0, 66, (1, 10))
            la = m(torch.cat([a, torch.full((1, 6), 3)], dim=1))
            lb = m(torch.cat([a, torch.randint(0, 66, (1, 6))], dim=1))
            pv = (la[:, :10] - lb[:, :10]).abs().max().item()
        assert pv <= 1e-6, (fam, pv)


# --- Parity + honest A3/A4 controls ---

def test_p2_p3_parity_within_two_percent():
    for scale in ("toy", "tiny", "small"):
        base, _ = count_params("transformer", scale)
        for fam in ("p2", "p3"):
            n, _ = count_params(fam, scale)
            assert abs(n - base) / base <= 0.02, (scale, fam, base, n)


def test_a3_a4_controls_keep_identical_params():
    n_p3, _ = count_params("p3", "toy")
    n_off, _ = count_params("p3", "toy", {"use_accumulator": False})
    assert n_off == n_p3, (n_off, n_p3)
    n_p2, _ = count_params("p2", "toy")
    n_s0, _ = count_params("p2", "toy", {"slots": 0})
    assert n_s0 == n_p2, (n_s0, n_p2)


def test_p2_slots_determinism_and_zero_slot_control():
    seed_all(33, "tester-m3-slots")
    for slots in (16, 0):
        m, _ = build_model("p2", "toy", {"slots": slots} if slots == 0 else {})
        m.eval()
        x = torch.randint(0, 66, (1, 24))
        with torch.no_grad():
            o1 = m(x)
            o2 = m(x)
        assert torch.isfinite(o1).all(), slots
        # Determinism intent: same model, same input, bitwise identical rerun.
        assert torch.equal(o1, o2), slots


# --- Loader ablation inheritance ---

def test_loader_inherits_ablation_keys_and_rejects_mismatch():
    import tempfile
    from postformer.harness.util import load_model
    seed_all(44, "tester-m3-loader")
    m, cfg = build_model("p3", "toy")
    with tempfile.TemporaryDirectory() as tmp:
        ckpt = os.path.join(tmp, "ckpt.pt")
        torch.save({"state_dict": m.state_dict(), "config": cfg}, ckpt)
        # Inherited without overrides.
        m2, c2, rnd = load_model("p3-toy", ckpt, None, {}, "cpu", "fp32")
        assert c2["use_accumulator"] is True
        assert rnd is False
        # Explicit mismatch on a non-window ablation key must fail loudly
        # (SystemExit, a BaseException, is the harness's loud-reject path).
        with pytest.raises(SystemExit):
            load_model("p3-toy", ckpt, None,
                       {"use_accumulator": False, "window": cfg["window"]},
                       "cpu", "fp32")
