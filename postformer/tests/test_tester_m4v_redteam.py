"""Tester M4v hostile suite: head-level live pins for M4b probe honesty,
guard execution paths, flatness, and doc hygiene.

Refs #294 (toy/tiny analytic checks only, never gate results).

Why this suite exists: 246 tests pass at head, but these live
behaviors were verified by hand (not pinned by any suite), so a
future edit could silently regress them:

- V1 (m4b ledger-vs-curve agreement): ledger g1 cells for the p4-toy
  M4b probe must equal the curve JSON ground truth (0.035 / 0.015625).
- V2 (p4 --window 0 live): M4a fixed p4 window routing; this executes
  a 1-episode eval with --window 0 and asserts it runs and inherits.
- V3 (transformer --window refusal live): must SystemExit loudly.
- V4 (N>vocab refusal live, correct flag): --n-pairs above --vocab
  must refuse loudly before sampling.
- V5 (P4==P1 state bytes live at toy): state_bytes flat 1k vs 32k
  and equal across P1/P4 (G4 tier-a/b shared inventory claim).
- V6 (no em dashes in head docs): changed docs/ideas/progress files
  must contain zero U+2014 (lab formatting invariant).
"""

import csv
import json
import subprocess
import sys

import torch

from postformer.models.factory import build_model


def _ledger_p4_row():
    with open("postformer/ledger/ledger.csv", newline="") as f:
        rows = list(csv.DictReader(f))
    cands = [r for r in rows if r["model"] == "p4-toy" and r["seed"] == "0"]
    assert cands, "no p4-toy seed0 ledger row"
    return cands[0]


def test_v1_m4b_ledger_matches_curve():
    row = _ledger_p4_row()
    s = json.load(open("postformer/ledger/curves/m4b-toy/g1_summary_p4-toy-s0.json"))
    assert abs(float(row["g1_mqar_8"]) - s["mqar"]["8"]["acc"]) < 1e-9
    assert abs(float(row["g1_mqar_16"]) - s["mqar"]["16"]["acc"]) < 1e-9
    assert float(row["g1_mqar_8"]) < 0.0625, "H4 must stay NEGATIVE at toy vs p1 ref"


def _run(*args):
    return subprocess.run(
        [sys.executable, "-m"] + list(args),
        capture_output=True, text=True, timeout=300,
    )


def test_v2_p4_window_zero_runs(tmp_path):
    out = str(tmp_path / "p4w0")
    r = _run("postformer.harness.synthetic_recall", "--model", "p4-toy",
             "--window", "0", "--episodes", "1", "--vocab", "64",
             "--n-pairs", "8",
             "--out", out)
    assert r.returncode == 0, r.stderr[-500:]
    s = json.load(open(out + "/g1_summary_seed0.json"))
    assert s["config"]["window"] == 0


def test_v3_transformer_window_refused():
    r = _run("postformer.harness.synthetic_recall", "--model", "transformer-toy",
             "--window", "0", "--episodes", "1",
             "--out", "/tmp/tester_m4v_rej.json")
    assert r.returncode != 0
    assert "no window" in (r.stderr + r.stdout).lower()


def test_v4_npairs_above_vocab_refused():
    r = _run("postformer.harness.synthetic_recall", "--model", "p1-toy",
             "--n-pairs", "100", "--episodes", "1", "--vocab", "64",
             "--out", "/tmp/tester_m4v_nv.json")
    assert r.returncode != 0
    assert "n_pairs" in (r.stderr + r.stdout).lower()


def test_v5_p4_p1_state_bytes_flat_and_equal():
    m1, _ = build_model("p1", "toy")
    m4, _ = build_model("p4", "toy")
    b1_1k, b1_32k = m1.state_bytes(1, 1000), m1.state_bytes(1, 32000)
    b4_1k, b4_32k = m4.state_bytes(1, 1000), m4.state_bytes(1, 32000)
    assert b1_1k == b1_32k, (b1_1k, b1_32k)
    assert b4_1k == b4_32k, (b4_1k, b4_32k)
    assert b1_1k == b4_1k, (b1_1k, b4_1k)


def test_v6_no_em_dashes_in_docs():
    import subprocess as sp
    # Scope: only files this PR added/touched (pre-existing ideas files
    # elsewhere in the repo predate the invariant and are out of scope).
    files = sp.run(["git", "diff", "--name-only", "origin/main...HEAD"],
                   capture_output=True, text=True).stdout.split()
    scoped = [f for f in files if f.startswith(
        ("docs/research/issue-294", "ideas/2026-09-0",
         "progress/294-", "postformer/"))]
    assert scoped, "no PR-scoped files found"
    out = sp.run(["git", "grep", "-l", "\u2014", "--"] + scoped,
                 capture_output=True, text=True).stdout.strip()
    assert out == "", out
