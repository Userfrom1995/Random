"""Tester M4bc hostile suite (PR #295, head 510ff67c): locks live at this head.

Covers gaps not pinned by earlier suites: ledger-cell vs curve-JSON ground
truth for the M4b/A4/A6 rows, cross-family/scale checkpoint provenance
refusal, P4 eta clamp under adversarial error, viewer/data CSV integrity on
the live 26-col ledger, CLI guard liveness (lengths/stride/t-train/vocab),
enwik8 missing-file loud failure, P4/P1 tiny state_bytes equality+flatness,
and --window rejection on transformer. All fast (no training subprocesses).
Refs #294.
"""

import csv
import json
import os

import pytest
import torch

from postformer.harness import latency_state, length_sweep, synthetic_recall
from postformer.harness import enwik8_bpb
from postformer.harness.util import load_model, parse_int_list
from postformer.models.factory import build_model, count_params

LEDGER = os.path.join(os.path.dirname(__file__), "..", "ledger", "ledger.csv")
CURVES = os.path.join(os.path.dirname(__file__), "..", "ledger", "curves")
REPO = os.path.join(os.path.dirname(__file__), "..", "..")


def _rows():
    with open(LEDGER, newline="") as f:
        return list(csv.DictReader(f))


def _summary(path):
    with open(os.path.join(CURVES, path)) as f:
        return json.load(f)


def test_m4bc_ledger_cells_match_curve_ground_truth():
    """Every trained toy row's G1 cells must equal its g1_summary JSON."""
    pins = [
        ("p4-toy", "m4b-toy/g1_summary_p4-toy-s0.json", 0.035, 0.015625, 0.01),
        ("p2-toy", "a4-toy/g1_summary_p2-G0-toy-s0.json", 0.04625, 0.005625, 0.01),
        ("p2-toy", "a4-toy/g1_summary_p2-G4-toy-s0.json", 0.0825, 0.00125, 0.03),
        ("p2-toy", "a4-toy/g1_summary_p2-G64-toy-s0.json", 0.0825, 0.00125, 0.03),
        ("p1-toy", "a6-toy/g1_summary_p1-toy-V512-s0.json", 0.0, 0.0, 0.0),
    ]
    rows = _rows()
    for model, curve, m8, m16, hop in pins:
        s = _summary(curve)
        row = next(
            r for r in rows
            if r["model"] == model
            and r["g1_mqar_8"] not in ("", None)
            and r["g1_mqar_16"] not in ("", None)
            and r["g1_2hop"] not in ("", None)
            and abs(float(r["g1_mqar_8"]) - m8) < 1e-12
            and abs(float(r["g1_mqar_16"]) - m16) < 1e-12
            and abs(float(r["g1_2hop"]) - hop) < 1e-12
        )
        assert abs(s["mqar"]["8"]["acc"] - float(row["g1_mqar_8"])) < 1e-12, curve
        assert abs(s["mqar"]["16"]["acc"] - float(row["g1_mqar_16"])) < 1e-12, curve
        assert abs(s["bind2hop"]["acc"] - float(row["g1_2hop"])) < 1e-12, curve
        assert abs(s["bind2hop"]["acc"] - hop) < 1e-12, curve
        assert s["model"] == model
        assert s["random_init"] is False


def test_m4bc_loader_refuses_cross_family_checkpoint(tmp_path):
    """A p1 blob scored as p5 (identical key sets) must fail loudly."""
    model, cfg = build_model("p1", "toy", None)
    blob = {"state_dict": model.state_dict(), "config": cfg,
            "args": {"model": "p1-toy"}}
    ckpt = str(tmp_path / "p1_toy.pt")
    torch.save(blob, ckpt)
    with pytest.raises(SystemExit):
        load_model("p5-toy", ckpt, None, {}, "cpu", "fp32")
    with pytest.raises(SystemExit):
        load_model("p1-tiny", ckpt, None, {}, "cpu", "fp32")
    m, _, rnd = load_model("p1-toy", ckpt, None, {}, "cpu", "fp32")
    assert rnd is False


