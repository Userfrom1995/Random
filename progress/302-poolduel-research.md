# Progress: poolduel research (issue #302)

Status: research complete, handoff to architect.
Date: 2026-09-11. Owner directive via #42 (supreme priority).

## Done

- Surveyed pgagroal, PgBouncer, pgpool-II, Odyssey, pgcat, Supavisor docs and
  source via four parallel subagents with doc URLs for every claim.
- Committed before any sweep: `poolduel/docs/modes.md`, `test-matrix.md`,
  `grid.md`, `methodology.md`, `versions.md`, `configs/` (5 poolers),
  `supavisor-deferral.md`, `harness-contract.md`, plus `poolduel/SPEC.md`,
  `poolduel/README.md`, `poolduel/repro.sh` placeholder.
- Defined identical adapter contract, cell JSON schema, CI-sized calibration
  (`-s 10`, warmup 30 plus measure 60/120, 3/5 repeats, caps 8/12 min),
  pilot discrimination gate, and anti-theater checklist.

## Next (Architect)

Read all of `poolduel/docs/`, choose harness language (Go/Python/Rust),
design adapter layout, chunked workflow (postformer pattern), Pages report
skeleton, and M1 milestone plan (transaction pooling across all five plus
control with pilot proof).

Refs #302. No Closes: implementation milestones M1-M3 remain.
