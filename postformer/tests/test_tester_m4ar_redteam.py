"""Tester M4ar red-team: hostile audit of the A4 G4/G64 divergence disclosure (Refs #294).

Novel vs all prior suites: test_a4_probes.py pins pred_flips == 7 and the
m4* suites cover training paths, parity, and guards. Nothing independently
interrogates the Fixer's scoped claim (summary-cell equality + per-episode
N16 divergence + G4-eviction mechanism + bit-identical train curves). This
suite attacks that disclosure from seven hostile angles, all CPU-fast
(CSV reads + a tiny live SlotBuffer simulation, no training):

  1. Flips must be wrong-answer reshuffle ONLY (correct==0 both sides);
     any correctness flip breaks the summary-equality story -> tripwire.
  2. OOV-pred dominance: both arms must sit at the N16 noise floor
     (acc < chance 1/64, OOV '64' on >97% of rows) so N16 cannot be
     misread as signal later.
  3. Train/eval paradox: train curves byte-identical while eval N16
     CSVs differ -> pins the disclosed anomaly durably.
  4. Live eviction mechanism: SlotBuffer(G=4, stride=8) over 33 positions
     must record exactly 5 writes, hold 4, and evict position 0;
     G=5 must retain all 5. Proves the prose claim in code.
  5. Summaries differ ONLY in config.slots (no hidden score drift).
  6. Flips scattered across >=5 distinct episodes (rules out a single
     corrupt-episode artifact).
  7. Disclosure tripwire: envelope-audit.md and the A4 ideas entry must
     keep the divergence wording; ledger check green on 25 rows.
"""

import csv
import hashlib
import json
import os

import torch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
A4 = os.path.join(REPO_ROOT, "postformer", "ledger", "curves", "a4-toy")
N16_G4 = os.path.join(A4, "g1_mqar_N16_seed0_p2-G4-toy-s0.csv")
N16_G64 = os.path.join(A4, "g1_mqar_N16_seed0_p2-G64-toy-s0.csv")


