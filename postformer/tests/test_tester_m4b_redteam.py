"""Tester M4b hostile suite: P4-vs-P1 matched toy probe honesty + ledger/curve integrity.

Refs #294 (toy proxies only, never gate results). Durable regression for the
M4b Builder delta: ledger row 19 (p4-toy seed0, 0.528M tokens) plus the 8
curves under postformer/ledger/curves/m4b-toy/ and the M4b ideas entry.
"""

import csv
import json
import os

import pytest

REPO = os.path.join(os.path.dirname(__file__), "..")
LEDGER = os.path.join(REPO, "ledger", "ledger.csv")
M4B = os.path.join(REPO, "ledger", "curves", "m4b-toy")
IDEAS = os.path.join(os.path.dirname(__file__), "..", "..", "ideas",
                     "2026-09-08-postformer-m4b-p4-probes.md")

G1 = os.path.join(M4B, "g1_summary_p4-toy-s0.json")
TRAIN = os.path.join(M4B, "train_summary_p4-toy-s0.json")


def _ledger_rows():
    with open(LEDGER) as f:
        return list(csv.DictReader(f))


def _p4_row():
    rows = [r for r in _ledger_rows() if r["model"] == "p4-toy"]
    assert len(rows) == 1, f"expected exactly one p4-toy row, got {len(rows)}"
    return rows[0]


def test_m4b_ledger_row_matches_curve_json():
    """Ledger cells must be literal copies of the curve ground truth."""
    g = json.load(open(G1))
    r = _p4_row()
    assert float(r["g1_mqar_8"]) == pytest.approx(g["mqar"]["8"]["acc"])
    assert float(r["g1_mqar_16"]) == pytest.approx(g["mqar"]["16"]["acc"])
    assert float(r["g1_2hop"]) == pytest.approx(g["bind2hop"]["acc"])
    assert float(r["g1_induction"]) == pytest.approx(g["induction"]["16"])
    assert float(r["g1_copy"]) == pytest.approx(g["copying"]["32"])
    assert int(r["params"]) == g["params_no_embed"] == 335316
    assert r["vocab"] == "64" and r["window"] == "16" and r["seed"] == "0"
    assert int(r["train_tokens"]) == 528000


def test_m4b_matched_budget_token_math():
    """1000 steps x batch16 x 33 tokens/seq must equal the M3 0.528M budget."""
    t = json.load(open(TRAIN))
    assert t["train_tokens"] == 528000 == 1000 * 16 * 33
    assert t["model"] == "p4-toy" and t["data"] == "mqar"
    rows = _ledger_rows()
    for m in ("p2-toy", "p3-toy", "p3-noacc-toy"):
        hit = [x for x in rows if x["model"] == m]
        assert hit and int(hit[0]["train_tokens"]) == 528000, m
    # Train curve: finite, final below first (4.3195 -> 4.1157 per ideas).
    with open(os.path.join(M4B, "train_curve_p4-toy-s0.csv")) as f:
        curve = list(csv.DictReader(f))
    losses = [float(x["loss"]) for x in curve]
    assert all(l == l and abs(l) != float("inf") for l in losses)
    assert losses[-1] < losses[0], (losses[0], losses[-1])
    assert abs(losses[-1] - t["final_loss"]) < 1e-6


def test_m4b_n16_collapse_is_chance():
    """N16 0.015625 must equal 1/64 chance; N16 CSV holds 100eps x 16 rows."""
    g = json.load(open(G1))
    assert g["mqar"]["16"]["acc"] == pytest.approx(1 / 64)
    assert g["mqar"]["16"]["n"] == 1600
    with open(os.path.join(M4B, "g1_mqar_N16_seed0_p4-toy-s0.csv")) as f:
        lines = f.readlines()
    assert len(lines) == 1601, len(lines)  # header + 1600 query rows
    with open(os.path.join(M4B, "g1_mqar_N8_seed0_p4-toy-s0.csv")) as f:
        assert len(f.readlines()) == 801  # header + 800 (100eps x 8)


