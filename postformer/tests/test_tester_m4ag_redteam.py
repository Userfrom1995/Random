"""Tester M4ag hostile suite: G4 flatness, inventory formulae, ledger honesty.

Refs #294 (toy/mini-scale proxies only, never gate results).

Why this suite exists: the full 318-test corpus at f34e5def passes, but no
single suite pins the amended G4 Pareto gate end-to-end at the current head:
(AG1) every candidate family's state_bytes is exactly flat 1k->32k while the
baseline grows superlinearly; (AG2) P2/P3 state_size match an independent
recomputation from MINI dims (guards the M3 2x-overcount/phantom regression
class); (AG3) every tiny/small ledger row carries a "random init" honesty
marker so smoke rows can never be mistaken for trained gate results;
(AG4) P4 MINI forward is exactly deterministic across reruns; (AG5) the
trainer CLI rejects steps=0 loudly instead of IndexError/ZeroDivision.
"""

import csv
import pathlib

import pytest
import torch

from postformer.models.common import seed_all
from postformer.models.factory import build_model
from .conftest import FAMILIES, MINI

_HERE = pathlib.Path(__file__).resolve()
_POSTFORMER = _HERE.parents[1]
_LEDGER = _POSTFORMER / "ledger" / "ledger.csv"

CANDIDATES = ["p1", "p2", "p3", "p4", "p5"]


def test_ag1_candidates_flat_baseline_grows():
    """AG1: G4 tier-(a) shape - candidates flat 1k vs 32k, baseline ~32x."""
    for fam in CANDIDATES:
        m, _ = build_model(fam, "tiny", dict(MINI))
        lo = m.state_bytes(1, 1000)
        hi = m.state_bytes(1, 32000)
        assert lo == hi, (fam, lo, hi)
        assert lo > 0, fam
    base, _ = build_model("transformer", "tiny", dict(MINI))
    b_lo = base.state_bytes(1, 1000)
    b_hi = base.state_bytes(1, 32000)
    assert b_hi >= 20 * b_lo, (b_lo, b_hi)


def test_ag2_p2_p3_p5_state_size_matches_independent_formula():
    """AG2: P2/P3/P5 inventories recomputed from dims, no 2x/phantom terms."""
    m2, cfg2 = build_model("p2", "tiny", dict(MINI))
    H, dk, dv = cfg2["heads"], cfg2["d_k"], cfg2["d_v"]
    W, G = cfg2["window"], cfg2["slots"]
    wd = cfg2["win_heads"] * cfg2["win_hd"]
    bpe = 4
    win = 2 * W * wd * bpe
    expect_p2 = H * dk * dv * bpe + G * H * (dk + dv) * bpe + win
    assert m2.blocks[0].state_size(bpe) == expect_p2, (
        m2.blocks[0].state_size(bpe), expect_p2)
    # Regression tripwire for the old 2x-slots + phantom-H bug:
    buggy = 2 * G * H * (dk + dv) * bpe + H * dk * dv * bpe + H * bpe + win
    assert expect_p2 != buggy and expect_p2 < buggy
    m3, cfg3 = build_model("p3", "tiny", dict(MINI))
    H3, dk3, dv3 = cfg3["heads"], cfg3["d_k"], cfg3["d_v"]
    win3 = 2 * cfg3["window"] * cfg3["win_heads"] * cfg3["win_hd"] * bpe
    assert m3.blocks[0].state_size(bpe) == 2 * H3 * dk3 * dv3 * bpe + win3
    m3n, _ = build_model("p3", "tiny", dict(MINI, use_accumulator=False))
    # A stays resident (zeros when disabled), so off reports the same 2x.
    assert m3n.blocks[0].state_size(bpe) == 2 * H3 * dk3 * dv3 * bpe + win3
    m5, cfg5 = build_model("p5", "tiny", dict(MINI))
    H5, dv5 = cfg5["heads"], cfg5["d_v"]
    win5 = 2 * cfg5["window"] * cfg5["win_heads"] * cfg5["win_hd"] * bpe
    expect_p5 = H5 * (2 * cfg5["d_k"]) * dv5 * bpe + win5
    assert m5.blocks[0].state_size(bpe) == expect_p5, (
        m5.blocks[0].state_size(bpe), expect_p5)


def test_ag3_scale_rows_carry_random_init_honesty_marker():
    """AG3: every tiny/small ledger row is tagged random-init smoke."""
    rows = list(csv.DictReader(_LEDGER.open()))
    assert len(rows) == 25, len(rows)
    scaled = [r for r in rows if "tiny" in r["model"] or "small" in r["model"]]
    assert scaled, "expected tiny/small smoke rows"
    for r in scaled:
        note = (r.get("notes") or "").lower()
        assert ("random init" in note or "random-init" in note
                or "not a gate result" in note), r["model"]


def test_ag4_p4_mini_forward_exactly_deterministic():
    """AG4: same seed twice gives bitwise-identical P4 MINI logits."""
    def run_once():
        seed_all(4242, "ag4")
        m, _ = build_model("p4", "tiny", dict(MINI))
        m.eval()
        x = torch.randint(0, MINI["vocab_size"], (1, 12))
        with torch.no_grad():
            return m(x)
    assert torch.equal(run_once(), run_once())


def test_ag5_train_rejects_zero_steps_loudly():
    """AG5: train CLI with steps=0 fails via SystemExit, never ZeroDivision."""
    from postformer.harness import train as _train
    with pytest.raises(SystemExit):
        _train.main(["--model", "p1-toy", "--steps", "0", "--batch", "2"])
