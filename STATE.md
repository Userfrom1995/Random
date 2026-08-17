# STATE - Random factory checkpoint

- **Updated:** 2026-08-17 (~20:30Z event run 32065726348, owner `/oc maintainer`
  on PR #76). PR #76's Obsidian codec core is COMPLETE and branch-aligned
  (MERGEABLE); the owner's `/oc review` (20:25:25Z) has the Reviewer
  IN PROGRESS on the PR. This run is a status-only pass - no triggers
  dispatched, no duplicates.

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec (Kodak-benchmarked,
  vs JPEG XL / WebP).** OPEN, still the priority project. PR #76 carries the
  research + spec + architecture + the COMPLETE codec core (checklist 1-9):
  43 lib tests green, bit-exact round trips at efforts 0-7 over fuzz images,
  corrupt/truncated streams rejected, adaptive rANS lockstep fixed (forward
  dry-run + `put_fc`), causal predictor borders, effort-0 single global context
  per plane, measured model-size guard, `target/` artifacts untracked +
  `.gitignore`. Progress file `68-obsidian-lossless-image-codec.md` marks 1-9
  complete; next step = checklist 10 (benchmark harness + first Kodak row).

## In flight

- **PR #76 (Obsidian) - UNDER REVIEW.** Head `2a9489a` on
  `opencode/issue68-20260817120528`, 29 files, `mergeable: MERGEABLE`.
  Reviewer run **32065716177 in_progress** (owner's `/oc review`). A duplicate
  opencode-review run 32065726229 will self-skip (its job guard requires the
  comment to start with `/oc review`). On `/oc approve`: Tester auto-dispatches
  -> on `/oc approve-test`: MERGE + close #68. On `/oc fix`: Fixer applies
  findings, re-review via `/oc review`.

## Issues

- **#68 (Obsidian)** - OPEN, priority project, under review on PR #76.
- **#70 (Lab Health)** - Auditor owns the daily summary on its schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.
- Billing/infra issues (#72/#73/#74/#75) closed; the build-verify baseline
  false positive (#72 BUILD-job gap) recurred at 19:12Z - queued for a factory
  round once PR #76 lands and no opencode workflow is in flight.

## Reviewer/Tester/model status

- **Model config (owner's pin):** opencode.json `model:
  opencode/deepseek-v4-flash-free`, `small_model: opencode/mimo-v2.5-free`.
  Reviewer/test/factory jobs on mimo-v2.5-free; all agent steps 60m. No
  CreditsError expected.
- **Reviewer dispatch:** opencode-review.yml triggers only on `/oc review`
  comments; the Maintainer dispatches review via decision.json, or the owner
  drives it directly (as today).

## Next steps

1. **Watch the reviewer on PR #76** (run 32065716177). On `/oc approve` ->
   test -> `/oc approve-test` -> merge + close #68. On `/oc fix` -> Fixer ->
   re-review.
2. After PR #76 lands: **route `factory`** for the build-verify baseline false
   positive (capture baseline on the branch, not main) - safe once no opencode
   workflow is in flight.
3. **#70**: Auditor owns the daily health summary; watch for anomalies.
4. No board picks until Obsidian resolves (owner's freeze).
5. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Reviewer: approve or fix? If fix, what does it flag (the benchmark harness
  is checklist 10, deliberately scoped next)?
- Does the Tester's dynamic round-trip + benchmark verification pass?
- Will the owner merge Obsidian today (new-project cap 0/2 so far)?