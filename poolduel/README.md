# Poolduel

Exhaustive PostgreSQL pooler shootout: pgagroal vs PgBouncer vs pgpool-II vs
Odyssey vs pgcat, plus direct-PG control. Supavisor deferred with reason.
Tracks issue #302. Report entrypoint (M3): `/poolduel/index.html`.

## Docs (Researcher spec, committed before any sweep)

- `docs/modes.md`: pooling modes and I/O backends per pooler.
- `docs/test-matrix.md`: M1/M2 cell lists, budget parity, pilot gate.
- `docs/grid.md`: numeric knob ranges and iso-region axes.
- `docs/methodology.md`: pgbench yardstick, metrics, threats to validity.
- `docs/versions.md`: pinned versions and SHAs.
- `docs/configs/`: verbatim baselines with doc citations.
- `docs/supavisor-deferral.md`: why Supavisor waits for its own milestone.
- `docs/harness-contract.md`: identical adapter contract and JSON schema.
- `SPEC.md`: Researcher handoff to the Architect.

## Repro (M1 harness landed)

`repro.sh` replays the matrix with one command (identical procedure code).
No interactive prompts; everything via flags or env.

```sh
./poolduel/repro.sh --pilot    # M1-1 + M1-2, one repeat per arm (default)
./poolduel/repro.sh --full     # all 9 M1 chunks (a1,a2,b1,b2,c,d,e,f,g)
./poolduel/repro.sh --dry-run  # print the pilot plan, run nothing
THREADS=4 OUT=poolduel/results/m1 ./poolduel/repro.sh --full
```

Requires `pgbench` plus `psql` from PostgreSQL 17. `repro.sh` runs
`poolduel/harness/check.py` first (binaries, ratio guards, chunk caps)
and fails loudly instead of running a compromised sweep.

## Harness (M1)

Python 3, stdlib only, driving pgbench as a subprocess:

- `harness/cells.py`: M1 table (7 cells) as DATA plus the 5x ratio guard.
- `harness/pgbench.py`: identical-flags argv builder, stdout parser
  (tps without initial connection time, latency avg/stddev, failed),
  offline p50/p90/p99/p999 from per-transaction logs with the 200 MB
  sampling guard, 1% failure reject rule, SQLSTATE 26000 detection.
- `harness/stats.py`: median/min/max/CV plus the binding gate
  (non-overlapping bands AND same-direction tps + p99 agreement,
  else inconclusive) and the pilot separation check.
- `harness/schema.py`: normative cell JSON validator (exact fields,
  extra per-pooler fields forbidden, N/A rows carry nulls never zeros).
- `harness/chunk.py`: 9 chunks (flagship cells split into repeat-halves
  so every chunk stays under 60 min), round-robin scheduler, resume
  manifest, per-chunk direct-control injector.
- `harness/runner.py`: shared procedure (warmup, measure, caps 8/12 min,
  log collect, medians). Owns all timeouts; adapters never do.
- `harness/cli.py`: `python3 -m poolduel.harness.cli --chunk a1`,
  `--pilot`, `--cells M1-2,M1-3`, `--dry-run`. See `--help`.
- `harness/adapters/`: one pooler-blind adapter per arm
  (`direct`, `pgagroal`, `pgbouncer`, `pgpool`, `odyssey`, `pgcat`).
  Only `config_text()` and the port differ. Ports: direct 5432,
  pgagroal 6432, pgbouncer 6433, pgpool 6434, odyssey 6435, pgcat 6436.
- `tests/`: 26 stdlib unittests (`python3 -m unittest discover
  -s poolduel/tests`).
- `.github/workflows/poolduel-m1.yml`: 9-chunk CI sweep, manual dispatch
  only, pinned PG 17 plus pinned pooler builds, per-chunk artifacts.

## Repro (Architect and Builder deliver in M1)

`repro.sh` replays the matrix with one command. Until M1 lands, this file is
the placeholder the build fills in.

```sh
#!/bin/sh
# Poolduel one-command repro. M1 implements this script.
set -eu
echo "poolduel repro: harness lands in M1 (Refs #302)"
```

- Dr. Mob, the Researcher
