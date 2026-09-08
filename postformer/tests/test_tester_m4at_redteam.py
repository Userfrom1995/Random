"""Tester M4at red-team: checkpoint trust boundary, p1<->p5 silent family swap (Refs #294).

Hostile finding (proven live on this head, torch 2.14 CPU): the P1 and P5
families share identical state_dict key sets by design ("identical proj
shapes so T2 holds by construction"), and `util.load_model` loads with
`strict=False` plus a missing/unexpected-keys check that passes vacuously
for this pair. The checkpoint blob records its provenance
(`blob['args']['model']`, e.g. 'p1-toy') but `load_model` never reads it.
Result: `synthetic_recall --model p5-toy --checkpoint <p1 ckpt>` exits 0
and writes a p5-labeled summary whose weights are bit-identical to the P1
checkpoint. This is the exact M2-A2 silent-invalidation class (W0 weights
silently evaluated as W16) transposed to family: the two most-compared
arms of the headline M2 A1 falsification (P1 vs P5 MQAR) can be silently
swapped with zero warning, and every downstream ledger cell inherits the
wrong family label.

Novel vs all prior suites: no suite interrogates checkpoint provenance.
m4ak pins --config-window mismatch refusal, m4q/m4y pin ablation-flag
routing, m4af pins G1 rerun identity, but nothing stops a p1 blob from
being scored as p5. All other cross-family pairs (p1->p2/p3/p4,
transformer->p1) already fail loudly via key mismatch; only the
identical-keyset p1<->p5 pair slips through, which is precisely why it
needs a dedicated tripwire.

Failing (red) until the Fixer adds a provenance guard in `load_model`:
  AT1/AT2: wrong-family CLI eval must exit nonzero (currently exit 0).
  AT3: in-process cross-family load must raise SystemExit (currently
    returns silently with random_init False).
  AT5: wrong-family eval must either refuse or disclose true weight
    provenance in the summary (currently exits 0 with a p5 label on
    p1 weights).

Passing positive controls (lock the fix against over/under-correction):
  AT4: same-family checkpoint loads with random_init False (no over-
    rejection of the trusted path).
  AT6: scale mismatch, garbage file, and missing path all raise loudly
    today and must keep raising loudly (never degrade to silent
    random-init).
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest
import torch

from postformer.harness.util import load_model
from postformer.models.factory import build_model

REPO = Path(__file__).resolve().parents[2]


def _run(*args, timeout=300):
    return subprocess.run(
        [sys.executable, "-m"] + list(args),
        capture_output=True, text=True, timeout=timeout, cwd=str(REPO),
    )


def _train_toy_ckpt(family, seed, outdir):
    r = _run("postformer.harness.train", "--model", f"{family}-toy",
             "--data", "mqar", "--vocab", "64", "--steps", "4",
             "--batch", "2", "--seed", str(seed), "--out", str(outdir))
    assert r.returncode == 0, r.stderr[-2000:]
    ckpt = outdir / "checkpoint.pt"
    assert ckpt.exists(), "train produced no checkpoint"
    return str(ckpt)


def _blob_model(ckpt_path):
    blob = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    assert isinstance(blob, dict) and "args" in blob, "ckpt lacks provenance"
    return blob["args"]["model"]


def test_at1_p1_checkpoint_scored_as_p5_must_be_refused(tmp_path):
    """p1 weights evaluated under --model p5-toy must exit nonzero."""
    ckpt = _train_toy_ckpt("p1", 7, tmp_path / "t")
    assert _blob_model(ckpt) == "p1-toy"
    r = _run("postformer.harness.synthetic_recall", "--model", "p5-toy",
             "--checkpoint", ckpt, "--task", "mqar", "--vocab", "64",
             "--n-pairs", "8", "--episodes", "2", "--seed", "7",
             "--out", str(tmp_path / "e"))
    assert r.returncode != 0, (
        "SILENT FAMILY SWAP: p1 checkpoint scored as p5 with exit 0; "
        "summary inherits the wrong family label"
    )


def test_at2_p5_checkpoint_scored_as_p1_must_be_refused(tmp_path):
    """Reverse direction: p5 weights evaluated as p1-toy must exit nonzero."""
    ckpt = _train_toy_ckpt("p5", 9, tmp_path / "t")
    assert _blob_model(ckpt) == "p5-toy"
    r = _run("postformer.harness.synthetic_recall", "--model", "p1-toy",
             "--checkpoint", ckpt, "--task", "mqar", "--vocab", "64",
             "--n-pairs", "8", "--episodes", "2", "--seed", "9",
             "--out", str(tmp_path / "e"))
    assert r.returncode != 0, (
        "SILENT FAMILY SWAP: p5 checkpoint scored as p1 with exit 0"
    )


def test_at3_load_model_cross_family_raises_system_exit(tmp_path):
    """In-process: load_model must refuse p1<->p5 swaps loudly."""
    m, cfg = build_model("p1", "toy", {"vocab": 66})
    ckpt = str(tmp_path / "p1.pt")
    torch.save({"state_dict": m.state_dict(), "config": cfg,
                "args": {"model": "p1-toy"}}, ckpt)
    with pytest.raises(SystemExit):
        load_model("p5-toy", ckpt, None, {"vocab": 66}, "cpu", "fp32")
    m5, cfg5 = build_model("p5", "toy", {"vocab": 66})
    ckpt5 = str(tmp_path / "p5.pt")
    torch.save({"state_dict": m5.state_dict(), "config": cfg5,
                "args": {"model": "p5-toy"}}, ckpt5)
    with pytest.raises(SystemExit):
        load_model("p1-toy", ckpt5, None, {"vocab": 66}, "cpu", "fp32")


def test_at4_same_family_checkpoint_still_loads(tmp_path):
    """Positive control: the trusted path must keep working after the fix."""
    m, cfg = build_model("p1", "toy", {"vocab": 66})
    ckpt = str(tmp_path / "p1.pt")
    torch.save({"state_dict": m.state_dict(), "config": cfg,
                "args": {"model": "p1-toy"}}, ckpt)
    loaded, _, random_init = load_model(
        "p1-toy", ckpt, None, {"vocab": 66}, "cpu", "fp32")
    assert random_init is False
    for k, v in m.state_dict().items():
        assert torch.equal(v, loaded.state_dict()[k]), k


def test_at5_wrong_family_eval_refused_or_discloses_provenance(tmp_path):
    """Either refuse the swap, or label the summary with true provenance."""
    ckpt = _train_toy_ckpt("p1", 11, tmp_path / "t")
    true_family_model = _blob_model(ckpt)
    out = tmp_path / "e"
    r = _run("postformer.harness.synthetic_recall", "--model", "p5-toy",
             "--checkpoint", ckpt, "--task", "mqar", "--vocab", "64",
             "--n-pairs", "8", "--episodes", "2", "--seed", "11",
             "--out", str(out))
    if r.returncode == 0:
        summaries = list(out.glob("g1_summary*.json"))
        assert summaries, "eval exited 0 but wrote no summary"
        s = json.loads(summaries[0].read_text())
        assert s["model"] == true_family_model, (
            f"summary claims {s['model']!r} but weights are {true_family_model!r}"
        )
    # nonzero exit (loud refusal) is the acceptable alternative.


def test_at6_scale_garbage_missing_checkpoints_stay_loud(tmp_path):
    """Positive locks: other corrupt checkpoints must keep failing loudly."""
    m, cfg = build_model("p1", "toy", {"vocab": 66})
    ckpt = str(tmp_path / "p1.pt")
    torch.save({"state_dict": m.state_dict(), "config": cfg,
                "args": {"model": "p1-toy"}}, ckpt)
    # Scale mismatch: shapes differ, must raise, never silent random-init.
    with pytest.raises(Exception):
        load_model("p1-tiny", ckpt, None, {}, "cpu", "fp32")
    # Garbage bytes: must raise, never silent random-init.
    gar = str(tmp_path / "garbage.pt")
    Path(gar).write_text("not a checkpoint")
    with pytest.raises(Exception):
        load_model("p1-toy", gar, None, {}, "cpu", "fp32")
    # Missing path: must raise, never silent random-init.
    with pytest.raises(Exception):
        load_model("p1-toy", str(tmp_path / "nope.pt"), None, {},
                   "cpu", "fp32")
    # Other cross-family pairs already fail loudly via key/shape mismatch
    # (SystemExit for missing/unexpected keys, RuntimeError for shape
    # mismatch): any loud exception is acceptable, silence is not.
    with pytest.raises(Exception):
        load_model("p2-toy", ckpt, None, {"vocab": 66}, "cpu", "fp32")
