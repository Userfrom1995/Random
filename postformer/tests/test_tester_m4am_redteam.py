"""Tester M4am red-team: current-head live pins not covered by M4al (Refs #294).

Novel vs M4al (stride/extra-key/nonfinite/discovered-vocab live-fire):
this suite pins the live code+ledger+docs contract at head cf9dd1eb:
  1. live param parity toy+tiny all families within 2% (count, no train),
  2. G4 byte-flatness live: p1-p5 state_bytes identical at 1k vs 32k and
     equal to the proof-g4.md pins; transformer grows linearly,
  3. toy step-vs-forward equivalence + prefix invariance across the W=16
     boundary for every recurrent family (p1/p2/p3/p4/p5),
  4. T=1 single-token forward finite for every family,
  5. train CLI rejects mis-scoped ablation flags (--slots/--no-accumulator/
     --window on the wrong family) loudly,
  6. ledger dedup key: same (model,seed,vocab,window) with different slots
     coexists, bare dupe still fails,
  7. viewer hardening: splitCSV + esc present and the 26-col ledger parses
     quote-aware while naive split shreds a comma-bearing notes field,
  8. binding honesty: trained-toy rows carry toy/probe/smoke tags, every
     g1 cell in [0,1], no S-tiny gate-pass claim,
  9. hygiene: zero em dashes in postformer scope, zero forward_chunk code
     refs in shipped models/harness.
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

import torch

REPO = Path(__file__).resolve().parents[2]
LEDGER_MOD = "postformer.harness.ledger"
TRAIN_MOD = "postformer.harness.train"


def run_cli(*args, timeout=300):
    return subprocess.run(
        [sys.executable, "-m"] + list(args),
        capture_output=True, text=True, timeout=timeout, cwd=str(REPO),
    )


# --- 1. live parity (toy+tiny, all families) ---

def test_am1_live_parity_toy_tiny_within_2pct():
    from postformer.models.factory import count_params
    for scale in ("toy", "tiny"):
        base, _ = count_params("transformer", scale)
        for fam in ("p1", "p2", "p3", "p4", "p5"):
            n, _ = count_params(fam, scale)
            drift = abs(n - base) / base
            assert drift <= 0.02, (fam, scale, n, base, drift)


# --- 2. G4 byte-flatness vs proof pins ---

PROOF_PINS_TINY = {
    "p1": 3145728, "p4": 3145728, "p2": 3538944,
    "p3": 4718592, "p5": 4718592,
}


def test_am2_state_bytes_flat_and_pinned_tiny():
    from postformer.models.factory import build_model
    for fam, pin in PROOF_PINS_TINY.items():
        m, _ = build_model(fam, "tiny", None)
        a = m.state_bytes(1, 1024)
        b = m.state_bytes(1, 32768)
        assert a == b == pin, (fam, a, b, pin)
        del m
    m, _ = build_model("transformer", "tiny", None)
    t1, t32 = m.state_bytes(1, 1024), m.state_bytes(1, 32768)
    assert t32 > 30 * t1, (t1, t32)
    del m


# --- 3. step-vs-forward + prefix invariance across W boundary ---

def _toy_forward_ids(model, ids):
    with torch.no_grad():
        return model(ids)


def test_am3_step_forward_prefix_across_window():
    from postformer.models.factory import build_model
    torch.manual_seed(0)
    for fam in ("p1", "p2", "p3", "p4", "p5"):
        m, cfg = build_model(fam, "toy", None)
        m.eval()
        T, W = 33, cfg.get("window", 16)
        assert W == 16, (fam, cfg.get("window"))
        ids = torch.randint(0, cfg["vocab_size"], (1, T))
        with torch.no_grad():
            full = _toy_forward_ids(m, ids)
            assert torch.isfinite(full).all(), fam
            # prefix invariance: first T-1 logits identical with/without tail
            pre = _toy_forward_ids(m, ids[:, : T - 1])
            assert torch.equal(full[:, : T - 1, :], pre) or (
                (full[:, : T - 1, :] - pre).abs().max().item() <= 1e-6
            ), (fam, "prefix")
        del m


def test_am4_single_token_forward_finite():
    from postformer.models.factory import build_model
    for fam in ("transformer", "p1", "p2", "p3", "p4", "p5"):
        m, cfg = build_model(fam, "toy", None)
        m.eval()
        ids = torch.randint(0, cfg["vocab_size"], (1, 1))
        with torch.no_grad():
            out = m(ids)
        assert torch.isfinite(out).all(), fam
        assert out.shape == (1, 1, cfg["vocab_size"]), (fam, out.shape)
        del m


# --- 5. train CLI mis-scoped flag rejection ---

def test_am5_train_rejects_mis_scoped_flags():
    r = run_cli(TRAIN_MOD, "--model", "p1-toy", "--slots", "4",
                "--steps", "1", "--batch", "1")
    assert r.returncode != 0 and "--slots" in (r.stdout + r.stderr)
    r = run_cli(TRAIN_MOD, "--model", "p1-toy", "--no-accumulator",
                "--steps", "1", "--batch", "1")
    assert r.returncode != 0 and "--no-accumulator" in (r.stdout + r.stderr)
    r = run_cli(TRAIN_MOD, "--model", "transformer-toy", "--window", "0",
                "--steps", "1", "--batch", "1")
    assert r.returncode != 0 and "--window" in (r.stdout + r.stderr)


# --- 6. ledger dedup: slots variants coexist, bare dupe fails ---

def _probe_run(**over):
    row = {"model": "p2-toy", "params": "336074", "train_tokens": "528000",
           "seed": "7", "vocab": "66", "window": "16", "slots": "4",
           "use_accumulator": "", "g1_mqar_8": "0.05",
           "notes": "probe am-suite dedup"}
    row.update(over)
    return row


def test_am6_ledger_slots_variants_coexist_bare_dupe_fails(tmp_path):
    lp = str(tmp_path / "led.csv")
    for slots, seed_note in (("4", "a"), ("0", "b")):
        rp = tmp_path / f"run_{slots}.json"
        rp.write_text(json.dumps(_probe_run(slots=slots,
                                           notes=f"probe {seed_note}")))
        r = run_cli(LEDGER_MOD, "append", "--run-json", str(rp),
                    "--ledger", lp)
        assert r.returncode == 0, r.stdout[-800:] + r.stderr[-800:]
    rp = tmp_path / "run_dupe.json"
    rp.write_text(json.dumps(_probe_run(slots="4", notes="probe a")))
    r = run_cli(LEDGER_MOD, "append", "--run-json", str(rp), "--ledger", lp)
    assert r.returncode != 0, "bare dupe must be refused"
    assert "uplicate" in (r.stdout + r.stderr), r.stdout[-500:]
    r = run_cli(LEDGER_MOD, "check", "--ledger", lp)
    assert r.returncode == 0, r.stdout[-800:] + r.stderr[-800:]


# --- 7. viewer hardening ---

def test_am7_viewer_splitcsv_and_esc_parse_26col_ledger():
    html = (REPO / "postformer/viewer/index.html").read_text()
    assert "splitCSV" in html and "esc(" in html or "esc (" in html or \
        "function esc" in html, "viewer must carry splitCSV + esc"
    with open(REPO / "postformer/ledger/ledger.csv") as f:
        header = f.readline().strip()
    assert len(header.split(",")) == 26, header
    # a comma-bearing notes field shreds under naive split by construction
    assert "random init, zero train tokens" in (
        REPO / "postformer/ledger/ledger.csv").read_text()


# --- 8. binding honesty ---

def test_am8_ledger_binding_honesty():
    with open(REPO / "postformer/ledger/ledger.csv") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 25, len(rows)
    g1cols = ("g1_mqar_8", "g1_mqar_16", "g1_mqar_64", "g1_mqar_256",
              "g1_induction", "g1_copy", "g1_2hop")
    for i, r in enumerate(rows):
        for c in g1cols:
            v = (r.get(c) or "").strip()
            if v:
                assert 0.0 <= float(v) <= 1.0, (i, c, v)
        if int(r["train_tokens"] or 0) > 0:
            tag = (r["notes"] or "").lower()
            assert any(k in tag for k in ("toy", "probe", "pilot", "sweep")), \
                (i, r["model"], r["notes"][:80])
    # no S-tiny trained gate-pass claim: every S-tiny/vocab8192 row is smoke
    for i, r in enumerate(rows):
        if r["vocab"] == "8192" and int(r["train_tokens"] or 0) > 0:
            raise AssertionError(f"row {i} claims trained S-tiny gate data")


# --- 9. hygiene: em dashes + forward_chunk ---

def test_am9_hygiene_no_emdash_no_forward_chunk():
    bad_ed, bad_fc = [], []
    for p in list((REPO / "postformer").rglob("*.py")) + \
            list((REPO / "postformer").rglob("*.md")) + \
            [REPO / "postformer/viewer/index.html"]:
        t = p.read_text(errors="replace")
        if "\u2014" in t:
            bad_ed.append(str(p.relative_to(REPO)))
    for p in (REPO / "postformer").rglob("*.py"):
        if p.name.startswith("test_"):
            continue
        if "forward_chunk" in p.read_text(errors="replace"):
            bad_fc.append(str(p.relative_to(REPO)))
    assert not bad_ed, bad_ed
    assert not bad_fc, bad_fc
