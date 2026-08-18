# STATE - Random factory checkpoint

- **Updated:** 2026-08-17 (~23:58Z event run 32082522931, PR #78). Reviewer
  round 2 APPROVED the fixed head `06a1494` (all 3 round-1 findings applied by
  the Fixer); the owner posted `/oc test` -> Tester run 32082601663 IN_PROGRESS.

## Priority project (the fundamental goal)

- **Issue #77 Obsidian checklist 10 (benchmark harness + reference baseline +
  first Kodak row).** OPEN, PR #78 references `Closes #77`. PR #78 head
  `06a1494` on `opencode/issue68-20260817231515` (MERGEABLE/CLEAN) carries the
  full harness: `obsidian/benchmarks/run_kodak.sh`, `fuzz_gate.sh`,
  `aggregate.py`, `build_toolchain.sh` + `toolchain.md`, pinned Kodak manifest
  (`data/kodak.sha256`, PCD0992 24x 768x512 P6 PPM), result CSV
  (2026-08-17-v1.csv, 7 codecs x 24 images, 168 fidelity-gated rows),
  reference-baseline CSV, README, docs/progress/ideas updates.
- **First Obsidian Kodak row: 27.8226 mean bpp (effort 4)**, bit-exact through
  the gate but not competitive. Reference figures land within ~0.5% of the
  independent WangXuan95 2024 benchmark on the same corpus (harness is honest).
  M1-M3 (beat WebP/PNG -> approach/match JPEG XL) are the next milestones.
- The owner's standing directive (20:42:32Z): test BOTH losslessness and
  performance on the Kodak dataset, keep iterating until Obsidian beats the
  other codecs. Codec core (checklist 1-9) shipped on main via PR #76 (46 lib
  tests green).

## In flight

- **Test on PR #78** (run 32082601663, owner's `/oc test` 23:57:29Z) -
  IN_PROGRESS on head `06a1494`. On `/oc approve-test`: merge, close #77,
  verify pages.yml, then route `factory`.
- **Review loop closed**: round 1 `/oc fix` (3 findings) -> Fixer applied all 3
  -> round 2 `/oc approve` (23:57:28Z). No outstanding findings.
- **pages.yml**: preview runs completed success for the PR head pushes.

## Issues

- **#77 (Obsidian checklist 10)** - OPEN; PR #78 closes it on merge.
- **#70 (Lab Health)** - Auditor owns the daily summary on its schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.
- **Factory round QUEUED (do NOT run concurrent with a build/review/test):**
  the build-verify baseline false positive (#72 BUILD-job gap) plus the
  fix-trigger guard relaxation (opencode.yml fix job requires an EXACT
  `/oc fix`; the Reviewer/Tester's findings comments don't match). Dispatch
  `factory` once PR #78 lands and no opencode build/review/test is in flight.

## Reviewer/Tester/model status

- **Model config (owner's pin):** opencode.json `model:
  opencode/deepseek-v4-flash-free`, `small_model: opencode/mimo-v2.5-free`.
  Reviewer/test/factory jobs on mimo-v2.5-free; all agent steps 60m. No
  CreditsError expected.
- **Reviewer/Tester gates** passed on PR #76 (round 5 approve -> approve-test
  -> merged) and are mid-flight on PR #78.

## Next steps

1. **Watch the Tester on PR #78** (run 32082601663, head `06a1494`). On `/oc
   approve-test`: merge (`gh pr merge 78 --rebase --delete-branch`), close #77,
   verify pages.yml, then route `factory` for the verify-baseline bug +
   fix-trigger guard (safe then - no build/review/test in flight).
2. **On `/oc fix` from the Tester**: the Fixer applies findings; re-dispatch
   `review` after the fix push (opencode-review fires on `/oc review`).
3. **Kodak iteration (M1-M3)**: once the first Obsidian Kodak row is recorded,
   drive predictor/context improvements to beat WebP/PNG (M1), then close in on
   JPEG XL (M2/M3). Owner's directive: keep iterating until Obsidian wins.
4. **Route `factory`** for the build-verify baseline false positive +
   fix-trigger guard relaxation - only when no opencode build/review/test is in
   flight.
5. **#70**: Auditor owns the daily health summary; watch for anomalies.
6. **#42**: no board picks until Obsidian resolves (owner's freeze).
7. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the Tester's round cover losslessness AND Kodak performance (owner's
  directive) and pass on head `06a1494`?
- How close is Obsidian's first Kodak row to WebP/PNG and JPEG XL (M1-M3 gap)?
- Factory round timing: dispatch as soon as PR #78 lands and no opencode
  workflow is in flight.