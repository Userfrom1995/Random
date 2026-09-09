"""Tester M4bb red-team: lock the M4ba head state (Refs #294).

Novel vs m4ba suite (which locked six-family parity, toy flatness,
p4 toy causality, strict names, tie guards, 25-row ledger, viewer,
CLI routing, n>vocab): this suite locks what the M4ba builder handoff
added on top - the envelope audit doc, the progress log entry, P4
flatness beyond toy (tiny/small, equal to P1), and ledger-to-curve
ground truth for the M4b p4 probe row. All CPU-fast, no training.
"""
import csv
import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
LEDGER = os.path.join(REPO_ROOT, "postformer", "ledger", "ledger.csv")
AUDIT = os.path.join(REPO_ROOT, "postformer", "docs", "envelope-audit.md")
PROGRESS = os.path.join(REPO_ROOT, "progress",
                         "294-post-transformer-sequence-architecture.md")


def test_bb1_envelope_audit_exists_and_honest():
    """Audit pins 25 rows, discloses H4 NEGATIVE + A2 INVALID, no gate claim."""
    assert os.path.exists(AUDIT), "envelope audit missing"
    src = open(AUDIT).read()
    assert "25 rows" in src, "row count pin missing"
    assert "NOT gate results" in src, "toy honesty missing"
    assert "Refs #294" in src
    assert "H4 NEGATIVE" in src, "p4 negative read must be disclosed"
    assert "INVALID" in src, "A2 invalidation must be disclosed"
    low = src.lower()
    assert "closes #294 only" in low or "waits on s-tiny" in low, \
        "Closes must stay conditional"


def test_bb2_progress_logs_m4ba_handoff():
    """Progress log records the M4ba verification handoff."""
    src = open(PROGRESS).read()
    assert "M4ba" in src, "M4ba handoff not logged"
    assert "Refs #294" in src


def test_bb3_p4_flat_beyond_toy_and_equal_to_p1():
    """P4 state_bytes flat 1k vs 32k at tiny/small and equal to P1."""
    from postformer.models.factory import build_model
    for scale in ("tiny", "small"):
        p4, _ = build_model("p4", scale, {})
        p1, _ = build_model("p1", scale, {})
        a, b = p4.state_bytes(1, 1000, 4), p4.state_bytes(1, 32000, 4)
        assert a == b, (scale, a, b)
        assert a == p1.state_bytes(1, 1000, 4), (scale, a)


def test_bb4_m4b_p4_ledger_row_matches_curve():
    """Ledger p4-toy row cells match the m4b curve summary ground truth."""
    summ = os.path.join(REPO_ROOT, "postformer", "ledger", "curves",
                        "m4b-toy", "g1_summary_p4-toy-s0.json")
    assert os.path.exists(summ), "m4b p4 summary missing"
    g = json.load(open(summ))
    with open(LEDGER, newline="") as f:
        rows = list(csv.DictReader(f))
    p4rows = [r for r in rows if r.get("model") == "p4-toy"]
    assert len(p4rows) == 1, len(p4rows)
    row = p4rows[0]
    assert abs(float(row["g1_mqar_8"]) - float(g["mqar"]["8"]["acc"])) < 1e-9, \
        (row["g1_mqar_8"], g["mqar"]["8"])
    assert "H4 NEGATIVE" in (row.get("notes") or ""), row.get("notes")


def test_bb5_no_closes_claims_in_ledger_or_audit():
    """No bare Closes #294 pass claims in ledger cells or audit doc."""
    with open(LEDGER, newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k, v in r.items():
            if isinstance(v, str):
                assert "closes #294" not in v.lower(), (k, v)
    audit_low = open(AUDIT).read().lower()
    for line in audit_low.splitlines():
        if "closes #294" in line:
            assert "only" in line or "waits on" in line, line
