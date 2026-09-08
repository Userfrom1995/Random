"""Tester M4au red-team: head fixer-delta locks (Refs #294).

Locks the 8 fixer commits that landed after the M4at suite without a
covering tester suite on this head:

  AU1: state_bytes requires length positionally (5e280da0). All six
    families expose state_bytes(batch, length, bpe); calling without
    length must raise TypeError so no caller silently scores a default
    length-0 footprint.
  AU2: candidate state flatness (O(1) tier). P1/P2/P3/P4/P5 byte totals
    are identical at length 1k vs 32k (length accepted for API parity
    only); baseline grows with length.
  AU3: tie_embeddings split (af3d168c + b72322d6). Candidates reject
    the override in factory (ValueError); baseline honors it
    (lm_head None, tied forward finite, fewer params than untied).
  AU4: provenance guard message quality (380b8d07). Cross-family load
    (p1 blob as p2) raises SystemExit naming both families, so the
    refusal is actionable, not a bare exit code.
  AU5: fail-open for provenance-free blobs. Hand-made blobs without
    args/model still load same-family (no over-rejection).

Fast and in-process (toy scale, no training, no subprocess).
"""

import pytest
import torch

from postformer.harness.util import load_model
from postformer.models.factory import build_model

FAMILIES = ["transformer", "p1", "p2", "p3", "p4", "p5"]
CANDIDATES = ["p1", "p2", "p3", "p4", "p5"]


def _toy(family):
    m, cfg = build_model(family, "toy", {"vocab": 66})
    return m, cfg


def test_au1_state_bytes_requires_length_all_families():
    """state_bytes(batch) without length must raise TypeError everywhere."""
    for fam in FAMILIES:
        m, _ = _toy(fam)
        with pytest.raises(TypeError):
            m.state_bytes(1)


def test_au2_candidate_state_flat_1k_vs_32k_baseline_grows():
    """Candidates flat across lengths; baseline scales with length."""
    for fam in CANDIDATES:
        m, _ = _toy(fam)
        assert m.state_bytes(1, 1024) == m.state_bytes(1, 32768)
    m, _ = _toy("transformer")
    assert m.state_bytes(1, 32768) > m.state_bytes(1, 1024)


def test_au3_candidates_reject_tie_baseline_honors_it():
    """Factory refuses tie for p1-p5; baseline ties and stays finite."""
    for fam in CANDIDATES:
        with pytest.raises(ValueError):
            build_model(fam, "toy", {"vocab": 66, "tie_embeddings": True})
    tied, _ = build_model("transformer", "toy",
                          {"vocab": 66, "tie_embeddings": True})
    assert tied.lm_head is None
    plain, _ = build_model("transformer", "toy", {"vocab": 66})
    assert sum(p.numel() for p in tied.parameters()) < sum(
        p.numel() for p in plain.parameters())
    ids = torch.randint(0, 66, (1, 8))
    assert torch.isfinite(tied(ids)).all()


def test_au4_provenance_refusal_names_both_families(tmp_path):
    """p1 blob loaded as p2 exits naming p1 and p2."""
    m, cfg = build_model("p1", "toy", {"vocab": 66})
    ckpt = str(tmp_path / "p1.pt")
    torch.save({"state_dict": m.state_dict(), "config": cfg,
                "args": {"model": "p1-toy"}}, ckpt)
    with pytest.raises(SystemExit) as ei:
        load_model("p2-toy", ckpt, None, {"vocab": 66}, "cpu", "fp32")
    msg = str(ei.value)
    assert "p1" in msg and "p2" in msg


def test_au5_provenance_free_blob_still_loads_same_family(tmp_path):
    """Legacy blobs without args/model fail open same-family."""
    m, cfg = build_model("p5", "toy", {"vocab": 66})
    ckpt = str(tmp_path / "legacy.pt")
    torch.save({"state_dict": m.state_dict(), "config": cfg}, ckpt)
    loaded, _, random_init = load_model(
        "p5-toy", ckpt, None, {"vocab": 66}, "cpu", "fp32")
    assert random_init is False
    for k, v in m.state_dict().items():
        assert torch.equal(v, loaded.state_dict()[k]), k
