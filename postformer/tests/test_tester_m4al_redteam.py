"""Tester M4al red-team: live-fire the four newest fixer hardenings (Refs #294).

Novel vs prior suites (M4ak covered train/eval rejection paths and ledger
dedup): this suite attacks the exact lines changed by fixer commits
4150d25d / 71ed56f7 / 0877c574 / 9a80dd26 on top of M4ak:
  1. ledger append must REFUSE non-default P2 slot_stride (stride changes
     slot math invisibly to the dedup key, so ledgering it would silently
     collide with the stride-8 row),
  2. ledger append must REFUSE extra run-json keys (was a printed note,
     now a loud SystemExit; silent key-drop would lose provenance),
  3. ledger validation must reject non-finite (NaN/inf) key columns
     (seed/vocab/train_tokens/gpu_hours) - both via _validate_row and via
     a live `check` on a crafted ledger file,
  4. length_sweep discovered-vocab path must refuse a baseline checkpoint
     whose train vocab disagrees with the candidate's (would force the
     wrong vocab onto the baseline embeddings), and must run end-to-end
     when the vocabs agree,
  5. A2-re W32 note precision pin (0.05125, the 4150d25d data fix).
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

import torch

REPO = Path(__file__).resolve().parents[2]
LEDGER_MOD = "postformer.harness.ledger"
SWEEP_MOD = "postformer.harness.length_sweep"


def run_cli(*args, timeout=600):
    return subprocess.run(
        [sys.executable, "-m"] + list(args),
        capture_output=True, text=True, timeout=timeout, cwd=str(REPO),
    )


def base_run(**over):
    """Minimal valid run-json row (one gate cell + probe notes tag)."""
    row = {"model": "p1-toy", "params": "336332", "train_tokens": "528000",
           "seed": "0", "vocab": "66", "window": "16", "slots": "",
           "use_accumulator": "", "g1_mqar_8": "0.05",
           "notes": "probe row for al-suite"}
    row.update(over)
    return row


def write_run(tmp_path, name, **over):
    p = tmp_path / name
    p.write_text(json.dumps(base_run(**over)))
    return str(p)


# --- 1. slot_stride guard (fixer 0877c574) ---

def test_al1_append_rejects_nondefault_stride(tmp_path):
    """slot_stride 4 (or '2') must fail loudly, never silently collide."""
    for stride in (4, "2", 16):
        rp = write_run(tmp_path, f"run_s{stride}.json", slot_stride=stride)
        lp = str(tmp_path / f"led_s{stride}.csv")
        r = run_cli(LEDGER_MOD, "append", "--run-json", rp, "--ledger", lp)
        assert r.returncode != 0, f"stride={stride!r} must be refused"
        assert "slot_stride" in (r.stdout + r.stderr), r.stdout[-500:]


def test_al2_append_accepts_default_stride(tmp_path):
    """stride 8 / '8' / '' / absent must pass (and slot_stride itself must
    not trip the extra-key guard)."""
    for seed, (tag, stride) in enumerate((("i8", 8), ("s8", "8"), ("empty", "")),
                                         start=10):
        rp = write_run(tmp_path, f"run_ok{tag}.json", slot_stride=stride,
                       seed=str(seed))
        lp = str(tmp_path / "led_ok.csv")
        r = run_cli(LEDGER_MOD, "append", "--run-json", rp, "--ledger", lp)
        assert r.returncode == 0, (tag, r.stdout[-800:] + r.stderr[-800:])
    rp = write_run(tmp_path, "run_nokey.json", seed="99")
    r = run_cli(LEDGER_MOD, "append", "--run-json", rp,
                "--ledger", str(tmp_path / "led_ok2.csv"))
    assert r.returncode == 0, r.stdout[-800:] + r.stderr[-800:]


# --- 2. extra-key refusal (fixer 0877c574) ---

def test_al3_append_rejects_extra_keys(tmp_path):
    """Unknown run-json keys must fail loudly (was a printed note)."""
    rp = write_run(tmp_path, "run_extra.json", bogus_key=1)
    r = run_cli(LEDGER_MOD, "append", "--run-json", rp,
                "--ledger", str(tmp_path / "led_extra.csv"))
    assert r.returncode != 0, "extra keys must be refused"
    assert "bogus_key" in (r.stdout + r.stderr), r.stdout[-500:]


# --- 3. non-finite key columns (fixer 0877c574) ---

def test_al4_validate_rejects_nonfinite_key_cols():
    """seed/vocab/train_tokens/gpu_hours NaN/inf must each yield errors."""
    from postformer.harness.ledger import _validate_row, SCHEMA
    clean = {c: "" for c in SCHEMA}
    clean.update({"model": "p1-toy", "seed": "0", "g1_mqar_8": "0.05",
                  "notes": "probe"})
    assert _validate_row(0, dict(clean)) == []
    for col, bad in (("seed", "nan"), ("seed", "inf"),
                     ("vocab", "inf"), ("vocab", "-inf"),
                     ("train_tokens", "nan"), ("gpu_hours", "inf")):
        row = dict(clean)
        row[col] = bad
        errs = _validate_row(0, row)
        assert any("non-finite" in e and col in e for e in errs), (col, bad, errs)


def test_al5_check_rejects_nonfinite_seed_row(tmp_path):
    """A ledger file carrying inf seed must fail `check` loudly."""
    from postformer.harness.ledger import SCHEMA
    lp = tmp_path / "led_inf.csv"
    with open(lp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA)
        w.writeheader()
        row = {c: "" for c in SCHEMA}
        row.update({"model": "p1-toy", "seed": "inf", "g1_mqar_8": "0.05",
                    "notes": "probe hostile inf"})
        w.writerow(row)
    r = run_cli(LEDGER_MOD, "check", "--ledger", str(lp))
    assert r.returncode != 0, "inf seed row must fail check"
    assert "non-finite" in (r.stdout + r.stderr), r.stdout[-500:]


def test_al6_live_ledger_check_green():
    """The real 25-row ledger must stay check-green (no collateral)."""
    r = run_cli(LEDGER_MOD, "check", "--ledger",
                "postformer/ledger/ledger.csv")
    assert r.returncode == 0, r.stdout[-1500:] + r.stderr[-1500:]
    assert "ledger OK" in r.stdout


# --- 4. discovered-vocab baseline guard (fixer 9a80dd26) ---

def _save_ckpt(path, family, scale="toy"):
    from postformer.models.factory import build_model
    m, cfg = build_model(family, scale, None)
    torch.save({"state_dict": m.state_dict(), "config": cfg}, str(path))
    return cfg["vocab_size"]


def test_al7_sweep_rejects_discovered_vocab_mismatch(tmp_path):
    """Candidate vocab 66 vs baseline ckpt vocab 8192 must fail loudly
    on the discovered path (no --vocab), before any eval runs."""
    cand = tmp_path / "cand.pt"
    _save_ckpt(cand, "p1")
    bad = tmp_path / "badbase.pt"
    torch.save({"config": {"vocab_size": 8192}}, str(bad))
    r = run_cli(SWEEP_MOD, "--model", "p1-toy", "--checkpoint", str(cand),
                "--baseline-checkpoint", str(bad),
                "--t-train", "16", "--lengths", "16",
                "--seed", "0", "--out", str(tmp_path / "o_bad"))
    assert r.returncode != 0, "vocab-mismatched baseline must be refused"
    assert "66" in (r.stdout + r.stderr) and "8192" in (r.stdout + r.stderr), \
        r.stdout[-600:] + r.stderr[-600:]


def test_al8_sweep_discovered_vocab_match_runs(tmp_path):
    """Agreeing vocabs on the discovered path must run end-to-end and
    write a finite-bpb G2 curve for both arms."""
    cand = tmp_path / "cand.pt"
    base = tmp_path / "base.pt"
    assert _save_ckpt(cand, "p1") == _save_ckpt(base, "transformer") == 66
    out = tmp_path / "o_ok"
    r = run_cli(SWEEP_MOD, "--model", "p1-toy", "--checkpoint", str(cand),
                "--baseline-checkpoint", str(base),
                "--t-train", "16", "--lengths", "16", "--stride", "8",
                "--seed", "0", "--out", str(out))
    assert r.returncode == 0, r.stdout[-1500:] + r.stderr[-1500:]
    curve = out / "g2_curve_seed0.csv"
    assert curve.exists(), "sweep must write the G2 curve"
    with open(curve) as f:
        rows = list(csv.DictReader(f))
    assert {x["model"] for x in rows} == {"p1-toy", "transformer-toy"}
    import math
    for x in rows:
        assert math.isfinite(float(x["bpb"])), x


# --- 5. A2 note precision pin (fixer 4150d25d) ---

def test_al9_a2_w32_note_precision():
    """A2-re W32 rows must carry the full-precision 0.05125 (not 0.0512)."""
    with open(REPO / "postformer/ledger/ledger.csv") as f:
        rows = list(csv.DictReader(f))
    w32 = [r for r in rows if r["model"] == "p1-toy" and r["window"] == "32"
           and "0.05125" in (r["notes"] or "")]
    assert w32, "at least one W32 row must pin mqar8 0.05125 in notes"
    for r in w32:
        assert "0.0512," not in (r["notes"] or ""), r["notes"][:120]
