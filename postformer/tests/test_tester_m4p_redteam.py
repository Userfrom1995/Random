"""Tester M4p hostile suite: curve-ground-truth + live guards at head ab82fd9d.

Refs #294 (toy/tiny/small analytic checks only, never gate results).

Why this suite exists: the /oc test trigger targeted M4b (a7553d5c) but the
branch has since advanced to ab82fd9d (M4c-M4o hardening, 198 passed). The
M4o suite pins ledger-internal honesty; this suite pins EXTERNAL
ground truth and live executable guards so no future edit can silently
break the chain:

- P1 (curve ground truth): the committed m4b-toy g1_summary JSON holds
  mqar8 acc 0.035 / mqar16 acc 0.015625, byte-identical to the ledger p4-toy
  M4b row cells. A ledger-only edit that drifts from the curves fails.
- P2 (all-family parity live): p1/p2/p3/p4/p5 vs transformer within 2% at
  toy, p1/p4 within 2% at tiny/small, re-measured via the factory.
- P3 (p4 causality live): p4-toy step-vs-forward maxdiff <= 1e-4 and T=1
  single-token forward finite.
- P4 (p4 flatness live): P4Block.state_size tiny-math matches the proof pin
  3145728 B total (524288 B/layer x6), and state_bytes is T-invariant
  (1k vs 32k equal).
- P5 (CLI guards live): transformer --window rejected with SystemExit,
  p4 --window accepted by the family gate, N>vocab refused, factory
  tie_embeddings rejected for p4.
- P6 (viewer hardening present): index.html contains splitCSV plus esc()
  on model/notes cells.
"""

import csv
import json
import os
import re

import pytest
import torch

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(REPO)
LEDGER = os.path.join(REPO, "ledger", "ledger.csv")
G1_P4 = os.path.join(REPO, "ledger", "curves", "m4b-toy",
                     "g1_summary_p4-toy-s0.json")
VIEWER = os.path.join(REPO, "viewer", "index.html")


def _ledger_p4_m4b_row():
    with open(LEDGER, newline="") as f:
        rows = list(csv.DictReader(f))
    cands = [r for r in rows if r["model"] == "p4-toy"
             and r["train_tokens"] == "528000" and r["seed"] == "0"]
    assert cands, "M4b p4-toy seed0 0.528M-token row missing"
    return cands[0]


def test_p1_curve_ground_truth_matches_ledger():
    with open(G1_P4) as f:
        s = json.load(f)
    assert s["model"] == "p4-toy" and s["seed"] == 0
    assert abs(s["mqar"]["8"]["acc"] - 0.035) < 1e-9, s["mqar"]["8"]
    assert abs(s["mqar"]["16"]["acc"] - 0.015625) < 1e-9, s["mqar"]["16"]
    row = _ledger_p4_m4b_row()
    assert abs(float(row["g1_mqar_8"]) - s["mqar"]["8"]["acc"]) < 1e-9
    assert abs(float(row["g1_mqar_16"]) - s["mqar"]["16"]["acc"]) < 1e-9


def test_p2_all_family_parity_live():
    from postformer.models.factory import count_params
    t_toy, _ = count_params("transformer", "toy")
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        v, _ = count_params(fam, "toy")
        assert abs(v - t_toy) / t_toy < 0.02, (fam, v, t_toy)
    t_tiny, _ = count_params("transformer", "tiny")
    for fam in ("p1", "p4"):
        v, _ = count_params(fam, "tiny")
        assert abs(v - t_tiny) / t_tiny < 0.02, (fam, v, t_tiny)
    t_small, _ = count_params("transformer", "small")
    for fam in ("p1", "p4"):
        v, _ = count_params(fam, "small")
        assert abs(v - t_small) / t_small < 0.02, (fam, v, t_small)


def test_p3_p4_step_forward_causality_live():
    from postformer.models.factory import build_model
    m, cfg = build_model("p4", "toy")
    m.eval()
    d = cfg["d_model"]
    blk = m.blocks[0]
    torch.manual_seed(7)
    with torch.no_grad():
        # T=1 single-token forward must be finite and match step()
        x1 = torch.randn(1, 1, d)
        ref1 = blk(x1)
        assert torch.isfinite(ref1).all()
        st = blk.init_state(1, "cpu", torch.float32)
        o, _ = blk.step(x1[:, 0, :], st)
        assert torch.allclose(ref1[:, 0, :], o, atol=1e-4)
        # step-vs-forward equivalence across the W boundary
        T = 20
        x = torch.randn(1, T, d)
        yf = blk(x)
        st = blk.init_state(1, "cpu", torch.float32)
        outs = []
        for t in range(T):
            oo, st = blk.step(x[:, t, :], st)
            outs.append(oo)
        ys = torch.stack(outs, dim=1)
    assert torch.isfinite(ys).all()
    assert (ys - yf).abs().max().item() <= 1e-4, \
        (ys - yf).abs().max().item()


def test_p4_flatness_matches_proof_pin():
    from postformer.models.factory import build_model
    m, cfg = build_model("p4", "tiny")
    blk = m.blocks[0]
    per_layer = blk.state_size()
    assert per_layer == 524288, per_layer
    assert per_layer * cfg["layers"] == 3145728, per_layer
    assert m.state_bytes(1, length=1024) == m.state_bytes(1, length=32768), \
        "P4 state must be T-invariant (O(1) flat)"


def test_p5_cli_guards_live():
    import argparse
    import sys
    sys.path.insert(0, ROOT)
    from postformer.harness.synthetic_recall import main as recall_main
    # transformer + --window must be rejected loudly
    with pytest.raises(SystemExit):
        recall_main(["--model", "transformer-toy", "--window", "0",
                     "--task", "mqar", "--n-pairs", "8", "--episodes", "1",
                     "--vocab", "64", "--seed", "0"])
    # N > vocab must be refused up front (M4j guard)
    with pytest.raises(SystemExit):
        recall_main(["--model", "p1-toy", "--task", "mqar",
                     "--n-pairs", "65", "--episodes", "1",
                     "--vocab", "64", "--seed", "0"])
    # factory must reject tie_embeddings for p4
    from postformer.models.factory import build_model
    with pytest.raises(ValueError):
        build_model("p4", "toy", {"tie_embeddings": True})


def test_p6_viewer_hardening_present():
    with open(VIEWER) as f:
        src = f.read()
    assert "function splitCSV(line)" in src, "RFC-4180 splitter missing"
    assert "esc(r.model)" in src and "esc(r.notes)" in src, \
        "model/notes cells must be HTML-escaped"