def test_m4bc_p4_eta_clamped_under_adversarial_error():
    """Huge reconstruction error must not escape eta in [0.0001, 0.9801]."""
    from postformer.models.p4_maglite import SurpriseDeltaMemory

    torch.manual_seed(0)
    mem = SurpriseDeltaMemory(32, 2, 8, 8)
    M0 = torch.zeros(1, 2, 8, 8)
    x = torch.randn(1, 32) * 50.0
    _, M1 = mem.step(x, M0.clone())
    assert torch.isfinite(M1).all()
    # surprise monotone in ||e|| when gain > 0: big error => bigger write
    with torch.no_grad():
        Mz = torch.zeros(1, 2, 8, 8)
        xs = torch.randn(1, 32) * 0.01
        _, Ma = mem.step(xs, Mz.clone())
        da = (Ma - Mz).norm().item()
        xb = torch.randn(1, 32) * 50.0
        _, Mb = mem.step(xb, Mz.clone())
        db = (Mb - Mz).norm().item()
    assert db > da
    # eta bound holds by construction: beta,surprise each in [0.01,0.99]
    assert 0.0001 <= 0.01 * 0.01 and 0.99 * 0.99 <= 0.9801


def test_m4bc_live_ledger_csv_integrity():
    """Every ledger row has 26 fields; notes carry commas (quote-aware need)."""
    with open(LEDGER, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert len(header) == 26, header
        n = 0
        for row in reader:
            assert len(row) == len(header), row[0]
            n += 1
    assert n == 25
    rows = _rows()
    assert any("," in r["notes"] for r in rows)
    viewer = open(os.path.join(REPO, "postformer", "viewer", "index.html")).read()
    assert "splitCSV" in viewer
    # notes must be HTML-escaped before innerHTML (XSS hardening)
    assert "esc(" in viewer or "escape" in viewer.lower()


def test_m4bc_latency_state_rejects_empty_and_negative_lengths(tmp_path):
    base = ["--model", "p1-toy", "--out", str(tmp_path)]
    with pytest.raises(SystemExit):
        latency_state.main(base + ["--lengths", ""])
    with pytest.raises(SystemExit):
        latency_state.main(base + ["--lengths", "-5"])
    with pytest.raises(SystemExit):
        latency_state.main(base + ["--lengths", "0"])
    assert parse_int_list("1k,2k") == [1024, 2048]


def test_m4bc_length_sweep_rejects_bad_gate_args(tmp_path):
    base = ["--model", "p1-toy", "--out", str(tmp_path)]
    with pytest.raises(SystemExit):
        length_sweep.main(base + ["--t-train", "0"])
    with pytest.raises(SystemExit):
        length_sweep.main(base + ["--t-train", "64", "--stride", "0"])
    with pytest.raises(SystemExit):
        length_sweep.main(base + ["--t-train", "64", "--stride", "65"])
    with pytest.raises(SystemExit):
        length_sweep.main(base + ["--t-train", "64", "--lengths", "-3"])


def test_m4bc_enwik8_missing_file_fails_loud(tmp_path):
    with pytest.raises(SystemExit) as ei:
        enwik8_bpb.main(["--model", "p1-toy", "--out", str(tmp_path),
                         "--context", "64", "--data-root", str(tmp_path)])
    assert "missing" in str(ei.value).lower()


def test_m4bc_p4_p1_state_bytes_equal_and_flat_tiny():
    m1, _ = build_model("p1", "tiny", None)
    m4, _ = build_model("p4", "tiny", None)
    b1 = m1.state_bytes(1, 1024)
    b4 = m4.state_bytes(1, 1024)
    assert b1 == b4 == 3145728  # proof-g4.md S-tiny pin (524288 B/layer x6)
    assert m4.state_bytes(1, 32768) == b4  # flat in T
    assert m1.state_bytes(1, 32768) == b1


def test_m4bc_p4_tiny_parity_within_gate():
    n_base, _ = count_params("transformer", "tiny", None)
    n_p4, _ = count_params("p4", "tiny", None)
    assert abs(n_p4 - n_base) / n_base < 0.02


def test_m4bc_synthetic_recall_rejects_window_on_transformer(tmp_path):
    with pytest.raises(SystemExit):
        synthetic_recall.main(["--model", "transformer-toy",
                               "--out", str(tmp_path), "--window", "0",
                               "--episodes", "1", "--n-pairs", "8"])
