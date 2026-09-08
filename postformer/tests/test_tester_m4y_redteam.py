"""Tester M4y hostile suite: roundtrip, CLI-guard, and schema liveness pins.

Refs #294 (toy/analytic checks only, never gate results).

Why this suite exists: the M4x suite pins family-wide step/forward,
flatness, key scale, parity, ledger-green, and viewer-source. The gaps
it leaves are the live paths that only fail under hostile use:

- Y1 (checkpoint roundtrip): a p2-toy state_dict saved to disk and
  loaded into a fresh model must give a bit-identical forward. The
  train-then-eval chain (load_model) assumes this; a silent key rename
  would corrupt every probe.
- Y2 (train ablation-guard routing): --slots on p1, --no-accumulator
  on p2, and --window on transformer must all refuse loudly instead
  of silently building the wrong arm (M2 silent-invalidation class).
- Y3 (synthetic_recall routing): --window on transformer must refuse,
  and a middle-tagged --model (p2-G0-toy) must refuse via the strict
  name gate.
- Y4 (ledger schema liveness): the shipped ledger must parse to
  exactly 26 columns with stdlib csv (proves notes commas survive),
  and every row model must pass parse_model_name (canonical names).
- Y5 (rebuild determinism): reseed + rebuild with the same seed must
  give an identical forward for p1-toy and transformer-toy (the
  reseed-before-build discipline train.py relies on).
- Y6 (P2 pure-SSD control): slots=0 step-vs-forward must match and
  stay finite (A4 control honesty live).
- Y7 (em-dash invariant): no U+2014 in any postformer/*.py (lab
  formatting rule, source-scanned live).
- Y8 (small-scale flatness): p3-small/p4-small state_bytes flat
  1k vs 32k while the transformer-small control grows (G4 tier
  premise beyond toy).
"""

import csv
import pathlib

import pytest
import torch

from postformer.harness import synthetic_recall as _syn
from postformer.harness import train as _train
from postformer.harness.util import reseed
from postformer.models.common import seed_all
from postformer.models.factory import build_model, parse_model_name

_HERE = pathlib.Path(__file__).resolve()
_POSTFORMER = _HERE.parents[1]


def _forward_ids(model, vocab, t=16):
    model.eval()
    ids = torch.randint(0, vocab, (1, t))
    with torch.no_grad():
        return model.forward(ids), ids


def test_y1_p2_state_dict_roundtrip_bit_identical(tmp_path):
    seed_all(7, "test-y1-init")
    m, cfg = build_model("p2", "toy", None)
    m.eval()
    a, ids = _forward_ids(m, cfg["vocab_size"])
    blob = tmp_path / "p2.pt"
    torch.save(m.state_dict(), blob)
    seed_all(999, "test-y1-other")
    m2, _ = build_model("p2", "toy", None)
    m2.load_state_dict(torch.load(blob, map_location="cpu", weights_only=True))
    m2.eval()
    with torch.no_grad():
        b = m2.forward(ids)
    assert torch.equal(a, b)


def test_y2_train_rejects_mismatched_ablation_flags(tmp_path):
    out = str(tmp_path / "o")
    with pytest.raises(SystemExit) as e:
        _train.main(["--model", "p1-toy", "--slots", "4", "--steps", "1",
                     "--batch", "1", "--log-every", "1", "--out", out])
    assert "slots" in str(e.value).lower()
    with pytest.raises(SystemExit) as e:
        _train.main(["--model", "p2-toy", "--no-accumulator", "--steps", "1",
                     "--batch", "1", "--log-every", "1", "--out", out])
    assert "accumulator" in str(e.value).lower()
    with pytest.raises(SystemExit) as e:
        _train.main(["--model", "transformer-toy", "--window", "0",
                     "--steps", "1", "--batch", "1", "--log-every", "1",
                     "--out", out])
    assert "window" in str(e.value).lower()


def test_y3_synth_rejects_window_on_transformer_and_tagged_names():
    with pytest.raises(SystemExit) as e:
        _syn.main(["--model", "transformer-toy", "--window", "0",
                   "--task", "mqar", "--episodes", "1", "--out", "x"])
    assert "window" in str(e.value).lower()
    with pytest.raises(SystemExit):
        parse_model_name("p2-G0-toy")
    with pytest.raises(SystemExit):
        parse_model_name("p1-toy-V512")


def test_y4_shipped_ledger_26_cols_and_canonical_names():
    led = _POSTFORMER / "ledger" / "ledger.csv"
    with open(led, newline="") as f:
        rows = list(csv.reader(f))
    assert len(rows[0]) == 26, rows[0]
    assert rows[0][0] == "model" and rows[0][-1] == "notes"
    for r in rows[1:]:
        assert len(r) == 26, r[0]
        parse_model_name(r[0])


def test_y5_rebuild_same_seed_identical_forward():
    for fam in ("p1", "transformer"):
        outs = []
        for _ in range(2):
            seed_all(3, "test-y5-init")
            reseed(3, f"init-{fam}-toy")
            m, cfg = build_model(fam, "toy", None)
            m.eval()
            torch.manual_seed(11)
            ids = torch.randint(0, cfg["vocab_size"], (1, 12))
            with torch.no_grad():
                outs.append(m.forward(ids))
        assert torch.equal(outs[0], outs[1]), fam


def test_y6_p2_slots_zero_step_matches_forward():
    seed_all(5, "test-y6-init")
    m, _ = build_model("p2", "toy", {"slots": 0})
    m.eval()
    ids = torch.randint(0, 66, (1, 20))
    with torch.no_grad():
        a = m.forward(ids)
        st = m.init_state(1, "cpu", torch.float32)
        outs = []
        for i in range(20):
            o, st = m.step(ids[:, i:i + 1], st)
            outs.append(o)
        b = torch.cat(outs, dim=1)
    assert bool(torch.isfinite(a).all())
    assert float((a - b).abs().max()) <= 1e-4


def test_y7_no_em_dash_in_postformer_sources():
    bad = []
    for p in sorted(_POSTFORMER.rglob("*.py")):
        if "\u2014" in p.read_text(encoding="utf-8"):
            bad.append(str(p.relative_to(_POSTFORMER)))
    assert bad == []


def test_y8_small_flatness_p3_p4_vs_control():
    for fam in ("p3", "p4"):
        m, _ = build_model(fam, "small", None)
        assert m.state_bytes(1, 1000) == m.state_bytes(1, 32000), fam
    m, _ = build_model("transformer", "small", None)
    assert m.state_bytes(1, 32000) > m.state_bytes(1, 1000)
