"""Tester M4ax red-team: hostile live-fire on current head (Refs #294).

Novel vs prior suites (aw pinned S-tiny code-vs-proof totals, p4 --window 0
train liveness, unknown-family/tie locks, ledger honesty sweep, --steps 1,
p2/p3 T=1; av/au/as/v/ap pinned cfg/stride/g4/parity/eval-window/determinism):
  1. S-small code state totals: p1/p4 == 7864320 (proof-pinned), p2 ==
     9043968, p3/p5 == 12582912 (hand-derived from small dims, never
     asserted before); plus cross-family relations p4==p1, p3==p5, p2>p1.
  2. Train-side --window liveness for p2/p3/p5 (p1 covered by ap, p4 by aw):
     4-step window-0 vs default trajectories must diverge, else the flag
     is a silent no-op (M2 invalidation class).
  3. P2 slot eviction fires and stays causal: SlotBuffer unit (G=2,
     stride=1, 3 writes -> writes==3, n==2 capped, read finite) plus
     full-model step/forward match at T=8 with slots=2/stride=1/window=0
     (8 writes vs 2 slots forces eviction on the compared path).
  4. P5 post-unit-norm train+eval liveness: 4-step p5-toy train finite,
     checkpoint loads, G1 mqar eval writes a summary with N8 acc in [0,1].
  5. G4 harness end-to-end + --vocab/+2 convention locks: latency_state on
     p1-toy at T=8,16 writes a curve row per length with integer
     state_bytes; a checkpoint trained at vocab64 evaluated with a
     mismatched --vocab fails loudly pinning both sides.
  6. Ledger ablation-column locks: slots/use_accumulator columns present;
     every model name canonical; p2 rows carry slots, p3 rows carry
     use_accumulator, all other families leave both empty.
"""
import csv
import glob
import json
import os

import torch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
LEDGER = os.path.join(REPO_ROOT, "postformer", "ledger", "ledger.csv")
PROOF = os.path.join(REPO_ROOT, "postformer", "docs", "proof-g4.md")

# Hand-derived S-small pins (H=6, dk=dv=128, W=128, win 4x64 -> wd 256,
# e=4 fp32, 12 layers):
#   P1/P4 per layer: 6*128*128*4=393216 + 2*128*256*4=262144 = 655360
#   P2 per layer: 393216 + 16*6*256*4=98304 + 262144 = 753664
#   P3/P5 per layer: 2*393216 + 262144 = 1048576
SMALL_PINS = {"p1": 7864320, "p2": 9043968, "p3": 12582912,
              "p4": 7864320, "p5": 12582912}


def _train(model, out, seed, steps=4, extra=()):
    from postformer.harness.train import main as train_main
    os.makedirs(out, exist_ok=True)
    train_main(["--model", model, "--data", "mqar", "--vocab", "64",
                "--n-pairs", "8", "--steps", str(steps), "--batch", "2",
                "--seed", str(seed), "--out", out,
                "--log-every", str(steps)] + list(extra))
    with open(os.path.join(out, "train_summary.json")) as f:
        return json.load(f)


def test_ax1_small_state_totals_exact_and_relations():
    """S-small code totals equal hand-derived pins; relations hold."""
    from postformer.models.factory import build_model
    with open(PROOF) as f:
        proof = f.read()
    totals = {}
    for fam, pin in SMALL_PINS.items():
        m, _ = build_model(fam, "small", {})
        total = sum(b.state_size(4) for b in m.blocks)
        totals[fam] = total
        assert total == pin, (fam, total, pin)
    assert str(SMALL_PINS["p1"]) in proof  # proof pins small P1/P4
    assert totals["p4"] == totals["p1"]  # identical inventory by construction
    assert totals["p3"] == totals["p5"]  # 2x trunk + window both
    assert totals["p2"] > totals["p1"]  # slots add state
    assert totals["p3"] > totals["p2"]  # full 2x trunk beats G16 slots


def test_ax2_window0_train_trajectory_differs_p2_p3_p5(tmp_path):
    """--window 0 changes the train trajectory for p2/p3/p5 (not ignored)."""
    for fam in ["p2", "p3", "p5"]:
        s0 = _train(f"{fam}-toy", str(tmp_path / f"{fam}-w0"), 11,
                    extra=("--window", "0"))
        s1 = _train(f"{fam}-toy", str(tmp_path / f"{fam}-wdef"), 11)
        for s in (s0, s1):
            assert s["final_loss"] == s["final_loss"], (fam, s)
            assert s["final_loss"] != float("inf"), (fam, s)
        assert s0["final_loss"] != s1["final_loss"], (fam, s0, s1)


