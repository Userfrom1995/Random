"""T4: determinism - same master seed reproduces g1_summary exactly on CPU."""

import json
import os
import tempfile

import yaml

from postformer.harness.synthetic_recall import main as recall_main
from .conftest import MINI


def run_once(tmp, seed):
    cfg_path = os.path.join(tmp, "mini.yaml")
    with open(cfg_path, "w") as f:
        yaml.safe_dump({k: v for k, v in MINI.items() if k != "vocab_size"}, f)
    out = os.path.join(tmp, f"out{seed}")
    recall_main(["--model", "p1-tiny", "--config", cfg_path, "--task", "mqar",
                 "--vocab", "32", "--n-pairs", "4", "--episodes", "4",
                 "--seed", str(seed), "--out", out])
    with open(os.path.join(out, f"g1_summary_seed{seed}.json")) as f:
        return f.read()


def test_determinism():
    with tempfile.TemporaryDirectory() as tmp:
        a = run_once(tmp, 5)
        b = run_once(tmp, 5)
    assert a == b
    s = json.loads(a)
    assert s["mqar"]["4"]["n"] == 16  # 4 episodes x 4 queries
