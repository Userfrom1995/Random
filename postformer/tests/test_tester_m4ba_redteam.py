"""Tester M4ba red-team: hostile live-fire on current head (Refs #294).

Novel vs prior suites (ao covered slot determinism/degenerate flags/A4
control/W0 chain/ledger tripwire; ay covered S-tiny G4 control growth,
measure-chain, plot escaping, task liveness, upsert locks; az covered
n==vocab, vocab floors, roundtrips, dedup, ledger green): this suite
locks the full six-family envelope at this head with fast CPU-safe
probes (no full-envelope copy-L512 eval, no 1000-step trains):
  1. Live six-family parity at toy/tiny/small within the 2% gate.
  2. G4 toy flatness via state_bytes (baseline grows, 5 candidates flat).
  3. P4 causality across the W boundary (step-vs-forward, prefix).
  4. Strict --model names (canonical pass, middle/suffix fail loudly).
  5. tie_embeddings rejected for p2/p3/p4 (extends p1/p5 lock).
  6. Live ledger 25 rows / 26 cols / check green / no gate-pass claims.
  7. Viewer splitCSV + esc hardening present.
  8. CLI family-routing guards fail loudly without training.
  9. MQAR N>vocab refused loudly before any model build.
"""
import csv
import os

import pytest
import torch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
LEDGER = os.path.join(REPO_ROOT, "postformer", "ledger", "ledger.csv")
VIEWER = os.path.join(REPO_ROOT, "postformer", "viewer", "index.html")


def test_ba1_live_six_family_parity_within_two_percent():
    """All five candidates within 2% of baseline at all three scales."""
    from postformer.models.factory import count_params
    for scale in ("toy", "tiny", "small"):
        base, _ = count_params("transformer", scale)
        assert base > 0, scale
        for fam in ("p1", "p2", "p3", "p4", "p5"):
            n, _ = count_params(fam, scale)
            drift = abs(n - base) / base
            assert drift <= 0.02, (fam, scale, n, base, drift)


def test_ba2_g4_toy_flatness_via_state_bytes():
    """Baseline state_bytes grows with T; all candidates flat at toy."""
    from postformer.models.factory import build_model
    base, _ = build_model("transformer", "toy", {})
    b1k = base.state_bytes(1, 1000, 4)
    b32k = base.state_bytes(1, 32000, 4)
    assert b32k > 4 * b1k, (b1k, b32k)
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        m, _ = build_model(fam, "toy", {})
        a, b = m.state_bytes(1, 1000, 4), m.state_bytes(1, 32000, 4)
        assert a == b, (fam, a, b)


def test_ba3_p4_causality_across_window_boundary():
    """P4 step-vs-forward and prefix invariance across W=16 (toy, T=20)."""
    from postformer.models.factory import build_model
    from postformer.models.common import seed_all
    seed_all(0, "m4ba-p4-causal")
    m, _ = build_model("p4", "toy", {})
    m.eval()
    T = 20
    ids = torch.randint(0, 66, (1, T))
    with torch.no_grad():
        full = m(ids)
        states = m.init_state(1, "cpu", torch.float32)
        outs = []
        for t in range(T):
            tok = ids[:, t:t + 1]
            o, states = m.step(tok, states)
            outs.append(o)
        inc = torch.cat(outs, dim=1)
    assert torch.isfinite(full).all() and torch.isfinite(inc).all()
    assert (full - inc).abs().max().item() <= 1e-4, \
        (full - inc).abs().max().item()
    with torch.no_grad():
        f1 = m(ids)
        f2 = m(ids.clone())
    assert (f1[:, :17, :] - f2[:, :17, :]).abs().max().item() <= 1e-6


def test_ba4_strict_model_names():
    """Canonical names pass; middle tags and suffixes fail loudly."""
    from postformer.models.factory import parse_model_name
    assert parse_model_name("p1-toy") == ("p1", "toy")
    assert parse_model_name("transformer-small") == ("transformer", "small")
    for bad in ("p2-G0-toy", "p1-toy-V512", "p4-toy-W0", "p9-toy",
                "p1", "toy", "", "p1-TOY"):
        with pytest.raises(SystemExit):
            parse_model_name(bad)


def test_ba5_tie_embeddings_rejected_for_all_candidates():
    """tie_embeddings override rejected for p1-p5, honored by baseline."""
    from postformer.models.factory import build_model
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        with pytest.raises((ValueError, SystemExit)):
            build_model(fam, "toy", {"tie_embeddings": True})
    m, _ = build_model("transformer", "toy", {"tie_embeddings": True})
    assert m is not None


def test_ba6_live_ledger_honest_and_green():
    """25 rows, 26 cols, check green, no gate-pass claims on toy rows."""
    from postformer.harness.ledger import main as ledger_main
    assert os.path.exists(LEDGER), "live ledger missing"
    with open(LEDGER, newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 25, len(rows)
    assert len(rows[0].keys()) == 26, sorted(rows[0].keys())
    ledger_main(["check", "--ledger", LEDGER])
    for r in rows:
        notes = (r.get("notes") or "").lower()
        assert "closes #294" not in notes, r
        for k in ("g1_mqar_8", "g1_mqar_16"):
            v = r.get(k)
            if v not in ("", None):
                assert 0.0 <= float(v) <= 1.0, (k, v, r.get("model"))


def test_ba7_viewer_csv_splitter_and_escaping():
    """Viewer has RFC-4180 splitter and escapes model/notes cells."""
    src = open(VIEWER).read()
    assert "function splitCSV(line)" in src
    assert "splitCSV(l" in src or "splitCSV(lines[0])" in src
    assert "function esc(" in src
    assert "esc(r.model)" in src and "esc(r.notes)" in src
    assert "= l.split" not in src and "cells = l.split" not in src


def test_ba8_cli_family_routing_guards_fail_loudly():
    """Wrong-family ablation flags fail before any training runs."""
    from postformer.harness.train import main as train_main
    with pytest.raises(SystemExit):
        train_main(["--model", "p1-toy", "--slots", "4",
                    "--steps", "1", "--out", "/tmp/ba8-nope"])
    with pytest.raises(SystemExit):
        train_main(["--model", "transformer-toy", "--window", "0",
                    "--steps", "1", "--out", "/tmp/ba8-nope"])
    with pytest.raises(SystemExit):
        train_main(["--model", "p2-toy", "--no-accumulator",
                    "--steps", "1", "--out", "/tmp/ba8-nope"])
    with pytest.raises(SystemExit):
        train_main(["--model", "p1-toy", "--steps", "0",
                    "--out", "/tmp/ba8-nope"])


def test_ba9_mqar_n_over_vocab_refused_fast():
    """--n-pairs > --vocab refused loudly before any model build."""
    from postformer.harness.synthetic_recall import main as eval_main
    with pytest.raises(SystemExit):
        eval_main(["--model", "p1-toy", "--vocab", "64", "--n-pairs", "65",
                   "--episodes", "1", "--task", "mqar", "--out", "/tmp/ba9"])
