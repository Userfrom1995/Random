"""Poolduel M1+M2 command line. No interactive prompts; all via flags."""

import argparse
import json
import os
import sys

from .cells import ARMS, M1_CELLS, get_cell
from .chunk import (CHUNKS, chunk_cells, filter_completed, load_manifest,
                    round_robin_schedule, save_manifest)
from .m2 import (M2_CHUNKS, M2_NA_ROWS, m2_cell, m2_cell_ids, m2_chunk_arms,
                 m2_chunk_cells)
from .runner import run_plan, write_medians


def build_parser():
    p = argparse.ArgumentParser(
        description="Poolduel harness: shared pgbench procedure, "
                    "pooler-blind arms. M1 transaction sweep plus "
                    "M2 modes/I-O/workload twins.")
    p.add_argument("--matrix", default="m1", choices=("m1", "m2"),
                   help="which matrix to run (default: m1)")
    p.add_argument("--cells", default="",
                   help="comma-separated cell ids (default: all in matrix)")
    p.add_argument("--arms", default=",".join(ARMS),
                   help="comma-separated arms, M1 only "
                        "(default: all six; M2 rows carry their own arm)")
    p.add_argument("--repeats", type=int, default=0,
                   help="override repeats per cell (0 = per-cell default)")
    p.add_argument("--chunk", default="",
                   help="run one chunk instead of --cells "
                        "(M1: a1,a2,b1,b2,c,d,e,f,g; "
                        "M2: m2a1..m2i2)")
    p.add_argument("--pilot", action="store_true",
                   help="pilot only: M1-1 + M1-2, one repeat per arm; "
                        "with --matrix m2: m2a1 rows, one repeat")
    p.add_argument("--list-m2", action="store_true",
                   help="print the M2 variant table plus N/A rows and exit")
    p.add_argument("--write-na", action="store_true",
                   help="with --matrix m2: emit N/A JSON records for "
                        "unsupported rows into --out/raw and exit")
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
    if args.matrix == "m2":
        if args.chunk:
            return m2_chunk_cells(args.chunk)
        if args.cells.strip():
            ids = [c.strip() for c in args.cells.split(",") if c.strip()]
            return [m2_cell(cid) for cid in ids]
        if args.pilot:
            return m2_chunk_cells("m2a1")
        return [m2_cell(cid) for cid in m2_cell_ids()]
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


def m2_direct_cell(row_cell):
    """Control twin of an M2 row: same geometry, direct arm, no variant."""
    cell = dict(row_cell)
    cell["arm"] = "direct"
    cell["variant"] = {}
    return cell


def m2_plan(cells, repeats_per_cell=None):
    """Build a round-robin plan from M2 rows.

    Each row runs its own arm plus the direct control on the same geometry
    (same-runner discipline). Order interleaves per repeat index so no arm
    blocks a whole repeat.
    """
    plan = []
    reps_of = {}
    for cell in cells:
        reps = (repeats_per_cell if repeats_per_cell is not None
                else cell.get("repeats", 3))
        reps_of[cell["cell_id"]] = list(range(1, reps + 1))
    max_rep = max((len(v) for v in reps_of.values()), default=0)
    for rep in range(1, max_rep + 1):
        for cell in cells:
            if rep not in reps_of[cell["cell_id"]]:
                continue
            plan.append((cell, cell["arm"], rep))
            plan.append((m2_direct_cell(cell), "direct", rep))
    return plan


def print_m2_table():
    from .m2 import (GEOMETRIES, M2_CHUNK_DESCRIPTIONS, M2_ROWS,
                     m2_budget_table)
    for (cid, geom, arm, variant) in M2_ROWS:
        g = GEOMETRIES[geom]
        print("%s %s %s c=%d pool=%d %s%s variant=%s" % (
            cid, arm, geom, g["clients"], g["pool_size"], g["workload"],
            " prepared" if g["protocol"] == "prepared" else "",
            variant or "{}"))
    print("--- N/A (unsupported, nulls, zero time) ---")
    for (cid, geom, arm, reason) in M2_NA_ROWS:
        print("%s %s %s N/A: %s" % (cid, arm, geom, reason))
    print("--- chunks ---")
    for name in sorted(M2_CHUNKS):
        print("%s: %s" % (name, M2_CHUNK_DESCRIPTIONS[name]))
    print("--- realized measured rows per pooler ---")
    print(json.dumps(m2_budget_table(), sort_keys=True))


def write_na_records(out_dir, threads=4, seed=42, pg_version="PG 17"):
    """Emit schema-valid N/A JSON records for unsupported M2 rows."""
    import copy

    from .m2 import GEOMETRIES
    from .runner import PG_CONFIG_BASELINE
    from .schema import make_na_record, validate_cell
    raw_dir = os.path.join(out_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)
    written = []
    for (cid, geom, arm, reason) in M2_NA_ROWS:
        g = GEOMETRIES[geom]
        cell = {"cell_id": cid, "workload": g["workload"],
                "clients": g["clients"], "pool_size": g["pool_size"],
                "protocol": g["protocol"], "churn": g["churn"],
                "duration_s": 60, "warmup_s": 30}
        config = ("# N/A (unsupported): %s has no %s arm here (%s); "
                  "see poolduel/docs/modes.md" % (arm, cid, reason))
        rec = make_na_record(cell, arm, config, pg_version,
                             copy.deepcopy(PG_CONFIG_BASELINE),
                             threads, 1, seed)
        errs = validate_cell(rec)
        if errs:
            raise SystemExit("N/A record invalid: %s" % "; ".join(errs))
        fname = os.path.join(raw_dir, "%s-%s-na.json" % (cid, arm))
        with open(fname, "w") as f:
            json.dump(rec, f, indent=2, sort_keys=True)
        written.append(fname)
    return written


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
    if args.list_m2:
        print_m2_table()
        return 0
    if args.write_na:
        if args.matrix != "m2":
            parser.error("--write-na needs --matrix m2")
        written = write_na_records(
            args.out, threads=args.threads, seed=args.seed,
            pg_version=args.pg_version)
        print("wrote %d N/A records -> %s/raw" % (len(written), args.out))
        return 0
    if args.matrix == "m2" and args.arms != ",".join(ARMS):
        parser.error("--arms is M1-only; M2 rows carry their own arm")
    cells = resolve_cells(args)
    repeats = args.repeats if args.repeats > 0 else None
    if args.pilot:
        repeats = 1
    if args.matrix == "m2":
        plan = m2_plan(cells, repeats_per_cell=repeats)
        arms = sorted({arm for (_, arm, _) in plan})
    else:
        arms = resolve_arms(args)
        plan = round_robin_schedule(cells, arms, repeats_per_cell=repeats)
    manifest = load_manifest(args.out)
    plan = filter_completed(plan, manifest)
    if args.dry_run:
        for (cell, arm, rep) in plan:
            variant = cell.get("variant") or {}
            print("%s %s r%d T=%d c=%d pool=%d %s%s%s" % (
                cell["cell_id"], arm, rep, cell["duration_s"],
                cell["clients"], cell["pool_size"], cell["workload"],
                " prepared" if cell["protocol"] == "prepared" else "",
                " %s" % (variant,) if variant else ""))
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
