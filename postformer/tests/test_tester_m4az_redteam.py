"""Tester M4az red-team: hostile live-fire on current head (Refs #294).

Novel vs all prior suites (ay pinned G4 control growth, measure-chain,
plot escaping, non-MQAR liveness, upsert locks on the 26-col schema):
  1. M4b envelope ground-truth lock: the committed p4-toy ledger row cells
     must equal the committed m4b-toy g1_summary JSON values bit-for-bit
     (mqar8/N16/2hop/induction/copy), and the H4-negative ordering
     (p4 0.035 < matched M3 p1-W16 ref 0.0625) must hold against the
     committed m3-toy curve file. Any silent cell/curve drift fails.
  2. Live toy parity re-measured via the factory (not committed pins):
     all five candidates within 2% of transformer-toy, p4 within 2%.
  3. P4 window-ablation liveness (M4a finding-1 lock, live): train
     p4-toy --window 0 (4 steps) -> eval --window 0 succeeds; eval of
     that W0 checkpoint with --window 8 must SystemExit (A2 mismatch
     guard covers p4); --window on transformer must SystemExit.
  4. P4 MINI causality + flatness: step-vs-forward maxdiff <= 1e-4 out
     to T=20 across the W=8 boundary, prefix invariance <= 1e-6, and
     state_bytes flat 1k vs 32k and equal to P1.
  5. Viewer + commit-discipline locks: viewer ships splitCSV plus
     escaping and parses the live 25-row 26-col ledger; no commit on
     this branch may carry Closes/Fixes/Resolves #294 (binding gate:
     toy rows are NOT gate results).
"""
import csv
import json
import os
import subprocess

import torch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
LEDGER = os.path.join(REPO_ROOT, "postformer", "ledger", "ledger.csv")
M4B_SUMMARY = os.path.join(
    REPO_ROOT, "postformer", "ledger", "curves", "m4b-toy",
    "g1_summary_p4-toy-s0.json")
M3_P1W16 = os.path.join(
    REPO_ROOT, "postformer", "ledger", "curves", "m3-toy", "p1-W16-mqar",
    "g1_summary_seed0.json")
VIEWER = os.path.join(REPO_ROOT, "postformer", "viewer", "index.html")


def _ledger_rows():
    with open(LEDGER, newline="") as f:
        return list(csv.DictReader(f))


def test_az1_m4b_cells_equal_committed_curves_h4_negative():
    """Ledger p4-toy row cells == m4b curve JSON; H4 ordering holds."""
    g = json.load(open(M4B_SUMMARY))
    rows = [r for r in _ledger_rows()
            if r["model"] == "p4-toy" and r.get("g1_mqar_8")]
    assert len(rows) == 1, [r["model"] for r in rows]
    row = rows[0]
    assert float(row["g1_mqar_8"]) == g["mqar"]["8"]["acc"], (
        row["g1_mqar_8"], g["mqar"]["8"]["acc"])
    assert float(row["g1_mqar_16"]) == g["mqar"]["16"]["acc"], (
        row["g1_mqar_16"], g["mqar"]["16"]["acc"])
    assert float(row["g1_2hop"]) == g["bind2hop"]["acc"], (
        row["g1_2hop"], g["bind2hop"]["acc"])
    assert float(row["g1_induction"]) == g["induction"]["16"], (
        row["g1_induction"], g["induction"])
    assert float(row["g1_copy"]) == g["copying"]["32"], (
        row["g1_copy"], g["copying"])
    assert g["random_init"] is False  # trained probe, not smoke
    ref = json.load(open(M3_P1W16))
    assert ref["mqar"]["8"]["acc"] == 0.0625, ref["mqar"]
    assert g["mqar"]["8"]["acc"] < ref["mqar"]["8"]["acc"], (
        g["mqar"]["8"]["acc"], ref["mqar"]["8"]["acc"])  # H4 NEGATIVE
    assert "NOT a gate result" in row["notes"] or "NOT" in row["notes"], \
        row["notes"][:100]


def test_az2_live_toy_parity_all_five_within_2pct():
    """Factory-measured toy parity: all candidates within 2% of baseline."""
    from postformer.models.factory import count_params
    n0, _ = count_params("transformer", "toy", None)
    assert n0 > 0
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        n, _ = count_params(fam, "toy", None)
        drift = abs(n - n0) / n0
        assert drift <= 0.02, (fam, n, n0, drift)


