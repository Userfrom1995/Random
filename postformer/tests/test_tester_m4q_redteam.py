"""Tester M4q hostile suite: family-wide gate readiness at head 22b51d60.

Refs #294 (toy/tiny analytic checks only, never gate results).

Why this suite exists: the /oc test trigger targeted M4b (a7553d5c) but the
branch has since advanced through M4c-M4p hardening (204 passed). The M4p
suite pins p4-only causality/flatness plus p4-toy curve ground truth; this
suite pins FAMILY-WIDE gate readiness so no future edit can silently break
a non-p4 arm or a harness guard:

- Q1 (tiny gate-vocab finite): all six families forward-finite at vocab 8192
  (the S-tiny gate vocab), T=16, batch 1. Catches a family that only works
  at toy vocab.
- Q2 (family-wide flatness): p1/p2/p3/p4/p5 state_bytes T-invariant
  (1k vs 32k equal); transformer grows (linear control). Extends the M4p
  p4-only flatness pin to every candidate.
- Q3 (misrouted ablation flags): train rejects --slots on p1,
  --no-accumulator on p1, and --window on transformer with SystemExit.
  Pins the M4i silent-invalidation guards live.
- Q4 (no forward_chunk code): zero `forward_chunk` refs in postformer
  *.py code (the M1 vacuous-docstring fix stays fixed; historical mentions
  in ideas/progress docs are out of scope).
- Q5 (ledger live green): harness `check` passes on the committed ledger,
  25 rows x 26 cols.
- Q6 (A4 G-identity ground truth): committed a4-toy summaries show
  G64 == G4 exactly (mqar8 0.0825) and G0 lower (0.04625). A curve-only
  edit that breaks the slot-count-untested claim fails.
- Q7 (strict middle-tag names): factory rejects `p2-G0` style middle tags
  loudly (M4i strict gate); replay is via plain name plus flags.
- Q8 (viewer 26-col consistency): index.html comment cites the live 26-col
  header and ships splitCSV plus esc() on model/notes cells.
"""

import csv
import glob
import json
import os
import subprocess
import sys

import pytest
import torch

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(REPO)
LEDGER = os.path.join(REPO, "ledger", "ledger.csv")
VIEWER = os.path.join(REPO, "viewer", "index.html")
A4_DIR = os.path.join(REPO, "ledger", "curves", "a4-toy")


def test_q1_tiny_gate_vocab_forward_finite_all_families():
    from postformer.models.factory import build_model
    for fam in ("transformer", "p1", "p2", "p3", "p4", "p5"):
        m, cfg = build_model(fam, "tiny", {"vocab_size": 8192})
        m.eval()
        with torch.no_grad():
            x = torch.randint(0, 8192, (1, 16))
            y = m(x)
        assert torch.isfinite(y).all(), fam
        assert y.shape == (1, 16, 8192), (fam, tuple(y.shape))


def test_q2_family_wide_state_flatness():
    from postformer.models.factory import build_model
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        m, _ = build_model(fam, "tiny")
        a = m.state_bytes(1, length=1024)
        b = m.state_bytes(1, length=32768)
        assert a == b, (fam, a, b)
    mt, _ = build_model("transformer", "tiny")
    assert mt.state_bytes(1, length=32768) > mt.state_bytes(1, length=1024), \
        "transformer control must grow with T (linear KV cache)"


def test_q3_misrouted_ablation_flags_rejected():
    sys.path.insert(0, ROOT)
    from postformer.harness.train import main as train_main
    base = ["--model", "p1-toy", "--data", "mqar", "--steps", "1",
            "--batch", "1", "--seed", "0"]
    with pytest.raises(SystemExit):
        train_main(base + ["--slots", "4"])
    with pytest.raises(SystemExit):
        train_main(base + ["--no-accumulator"])
    with pytest.raises(SystemExit):
        train_main(["--model", "transformer-toy", "--data", "mqar",
                    "--steps", "1", "--batch", "1", "--seed", "0",
                    "--window", "0"])


def test_q4_no_forward_chunk_in_code():
    # Scope: production code (models/ + harness/). Test files that pin the
    # M1 fix legitimately mention the forbidden token, including this file.
    hits = []
    for sub in ("models", "harness"):
        for p in glob.glob(os.path.join(REPO, sub, "**", "*.py"),
                            recursive=True):
            with open(p) as f:
                for i, line in enumerate(f, 1):
                    if "forward_chunk" in line:
                        hits.append(f"{os.path.relpath(p, ROOT)}:{i}")
    assert hits == [], hits


def test_q5_ledger_live_green_25x26():
    r = subprocess.run(
        [sys.executable, "-m", "postformer.harness.ledger", "check",
         "--ledger", LEDGER],
        capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr[-2000:]
    assert "ledger OK (25 rows)" in (r.stdout + r.stderr)
    with open(LEDGER, newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 25
    assert len(rows[0].keys()) == 26, sorted(rows[0].keys())


def test_q6_a4_g_identity_ground_truth():
    def acc(g, n):
        with open(os.path.join(A4_DIR, f"g1_summary_p2-{g}-toy-s0.json")) as f:
            return json.load(f)["mqar"][str(n)]["acc"]
    assert abs(acc("G4", 8) - 0.0825) < 1e-9
    assert abs(acc("G64", 8) - acc("G4", 8)) < 1e-12, "G64 must equal G4"
    assert abs(acc("G64", 16) - acc("G4", 16)) < 1e-12
    assert acc("G0", 8) < acc("G4", 8), "pure-SSD control must sit below slots"


def test_q7_strict_middle_tag_names_rejected():
    from postformer.models.factory import build_model
    with pytest.raises((ValueError, SystemExit)):
        build_model("p2-G0", "toy")
    with pytest.raises((ValueError, SystemExit)):
        build_model("p1", "toy-V512")


def test_q8_viewer_26col_consistency():
    with open(VIEWER) as f:
        src = f.read()
    assert "function splitCSV(line)" in src
    assert "esc(r.model)" in src and "esc(r.notes)" in src
    with open(LEDGER, newline="") as f:
        rdr = csv.reader(f)
        header = next(rdr)
        assert len(header) == 26, len(header)
        for i, row in enumerate(rdr, 2):
            assert len(row) == len(header), (i, len(row))
