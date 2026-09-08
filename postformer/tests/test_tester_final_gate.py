"""Tester final-gate hostile suite at current head (post-M4ah).

Refs #294 (toy/MINI-scale proxies only, never gate results).

Consolidates the release-blocking invariants live at this exact commit:
(F1) binding-gate discipline repo-wide - every "Closes #294" occurrence in
shipped docs/progress/ideas must be conditional ("only on/when ..."), never
a premature close claim; (F2) family-wide param parity within 2% at
toy/tiny/small via live count_params; (F3) ledger strictness - dup append
rejected, NaN row rejected, garbage header rejected loudly, live check
green on 25 rows; (F4) train CLI guards reject steps/batch/log_every = 0;
(F5) viewer CSV hardening present (splitCSV + escaping); (F6) P4 live
hostile probes - determinism, T=1 forward, eta bounds, step/forward across
the W boundary; (F7) lab formatting - zero em dashes in issue docs; (F8) no
eval/exec/input() in shipped postformer code.
"""

import csv
import os
import re
import subprocess

import pytest
import torch

from postformer.harness.ledger import main as ledger_main
from postformer.models.factory import build_model, count_params

REPO = os.path.join(os.path.dirname(__file__), "..", "..")
POSTFORMER = os.path.join(REPO, "postformer")
LEDGER = os.path.join(POSTFORMER, "ledger", "ledger.csv")
VIEWER = os.path.join(POSTFORMER, "viewer", "index.html")

CANDIDATES = ["p1", "p2", "p3", "p4", "p5"]
CONDITIONAL = ("only on", "only when", "only if", "if g1", "unless",
               "all four gates pass", "full pass", "reproducible numbers",
               "waits on", "until", "pending")


def _ledger_rows():
    with open(LEDGER) as f:
        return list(csv.DictReader(f))


def test_f1_closes_always_conditional():
    """F1: no premature close claim anywhere in shipped docs."""
    roots = [os.path.join(REPO, "ideas"), os.path.join(REPO, "progress"),
             os.path.join(REPO, "docs"), POSTFORMER]
    hits = []
    for root in roots:
        for dp, _, fns in os.walk(root):
            norm = dp.replace("\\", "/")
            if "__pycache__" in dp or norm.endswith("/tests"):
                # Test files assert the discipline and necessarily mention
                # the string (self-pins); gate the shipped content instead.
                continue
            for fn in fns:
                if fn.endswith((".pyc", ".svg", ".csv")):
                    continue
                p = os.path.join(dp, fn)
                try:
                    text = open(p, encoding="utf-8", errors="strict").read()
                except (UnicodeDecodeError, OSError):
                    continue
                lines = text.splitlines()
                for idx, ln in enumerate(lines):
                    if "Closes #294" in ln:
                        # The gating clause may sit on the next line
                        # ("...use `Closes #294`\nONLY when all four gates...").
                        window = (ln + " " + lines[idx + 1]
                                  if idx + 1 < len(lines) else ln).lower()
                        assert any(c in window for c in CONDITIONAL), (p, ln)
                        hits.append((p, ln))
    assert hits, "expected at least one conditional Closes reference"


def test_f2_parity_all_families_all_scales():
    """F2: every candidate within 2% of baseline at toy/tiny/small."""
    for scale in ("toy", "tiny", "small"):
        base, _ = count_params("transformer", scale, None)
        assert base > 0, scale
        for fam in CANDIDATES:
            n, _ = count_params(fam, scale, None)
            assert abs(n - base) / base <= 0.02, (fam, scale, n, base)


def test_f3a_ledger_check_green_25_rows():
    """F3a: live ledger check passes on the 25-row ledger."""
    ledger_main(["check", "--ledger", LEDGER])
    assert len(_ledger_rows()) == 25


def test_f3b_ledger_rejects_dupe_nan_garbage(tmp_path):
    """F3b: dupes/NaN/garbage are rejected loudly, never pass silently."""
    import json
    import shutil
    work = str(tmp_path / "ledger.csv")
    shutil.copy(LEDGER, work)
    rows = _ledger_rows()
    # Dupe: re-append an existing row's run-json must fail without --force.
    probe = {"model": rows[0]["model"], "seed": int(rows[0]["seed"] or 0),
             "params_no_embed": int(rows[0]["params"] or 0),
             "train_tokens": int(rows[0]["train_tokens"] or 0)}
    for k in ("vocab", "window", "slots", "use_accumulator"):
        if rows[0][k] not in ("", None):
            probe[k] = rows[0][k]
    rj = str(tmp_path / "run.json")
    json.dump(probe, open(rj, "w"))
    with pytest.raises(SystemExit):
        ledger_main(["append", "--run-json", rj, "--ledger", work])
    # NaN gate cell must fail check loudly.
    bad = str(tmp_path / "nan.csv")
    shutil.copy(LEDGER, bad)
    with open(bad, "a") as f:
        f.write("p1-toy,100,100,9,64,16,,,nan,,,,,,,,,,,,,,,,,,probe nan\n")
    with pytest.raises(SystemExit):
        ledger_main(["check", "--ledger", bad])
    # Garbage header must fail loudly (SystemExit or KeyError), never pass.
    gar = str(tmp_path / "garbage.csv")
    with open(gar, "w") as f:
        f.write("foo,bar,baz\n1,2,3\n")
    with pytest.raises((SystemExit, KeyError)):
        ledger_main(["check", "--ledger", gar])


