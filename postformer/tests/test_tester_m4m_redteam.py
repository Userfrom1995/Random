"""Tester M4m hostile suite: cross-window causality + flatness pins + live-process guards.

Refs #294 (toy probes only, never gate results).

What prior suites left open (M4l covered in-process parity/ledger/viewer,
M4k/M4j covered the n-guard itself):

- R1 (cross-W causality): step()-vs-forward() equivalence is only pinned at
  short T elsewhere. Toy W=16, so T=33 crosses the window/slot boundary
  twice. All six families must stay <= 1e-4 there, plus T=1 degenerate.
- R2 (flatness pins): every recurrent family's state_bytes must be
  identical at 1k vs 32k AND match the proof-g4.md S-tiny pins
  (P1/P4 3145728, P2 3538944, P3/P5 4718592). A silent inventory regression
  breaks the G4 tier claim without failing any other test.
- R3 (live-process guards): in-process SystemExit is pinned, but a real
  user meets the subprocess exit code. --window on transformer,
  train --steps 0, and N>vocab MQAR must all exit nonzero as live
  processes with zero partial g1_* outputs.
- R4 (prefix invariance at the W edge): truncating a T=20 prefix to T=16
  (exactly W) must not change the first 16 logits (<= 1e-6) for the
  window/slot families p1..p5.
- R5 (tie guard family-wide): tie_embeddings=True must raise for every
  candidate p1..p5 while the baseline builds fine with it.
"""

import os
import subprocess
import sys

import pytest
import torch

from postformer.models.factory import build_model

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROOF_PINS_TINY = {"p1": 3145728, "p2": 3538944, "p3": 4718592,
                   "p4": 3145728, "p5": 4718592}


def _step_forward_maxdiff(family, T, seed=0):
    torch.manual_seed(seed)
    m, _ = build_model(family, "toy")
    m.eval()
    x = torch.randint(0, 66, (1, T))
    with torch.no_grad():
        o = m.forward(x)
    S = m.init_state(1, "cpu", torch.float32)
    outs = []
    with torch.no_grad():
        for i in range(T):
            oi, S = m.step(x[:, i:i + 1], S)
            outs.append(oi)
    oo = torch.cat(outs, dim=1)
    return (o - oo).abs().max().item()


@pytest.mark.parametrize("family", ["transformer", "p1", "p2", "p3", "p4", "p5"])
def test_m4m_step_forward_cross_window_T33(family):
    """R1: recurrence matches forward across two W crossings (W=16, T=33)."""
    assert _step_forward_maxdiff(family, 33) <= 1e-4


@pytest.mark.parametrize("family", ["transformer", "p1", "p2", "p3", "p4", "p5"])
def test_m4m_step_forward_degenerate_T1(family):
    """R1: single-token forward composes with step()."""
    assert _step_forward_maxdiff(family, 1) <= 1e-6


@pytest.mark.parametrize("family", ["p1", "p2", "p3", "p4", "p5"])
def test_m4m_state_bytes_flat_and_pinned(family):
    """R2: flat 1k vs 32k and equal to the proof-g4.md S-tiny pin."""
    m, _ = build_model(family, "tiny")
    b1k = m.state_bytes(1, 1000)
    b32k = m.state_bytes(1, 32000)
    assert b1k == b32k, f"{family} state grows with T: {b1k} vs {b32k}"
    assert b1k == PROOF_PINS_TINY[family], \
        f"{family} {b1k} != proof pin {PROOF_PINS_TINY[family]}"


def _run_cli(args):
    return subprocess.run([sys.executable, "-m"] + args, cwd=REPO,
                          capture_output=True, text=True, timeout=300)


def test_m4m_live_window_on_transformer_refused(tmp_path):
    """R3: live process rejects --window for the transformer (exit != 0)."""
    out = str(tmp_path / "eval")
    os.makedirs(out, exist_ok=True)
    r = _run_cli(["postformer.harness.synthetic_recall", "--model",
                  "transformer-toy", "--window", "0", "--task", "mqar",
                  "--vocab", "64", "--n-pairs", "8", "--episodes", "1",
                  "--out", out])
    assert r.returncode != 0, f"must refuse, stdout={r.stdout[-300:]}"
    assert [f for f in os.listdir(out) if f.startswith("g1_")] == []


def test_m4m_live_train_steps0_refused(tmp_path):
    """R3: live process rejects --steps 0 (exit != 0)."""
    out = str(tmp_path / "train")
    r = _run_cli(["postformer.harness.train", "--model", "p1-toy",
                  "--steps", "0", "--out", out])
    assert r.returncode != 0


def test_m4m_live_n_above_vocab_refused(tmp_path):
    """R3: live process refuses N=300 > vocab 64 (exit != 0, no partials)."""
    out = str(tmp_path / "eval")
    os.makedirs(out, exist_ok=True)
    r = _run_cli(["postformer.harness.synthetic_recall", "--model",
                  "p1-toy", "--task", "mqar", "--vocab", "64",
                  "--n-pairs", "300", "--episodes", "2", "--out", out])
    assert r.returncode != 0, f"must refuse, stdout={r.stdout[-300:]}"
    assert [f for f in os.listdir(out) if f.startswith("g1_")] == []


@pytest.mark.parametrize("family", ["p1", "p2", "p3", "p4", "p5"])
def test_m4m_prefix_invariance_at_W_edge(family):
    """R4: first W=16 logits identical for T=20 vs truncated T=16 input."""
    torch.manual_seed(7)
    m, _ = build_model(family, "toy")
    m.eval()
    x = torch.randint(0, 66, (1, 20))
    with torch.no_grad():
        full = m.forward(x)[:, :16, :]
        trunc = m.forward(x[:, :16])[:, :16, :]
    assert (full - trunc).abs().max().item() <= 1e-6


@pytest.mark.parametrize("family", ["p1", "p2", "p3", "p4", "p5"])
def test_m4m_tie_embeddings_rejected_candidates(family):
    """R5: tie_embeddings override raises for every candidate family."""
    with pytest.raises(ValueError):
        build_model(family, "toy", {"tie_embeddings": True})


def test_m4m_tie_embeddings_allowed_baseline():
    """R5: the baseline still honors tie_embeddings (no over-refusal)."""
    m, cfg = build_model("transformer", "toy", {"tie_embeddings": True})
    assert m is not None
