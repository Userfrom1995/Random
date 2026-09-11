# Progress: poolduel build (issue #302)

Status: in-progress
Date: 2026-09-11. Owner directive via #42 (supreme priority).
Blueprint: `ideas/2026-09-11-poolduel.md`. Researcher spec: `poolduel/docs/`.

Active Milestone: M1

## Milestone roadmap

- Milestone 1 (M1 harness + transaction sweep): [ ] Python harness
  (`runner`, `pgbench`, `cells`, `stats`, `schema`, `chunk`) with 6
  pooler-blind adapters; [ ] M1-1..M1-7 sweep with pilot gate proof;
  [ ] per-cell caps + JSON schema validation; [ ] working `repro.sh`;
  [ ] chunked CI workflow (4+ chunks, own control each, under 60 min).
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

Current step: Ready for initial build (Milestone 1)
Next steps: Builder to implement Milestone 1 with real code and zero stubs

Refs #302. No Closes: implementation milestones M1-M3 remain.

- the Architect
