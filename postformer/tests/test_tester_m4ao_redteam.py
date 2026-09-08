"""Tester M4ao red-team: hostile live-fire on current head (Refs #294).

Novel vs prior suites (aj covered p5 determinism + E2E chain; af covered
negative ledger cells; aa covered parse_int_list): this suite attacks the
paths no prior suite runs live:
  1. p2 slot-buffer determinism (oldest-evict ordering is the risky path;
     aj3 pinned p5 only) - same (model, seed) twice -> identical loss.
  2. Degenerate CLI flags end to end: --slots -1 / --window -1 must fail
     loudly (nonzero exit), never train silently.
  3. A4 control honesty live: p2-toy --slots 0 is param-identical to the
     default-slots build (pure-SSD control claim).
  4. A2 control path live: p1-toy trains with --window 0 and the checkpoint
     evaluates via synthetic_recall --window 0 (the M2-mandated guard path).
  5. Live repo ledger: >= 25 rows and `ledger check` exits 0 on the real
     ledger (tripwire against ledger corruption at this head).
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest
import torch

REPO = Path(__file__).resolve().parents[2]


def run_cli(*args, timeout=600):
    return subprocess.run(
        [sys.executable, "-m"] + list(args),
        capture_output=True, text=True, timeout=timeout, cwd=str(REPO),
    )


def test_ao1_p2_slot_path_deterministic(tmp_path):
    """p2 slot eviction ordering must be reproducible across reruns."""
    losses = []
    for i in range(2):
        out = tmp_path / f"p2det{i}"
        r = run_cli("postformer.harness.train", "--model", "p2-toy",
                    "--data", "mqar", "--vocab", "64", "--steps", "6",
                    "--batch", "2", "--seed", "7", "--out", str(out))
        assert r.returncode == 0, r.stderr[-2000:]
        cands = list(out.glob("train_summary*.json"))
        assert cands, f"no train summary in {out}"
        losses.append(json.loads(cands[0].read_text())["final_loss"])
    assert losses[0] == losses[1], losses
    assert all(torch.isfinite(torch.tensor(v)) for v in losses), losses


def test_ao2_negative_slots_window_rejected_loudly(tmp_path):
    """--slots -1 and --window -1 must fail, never train silently."""
    r1 = run_cli("postformer.harness.train", "--model", "p2-toy",
                 "--data", "mqar", "--vocab", "64", "--steps", "2",
                 "--batch", "1", "--slots", "-1",
                 "--out", str(tmp_path / "negslots"))
    assert r1.returncode != 0, "negative --slots accepted silently"
    r2 = run_cli("postformer.harness.train", "--model", "p1-toy",
                 "--data", "mqar", "--vocab", "64", "--steps", "2",
                 "--batch", "1", "--window", "-1",
                 "--out", str(tmp_path / "negwin"))
    assert r2.returncode != 0, "negative --window accepted silently"


def test_ao3_p2_slots_zero_param_identical():
    """A4 control: slots=0 build has identical params to default build."""
    from postformer.models.factory import count_params
    default_n = count_params("p2", "toy")[0]
    zero_n = count_params("p2", "toy", {"slots": 0})[0]
    assert default_n == zero_n, (default_n, zero_n)


def test_ao4_window_zero_train_eval_chain(tmp_path):
    """A2 control path: --window 0 trains, checkpoint evals with --window 0."""
    out = tmp_path / "w0"
    r = run_cli("postformer.harness.train", "--model", "p1-toy",
                "--data", "mqar", "--vocab", "64", "--steps", "4",
                "--batch", "2", "--window", "0", "--seed", "3",
                "--out", str(out))
    assert r.returncode == 0, r.stderr[-2000:]
    ckpts = list(out.glob("*.pt"))
    assert ckpts, f"no checkpoint in {out}"
    evo = tmp_path / "w0eval"
    evo.mkdir()
    r2 = run_cli("postformer.harness.synthetic_recall",
                 "--model", "p1-toy", "--checkpoint", str(ckpts[0]),
                 "--vocab", "64", "--n-pairs", "8", "--episodes", "4",
                 "--window", "0", "--out", str(evo),
                 # Full-envelope eval (task=all incl. copy L512 greedy
                 # decode) costs ~14 min unloaded on CPU (M4ap measured);
                 # the budget must cover it, not the product's correctness.
                 timeout=1500)
    assert r2.returncode == 0, r2.stderr[-2000:]
    sums = list(evo.glob("g1_summary*.json"))
    assert sums, f"no g1 summary in {evo}"
    payload = json.loads(sums[0].read_text())
    assert payload, "empty g1 summary"


def test_ao5_live_repo_ledger_rows_and_check_green():
    """Tripwire: live ledger has >= 25 rows and `ledger check` exits 0."""
    ledger = REPO / "postformer" / "ledger" / "ledger.csv"
    assert ledger.exists(), "live ledger missing"
    with open(ledger, newline="") as f:
        rows = [ln for ln in f if ln.strip()]
    assert len(rows) - 1 >= 25, f"only {len(rows) - 1} data rows"
    r = run_cli("postformer.harness.ledger", "check",
                "--ledger", str(ledger))
    assert r.returncode == 0, r.stderr[-2000:] + r.stdout[-2000:]
