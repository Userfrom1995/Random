# Progress: poolduel build (issue #302)

Status: in-progress
Date: 2026-09-11. Owner directive via #42 (supreme priority).
Blueprint: `ideas/2026-09-11-poolduel.md`. Researcher spec: `poolduel/docs/`.

Active Milestone: M3 (in progress on `opencode/issue302-poolduel-m3`)

## Milestone roadmap

- Milestone 1 (M1 harness + transaction sweep): [x] Python harness
  (`runner`, `pgbench`, `cells`, `stats`, `schema`, `chunk`, `cli`,
  `check`) with 6 pooler-blind adapters; [x] M1-1..M1-7 cell table with
  pilot gate proof (`pilot_separates` + `--pilot` dry-run plan);
  [x] per-cell caps (8 min standard, 12 flagship) + JSON schema
  validation; [x] working `repro.sh` (`--pilot`/`--full`/`--dry-run`
  plus preflight `check.py`); [x] chunked CI workflow (9 chunks,
  each with own direct control, each under 60 min, manual dispatch).
  (Merged as PR #303, Refs #302)
- Milestone 2 (M2 modes + I/O + extra workloads): [x] session arms
  (pgagroal session + performance, pgbouncer/odyssey/pgcat session,
  pgpool session-class); [x] statement arms (PgBouncer + provisional
  Odyssey, rest N/A with nulls); [x] I/O axes (io_uring/epoll,
  so_reuseport 2-instance, workers 1/2/4, worker_threads 1/5, pgpool
  children sweep with 200x4 corner substituted); [x] extra workload
  twins (simple-update + churn for session arms, prepared where
  supported). 52 measured rows + 7 N/A rows, 16 chunks each under
  60 min, `--list-m2` budget table published. (This PR, Refs #302)
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

Current step: M2 implementation complete, awaiting review
Next steps: Reviewer audit, then Tester sample-cell reproduction;
  M2 sweep dispatch needs PAT promotion of poolduel/ci/poolduel-m2.yml
  to .github/workflows/ (/oc lab route or owner push); M3 Pages report
  in the next milestone PR.

Builder follow-up (2026-09-11): added `poolduel/index.html` Pages report
skeleton closing the last open M1 spec item. Honest pending state: lineup
table with pins, normative M1 cell table, verbatim 12-line pilot dry-run
plan, results table with pending cells (fills live from
`results/medians.json` only after the sweep publishes it), fairness and
threats summary, repro commands. No numbers claimed, no zeros, no
interpolation. Also cleaned the stale README placeholder block and fixed
the test count (65) plus the promoted workflow path. Verified: 65/65
unittests green, HTML parses, page JS passes `node --check`, pilot dry-run
reproduces the embedded plan.

Builder M2 (2026-09-11): full M2 arms on branch
`opencode/issue302-poolduel-m2`. `harness/m2.py` variant table as DATA
(52 measured rows on 5 shared geometries reusing M1 shapes at standard
60 s/3-rep timing, 7 N/A rows with nulls), 16 chunks each under 60 min
with per-chunk direct control (worst 48 min). Adapters render the cell
`variant` dict (pgagroal pipeline/ev_backend, pgbouncer pool_mode plus
2-instance so_reuseport multi-proc start, odyssey pool/workers with
provisional statement label, pgcat pool_mode/worker_threads, pgpool
children sweep with the 200x4 corner substituted); M1 cells without a
variant render unchanged (65/65 M1 tests still green untouched).
CLI gains `--matrix m2`, `--list-m2`, `--write-na`; `check.py` covers M2
ratios, budgets, chunk coverage, N/A schema; `repro.sh` gains `--m2-*`
modes. M2 sweep workflow staged at `poolduel/ci/poolduel-m2.yml` for
PAT-backed promotion (same route M1 took). Parity: same procedure code,
same caps, at most 2 workloads per new arm per block, realized counts
published (`--list-m2`: pgagroal 11, pgbouncer 12, odyssey 11, pgcat 9,
pgpool 9; residual spread is structural and documented in
`m2_budget_table`). Verified: 83/83 unittests green, M1 pilot dry-run
byte-identical to the plan embedded in `index.html`, full M2 dry-run
plans 312 arm-runs, N/A emission schema-valid. No numbers claimed:
CI has not run either matrix yet. `index.html` untouched (M3 owns it).

Refs #302. No Closes: M2 report and M3 binding gates remain.

## M3 build log (branch `opencode/issue302-poolduel-m3`)

- M3-1 (2026-09-11): `harness/report.py` publication engine (stdlib
  only): `load_raw` with schema validation, `aggregate` medians with
  bands/CV plus measurement context (runner-compatible shape),
  `per_cell_best` best-vs-best with binding-gate verdicts,
  `pairwise` full verdict matrix, `iso_regions` shared-axes slices,
  `flatness` flat/peaky/single-point, `matrix_csv` full export,
  `build_bundle`/`write_outputs` (`m1/medians.json`,
  `m1/matrix.csv`, `m2/...`, `report.json` for the page live hooks).
  CLI fails loudly on missing/empty results (no invented numbers).
  `tests/test_report.py`: 17 new tests; 100/100 green total.

- the Builder
