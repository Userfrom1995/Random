#!/bin/sh
# Poolduel one-command repro (M1). Replays the matrix with identical
# procedure code. Default is the pilot subset; --full runs all M1.
# No interactive prompts; everything via flags. Refs #302.
set -eu

THREADS="${THREADS:-$(nproc 2>/dev/null || echo 4)}"
OUT="${OUT:-poolduel/results/m1}"
MODE="${1:-}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "poolduel repro: python3 is required" >&2
  exit 2
fi
if ! command -v pgbench >/dev/null 2>&1; then
  echo "poolduel repro: pgbench is required (install PostgreSQL 17)" >&2
  exit 2
fi

python3 poolduel/harness/check.py

case "$MODE" in
  --full)
    for chunk in a1 a2 b1 b2 c d e f g; do
      echo "poolduel repro: chunk $chunk"
      python3 -m poolduel.harness.cli --chunk "$chunk" \
        --threads "$THREADS" --out "$OUT"
    done
    ;;
  --pilot | "")
    echo "poolduel repro: pilot (M1-1 + M1-2, one repeat per arm)"
    python3 -m poolduel.harness.cli --pilot \
      --threads "$THREADS" --out "$OUT-pilot"
    ;;
  --dry-run)
    python3 -m poolduel.harness.cli --pilot --dry-run
    ;;
  *)
    echo "usage: repro.sh [--pilot|--full|--dry-run]" >&2
    exit 2
    ;;
esac

echo "poolduel repro: done"
