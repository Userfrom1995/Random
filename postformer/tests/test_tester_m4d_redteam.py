"""Tester M4d red-team: hostile verification of the ledger _key str-normalization fix.

Refs #294 (toy proxies only, never gate results). The Fixer normalized
_key to str so int-typed run-json dupes are rejected; this suite attacks
the type-confusion boundary (str "0" vs int 0) plus NaN strictness.
If any of these fail, the dedup guard is bypassable and the PR goes back
to the Fixer.
"""

import csv
import json
import shutil

import pytest

from postformer.harness.ledger import main as ledger_main

LEDGER = "postformer/ledger/ledger.csv"


def _rows(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def test_m4d_str_typed_dupe_rejected(tmp_path):
    """A dupe with seed/vocab/window as STRINGS must hit the same key as ints."""
    copy = str(tmp_path / "ledger.csv")
    shutil.copy(LEDGER, copy)
    dupe = str(tmp_path / "dupe.json")
    json.dump({"model": "p2-G4-toy", "params": 336074, "train_tokens": 528000,
               "seed": "0", "vocab": "64", "window": "16",
               "g1_mqar_8": 0.0825, "notes": "str-type dupe probe Refs #294"},
              open(dupe, "w"))
    with pytest.raises(SystemExit):
        ledger_main(["append", "--run-json", dupe, "--ledger", copy])
    assert len(_rows(copy)) == 22


def test_m4d_nan_gate_value_rejected(tmp_path):
    """NaN in a filled gate cell must fail check loudly, never pass silently."""
    copy = str(tmp_path / "ledger.csv")
    shutil.copy(LEDGER, copy)
    bad = str(tmp_path / "bad.json")
    json.dump({"model": "p9-probe-toy", "params": 1, "train_tokens": 1,
               "seed": 9, "vocab": 64, "window": 16,
               "g1_mqar_8": float("nan"), "notes": "nan probe Refs #294"},
              open(bad, "w"))
    ledger_main(["append", "--run-json", bad, "--ledger", copy, "--force"])
    with pytest.raises(SystemExit):
        ledger_main(["check", "--ledger", copy])
