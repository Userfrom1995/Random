"""Tester M4aj red-team: live black-box CLI chain on current head (Refs #294).

Novel vs prior suites: instead of asserting pinned values, this suite RUNS
the product end to end as a hostile consumer would:
  1. train tiny toy models for a handful of steps via the real CLI,
  2. evaluate the checkpoint via the real G1 CLI,
  3. round-trip a ledger append/check cycle in an isolated ledger,
  4. while attacking determinism, state flatness, degenerate shapes,
     and hostile ledger notes (quotes/commas) that once broke the viewer.
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest
import torch

REPO = Path(__file__).resolve().parents[2]
FAMS = ["transformer", "p1", "p2", "p3", "p4", "p5"]


def run_cli(*args, timeout=600):
    return subprocess.run(
        [sys.executable, "-m"] + list(args),
        capture_output=True, text=True, timeout=timeout, cwd=str(REPO),
    )


def test_aj1_e2e_train_eval_chain_tmp(tmp_path):
    """Black-box chain: train p1-toy 4 steps, eval checkpoint, outputs finite."""
    out = tmp_path / "t"
    r = run_cli("postformer.harness.train", "--model", "p1-toy",
                "--data", "mqar", "--vocab", "64", "--steps", "4",
                "--batch", "2", "--seed", "7", "--out", str(out))
    assert r.returncode == 0, r.stderr[-2000:]
    ckpts = list(out.glob("*.pt"))
    assert ckpts, "train produced no checkpoint"
    summ = json.loads((out / "train_summary.json").read_text()) \
        if (out / "train_summary.json").exists() \
        else json.loads(next(out.glob("train_summary*.json")).read_text())
    assert all(v == v for v in [summ["final_loss"]]), summ
    eout = tmp_path / "e"
    r2 = run_cli("postformer.harness.synthetic_recall", "--model", "p1-toy",
                 "--checkpoint", str(ckpts[0]), "--task", "mqar",
                 "--vocab", "64", "--n-pairs", "8", "--episodes", "5",
                 "--seed", "7", "--out", str(eout))
    assert r2.returncode == 0, r2.stderr[-2000:]
    files = list(eout.glob("*.json")) + list(eout.glob("*.csv"))
    assert files, "eval produced no output files"


def test_aj2_e2e_transformer_control_chain_tmp(tmp_path):
    """Baseline arm runs the same chain (control must not crash either)."""
    out = tmp_path / "t"
    r = run_cli("postformer.harness.train", "--model", "transformer-toy",
                "--data", "mqar", "--vocab", "64", "--steps", "4",
                "--batch", "2", "--seed", "7", "--out", str(out))
    assert r.returncode == 0, r.stderr[-2000:]
    assert list(out.glob("*.pt")), "baseline train produced no checkpoint"


def test_aj3_train_determinism_same_seed(tmp_path):
    """Same (model, seed) twice -> identical final loss (reproducibility)."""
    losses = []
    for i in range(2):
        out = tmp_path / f"t{i}"
        r = run_cli("postformer.harness.train", "--model", "p5-toy",
                    "--data", "mqar", "--vocab", "64", "--steps", "4",
                    "--batch", "2", "--seed", "11", "--out", str(out))
        assert r.returncode == 0, r.stderr[-2000:]
        cands = list(out.glob("train_summary*.json"))
        assert cands
        losses.append(json.loads(cands[0].read_text())["final_loss"])
    assert losses[0] == losses[1], losses


def test_aj4_state_bytes_flat_property_all_fams():
    """G4 property (not pinned value): state bytes identical at T=1k vs 32k."""
    sys.path.insert(0, str(REPO))
    from postformer.models.factory import build_model
    from postformer.tests.conftest import MINI
    for fam in FAMS:
        m, _ = build_model(fam, "tiny", dict(MINI))
        lo = m.state_bytes(1, length=1000)
        hi = m.state_bytes(1, length=32000)
        if fam == "transformer":
            # Control must GROW (KV cache): proves the property discriminates.
            assert hi > lo > 0, (fam, lo, hi)
        else:
            assert hi == lo > 0, (fam, lo, hi)


def test_aj5_degenerate_t1_forward_all_fams():
    """Single-token block forward is finite for every family (degenerate shape)."""
    sys.path.insert(0, str(REPO))
    from postformer.models.factory import build_model
    from postformer.models.common import seed_all
    from postformer.tests.conftest import MINI
    seed_all(407, "tester-m4aj-t1")
    for fam in FAMS:
        m, _ = build_model(fam, "tiny", dict(MINI))
        m.eval()
        blk = m.blocks[0]
        with torch.no_grad():
            x1 = torch.randn(1, 1, MINI["d_model"])
            ref1 = blk(x1)
            assert torch.isfinite(ref1).all(), fam


def test_aj6_ledger_hostile_notes_roundtrip(tmp_path):
    """Notes with quotes/commas survive append+check (viewer CSV class)."""
    led = tmp_path / "ledger.csv"
    led.write_text(
        "model,params,train_tokens,seed,vocab,window,slots,use_accumulator,"
        "g1_mqar_8,g1_mqar_16,g1_mqar_64,g1_mqar_256,g1_induction,g1_copy,"
        "g1_2hop,g2_bpb_1x,g2_bpb_4x,g2_bpb_8x,g2_delta_4x,g2_delta_8x,"
        "g3_valid_bpb,g3_test_bpb,g4_state_bytes,g4_ms_per_token,gpu_hours,notes\n")
    nasty = 'toy probe, says "hi, bye", commas,everywhere'
    row = {"model": "p1-toy", "params": "336332", "train_tokens": "528000",
           "seed": "0", "vocab": "64", "window": "16", "slots": "",
           "use_accumulator": "", "g1_mqar_8": "0.06", "g1_mqar_16": "",
           "g1_mqar_64": "", "g1_mqar_256": "", "g1_induction": "",
           "g1_copy": "", "g1_2hop": "", "g2_bpb_1x": "", "g2_bpb_4x": "",
           "g2_bpb_8x": "", "g2_delta_4x": "", "g2_delta_8x": "",
           "g3_valid_bpb": "", "g3_test_bpb": "", "g4_state_bytes": "",
           "g4_ms_per_token": "", "gpu_hours": "", "notes": nasty}
    with led.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        w.writerow(row)
    r = run_cli("postformer.harness.ledger", "check", "--ledger", str(led))
    assert r.returncode == 0, r.stderr[-2000:] + r.stdout[-2000:]
    with led.open(newline="") as f:
        back = list(csv.DictReader(f))[0]["notes"]
    assert back == nasty, back


def test_aj7_ledger_rejects_garbage_model_key(tmp_path):
    """Ledger check loudly rejects a row with a garbage model key."""
    led = tmp_path / "ledger.csv"
    led.write_text("model,params,notes\nnot-a-model!!!,xyz,\"hi\"\n")
    r = run_cli("postformer.harness.ledger", "check", "--ledger", str(led))
    assert r.returncode != 0, "garbage row must not pass check"


def test_aj8_step_prefix_invariance_p4_across_w():
    """P4 incremental step matches block forward across the W boundary."""
    sys.path.insert(0, str(REPO))
    from postformer.models.factory import build_model
    from postformer.models.common import seed_all
    from postformer.tests.conftest import MINI
    seed_all(408, "tester-m4aj-prefix")
    m, _ = build_model("p4", "tiny", dict(MINI))
    m.eval()
    blk = m.blocks[0]
    with torch.no_grad():
        x = torch.randn(1, 20, MINI["d_model"])
        ref = blk(x)
        st = blk.init_state(1, "cpu", torch.float32)
        outs = []
        for i in range(20):
            o, st = blk.step(x[:, i, :], st)
            outs.append(o)
        seq = torch.stack(outs, dim=1)
        assert torch.isfinite(ref).all() and torch.isfinite(seq).all()
        assert torch.allclose(ref, seq, atol=1e-4), (ref - seq).abs().max().item()
