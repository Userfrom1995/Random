"""G2 length sweep: degradation delta BPB(L) - BPB(T_train) at 1x/2x/4x/8x.

Sliding-window NLL eval (stride T_train/2, no arm-specific truncation).
Writes g2_curve_seed{s}.csv (model,length,bpb,ppl,delta_vs_1x,gap_vs_baseline).

--split synthetic: seeded random streams over the model vocab (isolates
retrieval/drift plumbing; real text streams arrive with enwik8_bpb G3).
--split bytes: raw-byte stream from --data-root (byte vocab models only).
"""

import argparse
import math
import os

import numpy as np
import torch

from ..models.common import param_count_no_embed
from .util import add_common_args, env_info, load_model, parse_int_list, reseed, write_csv, write_json


def stream_synthetic(rng, vocab, length):
    return torch.tensor(rng.integers(0, vocab, size=length), dtype=torch.long)


def stream_bytes(path, length, offset):
    with open(path, "rb") as f:
        f.seek(offset)
        raw = f.read(length)
    if len(raw) < length:
        raise SystemExit(f"{path}: only {len(raw)} bytes at offset {offset}, need {length}")
    return torch.tensor(list(raw), dtype=torch.long)


@torch.no_grad()
def token_nlls(model, ids, device):
    """Per-token NLL for ids[1:] given ids[:-1] as prefix. Returns list[float]."""
    logits = model(ids.unsqueeze(0).to(device)).float()
    logp = torch.log_softmax(logits[0], dim=-1)
    tgt = ids[1:].to(device)
    return (-logp[:-1].gather(1, tgt.unsqueeze(1)).squeeze(1)).tolist()


def eval_length(model, vocab, kind, data_root, length, t_train, stride, seed, device):
    """Score-once strided eval: stream of `length` fresh tokens after a T_train
    warmup prefix; each token scored exactly once with <= T_train context."""
    total = t_train + length
    if kind == "synthetic":
        rng = np.random.default_rng(reseed(seed, f"g2-stream-L{length}"))
        stream = stream_synthetic(rng, vocab, total)
    else:
        path = os.path.join(data_root, "enwik8")
        if not os.path.exists(path):
            raise SystemExit(f"--data-root {data_root} lacks enwik8 file")
        size = os.path.getsize(path)
        start = 90_000_000 % max(1, size - total - 1)  # valid head; wraps for fixtures
        stream = stream_bytes(path, min(total, size - start), start)
        if len(stream) < 16:
            raise SystemExit("byte stream too short to score")
    nlls = []
    for s in range(0, len(stream) - t_train + 1, stride):
        seg = stream[s:s + t_train]
        if len(seg) < 16:
            continue
        per = token_nlls(model, seg, device)
        keep_from = 0 if s == 0 else (t_train - stride - 1)
        nlls.extend(per[keep_from:])
        if s + t_train >= len(stream):
            break
    if not nlls:
        raise SystemExit("no windows scored; check lengths/stride")
    mean_nll = float(np.mean(nlls))
    return mean_nll, mean_nll / math.log(2), len(nlls)


