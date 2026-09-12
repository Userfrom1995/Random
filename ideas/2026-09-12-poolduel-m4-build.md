# Poolduel M4 build: per-pooler deep-dives plus ECharts charts

Refs #302 (M4 blueprint `ideas/2026-09-12-poolduel-m4.md`). Milestone
branch family `opencode/issue302-*`. No `Closes` without explicit
@Userfrom1995 approval.

## What was built

Five per-pooler deep-dive pages plus a full comparison surface on the
main `/poolduel/` page, all charted with in-repo ECharts 5.5.1 (SVG
renderer, offline-clean), every figure generated from committed report
bundles by committed code.

## Key files

- `poolduel/vendor/echarts-5.5.1/dist/echarts.min.js` + `LICENSE` +
  `poolduel/vendor/VERSION` (pin 5.5.1, dist URL, sha256).
- `poolduel/harness/charts.py` (stdlib only): `build_options(m1, m2,
  bundle)` returns per-page option dicts; CLI `--out
  poolduel/results/charts` writes one JSON per page plus `manifest.json`
  (source SHAs). Loud failure on missing inputs. Min-max bands are
  dashed min/max `line` series (a `custom` series would need a JS
  function that cannot live in JSON); N/A and timeout cells are explicit
  scatter markers, never zero-filled; every yAxis starts at zero.
- `poolduel/assets/poolduel-charts.js`: single loader for all six pages
  (`echarts.init(el, null, {renderer: "svg"})`, fetches page option
  JSON, no inline data); passes `node --check`.
- `poolduel/<pooler>/index.html` (five files, one template): seven fixed
  sections; strengths/limits are derived strings computed live from
  `report.json` ranked verdicts (best/inconclusive/loss/N/A/timeout
  counts), never free prose.
- `poolduel/index.html`: section 6b with 8 comparison figures, published
  banner, deep-dive nav.
- `poolduel/tests/test_charts.py`: Tier-1 gate, 17 tests green.
- `poolduel/ci/vision-shots.sh`: Tier-2 loop wiring (serves repo root,
  headless Chromium screenshots of all six pages to /tmp).
- `poolduel/docs/fairness-audit.md` section 5: post-sweep re-check.

## Verification

- Full suite 179/179 green (162 pre-existing + 17 new).
- Tier-0 vision probe PASS: headless screenshot read back, known median
  M1-1 direct 25405.035073 visible on the rendered page.
- Tier-2 render proven: dump-dom shows ECharts SVG blocks with real axis
  labels and series names on all six pages; per-cell PNG value reads are
  the Tester's blocking job at test phase.
- `repro.sh --charts` (report then charts) green; `--dry-run` intact.

## Notes

- Shared palette (Okabe-Ito): pgagroal `#D55E00`, PgBouncer `#56B4E9`,
  pgpool-II `#E69F00`, Odyssey `#009E73`, pgcat `#CC79A7`, direct
  `#9AA7B4`, N/A `#484F58`.
- Timeouts stay honest findings: pgcat M2 7 and pgagroal M2 7 render as
  marked triangle points on every chart.

- the Builder
