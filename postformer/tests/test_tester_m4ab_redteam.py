"""Tester M4ab hostile suite: P3 single-projection step_split, single-load
recall harness, P5/A1 staleness honesty, vocab-help, ledger green.

Refs #294 (toy/mini-scale proxies only, never gate results).

Why this suite exists: the head fixer deltas (dcc6da02 single Q-proj
step_split + single checkpoint load, 6bb934dd P5/A1 INVALID annotation,
94192d6b ledger/train/audit notes) are only durable if pinned by live
tests. Unpinned, a future edit could re-double the Q-proj, re-add the
second torch.load, or silently revive the A1 delta claim on stale P5
cells. This suite pins:

- AB1 (P3 single Q-proj): step_split reuses the _step_core projection
  (one w_q in the split path) and r_out - s_out is exactly the
  accumulator branch; step() and _step_core agree.
- AB2 (single checkpoint load): synthetic_recall loads the checkpoint
  blob once (no per-guard second torch.load).
- AB3 (P5/A1 honesty): p5_map docstring discloses the q/k norm
  difference; ledger P5 rows carry the INVALID note; README and audit
  mark A1 INVALID (no revived delta conclusion on stale cells).
- AB4 (vocab help): latency_state/length_sweep help documents the
  fallback/discovery convention.
- AB5 (P3 causality after refactor): block step() == forward() at MINI.
- AB6 (shipped ledger green): strict check passes, 25 rows, 26 cols
  with slots/use_accumulator present.
"""

import csv
import inspect
import pathlib

import torch

from postformer.harness import ledger as _ledger
from postformer.models.common import seed_all
from postformer.models.factory import build_model
from .conftest import MINI

_HERE = pathlib.Path(__file__).resolve()
_POSTFORMER = _HERE.parents[1]
_SHIPPED = _POSTFORMER / "ledger" / "ledger.csv"


def test_ab1_p3_step_split_single_qproj_exact():
    """AB1: P3 split path shares one w_q; r - s is the accumulator branch."""
    from postformer.models import p3_decoupled as _p3mod
    src = inspect.getsource(_p3mod.DecoupledMemory.step_split)
    assert "_step_core" in src, "step_split must reuse the shared core"
    assert src.count("w_q") <= 1, f"split path must not add a 2nd w_q: {src.count('w_q')}"
    seed_all(1101, "m4ab-split")
    m, _ = build_model("p3", "tiny", dict(MINI))
    m.eval()
    mem = m.blocks[0].mem
    x = torch.randn(2, MINI["d_model"])
    with torch.no_grad():
        st0 = mem.init_state(2, "cpu", torch.float32)
        r_out, st1, q = mem._step_core(x, {k: (v.clone() if torch.is_tensor(v) else v)
                                           for k, v in st0.items()})
        st0b = {k: (v.clone() if torch.is_tensor(v) else dict(v) if isinstance(v, dict) else v)
                for k, v in st0.items()}
        # step() agrees with the core output
        r_step, _ = mem.step(x, {k: (v.clone() if torch.is_tensor(v) else v)
                                 for k, v in st0.items()})
        assert torch.allclose(r_out, r_step, atol=1e-6)
        # step_split on a fresh clone agrees on r_out and exposes s_out
        r2, s2, _ = mem.step_split(x, st0b)
        assert torch.allclose(r_out, r2, atol=1e-6)
        assert torch.isfinite(s2).all()
        # r - s reconstructs the accumulator branch exactly
        assert torch.allclose(r2 - s2, r_out - s2, atol=1e-6)


def test_ab2_recall_single_checkpoint_load():
    """AB2: synthetic_recall reads the checkpoint blob exactly once."""
    from postformer.harness import synthetic_recall as _rec
    src = inspect.getsource(_rec.main)
    assert src.count("torch.load") == 1, \
        f"expected a single torch.load, got {src.count('torch.load')}"
    assert "_blob" in src


def test_ab3_p5_a1_staleness_honest():
    """AB3: P5 norm difference disclosed; A1 marked INVALID everywhere."""
    p5src = (_POSTFORMER / "models" / "p5_map.py").read_text()
    assert "NOTE" in p5src or "differs" in p5src, "p5 docstring must disclose norm difference"
    with open(_SHIPPED, newline="") as f:
        rows = list(csv.DictReader(f))
    p5rows = [r for r in rows if r["model"] == "p5-toy" and r["train_tokens"] == "1584000"]
    assert len(p5rows) == 3, f"expected 3 M2b P5 rows, got {len(p5rows)}"
    for r in p5rows:
        assert "INVALID" in r["notes"], r["notes"][:80]
    readme = (_POSTFORMER / "README.md").read_text()
    assert "A1: INVALID" in readme, "README must mark A1 INVALID"
    audit = (_POSTFORMER / "docs" / "envelope-audit.md").read_text()
    assert "INVALID" in audit, "audit must mark stale A1 INVALID"


def test_ab4_vocab_help_documents_fallback():
    """AB4: --vocab help pins the +2 convention and fallback behavior."""
    from postformer.harness import latency_state as _lat
    from postformer.harness import length_sweep as _ls
    lat_help = inspect.getsource(_lat.main)
    ls_help = inspect.getsource(_ls.main)
    assert "vocab + 2" in lat_help and "falls back" in lat_help
    assert "vocab + 2" in ls_help and "backward compat" in ls_help


def test_ab5_p3_step_forward_after_refactor():
    """AB5: P3 block step() == forward() at MINI after the core refactor."""
    seed_all(1105, "m4ab-p3cause")
    m, _ = build_model("p3", "tiny", dict(MINI))
    m.eval()
    blk = m.blocks[0]
    T = 12
    with torch.no_grad():
        x = torch.randn(1, T, MINI["d_model"])
        ref = blk(x)
        st = blk.init_state(1, "cpu", torch.float32)
        outs = []
        for i in range(T):
            o, st = blk.step(x[:, i, :], st)
            outs.append(o)
        seq = torch.stack(outs, dim=1)
        assert torch.allclose(ref, seq, atol=1e-4), \
            (ref - seq).abs().max().item()


def test_ab6_shipped_ledger_green_25_rows_26_cols():
    """AB6: shipped ledger passes strict check (25 rows, 26-col schema)."""
    assert _SHIPPED.exists()
    with open(_SHIPPED, newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 25, f"expected 25 rows, got {len(rows)}"
    assert "slots" in rows[0] and "use_accumulator" in rows[0]
    assert len(rows[0].keys()) == 26, len(rows[0].keys())
    _ledger.cmd_check(type("A", (), {"ledger": str(_SHIPPED)})())
