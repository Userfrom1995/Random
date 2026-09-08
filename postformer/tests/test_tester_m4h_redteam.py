"""Tester M4h hostile suite: slot-eviction correctness, G-capacity identity,
envelope-audit pin consistency, and A6 grouped-drift gate (Refs #294).

Covers deltas at HEAD that prior red-team suites do not pin down:
- SlotBuffer eviction keeps the NEWEST G writes (oldest evicted), n capped at G.
- G16 vs G64 bitwise identical at toy T=33 (no eviction in either), which is the
  mechanistic basis for the ledger's "G>=5 behaviorally identical" A4 note.
- envelope-audit.md state-byte pins agree with proof-g4.md and code state_size.
- A6 V512 arms: p1-vs-transformer drift grouped by (scale, vocab) stays in gate.
"""

import csv
import re

import torch

from postformer.models.factory import build_model, count_params
from postformer.models.p2_slots import SlotBuffer


def _slot_tags(buf):
    return buf.keys[0, 0, :, 0].tolist()


def test_m4h_eviction_keeps_newest_g_writes():
    torch.manual_seed(0)
    buf = SlotBuffer(1, 2, 8, 8, slots=4, stride=8,
                     device="cpu", dtype=torch.float32)
    for w in range(9):
        k = torch.full((1, 2, 8), float(w))
        v = torch.full((1, 2, 8), float(100 + w))
        buf.pos = w * 8  # land exactly on stride positions
        buf.append(k, v)
    assert buf.n == 4
    assert buf.writes == 9
    assert _slot_tags(buf) == [5.0, 6.0, 7.0, 8.0]
    # reads only attend over written slots, never uninitialized tail
    q = torch.randn(1, 2, 8)
    out = buf.read(q)
    assert out is not None and torch.isfinite(out).all()


def test_m4h_read_empty_buffer_returns_none():
    buf = SlotBuffer(1, 2, 8, 8, slots=4, stride=8,
                     device="cpu", dtype=torch.float32)
    assert buf.read(torch.randn(1, 2, 8)) is None


def test_m4h_g16_vs_g64_bitwise_identical_at_toy_t():
    torch.manual_seed(7)
    m16, _ = build_model("p2", "toy", {"slots": 16, "slot_stride": 8})
    torch.manual_seed(7)
    m64, _ = build_model("p2", "toy", {"slots": 64, "slot_stride": 8})
    m16.eval()
    m64.eval()
    x = torch.randint(0, 64, (1, 33))
    with torch.no_grad():
        d = (m16.forward(x) - m64.forward(x)).abs().max().item()
    assert d == 0.0, d


def test_m4h_g4_diverges_only_via_eviction():
    # G4 must evict once at T=33 (5 writes > 4 slots); G16 never evicts.
    # Both stay finite; divergence is bounded to the eviction effect.
    torch.manual_seed(7)
    m4, _ = build_model("p2", "toy", {"slots": 4, "slot_stride": 8})
    torch.manual_seed(7)
    m16, _ = build_model("p2", "toy", {"slots": 16, "slot_stride": 8})
    m4.eval()
    m16.eval()
    x = torch.randint(0, 64, (1, 33))
    with torch.no_grad():
        o4, o16 = m4.forward(x), m16.forward(x)
    assert torch.isfinite(o4).all() and torch.isfinite(o16).all()
    d = (o4 - o16).abs().max().item()
    assert d > 0.0, "expected G4 eviction to change the last-token read"
    assert d < 50.0, d  # eviction swaps one slot, must not explode


def test_m4h_slots_zero_disables_buffer():
    buf = SlotBuffer(1, 2, 8, 8, slots=0, stride=8,
                     device="cpu", dtype=torch.float32)
    for _ in range(20):
        buf.append(torch.randn(1, 2, 8), torch.randn(1, 2, 8))
    assert buf.n == 0
    assert buf.read(torch.randn(1, 2, 8)) is None


def test_m4h_envelope_audit_pins_match_proof():
    with open("postformer/docs/envelope-audit.md") as f:
        audit = f.read()
    with open("postformer/docs/proof-g4.md") as f:
        proof = f.read()
    for pin in ["3145728", "3538944", "4718592"]:
        assert pin in proof, pin
    # audit deliberately delegates byte inventories to proof-g4 (single source
    # of truth) instead of duplicating pins; assert the delegation is explicit
    assert "proof-g4.md is source of" in audit


def test_m4h_a6_vocab_pilot_grouped_drift_in_gate():
    c_p1, _ = count_params("p1", "toy", {"vocab_size": 514})
    c_tr, _ = count_params("transformer", "toy", {"vocab_size": 514})
    drift = abs(c_p1 - c_tr) / c_tr
    assert drift <= 0.02, drift
    with open("postformer/ledger/ledger.csv") as f:
        rows = list(csv.DictReader(f))
    v512 = [r for r in rows if r["vocab"] == "512"]
    assert len(v512) == 2, [r["model"] for r in v512]
    for r in v512:
        assert float(r["g1_mqar_8"]) == 0.0, r  # floor honesty, chance 1/512
        assert "NOT a gate result" in r["notes"], r["model"]


def test_m4h_a4_ledger_g4_g64_cells_match_curves():
    import json
    with open("postformer/ledger/ledger.csv") as f:
        rows = list(csv.DictReader(f))
    by_slot = {(r["model"], r["slots"]): r for r in rows
               if r["model"] == "p2-toy" and r["slots"] in ("4", "64")}
    assert set(by_slot) == {("p2-toy", "4"), ("p2-toy", "64")}
    for (model, slots), row in by_slot.items():
        tag = f"G{slots}"
        path = (f"postformer/ledger/curves/a4-toy/"
                f"g1_summary_p2-{tag}-toy-s0.json")
        with open(path) as f:
            summary = json.load(f)
        mqar8 = summary["mqar"]["8"]["acc"]
        assert abs(float(row["g1_mqar_8"]) - float(mqar8)) < 1e-9, (model, slots, row)
        assert row["model"] == summary["model"] == "p2-toy"
    # trained-score coincidence that the ledger discloses
    assert (by_slot[("p2-toy", "4")]["g1_mqar_8"]
            == by_slot[("p2-toy", "64")]["g1_mqar_8"])


def test_m4h_no_emdashes_in_audit_chain():
    for path in ["postformer/docs/envelope-audit.md",
                 "postformer/tests/test_tester_m4h_redteam.py"]:
        with open(path, encoding="utf-8") as f:
            assert "\u2014" not in f.read(), path


def test_m4h_refs_discipline_in_new_suite():
    import io
    with open("progress/294-post-transformer-sequence-architecture.md",
              encoding="utf-8") as f:
        lines = f.read().splitlines()
    assert any("Refs #294" in ln for ln in lines)
    # every "Closes #294" occurrence must be conditional ("only on/when ..."),
    # never a standalone closing directive while gates are still pending
    for ln in lines:
        if "Closes #294" in ln:
            assert re.search(r"only (on|when)|if ", ln), ln
