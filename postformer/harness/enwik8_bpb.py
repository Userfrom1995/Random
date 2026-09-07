"""G3 Enwik8 BPB: primary scoreboard is enwik8-valid BPB (byte level).

BPB = loss_nats / ln2 mapped to bytes. Fixed split: first 90M train,
next 5M valid, last 5M test (pins to available bytes for small fixtures,
recording n_bytes honestly). Test split is scored only at gate time.
Writes g3_bpb_seed{s}.csv
(model,split,context,stride,tokenizer,loss_nats,bpb,n_bytes,sha256_data).
"""

import argparse
import hashlib
import math
import os

import numpy as np
import torch

from ..models.common import param_count_no_embed
from .util import add_common_args, env_info, load_model, reseed, write_csv, write_json

TRAIN_END = 90_000_000
VALID_END = 95_000_000


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


@torch.no_grad()
def score_stream(model, ids, context, stride, device, cap_windows=None):
    nlls, n = [], 0
    for s in range(0, len(ids) - context + 1, stride):
        seg = ids[s:s + context]
        logits = model(seg.unsqueeze(0).to(device)).float()
        logp = torch.log_softmax(logits[0], dim=-1)
        tgt = seg[1:].to(device)
        per = (-logp[:-1].gather(1, tgt.unsqueeze(1)).squeeze(1)).tolist()
        keep_from = 0 if s == 0 else (context - stride - 1)
        nlls.extend(per[keep_from:])
        n += 1
        if cap_windows and n >= cap_windows:
            break
    if not nlls:
        raise SystemExit("no windows scored; check context/stride/data size")
    return float(np.mean(nlls)), len(nlls)


def main(argv=None):
    p = argparse.ArgumentParser(description="G3 Enwik8 BPB harness")
    add_common_args(p)
    p.add_argument("--split", default="valid", choices=["valid", "test"])
    p.add_argument("--context", type=int, required=True)
    p.add_argument("--stride", type=int, default=None)
    p.add_argument("--tokenizer", default="byte", choices=["byte", "bpe"])
    p.add_argument("--data-root", required=True)
    p.add_argument("--checksum", default=None, help="expected sha256 of data file")
    p.add_argument("--max-windows", type=int, default=None,
                   help="cap windows scored (smoke fixtures); full eval when absent")
    a = p.parse_args(argv)
    if a.tokenizer == "bpe":
        raise SystemExit("BPE is a secondary diagnostic deferred past M1; "
                         "use --tokenizer byte (primary scoreboard)")
    path = os.path.join(a.data_root, "enwik8")
    if not os.path.exists(path):
        raise SystemExit(f"missing Enwik8 data file: {path} "
                         "(Hutter Prize Enwik8, 100M bytes)")
    digest = sha256_file(path)
    if a.checksum and digest != a.checksum:
        raise SystemExit(f"checksum mismatch: got {digest}, want {a.checksum}")
    size = os.path.getsize(path)
    lo = TRAIN_END if size > VALID_END else 0
    hi = (VALID_END if a.split == "valid" else size) if size > VALID_END else size
    if a.split == "test" and size <= VALID_END:
        raise SystemExit("test split needs the full 100M file; fixture too small")
    with open(path, "rb") as f:
        f.seek(lo)
        raw = f.read(hi - lo)
    ids = torch.tensor(list(raw), dtype=torch.long)
    if int(ids.max()) > 255:
        raise SystemExit("byte stream out of range")
    reseed(a.seed, f"init-{a.model}")  # deterministic init before any torch draws
    model, cfg, random_init = load_model(a.model, a.checkpoint, a.config,
                                         {"vocab_size": 256}, a.device, a.dtype)
    if cfg["vocab_size"] != 256:
        raise SystemExit(f"byte-level BPB needs vocab_size 256, got {cfg['vocab_size']}")
    stride = a.stride or max(1, a.context // 2)
    reseed(a.seed, f"g3-{a.split}")
    loss_nats, n_tok = score_stream(model, ids, a.context, stride, a.device, a.max_windows)
    bpb = loss_nats / math.log(2)
    row = {"model": a.model, "split": a.split, "context": a.context, "stride": stride,
           "tokenizer": a.tokenizer, "loss_nats": loss_nats, "bpb": bpb,
           "n_bytes": n_tok, "sha256_data": digest,
           "seed": a.seed, "random_init": random_init,
           "params": param_count_no_embed(model)}
    write_csv(f"{a.out}/g3_bpb_seed{a.seed}.csv",
              ["model", "split", "context", "stride", "tokenizer", "loss_nats",
               "bpb", "n_bytes", "sha256_data", "seed", "random_init", "params"], [row])
    info = env_info()
    info["dtype"] = a.dtype
    write_json(f"{a.out}/g3_summary_seed{a.seed}.json", {"rows": [row], "env": info})
    print(f"wrote {a.out}/g3_bpb_seed{a.seed}.csv bpb={bpb:.4f}")


if __name__ == "__main__":
    main()