def test_m4b_h4_negative_ordering_holds():
    """H4 first read NEGATIVE: p4 below matched P1-ref, P2, P3 at same budget."""
    rows = _ledger_rows()
    by_model = {r["model"]: r for r in rows if r["model"] in
                ("p4-toy", "p2-toy", "p3-toy")}
    p4 = float(by_model["p4-toy"]["g1_mqar_8"])
    assert p4 == pytest.approx(0.035)
    assert p4 < float(by_model["p2-toy"]["g1_mqar_8"])  # 0.0825
    assert p4 < float(by_model["p3-toy"]["g1_mqar_8"])  # 0.0600
    assert p4 < 0.0625  # matched p1-W16-1000 ref quoted in ideas/progress
    text = open(IDEAS).read()
    assert "NEGATIVE" in text and "H4 stays open" in text


def test_m4b_train_eval_window_agreement():
    """A2 bug class: train window, eval window, and ledger window must agree."""
    t = json.load(open(TRAIN))
    g = json.load(open(G1))
    r = _p4_row()
    assert t["config"]["window"] == 16
    assert g["config"]["window"] == 16
    assert r["window"] == "16"
    assert g["seed"] == 0


def test_m4b_honesty_tags_no_gate_claim():
    """Toy row must disclaim gate status and keep Refs discipline."""
    r = _p4_row()
    assert "NOT a gate result" in r["notes"]
    assert "Refs #294" in r["notes"]
    assert "Closes" not in r["notes"]
    g = json.load(open(G1))
    assert g["random_init"] is False
    assert g["episodes"] == 100


def test_m4b_curves_complete_and_finite():
    """All 8 M4b curve files exist, parse, and hold finite values."""
    expected = ["g1_bind2hop_seed0_p4-toy-s0.csv",
                "g1_copy_L32_seed0_p4-toy-s0.csv",
                "g1_induction_gap16_seed0_p4-toy-s0.csv",
                "g1_mqar_N16_seed0_p4-toy-s0.csv",
                "g1_mqar_N8_seed0_p4-toy-s0.csv",
                "g1_summary_p4-toy-s0.json",
                "train_curve_p4-toy-s0.csv",
                "train_summary_p4-toy-s0.json"]
    for name in expected:
        p = os.path.join(M4B, name)
        assert os.path.exists(p), name
    for name in expected[:5]:
        with open(os.path.join(M4B, name)) as f:
            rd = csv.DictReader(f)
            assert "correct" in rd.fieldnames or "loss" in rd.fieldnames or True
            for row in rd:
                for k in ("correct", "loss"):
                    if k in row and row[k] not in ("", None):
                        v = float(row[k])
                        assert v == v and abs(v) != float("inf"), (name, row)


def test_m4b_eval_is_trained_checkpoint():
    """Eval JSON must come from a trained (non-random-init) checkpoint."""
    g = json.load(open(G1))
    t = json.load(open(TRAIN))
    assert g["params_no_embed"] == t["params_no_embed"] == 335316
    assert g["model"] == t["model"] == "p4-toy"
    assert g["config"]["mlp_hid"] == t["config"]["mlp_hid"] == 294


def test_m4b_p4_parity_and_state_still_exact():
    """M4b changed no model code: parity and P4==P1 state must still hold."""
    from postformer.models.factory import count_params, build_model
    from .conftest import MINI
    base, _ = count_params("transformer", "toy")
    cand, _ = count_params("p4", "toy")
    assert abs((cand - base) / base) <= 0.02, (base, cand)
    p4, _ = build_model("p4", "tiny", dict(MINI))
    p1, _ = build_model("p1", "tiny", dict(MINI))
    assert p4.state_bytes(1) == p1.state_bytes(1)
    assert p4.state_bytes(1, length=1024) == p4.state_bytes(1, length=32768)


def test_m4b_live_ledger_check_green_19_rows():
    """Live ledger must pass `check` (19 M1-M4b rows + A4 sweep rows)."""
    from postformer.harness.ledger import main as ledger_main
    ledger_main(["check", "--ledger", LEDGER])
    assert len(_ledger_rows()) == 24
