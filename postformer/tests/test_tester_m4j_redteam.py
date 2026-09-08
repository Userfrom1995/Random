"""Tester M4j hostile suite: N>vocab eval crash + cross-artifact consistency.

Refs #294 (toy probes only, never gate results).

R1 - unhandled crash on a valid CLI combination (FAILING until fixed):
  `synthetic_recall --model p1-toy --vocab 64` (default --n-pairs 16,64,256)
  dies mid-run with an unhandled numpy ValueError
  ("Cannot take a larger sample than population when replace is False")
  from gen_mqar (rng.choice(vocab, size=n_pairs, replace=False)) once N
  exceeds vocab, AFTER writing partial g1 CSVs and with no summary JSON.
  --vocab 64 is valid (>= 16) and the default n-pairs list is valid, so a
  user following the toy protocol without an explicit --n-pairs gets a raw
  traceback instead of a friendly refusal. The harness must validate
  n_pairs <= vocab up front and refuse loudly (SystemExit) before writing
  anything, or skip infeasible N with a documented warning. All committed
  toy rows used explicit --n-pairs 8,16, so no ledger cell is affected.

The remaining tests are durable passing guards around the same code paths:
feasible-N roundtrip, six-family causality/flatness sweep, code-vs-proof
state pins, and ledger inf/range rejection.
"""

import csv
import json
import os

import pytest
import torch

from postformer.harness.ledger import SCHEMA, main as ledger_main
from postformer.harness.synthetic_recall import main as recall_main
from postformer.models.factory import build_model


def _write(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA)
        w.writeheader()
        w.writerows(rows)


def _row(model="p1-toy", params="336332", seed="0", vocab="64", window="16",
         gate="g1_mqar_8", gateval="0.06", notes="m4j probe Refs #294"):
    r = {c: "" for c in SCHEMA}
    r.update({"model": model, "params": params, "train_tokens": "528000",
              "seed": seed, "vocab": vocab, "window": window,
              "gpu_hours": "0", "notes": notes})
    r[gate] = gateval
    return r


def test_m4j_npairs_above_vocab_refuses_loudly(tmp_path):
    """R1: N=256 at vocab 64 must be a friendly CLI refusal, not a traceback.

    Currently raises ValueError from numpy after partial CSV writes.
    Passes once the harness validates n_pairs <= vocab up front
    (SystemExit) and writes no partial g1 outputs on refusal.
    """
    out = str(tmp_path / "eval")
    os.makedirs(out, exist_ok=True)
    with pytest.raises(SystemExit):
        recall_main(["--model", "p1-toy", "--vocab", "64",
                     "--n-pairs", "8,256", "--task", "mqar",
                     "--episodes", "2", "--out", out, "--seed", "0"])
    leftovers = [f for f in os.listdir(out) if f.startswith("g1_")]
    assert leftovers == [], f"refusal must not leave partial outputs: {leftovers}"


def test_m4j_feasible_toy_eval_roundtrip(tmp_path):
    """The feasible-N path the R1 guard must not break: vocab64/N8 eval."""
    out = str(tmp_path / "eval")
    os.makedirs(out, exist_ok=True)
    recall_main(["--model", "p1-toy", "--vocab", "64",
                 "--n-pairs", "8", "--task", "mqar",
                 "--episodes", "2", "--out", out, "--seed", "0"])
    summary = os.path.join(out, "g1_summary_seed0.json")
    assert os.path.exists(summary), os.listdir(out)
    with open(summary) as f:
        blob = json.load(f)
    acc = blob["mqar"]["8"]["acc"]
    assert 0.0 <= acc <= 1.0, acc
    assert blob["random_init"] is True


def test_m4j_six_family_causality_flatness_sweep():
    """Step/forward equivalence + flat-vs-linear state across all families."""
    for fam in ["transformer", "p1", "p2", "p3", "p4", "p5"]:
        m, _ = build_model(fam, "toy")
        m.eval()
        with torch.no_grad():
            o1 = m.forward(torch.randint(0, 64, (1, 1)))
            assert torch.isfinite(o1).all(), fam
            T = 33  # crosses the toy W=16 window boundary
            x = torch.randint(0, 64, (1, T))
            of = m.forward(x)
            st = m.init_state(1, "cpu", torch.float32)
            outs = []
            for i in range(T):
                oi, st = m.step(x[:, i:i + 1], st)
                outs.append(oi)
            d = (of - torch.cat(outs, dim=1)).abs().max().item()
            assert d <= 1e-4, (fam, d)
            lo, hi = m.state_bytes(1, 1024), m.state_bytes(1, 32768)
            if fam == "transformer":
                assert hi > lo, (fam, lo, hi)  # KV cache grows by design
            else:
                assert hi == lo, (fam, lo, hi)  # recurrent state is O(1)


def test_m4j_candidate_state_matches_proof_toy_pins():
    """Code state_bytes agree with the proof-g4.md toy pins (post-fix)."""
    sizes = {}
    for fam in ["p1", "p2", "p3", "p4", "p5"]:
        m, _ = build_model(fam, "toy")
        sizes[fam] = (m.state_bytes(1, 1024), m.state_bytes(1, 32768))
    assert sizes["p1"] == (24576, 24576), sizes["p1"]
    assert sizes["p4"] == sizes["p1"], (sizes["p4"], sizes["p1"])  # P4 == P1
    assert sizes["p5"] == (40960, 40960), sizes["p5"]
    with open("postformer/docs/proof-g4.md") as f:
        proof = f.read()
    assert "24576" in proof and "40960" in proof


def test_m4j_ledger_rejects_inf_gate_cell(tmp_path):
    """Hand-crafted inf gate cell (bypasses append validation) must fail."""
    p = str(tmp_path / "ledger.csv")
    base = _row(model="transformer-toy", params="336768", window="",
                notes="m4j baseline Refs #294")
    bad = _row(gateval="inf")
    _write(p, [base, bad])
    with pytest.raises(SystemExit):
        ledger_main(["check", "--ledger", p])


def test_m4j_ledger_rejects_out_of_range_acc(tmp_path):
    """Accuracy cells live in [0,1]; 1.5 must fail loudly, never pass."""
    p = str(tmp_path / "ledger.csv")
    base = _row(model="transformer-toy", params="336768", window="",
                notes="m4j baseline Refs #294")
    bad = _row(gateval="1.5")
    _write(p, [base, bad])
    with pytest.raises(SystemExit):
        ledger_main(["check", "--ledger", p])


def test_m4j_gen_mqar_requires_n_within_vocab():
    """Unit contract behind R1: the generator cannot serve n_pairs > vocab."""
    import numpy as np

    from postformer.harness.synthetic_recall import gen_mqar
    rng = np.random.default_rng(0)
    seq, queries = gen_mqar(rng, 64, 8)
    assert len(queries) == 8 and len(seq) == 16
    with pytest.raises(Exception):
        gen_mqar(np.random.default_rng(0), 64, 256)
