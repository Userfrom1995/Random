"""Tester M4l hostile suite: n-guard off-by-one boundaries + task scoping,
arg-refusal edges, live parity, ledger green, viewer hardening.

Refs #294 (toy probes only, never gate results).

M4k pinned the bare-defaults N=256>vocab refusal and the n=0 edge of the
new up-front `--n-pairs` guard in synthetic_recall. This suite pins what
M4k left open:

- R1 (off-by-one, both sides): n == vocab (64,64) MUST succeed (the guard
  is `n > vocab`, not `>=`); n == vocab+1 (65,64) MUST refuse loudly with
  zero partial g1_* outputs.
- R2 (no over-refusal): a non-MQAR task (`--task induction`) with an
  out-of-vocab `--n-pairs 256` MUST proceed, since the guard only applies
  when mqar is among the evaluated tasks.
- R3 (arg-refusal edges): `--window -1` and `--vocab 8` refuse before any
  model build (fast SystemExit, no partial outputs).
- R4 (live parity): every candidate family p1..p5 lands within +-2% of
  the transformer non-embedding param count at toy/tiny/small.
- R5 (ledger green): the committed 25-row ledger passes `check` in-process.
- R6 (viewer hardening): viewer parses with an RFC-4180 splitter and
  escapes model/notes cells before innerHTML.
"""

import json
import os

import pytest

from postformer.harness.ledger import main as ledger_main
from postformer.harness.synthetic_recall import main as recall_main
from postformer.models.common import param_count_no_embed
from postformer.models.factory import build_model

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _fresh_out(tmp_path, name="eval"):
    out = str(tmp_path / name)
    os.makedirs(out, exist_ok=True)
    return out


def _no_partials(out):
    leftovers = [f for f in os.listdir(out) if f.startswith("g1_")]
    assert leftovers == [], f"refusal must not leave partial outputs: {leftovers}"


def test_m4l_npairs_equals_vocab_succeeds(tmp_path):
    """R1a: n == vocab is legal (guard is strict `>`); eval must succeed."""
    out = _fresh_out(tmp_path)
    recall_main(["--model", "p1-toy", "--vocab", "64", "--n-pairs", "64",
                 "--task", "mqar", "--episodes", "1",
                 "--out", out, "--seed", "0"])
    with open(os.path.join(out, "g1_summary_seed0.json")) as f:
        summary = json.load(f)
    assert "mqar" in summary, "mqar section missing from boundary-eval summary"
    assert "64" in {str(k) for k in summary["mqar"]}, (
        f"N=64 column missing: {list(summary['mqar'])}")


def test_m4l_npairs_vocab_plus_one_refuses_cleanly(tmp_path):
    """R1b: n == vocab+1 must SystemExit before writing any g1_* files."""
    out = _fresh_out(tmp_path)
    with pytest.raises(SystemExit):
        recall_main(["--model", "p1-toy", "--vocab", "64", "--n-pairs", "65",
                     "--task", "mqar", "--episodes", "1",
                     "--out", out, "--seed", "0"])
    _no_partials(out)


def test_m4l_nonmqar_task_ignores_npairs_guard(tmp_path):
    """R2: induction-only eval must NOT be blocked by the MQAR n-guard."""
    out = _fresh_out(tmp_path)
    recall_main(["--model", "p1-toy", "--vocab", "64", "--n-pairs", "256",
                 "--task", "induction", "--episodes", "1",
                 "--out", out, "--seed", "0"])
    with open(os.path.join(out, "g1_summary_seed0.json")) as f:
        summary = json.load(f)
    assert "induction" in summary, "induction section missing"


def test_m4l_negative_window_refuses(tmp_path):
    """R3a: --window -1 must refuse loudly without partial outputs."""
    out = _fresh_out(tmp_path)
    with pytest.raises(SystemExit):
        recall_main(["--model", "p1-toy", "--vocab", "64", "--window", "-1",
                     "--task", "mqar", "--episodes", "1",
                     "--out", out, "--seed", "0"])
    _no_partials(out)


def test_m4l_small_vocab_refuses(tmp_path):
    """R3b: --vocab 8 (< 16 floor) must refuse loudly, no partials."""
    out = _fresh_out(tmp_path)
    with pytest.raises(SystemExit):
        recall_main(["--model", "p1-toy", "--vocab", "8",
                     "--task", "mqar", "--episodes", "1",
                     "--out", out, "--seed", "0"])
    _no_partials(out)


def test_m4l_parity_within_two_percent_all_scales():
    """R4: live re-measurement of the binding +-2% param gate, all arms."""
    for scale in ("toy", "tiny", "small"):
        m, _ = build_model("transformer", scale)
        base = param_count_no_embed(m)
        assert base > 0
        for fam in ("p1", "p2", "p3", "p4", "p5"):
            m, _ = build_model(fam, scale)
            n = param_count_no_embed(m)
            drift = abs(n - base) / base
            assert drift <= 0.02, (
                f"{fam}-{scale}: drift {drift * 100:.3f}% > 2% "
                f"({n} vs baseline {base})")


def test_m4l_committed_ledger_check_green(capsys):
    """R5: the shipped ledger must pass `check` in-process (no SystemExit)."""
    ledger_main(["check", "--ledger",
                 os.path.join(REPO, "ledger", "ledger.csv")])
    out = capsys.readouterr().out
    assert "ledger OK" in out, f"unexpected check output: {out!r}"


def test_m4l_viewer_hardened():
    """R6: viewer uses a quote-aware splitter and escapes cells."""
    with open(os.path.join(REPO, "viewer", "index.html")) as f:
        html = f.read()
    assert "splitCSV" in html, "viewer lost its RFC-4180 splitter"
    code = "\n".join(l for l in html.splitlines()
                     if not l.strip().startswith("//"))
    assert '.split(",")' not in code, "quote-unaware split is back in code"
    for cell in ("esc(r.model)", "esc(r.notes)"):
        assert cell in html, f"viewer no longer escapes {cell}"
