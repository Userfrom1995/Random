"""Shared harness helpers: model loading, dtypes, CSV/JSON output, env info."""

import argparse
import csv
import json
import os
import platform

import torch
import yaml

from ..models.common import seed_all
from ..models.factory import build_model


DTYPES = {"fp32": torch.float32, "fp16": torch.float16, "bf16": torch.bfloat16}


def load_model(name, checkpoint, config_path, extra_overrides, device, dtype_s):
    """Build (family-scale) model; load checkpoint if given else seeded random init.

    Returns (model.eval(), config, random_init_flag).
    """
    parts = name.rsplit("-", 1)
    if len(parts) != 2:
        raise SystemExit(f"--model must look like p1-tiny, got {name!r}")
    family, scale = parts
    overrides = dict(extra_overrides or {})
    if config_path:
        with open(config_path) as f:
            file_cfg = yaml.safe_load(f) or {}
        overrides.update(file_cfg)
    model, cfg = build_model(family, scale, overrides or None)
    random_init = False
    if checkpoint:
        blob = torch.load(checkpoint, map_location="cpu", weights_only=False)
        sd = blob["state_dict"] if isinstance(blob, dict) and "state_dict" in blob else blob
        missing, unexpected = model.load_state_dict(sd, strict=False), None
        if missing.missing_keys or missing.unexpected_keys:
            raise SystemExit(f"checkpoint mismatch: missing={missing.missing_keys} "
                             f"unexpected={missing.unexpected_keys}")
    else:
        random_init = True
    dtype = DTYPES[dtype_s]
    model = model.to(device=device, dtype=dtype).eval()
    return model, cfg, random_init


def write_csv(path, fieldnames, rows):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def write_json(path, obj):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, sort_keys=True)


def env_info():
    return {
        "hardware": f"{platform.machine()} x{os.cpu_count()} {platform.processor()}".strip(),
        "dtype": None,
        "torch": torch.__version__,
        "cuda": torch.version.cuda or "cpu",
        "platform": platform.platform(),
    }


def reseed(master, purpose):
    return seed_all(master, purpose)


def add_common_args(p):
    p.add_argument("--model", required=True, help="e.g. p1-tiny, transformer-small")
    p.add_argument("--checkpoint", default=None, help="torch checkpoint; absent = seeded random init")
    p.add_argument("--config", default=None, help="yaml overrides for dims/vocab")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--device", default="cpu")
    p.add_argument("--dtype", default="fp32", choices=list(DTYPES))
    p.add_argument("--out", required=True, help="output directory for CSV/JSON")


def parse_int_list(s):
    return [int(x) for x in str(s).split(",") if str(x).strip() != ""]
