"""Tester M4t hostile suite: small inventory pins, toy boundary causality, live
p4 window inheritance, model determinism, JS viewer execution, ledger
canonicity, Refs discipline.

Refs #294 (toy/tiny/small analytic checks only, never gate results).

Why this suite exists: at head 227 tests pass, but the following live
behaviors are pinned only by source-presence or not at all, so a future
edit could silently regress them:

- T1 (small inventory pins): M4s pins small P1 only; P2/P3/P4/P5 small
  footprints are unpinned. This pins all five live plus structural
  relations (P4 == P1, P3 == P5, P1 < P2 < P3) and T-flatness.
- T2 (toy cross-window causality): M4r pins tiny T=12 step/forward, but
  tiny W=128, so the window-eviction boundary is never crossed there.
  Toy W=16 is the scale where every training/eval claim lives; T=24
  crosses it. All five recurrent families must agree step-vs-forward.
- T3 (toy prefix invariance, slot/accumulator arms): existing T3 is
  MINI-scale; toy-scale with a prefix crossing W=16 for p2/p3/p4 is new.
- T4 (p4 window inheritance live): the M4a reviewer finding (p4 --window
  routing) is pinned only by source inspection. This executes the real
  load_model path on a crafted W0 p4 checkpoint.
- T5 (model determinism p2/p3/p4): harness-level T4 covers p1-tiny only.
- T6 (viewer JS executes): splitCSV/esc are pinned by source-presence;
  this runs the actual JS functions under node against the live ledger.
- T7 (ledger canonicity): every row model parses under the strict gate
  and every ablation key is unique (no silent dupes).
- T8 (Refs discipline): no commit subject on the branch claims
  Closes #294; Refs is present.
"""

import csv
import json
import os
import re
import subprocess

import pytest
import torch
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(REPO)
LEDGER = os.path.join(REPO, "ledger", "ledger.csv")
VIEWER = os.path.join(REPO, "viewer", "index.html")

SMALL_PINS = {"p1": 7864320, "p2": 9043968, "p3": 12582912,
              "p4": 7864320, "p5": 12582912}
RECURRENT = ("p1", "p2", "p3", "p4", "p5")


def test_t1_small_state_inventory_pins_and_relations():
    from postformer.models.factory import build_model
    live = {}
    for fam in RECURRENT:
        m, _ = build_model(fam, "small")
        lo, hi = m.state_bytes(1, 1024), m.state_bytes(1, 32768)
        assert lo == hi, (fam, lo, hi)
        live[fam] = lo
    assert live == SMALL_PINS, live
    assert live["p4"] == live["p1"], "P4 inventory identical to P1 by construction"
    assert live["p3"] == live["p5"], "P3 A+S is 2x, same as P5 2*d_k map"
    assert live["p1"] < live["p2"] < live["p3"], live


def test_t2_toy_cross_window_step_forward():
    from postformer.models.factory import build_model
    from postformer.models.common import seed_all
    seed_all(4401, "m4t-t2")
    T = 24
    for fam in RECURRENT:
        m, cfg = build_model(fam, "toy")
        assert m.blocks[0].window.window == 16, (fam, "toy W must be 16")
        assert T > 16, "probe must cross the eviction boundary"
        m.eval()
        x = torch.randint(0, 64, (1, T))
        with torch.no_grad():
            y_fwd = m(x)
            st = m.init_state(1, "cpu", torch.float32)
            outs = [m.step(x[:, i:i + 1], st)[0] for i in range(T)]
            y_step = torch.cat(outs, dim=1)
        assert torch.isfinite(y_fwd).all() and torch.isfinite(y_step).all(), fam
        assert (y_fwd - y_step).abs().max().item() <= 1e-4, fam


def test_t3_toy_prefix_invariance_slot_accumulator_arms():
    from postformer.models.factory import build_model
    from postformer.models.common import seed_all
    seed_all(4402, "m4t-t3")
    for fam in ("p2", "p3", "p4"):
        m, _ = build_model(fam, "toy")
        m.eval()
        pre = torch.randint(0, 64, (1, 20))
        assert pre.shape[1] > 16, "prefix must span the toy window"
        ta = torch.randint(0, 64, (1, 8))
        tb = torch.randint(0, 64, (1, 8))
        a = torch.cat([pre, ta], dim=1)
        b = torch.cat([pre, tb], dim=1)
        with torch.no_grad():
            la, lb = m(a), m(b)
        diff = (la[:, :20, :] - lb[:, :20, :]).abs().max().item()
        assert diff <= 1e-6, (fam, diff)


