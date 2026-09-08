# PostFormer M4e: toy envelope audit (2026-09-08)

## What

M4e consolidates every CPU-feasible toy probe (M1-M4d) into one honest
scoreboard so the Reviewer can re-gate the full head (M4b/c/d landed after
the last review at a7553d5c). No new training: this milestone is docs-only
plus static viewer validation.

## Files

- `postformer/docs/envelope-audit.md`: the audit. One table over all 20
  trained toy rows (ledger rows 5-24) with exact mqar8/N16/2hop cells taken
  from `ledger.csv`, plus ablation verdicts (A1 unresolved, A2 invalid pre-fix
  with A2-re no-advantage, A3 unresolved, A4 slots-help-but-count-untested,
  A6 floor, A7 split) and H1-H5 first reads (H4 NEGATIVE at toy, rest open).
- `postformer/viewer/index.html`: banner now names the M1-M4d envelope and
  links the audit doc.
- `postformer/README.md`: header (M4e, 102 tests), new M3/M4b/A4/A6 probe
  section, layout row counts.

## Validation (torch 2.14 CPU, this run)

- Full suite: 102 passed (no new tests; docs-only milestone).
- `ledger check` green on 24 rows.
- Viewer static check: replicated the page's RFC-4180 `splitCSV` in Python
  over the live 24-col ledger - header parses to 24 cols, every row parses
  to 24 cells, quoted-commas notes column stays intact (naive split would
  shred it). No browser on the runner, so the Playwright snapshot stays
  deferred.

## Why this shape

S-tiny/S-small trained gates remain GPU-blocked (~50+h/arm on CPU, measured
2026-09-08). The audit is the last CPU-feasible milestone: it freezes the
toy narrative in one place with no inflated claims, so S-tiny work starts
from a clean, reviewed baseline. `Refs #294` kept; `Closes #294` only on
G1+G2+G3+G4-tier-a/b head-to-head at scale.
