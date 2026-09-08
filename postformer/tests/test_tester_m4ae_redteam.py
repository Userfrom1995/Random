"""Tester M4ae hostile suite: current-head pins at 22012286 (post-M4ad).

Refs #294 (toy/mini-scale proxies only, never gate results).

Why this suite exists: the head moved to 22012286 (builder M4ad handoff)
with M4ad suites pinning 25-row liveness, p4 curve ground truth, and
p1/p4/transformer causality. This suite closes the remaining hostile gaps
at the current head: p2/p3/p5 MINI step-vs-forward causality (the three
families m4ad did NOT cover), tie_embeddings rejection across all five
recurrent families, parse_model_name hostile rejections (M2
silent-invalidation class), p4 --window routing in synthetic_recall, and a
commit-subject discipline lock (zero Closes across the branch).
"""

import pathlib
import subprocess

import pytest
import torch

from postformer.models.factory import (
    build_model,
    count_params,
    parse_model_name,
)
from .conftest import FAMILIES, MINI

_HERE = pathlib.Path(__file__).resolve()
_POSTFORMER = _HERE.parents[1]
_LEDGER = _POSTFORMER / "ledger" / "ledger.csv"


def test_ae1_p2_p3_p5_mini_step_forward_causal():
    """The three families m4ad skipped must also be step/forward equivalent."""
    from postformer.models.common import seed_all
    seed_all(4242, "tester-m4ae-causal")
    for fam in ("p2", "p3", "p5"):
        assert fam in FAMILIES
        m, cfg = build_model(fam, "toy", {"layers": 1, "d_model": 32,
                                          "heads": 2, "mlp_hid": 64,
                                          "vocab_size": 48, "d_k": 8,
                                          "d_v": 8, "window": 8,
                                          "slots": 4, "slot_stride": 2,
                                          "use_accumulator": True})
        m.eval()
        x = torch.randint(0, cfg["vocab_size"], (1, 12))
        with torch.no_grad():
            full = m(x)
            st = m.init_state(1, "cpu", torch.float32)
            outs = [m.step(x[:, i:i + 1], st)[0] for i in range(12)]
        assert torch.isfinite(full).all(), fam
        assert (full - torch.cat(outs, dim=1)).abs().max().item() <= 1e-4, fam


def test_ae2_tie_embeddings_rejected_all_recurrent():
    """tie_embeddings must raise for every recurrent family (parity guard)."""
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        with pytest.raises(ValueError):
            build_model(fam, "toy", {"tie_embeddings": True})


def test_ae3_parse_model_name_rejects_silent_invalidation():
    """Middle-inserted tags and suffixes must fail loudly, never misbuild."""
    for bad in ("p2-G0-toy", "p1-toy-V512", "p1-W0-toy", "P1-tiny",
                "p1", "p6-toy", "p1-toy "):
        with pytest.raises(SystemExit):
            parse_model_name(bad)
    assert parse_model_name("p4-tiny") == ("p4", "tiny")
    assert parse_model_name("transformer-small") == ("transformer", "small")


def test_ae4_p4_window_routing_present():
    """M4a finding-1 regression lock: p4 keeps --window ablation protection."""
    src = (_POSTFORMER / "harness" / "synthetic_recall.py").read_text()
    assert 'family not in ("p1", "p2", "p3", "p4", "p5")' in src
    assert 'if family in ("p1", "p2", "p3", "p4", "p5")' in src


def test_ae5_small_scale_parity_within_2pct():
    """Live re-measure at small scale (m4ad pinned tiny only)."""
    base, _ = count_params("transformer", "small")
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        c, _ = count_params(fam, "small")
        assert abs(c - base) / base < 0.02, (fam, c, base)


def test_ae6_branch_discipline_zero_closes():
    """No commit subject on this branch may claim Closes (gates still open)."""
    r = subprocess.run(["git", "log", "--format=%s", "FETCH_HEAD..HEAD"],
                       capture_output=True, text=True, cwd=str(_HERE.parents[2]))
    if r.returncode != 0 or not r.stdout.strip():
        r = subprocess.run(["git", "log", "--format=%s", "-200"],
                           capture_output=True, text=True,
                           cwd=str(_HERE.parents[2]))
    subjects = r.stdout.splitlines()
    assert subjects, "no commit subjects found"
    bad = [s for s in subjects if "closes #" in s.lower()]
    assert not bad, bad


def test_ae7_mini_config_keys_subset():
    """MINI shared config must stay a valid override subset for all families."""
    for fam in FAMILIES:
        m, cfg = build_model(fam, "toy", dict(MINI))
        assert cfg["vocab_size"] == 48, (fam, cfg["vocab_size"])
        assert m is not None
