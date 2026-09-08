"""M2 matched-budget trainer: MQAR associative-recall + Markov LM training.

Trains baseline and candidate arms under identical token streams, steps,
batch, optimizer (AdamW cosine, blueprint section "Optimizer shared across
arms"), and seeds: the data RNG is keyed by (seed, data) only, so every arm
at one seed sees the same episodes in the same order; the init RNG is keyed
by (seed, model, data), so each arm keeps its own deterministic init.
Checkpoints are torch.save dicts loadable by every harness --checkpoint flag.

MQAR episodes mirror harness/synthetic_recall.gen_mqar (k v bigrams
shuffled, permuted queries after a separator, greedy-decodable), trained
with full-sequence next-token cross-entropy: every position (study pairs,
separator, and query answers) contributes to the loss. This is deliberate
for M2 - the study tokens provide LM-shaped gradient and the query-answer
positions carry the recall gradient measured by G1; a span-masked
(query-only) loss variant is M3 work (see mqar_query_positions below for the
exact query-answer index set it must use).

Example (toy proxy, CPU):
  python -m postformer.harness.train --model p1-toy --data mqar \\
    --vocab 64 --n-pairs 8 --steps 1500 --batch 16 --lr 3e-4 --seed 0 \\
    --out postformer/ledger/checkpoints/p1-toy-seed0
"""

import argparse
import math
import os

import numpy as np
import torch
import torch.nn.functional as F

from ..models.common import param_count_no_embed, seed_all
from .util import env_info, write_csv, write_json


def gen_mqar_episode(rng, vocab, n_pairs):
    """One MQAR episode as an id list (mirrors G1 gen_mqar plus separator).

    Layout: 2*n_pairs study tokens, one separator id (vocab), then the
    permuted query pairs. Query-answer target positions are given by
    mqar_query_positions(n_pairs); the M2 loss covers the full sequence
    (study + separator + query) by design, see module docstring."""
    keys = rng.choice(vocab, size=n_pairs, replace=False)
    vals = rng.integers(0, vocab, size=n_pairs)
    for i in range(n_pairs):
        while vals[i] == keys[i]:
            vals[i] = rng.integers(0, vocab)
    sep = vocab
    order = rng.permutation(n_pairs)
    seq = []
    for i in order:
        seq += [int(keys[i]), int(vals[i])]
    seq.append(sep)
    qorder = rng.permutation(n_pairs)
    for i in qorder:
        seq += [int(keys[i]), int(vals[i])]
    return seq


def mqar_query_positions(n_pairs):
    """Target-side index set of the query-answer tokens in an MQAR episode.

    Episode layout (see gen_mqar_episode): 2*n_pairs study tokens, one
    separator, then 2*n_pairs query tokens (key, answer, key, answer, ...).
    Full-sequence CE (M2) trains on all positions; a future span-masked loss
    must restrict the loss to the answer positions {2*n+1 + 2*i + 1}.
    Pure-python helper kept alongside the generator so the masked variant
    cannot drift from this layout.
    """
    base = 2 * n_pairs + 1
    return [base + 2 * i + 1 for i in range(n_pairs)]


def gen_markov_episode(rng, vocab, length, order=3):
    """Seeded order-`order` Markov stream (LM-flavoured control task)."""
    ctx = tuple(int(x) for x in rng.integers(0, vocab, size=order))
    out = list(ctx)
    trans = {}
    for _ in range(length - order):
        if ctx not in trans:
            trans[ctx] = rng.integers(0, vocab, size=4)
        nxt = int(rng.choice(trans[ctx]))
        out.append(nxt)
        ctx = (*ctx[1:], nxt)
    return out


def batch_mqar(rng, vocab, n_pairs, batch):
    seqs = [gen_mqar_episode(rng, vocab, n_pairs) for _ in range(batch)]
    return torch.tensor(seqs, dtype=torch.long)


def batch_markov(rng, vocab, length, batch):
    return torch.tensor([gen_markov_episode(rng, vocab, length) for _ in range(batch)],
                        dtype=torch.long)


def cosine_lr(step, total, warmup, peak):
    if step < warmup:
        return peak * (step + 1) / max(1, warmup)
    t = (step - warmup) / max(1, total - warmup)
    return peak * 0.5 * (1.0 + math.cos(math.pi * min(1.0, t)))


