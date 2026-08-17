# STATE - Random factory checkpoint

- **Updated:** 2026-08-17 (~22:02Z event run 32074063815, owner `/oc maintainer`
  on PR #76 at 22:01:36Z, right after `/oc review` at 22:01:26Z). PR #76's
  Obsidian codec core is COMPLETE, branch-aligned (MERGEABLE/CLEAN), and the
  Reviewer's round-4 finding (index.html test count "43" -> "46") is now APPLIED
  by the Fixer (head `0f804ed`, 22:01:20Z). Review round 5 is in flight on that
  head; this run posts a status note and no triggers.

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec (Kodak-benchmarked,
  vs JPEG XL / WebP).** OPEN, still the priority project. PR #76 carries the
  research + spec + architecture + the COMPLETE codec core (checklist 1-9):
  46 lib tests green, bit-exact round trips at efforts 0-7 over fuzz images
  (Tester verified 4000 round-trips at --fuzz 1000), corrupt/truncated streams
  rejected (dimension caps MAX_DIM 2^20 / MAX_AREA 2^25), adaptive rANS lockstep
  fixed (forward dry-run + `put_fc`), causal predictor borders + width-1 TR
  clamp, YCoCg-R + palette, 8-predictor bank, gradient+activity contexts,
  measured model-size guard, `target/` untracked + `.gitignore`. Landing page
  Obsidian card updated ("46 lib tests"). Progress file
  `68-obsidian-lossless-image-codec.md` marks 1-9 complete; next step =
  checklist 10 (benchmark harness + first Kodak row).

## In flight

- **PR #76 (Obsidian) - REVIEW ROUND 5 IN FLIGHT.** Head `0f804ed` ("fixer:
  obsidian: update landing-page test count to 46", pushed 22:01:20Z) on
  `opencode/issue68-20260817120528`, 30 files, `mergeable: MERGEABLE`,
  `mergeStateStatus: CLEAN`. Timeline: Reviewer round 1 `/oc fix` -> Fixer
  `91d8175` -> Reviewer round 2 `/oc approve` -> Tester round 1 `/oc fix` (OOM
  header) -> Fixer `83dd66b` -> Reviewer round 3 `/oc approve` -> Tester round 2
  `/oc fix` (fuzz >= 103) -> Fixer `11265bd` -> Reviewer round 4 `/oc fix`
  (index.html "43" -> "46") -> **Fixer `0f804ed` (22:01:20Z)** -> owner `/oc
  review` 22:01:26Z -> **opencode-review run 32074049350 in_progress** on the
  fixed head. This run: `ping` status note only. On `/oc approve`: Tester
  auto-dispatches -> on `/oc approve-test`: MERGE + close #68.

## Issues

- **#68 (Obsidian)** - OPEN, priority project, fifth review round on PR #76.
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
- **Fixer dispatch gotcha (logged for the CTO):** opencode.yml's fix job only
  fires on an EXACT `/oc fix` comment body. The Reviewer/Tester's findings
  comments (`/oc fix\n\n**Checklist findings:**...`) do NOT match, so the Fixer
  only runs when the owner or the Maintainer posts an exact `/oc fix`. Proposed
  post-merge factory item: relax the guard to `startsWith('/oc fix')`.

## Next steps

1. **Review round 5 on PR #76** (in flight): shepherd approve -> test ->
   `/oc approve-test` -> merge (`gh pr merge 76 --rebase --delete-branch`) +
   close #68 + verify pages.yml ran.
2. **Kodak directive (owner, 20:42:32Z)**: after PR #76 lands, route the build
   for checklist 10 (benchmark harness + first Obsidian Kodak row) and the M1-M3
   iteration to beat WebP/PNG and close in on JPEG XL; Tester's rounds must cover
   losslessness AND Kodak performance.
3. After PR #76 lands: **route `factory`** for the build-verify baseline false
   positive (capture baseline on the branch, not main) - safe once no opencode
   workflow is in flight. Also propose the fix-trigger guard relaxation.
4. **#70**: Auditor owns the daily health summary; watch for anomalies.
5. No board picks until Obsidian resolves (owner's freeze).
6. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the Reviewer approve round 5 on head `0f804ed`, ending the fix loop?
- Will the owner merge Obsidian today (new-project cap 0/2 so far)?
- Does the Tester's next round cover both losslessness AND Kodak performance per
  the owner's directive, once the benchmark harness exists?