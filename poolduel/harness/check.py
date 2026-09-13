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


def check_m8_calibration():
    """M8 calibration specs are coherent (warmup, pilot, breadth).

    Returns error strings (empty when the specs hold).
    """
    from poolduel.harness import calibrate as calibrate_mod
    from poolduel.harness import workloads as workloads_mod
    errors = []
    if 30 not in calibrate_mod.WARMUP_CANDIDATES:
        errors.append("M8 warmup curve must include the 30 s provisional")
    if sorted(calibrate_mod.WARMUP_CANDIDATES) != sorted(
            set(calibrate_mod.WARMUP_CANDIDATES)):
        errors.append("M8 warmup candidates must be distinct")
    try:
        cells = calibrate_mod.scale100_pilot_cells()
    except (ValueError, KeyError) as exc:
        return ["M8 scale-100 pilot error: %s" % exc]
    if len(cells) < 2:
        errors.append("M8 scale-100 pilot needs at least two cells")
    for cell in cells:
        if cell.get("scale") != 100:
            errors.append("M8 pilot cell %s must be scale 100, got %r"
                          % (cell.get("cell_id"), cell.get("scale")))
    for workload in workloads_mod.SCRIPT_WORKLOADS:
        try:
            sql = workloads_mod.script_sql(workload)
        except KeyError as exc:
            errors.append("M8 script workload error: %s" % exc)
            continue
        if not sql.strip():
            errors.append("M8 script workload %s renders empty SQL"
                          % workload)
    if not workloads_mod.PIPELINE_FORBIDDEN_REASON.strip():
        errors.append("M8 pipeline forbidden reason must be written")
    return errors


def check_supavisor_budget():
    """M9 Supavisor budget equals the matrix maximum (plan section 8).

    Equal cell budget is structural: Supavisor must run every geometry
    any other arm runs. Returns error strings (empty when parity holds).
    """
    from poolduel.harness.supavisor import budget_parity_ok
    ok, detail = budget_parity_ok()
    if ok:
        return []
    return ["Supavisor M9 budget parity broken: %s" % detail]


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
    errors.extend(check_supavisor_budget())
    errors.extend(check_m8_calibration())
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
