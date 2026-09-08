"""Tester hostile suite for head c55cf6cd (M4ah): current-head ground-truth pins.

Refs #294 (toy/MINI-scale proxies only, never gate results).

Why this suite exists: pins the CURRENT head end-to-end in one fast place:
(AI1) committed m4b p4 ledger cells byte-match curve JSON ground truth
(honesty lock against cell/note drift); (AI2) S-tiny state_bytes match
proof-g4.md pins with 1k-vs-32k flatness and a growing baseline control;
(AI3) prefix invariance across the W boundary for p1/p4 (causality under
hostile prefixes); (AI4) train CLI rejects --window on transformer loudly;
(AI5) ledger append rejects exact duplicates without --force; (AI6) viewer
ships splitCSV plus cell escaping and parses the live 26-col header;
(AI7) no forward_chunk refs in shipped code and no em dashes in scope.
"""

import csv
import json
import pathlib
import re
import subprocess
import sys

import pytest
import torch

from postformer.models.factory import build_model

_HERE = pathlib.Path(__file__).resolve()
_POSTFORMER = _HERE.parents[1]
_LEDGER = _POSTFORMER / "ledger" / "ledger.csv"
_M4B_SUMMARY = _POSTFORMER / "ledger" / "curves" / "m4b-toy" / "g1_summary_p4-toy-s0.json"
_VIEWER = _POSTFORMER / "viewer" / "index.html"
_PROOF = _POSTFORMER / "docs" / "proof-g4.md"


def _ledger_row(model):
    with open(_LEDGER) as f:
        for row in csv.DictReader(f):
            if row["model"] == model and row["seed"] == "0" and row["vocab"] == "64":
                return row
    raise AssertionError(f"row not found: {model}")


def test_ai1_m4b_p4_cells_match_curve_ground_truth():
    """AI1: ledger p4-toy cells byte-match the committed curve JSON."""
    s = json.loads(_M4B_SUMMARY.read_text())
    row = _ledger_row("p4-toy")
    assert float(row["g1_mqar_8"]) == pytest.approx(s["mqar"]["8"]["acc"], abs=1e-12)
    assert float(row["g1_mqar_16"]) == pytest.approx(s["mqar"]["16"]["acc"], abs=1e-12)
    assert float(row["g1_2hop"]) == pytest.approx(s["bind2hop"]["acc"], abs=1e-12)
    # Ground-truth values pinned literally (regression trip-wire):
    assert s["mqar"]["8"]["acc"] == pytest.approx(0.035, abs=1e-12)
    assert s["mqar"]["16"]["acc"] == pytest.approx(0.015625, abs=1e-12)
    assert s["bind2hop"]["acc"] == pytest.approx(0.01, abs=1e-12)


def test_ai2_stiny_state_bytes_match_proof_and_flat():
    """AI2: S-tiny inventories match proof pins; flat 1k vs 32k; T grows."""
    pins = {"p1": 3145728, "p4": 3145728, "p2": 3538944,
            "p3": 4718592, "p5": 4718592}
    for fam, pin in pins.items():
        m, _ = build_model(fam, "tiny", None)
        m.eval()
        assert m.state_bytes(1, 1000) == pin, (fam, m.state_bytes(1, 1000))
        assert m.state_bytes(1, 32000) == pin, (fam, "not flat")
    t, _ = build_model("transformer", "tiny", None)
    t.eval()
    assert t.state_bytes(1, 32000) > 10 * t.state_bytes(1, 1000)
    text = _PROOF.read_text()
    for pin in set(pins.values()):
        assert str(pin) in text, pin


def test_ai3_prefix_invariance_across_w_boundary():
    """AI3: prefix logits invariant to hostile futures (true causality).

    Same prefix, differing trigger tails: the shared-prefix logits must
    match to <=1e-6 even though the prefix spans the toy W=16 boundary.
    (Cross-prefix suffix equality would be FALSE for recurrent memory by
    design: memory legitimately carries prefix information forward.)
    """
    from postformer.models.common import seed_all
    seed_all(1403, "ai3")
    for fam in ["p1", "p4"]:
        m, _ = build_model(fam, "toy", None)
        m.eval()
        pre = torch.randint(0, 66, (1, 18))
        assert pre.shape[1] > 16, "prefix must span the toy W=16 boundary"
        trig_a = torch.full((1, 6), 3, dtype=torch.long)
        trig_b = torch.randint(0, 66, (1, 6))
        a = torch.cat([pre, trig_a], dim=1)
        b = torch.cat([pre, trig_b], dim=1)
        with torch.no_grad():
            la = m.forward(a)[:, :18, :]
            lb = m.forward(b)[:, :18, :]
        d = (la - lb).abs().max().item()
        assert d <= 1e-6, (fam, d)


def test_ai4_train_rejects_window_on_transformer():
    """AI4: --window on a windowless family fails loudly (no silent ignore)."""
    r = subprocess.run(
        [sys.executable, "-m", "postformer.harness.train", "--model", "transformer-toy",
         "--window", "0", "--steps", "1"],
        capture_output=True, text=True, cwd=str(_POSTFORMER.parent),
    )
    assert r.returncode != 0, (r.stdout[-1000:], r.stderr[-1000:])
    assert "--window" in (r.stdout + r.stderr), (r.stdout, r.stderr)


def test_ai5_ledger_rejects_duplicate_append(tmp_path):
    """AI5: exact-duplicate append is rejected unless --force upserts."""
    import shutil
    live = _LEDGER.read_text()
    tmp = tmp_path / "ledger.csv"
    tmp.write_text(live)
    r = subprocess.run(
        [sys.executable, "postformer/harness/ledger.py", "append",
         "--ledger", str(tmp), "--model", "p4-toy", "--seed", "0",
         "--vocab", "64", "--window", "16", "--params", "335316",
         "--train-tokens", "528000", "--notes", "dupe-probe"],
        capture_output=True, text=True, cwd=str(_POSTFORMER.parent),
    )
    assert r.returncode != 0, (r.stdout[-1500:], r.stderr[-1500:])


def test_ai6_viewer_hardened_and_parses_live_header():
    """AI6: viewer has RFC-4180 splitCSV plus escaping; live header is 26 cols."""
    html = _VIEWER.read_text()
    assert "function splitCSV(line)" in html
    assert "line[i + 1] == '\"'" in html, "quote-state logic missing"
    assert "function esc(s)" in html
    assert "esc(v)" in html, "cell() must escape before innerHTML"
    with open(_LEDGER) as f:
        ncols = len(next(csv.reader(f)))
    assert ncols == 26, ncols
    # Naive split must shred the quoted notes column (proves splitCSV load-bearing).
    with open(_LEDGER) as f:
        lines = f.read().splitlines()
    naive_widths = {len(l.split(",")) for l in lines[1:]}
    assert naive_widths != {ncols}, "naive split parses cleanly; splitCSV unneeded?"


def test_ai7_no_forward_chunk_no_emdashes_in_scope():
    """AI7: vacuous chunk API stays dead; scope stays em-dash free."""
    bad = []
    for p in list((_POSTFORMER / "models").glob("*.py")) + list(
            (_POSTFORMER / "harness").glob("*.py")):
        src = p.read_text()
        if "forward_chunk" in src:
            bad.append(str(p))
    assert bad == [], bad
    dash_hits = []
    for p in list(_POSTFORMER.rglob("*.py")) + [_VIEWER, _PROOF]:
        if "\u2014" in p.read_text():
            dash_hits.append(str(p))
    assert dash_hits == [], dash_hits
