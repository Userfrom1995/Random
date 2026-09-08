"""Tester M4i red-team: hostile regression for the M4h-fixer hardening batch.

Refs #294 (toy probes only, never gate results). Fixer commits 9e44b7f4 /
22506c07 / 2e712a0e hardened the ledger drift gate, the train ablation
routing, and the harness family parsing. Two regressions slipped through and
currently keep the suite red (4 failed, 114 passed at bcf769e3):

R1 - ledger "no transformer baseline" false failure (ledger.py:147-153):
  a temp ledger holding a single candidate row (the normal first-append
  state of incremental ledger building) now fails `check` with
  "no transformer baseline; cannot verify +-2% param parity". Same for a
  cross-vocab probe arm at a vocab with no baseline. The drift gate must
  only compare arms that share (scale, vocab) AND have a baseline present;
  a group with no baseline has nothing to compare, so it must be skipped,
  not failed. Breaks test_ledger.py x3 + test_tester_m4f_redteam.py x1.

R2 - suffixed-arm guard misroute (train.py:160, synthetic_recall.py:154):
  family is parsed with rsplit("-", 1)[0], so ledger-labelled arms such as
  p2-G0-toy yield family "p2-G0" and their own valid ablation flags are
  falsely rejected (`--slots applies to p2 arms only`,
  `--window applies to p1/p2/p3/p4/p5 arms only`). The factory parses
  family with split("-", 1)[0] ("p2" - correct); the harness guards must
  use the same parse. Verified live: train + synthetic_recall both
  misroute on p2-G0-toy.

All tests below are self-contained (tmp dirs only, never the live ledger)
and fast (1-step toy train, 4-episode random-init recall). If any fail,
the defects above are still present - hand back to the Fixer.
"""

import csv
import json
import os

from postformer.harness.ledger import SCHEMA, main as ledger_main


def _write(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA)
        w.writeheader()
        w.writerows(rows)


def _row(model="p1-toy", params="336332", seed="0", vocab="64", window="16",
          gate="g1_mqar_8", gateval="0.06", notes="m4i probe Refs #294"):
    r = {c: "" for c in SCHEMA}
    r.update({"model": model, "params": params, "train_tokens": "528000",
              "seed": seed, "vocab": vocab, "window": window,
              "gpu_hours": "0", "notes": notes})
    r[gate] = gateval
    return r


def _baseline(vocab="64"):
    r = _row(model="transformer-toy", params="336768", window="",
             notes="m4i baseline Refs #294")
    r["vocab"] = vocab
    return r


def test_m4i_single_candidate_tmp_ledger_passes_check(tmp_path):
    """R1: one candidate row, no baseline yet - nothing to compare, must pass."""
    p = str(tmp_path / "ledger.csv")
    _write(p, [_row()])
    ledger_main(["check", "--ledger", p])


def test_m4i_cross_vocab_probe_no_false_positive(tmp_path):
    """R1: wild-params arm at a vocab with no baseline must be skipped, not failed."""
    p = str(tmp_path / "ledger.csv")
    _write(p, [_baseline(vocab="64"),
               _row(model="p9-probe-toy", params="999999999", seed="9",
                    vocab="999", gateval="0.05")])
    ledger_main(["check", "--ledger", p])


def test_m4i_same_vocab_drift_still_fails_loudly(tmp_path):
    """Guard must survive the R1 fix: >2% drift at a baselined (scale,vocab) fails."""
    import pytest
    p = str(tmp_path / "ledger.csv")
    _write(p, [_baseline(vocab="64"),
               _row(model="p9-probe-toy", params="1", seed="9",
                    vocab="64", gateval="0.05")])
    with pytest.raises(SystemExit):
        ledger_main(["check", "--ledger", p])


def test_m4i_train_guard_accepts_suffixed_p2_slots(tmp_path):
    """R2: --model p2-G0-toy --slots 0 is a valid p2 ablation, must not misroute."""
    from postformer.harness.train import main as train_main
    out = str(tmp_path / "train-out")
    train_main(["--model", "p2-G0-toy", "--slots", "0", "--out", out,
                "--steps", "1", "--batch", "2", "--log-every", "1",
                "--seed", "0"])
    with open(os.path.join(out, "train_summary.json")) as f:
        s = json.load(f)
    assert s["config"]["slots"] == 0, s["config"]
    assert s["model"] == "p2-G0-toy", s["model"]


def test_m4i_train_guard_still_rejects_misrouted_slots():
    """Guard must survive the R2 fix: --slots on a p1 arm still fails loudly."""
    import pytest
    from postformer.harness.train import main as train_main
    with pytest.raises(SystemExit):
        train_main(["--model", "p1-toy", "--slots", "0", "--out", "/tmp/m4i-nope",
                    "--steps", "1", "--batch", "2"])


def test_m4i_recall_guard_accepts_suffixed_p2_window(tmp_path):
    """R2: --model p2-G0-toy --window 16 is a valid p2 eval, must not misroute."""
    from postformer.harness.synthetic_recall import main as recall_main
    out = str(tmp_path / "recall-out")
    recall_main(["--model", "p2-G0-toy", "--window", "16", "--out", out,
                 "--task", "mqar", "--episodes", "4", "--n-pairs", "2",
                 "--vocab", "64", "--seed", "0"])
    with open(os.path.join(out, "g1_summary_seed0.json")) as f:
        s = json.load(f)
    assert "mqar" in s, s.keys()


def test_m4i_recall_guard_still_rejects_transformer_window(tmp_path):
    """Guard must survive the R2 fix: --window on transformer still fails loudly."""
    import pytest
    from postformer.harness.synthetic_recall import main as recall_main
    with pytest.raises(SystemExit):
        recall_main(["--model", "transformer-toy", "--window", "16",
                     "--out", str(tmp_path / "recall-nope"),
                     "--task", "mqar", "--episodes", "4", "--n-pairs", "2",
                     "--vocab", "64", "--seed", "0"])
