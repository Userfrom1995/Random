"""T5: ledger schema - check rejects missing cols, NaN gates, param drift."""

import csv
import os
import tempfile

import pytest

from postformer.harness.ledger import SCHEMA, main as ledger_main


def write(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA)
        w.writeheader()
        w.writerows(rows)


def good_row(model="p1-tiny", params="29373756"):
    return {"model": model, "params": params, "train_tokens": "0", "seed": "0",
            "vocab": "8192", "window": "128",
            "g1_mqar_8": "", "g1_mqar_16": "0.1", "g1_mqar_64": "", "g1_mqar_256": "",
            "g1_induction": "", "g1_copy": "", "g1_2hop": "",
            "g2_bpb_1x": "", "g2_bpb_4x": "", "g2_bpb_8x": "",
            "g2_delta_4x": "", "g2_delta_8x": "",
            "g3_valid_bpb": "", "g3_test_bpb": "",
            "g4_state_bytes": "", "g4_ms_per_token": "", "gpu_hours": "0",
            "notes": "smoke"}


def base_row():
    r = good_row(model="transformer-tiny", params="29366784")
    r["window"] = ""  # the baseline has no sliding window
    return r


def test_check_accepts_good():
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "ledger.csv")
        write(p, [base_row(), good_row()])
        ledger_main(["check", "--ledger", p])


def test_check_rejects_nan():
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "ledger.csv")
        r = good_row()
        r["g1_mqar_16"] = "nan"
        write(p, [base_row(), r])
        with pytest.raises(SystemExit):
            ledger_main(["check", "--ledger", p])


def test_check_rejects_drift():
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "ledger.csv")
        write(p, [base_row(), good_row(params="99999999")])
        with pytest.raises(SystemExit):
            ledger_main(["check", "--ledger", p])


def test_check_rejects_schema():
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "ledger.csv")
        with open(p, "w") as f:
            f.write("model,seed\np1-tiny,0\n")
        with pytest.raises(SystemExit):
            ledger_main(["check", "--ledger", p])


def _run_json(tmp, row):
    import json
    p = os.path.join(tmp, "run.json")
    with open(p, "w") as f:
        json.dump(row, f)
    return p


def test_append_rejects_duplicate_without_force():
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "ledger.csv")
        r = _run_json(tmp, good_row())
        ledger_main(["append", "--run-json", r, "--ledger", p])
        with pytest.raises(SystemExit):
            ledger_main(["append", "--run-json", r, "--ledger", p])
        ledger_main(["check", "--ledger", p])


def test_append_force_upserts():
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "ledger.csv")
        r = _run_json(tmp, good_row())
        ledger_main(["append", "--run-json", r, "--ledger", p])
        row2 = good_row()
        row2["g1_mqar_16"] = "0.2"
        r2 = _run_json(tmp, row2)
        ledger_main(["append", "--run-json", r2, "--ledger", p, "--force"])
        ledger_main(["check", "--ledger", p])
        with open(p) as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 1 and rows[0]["g1_mqar_16"] == "0.2"


def test_append_window_variants_share_model_seed():
    # A2 ablations legitimately share (model, seed); window disambiguates.
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "ledger.csv")
        for w in ("0", "16", "32"):
            row = good_row()
            row["window"] = w
            ledger_main(["append", "--run-json", _run_json(tmp, row),
                         "--ledger", p])
        ledger_main(["check", "--ledger", p])
        with open(p) as f:
            assert len(list(csv.DictReader(f))) == 3


def test_check_rejects_empty_row_without_tag():
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "ledger.csv")
        empty = good_row()
        for c in ("g1_mqar_8", "g1_mqar_16"):
            empty[c] = ""
        empty["notes"] = "fresh row"
        write(p, [base_row(), empty])
        with pytest.raises(SystemExit):
            ledger_main(["check", "--ledger", p])
