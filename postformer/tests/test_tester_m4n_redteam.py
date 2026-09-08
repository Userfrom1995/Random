"""Tester M4n hostile suite: current-head pins (tiny causality, flatness,
parity, live ledger, gate honesty).

Refs #294 (toy/tiny smoke only, never gate results).

Why this suite exists: head 3cb98eb3 sits one builder progress-log commit
above the last tester suite (M4m). The full 175-test corpus is green, but
no committed test pins THIS head's live invariants at tiny scale. M4n
closes that gap with head-level regression pins:

- N1 (tiny causality): step()-vs-forward() equivalence at tiny scale
  (all prior cross-W pins used toy). T=20 crosses no W=128 boundary but
  exercises the real gate dims; must stay <= 1e-4, plus T=1 degenerate.
- N2 (flatness): every recurrent family's state_bytes(batch=1) identical
  at length 1k vs 32k (O(1) claim), while the transformer control grows.
- N3 (parity): all five candidates within 2% of the baseline at tiny
  AND small via the factory (re-measured live, not copied pins).
- N4 (live ledger): the committed ledger passes `ledger check` as a live
  subprocess and holds >= 25 rows with zero Closes directives in the
  progress tracker (Refs discipline until G1-G4 pass head-to-head).
- N5 (viewer): the shipped viewer still parses RFC-4180 quoted notes
  (splitCSV present, no bare l.split(",")) and escapes cell HTML.
"""

import csv
import os
import subprocess
import sys

import pytest
import torch

from postformer.models.factory import build_model, count_params

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAMILIES = ["transformer", "p1", "p2", "p3", "p4", "p5"]


def _maxdiff(family, scale, T, seed=0):
    torch.manual_seed(seed)
    m, _ = build_model(family, scale)
    m.eval()
    x = torch.randint(0, 64, (1, T))
    with torch.no_grad():
        o = m.forward(x)
    S = m.init_state(1, "cpu", torch.float32)
    outs = []
    with torch.no_grad():
        for i in range(T):
            oi, S = m.step(x[:, i:i + 1], S)
            outs.append(oi)
    return (o - torch.cat(outs, dim=1)).abs().max().item()


@pytest.mark.parametrize("family", FAMILIES)
def test_m4n_tiny_step_forward_T20(family):
    """N1: tiny-scale recurrence matches forward (<= 1e-4), real gate dims."""
    assert _maxdiff(family, "tiny", 20) <= 1e-4


def test_m4n_tiny_forward_T1_finite():
    """N1b: degenerate single-token forward is finite for every family."""
    for family in FAMILIES:
        m, _ = build_model(family, "tiny")
        m.eval()
        with torch.no_grad():
            o = m.forward(torch.randint(0, 64, (1, 1)))
        assert torch.isfinite(o).all(), family


@pytest.mark.parametrize("family", ["p1", "p2", "p3", "p4", "p5"])
def test_m4n_state_bytes_flat_1k_32k(family):
    """N2: recurrent state flat at 1k vs 32k (O(1) claim)."""
    m, _ = build_model(family, "tiny")
    a = m.state_bytes(1, 1024)
    b = m.state_bytes(1, 32768)
    assert a == b > 0, (family, a, b)


def test_m4n_transformer_control_grows():
    """N2b: transformer control state grows with length (contrast)."""
    m, _ = build_model("transformer", "tiny")
    assert m.state_bytes(1, 32768) > m.state_bytes(1, 1024)


@pytest.mark.parametrize("scale", ["tiny", "small"])
def test_m4n_parity_within_2pct(scale):
    """N3: all candidates within 2% of baseline at tiny and small."""
    base, _ = count_params("transformer", scale)
    for family in ["p1", "p2", "p3", "p4", "p5"]:
        n, _ = count_params(family, scale)
        assert abs(n - base) / base < 0.02, (family, scale, n, base)


def test_m4n_live_ledger_check_green():
    """N4: committed ledger passes live check with >= 25 rows."""
    ledger = os.path.join(REPO, "ledger", "ledger.csv")
    r = subprocess.run(
        [sys.executable, "-m", "postformer.harness.ledger", "check",
         "--ledger", ledger],
        capture_output=True, text=True, cwd=os.path.dirname(REPO))
    assert r.returncode == 0, r.stderr[-2000:]
    with open(ledger) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 25, len(rows)


def test_m4n_refs_discipline_no_closes_directive():
    """N4b: progress tracker keeps Refs discipline (no Closes #294)."""
    p = os.path.join(os.path.dirname(REPO),
                     "progress", "294-post-transformer-sequence-architecture.md")
    with open(p) as f:
        text = f.read()
    assert "Refs #294" in text
    for line in text.splitlines():
        s = line.strip()
        if s.startswith(("Closes #294", "Fixes #294", "Resolves #294")):
            raise AssertionError(f"premature close directive: {line}")


def test_m4n_viewer_csv_and_escape():
    """N5: viewer keeps RFC-4180 parsing and HTML escaping."""
    p = os.path.join(REPO, "viewer", "index.html")
    with open(p) as f:
        html = f.read()
    assert "splitCSV" in html
    assert "splitCSV(lines[0])" in html
    assert "cells = l.split" not in html
    assert "esc(r.notes)" in html and "esc(r.model)" in html
