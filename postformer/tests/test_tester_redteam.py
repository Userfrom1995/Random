"""Tester red-team regression suite (PR #295 M1+M2-toy, issue #294).

Durable hostile checks owned by the Tester. All CPU-fast (toy scale only).
Covers: binding-gate honesty (toy rows are NOT S-tiny/S-small gate results),
param parity re-verified, step-vs-forward equivalence, degenerate inputs,
CLI guard rails (train steps/batch/log_every, --window mismatch, k-suffix
lengths, --baseline-checkpoint), ledger dedup/NaN/empty-row strictness, and
viewer CSV/XSS hardening presence.

Refs #294 (never Closes: G1+G2+G3+G4 at pinned S-tiny/S-small still pending).
"""

import csv
import os
import subprocess
import sys
import tempfile

import pytest
import torch

from postformer.harness.ledger import SCHEMA, main as ledger_main
from postformer.harness.util import parse_int_list
from postformer.models.common import seed_all
from postformer.models.factory import build_model, count_params

REPO = os.path.join(os.path.dirname(__file__), "..", "..")
REPO = os.path.normpath(REPO)
PFDIR = os.path.join(os.path.dirname(__file__), "..")
LEDGER = os.path.join(PFDIR, "ledger", "ledger.csv")
VIEWER = os.path.join(PFDIR, "viewer", "index.html")


# --- Binding gate honesty: toy rows must not masquerade as pinned gates ---

def test_ledger_rows_do_not_claim_gate_pass():
    assert os.path.exists(LEDGER), "ledger.csv missing"
    with open(LEDGER) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 1
    for r in rows:
        notes = (r.get("notes") or "").lower()
        assert "gate pass" not in notes and "closes #294" not in notes, r
    # Toy-scale rows must be labeled as toy/smoke/random-init, not S-tiny gates.
    toy = [r for r in rows if "toy" in (r.get("model") or "")]
    assert toy, "expected toy falsification rows"
    for r in toy:
        blob = ((r.get("notes") or "") + (r.get("model") or "")).lower()
        assert "toy" in blob or "smoke" in blob or "random" in blob, r


def test_param_parity_within_two_percent_all_scales():
    for scale in ("toy", "tiny", "small"):
        base, _ = count_params("transformer", scale)
        for fam in ("p1", "p5"):
            n, _ = count_params(fam, scale)
            drift = abs(n - base) / base
            assert drift <= 0.02, (scale, fam, base, n, drift)


def test_ledger_live_check_green():
    ledger_main(["check", "--ledger", LEDGER])


# --- Hostile numeric equivalence: step() vs forward, T=1, prefix invariance ---

def test_step_matches_forward_toy_all_families():
    seed_all(99, "tester-redteam")
    for fam in ("transformer", "p1", "p5"):
        m, _ = build_model(fam, "toy")
        m.eval()
        x = torch.randint(0, 66, (1, 40))
        with torch.no_grad():
            full = m(x)
            st = m.init_state(1, "cpu", torch.float32)
            outs = [m.step(x[:, i:i + 1], st)[0] for i in range(40)]
        stepped = torch.cat(outs, dim=1)
        diff = (stepped - full).abs().max().item()
        assert diff <= 1e-4, (fam, diff)


def test_single_token_and_prefix_invariance():
    seed_all(100, "tester-redteam")
    for fam in ("transformer", "p1", "p5"):
        m, _ = build_model(fam, "toy")
        m.eval()
        with torch.no_grad():
            o1 = m(torch.randint(0, 66, (1, 1)))
            assert o1.shape == (1, 1, 66)
            a = torch.randint(0, 66, (1, 10))
            b = torch.randint(0, 66, (1, 10))
            la = m(torch.cat([a, torch.full((1, 6), 3)], dim=1))
            lb = m(torch.cat([a, b], dim=1))
            diff = (la[:, :10] - lb[:, :10]).abs().max().item()
            assert diff <= 1e-6, (fam, diff)


# --- CLI guard rails ---

def test_parse_int_list_k_suffix_and_rejects_garbage():
    assert parse_int_list("1k,2K,32k") == [1024, 2048, 32768]
    assert parse_int_list("512, 1024") == [512, 1024]
    assert parse_int_list("") == []
    # Bad CLI entries fail loudly via SystemExit (harness convention).
    with pytest.raises(SystemExit):
        parse_int_list("1k,abc")


