"""Tester M4as red-team: hostile live-fire on the post-M4b head (Refs #294).

Novel vs all prior suites: no single suite pins the CURRENT head end to
end with fast scoped probes. Slow chain tests (ao4/v2 full-envelope
task=all, ~14 min on CPU) cover the window-0 path but cannot run in a
tester pass; this suite proves the same paths with scoped
--task mqar evals (seconds). It also locks live factory parity for all
six families x three scales, correct-arg-order G4 flatness, A4
summary-cell equality with ledger coexistence, guard refusal exits, and
head honesty invariants:

  1. Live parity: all five candidates within 2% of transformer at
     toy/tiny/small, computed live from factory (not copied pins).
  2. Scoped p4 --window 0 eval: runs green, inherits window 0, writes a
     non-empty summary (fast equivalent of slow v2 envelope-all).
  3. Guards refuse loudly: transformer --window and N>vocab exit
     nonzero (fast, scoped).
  4. A4 honesty: slots 4/64 summary cells equal (mqar8/N16/2hop),
     N16 at noise floor, slots variants coexist in ledger key.
  5. G4 flatness with correct (batch, length) arg order + tiny pins
     match proof-g4.md (P1/P4 3145728, P2 3538944, P3/P5 4718592).
  6. Step-vs-forward equivalence <=1e-4 for all five candidates.
  7. Head honesty: ledger check green, >=25 rows, toy rows carry
     NOT-gate-result tags, zero Closes in new history, no U+2014 in
     changed docs, viewer splitCSV+esc present.
"""

import csv
import json
import subprocess
import sys
from pathlib import Path

import torch

from postformer.models.factory import build_model, count_params

REPO = Path(__file__).resolve().parents[2]


def _run(*args, timeout=300):
    return subprocess.run(
        [sys.executable, "-m"] + list(args),
        capture_output=True, text=True, timeout=timeout, cwd=str(REPO),
    )


def test_as1_live_parity_all_families_all_scales_within_2pct():
    """Live +-2% gate for p1/p2/p3/p4/p5 at toy/tiny/small."""
    base = {s: count_params("transformer", s)[0] for s in ("toy", "tiny", "small")}
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        for scale, b in base.items():
            n, _ = count_params(fam, scale)
            drift = (n - b) / b
            assert abs(drift) <= 0.02, (fam, scale, n, b, drift)


def test_as2_scoped_p4_window_zero_eval_runs_and_inherits(tmp_path):
    """p4 --window 0 scoped mqar eval: the M4a fix, proven fast."""
    out = str(tmp_path / "p4w0")
    r = _run("postformer.harness.synthetic_recall", "--model", "p4-toy",
             "--window", "0", "--task", "mqar", "--vocab", "64",
             "--n-pairs", "8", "--episodes", "2", "--out", out)
    assert r.returncode == 0, r.stderr[-2000:]
    s = json.loads(next(iter(Path(out).glob("g1_summary*.json"))).read_text())
    assert s["config"]["window"] == 0, s["config"]
    assert s["mqar"]["8"]["acc"] is not None


def test_as3_guards_refuse_loudly_scoped():
    """transformer --window and N>vocab must exit nonzero, fast."""
    r1 = _run("postformer.harness.synthetic_recall", "--model", "transformer-toy",
              "--window", "0", "--task", "mqar", "--episodes", "1",
              "--out", "/tmp/tester_m4as_rej")
    assert r1.returncode != 0, "transformer --window accepted silently"
    assert "no window" in (r1.stderr + r1.stdout).lower()
    r2 = _run("postformer.harness.synthetic_recall", "--model", "p1-toy",
              "--n-pairs", "100", "--vocab", "64", "--task", "mqar",
              "--episodes", "1", "--out", "/tmp/tester_m4as_nv")
    assert r2.returncode != 0, "N>vocab accepted silently"
    assert "n_pairs" in (r2.stderr + r2.stdout).lower()