def _rows(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def _flips():
    r4, r64 = _rows(N16_G4), _rows(N16_G64)
    assert len(r4) == len(r64) == 1600
    return r4, r64, [(a, b) for a, b in zip(r4, r64) if a["pred"] != b["pred"]]


def test_ar1_flips_are_wrong_answer_reshuffle_only():
    """No flip may change correctness; acc must sit below chance."""
    r4, r64, flips = _flips()
    assert len(flips) == 7, len(flips)
    for a, b in flips:
        assert a["correct"] == b["correct"] == "0", (a, b)
    acc4 = sum(int(r["correct"]) for r in r4) / len(r4)
    acc64 = sum(int(r["correct"]) for r in r64) / len(r64)
    assert acc4 == acc64 == 0.00125, (acc4, acc64)
    assert acc4 < 1 / 64, "N16 arm above chance: no longer noise floor"


def test_ar2_oov_pred_dominance_both_arms():
    """Both arms must predict OOV '64' on >97% of N16 rows (noise floor)."""
    r4, r64, _ = _flips()
    oov4 = sum(1 for r in r4 if r["pred"] == "64")
    oov64 = sum(1 for r in r64 if r["pred"] == "64")
    assert oov4 / len(r4) > 0.97, oov4
    assert oov64 / len(r64) > 0.97, oov64
    assert oov4 == 1562, oov4
    assert oov64 == 1569, oov64


def test_ar3_train_identical_eval_differs_paradox():
    """Train curves byte-identical AND eval N16 differs: pin the paradox."""
    for name in ("train_curve_p2-G4-toy-s0.csv",
                 "train_curve_p2-G64-toy-s0.csv"):
        assert os.path.exists(os.path.join(A4, name)), name
    h = lambda n: hashlib.md5(open(os.path.join(A4, n), "rb").read()
                              ).hexdigest()
    assert h("train_curve_p2-G4-toy-s0.csv") == \
        h("train_curve_p2-G64-toy-s0.csv") == \
        "b91888eef367316fef3e31702cad9539", \
        "G4/G64 train curves diverged: identical-training claim broken"
    assert h("g1_mqar_N16_seed0_p2-G4-toy-s0.csv") != \
        h("g1_mqar_N16_seed0_p2-G64-toy-s0.csv"), \
        "eval N16 CSVs identical now: divergence silently vanished"
    t4 = json.load(open(os.path.join(A4, "train_summary_p2-G4-toy-s0.json")))
    t64 = json.load(open(os.path.join(A4, "train_summary_p2-G64-toy-s0.json")))
    assert t4["final_loss"] == t64["final_loss"] == 3.942723035812378, \
        (t4["final_loss"], t64["final_loss"])


def test_ar4_live_eviction_mechanism_g4_vs_g5():
    """SlotBuffer live: G4/stride8 over T=33 writes 5, holds 4, evicts pos0."""
    from postformer.models.p2_slots import SlotBuffer
    for slots, keep in ((4, [8, 16, 24, 32]), (5, [0, 8, 16, 24, 32])):
        buf = SlotBuffer(1, 2, 8, 8, slots, 8, "cpu", torch.float32)
        for pos in range(33):
            k = torch.full((1, 2, 8), float(pos))
            v = torch.full((1, 2, 8), float(-pos))
            buf.append(k, v)
        assert buf.writes == 5, (slots, buf.writes)
        assert buf.n == slots, (slots, buf.n)
        got = sorted(int(x) for x in buf.keys[0, 0, :, 0].tolist())
        assert got == keep, (slots, got)
        gotv = sorted(int(x) for x in buf.vals[0, 0, :, 0].tolist())
        assert gotv == sorted(-p for p in keep), (slots, gotv)
    # slots=0 control: clock advances, nothing stored.
    buf0 = SlotBuffer(1, 2, 8, 8, 0, 8, "cpu", torch.float32)
    for pos in range(33):
        buf0.append(torch.zeros(1, 2, 8), torch.zeros(1, 2, 8))
    assert buf0.writes == 0 and buf0.n == 0 and buf0.pos == 33


def test_ar5_summaries_differ_only_in_config_slots():
    """Flattened G4/G64 summaries must differ in exactly one leaf."""
    s4 = json.load(open(os.path.join(A4, "g1_summary_p2-G4-toy-s0.json")))
    s64 = json.load(open(os.path.join(A4, "g1_summary_p2-G64-toy-s0.json")))

    def flat(d, p=""):
        for k, v in d.items():
            if isinstance(v, dict):
                yield from flat(v, p + str(k) + ".")
            else:
                yield (p + str(k), v)

    d4, d64 = dict(flat(s4)), dict(flat(s64))
    diffs = [k for k in set(d4) | set(d64) if d4.get(k) != d64.get(k)]
    assert diffs == ["config.slots"], diffs
    assert d4["config.slots"] == 4 and d64["config.slots"] == 64


def test_ar6_flips_scattered_across_episodes():
    """The 7 flips must span >=5 distinct episodes (no single-episode rot)."""
    _, _, flips = _flips()
    eps = {a["episode"] for a, _ in flips}
    assert len(eps) >= 5, sorted(eps)


def test_ar7_disclosure_wording_and_ledger_green():
    """Docs must keep the divergence disclosure; ledger check green."""
    env = open(os.path.join(REPO_ROOT, "postformer", "docs",
                            "envelope-audit.md")).read()
    assert "7 pred flips" in env, "envelope audit dropped the flip count"
    assert "evict" in env, "envelope audit dropped the eviction note"
    ideas = open(os.path.join(
        REPO_ROOT, "ideas", "2026-09-08-postformer-a4-slots-sweep.md")).read()
    assert "7 pred flips" in ideas, "A4 ideas entry dropped the flip count"
    from postformer.harness.ledger import main as ledger_main
    ledger_main(["check", "--ledger",
                 os.path.join(REPO_ROOT, "postformer", "ledger",
                              "ledger.csv")])
    rows = _rows(os.path.join(REPO_ROOT, "postformer", "ledger", "ledger.csv"))
    assert len(rows) == 25, len(rows)
