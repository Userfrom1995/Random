"""Tester M4c red-team: hostile verification of the A4 slots sweep + M4b P4 probe.

Refs #294 (toy proxies only, never gate results). This suite independently
recomputes Builder claims from raw curve files (never trusting ledger cells
or summaries alone) and attacks the slot-count ceiling explanation
mechanistically. If any of these fail, the A4/M4b findings are fabrication
or mislabeling and the PR must go back to the Fixer.
"""

import csv
import hashlib
import json
import os

import pytest
import torch

REPO = os.path.join(os.path.dirname(__file__), "..")
LEDGER = os.path.join(REPO, "ledger", "ledger.csv")
A4 = os.path.join(REPO, "ledger", "curves", "a4-toy")
M4B = os.path.join(REPO, "ledger", "curves", "m4b-toy")


def _md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def _acc(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) > 0, path
    return sum(int(r["correct"]) for r in rows) / len(rows)


def _ledger_rows():
    with open(LEDGER) as f:
        return list(csv.DictReader(f))


def test_m4c_n8_csv_recompute_matches_ledger_cells():
    """Independent recompute: raw N8 CSV accuracy must equal ledger cells."""
    rows = {r["model"]: r for r in _ledger_rows()}
    for g in (0, 4, 64):
        csv_acc = _acc(os.path.join(A4, f"g1_mqar_N8_seed0_p2-G{g}-toy-s0.csv"))
        assert csv_acc == pytest.approx(float(rows[f"p2-G{g}-toy"]["g1_mqar_8"]))
        assert csv_acc == pytest.approx(
            json.load(open(os.path.join(A4, f"g1_summary_p2-G{g}-toy-s0.json")))
            ["mqar"]["8"]["acc"])


def _scored_signal(path):
    """Scored signal of a curve file: `correct` column if present, else raw bytes."""
    with open(path) as f:
        rows = list(csv.DictReader(f))
    if rows and "correct" in rows[0]:
        return ("correct", [r["correct"] for r in rows])
    return ("bytes", _md5(path))


def test_m4c_ceiling_byte_identity_g4_g64_g0_differs():
    """G4/G64 scored outcomes must be identical (ceiling); G0 must differ.

    Note: the N16 CSVs differ in the diagnostic `rank` tie-break column
    (more tied-zero slots under G64 shift tie ranks) while every scored
    `correct` outcome agrees, so identity is asserted on the scored
    signal, not raw bytes.
    """
    for name in ("g1_mqar_N8_seed0", "g1_mqar_N16_seed0",
                 "train_curve", "g1_bind2hop_seed0"):
        k4, s4 = _scored_signal(os.path.join(A4, f"{name}_p2-G4-toy-s0.csv"))
        k64, s64 = _scored_signal(os.path.join(A4, f"{name}_p2-G64-toy-s0.csv"))
        k0, s0 = _scored_signal(os.path.join(A4, f"{name}_p2-G0-toy-s0.csv"))
        assert k4 == k64 == k0, (name, k4, k64, k0)
        assert s4 == s64, f"{name} ({k4}): G4/G64 scored signals differ"
        assert s0 != s4, f"{name}: G0 unexpectedly identical to G4"


def test_m4c_train_loss_ordering_from_raw_curves():
    """Raw train curves: G0 final loss must exceed G4 final (slots help)."""
    def final(g):
        with open(os.path.join(A4, f"train_curve_p2-G{g}-toy-s0.csv")) as f:
            losses = [float(r["loss"]) for r in csv.DictReader(f)]
        assert all(l == l and abs(l) != float("inf") for l in losses)
        assert losses[-1] < losses[0]
        return losses[-1]
    assert final(0) > final(4)


