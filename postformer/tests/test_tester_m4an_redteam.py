"""Tester M4an red-team: head-d9fd82e8 live pins not covered by M4am (Refs #294).

Novel vs M4am (parity toy+tiny, flatness totals, W16 causality, CLI flags,
dedup, viewer, honesty, hygiene):
  1. live param parity at SMALL scale, all five candidates within 2%,
  2. tie_embeddings guard live-fire: rejected for p1-p5, honored by baseline,
  3. parse_model_name strictness: canonical names parse, middle tags
     (p2-G0-toy), vocab suffixes (p1-toy-V512), unknown families
     (p9-probe-toy) fail loudly,
  4. build_model contract: returns (model, cfg) with vocab_size/window keys,
     family name must not contain '-',
  5. per-layer state_size pins at tiny (P1/P4 524288, P2 589824,
     P3/P5 786432) summing to the proof-g4.md totals,
  6. MINI causality for p2/p3 (step-vs-forward <= 1e-4, T=1 finite),
  7. enwik8_bpb model-name guard reachable via load_model even though the
     CLI checks the data file first (documents the ordering wart),
  8. ledger schema is 26 cols and `check` is green on the committed ledger.
"""
import subprocess
import sys
from pathlib import Path

import pytest
import torch

REPO = Path(__file__).resolve().parents[2]

PER_LAYER_TINY = {"p1": 524288, "p4": 524288, "p2": 589824,
                  "p3": 786432, "p5": 786432}
TOTALS_TINY = {"p1": 3145728, "p4": 3145728, "p2": 3538944,
               "p3": 4718592, "p5": 4718592}


# --- 1. small-scale parity ---

def test_an1_live_parity_small_within_2pct():
    from postformer.models.factory import count_params
    base, _ = count_params("transformer", "small")
    assert base == 113462016
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        n, _ = count_params(fam, "small")
        assert abs(n - base) / base <= 0.02, (fam, n, base)


# --- 2. tie_embeddings guard ---

def test_an2_tie_embeddings_rejected_for_candidates_honored_by_baseline():
    from postformer.models.factory import build_model
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        with pytest.raises(ValueError):
            build_model(fam, "toy", {"tie_embeddings": True})
    m, _ = build_model("transformer", "toy", {"tie_embeddings": True})
    assert m.lm_head is None


# --- 3. parse_model_name strictness ---

def test_an3_parse_model_name_accepts_canonical_rejects_variants():
    from postformer.models.factory import parse_model_name
    assert parse_model_name("p1-tiny") == ("p1", "tiny")
    assert parse_model_name("transformer-small") == ("transformer", "small")
    for bad in ("p2-G0-toy", "p1-toy-V512", "p9-probe-toy", "p1",
                "p1-toy-extra", ""):
        with pytest.raises((ValueError, SystemExit)):
            parse_model_name(bad)


# --- 4. build_model contract ---

def test_an4_build_model_returns_tuple_with_vocab_and_window():
    from postformer.models.factory import build_model
    m, cfg = build_model("p1", "toy", {})
    assert isinstance(cfg, dict)
    assert cfg["vocab_size"] >= 16 and cfg["window"] >= 0
    with pytest.raises(ValueError):
        build_model("p1-toy", "toy", {})


# --- 5. per-layer state inventory ---

def test_an5_per_layer_state_pins_sum_to_proof_totals():
    from postformer.models.factory import build_model
    for fam, per_layer in PER_LAYER_TINY.items():
        m, _ = build_model(fam, "tiny", {})
        assert m.blocks[0].state_size() == per_layer, (fam,)
        assert m.blocks[0].state_size() * 6 == TOTALS_TINY[fam], fam
        assert m.state_bytes(1, 1024) == TOTALS_TINY[fam], fam
        del m


# --- 6. MINI causality for p2/p3 ---

def test_an6_mini_p2_p3_step_forward_and_t1():
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).parent))
    from conftest import MINI
    from postformer.models.factory import build_model
    torch.manual_seed(0)
    for fam in ("p2", "p3"):
        m, cfg = build_model(fam, "toy", dict(MINI))
        m.eval()
        V = cfg["vocab_size"]
        with torch.no_grad():
            x = torch.randint(0, V - 2, (1, 20))
            out_f = m.forward(x)
            S = m.init_state(1, "cpu", torch.float32)
            outs = []
            for i in range(20):
                o, S = m.step(x[:, i:i + 1], S)
                outs.append(o)
            d = (out_f - torch.cat(outs, dim=1)).abs().max().item()
            assert d <= 1e-4, (fam, d)
            x1 = torch.randint(0, V - 2, (1, 1))
            assert bool(torch.isfinite(m.forward(x1)).all()), fam


# --- 7. enwik8 model-name guard reachable via load_model ---

def test_an7_load_model_rejects_unknown_family_before_io():
    from postformer.harness.util import load_model
    with pytest.raises((ValueError, SystemExit)):
        load_model("p9-probe-toy", None, None, {}, "cpu", torch.float32)


# --- 8. ledger schema + green check ---

def test_an8_ledger_26col_and_check_green():
    import csv
    p = REPO / "postformer" / "ledger" / "ledger.csv"
    with open(p, newline="") as f:
        header = next(csv.reader(f))
    assert len(header) == 26, len(header)
    r = subprocess.run(
        [sys.executable, "-m", "postformer.harness.ledger",
         "check", "--ledger", str(p)],
        capture_output=True, text=True, timeout=300, cwd=str(REPO),
    )
    assert r.returncode == 0, r.stderr[-2000:]
    assert "ledger OK" in r.stdout
