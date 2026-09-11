#!/bin/sh
# Poolduel one-command repro (M1+M2). Replays the matrix with identical
# procedure code. Default is the M1 pilot subset; M2 rides --m2-* flags.
# No interactive prompts; everything via flags. Refs #302.
set -eu

THREADS="${THREADS:-$(nproc 2>/dev/null || echo 4)}"
OUT="${OUT:-poolduel/results/m1}"
M2OUT="${M2OUT:-poolduel/results/m2}"
MODE="${1:-}"
M2CHUNK="${2:-}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "poolduel repro: python3 is required" >&2
  exit 2
fi
if ! command -v pgbench >/dev/null 2>&1; then
  echo "poolduel repro: pgbench is required (install PostgreSQL 17)" >&2
  exit 2
fi

PYTHONPATH=. python3 poolduel/harness/check.py

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
  --m2-dry-run)
    python3 -m poolduel.harness.cli --matrix m2 --dry-run
    ;;
  --m2-smoke)
    echo "poolduel repro: M2 smoke (m2a1 session rows, one repeat per arm)"
    python3 -m poolduel.harness.cli --matrix m2 --pilot \
      --threads "$THREADS" --out "$M2OUT-smoke"
    ;;
  --m2-chunk)
    if [ -z "$M2CHUNK" ]; then
      echo "usage: repro.sh --m2-chunk <m2a1..m2i2>" >&2
      exit 2
    fi
    echo "poolduel repro: M2 chunk $M2CHUNK"
    python3 -m poolduel.harness.cli --matrix m2 --chunk "$M2CHUNK" \
      --threads "$THREADS" --out "$M2OUT-$M2CHUNK"
    ;;
  --m2-na)
    echo "poolduel repro: M2 N/A records (unsupported rows, nulls)"
    python3 -m poolduel.harness.cli --matrix m2 --write-na \
      --threads "$THREADS" --out "$M2OUT"
    ;;
  --m2-full)
    for chunk in m2a1 m2a2 m2b1 m2b2 m2c m2d1 m2d2 m2e m2f1 m2f2 \
                 m2g1 m2g2 m2h1 m2h2 m2i1 m2i2; do
      echo "poolduel repro: M2 chunk $chunk"
      python3 -m poolduel.harness.cli --matrix m2 --chunk "$chunk" \
        --threads "$THREADS" --out "$M2OUT-$chunk"
    done
    python3 -m poolduel.harness.cli --matrix m2 --write-na \
      --threads "$THREADS" --out "$M2OUT"
    ;;
  *)
    echo "usage: repro.sh [--pilot|--full|--dry-run]" >&2
    echo "       repro.sh [--m2-smoke|--m2-chunk <name>|--m2-na|" >&2
    echo "                --m2-dry-run|--m2-full]" >&2
    exit 2
    ;;
esac

echo "poolduel repro: done"
