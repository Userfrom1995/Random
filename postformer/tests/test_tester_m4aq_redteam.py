"""Tester M4aq red-team: hostile live-fire on the Markov training path (Refs #294).

Novel vs all prior suites: every live training test to date uses
--data mqar (ap1 spies on batch_mqar, aj/m4* chains train mqar).
The --data markov branch (batch_markov, --seq-len) has never been
executed by any test. This suite attacks it:
  1. All six families train finite on markov at toy scale.
  2. Same-seed rerun determinism on the markov path.
  3. Cross-arm data-stream identity on the markov path (matched-budget
     invariant must hold for batch_markov, not just batch_mqar).
  4. --seq-len guard edges (<= order+0 rejected loudly).
  5. Markov checkpoint composes into the G1 eval harness.
  6. Token accounting exact on the markov path.
All runs are tiny (steps<=8, seq-len 16) so the suite stays fast on CPU.
"""
import json
import os

import torch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

FAMILIES = ["transformer", "p1", "p2", "p3", "p4", "p5"]


def _train(model, out, seed, steps=4, extra=()):
    from postformer.harness.train import main as train_main
    os.makedirs(out, exist_ok=True)
    train_main(["--model", model, "--data", "markov", "--vocab", "64",
                "--seq-len", "16", "--steps", str(steps), "--batch", "2",
                "--seed", str(seed), "--out", out,
                "--log-every", str(steps)] + list(extra))
    with open(os.path.join(out, "train_summary.json")) as f:
        return json.load(f)


def test_aq1_markov_trains_finite_all_families(tmp_path):
    """Every family must train finite loss on markov and write artifacts."""
    import math
    for fam in FAMILIES:
        out = str(tmp_path / fam)
        s = _train(f"{fam}-toy", out, seed=7, steps=4)
        assert s["data"] == "markov"
        assert math.isfinite(s["final_loss"]), (fam, s["final_loss"])
        assert os.path.exists(os.path.join(out, "checkpoint.pt"))
        assert os.path.exists(os.path.join(out, "train_curve.csv"))
        assert s["train_tokens"] == 4 * 2 * 16, s["train_tokens"]


def test_aq2_markov_same_seed_rerun_deterministic(tmp_path):
    """Same seed markov rerun must be bit-identical (loss + weights)."""
    s1 = _train("p1-toy", str(tmp_path / "a"), seed=11, steps=6)
    s2 = _train("p1-toy", str(tmp_path / "b"), seed=11, steps=6)
    assert s1["final_loss"] == s2["final_loss"]
    w1 = torch.load(os.path.join(str(tmp_path / "a"), "checkpoint.pt"),
                    map_location="cpu", weights_only=False)["state_dict"]
    w2 = torch.load(os.path.join(str(tmp_path / "b"), "checkpoint.pt"),
                    map_location="cpu", weights_only=False)["state_dict"]
    assert set(w1) == set(w2)
    for k in w1:
        assert torch.equal(w1[k].cpu(), w2[k].cpu()), k


def test_aq3_markov_cross_arm_stream_identical_init_differs(tmp_path):
    """Same seed => identical markov batches across arms, per-arm inits."""
    import postformer.harness.train as train_mod
    seen = {}
    real_batch = train_mod.batch_markov

    def spy(rng, vocab, length, batch):
        ids = real_batch(rng, vocab, length, batch)
        seen.setdefault("batches", []).append(ids.clone())
        return ids

    import _pytest.monkeypatch as _mp
    mp = _mp.MonkeyPatch()
    mp.setattr(train_mod, "batch_markov", spy)
    try:
        s1 = _train("p1-toy", str(tmp_path / "p1"), seed=21, steps=2)
        b1 = [b.tolist() for b in seen["batches"]]
        seen["batches"].clear()
        s2 = _train("transformer-toy", str(tmp_path / "tr"), seed=21,
                    steps=2)
        b2 = [b.tolist() for b in seen["batches"]]
    finally:
        mp.undo()
    assert b1 == b2, "matched-budget streams diverge on markov path"
    assert s1["final_loss"] != s2["final_loss"], \
        "per-arm inits unexpectedly identical"


def test_aq4_markov_seq_len_guard_rejects_degenerate(tmp_path):
    """--seq-len at/below the Markov order must fail loudly, not crash."""
    import pytest
    from postformer.harness.train import main as train_main
    for bad in ("3", "0", "-5"):
        with pytest.raises(SystemExit):
            train_main(["--model", "p1-toy", "--data", "markov",
                        "--vocab", "64", "--seq-len", bad, "--steps", "2",
                        "--batch", "2", "--seed", "0",
                        "--out", str(tmp_path / f"s{bad}"),
                        "--log-every", "2"])


def test_aq5_markov_checkpoint_composes_into_g1_eval(tmp_path):
    """A markov-trained checkpoint must load and score in synthetic_recall."""
    from postformer.harness.synthetic_recall import main as eval_main
    _train("p5-toy", str(tmp_path / "ckpt"), seed=5, steps=4)
    eout = str(tmp_path / "eval")
    os.makedirs(eout, exist_ok=True)
    eval_main(["--model", "p5-toy", "--checkpoint",
               os.path.join(str(tmp_path / "ckpt"), "checkpoint.pt"),
               "--vocab", "64", "--task", "mqar", "--n-pairs", "8",
               "--episodes", "2", "--seed", "5", "--out", eout])
    with open(os.path.join(eout, "g1_summary_seed5.json")) as f:
        summary = json.load(f)
    acc = summary["mqar"]["8"]["acc"]
    assert 0.0 <= acc <= 1.0, acc
    assert summary["random_init"] is False


def test_aq6_markov_tokens_accounting_exact(tmp_path):
    """train_tokens must equal steps*batch*seq_len on the markov path."""
    s = _train("p3-toy", str(tmp_path / "a"), seed=3, steps=8)
    assert s["train_tokens"] == 8 * 2 * 16
    with open(os.path.join(str(tmp_path / "a"), "train_curve.csv")) as f:
        lines = [ln for ln in f.read().splitlines() if ln.strip()]
    assert len(lines) == 3, lines  # header + step0 + final
