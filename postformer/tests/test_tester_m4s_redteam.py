"""Tester M4s hostile suite: full curve ground truth + small-scale gates at head.

Refs #294 (toy/tiny/small analytic checks only, never gate results).

Why this suite exists: head carries 25 ledger rows with curve provenance
spread over m2-toy (9 matched-budget summaries), m3-toy (6 probe summaries),
a4-toy (3 slot-sweep summaries), a6-toy and m4b-toy (pinned by the M4r
suite). Prior suites pin m4b/a6 plus tiny parity/flatness/causality. This
suite pins the remaining CPU-verifiable ground truth so no future edit can
silently rewrite history or drift the docs:

- S1 (m2 matched-budget ground truth): all 9 m2-toy g1_summary JSONs
  (p1/p5/transformer x s0/s1/s2) agree with their ledger cells (N8 exact,
  N16 within ledger-rounding 5e-4, params_no_embed exact).
- S2 (m3 probe ground truth): the 6 m3-toy summaries agree with ledger
  cells/notes (p2 0.0825, p3 0.0600, p3-noacc 0.06125, W0 0.0875,
  W16-ref 0.0625, W32 0.05125 vs note-rounded 0.0512).
- S3 (a4 sweep ground truth): G0/G4/G64 summaries agree with ledger cells
  and their config slots field matches the sweep arm (0/4/64).
- S4 (small parity live): all five candidates within 2% of
  transformer-small (tiny-only was pinned before; small never was).
- S5 (small flatness live): every recurrent family T-flat at small
  (1k vs 32k equal); transformer-small grows ~32x (linear control).
- S6 (proof-vs-code at small): proof-g4.md states S-small P1 7864320 B,
  exactly matching live state_bytes(); pre-fix values are labeled as such.
"""

import csv
import glob
import json
import os

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURVES = os.path.join(REPO, "ledger", "curves")
LEDGER = os.path.join(REPO, "ledger", "ledger.csv")
PROOF = os.path.join(REPO, "docs", "proof-g4.md")


def _ledger_rows():
    with open(LEDGER, newline="") as f:
        return list(csv.DictReader(f))


def _m2_row(rows, model, seed):
    want_window = "" if model.startswith("transformer") else "16"
    cands = [r for r in rows
             if r["model"] == model and r["seed"] == str(seed)
             and r["window"] == want_window and r["vocab"] == "64"
             and r["train_tokens"] == "1584000"]
    assert len(cands) == 1, (model, seed, len(cands))
    return cands[0]


def test_s1_m2_matched_budget_ground_truth():
    rows = _ledger_rows()
    for model in ("p1-toy", "p5-toy", "transformer-toy"):
        for seed in (0, 1, 2):
            path = os.path.join(CURVES, "m2-toy",
                                f"g1_summary_{model}-s{seed}.json")
            with open(path) as f:
                s = json.load(f)
            row = _m2_row(rows, model, seed)
            assert abs(s["mqar"]["8"]["acc"] - float(row["g1_mqar_8"])) < 1e-9, path
            # Ledger G1 cells are 3-decimal roundings of the curve value
            # (e.g. curve 0.0925 -> cell 0.092 via round-half-even).
            assert abs(round(s["mqar"]["16"]["acc"], 3)
                       - float(row["g1_mqar_16"])) < 1e-9, path
            assert s["params_no_embed"] == int(row["params"]), path
            assert s["random_init"] is False, path


