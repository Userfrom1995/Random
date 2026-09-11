"""Preflight check for poolduel/repro.sh: versions, binaries, ratio guards.

Fails loudly (non-zero exit) instead of running a compromised sweep.
Covers the M1 matrix (cells, chunks) and the M2 matrix (variants, chunks,
chunk coverage, N/A schema validity).
"""

import shutil
import sys

from poolduel.harness.cells import validate_all_ratios
from poolduel.harness.chunk import check_chunk_budgets, CHUNKS
from poolduel.harness.m2 import (M2_CHUNKS, M2_NA_ROWS, check_m2_chunk_budgets,
                                 m2_cell_ids, validate_m2_ratios)


def check_m2_coverage():
    """Every M2 row lives in exactly one chunk."""
    from poolduel.harness.m2 import M2_CHUNKS
    seen = {}
    errors = []
    for chunk, ids in M2_CHUNKS.items():
        for cid in ids:
            if cid in seen:
                errors.append("M2 cell %s in chunks %s and %s"
                              % (cid, seen[cid], chunk))
            seen[cid] = chunk
    missing = set(m2_cell_ids()) - set(seen)
    if missing:
        errors.append("M2 cells missing from chunks: %s" % sorted(missing))
    return errors


def check_m2_na_schema():
    """Every M2 N/A row renders a schema-valid nulls record."""
    import copy

    from poolduel.harness.m2 import GEOMETRIES, M2_NA_ROWS
    from poolduel.harness.runner import PG_CONFIG_BASELINE
    from poolduel.harness.schema import make_na_record, validate_cell
    errors = []
    for (cid, geom, arm, reason) in M2_NA_ROWS:
        g = GEOMETRIES[geom]
        cell = {"cell_id": cid, "workload": g["workload"],
                "clients": g["clients"], "pool_size": g["pool_size"],
                "protocol": g["protocol"], "churn": g["churn"],
                "duration_s": 60, "warmup_s": 30}
        rec = make_na_record(cell, arm, "N/A: %s" % reason, "PG 17",
                             copy.deepcopy(PG_CONFIG_BASELINE), 4, 1, 42)
        errs = validate_cell(rec)
        if errs:
            errors.append("%s/%s N/A invalid: %s" % (cid, arm, "; ".join(errs)))
    return errors


def main():
    errors = []
    for binary in ("pgbench", "psql"):
        if shutil.which(binary) is None:
            errors.append("missing required binary: %s" % binary)
    try:
        validate_all_ratios()
    except ValueError as exc:
        errors.append(str(exc))
    over = check_chunk_budgets()
    if over:
        errors.append("chunks over 60 min cap: %s" % over)
    if not CHUNKS:
        errors.append("no chunks defined")
    try:
        validate_m2_ratios()
    except (ValueError, KeyError) as exc:
        errors.append("M2 ratio/cell error: %s" % exc)
    over2 = check_m2_chunk_budgets()
    if over2:
        errors.append("M2 chunks over 60 min cap: %s" % over2)
    if not M2_CHUNKS:
        errors.append("no M2 chunks defined")
    errors.extend(check_m2_coverage())
    errors.extend(check_m2_na_schema())
    if errors:
        for err in errors:
            print("poolduel check FAILED: %s" % err)
        return 1
    print("poolduel check ok: pgbench present, 7 M1 cells ratio-clean, "
          "%d M1 chunks under cap, %d M2 rows ratio-clean, "
          "%d M2 chunks under cap, %d N/A rows schema-valid"
          % (len(CHUNKS), len(m2_cell_ids()), len(M2_CHUNKS),
             len(M2_NA_ROWS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
