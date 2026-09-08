"""Tester M4g red-team: hostile verification of the M4e toy envelope audit.

Refs #294 (toy proxies only, never gate results). M4e is docs-only: it
freezes every CPU-feasible toy probe into postformer/docs/envelope-audit.md
plus a viewer banner link and README updates. Docs can lie quietly, so this
suite recomputes every audit scoreboard cell from ledger.csv (never trusting
the markdown alone), re-derives the M2b 3-seed means, pins the A4/A6 audit
claims against raw curves, replicates the viewer's RFC-4180 splitCSV in
Python over the live 24-col ledger, and enforces Refs discipline. If any of
these fail, the audit narrative is fabrication and the PR goes to the Fixer.
"""

import csv
import json
import math
import os
import re

import pytest

from postformer.harness.ledger import main as ledger_main

REPO = os.path.join(os.path.dirname(__file__), "..")
LEDGER = os.path.join(REPO, "ledger", "ledger.csv")
AUDIT = os.path.join(REPO, "docs", "envelope-audit.md")
VIEWER = os.path.join(REPO, "viewer", "index.html")
A6 = os.path.join(REPO, "ledger", "curves", "a6-toy")


def _rows():
    with open(LEDGER) as f:
        return list(csv.DictReader(f))


def _mean(rows, key):
    return sum(float(r[key]) for r in rows) / len(rows)


def test_m4g_m2b_means_recompute_from_ledger():
    """M2b 3-seed means in the audit must recompute from ledger rows."""
    rows = _rows()
    p1 = [r for r in rows if r["model"] == "p1-toy" and r["vocab"] == "64"
          and r["train_tokens"] == "1584000" and r["window"] == "16"]
    p5 = [r for r in rows if r["model"] == "p5-toy" and r["vocab"] == "64"
          and r["train_tokens"] == "1584000" and r["window"] == "16"]
    tr = [r for r in rows if r["model"] == "transformer-toy"
          and r["vocab"] == "64" and r["train_tokens"] == "1584000"]
    assert len(p1) == 3 and len(p5) == 3 and len(tr) == 3, (
        len(p1), len(p5), len(tr))
    assert _mean(tr, "g1_mqar_8") == pytest.approx(0.146, abs=1e-3)
    assert _mean(tr, "g1_mqar_16") == pytest.approx(0.091, abs=1e-3)
    assert _mean(tr, "g1_2hop") == pytest.approx(0.12, abs=5e-3)
    assert _mean(p1, "g1_mqar_8") == pytest.approx(0.287, abs=1e-3)
    assert _mean(p1, "g1_mqar_16") == pytest.approx(0.039, abs=1e-3)
    assert _mean(p1, "g1_2hop") == pytest.approx(0.46, abs=5e-3)
    assert _mean(p5, "g1_mqar_8") == pytest.approx(0.300, abs=1e-3)
    assert _mean(p5, "g1_mqar_16") == pytest.approx(0.0, abs=1e-9)
    assert _mean(p5, "g1_2hop") == pytest.approx(0.53, abs=5e-3)


