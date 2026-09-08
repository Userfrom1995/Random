"""G4 footprint microbench: state bytes + median/p90 ms per token vs T.

For T in --lengths: seed a prompt of length T, warm up (--warmup steps),
then time --decode-steps single-token step() calls. State bytes come from
model.state_bytes(batch, T) (recurrent arms must be flat in T; the
Transformer control must grow linearly).
Writes g4_curve_seed{s}.csv
(model,T,state_bytes,ms_per_token_median,ms_p90,hardware,dtype,torch,cuda)
plus g4_proof.json skeleton when --report-proof is passed.
"""

import argparse
import statistics
import time

import numpy as np
import torch

from ..models.common import param_count_no_embed
from .util import add_common_args, env_info, load_model, parse_int_list, reseed, write_csv, write_json


@torch.no_grad()
def bench_T(model, vocab, length, decode_steps, warmup, batch, seed, device):
    rng = np.random.default_rng(reseed(seed, f"g4-prompt-T{length}"))
    prompt = torch.tensor(rng.integers(0, vocab, size=(batch, length)),
                          dtype=torch.long, device=device)
    states = model.init_state(batch, device, next(model.parameters()).dtype)
    # Prefill through the recurrent step API so every arm pays the same path.
    for i in range(length):
        _, states = model.step(prompt[:, i:i + 1], states)
    for _ in range(warmup):
        nxt = torch.randint(0, vocab, (batch, 1), device=device)
        _, states = model.step(nxt, states)
    if device == "cuda":
        torch.cuda.synchronize()
    per_step = []
    for _ in range(decode_steps):
        nxt = torch.randint(0, vocab, (batch, 1), device=device)
        t0 = time.perf_counter()
        _, states = model.step(nxt, states)
        if device == "cuda":
            torch.cuda.synchronize()
        per_step.append((time.perf_counter() - t0) * 1000.0)
    return per_step


def main(argv=None):
    p = argparse.ArgumentParser(description="G4 latency/state microbench")
    add_common_args(p)
    p.add_argument("--lengths", default="1024,2048,4096,8192,16384,32768")
    p.add_argument("--decode-steps", type=int, default=200)
    p.add_argument("--warmup", type=int, default=20)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--report-proof", action="store_true")
    p.add_argument("--vocab", type=int, default=None,
                   help="eval vocab (train --vocab convention); "
                        "model uses vocab_size = vocab + 2; "
                        "absent --vocab falls back to the checkpoint vocab_size")
    a = p.parse_args(argv)
    if a.decode_steps < 1:
        raise SystemExit("--decode-steps must be >= 1")
    if a.batch_size < 1:
        raise SystemExit("--batch-size must be >= 1")
    if a.warmup < 0:
        raise SystemExit("--warmup must be >= 0")
    if not parse_int_list(a.lengths):
        raise SystemExit("--lengths must list at least one length")
    reseed(a.seed, f"init-{a.model}")  # deterministic init before any torch draws
    if a.vocab is not None and a.checkpoint:
        _blob = torch.load(a.checkpoint, map_location="cpu", weights_only=False)
        _cv = ((_blob.get("config") or {}).get("vocab_size")
               if isinstance(_blob, dict) else None)
        if _cv is not None and int(_cv) != int(a.vocab) + 2:
            raise SystemExit(
                f"--vocab {a.vocab} (vocab_size {int(a.vocab) + 2}) != "
                f"checkpoint train vocab_size {_cv}; "
                f"refusing to partial-load or OOB the embedding")
    if a.vocab is not None and int(a.vocab) < 16:
        raise SystemExit(f"--vocab must be >= 16, got {a.vocab}")
    _vocab_ov = {"vocab_size": int(a.vocab) + 2} if a.vocab is not None else None
    model, cfg, random_init = load_model(a.model, a.checkpoint, a.config, _vocab_ov,
                                         a.device, a.dtype)
    vocab = int(a.vocab) if a.vocab is not None else cfg["vocab_size"]
    info = env_info()
    info["dtype"] = a.dtype
    bpe = {"fp32": 4, "fp16": 2, "bf16": 2}[a.dtype]
    rows = []
    for length in parse_int_list(a.lengths):
        per = bench_T(model, vocab, length, a.decode_steps, a.warmup,
                      a.batch_size, a.seed, a.device)
        rows.append({"model": a.model, "T": length,
                     "state_bytes": model.state_bytes(a.batch_size, length, bpe),
                     "ms_per_token_median": statistics.median(per),
                     "ms_p90": float(np.percentile(per, 90)),
                     "hardware": info["hardware"], "dtype": a.dtype,
                     "torch": info["torch"], "cuda": info["cuda"],
                     "seed": a.seed, "random_init": random_init,
                     "params": param_count_no_embed(model)})
    write_csv(f"{a.out}/g4_curve_seed{a.seed}.csv",
              ["model", "T", "state_bytes", "ms_per_token_median", "ms_p90",
               "hardware", "dtype", "torch", "cuda", "seed", "random_init", "params"], rows)
    if a.report_proof:
        proof = {"model": a.model, "config": cfg,
                 "claim": "O(1) state and O(1) per-token latency in T",
                 "state_inventory": "see postformer/docs/proof-g4.md",
                 "measured": rows, "env": info}
        write_json(f"{a.out}/g4_proof.json", proof)
    print(f"wrote {a.out}/g4_curve_seed{a.seed}.csv")


if __name__ == "__main__":
    main()
