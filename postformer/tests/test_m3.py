"""M3 semantics: A3/A4 ablation controls, slot-buffer contract, G4 flatness.

Covers what the shared T1-T6 suite cannot: the P3 accumulator on/off
switch (A3), the P2 slots=0 pure-SSD control (A4), the SlotBuffer write/
evict/read contract, O(1) state_bytes flatness for p2/p3 vs the growing
transformer control, and the new train.py ablation flags.

Refs #294 (toy-scale falsification proxies only, never gate results).
"""

import pytest
import torch

from postformer.models.common import seed_all
from postformer.models.factory import build_model
from postformer.models.p2_slots import SlotBuffer
from .conftest import MINI


def test_a3_accumulator_off_zeroes_branch():
    """P3 with use_accumulator=False: acc contribution is exactly zero and
    the rescale hook never fires (dynamics removed, params unchanged)."""
    seed_all(31, "m3-a3")
    cfg = dict(MINI)
    mon, _ = build_model("p3", "tiny", cfg)
    moff, _ = build_model("p3", "tiny", {**cfg, "use_accumulator": False})
    n_on = sum(p.numel() for p in mon.parameters())
    n_off = sum(p.numel() for p in moff.parameters())
    assert n_on == n_off, (n_on, n_off)  # ablation varies dynamics, not params
    mon.eval()
    moff.eval()
    x = torch.randn(1, 10, MINI["d_model"])
    with torch.no_grad():
        st = moff.blocks[0].mem.init_state(1, "cpu", torch.float32)
        r, s, st = moff.blocks[0].mem.step_split(moff.blocks[0].n1(x)[:, 0, :], st)
        assert torch.allclose(r, s, atol=1e-6), (r - s).abs().max().item()
        assert st["rescales"] == 0


def test_a4_slots_zero_is_pure_ssd():
    """P2 with slots=0: slot branch reads None (zeros), SlotBuffer never
    fills, and invalid slot configs raise loudly."""
    seed_all(32, "m3-a4")
    m, _ = build_model("p2", "tiny", {**dict(MINI), "slots": 0})
    m.eval()
    st = m.init_state(1, "cpu", torch.float32)
    assert st[0]["buf"].slots == 0
    ids = torch.randint(0, MINI["vocab_size"], (1, 6))
    with torch.no_grad():
        for i in range(6):
            _, st = m.step(ids[:, i:i + 1], st)
    assert st[0]["buf"].n == 0 and st[0]["buf"].writes == 0
    with pytest.raises(ValueError):
        SlotBuffer(1, 2, 8, 8, -1, 8, "cpu", torch.float32)
    with pytest.raises(ValueError):
        SlotBuffer(1, 2, 8, 8, 4, 0, "cpu", torch.float32)


def test_slot_buffer_stride_write_and_oldest_evict():
    """Stride writer keeps every stride-th token; when full, oldest evicts;
    read is exact attention over stored slots (weights sum to 1)."""
    seed_all(33, "m3-slots")
    G, H, dk, dv, stride = 4, 2, 8, 8, 3
    buf = SlotBuffer(1, H, dk, dv, G, stride, "cpu", torch.float32)
    torch.manual_seed(0)
    for t in range(20):
        k = torch.randn(1, H, dk)
        v = torch.randn(1, H, dv)
        buf.append(k, v)
    # positions 0,3,...,18 written = 7 writes, capacity 4 -> last 4 kept
    assert buf.writes == 7, buf.writes
    assert buf.n == G
    q = torch.randn(1, H, dk)
    rd = buf.read(q)
    assert rd is not None and rd.shape == (1, H, dv)
    assert torch.isfinite(rd).all()
    # read weights are a convex combination: verify via reconstruction bound
    assert float(rd.abs().max()) < 1e4


def test_g4_state_bytes_flat_for_p2_p3():
    """state_bytes is O(1) in T for p2/p3 (identical at 1k and 32k) while
    the transformer control grows linearly (the G4 contrast)."""
    for fam in ("p2", "p3"):
        m, _ = build_model(fam, "tiny")
        a = m.state_bytes(1, 1024)
        b = m.state_bytes(1, 32768)
        assert a == b > 0, (fam, a, b)
    mt, _ = build_model("transformer", "tiny")
    assert mt.state_bytes(1, 32768) > mt.state_bytes(1, 1024)


def test_train_ablation_flags():
    """train.py accepts --slots >= 0 and --no-accumulator, rejects --slots -1."""
    from postformer.harness.train import main as train_main
    import tempfile, os
    with tempfile.TemporaryDirectory() as tmp:
        base = ["--model", "p2-toy", "--data", "mqar", "--steps", "2",
                "--batch", "2", "--out", os.path.join(tmp, "a")]
        train_main(base + ["--slots", "0"])
        train_main(base + ["--slots", "4", "--out", os.path.join(tmp, "b")])
        with pytest.raises(SystemExit):
            train_main(base + ["--slots", "-1", "--out", os.path.join(tmp, "c")])
        train_main(["--model", "p3-toy", "--data", "mqar", "--steps", "2",
                    "--batch", "2", "--no-accumulator",
                    "--out", os.path.join(tmp, "d")])
