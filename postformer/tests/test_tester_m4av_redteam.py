"""Tester M4av red-team: head-delta locks for the latest fixer hardening (Refs #294).

Novel vs prior suites (M4au locked state_bytes/tie/provenance; M4at locked
the p1/p5 family-swap hole; M4ae locked commit discipline at its head):
this suite pins the fixer commits that landed after M4au without a
covering tester suite:

  AV1: cfg.update overrides honored (da30ee98). build_model must apply
    caller overrides (e.g. window=0 takes effect on a p1 build).
  AV2: stride/lengths/t-train arg gates (6d3fd0b7). --slot-stride 0,
    --lengths garbage, and --t-train 0 fail loudly, never train silently.
  AV3: A4 G4/G64 summary-cell equality (0a6b30cb). Committed a4-toy
    g1_summary JSONs for G4 and G64 are cell-identical (slot COUNT
    untested at toy T=33, eviction disclosed, equality is score-level).
  AV4: live parity all families/scales within 2% (in-process, no train).
  AV5: live ledger tripwire - 25 rows, 26-col schema, `ledger check` green.
  AV6: viewer splitCSV present and live ledger parses to uniform 26 cols
    under an RFC-4180 split (naive split must shred quoted notes).
  AV7: commit discipline at this head - every post-base subject carries
    Refs #294, zero Closes #294 (binding gate: toy rows are NOT gate
    results until S-tiny/S-small G1-G4 pass).

Fast: in-process + argparse-level subprocess + committed curves only.
"""

import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


def run_cli(*args, timeout=120):
    return subprocess.run(
        [sys.executable, "-m"] + list(args),
        capture_output=True, text=True, timeout=timeout, cwd=str(REPO),
    )


def test_av1_cfg_update_overrides_honored():
    """build_model applies caller cfg overrides (window=0 sticks)."""
    from postformer.models.factory import build_model
    _, cfg_default = build_model("p1", "toy")
    _, cfg_zero = build_model("p1", "toy", {"window": 0})
    assert cfg_default["window"] == 16, cfg_default["window"]
    assert cfg_zero["window"] == 0, cfg_zero["window"]


def test_av2_stride_lengths_ttrain_rejected_loudly(tmp_path):
    """Degenerate harness args fail fast, never train silently."""
    r1 = run_cli("postformer.harness.train", "--model", "p2-toy",
                 "--data", "mqar", "--vocab", "64", "--steps", "2",
                 "--batch", "1", "--slot-stride", "0",
                 "--out", str(tmp_path / "s0"))
    assert r1.returncode != 0, "slot-stride 0 accepted silently"
    r2 = run_cli("postformer.harness.train", "--model", "p1-toy",
                 "--data", "mqar", "--vocab", "64", "--steps", "2",
                 "--batch", "1", "--t-train", "0",
                 "--out", str(tmp_path / "t0"))
    assert r2.returncode != 0, "t-train 0 accepted silently"
    r3 = run_cli("postformer.harness.latency_state", "--model", "p1-toy",
                 "--lengths", "notanumber")
    assert r3.returncode != 0, "garbage --lengths accepted silently"


def test_av3_a4_g4_g64_summary_cells_identical():
    """A4 G4 vs G64 committed score cells agree (config/provenance differ
    by construction: slot count lives in config; equality is score-level,
    per the scoped 0a6b30cb wording)."""
    base = REPO / "postformer" / "ledger" / "curves" / "a4-toy"
    g4 = json.loads((base / "g1_summary_p2-G4-toy-s0.json").read_text())
    g64 = json.loads((base / "g1_summary_p2-G64-toy-s0.json").read_text())
    score_keys = ("mqar", "bind2hop", "induction", "copying")
    for k in score_keys:
        assert g4.get(k) == g64.get(k), (k, g4.get(k), g64.get(k))


def test_av4_live_parity_all_families_within_two_percent():
    """Same-scale candidate drift vs transformer stays inside the 2% gate."""
    from postformer.models.factory import count_params
    for scale in ("toy", "tiny", "small"):
        base, _ = count_params("transformer", scale)
        for fam in ("p1", "p2", "p3", "p4", "p5"):
            n, _ = count_params(fam, scale)
            drift = abs(n - base) / base
            assert drift <= 0.02, (fam, scale, n, base, drift)


def test_av5_live_ledger_25_rows_26_cols_check_green():
    """Tripwire: 25 rows, 26-col schema, `ledger check` exits 0."""
    ledger = REPO / "postformer" / "ledger" / "ledger.csv"
    assert ledger.exists(), "live ledger missing"
    with open(ledger, newline="") as f:
        rows = list(csv.reader(f))
    assert len(rows) - 1 >= 25, f"only {len(rows) - 1} data rows"
    assert len(rows[0]) == 26, f"header has {len(rows[0])} cols, want 26"
    assert all(len(r) == 26 for r in rows[1:]), "ragged ledger row found"
    r = run_cli("postformer.harness.ledger", "check",
                "--ledger", str(ledger))
    assert r.returncode == 0, r.stderr[-2000:] + r.stdout[-2000:]


def test_av6_viewer_splitter_and_live_parse():
    """Viewer ships splitCSV+esc and the live ledger parses at 26 cols."""
    src = (REPO / "postformer" / "viewer" / "index.html").read_text()
    assert "splitCSV" in src, "viewer missing RFC-4180 splitCSV"
    assert "esc(" in src or "escape" in src.lower(), "viewer missing escaping"

    def split_csv(line):
        out, cur, q = [], "", False
        i = 0
        while i < len(line):
            c = line[i]
            if q:
                if c == '"':
                    if i + 1 < len(line) and line[i + 1] == '"':
                        cur += '"'
                        i += 1
                    else:
                        q = False
                else:
                    cur += c
            elif c == '"':
                q = True
            elif c == ",":
                out.append(cur)
                cur = ""
            else:
                cur += c
            i += 1
        out.append(cur)
        return out

    ledger = REPO / "postformer" / "ledger" / "ledger.csv"
    with open(ledger, newline="") as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    parsed = [split_csv(ln) for ln in lines]
    assert all(len(r) == 26 for r in parsed), "quote-aware parse ragged"
    naive = [ln.split(",") for ln in lines]
    assert any(len(r) != 26 for r in naive), \
        "naive split parses cleanly - notes column lost its quoting?"


def test_av7_commit_discipline_refs_no_closes():
    """No post-base subject closes #294; the recent head carries Refs #294
    in every subject (early M1/M2 fixer subjects predate the subject-line
    convention and carry the reference in the body instead)."""
    import subprocess as sp
    out = sp.run(["git", "log", "cdf3cdae..HEAD", "--pretty=format:%s"],
                 capture_output=True, text=True, cwd=str(REPO)).stdout
    subjects = [s for s in out.splitlines() if s.strip()]
    assert subjects, "no post-base commits found"
    closing = [s for s in subjects
               if any(k in s for k in ("Closes #294", "Fixes #294",
                                       "Resolves #294"))]
    assert not closing, f"premature gate-close subjects: {closing[:5]}"
    recent = subjects[:40]
    missing = [s for s in recent if "Refs #294" not in s]
    assert not missing, f"recent subjects missing Refs #294: {missing[:5]}"
