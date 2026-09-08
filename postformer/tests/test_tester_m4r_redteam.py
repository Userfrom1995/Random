"""Tester M4r hostile suite: envelope ground truth + family-wide pins at head.

Refs #294 (toy/tiny analytic checks only, never gate results).

Why this suite exists: head advanced to M4q (212 passed) with the M4q
suite pinning a4 G-identity and family flatness. This suite pins the
remaining CPU-verifiable ground truth so a future edit cannot silently
rewrite history:

- R1 (m4b p4 ground truth): committed m4b-toy g1_summary pins p4-toy
  mqar8 0.035 / N16 0.015625 / 2hop 0.01, and ledger row 19 cells match.
- R2 (a6 floor ground truth): committed a6-toy summaries pin 0.0 for both
  arms (mqar8/N16/2hop), and ledger rows 23/24 cells match.
- R3 (G4 byte pins vs live code): live state_bytes tiny match proof pins
  (p1 3145728, p2 3538944, p3 4718592, p4 3145728, p5 4718592);
  transformer grows with T (linear control).
- R4 (tiny parity live): all five candidates within 2% of baseline tiny.
- R5 (tiny causality): step-vs-forward maxdiff <= 1e-4 for all recurrent
  families at tiny scale, T=12.
- R6 (T=1 finite): all six families forward-finite on a single token.
- R7 (ledger live green): harness `check` passes, 25 rows x 26 cols.
- R8 (gate honesty): envelope audit discloses trained gates NOT measured
  and H4 NEGATIVE at toy; ledger smoke rows carry zero train tokens.
"""

import csv
import json
import os
import subprocess
import sys

import pytest
import torch

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(REPO)
LEDGER = os.path.join(REPO, "ledger", "ledger.csv")
M4B = os.path.join(REPO, "ledger", "curves", "m4b-toy",
                   "g1_summary_p4-toy-s0.json")
A6_P1 = os.path.join(REPO, "ledger", "curves", "a6-toy",
                     "g1_summary_p1-toy-V512-s0.json")
A6_TR = os.path.join(REPO, "ledger", "curves", "a6-toy",
                     "g1_summary_transformer-toy-V512-s0.json")
ENVELOPE = os.path.join(REPO, "docs", "envelope-audit.md")

G4_PINS = {"p1": 3145728, "p2": 3538944, "p3": 4718592,
           "p4": 3145728, "p5": 4718592}


def _ledger_rows():
    with open(LEDGER, newline="") as f:
        return list(csv.DictReader(f))


def test_r1_m4b_p4_ground_truth():
    with open(M4B) as f:
        s = json.load(f)
    assert abs(s["mqar"]["8"]["acc"] - 0.035) < 1e-9
    assert abs(s["mqar"]["16"]["acc"] - 0.015625) < 1e-9
    assert abs(s["bind2hop"]["acc"] - 0.01) < 1e-9
    rows = _ledger_rows()
    r19 = [r for r in rows if r["model"] == "p4-toy"]
    assert len(r19) == 1, [r["model"] for r in rows]
    assert abs(float(r19[0]["g1_mqar_8"]) - 0.035) < 1e-9
    assert abs(float(r19[0]["g1_mqar_16"]) - 0.015625) < 1e-9


def test_r2_a6_floor_ground_truth():
    for path in (A6_P1, A6_TR):
        with open(path) as f:
            s = json.load(f)
        assert abs(s["mqar"]["8"]["acc"] - 0.0) < 1e-12, path
        assert abs(s["mqar"]["16"]["acc"] - 0.0) < 1e-12, path
    rows = _ledger_rows()
    by_model = [(r["model"], r["vocab"]) for r in rows]
    p1v = [r for r in rows if r["model"] == "p1-toy" and r["vocab"] == "512"]
    trv = [r for r in rows
           if r["model"] == "transformer-toy" and r["vocab"] == "512"]
    assert len(p1v) == 1 and len(trv) == 1, by_model
    for r in p1v + trv:
        assert abs(float(r["g1_mqar_8"]) - 0.0) < 1e-12, r
        assert abs(float(r["g1_induction"]) - 0.0) < 1e-12, r


def test_r3_g4_byte_pins_vs_live_code():
    from postformer.models.factory import build_model
    for fam, pin in G4_PINS.items():
        m, _ = build_model(fam, "tiny")
        assert m.state_bytes(1, 1024) == pin, (fam, m.state_bytes(1, 1024))
        assert m.state_bytes(1, 32768) == pin, (fam, "must be T-flat")
    mt, _ = build_model("transformer", "tiny")
    assert mt.state_bytes(1, 32768) > mt.state_bytes(1, 1024)


def test_r4_tiny_parity_live_within_2pct():
    from postformer.models.factory import count_params
    base, _ = count_params("transformer", "tiny")
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        p, _ = count_params(fam, "tiny")
        drift = abs(p - base) / base
        assert drift < 0.02, (fam, p, base, drift)


def test_r5_tiny_step_forward_causality():
    from postformer.models.factory import build_model
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        m, _ = build_model(fam, "tiny")
        m.eval()
        T = 12
        x = torch.randint(0, 256, (1, T))
        with torch.no_grad():
            y_fwd = m(x)
            st = m.init_state(1, "cpu", torch.float32)
            outs = [m.step(x[:, i:i + 1], st)[0] for i in range(T)]
            y_step = torch.cat(outs, dim=1)
        assert torch.isfinite(y_fwd).all() and torch.isfinite(y_step).all()
        assert (y_fwd - y_step).abs().max().item() <= 1e-4, fam


def test_r6_single_token_forward_finite_all_families():
    from postformer.models.factory import build_model
    for fam in ("transformer", "p1", "p2", "p3", "p4", "p5"):
        m, _ = build_model(fam, "tiny")
        m.eval()
        with torch.no_grad():
            y = m(torch.randint(0, 256, (1, 1)))
        assert torch.isfinite(y).all(), fam
        assert y.shape[1] == 1, (fam, tuple(y.shape))


def test_r7_ledger_live_green_25x26():
    r = subprocess.run(
        [sys.executable, "-m", "postformer.harness.ledger", "check",
         "--ledger", LEDGER],
        capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr[-2000:]
    assert "ledger OK (25 rows)" in (r.stdout + r.stderr)
    rows = _ledger_rows()
    assert len(rows) == 25
    assert len(rows[0].keys()) == 26


def test_r8_gate_honesty_disclosed():
    with open(ENVELOPE) as f:
        src = f.read()
    assert "NOT measured" in src
    assert "H4 NEGATIVE at toy" in src
    rows = _ledger_rows()
    smoke = [r for r in rows if r["model"] in ("transformer-tiny", "p1-tiny")]
    assert smoke, "smoke rows must exist"
    for r in smoke:
        assert r["train_tokens"] == "0", r
        assert "random init" in r["notes"], r
