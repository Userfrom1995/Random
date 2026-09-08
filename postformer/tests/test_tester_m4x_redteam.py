"""Tester M4x hostile suite: family-wide live pins for the current head.

Refs #294 (toy/analytic checks only, never gate results).

Why this suite exists: prior suites pin components per-milestone, but no
single suite pins the whole-family contract live at one head:

- X1 (LM step/forward equivalence, all six arms): every family must
  satisfy maxdiff <= 1e-4 at toy T=24 (causality premise for all probes).
- X2 (G4 flatness live): state_bytes(1k) == state_bytes(32k) for all five
  candidates while the transformer control grows (tier-a/b premise).
- X3 (A1 matched key scale): P1 and P5 _normed_k both emit unit-norm
  keys at high input gain (honest ablation premise after the unit-norm
  fixer delta).
- X4 (parity envelope): every candidate within 2% of baseline at
  toy/tiny/small (factory pin regression guard).
- X5 (ledger live): the shipped ledger passes cmd_check green.
- X6 (viewer hardening source pin): splitCSV is used for header and rows
  and esc() wraps model/seed/notes cells (CSV+XSS premise).
"""

import torch

from postformer.harness.ledger import cmd_check
from postformer.models.factory import build_model, count_params

_FAMS = ["transformer", "p1", "p2", "p3", "p4", "p5"]
_CANDS = ["p1", "p2", "p3", "p4", "p5"]


def test_x1_lm_step_matches_forward_all_families():
    torch.manual_seed(1)
    for fam in _FAMS:
        m, _ = build_model(fam, "toy", None)
        m.eval()
        ids = torch.randint(0, 66, (2, 24))
        with torch.no_grad():
            a = m.forward(ids)
            states = m.init_state(2, "cpu", torch.float32)
            outs = []
            for i in range(24):
                o, states = m.step(ids[:, i:i + 1], states)
                outs.append(o)
            b = torch.cat(outs, dim=1)
        assert bool(torch.isfinite(a).all()), fam
        d = float((a - b).abs().max())
        assert d <= 1e-4, (fam, d)


def test_x2_state_bytes_flat_for_candidates_grows_for_control():
    for fam in _CANDS:
        m, _ = build_model(fam, "toy", None)
        assert m.state_bytes(1, 1000) == m.state_bytes(1, 32000), fam
    m, _ = build_model("transformer", "toy", None)
    assert m.state_bytes(1, 32000) > m.state_bytes(1, 1000)


def test_x3_p1_p5_keys_unit_norm_at_high_gain():
    from postformer.models.p1_delta_hybrid import GatedDeltaMemory
    from postformer.models.p5_map import GatedMapMemory
    torch.manual_seed(0)
    d1 = GatedDeltaMemory(d_model=32, heads=2, d_k=8, d_v=8)
    d5 = GatedMapMemory(d_model=32, heads=2, d_k=8, d_v=8)
    d1.eval()
    d5.eval()
    x = torch.randn(4, 32) * 5.0
    with torch.no_grad():
        k1 = d1._normed_k(d1._split(d1.w_k(x), 8))
        k5 = d5._normed_k(d5._split(d5.w_k(x), 8))
    for name, k in (("p1", k1), ("p5", k5)):
        n = k.norm(dim=-1)
        assert torch.all(torch.isfinite(k)), name
        assert torch.allclose(n, torch.ones_like(n), atol=1e-5), (
            name, float(n.min()), float(n.max()))


def test_x4_parity_within_two_percent_all_scales():
    base = {}
    for sc in ("toy", "tiny", "small"):
        n, _ = count_params("transformer", sc)
        base[sc] = n
    for fam in _CANDS:
        for sc in ("toy", "tiny", "small"):
            n, _ = count_params(fam, sc)
            drift = abs(n - base[sc]) / base[sc]
            assert drift <= 0.02, (fam, sc, n, base[sc], drift)


def test_x5_shipped_ledger_check_green():
    cmd_check(type("A", (), {"ledger": "postformer/ledger/ledger.csv"})())


def test_x6_viewer_splitcsv_and_esc():
    text = open("postformer/viewer/index.html").read()
    assert "function splitCSV(line)" in text
    assert "splitCSV(lines[0])" in text
    assert "splitCSV(l)" in text
    for cell in ("esc(r.model)", "esc(r.seed)", "esc(r.notes)"):
        assert cell in text, cell
    code_uses = [l for l in text.splitlines()
                 if 'split(",")' in l and not l.strip().startswith("//")]
    assert code_uses == [], code_uses