def test_f4_train_guards_reject_degenerate():
    """F4: steps/batch/log_every = 0 must be rejected, not hang/crash."""
    from postformer.harness.train import main as train_main
    base = ["--model", "p1-toy", "--data", "mqar", "--steps", "4",
            "--batch", "2", "--seed", "0"]
    with pytest.raises(SystemExit):
        train_main(base + ["--steps", "0"])
    with pytest.raises(SystemExit):
        train_main(base + ["--batch", "0"])
    with pytest.raises(SystemExit):
        train_main(base + ["--log-every", "0"])


def test_f5_viewer_csv_hardening():
    """F5: viewer parses CSV quote-aware and escapes cells."""
    text = open(VIEWER).read()
    assert "splitCSV" in text
    # Strip // comments (which document the naive split as the bug being
    # fixed) and assert no live code path still uses a naive split.
    code = "\n".join(ln for ln in text.splitlines()
                     if ln.strip() and not ln.strip().startswith(("//", "*")))
    assert 'split(",")' not in code and "split(',')" not in code
    assert "splitCSV(lines[0])" in code or "splitCSV(l" in code
    assert re.search(r"escape|esc\(|&amp;|textContent", text), "no escaping"


def test_f6_p4_hostile_live():
    """F6: P4 determinism, T=1, eta bounds, step/forward across W edge."""
    torch.manual_seed(0)
    m, _ = build_model("p4", "toy", None)
    m.eval()
    with torch.no_grad():
        x = torch.randint(0, 66, (1, 1))
        assert torch.isfinite(m.forward(x)).all()  # T=1 single token
        xa = torch.randint(0, 66, (1, 8))
        assert torch.equal(m.forward(xa), m.forward(xa))  # deterministic
        T, W = 40, 16
        xb = torch.randint(0, 66, (1, T))
        logits = m.forward(xb)
        st = m.init_state(1, "cpu", torch.float32)
        outs = []
        for i in range(T):
            o, st = m.step(xb[:, i:i + 1], st)
            outs.append(o)
        d = (logits - torch.cat(outs, dim=1)).abs().max().item()
        assert d <= 1e-4, (W, d)
    # Eta band: beta in [BETA_MIN, BETA_MAX] x surprise in [0.01, 0.99].
    import postformer.models.p4_maglite as p4m
    from postformer.models.p1_delta_hybrid import BETA_MAX, BETA_MIN
    src = open(p4m.__file__).read()
    assert "eta = beta * surprise" in src
    assert ".clamp(0.01, 0.99)" in src  # surprise clamp
    assert BETA_MIN == 0.01 and BETA_MAX == 0.99
    assert BETA_MIN * 0.01 == pytest.approx(0.0001)  # eta floor
    assert BETA_MAX * 0.99 == pytest.approx(0.9801)  # eta ceiling


def test_f7_no_em_dashes_in_issue_docs():
    """F7: lab formatting rule - zero U+2014 in this PR's own docs.

    Scoped to files this PR owns (postformer/, issue-294 research, the
    postformer/post-transformer ideas entries, progress/294-). Pre-existing
    files from unrelated issues are out of scope for this gate.
    """
    owned_dirs = [POSTFORMER, os.path.join(REPO, "docs", "research"),
                  os.path.join(REPO, "progress")]
    owned_ideas = [fn for fn in os.listdir(os.path.join(REPO, "ideas"))
                   if "postformer" in fn or "post-transformer" in fn]
    targets = []
    for root in owned_dirs:
        for dp, _, fns in os.walk(root):
            if "__pycache__" in dp:
                continue
            for fn in fns:
                if fn.endswith((".md", ".py", ".html")) and "294" in dp + fn \
                        or root == POSTFORMER and fn.endswith((".md", ".py", ".html")):
                    targets.append(os.path.join(dp, fn))
    for fn in owned_ideas:
        targets.append(os.path.join(REPO, "ideas", fn))
    assert targets
    for p in targets:
        assert "\u2014" not in open(p, encoding="utf-8").read(), p


def test_f8_no_dangerous_builtins_in_shipped_code():
    """F8: no eval(/exec(/input(/__import__ in shipped code (model.eval ok)."""
    bad = re.compile(r"(?<![\w.])eval\s*\(|(?<![\w.])exec\s*\("
                     r"|(?<![\w.])input\s*\(|__import__")
    offenders = []
    for dp, _, fns in os.walk(POSTFORMER):
        if "__pycache__" in dp or "/tests" in dp.replace("\\", "/"):
            continue
        for fn in fns:
            if not fn.endswith(".py"):
                continue
            p = os.path.join(dp, fn)
            for i, ln in enumerate(open(p).read().splitlines(), 1):
                if bad.search(ln):
                    offenders.append(f"{p}:{i}:{ln.strip()}")
    assert not offenders, offenders
