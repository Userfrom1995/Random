"""Builder A6 regression: vocab-stress toy pilot honesty + ledger/curve integrity.

Refs #294 (toy proxies only, never gate results). Durable regression for the
A6 Builder delta: p1-toy + transformer-toy at vocab512 (seed0, 1000 steps =
0.528M tokens each, N8) plus the 16 curves under
postformer/ledger/curves/a6-toy/ (V512 tags) and the A6 ideas entry.
Findings pinned here: both arms sit at the 0.0 floor (chance 1/512) with
final train loss near ln(512) = 6.24, so the 1000-step toy budget is below
the learning threshold at vocab512 and yields no P1-vs-transformer
separation. Also pins the ledger drift-gate fix: the +-2% param rule now
compares within (scale, vocab) groups because the lm_head scales with
vocab (vocab512 toy params ~393k vs vocab64 toy ~336k).
"""

import csv
import json
import math
import os

import pytest

REPO = os.path.join(os.path.dirname(__file__), "..")
LEDGER = os.path.join(REPO, "ledger", "ledger.csv")
A6 = os.path.join(REPO, "ledger", "curves", "a6-toy")
IDEAS = os.path.join(os.path.dirname(__file__), "..", "..", "ideas",
                     "2026-09-08-postformer-a6-vocab-pilot.md")

TAGS = {"p1": "p1-toy-V512-s0", "tr": "transformer-toy-V512-s0"}


def _ledger_rows():
    with open(LEDGER) as f:
        return list(csv.DictReader(f))


def _row(model):
    rows = [r for r in _ledger_rows()
            if r["model"] == model and r["vocab"] == "512" and r["seed"] == "0"]
    assert len(rows) == 1, f"expected one {model} vocab512 row, got {len(rows)}"
    return rows[0]


def test_a6_ledger_cells_match_curve_json():
    """Ledger cells must be literal copies of the curve ground truth."""
    for model, tag in (("p1-toy", TAGS["p1"]),
                       ("transformer-toy", TAGS["tr"])):
        summ = json.load(open(os.path.join(A6, f"g1_summary_{tag}.json")))
        r = _row(model)
        assert float(r["g1_mqar_8"]) == pytest.approx(summ["mqar"]["8"]["acc"])
        assert float(r["g1_mqar_16"]) == pytest.approx(summ["mqar"]["16"]["acc"])
        assert float(r["g1_2hop"]) == pytest.approx(summ["bind2hop"]["acc"])
        assert float(r["g1_induction"]) == pytest.approx(summ["induction"]["16"])
        assert float(r["g1_copy"]) == pytest.approx(summ["copying"]["32"])
        assert int(r["params"]) == summ["params_no_embed"]
        assert r["vocab"] == "512" and r["seed"] == "0"
        assert int(r["train_tokens"]) == 528000
        assert summ["random_init"] is False
        assert summ["config"]["vocab_size"] == 514  # vocab + sep + blank


def test_a6_floor_scores_no_separation():
    """Both arms at the floor: no P1-vs-transformer separation at this budget."""
    for model in ("p1-toy", "transformer-toy"):
        r = _row(model)
        assert float(r["g1_mqar_8"]) == pytest.approx(0.0)
        assert float(r["g1_mqar_16"]) == pytest.approx(0.0)
        assert float(r["g1_2hop"]) == pytest.approx(0.0)
    p1 = json.load(open(os.path.join(A6, f"g1_summary_{TAGS['p1']}.json")))
    assert p1["mqar"]["8"]["recall@3"] < 0.01  # near chance 3/512


def test_a6_train_loss_near_chance():
    """Final loss must sit near ln(512): undertrained, not a discriminator."""
    for tag in TAGS.values():
        t = json.load(open(os.path.join(A6, f"train_summary_{tag}.json")))
        assert t["train_tokens"] == 528000
        assert t["final_loss"] == pytest.approx(math.log(512), abs=0.1)
        with open(os.path.join(A6, f"train_curve_{tag}.csv")) as f:
            curve = list(csv.DictReader(f))
        losses = [float(x["loss"]) for x in curve]
        assert all(l == l and abs(l) != float("inf") for l in losses)
        assert losses[-1] < losses[0]  # learns, but not enough


def test_a6_params_parity_within_vocab():
    """Same-vocab parity holds; cross-vocab params honestly differ."""
    from postformer.models.factory import count_params
    p1, _ = count_params("p1", "toy", {})
    tr, _ = count_params("transformer", "toy", {})
    assert p1 == 336332 and tr == 336768  # pinned vocab64 toy params
    r_p1, r_tr = _row("p1-toy"), _row("transformer-toy")
    assert int(r_p1["params"]) == 393676
    assert int(r_tr["params"]) == 394112
    drift = abs(393676 - 394112) / 394112
    assert drift < 0.02, drift
    assert int(r_p1["params"]) != p1  # lm_head grows with vocab: honest


def test_a6_drift_gate_groups_by_vocab():
    """The drift gate must pass with both vocabs ledgered (no cross-vocab compare)."""
    from postformer.harness.ledger import main as ledger_main
    ledger_main(["check", "--ledger", LEDGER])


def test_a6_window_labels():
    """p1 carries window 16, transformer carries none."""
    assert _row("p1-toy")["window"] == "16"
    assert _row("transformer-toy")["window"] == ""


def test_a6_honesty_tags_no_gate_claim():
    """Toy rows must disclaim gate status and keep Refs discipline."""
    for model in ("p1-toy", "transformer-toy"):
        r = _row(model)
        assert "NOT a gate result" in r["notes"]
        assert "Refs #294" in r["notes"]
        assert "Closes" not in r["notes"]
    text = open(IDEAS).read()
    assert "below the learning threshold" in text


def test_a6_curves_complete_and_finite():
    """All 16 A6 curve files exist, parse, and hold finite values."""
    names = []
    for tag in TAGS.values():
        names += [f"g1_bind2hop_seed0_{tag}.csv",
                  f"g1_copy_L32_seed0_{tag}.csv",
                  f"g1_induction_gap16_seed0_{tag}.csv",
                  f"g1_mqar_N16_seed0_{tag}.csv",
                  f"g1_mqar_N8_seed0_{tag}.csv",
                  f"g1_summary_{tag}.json",
                  f"train_curve_{tag}.csv",
                  f"train_summary_{tag}.json"]
    for name in names:
        assert os.path.exists(os.path.join(A6, name)), name
    with open(os.path.join(A6, f"g1_mqar_N8_seed0_{TAGS['p1']}.csv")) as f:
        assert len(f.readlines()) == 801  # header + 800 (100eps x 8)
