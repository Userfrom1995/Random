"""Tester M4ak red-team: guard live-fire + full-model determinism (Refs #294).

Novel vs prior suites (M4aj did the happy-path E2E chain): this suite
live-fires the REJECTION paths and full-model properties as a hostile
consumer would:
  1. train CLI must loudly reject degenerate args (steps/batch/window),
  2. eval CLI must loudly reject checkpoint vocab mismatch,
  3. the M2 window-ablation guard must fire live (train W0, eval W16 fails,
     eval W0 passes),
  4. full-model (not just block) forward is finite + bit-identical reruns,
  5. eval summaries are deterministic for a fixed seed,
  6. ledger append dedups on the full key and --force upserts,
  7. P2 slots=0 vs slots=4 state inventories discriminate honestly.
"""
import json
import subprocess
import sys
from pathlib import Path

import torch

REPO = Path(__file__).resolve().parents[2]
FAMS = ["transformer", "p1", "p2", "p3", "p4", "p5"]


def run_cli(*args, timeout=600):
    return subprocess.run(
        [sys.executable, "-m"] + list(args),
        capture_output=True, text=True, timeout=timeout, cwd=str(REPO),
    )


def test_ak1_train_rejects_zero_steps():
    """steps=0 must fail loudly, never silently produce an empty curve."""
    r = run_cli("postformer.harness.train", "--model", "p1-toy",
                "--data", "mqar", "--vocab", "64", "--steps", "0",
                "--batch", "2", "--seed", "0", "--out", "/tmp/ak-reject-steps")
    assert r.returncode != 0, "steps=0 must not pass"


def test_ak2_train_rejects_zero_batch_and_negative_window():
    """batch=0 and window=-1 must both fail loudly."""
    r = run_cli("postformer.harness.train", "--model", "p1-toy",
                "--data", "mqar", "--vocab", "64", "--steps", "4",
                "--batch", "0", "--seed", "0", "--out", "/tmp/ak-reject-batch")
    assert r.returncode != 0, "batch=0 must not pass"
    r2 = run_cli("postformer.harness.train", "--model", "p1-toy",
                 "--data", "mqar", "--vocab", "64", "--steps", "4",
                 "--batch", "2", "--window", "-1", "--seed", "0",
                 "--out", "/tmp/ak-reject-window")
    assert r2.returncode != 0, "window=-1 must not pass"


def test_ak3_eval_rejects_vocab_mismatch(tmp_path):
    """Checkpoint trained at vocab 64 must refuse eval at vocab 65."""
    out = tmp_path / "t"
    r = run_cli("postformer.harness.train", "--model", "p1-toy",
                "--data", "mqar", "--vocab", "64", "--steps", "4",
                "--batch", "2", "--seed", "3", "--out", str(out))
    assert r.returncode == 0, r.stderr[-2000:]
    ckpts = list(out.glob("*.pt"))
    assert ckpts, "train produced no checkpoint"
    bad = run_cli("postformer.harness.synthetic_recall", "--model", "p1-toy",
                  "--checkpoint", str(ckpts[0]), "--task", "mqar",
                  "--vocab", "65", "--n-pairs", "8", "--episodes", "5",
                  "--seed", "3", "--out", str(tmp_path / "e-bad"))
    assert bad.returncode != 0, "vocab-mismatched eval must fail loudly"


def test_ak4_window_ablation_guard_live(tmp_path):
    """W0 checkpoint inherits W0 when no --window is passed (the M2 fix);
    a --config file disagreeing with the checkpoint fails loudly; an
    explicit --window remains the sanctioned deliberate-override path."""
    import yaml
    out = tmp_path / "t"
    r = run_cli("postformer.harness.train", "--model", "p1-toy",
                "--data", "mqar", "--vocab", "64", "--window", "0",
                "--steps", "4", "--batch", "2", "--seed", "5",
                "--out", str(out))
    assert r.returncode == 0, r.stderr[-2000:]
    ckpts = list(out.glob("*.pt"))
    assert ckpts, "train produced no checkpoint"
    # 1. No --window flag: must inherit the checkpoint's W0, not silent W16.
    e_inherit = tmp_path / "e-inherit"
    r_inherit = run_cli("postformer.harness.synthetic_recall",
                        "--model", "p1-toy",
                        "--checkpoint", str(ckpts[0]), "--task", "mqar",
                        "--vocab", "64", "--n-pairs", "8",
                        "--episodes", "5", "--seed", "5",
                        "--out", str(e_inherit))
    assert r_inherit.returncode == 0, r_inherit.stderr[-2000:]
    summ = json.loads(next(e_inherit.glob("g1_summary*.json")).read_text())
    assert summ["config"]["window"] == 0, summ["config"]
    # 2. --config file with a conflicting window and no override: loud fail.
    cfg = tmp_path / "bad-window.yaml"
    cfg.write_text(yaml.safe_dump({"window": 16}))
    r_cfg = run_cli("postformer.harness.synthetic_recall",
                    "--model", "p1-toy", "--checkpoint", str(ckpts[0]),
                    "--config", str(cfg), "--task", "mqar",
                    "--vocab", "64", "--n-pairs", "8",
                    "--episodes", "5", "--seed", "5",
                    "--out", str(tmp_path / "e-cfg"))
    assert r_cfg.returncode != 0, "--config window mismatch must fail loudly"
    # 3. Explicit --window override is the sanctioned deliberate path: passes.
    r_exp = run_cli("postformer.harness.synthetic_recall",
                    "--model", "p1-toy", "--checkpoint", str(ckpts[0]),
                    "--task", "mqar", "--vocab", "64", "--window", "0",
                    "--n-pairs", "8", "--episodes", "5", "--seed", "5",
                    "--out", str(tmp_path / "e-explicit"))
    assert r_exp.returncode == 0, r_exp.stderr[-2000:]
    summ_exp = json.loads(next((tmp_path / "e-explicit").glob("g1_summary*.json")).read_text())
    assert summ_exp["config"]["window"] == 0, summ_exp["config"]


