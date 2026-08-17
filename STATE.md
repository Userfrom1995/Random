# STATE - Random factory checkpoint

- **Updated:** 2026-08-17 (~20:32Z event run 32066290564, owner `/oc maintainer`
  on PR #76, right after `/oc review` at 20:31:47Z). PR #76's Obsidian codec
  core is COMPLETE, branch-aligned (MERGEABLE), and both Reviewer findings have
  been applied by the Fixer (head `91d8175`). The Reviewer is IN FLIGHT on that
  fixed head (run 32066277954). This run is a status-only pass - ping only, no
  triggers, no duplicates.

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

- **PR #76 (Obsidian) - SECOND REVIEW ROUND IN PROGRESS.** Head `91d8175`
  ("fixer: obsidian: PR body closes #68, add Obsidian to landing page", pushed
  20:31:45Z) on `opencode/issue68-20260817120528`, 30 files,
  `mergeable: MERGEABLE`. The Reviewer's first round (run 32065716177) returned
  `/oc fix` with two findings: (1) PR body lacked the `Closes #68` keyword,
  (2) root `index.html` not updated with an Obsidian card. The Fixer applied
  both in one commit (`91d8175`) via `/oc fix` (run 32066135837) and edited the
  PR body to carry `Closes #68.`. Owner's `/oc review` at 20:31:47Z ->
  reviewer run **32066277954 in_progress** on the fixed head. The duplicate
  opencode-review run 32066290559 (spawned by this `/oc maintainer` comment)
  is pending with zero jobs - its guard requires the comment to start with
  `/oc review`, so it self-skips. On `/oc approve`: Tester auto-dispatches ->
  on `/oc approve-test`: MERGE + close #68. On `/oc fix`: Fixer again.

## Issues

- **#68 (Obsidian)** - OPEN, priority project, second review round on PR #76.
- **#70 (Lab Health)** - Auditor owns the daily summary on its schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.
- Billing/infra issues (#72/#73/#74/#75) closed; the build-verify baseline
  false positive (#72 BUILD-job gap, recurred 19:12Z) is still queued for a
  factory round once PR #76 lands and no opencode workflow is in flight (a
  review is in flight right now - factory must wait).

## Reviewer/Tester/model status

- **Model config (owner's pin):** opencode.json `model:
  opencode/deepseek-v4-flash-free`, `small_model: opencode/mimo-v2.5-free`.
  Reviewer/test/factory jobs on mimo-v2.5-free; all agent steps 60m. No
  CreditsError expected.
- **Reviewer dispatch:** opencode-review.yml triggers only on `/oc review`
  comments; the Maintainer dispatches review via decision.json, or the owner
  drives it directly (as today).

## Next steps

1. **Watch the reviewer on PR #76** (run 32066277954, reviewing `91d8175`).
   On `/oc approve` -> test -> `/oc approve-test` -> merge + close #68. On
   `/oc fix` -> Fixer -> re-review.
2. After PR #76 lands: **route `factory`** for the build-verify baseline false
   positive (capture baseline on the branch, not main) - safe once no opencode
   workflow is in flight.
3. **#70**: Auditor owns the daily health summary; watch for anomalies.
4. No board picks until Obsidian resolves (owner's freeze).
5. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Reviewer round 2: approve or another fix round?
- Does the Tester's dynamic round-trip + benchmark verification pass?
- Will the owner merge Obsidian today (new-project cap 0/2 so far)?