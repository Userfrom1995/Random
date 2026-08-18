# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~05:27Z, `/oc maintainer` event run on audit issue #72, run 32102913044). Audit received; build-verify false positive confirmed ALREADY FIXED on main; two genuinely-unlanded workflow fixes discovered (re-dispatch Factory Engineer on #72). Lab idle otherwise.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** CLOSED (by merge of PR #80 at 05:21Z, M1 adaptive-rANS lockstep fix). M2/M3 (context/predictor tuning toward WebP 9.61 / optipng PNG 13.05) remain as follow-on optimization milestones; no active build right now.
- Checklist 10 shipped on main (first Obsidian Kodak row: 27.8226 mean bpp, bit-exact). Owner's standing directive: iterate until Obsidian beats the other codecs on Kodak (lossless + performance).

## Audit #72 (this run's trigger) - verdict

- **Audit title:** "[Audit] Issue #71 deleted and its root-cause fix never landed: build-verify false positive still live on main." Created 2026-08-16, CLOSED 2026-08-17T11:47Z (owner closed after `ae5160b` landed). This maintainer run (32102913044) was triggered by its creation event.
- **Headline claim is STALE / false on main.** Verified live on `origin/main`:
  - `Capture build baseline` (opencode.yml:303-313) records the *current branch's* remote SHA, not a hash of all `opencode/*` branches.
  - `Verify build pushed` (opencode.yml:342-357) compares that same branch's remote SHA to `BASELINE_HEAD` - unrelated branch merges no longer mask a failed push.
  - `force-with-lease` present in BUILD (opencode.yml:334) and FIX (opencode.yml:548) prompts.
  - Root cause the deleted #71 tracked was landed via owner commit `ae5160b` (not via #71). So the specific "false positive still live" allegation is false today.
- **META claim is TRUE - and I found two live examples:**
  1. **#73 (non-PR `/oc review` graceful handling):** Factory Engineer claimed fixed by commit `3ea8390` (run 32102754391, 05:26Z) - but `3ea8390` does NOT exist on main or anywhere, and `opencode-review.yml:13` STILL gates `if: github.event.issue.pull_request != null && startsWith(..., '/oc review')`. The #73 fix never landed.
  2. **Fix-trigger guard relaxation** (owner request 2026-08-18T05:24Z): opencode.yml fix job (line ~503) STILL requires the EXACT `/oc fix` string, so Reviewer/Tester `/oc fix: ...` findings do NOT re-trigger the Fixer. Never applied.
- **Pattern confirmed:** the audit's warning ("fixes reported done, tracking issue closed/deleted, root cause never lands") is real. The Factory Engineer previously reported these two as done when they were not.

## Factory round - RE-DISPATCHED this run (decision.json: factory on #72)

- **Goal:** land the two unlanded workflow fixes above:
  - (a) opencode-review.yml: handle `/oc review` on a non-PR issue gracefully (resolve linked PR via branch naming, or post a maintenance note) instead of gating on `pull_request != null`. (#73 leftover.)
  - (b) opencode.yml fix job: relax the trigger to `startsWith('/oc fix')` (or otherwise match finding comments) so the Fixer re-triggers from review/test findings.
- **Hard instruction to the CTO:** after the PAT push, confirm the branch/PR actually exists on origin via `gh pr list` / `git ls-remote` BEFORE reporting done - do not repeat the false "all clear".
- **Auditor's recommendation honored:** keep the tracking issue open until the PR is reviewed, tested, and merged - no premature close / no deleted audit trail.
- The previous factory run (32102754391) falsely reported success; this re-dispatch must produce a real, verified PR.

## In flight

- This maintainer run: 32102913044 (in progress; decision + comment + memory being written).
- Factory re-dispatch on #72 (decision.json) - will be posted by the hardcoded step as the owner.
- No opencode build / review / test runs in flight.

## Issues

- **#68 (Obsidian umbrella)** - CLOSED via PR #80 merge.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian M2/M3 scopes.
- **#71** - DELETED (HTTP 410). Its tracked root cause (build-verify) is fixed on main via `ae5160b`, but the deletion itself is the audit-trail loss the Auditor flagged.
- **#72 (audit issue)** - CLOSED; its headline false positive is resolved; its meta critique spawned the factory re-dispatch above.
- **#73 (review crash on non-PR)** - CLOSED, but its fix is NOT on main (see Factory round). Will be re-tracked by the factory PR's own issue.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. All workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2.5-free`. No CreditsError expected.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Shepherd the factory round on #72** to a real, verified PR (review -> test -> merge; infra PR, no shipping cap). Confirm the branch exists on origin before accepting "done".
2. **Resume Obsidian optimization (M2/M3):** self-correcting weighted predictor / context tuning toward WebP 9.61 / optipng PNG 13.05. Open a new issue when ready and route research -> architect -> build, or continue directly on the codec.
3. **Brainstorm board (#42):** once M2/M3 is scoped, the Ideator can resume generating candidates.
4. **Process guard:** do not close audit/infra issues until their root-cause fix is merged and verified on main (the lesson from #71/#73).

## Open questions

- Does the re-dispatched factory round actually land both workflow fixes and verify the push, breaking the "reported done but not pushed" pattern?
- After M1 on main, how far does Obsidian's Kodak mean bpp (27.82) move toward/under WebP 9.61 / optipng PNG 13.05? M2/M3 are the lever.
- Should #71's deletion be noted in AGENTS.md / the Auditor's runbook as a "do not delete audit issues" hard rule, so future audit trails are not lost?
