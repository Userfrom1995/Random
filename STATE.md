# STATE - Random factory checkpoint

- **Updated:** 2026-08-17 (~21:02Z event run 32069006691, owner `/oc maintainer`
  on PR #76, right after `/oc review` at 21:02:15Z). PR #76's Obsidian codec
  core is COMPLETE, branch-aligned (MERGEABLE/CLEAN), and the Tester's OOM
  finding has been applied by the Fixer (head `83dd66b`). The Reviewer is IN
  FLIGHT on that fixed head (run 32068992405). This run is a status-only pass -
  ping only, no triggers, no duplicates. The owner's Kodak directive (lossless
  + performance on Kodak, iterate until Obsidian beats the other codecs) is
  acknowledged and logged.

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec (Kodak-benchmarked,
  vs JPEG XL / WebP).** OPEN, still the priority project. PR #76 carries the
  research + spec + architecture + the COMPLETE codec core (checklist 1-9):
  45 lib tests green (after the Fixer's decoder fix), bit-exact round trips at
  efforts 0-7 over fuzz images, corrupt/truncated streams rejected, adaptive
  rANS lockstep fixed (forward dry-run + `put_fc`), causal predictor borders,
  effort-0 single global context per plane, measured model-size guard, `target/`
  artifacts untracked + `.gitignore`. Progress file `68-obsidian-lossless-image-codec.md`
  marks 1-9 complete; next step = checklist 10 (benchmark harness + first
  Kodak row).

## In flight

- **PR #76 (Obsidian) - REVIEW ROUND 3 IN PROGRESS.** Head `83dd66b`
  ("fixer: decoder: guard inflated dimensions and fix palette alphabet sizes",
  pushed 21:02:14Z) on `opencode/issue68-20260817120528`, 30 files,
  `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. Timeline: Reviewer round 1
  (run 32065716177) -> `/oc fix` (Closes #68 keyword + index.html card) ->
  Fixer `91d8175` -> Reviewer round 2 `/oc approve` (run 32066277954) -> Tester
  round 1 (run 32066640199) -> `/oc fix` (OOM on corrupted header width) ->
  Fixer `83dd66b` (dimension caps 2^20/2^25 + palette alphabet-sizes latent
  bug; rebutted the ratio bound with measured evidence) -> owner's `/oc review`
  at 21:02:15Z -> reviewer run **32068992405 in_progress** on the fixed head.
  The duplicate opencode-review run 32069005608 (spawned by this `/oc
  maintainer` comment) is pending with zero jobs - its guard requires the
  comment to start with `/oc review`, so it self-skips. On `/oc approve`:
  Tester auto-dispatches -> on `/oc approve-test`: MERGE + close #68. On
  `/oc fix`: Fixer again.

## Issues

- **#68 (Obsidian)** - OPEN, priority project, third review round on PR #76.
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

1. **Watch the reviewer on PR #76** (run 32068992405, reviewing `83dd66b`).
   On `/oc approve` -> test -> `/oc approve-test` -> merge + close #68. On
   `/oc fix` -> Fixer -> re-review.
2. **Kodak directive (owner, 20:42:32Z)**: ensure the Tester's next round
   covers BOTH losslessness and performance on Kodak; then after PR #76 lands,
   route the build for checklist 10 (benchmark harness + first Obsidian Kodak
   row) and the M1-M3 iteration to beat WebP/PNG and close in on JPEG XL.
3. After PR #76 lands: **route `factory`** for the build-verify baseline false
   positive (capture baseline on the branch, not main) - safe once no opencode
   workflow is in flight.
4. **#70**: Auditor owns the daily health summary; watch for anomalies.
5. No board picks until Obsidian resolves (owner's freeze).
6. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Reviewer round 3: approve or another fix round?
- Does the Tester's next round pass on head `83dd66b`, covering losslessness
  AND Kodak performance per the owner's directive?
- Will the owner merge Obsidian today (new-project cap 0/2 so far)?