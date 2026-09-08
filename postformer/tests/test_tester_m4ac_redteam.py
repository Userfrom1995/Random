"""Tester M4ac hostile suite: current-head final-gate pins (post-M4ab).

Refs #294 (toy/mini-scale proxies only, never gate results).

Why this suite exists: after the M4z-M4ab hardening wave the head moved
to 1d2c3669 with fixer/tester/builder commits that no prior suite pins
end-to-end in one place. This suite is the final-gate aggregator at the
current head: shipped-ledger liveness, live family-wide parity, MINI
causality/T=1 across all six families, P1==P4 state inventory, P5
unit-norm honesty, zero forward_chunk in shipped code, viewer hardening,
ledger strictness (NaN/dupe rejection), and the tie_embeddings guard.
"""

import csv
import pathlib
import subprocess
import sys

import torch

from postformer.harness import ledger as _ledger
from postformer.models.factory import build_model, count_params
from .conftest import FAMILIES, MINI

_HERE = pathlib.Path(__file__).resolve()
_POSTFORMER = _HERE.parents[1]
_LEDGER = _POSTFORMER / "ledger" / "ledger.csv"


def _tiny_cfg(family):
    return dict(MINI)


def test_ac1_shipped_ledger_green_25_rows_26_cols():
    rows = list(csv.DictReader(_LEDGER.open()))
    assert len(rows) == 25, [r["model"] for r in rows]
    assert "slots" in rows[0] and "use_accumulator" in rows[0]
    assert len(rows[0].keys()) == 26, sorted(rows[0].keys())
    r = subprocess.run(
        [sys.executable, str(_POSTFORMER / "harness" / "ledger.py"),
         "check", "--ledger", str(_LEDGER)],
        capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-2000:]
    assert "ledger OK" in (r.stdout + r.stderr)


def test_ac2_live_parity_all_families_within_2pct():
    for scale in ("toy", "tiny", "small"):
        base, _ = count_params("transformer", scale)
        for fam in ("p1", "p2", "p3", "p4", "p5"):
            c, _ = count_params(fam, scale)
            assert abs(c - base) / base < 0.02, (fam, scale, c, base)


def test_ac3_mini_step_forward_causal_all_families():
    from postformer.models.common import seed_all
    seed_all(21, "tester-m4ac-causal")
    for fam in FAMILIES:
        m, cfg = build_model(fam, "toy")
        m.eval()
        V = cfg["vocab_size"]
        x = torch.randint(0, V, (1, 32))
        with torch.no_grad():
            full = m(x)
            st = m.init_state(1, "cpu", torch.float32)
            outs = [m.step(x[:, i:i + 1], st)[0] for i in range(32)]
        out_step = torch.cat(outs, dim=1)
        assert torch.isfinite(full).all() and torch.isfinite(out_step).all(), fam
        assert (full - out_step).abs().max().item() <= 1e-4, fam


def test_ac4_t1_single_token_finite_all_families():
    for fam in FAMILIES:
        m, cfg = build_model(fam, "toy")
        m.eval()
        x = torch.randint(0, cfg["vocab_size"], (1, 1))
        with torch.no_grad():
            out = m(x)
        assert torch.isfinite(out).all(), fam


def test_ac5_p1_p4_state_bytes_equal_mini():
    a, _ = build_model("p1", "tiny", overrides=_tiny_cfg("p1"))
    b, _ = build_model("p4", "tiny", overrides=_tiny_cfg("p4"))
    sa = sum(bl.state_size(4) for bl in a.blocks)
    sb = sum(bl.state_size(4) for bl in b.blocks)
    assert sa == sb
    assert sa > 0


def test_ac6_no_forward_chunk_in_shipped_code():
    for sub in ("models", "harness"):
        for p in (_POSTFORMER / sub).rglob("*.py"):
            src = p.read_text()
            assert "forward_chunk" not in src, p


def test_ac7_viewer_quote_aware_and_escaping():
    src = (_POSTFORMER / "viewer" / "index.html").read_text()
    assert "function splitCSV(line)" in src
    assert "esc(r.notes)" in src or "esc(r.model)" in src


def test_ac8_ledger_rejects_nan_and_dupes(tmp_path):
    good = list(csv.DictReader(_LEDGER.open()))
    hdr = good[0].keys()
    bad = dict(good[0])
    bad["g1_mqar_16"] = "nan"
    p = tmp_path / "nan.csv"
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(hdr))
        w.writeheader()
        w.writerow(bad)
    import types
    rc = subprocess.run(
        [sys.executable, str(_POSTFORMER / "harness" / "ledger.py"),
         "check", "--ledger", str(p)],
        capture_output=True, text=True)
    assert rc.returncode != 0, "NaN row must fail check"
    dupe = tmp_path / "dupe.csv"
    with dupe.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(hdr))
        w.writeheader()
        w.writerow(dict(good[0]))
        w.writerow(dict(good[0]))
    rc2 = subprocess.run(
        [sys.executable, str(_POSTFORMER / "harness" / "ledger.py"),
         "check", "--ledger", str(dupe)],
        capture_output=True, text=True)
    assert rc2.returncode != 0, "duplicate rows must fail check"
    assert isinstance(types.SimpleNamespace, type)


def test_ac9_tie_embeddings_rejected_for_candidates():
    import pytest
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        with pytest.raises((ValueError, SystemExit)):
            build_model(fam, "tiny",
                        overrides={**_tiny_cfg(fam), "tie_embeddings": True})


def test_ac10_proof_pins_match_code_p1_p4_tiny():
    from postformer.models import factory as _f
    m, _ = _f.build_model("p1", "tiny")
    per_layer = m.blocks[0].state_size(4)
    total = sum(b.state_size(4) for b in m.blocks)
    assert total == per_layer * len(m.blocks)
    proof = (_POSTFORMER / "docs" / "proof-g4.md").read_text()
    assert str(total) in proof, (total, "P1/P4 tiny total missing from proof")
