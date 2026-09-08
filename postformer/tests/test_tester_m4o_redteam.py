"""Tester M4o hostile suite: M4b-probe honesty + head pins at 0ce62622.

Refs #294 (toy/tiny smoke only, never gate results).

Why this suite exists: the /oc test trigger targeted M4b (a7553d5c) but the
branch has since advanced through M4c-M4n to 0ce62622, and the corpus sits
at 193 passed. This suite pins the M4b deliverable's honesty claims live so
no future edit can silently rewrite them:

- O1 (H4 negative honesty): the committed ledger holds the p4-toy M4b row
  (0.528M tokens, seed0, vocab64) with mqar8 0.035 BELOW the matched
  p1-W16-1000 ref 0.0625, and its notes text discloses H4 NEGATIVE / below
  ref. A silent upgrade of p4's numbers without touching the notes fails.
- O2 (N16 chance collapse): that same p4-toy row has g1_mqar_16 at chance
  (<= 1/64 + 1e-9), matching the A6/A7 documented extrapolation collapse.
- O3 (ledger liveness): `ledger check` passes as a live subprocess on the
  committed ledger with >= 25 rows.
- O4 (p4 parity live): p4 vs transformer within 2% at toy/tiny/small via
  the factory (re-measured, not copied pins).
- O5 (no premature close): no PR-body-style `Closes #294` directive line
  exists in the progress tracker outside conditional "only on" sentences.
"""

import csv
import os
import re
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(REPO)
LEDGER = os.path.join(REPO, "ledger", "ledger.csv")
PROGRESS = os.path.join(
    ROOT, "progress", "294-post-transformer-sequence-architecture.md"
)


def _rows():
    with open(LEDGER, newline="") as f:
        return list(csv.DictReader(f))


def test_m4b_p4_row_honest_h4_negative():
    rows = _rows()
    cands = [
        r
        for r in rows
        if r["model"] == "p4-toy"
        and r["train_tokens"] == "528000"
        and r["seed"] == "0"
        and r["vocab"] == "64"
    ]
    assert cands, "M4b p4-toy seed0 0.528M-token row missing from ledger"
    r = cands[0]
    assert abs(float(r["g1_mqar_8"]) - 0.035) < 1e-9, r["g1_mqar_8"]
    assert float(r["g1_mqar_8"]) < 0.0625, "H4-negative claim: p4 must sit below p1 ref"
    notes = r["notes"]
    assert "0.0625" in notes, "ledger must cite the matched p1 ref value"
    assert re.search(r"H4.*(NEGATIVE|negative)|below.*p1", notes), (
        "ledger must disclose the negative H4 read, got: " + notes[:160]
    )


def test_m4b_p4_n16_at_chance():
    rows = _rows()
    r = next(
        r
        for r in rows
        if r["model"] == "p4-toy"
        and r["train_tokens"] == "528000"
        and r["seed"] == "0"
    )
    assert float(r["g1_mqar_16"]) <= 1.0 / 64 + 1e-9, r["g1_mqar_16"]


def test_ledger_check_live_green_25_rows():
    p = subprocess.run(
        [sys.executable, "-m", "postformer.harness.ledger", "check",
         "--ledger", LEDGER],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert p.returncode == 0, p.stderr[-2000:]
    assert len(_rows()) >= 25, len(_rows())


def test_p4_parity_live_all_scales():
    from postformer.models.factory import count_params

    tb = {}
    for s in ("toy", "tiny", "small"):
        tb[s], _ = count_params("transformer", s)
    for s in ("toy", "tiny", "small"):
        v, _ = count_params("p4", s)
        assert abs(v - tb[s]) / tb[s] < 0.02, (s, v, tb[s])


def test_no_premature_close_directive():
    with open(PROGRESS) as f:
        lines = f.read().splitlines()
    bad = [
        l for l in lines
        if re.search(r"^\s*(Closes|Fixes|Resolves)\s+#294", l)
    ]
    assert not bad, bad[:3]
