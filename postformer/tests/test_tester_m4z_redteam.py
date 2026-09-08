"""Tester M4z hostile suite: +2 vocab-convention, n==vocab, norm-dedup pins.

Refs #294 (toy/analytic checks only, never gate results).

Why this suite exists: the fixer delta after M4y (latency_state /
length_sweep --vocab train-+2 convention with >=16 guard, train
--n-pairs <= --vocab boundary, ledger _norm key/drift grouping) changed
live CLI contracts. Unpinned, a future edit could silently revert to the
raw-vocab_size convention (checkpoint OOB class) or re-tighten the
n-pairs guard (breaking the n==vocab full-key replay). This suite pins:

- Z1 (n==vocab boundary live): train with --n-pairs == --vocab runs to
  a checkpoint (full key set sampled without replacement is valid);
  --n-pairs == --vocab+1 refuses loudly with the n-pairs message.
- Z2 (latency_state vocab floor): --vocab 8 refuses (>= 16); --vocab 16
  runs and writes a curve file.
- Z3 (latency_state +2 roundtrip): a checkpoint trained at --vocab V
  (vocab_size V+2) composes with eval --vocab V, and eval --vocab V+2
  refuses loudly naming vocab_size (no silent partial-load / OOB).
- Z4 (length_sweep vocab floor): --vocab 8 refuses (>= 16) before any run.
- Z5 (ledger norm dedup): _key collides on whitespace-padded vocab, so a
  padded dupe is a dupe; a >2% drifter at a normalized (scale, vocab)
  still fails check loudly on param drift.
- Z6 (shipped ledger green): check passes on the 25-row shipped ledger.
"""

import csv
import json
import pathlib

import pytest
import torch

from postformer.harness import ledger as _ledger
from postformer.harness import latency_state as _lat
from postformer.harness import length_sweep as _sweep
from postformer.harness import train as _train

_HERE = pathlib.Path(__file__).resolve()
_POSTFORMER = _HERE.parents[1]
_SHIPPED = _POSTFORMER / "ledger" / "ledger.csv"


@pytest.fixture(scope="module")
def ckpt_vocab16(tmp_path_factory):
    """2-step p1-toy MQAR checkpoint at train --vocab 16, n==vocab replay."""
    out = tmp_path_factory.mktemp("m4z") / "ckpt16"
    _train.main(["--model", "p1-toy", "--data", "mqar",
                 "--vocab", "16", "--n-pairs", "16",
                 "--steps", "2", "--batch", "2",
                 "--out", str(out), "--seed", "0"])
    blob = torch.load(out / "checkpoint.pt", map_location="cpu",
                      weights_only=False)
    assert int(blob["config"]["vocab_size"]) == 18, \
        f"train --vocab 16 must build vocab_size 18, got {blob['config']['vocab_size']}"
    return out / "checkpoint.pt"


def test_z1_n_equals_vocab_trains_and_plus_one_refuses(tmp_path, ckpt_vocab16):
    """Z1: n==vocab is a valid full-key replay; n==vocab+1 refuses loudly."""
    assert ckpt_vocab16.exists()
    with pytest.raises(SystemExit, match="n-pairs"):
        _train.main(["--model", "p1-toy", "--data", "mqar",
                     "--vocab", "16", "--n-pairs", "17",
                     "--steps", "2", "--batch", "2",
                     "--out", str(tmp_path / "refuse"), "--seed", "0"])


def test_z2_latency_state_vocab_floor(tmp_path):
    """Z2: --vocab below 16 refuses; --vocab 16 runs and writes a curve."""
    with pytest.raises(SystemExit, match=">= 16"):
        _lat.main(["--model", "p1-toy", "--vocab", "8",
                   "--lengths", "64", "--out", str(tmp_path / "lat8")])
    ok = tmp_path / "lat16"
    _lat.main(["--model", "p1-toy", "--vocab", "16",
               "--lengths", "64", "--out", str(ok)])
    assert (ok / "g4_curve_seed0.csv").exists()


def test_z3_latency_state_plus_two_checkpoint_roundtrip(tmp_path, ckpt_vocab16):
    """Z3: eval --vocab V composes with a V-trained ckpt; V+2 refuses."""
    match_dir = tmp_path / "latmatch"
    _lat.main(["--model", "p1-toy", "--checkpoint", str(ckpt_vocab16),
               "--vocab", "16", "--lengths", "64",
               "--out", str(match_dir)])
    assert (match_dir / "g4_curve_seed0.csv").exists()
    with pytest.raises(SystemExit, match="vocab_size"):
        _lat.main(["--model", "p1-toy", "--checkpoint", str(ckpt_vocab16),
                   "--vocab", "18", "--lengths", "64",
                   "--out", str(tmp_path / "latmismatch")])


def test_z4_length_sweep_vocab_floor(tmp_path):
    """Z4: length_sweep --vocab below 16 refuses before any run."""
    with pytest.raises(SystemExit, match=">= 16"):
        _sweep.main(["--model", "p1-toy", "--vocab", "8",
                     "--lengths", "64", "--t-train", "64",
                     "--out", str(tmp_path / "ls8")])


def _empty_row(scale, model, params, vocab, note):
    row = {c: "" for c in _ledger.SCHEMA}
    row.update({"model": model, "params": str(params), "seed": "0",
                "vocab": vocab, "train_tokens": "100",
                "g1_mqar_8": "0.05",
                "notes": note + " Refs #294 probe"})
    return row


def test_z5_norm_dedup_and_grouped_drift(tmp_path, capsys):
    """Z5: padded vocab keys collide; normalized-group drift still fails."""
    padded = {"model": "p1-toy", "seed": "0", "vocab": " 64 ",
              "window": "", "slots": "", "use_accumulator": ""}
    plain = {"model": "p1-toy", "seed": "0", "vocab": "64",
             "window": "", "slots": "", "use_accumulator": ""}
    assert _ledger._key(padded) == _ledger._key(plain)
    assert _ledger._norm(" 64 ") == _ledger._norm(64) == "64"
    drift_path = tmp_path / "drift.csv"
    with open(drift_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=_ledger.SCHEMA)
        w.writeheader()
        w.writerow(_empty_row("toy", "transformer-toy", 336768, "64",
                              "baseline probe"))
        # 10% drift at the same normalized (toy, 64) with padded vocab.
        w.writerow(_empty_row("toy", "p1-toy", 370000, " 64 ",
                              "drifter probe"))
    with pytest.raises(SystemExit):
        _ledger.cmd_check(type("A", (), {"ledger": str(drift_path)})())
    assert "param drift" in capsys.readouterr().out


def test_z6_shipped_ledger_check_green(capsys):
    """Z6: the shipped 25-row ledger passes check after the norm delta."""
    assert _SHIPPED.exists()
    _ledger.cmd_check(type("A", (), {"ledger": str(_SHIPPED)})())
    out = capsys.readouterr().out
    assert "ledger OK" in out and "25 rows" in out