def test_m4g_single_arm_cells_match_ledger():
    """Audit single-arm cells (p2/p3/p4/A4/A6) must equal ledger cells."""
    rows = _rows()
    by_model = {}
    for r in rows:
        by_model.setdefault((r["model"], r["vocab"]), []).append(r)
    p2 = by_model[("p2-toy", "64")][0]
    assert float(p2["g1_mqar_8"]) == pytest.approx(0.0825, abs=1e-9)
    assert float(p2["g1_2hop"]) == pytest.approx(0.03, abs=1e-9)
    p3 = by_model[("p3-toy", "64")][0]
    assert float(p3["g1_mqar_8"]) == pytest.approx(0.0600, abs=1e-9)
    noacc = by_model[("p3-noacc-toy", "64")][0]
    assert float(noacc["g1_mqar_8"]) == pytest.approx(0.06125, abs=1e-9)
    p4 = by_model[("p4-toy", "64")][0]
    assert float(p4["g1_mqar_8"]) == pytest.approx(0.035, abs=1e-9)
    assert float(p4["g1_mqar_16"]) == pytest.approx(1 / 64, abs=1e-9)
    g0 = by_model[("p2-G0-toy", "64")][0]
    g4 = by_model[("p2-G4-toy", "64")][0]
    g64 = by_model[("p2-G64-toy", "64")][0]
    assert float(g0["g1_mqar_8"]) == pytest.approx(0.04625, abs=1e-9)
    assert float(g4["g1_mqar_8"]) == pytest.approx(0.0825, abs=1e-9)
    assert float(g64["g1_mqar_8"]) == pytest.approx(0.0825, abs=1e-9)
    assert float(g0["g1_mqar_8"]) < float(g4["g1_mqar_8"])
    for m in ("p1-toy", "transformer-toy"):
        v512 = by_model[(m, "512")][0]
        assert float(v512["g1_mqar_8"]) == 0.0
        assert float(v512["g1_mqar_16"]) == 0.0
        assert float(v512["g1_2hop"]) == 0.0


def test_m4g_h4_negative_read_is_honest():
    """H4 NEGATIVE claim: p4 below matched p1-ref and p2 must hold."""
    rows = _rows()
    p4 = [r for r in rows if r["model"] == "p4-toy"][0]
    p2 = [r for r in rows if r["model"] == "p2-toy"][0]
    assert float(p4["g1_mqar_8"]) < float(p2["g1_mqar_8"])
    assert float(p4["g1_mqar_8"]) < 0.0625  # M3 p1-W16-1000 matched ref


def test_m4g_a6_loss_near_chance():
    """A6 'near ln(512)' claim: both arms within 0.065 of chance loss."""
    for arm in ("p1-toy-V512-s0", "transformer-toy-V512-s0"):
        with open(os.path.join(A6, f"train_summary_{arm}.json")) as f:
            t = json.load(f)
        assert abs(t["final_loss"] - math.log(512)) < 0.065, (arm, t)


def _split_csv(line):
    out, cur, q = [], "", False
    i = 0
    while i < len(line):
        c = line[i]
        if q:
            if c == '"':
                if i + 1 < len(line) and line[i + 1] == '"':
                    cur += '"'
                    i += 1
                else:
                    q = False
            else:
                cur += c
        elif c == '"':
            q = True
        elif c == ',':
            out.append(cur)
            cur = ""
        else:
            cur += c
        i += 1
    out.append(cur)
    return out


def test_m4g_viewer_splitcsv_parses_live_ledger():
    """Viewer must ship splitCSV+escaping and it must parse the live ledger."""
    with open(VIEWER) as f:
        html = f.read()
    assert "splitCSV" in html, "viewer must use the RFC-4180 splitter"
    assert "envelope-audit.md" in html, "banner must link the audit doc"
    with open(LEDGER) as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    header = _split_csv(lines[0])
    assert len(header) == 24, len(header)
    for ln in lines[1:]:
        cells = _split_csv(ln)
        assert len(cells) == 24, (len(cells), ln[:80])
    naive = lines[1].split(",")
    assert len(naive) != 24, "notes quote check: naive split must shred"


def test_m4g_audit_refs_discipline_and_no_emdashes():
    """Audit + ideas entry: Refs kept, Closes only conditional, no em dashes."""
    ideas = os.path.normpath(os.path.join(
        REPO, "..", "ideas", "2026-09-08-postformer-m4e-envelope-audit.md"))
    for path in (AUDIT, ideas):
        with open(path) as f:
            text = f.read()
        assert "Refs #294" in text, path
        assert "\u2014" not in text, path
        for m in re.finditer(r"Closes #294", text):
            ctx = (text[max(0, m.start() - 60):m.start()]
                   + text[m.end():m.end() + 60])
            assert "only on" in ctx or "waits on" in ctx, (path, ctx)
    with open(AUDIT) as f:
        audit = f.read()
    assert "NOT gate results" in audit or "NOT measured" in audit, audit[:500]
    ledger_main(["check", "--ledger", LEDGER])
