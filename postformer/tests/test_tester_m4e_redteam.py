"""Tester M4e red-team: hostile verification of M4b non-MQAR probes + ledger scale.

Refs #294 (toy proxies only, never gate results). Prior suites pin M4b MQAR
cells and A4 N8 cells from raw CSVs; this suite attacks the remaining M4b
envelope (2hop / induction / copy recomputed from raw per-episode CSVs,
never trusting the summary JSON alone) plus the ledger row-count/scale
honesty after the A4/A6 sweeps grew the ledger to 25 rows (24 measured + 1
params-only drift-baseline pin). If any of these
fail, the M4b envelope or ledger provenance is fabrication and the PR goes
back to the Fixer.
"""

import csv
import json
import os

import pytest

REPO = os.path.join(os.path.dirname(__file__), "..")
LEDGER = os.path.join(REPO, "ledger", "ledger.csv")
M4B = os.path.join(REPO, "ledger", "curves", "m4b-toy")


def _acc(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) > 0, path
    return sum(int(r["correct"]) for r in rows) / len(rows)


def _summary():
    with open(os.path.join(M4B, "g1_summary_p4-toy-s0.json")) as f:
        return json.load(f)


def test_m4e_2hop_csv_recompute_matches_summary():
    """2hop 0.01 must recompute from the raw 100-episode CSV, not just JSON."""
    got = _acc(os.path.join(M4B, "g1_bind2hop_seed0_p4-toy-s0.csv"))
    want = _summary()["bind2hop"]["acc"]
    assert got == pytest.approx(want, abs=1e-9), (got, want)
    assert got == pytest.approx(0.01, abs=1e-9), got


def test_m4e_induction_copy_csv_recompute_are_zero():
    """Induction/copy 0.0 transfer must recompute from raw CSVs (untrained)."""
    ind = _acc(os.path.join(M4B, "g1_induction_gap16_seed0_p4-toy-s0.csv"))
    cop = _acc(os.path.join(M4B, "g1_copy_L32_seed0_p4-toy-s0.csv"))
    s = _summary()
    assert ind == pytest.approx(s["induction"]["16"], abs=1e-9), (ind, s)
    assert cop == pytest.approx(s["copying"]["32"], abs=1e-9), (cop, s)
    assert ind == 0.0 and cop == 0.0, (ind, cop)


def test_m4e_n16_csv_recompute_is_chance():
    """N16 0.015625 must recompute from the raw 1600-row CSV (= 1/64 chance)."""
    got = _acc(os.path.join(M4B, "g1_mqar_N16_seed0_p4-toy-s0.csv"))
    assert got == pytest.approx(1 / 64, abs=1e-9), got
    assert got == pytest.approx(_summary()["mqar"]["16"]["acc"], abs=1e-9)


def test_m4e_ledger_has_25_rows_all_toy_honest():
    """Ledger must hold 25 rows and no toy row may claim a gate pass."""
    with open(LEDGER) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 25, len(rows)
    for r in rows:
        blob = (r["notes"] + r["model"]).lower()
        honest = ("toy" in blob or "smoke" in blob or "random init" in blob
                  or "extrapolation" in blob or "g4" in blob)
        assert honest, r["model"]
        assert "gate pass" not in blob and "closes" not in blob, r["model"]
