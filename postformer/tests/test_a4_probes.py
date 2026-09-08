"""Builder A4 regression: P2 slot-count sweep honesty + ledger/curve integrity.

Refs #294 (toy proxies only, never gate results). Durable regression for the
A4 Builder delta: ledger rows p2-G0/G4/G64-toy (seed0, 0.528M tokens each)
plus the 24 curves under postformer/ledger/curves/a4-toy/ and the A4 ideas
entry. Findings pinned here: slots beat pure-SSD at toy N8, but G4/G16/G64
collapse to identical scores because toy episodes (T=33, stride 8) admit at
most 5 slot writes, so slot COUNT stays untested until S-tiny N64+.
"""

import csv
import json
import os

import pytest

REPO = os.path.join(os.path.dirname(__file__), "..")
LEDGER = os.path.join(REPO, "ledger", "ledger.csv")
A4 = os.path.join(REPO, "ledger", "curves", "a4-toy")
IDEAS = os.path.join(os.path.dirname(__file__), "..", "..", "ideas",
                     "2026-09-08-postformer-a4-slots-sweep.md")

VARIANTS = (0, 4, 64)
EXPECTED = {0: {"m8": 0.04625, "m16": 0.005625, "h2": 0.01},
            4: {"m8": 0.0825, "m16": 0.00125, "h2": 0.03},
            64: {"m8": 0.0825, "m16": 0.00125, "h2": 0.03}}


def _ledger_rows():
    with open(LEDGER) as f:
        return list(csv.DictReader(f))


def _row(g):
    rows = [r for r in _ledger_rows() if r["model"] == f"p2-G{g}-toy"]
    assert len(rows) == 1, f"expected exactly one p2-G{g}-toy row, got {len(rows)}"
    return rows[0]


def test_a4_ledger_rows_match_curve_json():
    """Ledger cells must be literal copies of the curve ground truth."""
    for g in VARIANTS:
        tag = f"p2-G{g}-toy-s0"
        summ = json.load(open(os.path.join(A4, f"g1_summary_{tag}.json")))
        r = _row(g)
        assert float(r["g1_mqar_8"]) == pytest.approx(summ["mqar"]["8"]["acc"])
        assert float(r["g1_mqar_16"]) == pytest.approx(summ["mqar"]["16"]["acc"])
        assert float(r["g1_2hop"]) == pytest.approx(summ["bind2hop"]["acc"])
        assert float(r["g1_induction"]) == pytest.approx(summ["induction"]["16"])
        assert float(r["g1_copy"]) == pytest.approx(summ["copying"]["32"])
        assert int(r["params"]) == summ["params_no_embed"] == 336074
        assert r["vocab"] == "64" and r["window"] == "16" and r["seed"] == "0"
        assert int(r["train_tokens"]) == 528000
        assert summ["config"]["slots"] == g
        assert summ["random_init"] is False


def test_a4_expected_scores():
    """Pin the measured A4 order: G0 below ref, G4/G64 equal at M3 G16 level."""
    for g in VARIANTS:
        r = _row(g)
        assert float(r["g1_mqar_8"]) == pytest.approx(EXPECTED[g]["m8"])
        assert float(r["g1_mqar_16"]) == pytest.approx(EXPECTED[g]["m16"])
        assert float(r["g1_2hop"]) == pytest.approx(EXPECTED[g]["h2"])
    g0 = float(_row(0)["g1_mqar_8"])
    g4 = float(_row(4)["g1_mqar_8"])
    assert g0 < 0.0625  # pure-SSD control below matched p1-W16-1000 ref
    assert g0 < g4  # slots help over pure SSD at toy N8


def test_a4_slot_count_ceiling_identity():
    """G4 and G64 summaries must agree exactly (<=5 writes at toy length)."""
    s4 = json.load(open(os.path.join(A4, "g1_summary_p2-G4-toy-s0.json")))
    s64 = json.load(open(os.path.join(A4, "g1_summary_p2-G64-toy-s0.json")))
    for task in ("mqar", "bind2hop", "induction", "copying"):
        assert s4[task] == s64[task], task
    t4 = json.load(open(os.path.join(A4, "train_summary_p2-G4-toy-s0.json")))
    t64 = json.load(open(os.path.join(A4, "train_summary_p2-G64-toy-s0.json")))
    assert t4["final_loss"] == t64["final_loss"]


def test_a4_params_identical_across_slots():
    """A4 is an honest ablation: slot count changes zero params."""
    from postformer.models.factory import count_params
    vals = set()
    for g in (0, 4, 16, 64):
        n, _ = count_params("p2", "toy", {"slots": g})
        vals.add(n)
    assert vals == {336074}, vals


def test_a4_train_eval_slots_agreement():
    """Slots bug class: train slots, eval slots, ledger label must agree."""
    for g in VARIANTS:
        tag = f"p2-G{g}-toy-s0"
        t = json.load(open(os.path.join(A4, f"train_summary_{tag}.json")))
        s = json.load(open(os.path.join(A4, f"g1_summary_{tag}.json")))
        assert t["config"]["slots"] == g
        assert s["config"]["slots"] == g
        assert t["params_no_embed"] == s["params_no_embed"] == 336074
        assert t["train_tokens"] == 528000 == 1000 * 16 * 33
        with open(os.path.join(A4, f"train_curve_{tag}.csv")) as f:
            curve = list(csv.DictReader(f))
        losses = [float(x["loss"]) for x in curve]
        assert all(l == l and abs(l) != float("inf") for l in losses)
        assert losses[-1] < losses[0], (losses[0], losses[-1])


def test_a4_honesty_tags_no_gate_claim():
    """Toy rows must disclaim gate status and keep Refs discipline."""
    for g in VARIANTS:
        r = _row(g)
        assert "NOT a gate result" in r["notes"]
        assert "Refs #294" in r["notes"]
        assert "Closes" not in r["notes"]
    text = open(IDEAS).read()
    assert "stays open" in text or "H2 stays open" in text


def test_a4_curves_complete_and_finite():
    """All 24 A4 curve files exist, parse, and hold finite values."""
    names = []
    for g in VARIANTS:
        tag = f"p2-G{g}-toy-s0"
        names += [f"g1_bind2hop_seed0_{tag}.csv",
                  f"g1_copy_L32_seed0_{tag}.csv",
                  f"g1_induction_gap16_seed0_{tag}.csv",
                  f"g1_mqar_N16_seed0_{tag}.csv",
                  f"g1_mqar_N8_seed0_{tag}.csv",
                  f"g1_summary_{tag}.json",
                  f"train_curve_{tag}.csv",
                  f"train_summary_{tag}.json"]
    for name in names:
        assert os.path.exists(os.path.join(A4, name)), name
    with open(os.path.join(A4, "g1_mqar_N8_seed0_p2-G4-toy-s0.csv")) as f:
        assert len(f.readlines()) == 801  # header + 800 (100eps x 8)
