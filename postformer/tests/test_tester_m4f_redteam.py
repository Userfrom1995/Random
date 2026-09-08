"""Tester M4f red-team: hostile verification of the M4d A6 vocab-stress pilot
plus the (scale, vocab)-grouped param-drift gate.

Refs #294 (toy proxies only, never gate results). The Builder added A6
rows 23-24 (p1-toy vs transformer-toy at vocab512, both at floor 0.0) and
grouped the binding +-2% drift gate by (scale, vocab) so cross-vocab arms
are never compared. This suite recomputes the A6 cells from raw per-episode
CSVs (never trusting summary JSON or ledger cells alone), pins the
chance-floor honesty, and attacks the grouping boundary: same-(scale,vocab)
drift must still fail loudly while cross-vocab drift must not false-positive.
If any of these fail, the A6 provenance or the drift gate is fabrication
and the PR goes back to the Fixer.
"""

import csv
import json
import math
import os
import shutil

import pytest

from postformer.harness.ledger import main as ledger_main

REPO = os.path.join(os.path.dirname(__file__), "..")
LEDGER = os.path.join(REPO, "ledger", "ledger.csv")
A6 = os.path.join(REPO, "ledger", "curves", "a6-toy")
ARMS = ("p1-toy-V512-s0", "transformer-toy-V512-s0")


def _acc(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) > 0, path
    return sum(int(r["correct"]) for r in rows) / len(rows)


def _summary(arm):
    with open(os.path.join(A6, f"g1_summary_{arm}.json")) as f:
        return json.load(f)


def _ledger_rows():
    with open(LEDGER) as f:
        return list(csv.DictReader(f))


def test_m4f_a6_mqar_cells_recompute_from_raw_csvs():
    """Both A6 arms at 0.0 must recompute from raw N8 (800-row) CSVs."""
    for arm in ARMS:
        got8 = _acc(os.path.join(A6, f"g1_mqar_N8_seed0_{arm}.csv"))
        got16 = _acc(os.path.join(A6, f"g1_mqar_N16_seed0_{arm}.csv"))
        s = _summary(arm)
        assert got8 == pytest.approx(s["mqar"]["8"]["acc"], abs=1e-9), (arm, got8)
        assert got16 == pytest.approx(s["mqar"]["16"]["acc"], abs=1e-9), (arm, got16)
        assert got8 == 0.0 and got16 == 0.0, (arm, got8, got16)


def test_m4f_a6_envelope_recomputes_at_floor():
    """2hop/induction/copy 0.0 for both arms must recompute from raw CSVs."""
    for arm in ARMS:
        h = _acc(os.path.join(A6, f"g1_bind2hop_seed0_{arm}.csv"))
        ind = _acc(os.path.join(A6, f"g1_induction_gap16_seed0_{arm}.csv"))
        cop = _acc(os.path.join(A6, f"g1_copy_L32_seed0_{arm}.csv"))
        s = _summary(arm)
        assert h == pytest.approx(s["bind2hop"]["acc"], abs=1e-9), (arm, h)
        assert ind == pytest.approx(s["induction"]["16"], abs=1e-9), (arm, ind)
        assert cop == pytest.approx(s["copying"]["32"], abs=1e-9), (arm, cop)
        assert h == 0.0 and ind == 0.0 and cop == 0.0, (arm, h, ind, cop)


def test_m4f_a6_train_loss_near_chance_and_params_match_ledger():
    """Final loss must sit near ln(512) (chance) and params must match ledger."""
    rows = {r["model"] + "|vocab=" + r["vocab"]: r for r in _ledger_rows()}
    for arm, model in (("p1-toy-V512-s0", "p1-toy"),
                       ("transformer-toy-V512-s0", "transformer-toy")):
        with open(os.path.join(A6, f"train_summary_{arm}.json")) as f:
            t = json.load(f)
        assert math.isfinite(t["final_loss"]), (arm, t)
        assert t["final_loss"] == pytest.approx(math.log(512), abs=0.15), t
        assert t["config"]["vocab_size"] == 514, t["config"]
        row = rows[model + "|vocab=512"]
        assert int(row["params"]) == t["params_no_embed"], (row, t)
        assert "NOT a gate result" in row["notes"], row["notes"]


def test_m4f_a6_ledger_cells_match_summaries():
    """Ledger g1_mqar_8/16 cells for both A6 rows must equal summary accs."""
    rows = {r["model"]: r for r in _ledger_rows() if r.get("vocab") == "512"}
    assert set(rows) == {"p1-toy", "transformer-toy"}, set(rows)
    for model in rows:
        arm = model + "-V512-s0"
        s = _summary(arm)
        assert float(rows[model]["g1_mqar_8"]) == pytest.approx(
            s["mqar"]["8"]["acc"], abs=1e-9), (model, rows[model])
        assert float(rows[model]["g1_mqar_16"]) == pytest.approx(
            s["mqar"]["16"]["acc"], abs=1e-9), (model, rows[model])


def test_m4f_same_vocab_drift_still_fails_loudly(tmp_path, capsys):
    """A >2% drifter at an existing (scale, vocab) must fail check on drift."""
    copy = str(tmp_path / "ledger.csv")
    shutil.copy(LEDGER, copy)
    bad = str(tmp_path / "bad.json")
    json.dump({"model": "p1-toy", "params": 1, "train_tokens": 528000,
               "seed": 9, "vocab": 64, "window": 16, "g1_mqar_8": 0.05,
               "notes": "same-vocab drift probe Refs #294"}, open(bad, "w"))
    ledger_main(["append", "--run-json", bad, "--ledger", copy, "--force"])
    with pytest.raises(SystemExit):
        ledger_main(["check", "--ledger", copy])
    assert "param drift" in capsys.readouterr().out


def test_m4f_cross_vocab_drift_does_not_false_positive(tmp_path):
    """A wild-params arm at a vocab with no transformer baseline must pass."""
    copy = str(tmp_path / "ledger.csv")
    shutil.copy(LEDGER, copy)
    odd = str(tmp_path / "odd.json")
    json.dump({"model": "p1-toy", "params": 999999999,
               "train_tokens": 528000, "seed": 9, "vocab": 999,
               "window": 16, "g1_mqar_8": 0.05,
               "notes": "cross-vocab grouping probe Refs #294"}, open(odd, "w"))
    ledger_main(["append", "--run-json", odd, "--ledger", copy, "--force"])
    ledger_main(["check", "--ledger", copy])


def test_m4f_a6_ideas_entry_honest_refs():
    """A6 ideas entry must exist, say Refs #294, and never claim Closes."""
    path = os.path.join(REPO, "..", "ideas",
                        "2026-09-08-postformer-a6-vocab-pilot.md")
    path = os.path.normpath(path)
    with open(path) as f:
        text = f.read()
    assert "Refs #294" in text, path
    assert "Closes #294" not in text, path
