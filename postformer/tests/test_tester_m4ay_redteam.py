"""Tester M4ay red-team: hostile live-fire on current head (Refs #294).

Novel vs all prior suites (ax pinned S-small state_size sums, p2/p3/p5
window-train liveness, P2 eviction, p5 train+eval, latency_state curve +
vocab mismatch, ablation columns; aw pinned S-tiny code-vs-proof totals,
p4 --window 0 train liveness, unknown-family/tie locks):
  1. G4 control-side lock at S-tiny via the public state_bytes API: the
     baseline must GROW exactly 32x from T=1000 to T=32000 (a flat baseline
     would make the O(1) gate vacuous), all five candidates exactly flat,
     code totals equal the proof pins (p1/p4 3145728, p2 3538944,
     p3/p5 4718592).
  2. Full measurement-chain composition on a tmp ledger copy: 8-step
     p4-toy train (seed 97) -> MQAR eval -> run-json assembled from the
     LIVE summaries -> append -> check green -> 26 rows with cells equal
     to the summary values. No prior suite runs append with live cells.
  3. Plot hardening live-fire: a crafted g4 curve with an XML-evil model
     label plus an inf point must plot without crashing, escape the label
     in SVG, and list the model in the manifest (locks the svg escaping
     and non-finite filtering fixes).
  4. Non-MQAR task-branch liveness on a trained candidate checkpoint:
     induction + copying + bind2hop evals on a p4-toy checkpoint must
     write summaries with accs in [0, 1] (ax covered mqar on p5 only).
  5. Dedup/upsert roundtrip on the 26-col schema: re-append without
     --force must fail loudly naming the duplicate; --force must upsert
     in place (still 26 rows) with updated notes.
"""
import csv
import glob
import json
import os
import shutil
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
LEDGER = os.path.join(REPO_ROOT, "postformer", "ledger", "ledger.csv")
PROOF = os.path.join(REPO_ROOT, "postformer", "docs", "proof-g4.md")


def _train(model, out, seed, steps=8):
    from postformer.harness.train import main as train_main
    os.makedirs(out, exist_ok=True)
    train_main(["--model", model, "--data", "mqar", "--vocab", "64",
                "--n-pairs", "8", "--steps", str(steps), "--batch", "2",
                "--seed", str(seed), "--out", out,
                "--log-every", str(steps)])
    with open(os.path.join(out, "train_summary.json")) as f:
        return json.load(f)


def _eval(model, ckpt, out, seed, task, episodes=8):
    from postformer.harness.synthetic_recall import main as eval_main
    os.makedirs(out, exist_ok=True)
    eval_main(["--model", model, "--checkpoint", ckpt, "--vocab", "64",
               "--n-pairs", "8", "--episodes", str(episodes),
               "--task", task, "--seed", str(seed), "--out", out])
    paths = glob.glob(os.path.join(out, "g1_summary_seed*.json"))
    assert len(paths) == 1, paths
    with open(paths[0]) as f:
        return json.load(f)


def test_ay1_baseline_grows_32x_candidates_flat_tiny():
    """Baseline state_bytes grows exactly 32x 1k->32k; candidates flat."""
    from postformer.models.factory import build_model
    with open(PROOF) as f:
        proof = f.read()
    base, _ = build_model("transformer", "tiny", {})
    b1k = base.state_bytes(1, 1000, 4)
    b32k = base.state_bytes(1, 32000, 4)
    assert (b1k, b32k) == (24576000, 786432000), (b1k, b32k)
    assert b32k == 32 * b1k  # linear control: gate is not vacuous
    pins = {"p1": 3145728, "p2": 3538944, "p3": 4718592,
            "p4": 3145728, "p5": 4718592}
    got = {}
    for fam, pin in pins.items():
        m, _ = build_model(fam, "tiny", {})
        a, b = m.state_bytes(1, 1000, 4), m.state_bytes(1, 32000, 4)
        assert a == b, (fam, a, b)  # flat in T via public API
        assert a == pin, (fam, a, pin)
        got[fam] = a
    assert got["p4"] == got["p1"]
    assert got["p3"] == got["p5"]
    for pin in (3145728, 3538944, 4718592):
        assert str(pin) in proof  # proof pins match code totals


