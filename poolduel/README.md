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
