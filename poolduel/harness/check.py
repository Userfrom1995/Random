"""Preflight check for poolduel/repro.sh: versions, binaries, ratio guards.

Fails loudly (non-zero exit) instead of running a compromised sweep.
"""

import shutil
import sys

from poolduel.harness.cells import validate_all_ratios
from poolduel.harness.chunk import check_chunk_budgets, CHUNKS


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
    if errors:
        for err in errors:
            print("poolduel check FAILED: %s" % err)
        return 1
    print("poolduel check ok: pgbench present, %d M1 cells ratio-clean, "
          "%d chunks under cap" % (7, len(CHUNKS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
