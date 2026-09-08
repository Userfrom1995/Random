"""Tester M4af hostile suite: ledger drift/numericity locks, harness determinism,
G3 byte-path roundtrip, and length_sweep +2 success path.

Refs #294 (toy/mini-scale proxies and seeded fixtures only, never gate results).

Why this suite exists: at head 595f5075 the suite count stood at 313 passed
with near-total coverage, but five hostile gaps remained unpinned:

- AF1 (disagreeing baselines): ledger.py:224 fails loudly when two
  transformer rows at one (scale, vocab) disagree on params, but no test
  pinned it; a silent-skip regression would let a corrupted baseline pass.
- AF2 (per-row numericity): _validate_row enforces numeric seed/vocab/
  train_tokens/gpu_hours plus integer window/slots >= 0, unpinned at
  check-time; a dead-branch regression would admit garbage rows.
- AF3 (G1 rerun determinism): matched-budget claims rest on identical
  (seed, data) streams, but no harness-level test re-ran one checkpoint
  twice to prove byte-identical summaries.
- AF4 (G3 byte path): only the missing-data refusal was pinned (u9); the
  positive byte-scoring path on a seeded fixture was never executed.
- AF5 (length_sweep +2 success): Z4 pinned the --vocab floor refusal, but
  the explicit---vocab success roundtrip against a real checkpoint
  (the M4ac fixer path) was never executed.
"""

import csv
import hashlib
import json
import os

import pytest
import torch

from postformer.harness.ledger import SCHEMA, main as ledger_main

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _write(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA)
        w.writeheader()
        w.writerows(rows)


def _row(model="p1-toy", params="336332", seed="0", vocab="64", window="16",
         slots="", use_accumulator="", train_tokens="528000",
         gate="g1_mqar_8", gateval="0.06",
         notes="m4af probe Refs #294"):
    r = {c: "" for c in SCHEMA}
    r.update({"model": model, "params": params, "train_tokens": train_tokens,
              "seed": seed, "vocab": vocab, "window": window,
              "slots": slots, "use_accumulator": use_accumulator,
              "gpu_hours": "0", "notes": notes})
    r[gate] = gateval
    return r


def test_af1_disagreeing_transformer_baselines_fail_loudly(tmp_path, capsys):
    """Two transformer-toy params at one vocab must fail, never silently win."""
    p = str(tmp_path / "ledger.csv")
    _write(p, [
        _row(model="transformer-toy", params="336768", window="",
             notes="m4af baseline A Refs #294"),
        _row(model="transformer-toy", params="336769", window="",
             notes="m4af baseline B Refs #294"),
    ])
    with pytest.raises(SystemExit):
        ledger_main(["check", "--ledger", p])
    out = capsys.readouterr().out
    assert "disagree" in out, out[-500:]


def test_af2_non_numeric_and_negative_cells_fail_loudly(tmp_path, capsys):
    """seed/vocab numericity plus window/slots integer>=0 guards must fire."""
    cases = [
        ({"seed": "abc"}, "seed"),
        ({"vocab": "64x"}, "vocab"),
        ({"train_tokens": "many"}, "train_tokens"),
        ({"window": "-1"}, "window"),
        ({"window": "1.5"}, "window"),
        ({"slots": "-4"}, "slots"),
        ({"slots": "1.5"}, "slots"),
    ]
    for override, col in cases:
        p = str(tmp_path / "ledger.csv")
        bad = _row(**{**{"model": "p1-toy"}, **override})
        _write(p, [bad])
        with pytest.raises(SystemExit):
            ledger_main(["check", "--ledger", p])
        out = capsys.readouterr().out
        assert col in out, (override, out[-300:])


def _train_tiny_ckpt(model, outdir, steps, vocab="64"):
    from postformer.harness.train import main as train_main
    os.makedirs(outdir, exist_ok=True)
    train_main(["--model", model, "--data", "mqar", "--vocab", vocab,
                "--steps", str(steps), "--batch", "4",
                "--out", outdir, "--log-every", "3", "--seed", "0"])
    ckpt = os.path.join(outdir, "checkpoint.pt")
    assert os.path.isfile(ckpt)
    return ckpt