def main(argv=None):
    p = argparse.ArgumentParser(description="G2 length sweep harness")
    add_common_args(p)
    p.add_argument("--baseline-model", default=None,
                   help="baseline arm name for gap_vs_baseline (default: transformer-<scale>)")
    p.add_argument("--baseline-checkpoint", default=None,
                   help="checkpoint for the baseline arm; absent = seeded random "
                        "init flagged random_init:true (NOT a gate measurement)")
    p.add_argument("--t-train", type=int, required=True)
    p.add_argument("--lengths", default=None,
                   help="comma list; default 1x,2x,4x,8x of --t-train")
    p.add_argument("--stride", type=int, default=None)
    p.add_argument("--split", default="synthetic", choices=["synthetic", "bytes"])
    p.add_argument("--tokenizer", default="byte", choices=["byte", "bpe"])
    p.add_argument("--data-root", default=None)
    p.add_argument("--vocab", type=int, default=None,
                   help="eval vocab (train --vocab convention); "
                        "model uses vocab_size = vocab + 2; "
                        "discovered path (no --vocab) keeps raw vocab_size units "
                        "for backward compat with existing G2 curves")
    a = p.parse_args(argv)
    if a.tokenizer == "bpe":
        raise SystemExit("BPE is a secondary diagnostic deferred past M1; "
                         "use --tokenizer byte (primary scoreboard)")
    if a.split == "bytes" and a.tokenizer != "byte":
        raise SystemExit(f"--split bytes needs --tokenizer byte, got {a.tokenizer!r}")
    lengths = parse_int_list(a.lengths) if a.lengths else [a.t_train * m for m in (1, 2, 4, 8)]
    stride = a.stride or max(1, a.t_train // 2)
    from ..models.factory import parse_model_name
    _family, scale = parse_model_name(a.model)
    if a.baseline_model:
        parse_model_name(a.baseline_model)  # fail loudly on tags, never silent
    base_name = a.baseline_model or f"transformer-{scale}"
    vocab = a.vocab
    if vocab is None:
        _m, cfg0, _ = load_model(a.model, a.checkpoint, a.config, None, a.device, a.dtype)
        vocab = cfg0["vocab_size"]
    else:
        if int(vocab) < 16:
            raise SystemExit(f"--vocab must be >= 16, got {vocab}")
        for _name, _ckpt in ((a.model, a.checkpoint),
                             (base_name, a.baseline_checkpoint)):
            if _ckpt:
                _blob = torch.load(_ckpt, map_location="cpu", weights_only=False)
                _cv = (( _blob.get("config") or {}).get("vocab_size")
                       if isinstance(_blob, dict) else None)
                if _cv is not None and int(_cv) != int(vocab) + 2:
                    raise SystemExit(
                        f"--vocab {vocab} (vocab_size {int(vocab) + 2}) != "
                        f"checkpoint train vocab_size {_cv} "
                        f"for {_name}; refusing to partial-load or OOB the embedding")
    rows = []
    # Explicit --vocab uses the train convention (model vocab_size = vocab + 2,
    # prompts sampled from 0..vocab-1); the discovered path keeps vocab_size
    # identity for backward compatibility with existing G2 curves.
    _vocab_size_ov = int(vocab) + 2 if a.vocab is not None else int(vocab)
    for name in ([a.model] if a.model == base_name else [base_name, a.model]):
        if name == a.model and a.model == base_name and a.baseline_checkpoint:
            raise SystemExit("--baseline-checkpoint ignored: --model is the baseline; "
                             "pass --checkpoint instead")
        reseed(a.seed, f"init-{name}")  # deterministic init before any torch draws
        ckpt = a.checkpoint if name == a.model else a.baseline_checkpoint
        arm_config = a.config if name == a.model else None
        model, cfg, rnd = load_model(name, ckpt,
                                     arm_config, {"vocab_size": _vocab_size_ov}, a.device, a.dtype)
        if rnd and name != a.model:
            print(f"note: baseline {name} uses seeded random init (no checkpoint given)")
        for length in lengths:
            nll, bpb, scored = eval_length(model, vocab, a.split, a.data_root, length,
                                           a.t_train, stride, a.seed, a.device)
            rows.append({"model": name, "length": length, "bpb": bpb,
                         "ppl": math.exp(nll), "seed": a.seed, "n_tokens": scored,
                         "random_init": rnd, "params": param_count_no_embed(model)})
    by_model = {}
    for r in rows:
        by_model.setdefault(r["model"], {})[r["length"]] = r["bpb"]
    for r in rows:
        b1 = by_model[r["model"]][lengths[0]]
        r["delta_vs_1x"] = r["bpb"] - b1
        if a.model in by_model and base_name in by_model:
            r["gap_vs_baseline"] = (by_model[a.model][r["length"]] - by_model[a.model][lengths[0]]
                                    - (by_model[base_name][r["length"]] - by_model[base_name][lengths[0]]))
        else:
            r["gap_vs_baseline"] = 0.0
    write_csv(f"{a.out}/g2_curve_seed{a.seed}.csv",
              ["model", "length", "bpb", "ppl", "delta_vs_1x", "gap_vs_baseline",
               "seed", "n_tokens", "random_init", "params"], rows)
    info = env_info()
    info["dtype"] = a.dtype
    write_json(f"{a.out}/g2_summary_seed{a.seed}.json",
               {"lengths": lengths, "t_train": a.t_train,
                "stride": stride, "split": a.split,
                "tokenizer": a.tokenizer, "env": info})
    print(f"wrote {a.out}/g2_curve_seed{a.seed}.csv")


if __name__ == "__main__":
    main()