def test_ay2_measure_chain_append_live_cells_check_green(tmp_path):
    """Train -> eval -> append(live cells) -> check green on tmp copy."""
    from postformer.harness.ledger import main as ledger_main
    tout = str(tmp_path / "chain-train")
    s = _train("p4-toy", tout, 97)
    assert s["final_loss"] == s["final_loss"]
    assert s["final_loss"] != float("inf")
    ckpt = os.path.join(tout, "checkpoint.pt")
    assert os.path.exists(ckpt)
    eout = str(tmp_path / "chain-eval")
    g = _eval("p4-toy", ckpt, eout, 97, "mqar")
    acc = g["mqar"]["8"]["acc"]
    assert 0.0 <= acc <= 1.0, acc
    lp = str(tmp_path / "ledger.csv")
    shutil.copy(LEDGER, lp)
    run = {"model": "p4-toy", "params": s["params_no_embed"],
           "train_tokens": s["train_tokens"], "seed": 97, "vocab": 64,
           "window": 16, "slots": "", "use_accumulator": "",
           "g1_mqar_8": acc, "g1_mqar_16": "", "g1_mqar_64": "",
           "g1_mqar_256": "", "g1_induction": "", "g1_copy": "",
           "g1_2hop": "", "g2_bpb_1x": "", "g2_bpb_4x": "", "g2_bpb_8x": "",
           "g2_delta_4x": "", "g2_delta_8x": "", "g3_valid_bpb": "",
           "g3_test_bpb": "", "g4_state_bytes": "", "g4_ms_per_token": "",
           "gpu_hours": 0,
           "notes": "tester M4ay probe: live p4-toy seed97 chain, "
                    "toy result NOT a gate result (Refs #294)"}
    rp = str(tmp_path / "run.json")
    with open(rp, "w") as f:
        json.dump(run, f)
    ledger_main(["append", "--run-json", rp, "--ledger", lp])
    ledger_main(["check", "--ledger", lp])
    with open(lp, newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 26, len(rows)  # 25 committed + 1 probe
    last = rows[-1]
    assert last["model"] == "p4-toy" and last["seed"] == "97", last
    assert float(last["g1_mqar_8"]) == acc, (last["g1_mqar_8"], acc)
    assert int(last["train_tokens"]) == s["train_tokens"]
    assert int(last["params"]) == s["params_no_embed"]


def test_ay3_plot_escapes_evil_label_skips_inf(tmp_path):
    """Crafted curve with evil label + inf point plots escaped, no crash."""
    from postformer.harness.ledger import main as ledger_main
    lp = str(tmp_path / "ledger.csv")
    shutil.copy(LEDGER, lp)
    cd = str(tmp_path / "curves")
    os.makedirs(cd)
    with open(os.path.join(cd, "g4_curve_evil.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "T", "state_bytes", "ms_per_token_median"])
        w.writerow(["p1-toy <evil>&", 8, 24576, 0.5])
        w.writerow(["p1-toy <evil>&", 16, 24576, 0.6])
        w.writerow(["p1-toy <evil>&", 32, "inf", 0.7])
    out = str(tmp_path / "plots")
    ledger_main(["plot", "--ledger", lp, "--out-dir", out,
                 "--curves-dir", cd])
    svg = open(os.path.join(out, "g4_state_bytes.svg")).read()
    assert "&lt;evil&gt;" in svg  # label escaped
    assert "<evil>" not in svg  # no raw injection
    assert "&amp;" in svg
    man = json.load(open(os.path.join(out, "manifest.json")))
    assert man["g4_models"] == ["p1-toy <evil>&"], man
    assert os.path.exists(os.path.join(out, "g4_ms_per_token.svg"))


def test_ay4_nontask_evals_live_on_trained_p4(tmp_path):
    """Induction/copying/bind2hop evals work on a trained p4 checkpoint."""
    tout = str(tmp_path / "p4train")
    s = _train("p4-toy", tout, 98, steps=4)
    assert s["final_loss"] == s["final_loss"]
    ckpt = os.path.join(tout, "checkpoint.pt")
    for task, key in [("induction", "induction"), ("copying", "copying"),
                      ("bind2hop", "bind2hop")]:
        g = _eval("p4-toy", ckpt, str(tmp_path / f"p4-{task}"), 98,
                  task, episodes=4)
        assert key in g, (task, sorted(g.keys()))
        if key == "bind2hop":
            assert 0.0 <= g[key]["acc"] <= 1.0, g[key]
        else:
            for n, v in g[key].items():
                assert 0.0 <= v <= 1.0, (task, n, v)


def test_ay5_dup_reject_then_force_upsert_tmp_copy(tmp_path):
    """Re-append without --force fails; --force upserts in place."""
    from postformer.harness.ledger import main as ledger_main
    lp = str(tmp_path / "ledger.csv")
    shutil.copy(LEDGER, lp)
    run = {"model": "p5-toy", "params": 336332, "train_tokens": 528,
           "seed": 97, "vocab": 64, "window": 16, "slots": "",
           "use_accumulator": "", "g1_mqar_8": 0.0, "g1_mqar_16": "",
           "g1_mqar_64": "", "g1_mqar_256": "", "g1_induction": "",
           "g1_copy": "", "g1_2hop": "", "g2_bpb_1x": "", "g2_bpb_4x": "",
           "g2_bpb_8x": "", "g2_delta_4x": "", "g2_delta_8x": "",
           "g3_valid_bpb": "", "g3_test_bpb": "", "g4_state_bytes": "",
           "g4_ms_per_token": "", "gpu_hours": 0,
           "notes": "tester M4ay probe v1 (Refs #294)"}
    rp = str(tmp_path / "run.json")
    with open(rp, "w") as f:
        json.dump(run, f)
    ledger_main(["append", "--run-json", rp, "--ledger", lp])
    try:
        ledger_main(["append", "--run-json", rp, "--ledger", lp])
    except SystemExit as e:
        assert "duplicate" in str(e).lower(), e
    else:
        raise AssertionError("duplicate re-append silently accepted")
    run["notes"] = "tester M4ay probe v2 upserted (Refs #294)"
    with open(rp, "w") as f:
        json.dump(run, f)
    ledger_main(["append", "--run-json", rp, "--ledger", lp, "--force"])
    ledger_main(["check", "--ledger", lp])
    with open(lp, newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 26, len(rows)  # upsert, not a second row
    assert rows[-1]["notes"] == run["notes"], rows[-1]["notes"]