def test_af3_g1_eval_rerun_is_byte_identical(tmp_path):
    """Same checkpoint + same eval seed twice must give identical summaries."""
    from postformer.harness.synthetic_recall import main as recall_main
    ckpt = _train_tiny_ckpt("p1-toy", str(tmp_path / "tr"), 4)
    blobs = []
    for run in ("a", "b"):
        ev = str(tmp_path / f"ev{run}")
        os.makedirs(ev, exist_ok=True)
        recall_main(["--model", "p1-toy", "--checkpoint", ckpt,
                     "--vocab", "64", "--n-pairs", "8", "--task", "mqar",
                     "--episodes", "4", "--out", ev, "--seed", "0"])
        with open(os.path.join(ev, "g1_summary_seed0.json")) as f:
            blobs.append(json.load(f))
    for b in blobs:
        b.pop("env", None)
    assert blobs[0] == blobs[1]
    assert blobs[0]["mqar"]["8"]["acc"] is not None
    assert blobs[0]["random_init"] is False


def test_af4_enwik8_byte_path_scores_seeded_fixture(tmp_path):
    """G3 byte harness must score a seeded fixture end to end (NOT Enwik8,
    NOT a gate result: random-init toy model, 2KB fixture, 2 windows)."""
    from postformer.harness.enwik8_bpb import main as bpb_main
    rng = torch.Generator().manual_seed(20260908)
    raw = torch.randint(0, 256, (2048,), generator=rng).tolist()
    data_root = str(tmp_path / "data")
    os.makedirs(data_root, exist_ok=True)
    with open(os.path.join(data_root, "enwik8"), "wb") as f:
        f.write(bytes(raw))
    digest = hashlib.sha256(bytes(raw)).hexdigest()
    out = str(tmp_path / "g3")
    os.makedirs(out, exist_ok=True)
    bpb_main(["--model", "p1-toy", "--out", out, "--split", "valid",
              "--context", "32", "--stride", "32", "--tokenizer", "byte",
              "--data-root", data_root, "--max-windows", "2", "--seed", "0"])
    with open(os.path.join(out, "g3_summary_seed0.json")) as f:
        blob = json.load(f)
    (row,) = blob["rows"]
    assert row["sha256_data"] == digest
    assert row["tokenizer"] == "byte" and row["random_init"] is True
    assert 0.0 < row["bpb"] < 16.0, row["bpb"]
    # At most max_windows x stride new tokens can be scored; the harness
    # counts only stride-new tokens per window after warmup (32 observed).
    assert 0 < row["n_bytes"] <= 64, row["n_bytes"]


def test_af5_length_sweep_explicit_vocab_success_roundtrip(tmp_path):
    """Explicit --vocab matching the checkpoint train vocab must compose
    (the M4ac fixer path); mismatched values must still refuse loudly."""
    from postformer.harness.length_sweep import main as sweep_main
    ckpt = _train_tiny_ckpt("p1-toy", str(tmp_path / "tr"), 2, vocab="16")
    out = str(tmp_path / "g2")
    os.makedirs(out, exist_ok=True)
    sweep_main(["--model", "p1-toy", "--checkpoint", ckpt, "--vocab", "16",
                "--t-train", "33", "--lengths", "33,66", "--split", "synthetic",
                "--out", out, "--seed", "0"])
    with open(os.path.join(out, "g2_summary_seed0.json")) as f:
        blob = json.load(f)
    assert blob["lengths"] == [33, 66], blob["lengths"]
    with open(os.path.join(out, "g2_curve_seed0.csv")) as f:
        rows = list(csv.DictReader(f))
    # The sweep always scores the transformer baseline arm too (random-init
    # here, honestly flagged); both arms cover both lengths.
    assert sorted(r["model"] for r in rows) == sorted(
        ["p1-toy", "p1-toy", "transformer-toy", "transformer-toy"])
    assert sorted(int(r["length"]) for r in rows) == [33, 33, 66, 66]
    assert all(float(r["bpb"]) > 0 for r in rows)
    base = [r for r in rows if r["model"] == "transformer-toy"]
    assert all(r["random_init"] == "True" for r in base), base
    out2 = str(tmp_path / "g2bad")
    os.makedirs(out2, exist_ok=True)
    with pytest.raises(SystemExit):
        sweep_main(["--model", "p1-toy", "--checkpoint", ckpt, "--vocab", "64",
                    "--t-train", "33", "--lengths", "33", "--split", "synthetic",
                    "--out", out2, "--seed", "0"])
