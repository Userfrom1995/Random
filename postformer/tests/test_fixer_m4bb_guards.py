"""Fixer M4bb hostile guards: lock the three review-mandated refusals.

Refs #294 (guard routing only, never gate results).

- slot_stride is p2-only: a --config (or checkpoint) carrying
  slot_stride for p1/p3/p4/p5/transformer must fail loudly instead of
  exiting 0 on the wrong arm (mirrors the slots/use_accumulator guards).
- enwik8 --stride == --context skips scored tokens (keep_from goes -1,
  per[-1:] keeps 1 of context-1 targets); stride >= context must refuse.
- ledger seed/vocab must be non-negative integers: '-1', '-5', '64.5'
  must fail validation instead of passing silently.
"""

import os

import pytest
import yaml


def _write_config(tmp_path, payload):
    cfg = os.path.join(str(tmp_path), "cfg.yaml")
    with open(cfg, "w") as f:
        yaml.safe_dump(payload, f)
    return cfg


def test_fixer_slot_stride_config_refused_off_p2(tmp_path):
    from postformer.harness.util import load_model
    cfg = _write_config(tmp_path, {"slot_stride": 4})
    with pytest.raises(SystemExit, match="slot_stride"):
        load_model("p1-toy", None, cfg, {}, "cpu", "fp32")


def test_fixer_slot_stride_checkpoint_refused_off_p2(tmp_path):
    import torch
    from postformer.harness.util import load_model
    ckpt = os.path.join(str(tmp_path), "stride.ckpt")
    torch.save({"state_dict": {}, "config": {"slot_stride": 4},
                "args": {}}, ckpt)
    with pytest.raises(SystemExit, match="slot_stride"):
        load_model("p1-toy", ckpt, None, {}, "cpu", "fp32")


def test_fixer_enwik8_stride_eq_context_refused(tmp_path):
    from postformer.harness.enwik8_bpb import main as bpb_main
    with pytest.raises(SystemExit, match="stride"):
        bpb_main(["--model", "p1-toy", "--out", str(tmp_path),
                  "--split", "valid", "--context", "4", "--stride", "4",
                  "--tokenizer", "byte", "--data-root", str(tmp_path),
                  "--max-windows", "1", "--seed", "0"])


def test_fixer_ledger_seed_vocab_rejected():
    from postformer.harness.ledger import SCHEMA, _validate_row

    def row(**kw):
        r = {c: "" for c in SCHEMA}
        r.update({"model": "p1-toy", "seed": "0", "vocab": "64",
                  "notes": "probe fixture"})
        r.update(kw)
        return r

    assert any("seed" in e for e in _validate_row(0, row(seed="-1")))
    assert any("vocab" in e for e in _validate_row(0, row(vocab="-5")))
    assert any("vocab" in e for e in _validate_row(0, row(vocab="64.5")))
    assert _validate_row(0, row(seed="0", vocab="64")) == []
