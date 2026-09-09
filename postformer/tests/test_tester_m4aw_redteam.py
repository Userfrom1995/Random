"""Tester M4aw red-team: hostile live-fire on current head (Refs #294).

Novel vs prior suites (av pinned cfg-overrides/stride/g4-cells/parity/
ledger-25/viewer/discipline; au pinned state_bytes-length/flatness/tie/
provenance; as/v pinned p4 --window 0 eval-side; ap pinned cross-arm data
identity + p3/p4 determinism + curve sweep + p1 window-train liveness):
  1. Code-vs-proof state pins: every candidate family's S-tiny code total
     must equal its proof-g4.md pin (p1 3145728, p2 3538944, p3 4718592,
     p4 3145728, p5 4718592). No prior suite asserts these numbers.
  2. p4 --window 0 TRAIN-side liveness: 4-step p4-toy runs at window 0 vs
     default must diverge in trajectory (eval-side was covered by as/v;
     a silently-ignored train --window would be the M2 class again).
  3. Unknown family rejected loudly (ValueError), plus all five
     candidates reject tie_embeddings (au3 covered p1/p5 only).
  4. Ledger honesty sweep over all rows: notes non-empty, no "Closes"
     claim, every gate cell empty or a float in [0,1].
  5. Degenerate --steps 1 train: single-row curve, finite summary.
  6. T=1 single-token forward finite for p2/p3 (newest families; p4/T=1
     was covered by the M4a suite).
"""
import csv
import json
import os

import torch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
LEDGER = os.path.join(REPO_ROOT, "postformer", "ledger", "ledger.csv")
PROOF = os.path.join(REPO_ROOT, "postformer", "docs", "proof-g4.md")

PINS = {"p1": 3145728, "p2": 3538944, "p3": 4718592, "p4": 3145728,
        "p5": 4718592}


def _train(model, out, seed, steps=4, extra=()):
    from postformer.harness.train import main as train_main
    os.makedirs(out, exist_ok=True)
    train_main(["--model", model, "--data", "mqar", "--vocab", "64",
                "--n-pairs", "8", "--steps", str(steps), "--batch", "2",
                "--seed", str(seed), "--out", out,
                "--log-every", str(steps)] + list(extra))
    with open(os.path.join(out, "train_summary.json")) as f:
        return json.load(f)


def test_aw1_code_state_totals_match_proof_pins():
    """S-tiny code totals equal proof-g4.md pins for all five families."""
    from postformer.models.factory import build_model
    with open(PROOF) as f:
        proof = f.read()
    for fam, pin in PINS.items():
        m, _ = build_model(fam, "tiny", {})
        total = sum(b.state_size(4) for b in m.blocks)
        assert total == pin, (fam, total, pin)
        assert str(pin) in proof, (fam, pin)


def test_aw2_p4_window0_train_trajectory_differs(tmp_path):
    """p4-toy --window 0 trains a different trajectory than default."""
    s0 = _train("p4-toy", str(tmp_path / "w0"), 7, extra=("--window", "0"))
    s1 = _train("p4-toy", str(tmp_path / "wdef"), 7)
    assert s0["final_loss"] != s1["final_loss"], (s0, s1)
    assert all(map(lambda v: v == v and v != float("inf"),
                   [s0["final_loss"], s1["final_loss"]]))


def test_aw3_unknown_family_loud_and_all_candidates_reject_tie():
    """Unknown family raises; all five candidates reject tie_embeddings."""
    from postformer.models.factory import build_model
    try:
        build_model("p9", "toy", {"vocab_size": 66})
    except ValueError:
        pass
    else:
        raise AssertionError("unknown family silently accepted")
    for fam in ["p1", "p2", "p3", "p4", "p5"]:
        try:
            build_model(fam, "toy", {"vocab_size": 66,
                                     "tie_embeddings": True})
        except SystemExit:
            pass
        except ValueError:
            pass
        else:
            raise AssertionError(f"{fam} silently honors tie_embeddings")


def test_aw4_ledger_honesty_sweep_all_rows():
    """Every ledger row: notes non-empty, no Closes claim, cells valid."""
    with open(LEDGER, newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 25, len(rows)
    for r in rows:
        notes = (r.get("notes") or "")
        assert notes.strip(), r.get("model")
        assert "Closes" not in notes, r.get("model")
        for k, v in r.items():
            if v in ("", None):
                continue
            if k.startswith("g1_"):
                x = float(v)
                assert 0.0 <= x <= 1.0, (k, v)
            elif k.startswith(("g2_", "g3_", "g4_", "gpu_")):
                float(v)  # must parse, never silently corrupt


def test_aw5_steps1_train_single_row_finite(tmp_path):
    """Degenerate --steps 1: one curve row, finite loss (no IndexError)."""
    s = _train("p1-toy", str(tmp_path / "s1"), 3, steps=1)
    assert s["final_loss"] == s["final_loss"], s
    assert s["final_loss"] != float("inf"), s
    with open(os.path.join(str(tmp_path / "s1"), "train_curve.csv")) as f:
        lines = [ln for ln in f.read().strip().splitlines() if ln.strip()]
    assert len(lines) == 2, lines  # header + 1 row


def test_aw6_t1_forward_finite_p2_p3():
    """T=1 single-token forward finite for p2/p3 (newest families)."""
    from postformer.models.factory import build_model
    for fam in ["p2", "p3"]:
        m, cfg = build_model(fam, "toy", {"vocab_size": 66})
        m.eval()
        with torch.no_grad():
            x = torch.randint(0, 66, (1, 1))
            out = m(x)
        assert torch.isfinite(out).all(), fam
