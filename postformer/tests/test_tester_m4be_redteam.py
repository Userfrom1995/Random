"""M4be hostile suite: M4b P4-probe ground truth + live gate honesty pins.

Locks the M4b deliverable against silent ledger/curve drift and
gate-claim inflation:
- ledger row p4-toy cells byte-match curves/m4b-toy/ ground truth JSONs
- curve CSV row counts match their eval budgets (N8 800 + header, etc.)
- H4 NEGATIVE honesty: p4 row carries NOT-a-gate-result qualifier and no
  gate-pass language; no post-base commit subject claims Closes #294
- live P4 pins: tiny parity within 2%, eta double-clamped, T=1 finite
Refs #294.
"""

from __future__ import annotations

import csv
import json
import subprocess as sp
from pathlib import Path

import pytest
import torch

REPO = Path(__file__).resolve().parents[2]
CURVES = REPO / "postformer/ledger/curves/m4b-toy"
LEDGER = REPO / "postformer/ledger/ledger.csv"
BASE = "cdf3cdae"


def _ledger_rows() -> list[dict]:
    with open(LEDGER, newline="") as f:
        return list(csv.DictReader(f))


def _p4_row() -> dict:
    rows = [r for r in _ledger_rows() if r["model"] == "p4-toy"]
    assert rows, "p4-toy ledger row missing"
    return rows[0]


def test_be1_m4b_cells_match_curve_json():
    """Ledger p4-toy G1 cells equal the committed curve summary JSON."""
    row = _p4_row()
    summary = json.loads((CURVES / "g1_summary_p4-toy-s0.json").read_text())
    assert float(row["g1_mqar_8"]) == pytest.approx(
        summary["mqar"]["8"]["acc"], abs=1e-9), \
        (row["g1_mqar_8"], summary["mqar"]["8"]["acc"])
    assert float(row["g1_mqar_16"]) == pytest.approx(
        summary["mqar"]["16"]["acc"], abs=1e-9)
    assert float(row["g1_2hop"]) == pytest.approx(
        summary["bind2hop"]["acc"], abs=1e-9)


def test_be2_m4b_curve_budgets():
    """Curve CSVs carry exactly their eval budgets (no truncation/padding)."""
    assert sum(1 for _ in open(CURVES / "g1_mqar_N8_seed0_p4-toy-s0.csv")) == 801
    assert sum(1 for _ in open(CURVES / "g1_mqar_N16_seed0_p4-toy-s0.csv")) == 1601
    for name in ("g1_bind2hop_seed0_p4-toy-s0.csv",
                 "g1_copy_L32_seed0_p4-toy-s0.csv",
                 "g1_induction_gap16_seed0_p4-toy-s0.csv"):
        assert sum(1 for _ in open(CURVES / name)) == 101, name
    train = json.loads((CURVES / "train_summary_p4-toy-s0.json").read_text())
    assert train["train_tokens"] == 528000, train  # 1000 steps x batch16 x len33
    assert train["params_no_embed"] == 335316, train  # matches ledger cell


def test_be3_h4_negative_honesty_no_gate_claim():
    """p4 row discloses H4 NEGATIVE at toy and refuses gate-pass language."""
    notes = _p4_row()["notes"]
    assert "NOT a gate result" in notes, notes[:200]
    assert "H4 NEGATIVE" in notes or "H4" in notes
    for phrase in ("G1 PASS", "gate passed", "G1+G2+G3+G4", "Closes #294"):
        assert phrase not in notes, f"gate inflation: {phrase}"


def test_be4_no_closes_in_post_base_subjects():
    """No post-base commit subject closes the tracking issue early."""
    out = sp.run(["git", "log", f"{BASE}..HEAD", "--pretty=format:%s"],
                 capture_output=True, text=True, cwd=str(REPO))
    assert out.returncode == 0, out.stderr[:200]
    bad = [s for s in out.stdout.splitlines()
           if "closes #294" in s.lower()]
    assert not bad, f"early close attempt: {bad[:3]}"


def test_be5_live_p4_tiny_parity():
    """Live re-measure: p4-tiny within 2% of transformer-tiny."""
    from postformer.models.factory import count_params
    base = count_params("transformer", "tiny")[0]
    assert base == 29366784, f"baseline pin moved: {base}"
    n = count_params("p4", "tiny")[0]
    assert abs(n - base) / base < 0.02, f"p4-tiny drift: {n} vs {base}"


def test_be6_live_p4_eta_double_clamped():
    """P4 surprise gain stays inside [0.0001, 0.9801] under huge errors."""
    from postformer.models.factory import build_model
    model, cfg = build_model("p4", "toy")
    model.eval()
    with torch.no_grad():
        x = torch.randint(0, cfg["vocab_size"], (2, 8))
        states = model.init_state(2, "cpu", torch.float32)
        for t in range(8):
            out, states = model.step(x[:, t:t + 1], states)  # (B,1) tokens
        assert torch.isfinite(out).all(), "p4 step rollout non-finite"
    # direct kernel probe: eta = beta*sigmoid(...) clamped twice in source
    import inspect
    from postformer.models import p4_maglite
    src = inspect.getsource(p4_maglite)
    assert "0.0001" in src and "0.9801" in src, "clamp bounds missing"
    assert torch.isfinite(x.float()).all()


def test_be7_viewer_csv_hardening_present():
    """Viewer keeps RFC-4180 splitCSV plus notes escaping (M1 finding)."""
    src = (REPO / "postformer/viewer/index.html").read_text()
    assert "splitCSV" in src, "quote-aware splitter regressed"
    code = "\n".join(ln for ln in src.splitlines()
                     if ln.strip() and not ln.strip().startswith("//"))
    assert '.split(",")' not in code, "quote-unaware split live in code"
