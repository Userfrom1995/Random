# Progress: poolduel build (issue #302)

Status: in-progress
Date: 2026-09-11. Owner directive via #42 (supreme priority).
Blueprint: `ideas/2026-09-11-poolduel.md`. Researcher spec: `poolduel/docs/`.

Active Milestone: M1 (Complete, ready for review)

## Milestone roadmap

- Milestone 1 (M1 harness + transaction sweep): [x] Python harness
  (`runner`, `pgbench`, `cells`, `stats`, `schema`, `chunk`, `cli`,
  `check`) with 6 pooler-blind adapters; [x] M1-1..M1-7 cell table with
  pilot gate proof (`pilot_separates` + `--pilot` dry-run plan);
  [x] per-cell caps (8 min standard, 12 flagship) + JSON schema
  validation; [x] working `repro.sh` (`--pilot`/`--full`/`--dry-run`
  plus preflight `check.py`); [x] chunked CI workflow (9 chunks,
  each with own direct control, each under 60 min, manual dispatch).
  (PR 1 target, Refs #302)
- Milestone 2 (M2 modes + I/O + extra workloads): [ ] session arms;
  [ ] statement arms (PgBouncer + provisional Odyssey, rest N/A);
  [ ] I/O axes (io_uring/epoll, so_reuseport, workers, worker_threads,
  pgpool children sweep); [ ] extra workload twins. (PR 2 target, Refs #302)
- Milestone 3 (report + audit): [ ] static Pages report at
  `/poolduel/index.html`; [ ] full M1+M2 medians with bands, iso-region
  slices, threats section; [ ] Tester independent cell reproduction;
  [ ] one-command repro green. (Final PR, Closes #302 only on passing
  binding gates: non-overlapping bands plus tps/p99 agreement; negative
  or marginal results stay Refs with logged ledger.)

## Done

- Researcher spec committed before any sweep (modes, matrix, grid,
  methodology, versions, 5 verbatim configs, supavisor deferral,
  harness contract, SPEC, README, repro placeholder).
- Architect blueprint written (`ideas/2026-09-11-poolduel.md`):
  Python harness language choice, adapter layout, chunked workflow,
  Pages skeleton, M1 plan with pilot gate and budget parity.
- Builder M1 (2026-09-11): full harness implemented, 26/26 unittests
  green, `repro.sh --dry-run` verified, 9-chunk workflow YAML parses.
  Design correction worth recording: the blueprint's "4+ chunks by
  workload pair" does not fit the 60 min cap (a flagship full cell is
  ~90 min for 5 repeats x 6 arms x 3 min per arm-run), so flagship
  cells split into repeat-halves (a1/a2, b1/b2) for 9 chunks total,
  worst chunk 54 min. Still compliant ("at least 4 chunks", per-chunk
  direct control, under-60-min). No sweep numbers claimed: CI has not
  run the matrix yet, so no medians, no rankings, no gates passed.
- Infra note (2026-09-11): the M1 sweep workflow is written and
  YAML-valid but staged at `poolduel/ci/poolduel-m1.yml`, NOT at
  `.github/workflows/`: the build token (GitHub App) is refused
  workflow-scope pushes ("without `workflows` permission"). Promotion
  is one mechanical `git mv` via a PAT-backed step (`/oc lab` route)
  or an owner push; content is final, no edits needed. The M1 sweep
  cannot be dispatched until that promotion lands.

Current step: M1 implementation complete, awaiting review
Next steps: Reviewer audit, then Tester sample-cell reproduction;
  M2 session/statement/I-O arms in the next milestone PR.

Refs #302. No Closes: M2 report and M3 binding gates remain.

- the Builder
