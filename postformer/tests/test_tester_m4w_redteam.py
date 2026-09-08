"""Tester M4w hostile suite: live pins for the post-M4v fixer delta.

Refs #294 (toy/analytic checks only, never gate results).

Why this suite exists: the fixer commits on top of the M4v suite
(P5 unit-norm keys, ledger zero-baseline drift guard + SVG escaping +
NaN filtering, latency_state --vocab forwarding + guard, P3 FusionGate
removal) were verified by hand, not pinned by any suite:

- W1 (P5 unit-norm keys live): GatedMapMemory._normed_k must emit
  unit-norm keys at any input scale (the honest-A1 matched-scale claim).
- W2 (P5 map bound live): poly_map on a unit-norm key has
  ||phi||^2 = 1 + 0.25*sum(k_i^4) <= 1.25 (T6 stability premise).
- W3 (SVG escaping + non-finite filtering live): svg_line with an
  XML-evil label and inf/nan points must escape markup and still write
  a finite-only file.
- W4 (zero-baseline drift guard live): cmd_check on a ledger whose
  transformer baseline has params=0 must fail loudly with a
  zero-baseline error, not ZeroDivisionError, not silent pass.
- W5 (latency --vocab guard live): latency_state --vocab 0 must refuse
  fast with a --vocab error before any checkpoint load.
- W6 (P3 FusionGate removal live): postformer.models.p3_decoupled must
  not export FusionGate (dead import dropped by the fixer).
"""

import csv
import subprocess
import sys

import torch

from postformer.harness.ledger import SCHEMA, cmd_check, svg_line
from postformer.models.p5_map import GatedMapMemory, poly_map


def test_w1_p5_normed_keys_unit_norm_at_any_scale():
    mem = GatedMapMemory(d_model=32, heads=2, d_k=8, d_v=8)
    mem.eval()
    for scale in (0.01, 1.0, 100.0):
        k = torch.randn(3, 2, 8) * scale
        n = mem._normed_k(k)
        norms = n.norm(dim=-1)
        assert torch.all(torch.isfinite(n)), scale
        assert torch.allclose(norms, torch.ones_like(norms), atol=1e-5), (
            scale, norms.max().item(), norms.min().item())


def test_w2_p5_poly_map_bound_on_unit_keys():
    torch.manual_seed(0)
    k = torch.randn(64, 2, 8)
    k = k / k.norm(dim=-1, keepdim=True).clamp_min(1e-6)
    pk = poly_map(k)
    assert pk.shape[-1] == 16
    sq = (pk ** 2).sum(dim=-1)
    assert bool((sq <= 1.25 + 1e-5).all()), sq.max().item()
    assert bool(torch.isfinite(pk).all())


def test_w3_svg_line_escapes_and_filters_nonfinite(tmp_path):
    out = str(tmp_path / "evil.svg")
    svg_line(out, "<title>&\"", [("<l&egend>",
                                  [(0, 1.0), (1, float("nan")),
                                   (2, float("inf")), (3, 2.0)])],
             "x<", "y>")
    text = open(out).read()
    assert "<title>" not in text and "<l&egend>" not in text
    assert "&lt;title&gt;" in text and "&lt;l&amp;egend&gt;" in text
    assert "nan" not in text.lower() and "inf" not in text.lower()


def _write_ledger(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA)
        w.writeheader()
        for r in rows:
            full = {c: "" for c in SCHEMA}
            full.update(r)
            w.writerow(full)


def test_w4_zero_baseline_params_rejected_loudly(tmp_path):
    led = str(tmp_path / "ledger.csv")
    _write_ledger(led, [
        {"model": "transformer-toy", "params": "0", "seed": "0",
         "vocab": "64", "g1_mqar_8": "0.1", "notes": "probe zero base"},
        {"model": "p1-toy", "params": "16400", "seed": "0",
         "vocab": "64", "g1_mqar_8": "0.1", "notes": "probe candidate"},
    ])
    try:
        cmd_check(type("A", (), {"ledger": led})())
    except SystemExit as e:
        assert e.code != 0
    else:
        raise AssertionError("zero-baseline ledger passed silently")
    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            cmd_check(type("A", (), {"ledger": led})())
    except SystemExit:
        pass
    assert "zero" in buf.getvalue().lower()


def test_w5_latency_state_rejects_zero_vocab():
    r = subprocess.run(
        [sys.executable, "-m", "postformer.harness.latency_state",
         "--model", "p1-toy", "--vocab", "0",
         "--lengths", "64", "--decode-steps", "1", "--warmup", "0"],
        capture_output=True, text=True, timeout=300)
    assert r.returncode != 0, r.stdout[-500:] + r.stderr[-500:]
    assert "--vocab" in (r.stderr + r.stdout)


def test_w6_p3_has_no_fusiongate():
    import postformer.models.p3_decoupled as p3
    assert not hasattr(p3, "FusionGate"), "dead FusionGate import regressed"
    assert hasattr(p3, "FusionGate3")