def test_ax3_p2_eviction_fires_and_stays_causal():
    """Slot eviction caps at G and step/forward still match past eviction."""
    from postformer.models.p2_slots import SlotBuffer
    buf = SlotBuffer(1, 2, 32, 32, slots=2, stride=1,
                     device="cpu", dtype=torch.float32)
    k = torch.randn(1, 2, 32)
    v = torch.randn(1, 2, 32)
    for _ in range(3):
        buf.append(k, v)
    assert buf.writes == 3, buf.writes
    assert buf.n == 2, buf.n  # capped at G: eviction fired
    r = buf.read(torch.randn(1, 2, 32))
    assert r is not None and torch.isfinite(r).all()

    from postformer.models.factory import build_model
    m, _ = build_model("p2", "toy", {"vocab_size": 66, "slots": 2,
                                     "slot_stride": 1, "window": 0})
    m.eval()
    with torch.no_grad():
        ids = torch.randint(0, 66, (1, 8))
        ref = m(ids)
        st = m.init_state(1, "cpu", torch.float32)
        outs = []
        for i in range(8):
            o, st = m.step(ids[:, i:i + 1], st)
            outs.append(o)
        got = torch.cat(outs, dim=1)
        assert torch.isfinite(got).all()
        d = (ref - got).abs().max().item()
        assert d <= 1e-4, d
        assert st[0]["buf"].writes == 8, st[0]["buf"].writes
        assert st[0]["buf"].n == 2, st[0]["buf"].n


def test_ax4_p5_post_unitnorm_train_eval_liveness(tmp_path):
    """P5 trains finite post-unit-norm and evals to a valid G1 summary."""
    from postformer.harness.synthetic_recall import main as eval_main
    out = str(tmp_path / "p5train")
    s = _train("p5-toy", out, 5)
    assert s["final_loss"] == s["final_loss"] and s["final_loss"] != float("inf")
    ckpt = os.path.join(out, "checkpoint.pt")
    assert os.path.exists(ckpt)
    eout = str(tmp_path / "p5eval")
    os.makedirs(eout, exist_ok=True)
    eval_main(["--model", "p5-toy", "--checkpoint", ckpt, "--vocab", "64",
               "--n-pairs", "8", "--episodes", "4", "--task", "mqar",
               "--seed", "5", "--out", eout])
    paths = glob.glob(os.path.join(eout, "g1_summary_seed*.json"))
    assert len(paths) == 1, paths
    with open(paths[0]) as f:
        summary = json.load(f)
    acc = summary["mqar"]["8"]["acc"]
    assert 0.0 <= acc <= 1.0, acc


def test_ax5_latency_state_curve_and_vocab_mismatch_lock(tmp_path):
    """G4 bench writes per-length rows; ckpt --vocab mismatch fails loudly."""
    from postformer.harness.latency_state import main as bench_main
    out = str(tmp_path / "g4")
    os.makedirs(out, exist_ok=True)
    bench_main(["--model", "p1-toy", "--lengths", "8,16", "--decode-steps",
                "1", "--warmup", "0", "--batch-size", "1", "--vocab", "64",
                "--seed", "0", "--out", out])
    curves = glob.glob(os.path.join(out, "*.csv"))
    assert curves, os.listdir(out)
    with open(curves[0]) as f:
        rows = list(csv.DictReader(f))
    assert {r["T"] for r in rows} == {"8", "16"}, rows
    for r in rows:
        assert int(r["state_bytes"]) > 0, r
        assert float(r["ms_per_token_median"]) >= 0, r

    tout = str(tmp_path / "mism")
    s = _train("p1-toy", tout, 9)
    assert s["final_loss"] == s["final_loss"]
    try:
        bench_main(["--model", "p1-toy", "--checkpoint",
                    os.path.join(tout, "checkpoint.pt"), "--lengths", "8",
                    "--decode-steps", "1", "--warmup", "0", "--vocab", "999",
                    "--seed", "0", "--out", str(tmp_path / "mism2")])
    except SystemExit as e:
        msg = str(e)
        assert "66" in msg and "1001" in msg, msg  # both sides pinned
    else:
        raise AssertionError("vocab-mismatched checkpoint silently accepted")


def test_ax6_ledger_ablation_column_locks():
    """slots/use_accumulator columns exist and agree with the family."""
    with open(LEDGER, newline="") as f:
        rdr = csv.DictReader(f)
        assert "slots" in rdr.fieldnames, rdr.fieldnames
        assert "use_accumulator" in rdr.fieldnames, rdr.fieldnames
        rows = list(rdr)
    assert len(rows) >= 25, len(rows)
    import re
    name_re = re.compile(r"(p1|p2|p3|p4|p5|transformer)-(toy|tiny|small)")
    for r in rows:
        assert name_re.fullmatch(r["model"]), r["model"]
        fam = r["model"].split("-")[0]
        slots, acc = r.get("slots") or "", r.get("use_accumulator") or ""
        if fam == "p2":
            assert slots != "", r
            assert acc == "", r
        elif fam == "p3":
            assert acc in ("True", "False"), r
            assert slots == "", r
        else:
            assert slots == "" and acc == "", r
