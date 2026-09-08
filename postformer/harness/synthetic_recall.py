"""G1 synthetic recall: MQAR + induction + copying + 2-hop variable binding.

Greedy decode (temperature 0, top-k disabled), exact-match accuracy plus
recall@k. Same tokenizer/window/order/scoring for every arm.
Writes g1_mqar_N{n}_seed{s}.csv (episode,query_idx,key,value,pred,correct,rank)
plus g1_summary_seed{s}.json (acc, recall@1/@3, mean, std, n).
"""

import argparse

import numpy as np
import torch

from ..models.common import param_count_no_embed
from .util import add_common_args, env_info, load_model, parse_int_list, reseed, write_csv, write_json


def gen_mqar(rng, vocab, n_pairs):
    keys = rng.choice(vocab, size=n_pairs, replace=False)
    vals = rng.integers(0, vocab, size=n_pairs)
    for i in range(n_pairs):
        while vals[i] == keys[i]:
            vals[i] = rng.integers(0, vocab)
    order = rng.permutation(n_pairs)
    seq = []
    for i in order:
        seq += [int(keys[i]), int(vals[i])]
    qorder = rng.permutation(n_pairs)
    return seq, [(int(keys[i]), int(vals[i])) for i in qorder]


@torch.no_grad()
def greedy_next(model, prefix, device):
    ids = torch.tensor([prefix], dtype=torch.long, device=device)
    logits = model(ids)
    last = logits[0, -1].float()
    order = torch.argsort(last, descending=True)
    return int(torch.argmax(last).item()), order


def run_mqar(model, cfg, vocab, n_pairs, episodes, seed, device, out):
    rng = np.random.default_rng(reseed(seed, f"g1-mqar-N{n_pairs}"))
    sep = vocab
    rows, accs, r1, r3 = [], [], [], []
    for ep in range(episodes):
        seq, queries = gen_mqar(rng, vocab, n_pairs)
        base = seq + [sep]
        for qi, (k, v) in enumerate(queries):
            prefix = base + [qq for pair in queries[:qi] for qq in (pair[0], pair[1])] + [k]
            pred, order = greedy_next(model, prefix, device)
            rank = int((order == v).nonzero(as_tuple=True)[0].item()) + 1
            ok = int(pred == v)
            rows.append({"episode": ep, "query_idx": qi, "key": k, "value": v,
                         "pred": pred, "correct": ok, "rank": rank})
            accs.append(ok)
            r1.append(int(rank <= 1))
            r3.append(int(rank <= 3))
    write_csv(f"{out}/g1_mqar_N{n_pairs}_seed{seed}.csv",
              ["episode", "query_idx", "key", "value", "pred", "correct", "rank"], rows)
    return float(np.mean(accs)), float(np.mean(r1)), float(np.mean(r3)), len(accs)


def run_induction(model, cfg, vocab, gaps, episodes, seed, device, out):
    rng = np.random.default_rng(reseed(seed, "g1-induction"))
    per_gap = {}
    for gap in gaps:
        rows, accs = [], []
        for ep in range(episodes):
            a = int(rng.integers(0, vocab))
            b = int(rng.integers(0, vocab))
            while b == a:
                b = int(rng.integers(0, vocab))
            filler = [int(x) for x in rng.integers(0, vocab, size=gap)]
            prefix = [a, b] + filler + [a]
            pred, _ = greedy_next(model, prefix, device)
            ok = int(pred == b)
            rows.append({"episode": ep, "gap": gap, "a": a, "b": b,
                         "pred": pred, "correct": ok})
            accs.append(ok)
        write_csv(f"{out}/g1_induction_gap{gap}_seed{seed}.csv",
                  ["episode", "gap", "a", "b", "pred", "correct"], rows)
        per_gap[gap] = float(np.mean(accs))
    return per_gap


def run_copying(model, cfg, vocab, copy_lens, episodes, seed, device, out):
    rng = np.random.default_rng(reseed(seed, "g1-copy"))
    sep = vocab
    per_len = {}
    for ln in copy_lens:
        rows, accs = [], []
        for ep in range(episodes):
            s = [int(x) for x in rng.integers(0, vocab, size=ln)]
            prefix = s + [sep]
            got = []
            ctx = list(prefix)
            for _ in range(ln):
                pred, _ = greedy_next(model, ctx, device)
                got.append(pred)
                ctx.append(pred)
            ok = int(got == s)
            rows.append({"episode": ep, "length": ln, "correct": ok})
            accs.append(ok)
        write_csv(f"{out}/g1_copy_L{ln}_seed{seed}.csv", ["episode", "length", "correct"], rows)
        per_len[ln] = float(np.mean(accs))
    return per_len


