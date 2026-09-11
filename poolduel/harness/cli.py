"""Poolduel M1 command line. No interactive prompts; everything via flags."""

import argparse
import json
import os
import sys

from .cells import ARMS, M1_CELLS, get_cell
from .chunk import (CHUNKS, chunk_cells, filter_completed, load_manifest,
                    round_robin_schedule, save_manifest)
from .runner import run_plan, write_medians


def build_parser():
    p = argparse.ArgumentParser(
        description="Poolduel M1 harness: shared pgbench procedure, "
                    "pooler-blind arms.")
    p.add_argument("--cells", default="",
                   help="comma-separated cell ids (default: all M1)")
    p.add_argument("--arms", default=",".join(ARMS),
                   help="comma-separated arms (default: all six)")
    p.add_argument("--repeats", type=int, default=0,
                   help="override repeats per cell (0 = per-cell default)")
    p.add_argument("--chunk", default="",
                   help="run one chunk (a1,a2,b1,b2,c,d,e,f,g) "
                        "instead of --cells")
    p.add_argument("--pilot", action="store_true",
                   help="pilot only: M1-1 + M1-2, one repeat per arm")
    p.add_argument("--threads", type=int, default=4)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--dbname", default="benchdb")
    p.add_argument("--user", default="benchuser")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--out", default="poolduel/results/m1",
                   help="output directory for raw JSON + medians")
    p.add_argument("--dry-run", action="store_true",
                   help="print the plan without executing anything")
    p.add_argument("--pg-version", default="PG 17")
    return p


def resolve_cells(args):
    if args.pilot:
        return [get_cell("M1-1"), get_cell("M1-2")]
    if args.chunk:
        return chunk_cells(args.chunk)
    if args.cells.strip():
        ids = [c.strip() for c in args.cells.split(",") if c.strip()]
        return [get_cell(cid) for cid in ids]
    return [dict(c) for c in M1_CELLS]


def resolve_arms(args):
    arms = [a.strip() for a in args.arms.split(",") if a.strip()]
    unknown = [a for a in arms if a not in ARMS]
    if unknown:
        raise SystemExit("unknown arms: %s (want %s)" % (unknown, ARMS))
    if "direct" not in arms:
        arms = ["direct"] + arms
    return arms


def load_adapters(arms):
    from .adapters import direct as direct_mod
    from .adapters import odyssey as odyssey_mod
    from .adapters import pgagroal as pgagroal_mod
    from .adapters import pgbouncer as pgbouncer_mod
    from .adapters import pgcat as pgcat_mod
    from .adapters import pgpool as pgpool_mod
    makers = {
        "direct": direct_mod.DirectAdapter,
        "pgagroal": pgagroal_mod.PgAgroalAdapter,
        "pgbouncer": pgbouncer_mod.PgBouncerAdapter,
        "pgpool": pgpool_mod.PgPoolAdapter,
        "odyssey": odyssey_mod.OdysseyAdapter,
        "pgcat": pgcat_mod.PgCatAdapter,
    }
    return {arm: makers[arm]() for arm in arms}


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.threads <= 0:
        parser.error("--threads must be positive")
    cells = resolve_cells(args)
    arms = resolve_arms(args)
    repeats = args.repeats if args.repeats > 0 else None
    if args.pilot:
        repeats = 1
    plan = round_robin_schedule(cells, arms, repeats_per_cell=repeats)
    manifest = load_manifest(args.out)
    plan = filter_completed(plan, manifest)
    if args.dry_run:
        for (cell, arm, rep) in plan:
            print("%s %s r%d T=%d c=%d pool=%d %s%s" % (
                cell["cell_id"], arm, rep, cell["duration_s"],
                cell["clients"], cell["pool_size"], cell["workload"],
                " prepared" if cell["protocol"] == "prepared" else ""))
        print("plan=%d out=%s" % (len(plan), args.out))
        return 0
    if not plan:
        print("nothing to do: manifest already complete at %s" % args.out)
        return 0
    os.makedirs(args.out, exist_ok=True)
    save_manifest(args.out, manifest)
    adapters = load_adapters(arms)
    records, errors = run_plan(
        plan, adapters, args.out, dbname=args.dbname, user=args.user,
        host=args.host, threads=args.threads, seed=args.seed,
        pg_version=args.pg_version)
    medians = write_medians(
        records, os.path.join(args.out, "medians.json"))
    summary = {"records": len(records), "errors": errors,
               "medians": len(medians), "out": args.out}
    with open(os.path.join(args.out, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
    for err in errors:
        print("ERROR: %s" % err, file=sys.stderr)
    print("wrote %d records, %d errors -> %s" % (
        len(records), len(errors), args.out))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
