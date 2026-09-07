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
            "g1_mqar_16": "0.1", "g1_mqar_64": "", "g1_mqar_256": "",
            "g1_induction": "", "g1_copy": "", "g1_2hop": "",
            "g2_bpb_1x": "", "g2_bpb_4x": "", "g2_bpb_8x": "",
            "g2_delta_4x": "", "g2_delta_8x": "",
            "g3_valid_bpb": "", "g3_test_bpb": "",
            "g4_state_bytes": "", "g4_ms_per_token": "", "gpu_hours": "0",
            "notes": "smoke"}


def base_row():
    return good_row(model="transformer-tiny", params="29366784")


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