def test_t4_p4_window_inheritance_live(tmp_path):
    from postformer.models.factory import build_model
    from postformer.harness.util import load_model
    m, cfg = build_model("p4", "toy", {"vocab_size": 66, "window": 0})
    ckpt = str(tmp_path / "p4w0.pt")
    torch.save({"state_dict": m.state_dict(), "config": cfg}, ckpt)
    m2, cfg2, rnd = load_model("p4-toy", ckpt, None, {"vocab_size": 66},
                               "cpu", "fp32")
    assert rnd is False
    assert cfg2["window"] == 0, cfg2.get("window")
    assert m2.blocks[0].window.window == 0, "W0 checkpoint must eval as W0"
    m3, cfg3, _ = load_model("p4-toy", ckpt, None,
                             {"vocab_size": 66, "window": 16}, "cpu", "fp32")
    assert cfg3["window"] == 16, "explicit --window override stays allowed"
    assert m3.blocks[0].window.window == 16
    bad = str(tmp_path / "bad.yaml")
    with open(bad, "w") as f:
        yaml.safe_dump({"window": 16}, f)
    with pytest.raises(SystemExit):
        load_model("p4-toy", ckpt, bad, {"vocab_size": 66}, "cpu", "fp32")


def test_t5_same_seed_identical_forward_p2_p3_p4():
    from postformer.models.factory import build_model
    from postformer.models.common import seed_all
    for fam in ("p2", "p3", "p4"):
        outs = []
        for _ in range(2):
            seed_all(4403, f"m4t-t5-{fam}")
            m, _ = build_model(fam, "toy")
            m.eval()
            x = torch.randint(0, 64, (1, 10))
            with torch.no_grad():
                outs.append(m(x))
        assert torch.equal(outs[0], outs[1]), (fam, "same seed must rebuild identically")


def test_t6_viewer_js_executes_on_live_ledger(tmp_path):
    node = subprocess.run(["node", "--version"], capture_output=True, text=True)
    assert node.returncode == 0, "node required for JS execution test"
    with open(VIEWER) as f:
        src = f.read()
    m_split = re.search(r"function splitCSV\(line\) \{.*?\n\}", src, re.S)
    m_esc = re.search(r"function esc\(s\) \{.*?\n\}", src, re.S)
    assert m_split and m_esc, "splitCSV/esc must be extractable DOM-free functions"
    driver = str(tmp_path / "run.js")
    with open(driver, "w") as f:
        f.write(m_split.group(0) + "\n" + m_esc.group(0) + "\n")
        f.write("const fs = require('fs');\n")
        f.write(f"const lines = fs.readFileSync({json.dumps(LEDGER)}, 'utf8').trim().split(/\\r?\\n/);\n")
        f.write("const head = splitCSV(lines[0]);\n")
        f.write("if (head.length !== 26) { console.error('header cols ' + head.length); process.exit(1); }\n")
        f.write("let naiveBreaks = 0;\n")
        f.write("for (let i = 1; i < lines.length; i++) {\n")
        f.write("  const cells = splitCSV(lines[i]);\n")
        f.write("  if (cells.length !== 26) { console.error('row ' + i + ' cols ' + cells.length); process.exit(1); }\n")
        f.write("  if (lines[i].split(',').length !== 26) naiveBreaks++;\n")
        f.write("}\n")
        f.write("if (naiveBreaks === 0) { console.error('naive split never breaks: fix unproven'); process.exit(1); }\n")
        f.write("const probe = esc('<b>&\"\\'');\n")
        f.write("if (probe !== '&lt;b&gt;&amp;&quot;&#39;') { console.error('esc failed: ' + probe); process.exit(1); }\n")
        f.write("console.log('viewer JS OK rows=' + (lines.length - 1) + ' naiveBreaks=' + naiveBreaks);\n")
    r = subprocess.run(["node", driver], capture_output=True, text=True)
    assert r.returncode == 0, (r.stdout[-1000:], r.stderr[-1000:])
    assert "viewer JS OK rows=25" in r.stdout, r.stdout


def test_t7_ledger_models_canonical_and_keys_unique():
    from postformer.models.factory import parse_model_name
    with open(LEDGER, newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 25, len(rows)
    seen = set()
    for r in rows:
        parse_model_name(r["model"])
        key = (r["model"].strip(), r["seed"].strip(), r["vocab"].strip(),
               (r["window"] or "").strip(), (r["slots"] or "").strip(),
               (r["use_accumulator"] or "").strip())
        assert key not in seen, ("duplicate ablation key", key)
        seen.add(key)


def test_t8_refs_discipline_no_closes_in_subjects():
    r = subprocess.run(["git", "log", "--format=%s", "-200"],
                       capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr[-500:]
    subjects = r.stdout.splitlines()
    assert any("Refs #294" in s for s in subjects), "branch must carry Refs #294"
    bad = [s for s in subjects if re.search(r"closes #294", s, re.I)]
    assert not bad, ("Closes claims before all four gates pass", bad)
