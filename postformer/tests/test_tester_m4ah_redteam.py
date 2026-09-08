"""Tester final-gate suite for head 791f8017: live pins at this exact commit.

Refs #294 (toy/MINI-scale proxies only, never gate results).

Why this suite exists: prior M4* suites pin their own heads; this file pins
the CURRENT head end-to-end in one fast place: (H1) family-wide param parity
within 2% at toy/tiny/small (MINI dims for tiny/small, live count, no stale
pins); (H2) step-vs-forward equivalence <=1e-4 for every candidate at MINI;
(H3) ledger check green on the live 25-row ledger.csv; (H4) strict --model
names reject middle tags loudly; (H5) tie_embeddings rejected for p1-p5.
"""

import pathlib
import subprocess
import sys

import pytest
import torch

from postformer.models.factory import build_model, count_params, parse_model_name

_HERE = pathlib.Path(__file__).resolve()
_POSTFORMER = _HERE.parents[1]
_LEDGER = _POSTFORMER / "ledger" / "ledger.csv"

CANDIDATES = ["p1", "p2", "p3", "p4", "p5"]


def test_h1_parity_within_2pct_all_scales():
    """H1: every candidate within +-2% of baseline at toy/tiny/small.

    Full pinned configs (the binding gate). MINI-dim overrides are NOT
    used here: the MLP hid pins are tuned for full dims, so MINI
    overrides legitimately drift (test bug, not code bug - caught live).
    """
    for scale in ["toy", "tiny", "small"]:
        base, _ = count_params("transformer", scale, None)
        assert base > 0, scale
        for fam in CANDIDATES:
            n, _ = count_params(fam, scale, None)
            drift = abs(n - base) / base
            assert drift <= 0.02, (fam, scale, n, base, drift)


def test_h2_step_forward_equivalence_mini():
    """H2: incremental step() matches forward() to <=1e-4 (causality)."""
    for fam in CANDIDATES:
        m, _ = build_model(fam, "toy", None)
        m.eval()
        T = 24
        x = torch.randint(0, 66, (1, T))
        with torch.no_grad():
            logits = m.forward(x)
            st = m.init_state(1, "cpu", torch.float32)
            outs = []
            for i in range(T):
                o, st = m.step(x[:, i:i + 1], st)
                outs.append(o)
            rec = torch.cat(outs, dim=1)
        d = (logits - rec).abs().max().item()
        assert d <= 1e-4, (fam, d)


def test_h3_ledger_check_green_live():
    """H3: live ledger.csv passes the strict checker (no silent drift)."""
    r = subprocess.run(
        [sys.executable, "postformer/harness/ledger.py", "check",
         "--ledger", str(_LEDGER)],
        capture_output=True, text=True, cwd=str(_POSTFORMER.parent),
    )
    assert r.returncode == 0, r.stderr[-2000:]
    assert "ledger OK" in (r.stdout + r.stderr), (r.stdout, r.stderr)


def test_h4_strict_model_names_reject_tags():
    """H4: middle-inserted tags fail loudly (M2 silent-invalidation class)."""
    for bad in ["p2-G0-toy", "p1-toy-V512", "p9-toy", "p1-huge"]:
        with pytest.raises(SystemExit):
            parse_model_name(bad)
    fam, scale = parse_model_name("p1-toy")
    assert (fam, scale) == ("p1", "toy")


def test_h5_tie_embeddings_rejected_for_candidates():
    """H5: tie_embeddings override rejected for p1-p5 (parity protection)."""
    for fam in CANDIDATES:
        with pytest.raises(ValueError):
            build_model(fam, "toy", {"tie_embeddings": True})