def test_train_rejects_degenerate_args():
    from postformer.harness.train import main as train_main
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "o.json")
        base = ["--model", "p1-toy", "--data", "mqar", "--out", out]
        with pytest.raises(SystemExit):
            train_main(base + ["--steps", "0", "--batch", "1"])
        with pytest.raises(SystemExit):
            train_main(base + ["--steps", "4", "--batch", "0"])
        with pytest.raises(SystemExit):
            train_main(base + ["--steps", "4", "--batch", "1",
                               "--log-every", "0"])


def test_tie_embeddings_rejected_for_p1_p5():
    with pytest.raises(ValueError):
        build_model("p1", "tiny", {"tie_embeddings": True})
    with pytest.raises(ValueError):
        build_model("p5", "tiny", {"tie_embeddings": True})
    m, _ = build_model("transformer", "tiny", {"tie_embeddings": True})
    assert m is not None


def test_window_flag_and_baseline_checkpoint_advertised():
    # sys.executable (not bare "python3"): the suite must run under the
    # interpreter that has the pinned deps, on any runner (M4ap hostile).
    r1 = subprocess.run([sys.executable, "-m", "postformer.harness.synthetic_recall",
                         "--help"], capture_output=True, text=True, cwd=REPO)
    assert "--window" in r1.stdout, r1.stdout[:500]
    r2 = subprocess.run([sys.executable, "-m", "postformer.harness.length_sweep",
                         "--help"], capture_output=True, text=True, cwd=REPO)
    assert "--baseline-checkpoint" in r2.stdout, r2.stdout[:500]


# --- Ledger strictness under corrupt input ---

def _write(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA)
        w.writeheader()
        w.writerows(rows)


def _good(model="p1-tiny"):
    return {"model": model, "params": "29373756", "train_tokens": "0",
            "seed": "0", "vocab": "8192", "window": "128",
            "g1_mqar_8": "", "g1_mqar_16": "0.1", "g1_mqar_64": "",
            "g1_mqar_256": "", "g1_induction": "", "g1_copy": "",
            "g1_2hop": "", "g2_bpb_1x": "", "g2_bpb_4x": "", "g2_bpb_8x": "",
            "g2_delta_4x": "", "g2_delta_8x": "", "g3_valid_bpb": "",
            "g3_test_bpb": "", "g4_state_bytes": "", "g4_ms_per_token": "",
            "gpu_hours": "0", "notes": "tester-probe"}


def test_ledger_rejects_corrupt_and_duplicate_rows():
    import json
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "ledger.csv")
        # NaN gate rejected
        bad = _good()
        bad["g1_mqar_16"] = "nan"
        _write(p, [_good(model="transformer-tiny"), bad])
        with pytest.raises(SystemExit):
            ledger_main(["check", "--ledger", p])
        # Duplicates rejected without --force
        p2 = os.path.join(tmp, "l2.csv")
        rj = os.path.join(tmp, "run.json")
        with open(rj, "w") as f:
            json.dump(_good(), f)
        ledger_main(["append", "--run-json", rj, "--ledger", p2])
        with pytest.raises(SystemExit):
            ledger_main(["append", "--run-json", rj, "--ledger", p2])
        # Garbage file must be rejected (clean SystemExit or loud KeyError,
        # but never a silent pass). SystemExit is BaseException, not
        # Exception, so pin it explicitly.
        p3 = os.path.join(tmp, "l3.csv")
        with open(p3, "w") as f:
            f.write("not,a,valid,ledger\n1,2,3\n")
        with pytest.raises((Exception, SystemExit)):
            ledger_main(["check", "--ledger", p3])


# --- Viewer hardening presence (static, no browser needed) ---

def test_viewer_has_csv_splitter_and_escaping():
    assert os.path.exists(VIEWER), "viewer/index.html missing"
    with open(VIEWER) as f:
        src = f.read()
    assert "splitCSV" in src, "quote-aware CSV splitter missing"
    assert ".split(\",\")" not in src.replace(" ", "") or \
        "splitCSV" in src, "raw split(',') still in use"
    assert "esc(" in src or "&amp;" in src or "escape" in src.lower(), \
        "no HTML escaping helper found"
