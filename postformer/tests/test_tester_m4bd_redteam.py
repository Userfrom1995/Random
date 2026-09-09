"""M4bd hostile suite: commit-attribution locks + live gate spot checks.

Locks the AGENTS.md attribution invariant that one Fixer commit broke:
no owner Co-authored-by trailers, every subject carries a role prefix.
Plus live spot checks (ledger green, tiny parity, T=1 finite) that must
stay green independent of the discipline findings.
Refs #294.
"""

from __future__ import annotations

import subprocess as sp
from pathlib import Path

import pytest
import torch

REPO = Path(__file__).resolve().parents[2]
BASE = "cdf3cdae"
PREFIXES = ("researcher:", "architect:", "builder:", "fixer:", "tester:",
            "lab:", "recover:", "general:", "maintainer:")


def _log(fmt: str) -> str:
    out = sp.run(["git", "log", f"{BASE}..HEAD", f"--pretty=format:{fmt}"],
                 capture_output=True, text=True, cwd=str(REPO))
    assert out.returncode == 0, f"git log failed: {out.stderr[:200]}"
    return out.stdout


def test_bd1_no_coauthored_by_trailers():
    """No post-base commit body may carry a Co-authored-by trailer.

    Attribution is strict: commits are authored by the bot identity with
    the agent persona name, never the owner, never with Co-authored-by.
    Reproducer: 04596a28 carries
    'Co-authored-by: Userfrom1995 <...>' and must be reworded away.
    """
    bodies = _log("%H %b ENDMSG")
    offenders = [ln.split()[0] for ln in bodies.split(" ENDMSG")
                 if "co-authored-by" in ln.lower()]
    assert not offenders, \
        f"forbidden Co-authored-by trailer in: {offenders[:5]}"


def test_bd2_every_subject_has_role_prefix():
    """Every post-base subject starts with a role prefix (fixer:, ...).

    Reproducer: 04596a28 'Re-applied 7 harness fixes, verified' has no
    prefix and no Refs #294; it must be reworded to 'fixer: ... (Refs #294)'.
    """
    subjects = [s for s in _log("%h %s").splitlines() if s.strip()]
    assert subjects, "no post-base commits found"
    bad = [s for s in subjects
           if not s.split(" ", 1)[1].startswith(PREFIXES)]
    assert not bad, f"subjects missing role prefix: {bad[:5]}"


def test_bd3_no_owner_authorship():
    """No post-base commit is authored by the owner address."""
    authors = _log("%h %an <%ae>").splitlines()
    bad = [a for a in authors
           if "Userfrom1995" in a or "users.noreply.github.com" not in a]
    # bot authors are '... <github-actions[bot]@users.noreply.github.com>'
    bad = [a for a in bad if "github-actions[bot]" not in a]
    assert not bad, f"non-bot authorship: {bad[:5]}"


def test_bd4_live_ledger_check_green():
    """Live ledger check passes on the committed 25-row ledger."""
    out = sp.run(["python3", "-m", "postformer.harness.ledger", "check",
                  "--ledger", "postformer/ledger/ledger.csv"],
                 capture_output=True, text=True, cwd=str(REPO))
    assert out.returncode == 0, out.stdout[-500:] + out.stderr[-500:]
    assert "ledger OK" in out.stdout


def test_bd5_live_tiny_parity_within_two_percent():
    """Live re-measure: all five candidates within 2% of baseline tiny."""
    from postformer.models.factory import count_params
    base = count_params("transformer", "tiny")[0]
    assert base == 29366784, f"baseline pin moved: {base}"
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        n = count_params(fam, "tiny")[0]
        drift = abs(n - base) / base
        assert drift < 0.02, f"{fam}-tiny drift {drift:.4%}"


def test_bd6_single_token_forward_finite_all_families():
    """T=1 forward is finite for all six families at toy scale."""
    from postformer.models.factory import build_model
    for fam in ("transformer", "p1", "p2", "p3", "p4", "p5"):
        model, cfg = build_model(fam, "toy")
        model.eval()
        with torch.no_grad():
            x = torch.randint(0, cfg["vocab_size"], (1, 1))
            out = model(x)
        assert torch.isfinite(out).all(), f"{fam} T=1 non-finite"
