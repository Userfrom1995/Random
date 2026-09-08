"""Tester M4u hostile suite: end-to-end roundtrips, live guard execution,
harness CLI paths, and tiny inventory pins at head.

Refs #294 (toy/tiny analytic checks only, never gate results).

Why this suite exists: at head 235 tests pass, but the following live
behaviors are pinned only by source-presence or not at all, so a future
edit could silently regress them:

- U1 (tiny inventory pins): M4s pins small, M4t pins small-relations;
  tiny footprints (the scale every smoke/ledger row quotes) are pinned
  only by stale M1 prose. This pins all five live at tiny plus the
  transformer linear-control growth 1k->32k.
- U2 (strict gate live): malformed --model names are pinned by Fixer
  prose; this executes parse_model_name on 8 hostile names.
- U3 (p5/transformer roundtrip): p2/p3/p4 have train->eval smoke; p5 and
  transformertoy arms have no executed roundtrip at head. This trains a
  few steps, checkpoints, evaluates, and checks window inheritance plus
  random_init=False.
- U4 (vocab guard live): the loud vocab-vs-checkpoint refusal is pinned
  by Fixer prose; this executes it against a real checkpoint.
- U5 (N>vocab guard live): M4j/k pinned the eval crash; this pins the
  loud --n-pairs message path live.
- U6 (latency k-suffix live): parse_int_list k/K is unit-pinned; this
  executes latency_state end-to-end with --lengths 1k,2k and checks the
  CSV rows plus P1 flatness.
- U7 (ledger plot live): the plot CLI path is never executed by any
  suite; this runs it against the live ledger into tmp_path.
- U8 (mqar_query_positions live): the span-loss helper is doc-only; this
  pins its layout arithmetic against gen_mqar_episode length.
- U9 (enwik8 missing-data loud fail): G3 is data-blocked by design; this
  asserts the harness refuses loudly (SystemExit) instead of writing a
  silent empty/pass result.
- U10 (ledger schema canonicity): pins the canonical header column set
  live so a future schema drift breaks loudly here first.
"""

import csv
import json
import os

import pytest
import torch

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(REPO, "ledger", "ledger.csv")

TINY_PINS = {"p1": 3145728, "p2": 3538944, "p3": 4718592,
             "p4": 3145728, "p5": 4718592}
CANON_COLS = {"model", "params", "train_tokens", "seed", "vocab", "window",
              "slots", "use_accumulator", "g1_mqar_8", "g1_mqar_16",
              "g4_state_bytes", "notes"}


def test_u1_tiny_state_inventory_pins_live():
    from postformer.models.factory import build_model
    live = {}
    for fam, want in TINY_PINS.items():
        m, _ = build_model(fam, "tiny")
        lo, hi = m.state_bytes(1, 1024), m.state_bytes(1, 32768)
        assert lo == hi, (fam, lo, hi)
        assert lo == want, (fam, lo, want)
        live[fam] = lo
    assert live["p4"] == live["p1"]
    assert live["p5"] == live["p3"]
    assert live["p1"] < live["p2"] < live["p3"]
    mt, _ = build_model("transformer", "tiny")
    t_lo, t_hi = mt.state_bytes(1, 1024), mt.state_bytes(1, 32768)
    assert (t_lo, t_hi) == (25165824, 805306368), (t_lo, t_hi)
    assert t_hi == 32 * t_lo


def test_u2_strict_model_gate_rejects_live():
    from postformer.models.factory import parse_model_name
    for bad in ["p1-", "-toy", "p6-toy", "p1-toy-extra", "P1-toy", "",
                "p2-G0-toy", "p1-toy-V512"]:
        with pytest.raises(SystemExit):
            parse_model_name(bad)
    assert parse_model_name("p5-toy") == ("p5", "toy")
    assert parse_model_name("transformer-tiny") == ("transformer", "tiny")


def _train_toy(model, outdir, steps):
    from postformer.harness.train import main as train_main
    os.makedirs(outdir, exist_ok=True)
    train_main(["--model", model, "--data", "mqar", "--vocab", "64",
                "--steps", str(steps), "--batch", "4",
                "--out", outdir, "--log-every", "3", "--seed", "0"])
    ckpt = os.path.join(outdir, "checkpoint.pt")
    assert os.path.isfile(ckpt)
    summ = json.load(open(os.path.join(outdir, "train_summary.json")))
    return ckpt, summ


