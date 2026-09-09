"""Shared harness helpers: model loading, dtypes, CSV/JSON output, env info."""

import csv
import json
import os
import platform

import torch
import yaml

from ..models.common import seed_all
from ..models.factory import build_model, parse_model_name


DTYPES = {"fp32": torch.float32, "fp16": torch.float16, "bf16": torch.bfloat16}


def load_model(name, checkpoint, config_path, extra_overrides, device, dtype_s):
    """Build (family-scale) model; load checkpoint if given else seeded random init.

    Non-parameter ablation keys (window, slots, use_accumulator,
    slot_stride) are not tensor shapes, so a state_dict load cannot catch
    their mismatch (M2 A2 lesson: a W0 checkpoint silently evaluated as
    W16). They are therefore inherited from the checkpoint's stored
    config unless the caller explicitly overrides them; a --config file
    value disagreeing with the checkpoint on these keys fails loudly.
    The --window CLI override stays explicitly allowed (deliberate A2
    protocol): an explicit window in extra_overrides may differ from the
    checkpoint, but a --config file window may not. Length/latency/enwik8
    harnesses have no --window flag, so any window mismatch there fails
    via this shared guard.

    Returns (model.eval(), config, random_init_flag).
    """
    # Strict --model gate (M2 silent-invalidation class): only canonical
    # family-scale names pass; middle tags (p2-G0-toy) or suffixes
    # (p1-toy-V512) fail loudly instead of silently building the wrong arm.
    family, scale = parse_model_name(name)
    # Explicit CLI wins over --config file (deliberate-A2 protocol):
    # a --config file value must not silently overwrite an explicit
    # --window/--slots flag; None means "not passed".
    file_cfg = {}
    if config_path:
        with open(config_path) as f:
            file_cfg = yaml.safe_load(f) or {}
    overrides = dict(file_cfg or {})
    overrides.update({k: v for k, v in (extra_overrides or {}).items() if v is not None})
    ckpt_cfg, blob = {}, None
    ckpt_provenance = None
    ckpt_scale = None
    if checkpoint:
        blob = torch.load(checkpoint, map_location="cpu", weights_only=False)
        if isinstance(blob, dict):
            ckpt_cfg = blob.get("config") or {}
            args = blob.get("args") or {}
            prov = args.get("model") if isinstance(args, dict) else None
            if isinstance(prov, str) and prov:
                try:
                    ckpt_provenance, ckpt_scale = parse_model_name(prov)
                except SystemExit:
                    ckpt_provenance = None
                    ckpt_scale = None
    # Checkpoint trust boundary (M4at lesson): p1<->p5 share identical
    # state_dict key sets by design, so strict=False passes vacuously and
    # a p1 blob scored as p5 (or reverse) exits 0 with the wrong family
    # label. Refuse loudly when the checkpoint's stored provenance
    # (blob['args']['model']) disagrees on family. Fail open when
    # provenance is absent (hand-made blobs, plain state_dicts) so the
    # trusted same-family path and legacy blobs keep loading.
    if ckpt_provenance is not None and ckpt_provenance != family:
        raise SystemExit(
            f"checkpoint family={ckpt_provenance!r} != requested "
            f"family={family!r}; refusing to silently score the wrong "
            f"family arm")
    if ckpt_scale is not None and ckpt_scale != scale:
        raise SystemExit(
            f"checkpoint scale={ckpt_scale!r} != requested "
            f"scale={scale!r}; refusing to silently score the wrong "
            f"scale arm")
    for k in ("window", "slots", "use_accumulator", "slot_stride"):
        if k in ckpt_cfg and k not in overrides:
            overrides[k] = ckpt_cfg[k]
    for k in ("slots", "use_accumulator", "slot_stride"):
        if k in overrides and k in ckpt_cfg and overrides[k] != ckpt_cfg[k]:
            raise SystemExit(
                f"--config {k}={overrides[k]!r} != checkpoint train "
                f"{k}={ckpt_cfg[k]!r}; refusing to silently run the wrong "
                f"ablation arm")
    if ("window" in ckpt_cfg and "window" in overrides
            and overrides["window"] != ckpt_cfg["window"]):
        explicit_window = (extra_overrides or {}).get("window", None)
        if not (explicit_window is not None
                and overrides["window"] == explicit_window):
            raise SystemExit(
                f"--config window={overrides['window']!r} != checkpoint train "
                f"window={ckpt_cfg['window']!r}; refusing to silently run the "
                f"wrong ablation arm (pass --window explicitly to override)")
    model, cfg = build_model(family, scale, overrides or None)
    random_init = False
    if blob is not None:
        sd = blob["state_dict"] if isinstance(blob, dict) and "state_dict" in blob else blob
        try:
            missing = model.load_state_dict(sd, strict=False)
        except RuntimeError as e:
            raise SystemExit(f"checkpoint mismatch (shape): {e}")
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
    """Comma list of ints with optional k/K (x1024) / m/M (x1024**2) suffixes.

    Supports blueprint shorthands such as --lengths 1k,2k,4k,8k (1k = 1024).
    """
    out = []
    for tok in str(s).split(","):
        t = tok.strip()
        if not t:
            continue
        mult = 1
        if t[-1] in ("k", "K"):
            mult, t = 1024, t[:-1]
        elif t[-1] in ("m", "M"):
            mult, t = 1024 ** 2, t[:-1]
        try:
            out.append(int(t.strip()) * mult)
        except ValueError:
            raise SystemExit(f"bad integer list entry {tok!r} in {s!r}")
    return out
