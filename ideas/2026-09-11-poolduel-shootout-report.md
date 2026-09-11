# Poolduel: exhaustive PostgreSQL pooler shootout plus publication report

Refs #302 (owner directive via #42, supreme priority). M3 milestone branch
`opencode/issue302-poolduel-m3`: the publication layer on top of the M1
(transaction pooling) and M2 (session/statement/I-O arms) harness.

## What was built (M3)

- `poolduel/harness/report.py`: stdlib-only publication engine. `load_raw`
  reads raw per-repeat JSON from any number of results dirs with schema
  validation (bad records reported, never silently dropped); `aggregate`
  groups into medians with min-max bands and CV plus measurement context in
  the runner-compatible shape; `per_cell_best` ranks arms per cell with
  binding-gate verdicts (`stats.compare_pair`: non-overlapping bands AND
  same-direction tps/p99, else inconclusive); `pairwise` covers every arm
  pair; `iso_regions` groups on the shared axes (workload, clients, backends,
  duration, protocol, churn); `flatness` reports flat/peaky/single-point over
  each pooler's own configs; `matrix_csv` exports every measured and N/A cell
  (nulls/empty, never zeros); `build_bundle`/`write_outputs` emit
  `results/m1/medians.json`, `results/m1/matrix.csv`, `results/m2/...`, and
  `results/report.json`. The CLI fails loudly on missing/empty results.
- `poolduel/index.html`: full M1+M2 publication report. Lineup with pins,
  both normative matrices, verbatim pilot plan, pending-honest M1 results
  table plus client-side SVG bar charts with min-max whiskers, M2
  best-vs-best table, iso-region and flatness blocks, fairness summary,
  full threats-to-validity text, repro commands. All data sections fill live
  from `results/` artifacts and stay pending (never zero-filled) until the
  sweeps publish them.
- `poolduel/docs/results.md`: normative reading guide (median math, binding
  gate, best-vs-best plus iso-region method, flatness, N/A/timeout semantics,
  CSV/JSON schemas).
- `poolduel/docs/fairness-audit.md`: per-pooler non-default re-check against
  upstream tuning docs with verdicts, published budget parity
  (pgagroal 11, PgBouncer 12, Odyssey 11, pgcat 9, pgpool-II 9), anti-theater
  checklist with pre-sweep pass complete and post-sweep gate blocking.
- `poolduel/tests/test_report.py`: 17 tests on synthetic fixtures (never
  claimed as measured): aggregation, N/A handling, verdicts, iso matching,
  flatness, CSV shape, CLI success and loud failure. 100/100 green total.
- `repro.sh --report`: one-command artifact build over every committed
  results dir; fails loudly with no sweep data. Also fixed a `--m2-full`
  progress echo that printed the wrong variable.
- Root `index.html` plus root `README.md`: Poolduel listed as in-progress
  (issue #302 open) without touching existing entries.

## Why

M3 is the acceptance surface the issue demands: report live at `/poolduel/`,
configs verbatim, full matrix CSVs/JSON, fairness audit pass,
threats-to-validity, repro verification, Pages deploy green. The pipeline
deliberately claims zero numbers before the CI sweeps run: every gate
(non-overlapping bands plus tps/p99 agreement) evaluates only on committed
sweep data, and negative or marginal results stay `Refs` with a logged
ledger, never `Closes`.

## Key files

- `poolduel/harness/report.py`, `poolduel/tests/test_report.py`
- `poolduel/index.html`, `poolduel/docs/results.md`,
  `poolduel/docs/fairness-audit.md`
- `poolduel/repro.sh`, `poolduel/README.md`, `progress/302-poolduel.md`

## Notes

- M1 pilot dry-run and M2 312-run dry-run plans verified byte-stable;
  M1/M2 sweep dispatch remains manual via `.github/workflows/poolduel-m*.yml`.
- Post-sweep work (not this PR): commit raw JSON plus medians, Tester
  reproduces one sample cell, Reviewer re-checks configs against the audit,
  then gates decide `Refs` vs `Closes`.

- the Builder
