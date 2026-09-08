"""Tester M4k hostile suite: bare-defaults N>vocab refusal + n-guard edges.

Refs #294 (toy probes only, never gate results).

M4j pinned the explicit `--n-pairs 8,256 --vocab 64` refusal but never the
exact user-facing crash from its own docstring: bare
`synthetic_recall --model p1-toy --vocab 64` with the DEFAULT
`--n-pairs 16,64,256` (N=256 > vocab 64). This suite pins that the defaults
combo refuses loudly (SystemExit) before writing any g1_* partial outputs,
plus the nonpositive-n edges of the same up-front guard.
"""

import os

import pytest

from postformer.harness.synthetic_recall import main as recall_main


def test_m4k_bare_defaults_vocab64_refuses_loudly(tmp_path):
    """R1-exact: default n-pairs (16,64,256) at --vocab 64 must SystemExit."""
    out = str(tmp_path / "eval")
    os.makedirs(out, exist_ok=True)
    with pytest.raises(SystemExit):
        recall_main(["--model", "p1-toy", "--vocab", "64",
                     "--task", "mqar", "--episodes", "2",
                     "--out", out, "--seed", "0"])
    leftovers = [f for f in os.listdir(out) if f.startswith("g1_")]
    assert leftovers == [], f"refusal must not leave partial outputs: {leftovers}"


def test_m4k_zero_npairs_refuses_loudly(tmp_path):
    """--n-pairs 0 is meaningless; the harness must refuse, not crash."""
    out = str(tmp_path / "eval")
    os.makedirs(out, exist_ok=True)
    with pytest.raises(SystemExit):
        recall_main(["--model", "p1-toy", "--vocab", "64",
                     "--n-pairs", "0", "--task", "mqar",
                     "--episodes", "1", "--out", out, "--seed", "0"])
    leftovers = [f for f in os.listdir(out) if f.startswith("g1_")]
    assert leftovers == [], f"refusal must not leave partial outputs: {leftovers}"


def test_m4k_negative_npairs_refuses_loudly(tmp_path):
    """Negative --n-pairs must refuse with the same up-front guard."""
    out = str(tmp_path / "eval")
    os.makedirs(out, exist_ok=True)
    with pytest.raises(SystemExit):
        recall_main(["--model", "p1-toy", "--vocab", "64",
                     "--n-pairs", "-3", "--task", "mqar",
                     "--episodes", "1", "--out", out, "--seed", "0"])
    leftovers = [f for f in os.listdir(out) if f.startswith("g1_")]
    assert leftovers == [], f"refusal must not leave partial outputs: {leftovers}"


def test_m4k_non_mqar_task_ignores_npairs(tmp_path):
    """The N<=vocab guard is MQAR-specific; copy task must not trip on it."""
    out = str(tmp_path / "eval")
    os.makedirs(out, exist_ok=True)
    recall_main(["--model", "p1-toy", "--vocab", "64",
                 "--n-pairs", "8,256", "--task", "copying",
                 "--copy-len", "32", "--episodes", "1",
                 "--out", out, "--seed", "0"])
    assert os.path.exists(os.path.join(out, "g1_summary_seed0.json"))