def run_bind2hop(model, cfg, vocab, episodes, seed, device, out):
    rng = np.random.default_rng(reseed(seed, "g1-bind2hop"))
    sep = vocab
    rows, accs = [], []
    for ep in range(episodes):
        ks = rng.choice(vocab, size=3, replace=False)
        k1, k2, v = int(ks[0]), int(ks[1]), int(ks[2])
        prefix = [k1, k2, k2, v, sep, k1]
        p1, _ = greedy_next(model, prefix, device)
        p2, _ = greedy_next(model, prefix + [p1], device)
        ok = int(p1 == k2 and p2 == v)
        rows.append({"episode": ep, "k1": k1, "k2": k2, "v": v,
                     "pred1": p1, "pred2": p2, "correct": ok})
        accs.append(ok)
    write_csv(f"{out}/g1_bind2hop_seed{seed}.csv",
              ["episode", "k1", "k2", "v", "pred1", "pred2", "correct"], rows)
    return float(np.mean(accs))


def main(argv=None):
    p = argparse.ArgumentParser(description="G1 synthetic recall harness")
    add_common_args(p)
    p.add_argument("--task", default="all",
                   choices=["mqar", "induction", "copying", "bind2hop", "all"])
    p.add_argument("--vocab", type=int, default=8192)
    p.add_argument("--n-pairs", default="16,64,256")
    p.add_argument("--episodes", type=int, default=1000)
    p.add_argument("--gap", default="16,64,256")
    p.add_argument("--copy-len", default="32,128,512")
    p.add_argument("--batch", type=int, default=1,
                   help="episodes per progress flush; decode is greedy batch-1 "
                        "(batched greedy decode is M2 work)")
    p.add_argument("--window", type=int, default=None,
                   help="eval sliding-window W for p1/p2/p3/p4/p5 arms; default inherits "
                        "the checkpoint's train window (fails if --config "
                        "disagrees with the checkpoint and no override is given)")
    a = p.parse_args(argv)
    if a.batch < 1:
        raise SystemExit("--batch must be >= 1")
    if a.vocab < 16:
        raise SystemExit("--vocab must be >= 16")
    if a.window is not None and a.window < 0:
        raise SystemExit("--window must be >= 0")
    reseed(a.seed, f"init-{a.model}")  # deterministic init before any torch draws
    overrides = {"vocab_size": a.vocab + 2}
    family = a.model.split("-", 1)[0]
    if a.window is not None and family not in ("p1", "p2", "p3", "p4", "p5"):
        raise SystemExit("--window applies to p1/p2/p3/p4/p5 arms only (transformer has no window)")
    if family in ("p1", "p2", "p3", "p4", "p5"):
        # A2 guard: the eval window must match the checkpoint's train window
        # unless explicitly overridden; silently evaluating a W0/W32
        # checkpoint as W16 invalidates the ablation (M2 review finding).
        ckpt_window, cfg_window = None, None
        if a.checkpoint:
            blob = torch.load(a.checkpoint, map_location="cpu", weights_only=False)
            if isinstance(blob, dict):
                ckpt_window = (blob.get("config") or {}).get("window")
        if a.config:
            import yaml
            with open(a.config) as f:
                cfg_window = (yaml.safe_load(f) or {}).get("window")
        if a.window is not None:
            overrides["window"] = a.window
        else:
            if ckpt_window is not None:
                if cfg_window is not None and cfg_window != ckpt_window:
                    raise SystemExit(
                        f"--config window {cfg_window} != checkpoint train window "
                        f"{ckpt_window}; pass --window explicitly to override")
                overrides["window"] = ckpt_window
            elif cfg_window is not None:
                overrides["window"] = cfg_window
    model, cfg, random_init = load_model(a.model, a.checkpoint, a.config,
                                         overrides, a.device, a.dtype)
    info = env_info()
    info["dtype"] = a.dtype
    summary = {"model": a.model, "config": cfg, "seed": a.seed,
               "params_no_embed": param_count_no_embed(model),
               "episodes": a.episodes, "random_init": random_init, "env": info}
    tasks = ["mqar", "induction", "copying", "bind2hop"] if a.task == "all" else [a.task]
    if "mqar" in tasks:
        summary["mqar"] = {}
        for n in parse_int_list(a.n_pairs):
            acc, rk1, rk3, cnt = run_mqar(model, cfg, a.vocab, n, a.episodes,
                                          a.seed, a.device, a.out)
            summary["mqar"][n] = {"acc": acc, "recall@1": rk1, "recall@3": rk3, "n": cnt}
    if "induction" in tasks:
        summary["induction"] = run_induction(model, cfg, a.vocab, parse_int_list(a.gap),
                                             a.episodes, a.seed, a.device, a.out)
    if "copying" in tasks:
        summary["copying"] = run_copying(model, cfg, a.vocab, parse_int_list(a.copy_len),
                                         a.episodes, a.seed, a.device, a.out)
    if "bind2hop" in tasks:
        summary["bind2hop"] = {"acc": run_bind2hop(model, cfg, a.vocab, a.episodes,
                                                   a.seed, a.device, a.out)}
    write_json(f"{a.out}/g1_summary_seed{a.seed}.json", summary)
    print(f"wrote {a.out}/g1_summary_seed{a.seed}.json")


if __name__ == "__main__":
    main()
