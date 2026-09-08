"""Tester M4aa hostile suite: ledger curve ground truth, P4 W-boundary
causality, degenerate T=1, live CLI guards.

Refs #294 (toy/mini-scale proxies only, never gate results).

Why this suite exists: the shipped ledger's G1 cells are only honest if
they reproduce the curve summary JSONs on disk byte-for-byte in value.
Unpinned, a future edit could hand-type a cell (the M2 A2-permutation
class) and `ledger check` would still pass because it validates schema,
not ground truth. This suite pins:

- AA1 (M4b ground truth): the "M4b P4 first falsification" ledger row's
  g1_mqar_8 / g1_mqar_16 cells equal curves/m4b-toy/
  g1_summary_p4-toy-s0.json mqar 8/16 acc exactly.
- AA2 (A4 ground truth): the P2 G4 slots-sweep row's g1_mqar_8 cell
  equals curves/a4-toy/g1_summary_p2-G4-toy-s0.json mqar 8 acc.
- AA3 (P4 W-boundary causality): block step() matches forward() across
  the W=8 window edge (T=20) and is prefix-invariant there.
- AA4 (degenerate T=1): every family runs a single-token forward finite
  at MINI scale (no empty-sequence / index crash).
- AA5 (live CLI guards): --window on transformer refuses loudly;
  tie_embeddings is rejected for p2/p4; parse_int_list honors k/K/M.
- AA6 (shipped ledger green): check passes on the shipped ledger.
"""

import csv
import json
import pathlib

import pytest
import torch

from postformer.harness import ledger as _ledger
from postformer.harness.synthetic_recall import main as _recall
from postformer.harness.util import parse_int_list
from postformer.models.common import seed_all
from postformer.models.factory import build_model
from .conftest import FAMILIES, MINI

_HERE = pathlib.Path(__file__).resolve()
_POSTFORMER = _HERE.parents[1]
_SHIPPED = _POSTFORMER / "ledger" / "ledger.csv"
_CURVES = _POSTFORMER / "ledger" / "curves"


def _rows():
    with open(_SHIPPED, newline="") as f:
        return list(csv.DictReader(f))


def test_aa1_m4b_p4_cells_match_curve_json():
    """AA1: M4b p4-toy ledger cells reproduce the curve summary values."""
    rows = [r for r in _rows() if "M4b P4 first falsification" in r["notes"]]
    assert len(rows) == 1, f"expected one M4b row, got {len(rows)}"
    row = rows[0]
    summary = json.loads(
        (_CURVES / "m4b-toy" / "g1_summary_p4-toy-s0.json").read_text())
    assert float(row["g1_mqar_8"]) == summary["mqar"]["8"]["acc"], \
        (row["g1_mqar_8"], summary["mqar"]["8"])
    assert float(row["g1_mqar_16"]) == summary["mqar"]["16"]["acc"], \
        (row["g1_mqar_16"], summary["mqar"]["16"])


def test_aa2_a4_g4_cell_matches_curve_json():
    """AA2: A4 P2-G4 slots-sweep cell reproduces its curve summary value."""
    rows = [r for r in _rows()
            if "A4 slots sweep" in r["notes"] and r.get("slots") == "4"]
    assert rows, "expected at least one A4 G4 ledger row"
    summary = json.loads(
        (_CURVES / "a4-toy" / "g1_summary_p2-G4-toy-s0.json").read_text())
    for row in rows:
        assert float(row["g1_mqar_8"]) == summary["mqar"]["8"]["acc"], \
            (row["g1_mqar_8"], summary["mqar"]["8"])


def test_aa3_p4_step_forward_across_window_edge():
    """AA3: P4 block step() == forward() across the W=8 edge; prefix holds."""
    seed_all(901, "m4aa-wedge")
    m, _ = build_model("p4", "tiny", dict(MINI))
    m.eval()
    blk = m.blocks[0]
    T = 20  # spans the MINI window W=8 twice over
    with torch.no_grad():
        x = torch.randn(1, T, MINI["d_model"])
        ref = blk(x)
        st = blk.init_state(1, "cpu", torch.float32)
        outs = []
        for i in range(T):
            o, st = blk.step(x[:, i, :], st)
            outs.append(o)
        seq = torch.stack(outs, dim=1)
        assert torch.allclose(ref, seq, atol=1e-4), \
            (ref - seq).abs().max().item()
        st2 = blk.init_state(1, "cpu", torch.float32)
        outs2 = []
        for i in range(5):  # prefix entirely inside the window
            o, st2 = blk.step(x[:, i, :], st2)
            outs2.append(o)
        pre = torch.stack(outs2, dim=1)
        assert torch.allclose(seq[:, :5, :], pre, atol=1e-6), \
            (seq[:, :5, :] - pre).abs().max().item()


def test_aa4_single_token_forward_finite_all_families():
    """AA4: T=1 forward is finite for every family (degenerate input)."""
    for fam in FAMILIES:
        seed_all(902, f"m4aa-t1-{fam}")
        m, _ = build_model(fam, "tiny", dict(MINI))
        m.eval()
        with torch.no_grad():
            ids = torch.randint(0, MINI["vocab_size"], (1, 1))
            out = m(ids)
        assert out.shape == (1, 1, MINI["vocab_size"]), (fam, out.shape)
        assert torch.isfinite(out).all(), fam


def test_aa5_cli_guards_live(tmp_path):
    """AA5: window/tie/suffix guards refuse or parse loudly, never silent."""
    with pytest.raises(SystemExit, match="window"):
        _recall(["--model", "transformer-toy", "--task", "mqar",
                 "--window", "0", "--vocab", "32", "--n-pairs", "4",
                 "--episodes", "2", "--seed", "0",
                 "--out", str(tmp_path / "rej")])
    with pytest.raises(ValueError, match="tie_embeddings"):
        build_model("p2", "tiny", dict(MINI, tie_embeddings=True))
    with pytest.raises(ValueError, match="tie_embeddings"):
        build_model("p4", "tiny", dict(MINI, tie_embeddings=True))
    assert parse_int_list("1k,2k") == [1024, 2048]
    assert parse_int_list("1M") == [1024 ** 2]
    assert parse_int_list("64") == [64]


def test_aa6_shipped_ledger_check_green(capsys):
    """AA6: the shipped ledger passes strict check after all deltas."""
    assert _SHIPPED.exists()
    _ledger.cmd_check(type("A", (), {"ledger": str(_SHIPPED)})())
    out = capsys.readouterr().out
    assert "ledger OK" in out