def test_s2_m3_probe_ground_truth():
    rows = _ledger_rows()
    by_model = {}
    for r in rows:
        by_model.setdefault(r["model"], []).append(r)
    cases = [
        ("m3-toy/p2-mqar/g1_summary_seed0.json", "p2-toy", "g1_mqar_8", 0.0825),
        ("m3-toy/p3-mqar/g1_summary_seed0.json", "p3-toy", "g1_mqar_8", 0.0600),
        ("m3-toy/p3-noacc-mqar/g1_summary_seed0.json", "p3-toy", "g1_mqar_8", 0.06125),
    ]
    for rel, model, col, expect in cases:
        with open(os.path.join(CURVES, rel)) as f:
            s = json.load(f)
        assert abs(s["mqar"]["8"]["acc"] - expect) < 1e-9, rel
        matches = [r for r in by_model[model] if abs(float(r[col]) - expect) < 1e-9]
        assert matches, (rel, model, col, expect)
    a2_notes = " ".join(r["notes"] for r in rows if r["model"] == "p1-toy")
    w_vals = {}
    for rel in ("m3-toy/p1-W0-mqar/g1_summary_seed0.json",
                "m3-toy/p1-W16-mqar/g1_summary_seed0.json",
                "m3-toy/p1-W32-mqar/g1_summary_seed0.json"):
        with open(os.path.join(CURVES, rel)) as f:
            s = json.load(f)
        w_vals[rel] = s["mqar"]["8"]["acc"]
    assert abs(w_vals["m3-toy/p1-W0-mqar/g1_summary_seed0.json"] - 0.0875) < 1e-9
    assert abs(w_vals["m3-toy/p1-W16-mqar/g1_summary_seed0.json"] - 0.0625) < 1e-9
    assert abs(w_vals["m3-toy/p1-W32-mqar/g1_summary_seed0.json"] - 0.05125) < 1e-9
    for disclosed in ("0.0875", "0.0625", "0.0512"):
        assert disclosed in a2_notes, disclosed


def test_s3_a4_slots_sweep_ground_truth():
    rows = _ledger_rows()
    for g, expect in (("G0", 0.04625), ("G4", 0.0825), ("G64", 0.0825)):
        path = os.path.join(CURVES, "a4-toy", f"g1_summary_p2-{g}-toy-s0.json")
        with open(path) as f:
            s = json.load(f)
        assert abs(s["mqar"]["8"]["acc"] - expect) < 1e-9, path
        assert s["config"]["slots"] == int(g[1:]), (path, s["config"]["slots"])
        cands = [r for r in rows if r["model"] == "p2-toy"
                 and r["slots"] == str(int(g[1:]))
                 and r["train_tokens"] == "528000"]
        assert cands, (g, expect)
        assert abs(float(cands[0]["g1_mqar_8"]) - expect) < 1e-9, (g, cands[0])


def test_s4_small_parity_live_within_2pct():
    from postformer.models.factory import count_params
    base, _ = count_params("transformer", "small")
    assert base == 113462016, base
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        p, _ = count_params(fam, "small")
        drift = abs(p - base) / base
        assert drift < 0.02, (fam, p, base, drift)


def test_s5_small_state_flatness_live():
    from postformer.models.factory import build_model
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        m, _ = build_model(fam, "small")
        lo, hi = m.state_bytes(1, 1024), m.state_bytes(1, 32768)
        assert lo == hi, (fam, lo, hi)
    mt, _ = build_model("transformer", "small")
    lo, hi = mt.state_bytes(1, 1024), mt.state_bytes(1, 32768)
    assert hi > 30 * lo, (lo, hi)


def test_s6_proof_small_p1_pin_matches_live_code():
    from postformer.models.factory import build_model
    m, _ = build_model("p1", "small")
    live = m.state_bytes(1, 1024)
    with open(PROOF) as f:
        src = f.read()
    assert "x12 = 7864320 B" in src
    assert live == 7864320, live
    assert "7864608 (small)" in src, "pre-fix small value must stay labeled"


def test_s7_no_orphan_curve_dirs_without_ledger_provenance():
    rows = _ledger_rows()
    notes = " ".join(r["notes"] for r in rows)
    for frag in ("m2-toy", "m3-toy", "A4", "a6-toy", "m4b-toy"):
        assert frag in notes, frag
    for path in glob.glob(os.path.join(CURVES, "m3-toy", "*-mqar", "g1_summary_seed0.json")):
        with open(path) as f:
            s = json.load(f)
        assert s["episodes"] == 100, path
        assert s["mqar"]["8"]["n"] == 800, path
    for path in glob.glob(os.path.join(CURVES, "m3-toy", "*-bind2hop", "g1_summary_seed0.json")):
        with open(path) as f:
            s = json.load(f)
        assert s["episodes"] == 100, path
        assert "bind2hop" in s, path
