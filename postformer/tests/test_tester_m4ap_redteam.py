"""Tester M4ap red-team: hostile live-fire on current head (Refs #294).

Novel vs prior suites (ao covered p2 determinism + A2 chain; aj3 covered
p5 determinism; af3 covered eval rerun identity; s1-s3 pinned m2/m3/a4
curve ground truth): this suite attacks the paths no prior suite runs live:
  1. Cross-arm data-stream identity (the M2 finding-1 matched-budget fix):
     p1-toy and transformer-toy at one seed must consume byte-identical
     training batches (recorded via monkeypatched batch_mqar), while their
     inits stay per-arm (final losses differ).
  2. p3 same-seed rerun determinism (accumulator + rescale-guard path;
     ao1 pinned p2 only, aj3 pinned p5 only).
  3. p4 same-seed rerun determinism (surprise-gated write path).
  4. Committed-curve integrity sweep: EVERY g1_summary*.json under
     postformer/ledger/curves must parse with finite acc in [0,1]
     (no prior suite walks the whole tree).
  5. A2 flag liveness: p1-toy --window 0 must train to a DIFFERENT
     trajectory than the default window (a silently-ignored --window
     would be the M2 silent-invalidation class all over again).
"""
import glob
import json
import os

import torch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
CURVES = os.path.join(REPO_ROOT, "postformer", "ledger", "curves")


def _train(model, out, seed, steps=4, extra=()):
    from postformer.harness.train import main as train_main
    os.makedirs(out, exist_ok=True)
    train_main(["--model", model, "--data", "mqar", "--vocab", "64",
                "--n-pairs", "8", "--steps", str(steps), "--batch", "2",
                "--seed", str(seed), "--out", out,
                "--log-every", str(steps)] + list(extra))
    with open(os.path.join(out, "train_summary.json")) as f:
        return json.load(f)


def test_ap1_cross_arm_data_stream_identical_init_differs(tmp_path):
    """Same seed => identical batches across arms, per-arm inits."""
    import postformer.harness.train as train_mod
    seen = {}
    real_batch = train_mod.batch_mqar

    def spy(rng, vocab, n_pairs, batch):
        ids = real_batch(rng, vocab, n_pairs, batch)
        seen.setdefault("batches", []).append(ids.clone())
        return ids

    import _pytest.monkeypatch as _mp
    mp = _mp.MonkeyPatch()
    mp.setattr(train_mod, "batch_mqar", spy)
    try:
        s1 = _train("p1-toy", str(tmp_path / "p1"), seed=21, steps=1)
        b1 = [b.tolist() for b in seen["batches"]]
        seen["batches"].clear()
        s2 = _train("transformer-toy", str(tmp_path / "tr"), seed=21,
                    steps=1)
        b2 = [b.tolist() for b in seen["batches"]]
    finally:
        mp.undo()
    assert b1 == b2, "arms at one seed saw different data streams"
    assert len(b1) == 1 and len(b1[0]) == 2, b1
    assert s1["final_loss"] != s2["final_loss"], \
        "identical loss across families suggests shared init (must differ)"
    assert s1["train_tokens"] == s2["train_tokens"] == 2 * (4 * 8 + 1), \
        (s1["train_tokens"], s2["train_tokens"])


def test_ap2_p3_same_seed_rerun_deterministic(tmp_path):
    """p3 accumulator path: same (model, seed) twice -> identical loss."""
    losses = [_train("p3-toy", str(tmp_path / f"r{i}"), seed=22)["final_loss"]
              for i in range(2)]
    assert losses[0] == losses[1], losses
    assert all(torch.isfinite(torch.tensor(v)) for v in losses), losses


def test_ap3_p4_same_seed_rerun_deterministic(tmp_path):
    """p4 surprise path: same (model, seed) twice -> identical loss."""
    losses = [_train("p4-toy", str(tmp_path / f"r{i}"), seed=23)["final_loss"]
              for i in range(2)]
    assert losses[0] == losses[1], losses
    assert all(torch.isfinite(torch.tensor(v)) for v in losses), losses


def test_ap4_all_committed_g1_summaries_finite_and_bounded():
    """Every committed g1_summary JSON must hold finite acc in [0,1]."""
    files = glob.glob(os.path.join(CURVES, "**", "g1_summary*.json"),
                      recursive=True)
    assert len(files) >= 20, f"only {len(files)} g1 summaries committed"
    bad = []
    for fp in files:
        try:
            blob = json.load(open(fp))
        except Exception as e:  # noqa: BLE001 - collected, not raised
            bad.append((fp, f"unparseable: {e}"))
            continue
        for section in ("mqar", "induction", "copying", "bind2hop"):
            node = blob.get(section)
            if node is None:
                continue
            accs = []
            if isinstance(node, dict) and "acc" in node:
                accs.append((section, node["acc"]))
            elif isinstance(node, dict):
                for k, v in node.items():
                    if isinstance(v, dict) and "acc" in v:
                        accs.append((f"{section}[{k}]", v["acc"]))
            for name, acc in accs:
                if acc is None:
                    continue
                if not isinstance(acc, (int, float)) or not torch.isfinite(
                        torch.tensor(float(acc))) or not 0.0 <= acc <= 1.0:
                    bad.append((fp, f"{name}={acc!r}"))
    assert not bad, f"{len(bad)} corrupt g1 cells: {bad[:5]}"


def test_ap5_window_zero_changes_p1_trajectory(tmp_path):
    """--window 0 must change p1 dynamics (flag is live, not ignored)."""
    base = _train("p1-toy", str(tmp_path / "wdef"), seed=24, steps=2)
    w0 = _train("p1-toy", str(tmp_path / "w0"), seed=24, steps=2,
                extra=("--window", "0"))
    assert base["final_loss"] != w0["final_loss"], \
        (base["final_loss"], w0["final_loss"])
