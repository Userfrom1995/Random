"""Tester M4ad hostile suite: current-head final pins at 448e838c (post-M4ac).

Refs #294 (toy/mini-scale proxies only, never gate results).

Why this suite exists: the head moved to 448e838c (builder M4ac handoff,
ledger 25 rows green) with no code delta since the last tester commit, so
no prior single suite pins the current head end-to-end. This suite is a
compact final-gate aggregator at the current head: shipped-ledger liveness
(25 rows / 26 cols), M4b curve ground truth (p4 ledger cells match
curves/m4b-toy g1_summary), H4-negative honesty, envelope-audit
consistency, live parity within 2pct, MINI step/forward causality, and
shipped-code hygiene (no forward_chunk, viewer splitCSV).
"""

import csv
import json
import pathlib
import subprocess
import sys

import torch

from postformer.models.factory import build_model, count_params
from .conftest import FAMILIES

_HERE = pathlib.Path(__file__).resolve()
_POSTFORMER = _HERE.parents[1]
_LEDGER = _POSTFORMER / "ledger" / "ledger.csv"
_M4B = _POSTFORMER / "ledger" / "curves" / "m4b-toy"
_AUDIT = _POSTFORMER / "docs" / "envelope-audit.md"


def _rows():
    return list(csv.DictReader(_LEDGER.open()))


def test_ad1_shipped_ledger_green_25_rows_26_cols():
    rows = _rows()
    assert len(rows) == 25, [r["model"] for r in rows]
    assert len(rows[0].keys()) == 26, sorted(rows[0].keys())
    r = subprocess.run(
        [sys.executable, str(_POSTFORMER / "harness" / "ledger.py"),
         "check", "--ledger", str(_LEDGER)],
        capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-2000:]
    assert "ledger OK" in (r.stdout + r.stderr)


def test_ad2_m4b_curve_ground_truth_p4_cells():
    rows = _rows()
    p4 = next(r for r in rows if r["model"] == "p4-toy")
    summary = json.loads((_M4B / "g1_summary_p4-toy-s0.json").read_text())
    assert abs(float(p4["g1_mqar_8"]) - summary["mqar"]["8"]["acc"]) < 1e-9
    assert abs(float(p4["g1_2hop"]) - summary["bind2hop"]["acc"]) < 1e-9
    assert "NOT a gate result" in p4["notes"]
    assert "Refs #294" in p4["notes"]


def test_ad3_h4_negative_honestly_ledgered():
    rows = _rows()
    p4 = next(r for r in rows if r["model"] == "p4-toy")
    assert float(p4["g1_mqar_8"]) == 0.035
    assert "BELOW eval-matched p1-W16-1000 ref 0.0625" in p4["notes"]
    assert "eval-matched only" in p4["notes"]
    assert "BELOW matched p1-W16" not in p4["notes"]  # unqualified claim banned
    assert "H4 NEGATIVE at toy" in p4["notes"]
    audit = _AUDIT.read_text()
    assert "H4 NEGATIVE at toy" in audit or "0.035" in audit


def test_ad4_live_parity_all_families_within_2pct():
    base, _ = count_params("transformer", "tiny")
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        c, _ = count_params(fam, "tiny")
        assert abs(c - base) / base < 0.02, (fam, c, base)


def test_ad5_mini_step_forward_causal_spot():
    from postformer.models.common import seed_all
    seed_all(99, "tester-m4ad-spot")
    for fam in ("p1", "p4", "transformer"):
        assert fam in FAMILIES
        m, cfg = build_model(fam, "toy")
        m.eval()
        x = torch.randint(0, cfg["vocab_size"], (1, 16))
        with torch.no_grad():
            full = m(x)
            st = m.init_state(1, "cpu", torch.float32)
            outs = [m.step(x[:, i:i + 1], st)[0] for i in range(16)]
        assert torch.isfinite(full).all(), fam
        assert (full - torch.cat(outs, dim=1)).abs().max().item() <= 1e-4, fam


def test_ad6_shipped_hygiene_no_chunk_viewer_split():
    for sub in ("models", "harness"):
        for p in (_POSTFORMER / sub).rglob("*.py"):
            assert "forward_chunk" not in p.read_text(), p
    viewer = (_POSTFORMER / "viewer" / "index.html").read_text()
    assert "function splitCSV(line)" in viewer