def test_ak5_full_model_forward_finite_and_deterministic():
    """Full-model token-id forward is finite and bit-identical across reruns."""
    sys.path.insert(0, str(REPO))
    from postformer.models.factory import build_model
    from postformer.models.common import seed_all
    from postformer.tests.conftest import MINI
    for fam in FAMS:
        outs = []
        for _ in range(2):
            seed_all(409, "tester-m4ak-fullmodel")
            m, _ = build_model(fam, "tiny", dict(MINI))
            m.eval()
            with torch.no_grad():
                ids = torch.randint(0, MINI["vocab_size"], (2, 12))
                outs.append(m(ids))
        for o in outs:
            assert torch.isfinite(o).all(), fam
        assert torch.equal(outs[0], outs[1]), f"{fam} rerun mismatch"


def test_ak6_eval_determinism_same_seed(tmp_path):
    """Same eval seed twice yields identical summary scores (no hidden RNG)."""
    sys.path.insert(0, str(REPO))
    scores = []
    for i in range(2):
        eout = tmp_path / f"e{i}"
        r = run_cli("postformer.harness.synthetic_recall", "--model", "p5-toy",
                    "--task", "mqar", "--vocab", "64", "--n-pairs", "8",
                    "--episodes", "10", "--seed", "9",
                    "--out", str(eout))
        assert r.returncode == 0, r.stderr[-2000:]
        cands = list(eout.glob("g1_summary*.json"))
        assert cands, "eval produced no summary"
        scores.append(json.loads(cands[0].read_text()))
    assert scores[0] == scores[1], "eval must be deterministic per seed"


def test_ak7_ledger_append_dedup_and_force_upsert(tmp_path):
    """Second append of the same key fails; --force upserts exactly one row."""
    led = tmp_path / "ledger.csv"
    led.write_text(
        "model,params,train_tokens,seed,vocab,window,slots,use_accumulator,"
        "g1_mqar_8,g1_mqar_16,g1_mqar_64,g1_mqar_256,g1_induction,g1_copy,"
        "g1_2hop,g2_bpb_1x,g2_bpb_4x,g2_bpb_8x,g2_delta_4x,g2_delta_8x,"
        "g3_valid_bpb,g3_test_bpb,g4_state_bytes,g4_ms_per_token,gpu_hours,notes\n")
    run = {"model": "p1-toy", "params": "336332", "train_tokens": "528000",
           "seed": "0", "vocab": "64", "window": "16", "slots": "",
           "use_accumulator": "", "g1_mqar_8": "0.06",
           "notes": "probe: dedup hostile fixture"}
    rj = tmp_path / "run.json"
    rj.write_text(json.dumps(run))
    r1 = run_cli("postformer.harness.ledger", "append",
                 "--run-json", str(rj), "--ledger", str(led))
    assert r1.returncode == 0, r1.stderr[-2000:] + r1.stdout[-2000:]
    r2 = run_cli("postformer.harness.ledger", "append",
                 "--run-json", str(rj), "--ledger", str(led))
    assert r2.returncode != 0, "bare duplicate append must fail loudly"
    run["g1_mqar_8"] = "0.07"
    rj.write_text(json.dumps(run))
    r3 = run_cli("postformer.harness.ledger", "append", "--force",
                 "--run-json", str(rj), "--ledger", str(led))
    assert r3.returncode == 0, r3.stderr[-2000:] + r3.stdout[-2000:]
    r4 = run_cli("postformer.harness.ledger", "check", "--ledger", str(led))
    assert r4.returncode == 0, r4.stderr[-2000:] + r4.stdout[-2000:]


def test_ak8_p2_slots_control_discriminates():
    """slots=0 vs slots=4 state bytes differ; slots=0 is the pure-SSD control."""
    sys.path.insert(0, str(REPO))
    from postformer.models.factory import build_model
    from postformer.tests.conftest import MINI
    cfg0 = dict(MINI)
    cfg0["slots"] = 0
    m0, _ = build_model("p2", "tiny", cfg0)
    m4, _ = build_model("p2", "tiny", dict(MINI))
    b0 = m0.state_bytes(1, length=8000)
    b4 = m4.state_bytes(1, length=8000)
    assert b4 > b0 > 0, (b0, b4)
    # Flatness still holds for both (G4-tier property, not pinned value).
    assert m0.state_bytes(1, length=1000) == b0
    assert m4.state_bytes(1, length=1000) == b4