def main(argv=None):
    from ..models.factory import build_model

    p = argparse.ArgumentParser(description="M2 matched-budget trainer")
    p.add_argument("--model", required=True, help="e.g. p1-toy, transformer-tiny")
    p.add_argument("--data", default="mqar", choices=["mqar", "markov"])
    p.add_argument("--vocab", type=int, default=64)
    p.add_argument("--n-pairs", type=int, default=8)
    p.add_argument("--seq-len", type=int, default=128,
                   help="markov episode length (mqar length is 4*n_pairs+1)")
    p.add_argument("--steps", type=int, default=1500)
    p.add_argument("--batch", type=int, default=16)
    p.add_argument("--lr", type=float, default=3e-4)
    p.add_argument("--warmup", type=int, default=100)
    p.add_argument("--weight-decay", type=float, default=0.1)
    p.add_argument("--grad-clip", type=float, default=1.0)
    p.add_argument("--window", type=int, default=None,
                   help="override sliding-window W (A2: 0/16/32 at matched toy params)")
    p.add_argument("--slots", type=int, default=None,
                   help="override P2 global-slot count G (A4: 0/4/16/64; "
                        "slots=0 is the pure-SSD control)")
    p.add_argument("--no-accumulator", action="store_true",
                   help="A3 control: freeze the P3 accumulator branch "
                        "(dynamics removed, params unchanged)")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--device", default="cpu")
    p.add_argument("--out", required=True)
    p.add_argument("--log-every", type=int, default=100)
    a = p.parse_args(argv)
    if a.vocab < 16:
        raise SystemExit("--vocab must be >= 16")
    if a.n_pairs >= a.vocab:
        raise SystemExit("--n-pairs must be < --vocab (keys sampled without replacement)")
    if a.n_pairs < 1:
        raise SystemExit("--n-pairs must be >= 1")
    if a.steps < 1:
        raise SystemExit("--steps must be >= 1")
    if a.batch < 1:
        raise SystemExit("--batch must be >= 1")
    if a.log_every < 1:
        raise SystemExit("--log-every must be >= 1")
    if a.seq_len <= 3:
        raise SystemExit("--seq-len must exceed the Markov order (3)")

    # Matched budget: data stream keyed by (seed, data) ONLY - identical
    # episodes for every arm at one seed. Init keyed by (seed, model, data)
    # AFTER, so torch's global RNG (consumed by build_model below) keeps a
    # per-arm deterministic init.
    data_sub = seed_all(a.seed, f"train-data-{a.data}")
    data_rng = np.random.default_rng(data_sub ^ 0x5F3D2917)
    seed_all(a.seed, f"train-init-{a.model}-{a.data}")
    dev = torch.device(a.device)

    overrides = {"vocab_size": a.vocab + 2}
    family = a.model.rsplit("-", 1)[0]
    if a.window is not None and family not in ("p1", "p2", "p3", "p4", "p5"):
        raise SystemExit("--window applies to p1/p2/p3/p4/p5 arms only (transformer has no window)")
    if a.slots is not None and family != "p2":
        raise SystemExit("--slots applies to p2 arms only")
    if a.no_accumulator and family != "p3":
        raise SystemExit("--no-accumulator applies to p3 arms only")
    if a.window is not None:
        if a.window < 0:
            raise SystemExit("--window must be >= 0")
        overrides["window"] = a.window
    if a.slots is not None:
        if a.slots < 0:
            raise SystemExit("--slots must be >= 0")
        overrides["slots"] = a.slots
    if a.no_accumulator:
        overrides["use_accumulator"] = False
    parts = a.model.rsplit("-", 1)
    if len(parts) != 2:
        raise SystemExit(f"--model must look like p1-toy, got {a.model!r}")
    model, cfg = build_model(parts[0], parts[1], overrides)
    model = model.to(dev).train()
    n_params = param_count_no_embed(model)

    opt = torch.optim.AdamW(model.parameters(), lr=a.lr,
                            betas=(0.9, 0.95), weight_decay=a.weight_decay)
    curve = []
    tokens = 0
    for step in range(a.steps):
        lr = cosine_lr(step, a.steps, a.warmup, a.lr)
        for g in opt.param_groups:
            g["lr"] = lr
        if a.data == "mqar":
            ids = batch_mqar(data_rng, a.vocab, a.n_pairs, a.batch).to(dev)
        else:
            ids = batch_markov(data_rng, a.vocab, a.seq_len, a.batch).to(dev)
        logits = model(ids[:, :-1])
        loss = F.cross_entropy(logits.reshape(-1, logits.shape[-1]),
                               ids[:, 1:].reshape(-1))
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), a.grad_clip)
        opt.step()
        tokens += ids.numel()
        if step % a.log_every == 0 or step == a.steps - 1:
            curve.append({"step": step, "loss": float(loss.item()),
                          "lr": lr, "train_tokens": tokens})
            print(f"[{a.model} s{a.seed}] step {step}/{a.steps} loss={loss.item():.4f}", flush=True)

    os.makedirs(a.out, exist_ok=True)
    ckpt = os.path.join(a.out, "checkpoint.pt")
    torch.save({"state_dict": model.state_dict(), "config": cfg,
                "args": vars(a), "params_no_embed": n_params,
                "train_tokens": tokens}, ckpt)
    write_csv(os.path.join(a.out, "train_curve.csv"),
              ["step", "loss", "lr", "train_tokens"], curve)
    info = env_info()
    write_json(os.path.join(a.out, "train_summary.json"),
               {"model": a.model, "config": cfg, "data": a.data,
                "params_no_embed": n_params, "train_tokens": tokens,
                "final_loss": curve[-1]["loss"], "env": info})
    print(f"saved {ckpt} ({tokens} tokens)")


if __name__ == "__main__":
    main()