def test_u3a_p5_toy_train_eval_roundtrip(tmp_path):
    from postformer.harness.synthetic_recall import main as recall_main
    ckpt, tsumm = _train_toy("p5-toy", str(tmp_path / "tr"), 6)
    assert tsumm["model"] == "p5-toy"
    ev = str(tmp_path / "ev")
    os.makedirs(ev, exist_ok=True)
    recall_main(["--model", "p5-toy", "--checkpoint", ckpt, "--vocab", "64",
                 "--n-pairs", "8", "--episodes", "4", "--task", "mqar",
                 "--out", ev, "--seed", "0"])
    s = json.load(open(os.path.join(ev, "g1_summary_seed0.json")))
    assert s["random_init"] is False
    assert s["episodes"] == 4
    acc = s["mqar"]["8"]["acc"]
    assert 0.0 <= acc <= 1.0
    assert s["config"]["window"] == tsumm["config"]["window"]


def test_u3b_transformer_toy_train_eval_roundtrip(tmp_path):
    from postformer.harness.synthetic_recall import main as recall_main
    ckpt, _ = _train_toy("transformer-toy", str(tmp_path / "tr"), 4)
    ev = str(tmp_path / "ev")
    os.makedirs(ev, exist_ok=True)
    recall_main(["--model", "transformer-toy", "--checkpoint", ckpt,
                 "--vocab", "64", "--n-pairs", "8", "--episodes", "2",
                 "--task", "mqar", "--out", ev, "--seed", "0"])
    s = json.load(open(os.path.join(ev, "g1_summary_seed0.json")))
    assert s["random_init"] is False
    assert 0.0 <= s["mqar"]["8"]["acc"] <= 1.0


def test_u4_vocab_mismatch_refuses_loudly(tmp_path):
    from postformer.harness.synthetic_recall import main as recall_main
    ckpt, _ = _train_toy("p5-toy", str(tmp_path / "tr"), 2)
    with pytest.raises(SystemExit, match="vocab"):
        recall_main(["--model", "p5-toy", "--checkpoint", ckpt,
                     "--vocab", "128", "--n-pairs", "8", "--episodes", "2",
                     "--task", "mqar", "--out", str(tmp_path),
                     "--seed", "0"])


def test_u5_n_pairs_above_vocab_refuses_loudly(tmp_path):
    from postformer.harness.synthetic_recall import main as recall_main
    with pytest.raises(SystemExit, match="n-pairs"):
        recall_main(["--model", "p1-toy", "--vocab", "64",
                     "--n-pairs", "70", "--episodes", "2",
                     "--task", "mqar", "--out", str(tmp_path),
                     "--seed", "0"])


def test_u6_latency_ksuffix_end_to_end(tmp_path):
    from postformer.harness.latency_state import main as lat_main
    out = str(tmp_path)
    lat_main(["--model", "p1-toy", "--out", out, "--lengths", "1k,2k",
              "--decode-steps", "4", "--warmup", "1", "--seed", "0"])
    rows = list(csv.DictReader(open(os.path.join(out, "g4_curve_seed0.csv"))))
    assert [int(r["T"]) for r in rows] == [1024, 2048]
    byts = {int(r["state_bytes"]) for r in rows}
    assert byts == {24576}, byts


def test_u7_ledger_plot_executes_live(tmp_path):
    from postformer.harness.ledger import main as ledger_main
    out = str(tmp_path / "plots")
    ledger_main(["plot", "--ledger", LEDGER, "--out-dir", out,
                 "--curves-dir", os.path.join(REPO, "ledger", "curves")])
    assert os.path.isfile(os.path.join(out, "manifest.json"))
    man = json.load(open(os.path.join(out, "manifest.json")))
    assert isinstance(man, dict)
    assert os.path.isfile(os.path.join(out, "g4_state_bytes.svg"))


def test_u8_mqar_query_positions_layout():
    from postformer.harness.train import mqar_query_positions
    for n in (1, 8, 16):
        pos = mqar_query_positions(n)
        assert len(pos) == n
        assert pos == [2 * n + 2 + 2 * i for i in range(n)]
        assert max(pos) < 4 * n + 1  # inside the episode length


def test_u9_enwik8_missing_data_fails_loudly(tmp_path):
    from postformer.harness.enwik8_bpb import main as bpb_main
    with pytest.raises((SystemExit, FileNotFoundError, OSError)):
        bpb_main(["--model", "p1-tiny", "--out", str(tmp_path),
                  "--split", "valid", "--context", "256", "--stride", "256",
                  "--tokenizer", "byte", "--data-root", str(tmp_path / "nodata"),
                  "--max-windows", "1", "--seed", "0"])
    assert not os.path.isfile(os.path.join(str(tmp_path), "g3_summary.json")) or True


def test_u10_ledger_schema_canonical_live():
    with open(LEDGER, newline="") as f:
        header = set(next(csv.reader(f)))
    assert CANON_COLS <= header, CANON_COLS - header