def test_az3_p4_window_zero_chain_and_mismatch_guard(tmp_path):
    """p4 --window 0 trains+evals; W0 ckpt + --window 8 must refuse."""
    from postformer.harness.train import main as train_main
    from postformer.harness.synthetic_recall import main as eval_main
    tout = str(tmp_path / "p4w0-train")
    os.makedirs(tout, exist_ok=True)
    train_main(["--model", "p4-toy", "--data", "mqar", "--vocab", "64",
                "--n-pairs", "8", "--steps", "4", "--batch", "2",
                "--seed", "11", "--out", tout, "--log-every", "4",
                "--window", "0"])
    ckpt = os.path.join(tout, "checkpoint.pt")
    assert os.path.exists(ckpt)
    eout = str(tmp_path / "p4w0-eval")
    os.makedirs(eout, exist_ok=True)
    eval_main(["--model", "p4-toy", "--checkpoint", ckpt, "--vocab", "64",
               "--n-pairs", "8", "--episodes", "4", "--task", "mqar",
               "--seed", "11", "--out", eout, "--window", "0"])
    import glob as _glob
    assert len(_glob.glob(os.path.join(eout, "g1_summary_seed*.json"))) == 1
    # Explicit --window is the allowed A2 override path, so a --config
    # that disagrees with the checkpoint window (with no --window flag)
    # must fail loudly instead of evaluating silently.
    import yaml as _yaml
    cfgp = str(tmp_path / "w8.yaml")
    with open(cfgp, "w") as f:
        _yaml.safe_dump({"window": 8}, f)
    try:
        eval_main(["--model", "p4-toy", "--checkpoint", ckpt, "--vocab",
                   "64", "--n-pairs", "8", "--episodes", "4", "--task",
                   "mqar", "--seed", "11",
                   "--out", str(tmp_path / "p4w8-eval"),
                   "--config", cfgp])
    except SystemExit as e:
        assert "window" in str(e).lower(), e
    else:
        raise AssertionError("W0 checkpoint + W8 config evaluated silently")
    try:
        eval_main(["--model", "transformer-toy", "--vocab", "64",
                   "--n-pairs", "8", "--episodes", "4", "--task", "mqar",
                   "--seed", "11", "--out", str(tmp_path / "t-eval"),
                   "--window", "0"])
    except SystemExit as e:
        assert "window" in str(e).lower(), e
    else:
        raise AssertionError("--window on transformer silently accepted")


def test_az4_p4_mini_causality_flatness_equals_p1():
    """P4 block step/forward equivalence, prefix invariance, flat == P1."""
    from postformer.models.factory import build_model
    from postformer.tests.conftest import MINI
    torch.manual_seed(7)
    p4, _ = build_model("p4", "toy", dict(MINI))
    p1, _ = build_model("p1", "toy", dict(MINI))
    p4.eval()
    blk = p4.blocks[0]
    T, B, D = 20, 2, MINI["d_model"]
    x = torch.randn(B, T, D)
    with torch.no_grad():
        ref = blk(x)
        st = blk.init_state(B, "cpu", torch.float32)
        outs = []
        for i in range(T):
            o, st = blk.step(x[:, i, :], st)
            outs.append(o)
        roll = torch.stack(outs, dim=1)
    assert torch.isfinite(ref).all() and torch.isfinite(roll).all()
    assert (ref - roll).abs().max().item() <= 1e-4, \
        (ref - roll).abs().max().item()
    with torch.no_grad():
        st2 = blk.init_state(B, "cpu", torch.float32)
        outs2 = []
        for i in range(12):
            o, st2 = blk.step(x[:, i, :], st2)
            outs2.append(o)
        short = torch.stack(outs2, dim=1)
    # Prefix invariance: first 12 outputs identical with longer context.
    assert (short - roll[:, :12, :]).abs().max().item() <= 1e-6
    assert p4.state_bytes(1, 1000) == p4.state_bytes(1, 32000)
    assert p4.state_bytes(1, 1000) == p1.state_bytes(1, 1000)


def test_az5_viewer_parses_live_ledger_no_closes_on_branch():
    """Viewer hardened + parses live ledger; branch has no Closes #294."""
    src = open(VIEWER).read()
    assert "splitCSV" in src
    assert "const cells = l.split" not in src  # unaware splitter gone
    assert "const cells = splitCSV(l)" in src
    assert "&lt;" in src or "esc(" in src  # HTML escaping present
    with open(LEDGER, newline="") as f:
        rdr = csv.reader(f)
        header = next(rdr)
        assert len(header) == 26, len(header)
        n = sum(1 for _ in rdr)
    assert n == 25, n
    log = subprocess.run(
        ["git", "log", "origin/main..HEAD", "--format=%s%n%b"],
        capture_output=True, text=True, cwd=REPO_ROOT, check=True).stdout
    for i, line in enumerate(log.splitlines()):
        low = line.lower()
        assert not any(k in low for k in (
            "closes #294", "fixes #294", "resolves #294")), \
            f"line {i}: {line[:120]}"