def test_m4c_slot_write_ceiling_mechanism():
    """Mechanistic proof: T=33/stride8 admits at most 5 writes, so G>=5 identical."""
    from postformer.models.p2_slots import SlotBuffer
    for G in (5, 16, 64):
        buf = SlotBuffer(1, 2, 8, 8, G, 8, "cpu", torch.float32)
        for _ in range(33):
            buf.append(torch.randn(1, 2, 8), torch.randn(1, 2, 8))
        assert buf.writes <= 5, (G, buf.writes)
        assert buf.n <= 5, (G, buf.n)
    # slots=0 is a pure no-op that still advances the clock
    buf0 = SlotBuffer(1, 2, 8, 8, 0, 8, "cpu", torch.float32)
    buf0.append(torch.randn(1, 2, 8), torch.randn(1, 2, 8))
    assert buf0.n == 0 and buf0.writes == 0 and buf0.pos == 1
    with pytest.raises(ValueError):
        SlotBuffer(1, 2, 8, 8, -1, 8, "cpu", torch.float32)
    with pytest.raises(ValueError):
        SlotBuffer(1, 2, 8, 8, 4, 0, "cpu", torch.float32)


def test_m4c_g4_g64_jsons_differ_only_in_config():
    """G4/G64 summaries must agree on every score; only the label may differ."""
    s4 = json.load(open(os.path.join(A4, "g1_summary_p2-G4-toy-s0.json")))
    s64 = json.load(open(os.path.join(A4, "g1_summary_p2-G64-toy-s0.json")))
    for task in ("mqar", "bind2hop", "induction", "copying"):
        assert s4[task] == s64[task], task
    assert s4["config"]["slots"] == 4
    assert s64["config"]["slots"] == 64


def test_m4c_ledger_dedup_rejects_duplicate_slot_row(tmp_path):
    """Appending an existing (model,seed,vocab,window) key must fail; --force upserts."""
    import shutil
    from postformer.harness.ledger import main as ledger_main
    copy = str(tmp_path / "ledger.csv")
    shutil.copy(LEDGER, copy)
    # SCHEMA-shaped run-json colliding with the live p2-G4-toy row key
    dupe = str(tmp_path / "dupe.json")
    json.dump({"model": "p2-G4-toy", "params": 336074, "train_tokens": 528000,
               "seed": 0, "vocab": 64, "window": 16,
               "g1_mqar_8": 0.0825, "notes": "dupe probe Refs #294"}, open(dupe, "w"))
    with pytest.raises(SystemExit):
        ledger_main(["append", "--run-json", dupe, "--ledger", copy])
    # force upsert keeps row count stable
    before = len(list(csv.DictReader(open(copy))))
    ledger_main(["append", "--run-json", dupe, "--ledger", copy, "--force"])
    after = len(list(csv.DictReader(open(copy))))
    assert before == after == 24
    ledger_main(["check", "--ledger", copy])


def test_m4b_p4_csv_recompute_matches_ledger_cell():
    """M4b P4 probe: raw N8 CSV recompute must equal the ledger cell (anti-fabrication)."""
    csv_acc = _acc(os.path.join(M4B, "g1_mqar_N8_seed0_p4-toy-s0.csv"))
    rows = {r["model"]: r for r in _ledger_rows()}
    assert csv_acc == pytest.approx(float(rows["p4-toy"]["g1_mqar_8"]))
    assert csv_acc == pytest.approx(
        json.load(open(os.path.join(M4B, "g1_summary_p4-toy-s0.json")))["mqar"]["8"]["acc"])
    # H4 negative read: p4 below the matched p1 ref and below p2-G4
    assert csv_acc < float(rows["p2-G4-toy"]["g1_mqar_8"])
    assert "NOT a gate result" in rows["p4-toy"]["notes"]


def test_m4c_no_gate_claim_in_new_rows():
    """Every new M4b/M4c ledger row must disclaim gate status and keep Refs discipline."""
    rows = {r["model"]: r for r in _ledger_rows()}
    for m in ("p4-toy", "p2-G0-toy", "p2-G4-toy", "p2-G64-toy"):
        assert "NOT a gate result" in rows[m]["notes"], m
        assert "Refs #294" in rows[m]["notes"], m
        assert "Closes" not in rows[m]["notes"], m
