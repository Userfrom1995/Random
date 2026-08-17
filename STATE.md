# STATE - Random factory checkpoint

- **Updated:** 2026-08-17 (~21:53Z event run 32073403297, owner `/oc maintainer`
  on PR #76 at 21:53:37Z, right after the Tester's all-pass round). PR #76's
  Obsidian codec core is COMPLETE, branch-aligned (MERGEABLE/CLEAN), and the
  Tester passed round 3 (46/46 tests, fuzz 1000, corruption rejection). The
  Reviewer's round-4 finding (index.html test count "43" -> "46") is UNAPPLIED -
  the owner's `/oc test` ran the Tester instead of an exact `/oc fix`, so the
  Fixer never ran. This run dispatches the Fixer.

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec (Kodak-benchmarked,
  vs JPEG XL / WebP).** OPEN, still the priority project. PR #76 carries the
  research + spec + architecture + the COMPLETE codec core (checklist 1-9):
  46 lib tests green, bit-exact round trips at efforts 0-7 over fuzz images
  (Tester verified 4000 round-trips at --fuzz 1000), corrupt/truncated streams
  rejected, adaptive rANS lockstep fixed (forward dry-run + `put_fc`), causal
  predictor borders + width-1 TR clamp, YCoCg-R + palette, 8-predictor bank,
  gradient+activity contexts, measured model-size guard, `target/` untracked +
  `.gitignore`. Progress file `68-obsidian-lossless-image-codec.md` marks 1-9
  complete; next step = checklist 10 (benchmark harness + first Kodak row).

## In flight

- **PR #76 (Obsidian) - REVIEW ROUND 5 PENDING A FIX.** Head `11265bd`
  ("fixer: predict: clamp TR column to width-1 for border rows", pushed
  21:46:34Z) on `opencode/issue68-20260817120528`, 30 files,
  `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. Timeline: Reviewer round 1
  `/oc fix` -> Fixer `91d8175` -> Reviewer round 2 `/oc approve` -> Tester round
  1 `/oc fix` (OOM header) -> Fixer `83dd66b` -> Reviewer round 3 `/oc approve`
  -> Tester round 2 `/oc fix` (fuzz >= 103) -> Fixer `11265bd` -> Reviewer round
  4 (run 32072837302) posted `/oc fix` at 21:50:11Z with ONE finding:
  `index.html:140` says "43 lib tests", should be "46 lib tests" -> owner posted
  `/oc test` (NOT `/oc fix`) -> Tester round 3 (run 32073134438) PASSED all
  tests at 21:53:36Z but docs untouched -> finding UNAPPLIED. **THIS run: `fix`
  dispatched**; the fix workflow then auto-posts `/oc review`. On `/oc approve`:
  Tester auto-dispatches -> on `/oc approve-test`: MERGE + close #68.

## Issues

- **#68 (Obsidian)** - OPEN, priority project, fifth review round on PR #76.
- **#70 (Lab Health)** - Auditor owns the daily summary on its schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.
- Billing/infra issues (#72/#73/#74/#75) closed; the build-verify baseline
  false positive (#72 BUILD-job gap, recurred 19:12Z) is still queued for a
  factory round once PR #76 lands and no opencode workflow is in flight (a fix
  run is being dispatched right now - factory must wait).

## Reviewer/Tester/model status

- **Model config (owner's pin):** opencode.json `model:
  opencode/deepseek-v4-flash-free`, `small_model: opencode/mimo-v2.5-free`.
  Reviewer/test/factory jobs on mimo-v2.5-free; all agent steps 60m. No
  CreditsError expected.
- **Reviewer dispatch:** opencode-review.yml triggers only on `/oc review`
  comments; the Maintainer dispatches review via decision.json, or the owner
  drives it directly (as today).
- **Fixer dispatch gotcha (logged for the CTO):** opencode.yml's fix job only
  fires on an EXACT `/oc fix` comment body (line 503). The Reviewer/Tester's
  findings comments are `/oc fix\n\n**Checklist findings:**...` and do NOT
  match, so the Fixer only runs when the owner or the Maintainer posts an exact
  `/oc fix`. This round the owner's `/oc test` did not dispatch the Fixer.

## Next steps

1. **Fixer on PR #76** (dispatched this run): apply the index.html test-count
   fix, push -> auto `/oc review`. Then shepherd approve -> test ->
   `/oc approve-test` -> merge + close #68.
2. **Kodak directive (owner, 20:42:32Z)**: after PR #76 lands, route the build
   for checklist 10 (benchmark harness + first Obsidian Kodak row) and the M1-M3
   iteration to beat WebP/PNG and close in on JPEG XL; Tester's rounds must cover
   losslessness AND Kodak performance.
3. After PR #76 lands: **route `factory`** for the build-verify baseline false
   positive (capture baseline on the branch, not main) - safe once no opencode
   workflow is in flight. Also propose the fix-trigger guard relaxation
   (`startsWith('/oc fix')`) to auto-dispatch the Fixer from reviewer findings.
4. **#70**: Auditor owns the daily health summary; watch for anomalies.
5. No board picks until Obsidian resolves (owner's freeze).
6. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the Fixer land the index.html count update and push cleanly, and does
  review round 5 approve?
- Will the owner merge Obsidian today (new-project cap 0/2 so far)?
- Does the Tester's next round cover both losslessness AND Kodak performance per
  the owner's directive, once the benchmark harness exists?