def test_as4_a4_summary_cell_equality_and_key_coexistence():
    """G4==G64 summary cells, noise-floor N16, slots key coexistence."""
    rows = list(csv.DictReader(open(REPO / "postformer/ledger/ledger.csv")))
    g4 = [r for r in rows if r["model"] == "p2-toy" and r.get("slots") == "4"]
    g64 = [r for r in rows if r["model"] == "p2-toy" and r.get("slots") == "64"]
    assert g4 and g64, "A4 slots variants missing from ledger"
    for col in ("g1_mqar_8", "g1_mqar_16", "g1_2hop"):
        assert g4[0][col] == g64[0][col], (col, g4[0][col], g64[0][col])
    assert float(g4[0]["g1_mqar_16"]) < 1 / 64, "N16 must sit at noise floor"
    keys = [(r["model"], r["seed"], r.get("vocab"), r.get("window"),
             r.get("slots"), r.get("use_accumulator")) for r in rows]
    assert len(set(keys)) == len(keys), "ledger key collision on slots variants"


def test_as5_g4_flatness_correct_arg_order_and_tiny_pins():
    """state_bytes(batch, length): flat in length, pins match proof."""
    expect_tiny = {"p1": 3145728, "p4": 3145728, "p2": 3538944,
                   "p3": 4718592, "p5": 4718592}
    for fam, tiny_pin in expect_tiny.items():
        m = build_model(fam, "toy", {"vocab": 66})[0]
        assert m.state_bytes(1, 1000) == m.state_bytes(1, 32000), fam
        mt = build_model(fam, "tiny", {"vocab": 8194})[0]
        assert mt.state_bytes(1, 32000) == tiny_pin, (fam, mt.state_bytes(1, 32000))
    t = build_model("transformer", "toy", {"vocab": 66})[0]
    assert t.state_bytes(1, 32000) > t.state_bytes(1, 1000), "control must grow"


def test_as6_step_forward_equivalence_all_candidates():
    """step() incremental path matches forward() to <=1e-4."""
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        m = build_model(fam, "toy", {"vocab": 66})[0]
        m.eval()
        T = 20
        x = torch.randint(0, 66, (1, T))
        with torch.no_grad():
            r = m.forward(x)
            logits = r[0] if isinstance(r, (tuple, list)) else r
            st = m.init_state(1, "cpu", torch.float32)
            outs = []
            for i in range(T):
                ro, st = m.step(x[:, i:i + 1], st)
                outs.append(ro[0] if isinstance(ro, (tuple, list)) else ro)
            stacked = torch.cat(outs, dim=1)
        d = (logits - stacked).abs().max().item()
        assert d <= 1e-4, (fam, d)


def test_as7_head_honesty_ledger_viewer_docs():
    """Ledger green, toy honesty tags, viewer hardening, no em dashes."""
    ledger = REPO / "postformer/ledger/ledger.csv"
    rows = list(csv.DictReader(open(ledger)))
    assert len(rows) >= 25, len(rows)
    r = _run("postformer.harness.ledger", "check", "--ledger", str(ledger))
    assert r.returncode == 0, r.stderr[-2000:] + r.stdout[-2000:]
    toy_rows = [x for x in rows if x["model"].endswith("-toy")]
    assert toy_rows, "no toy rows"
    for x in toy_rows:
        blob = (x["notes"] + x["model"]).lower()
        honest = ("toy" in blob or "smoke" in blob or "random init" in blob
                  or "extrapolation" in blob or "g4" in blob)
        assert honest, (x["model"], x["notes"][:80])
        assert "gate pass" not in blob and "closes" not in blob, x["model"]
    viewer = (REPO / "postformer/viewer/index.html").read_text()
    assert "splitCSV" in viewer and "esc(" in viewer
    bad = []
    import subprocess as sp
    files = sp.run(["git", "diff", "--name-only", "origin/main...HEAD"],
                   capture_output=True, text=True, cwd=str(REPO)).stdout.split()
    for f in files:
        if f.endswith((".md", ".py", ".html")):
            if "\u2014" in (REPO / f).read_text(encoding="utf-8"):
                bad.append(f)
    assert not bad, bad
