# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~03:07Z, maintainer event run 32327031693, triggered by owner `/oc maintainer` on PR #93 after the Builder's escalation). Decision: dispatch Architect R12 blueprint (adaptive per-band weighted predictor + MA-tree entropy context). One-PR rule intact; orphan re-link remains fixed.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`. (#91 + #92 branches `opencode/lab-68-orphan-main-guard` intentionally left intact.)
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. Still deferred; schedule once JXL nears.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** PR #93 is the single canonical, open Obsidian PR (supersedes closed #83), branch `opencode/issue68-20260818070512`.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec).
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #93 (or issue #68 for factory/lab) - not on a new PR.

## CRITICAL INFRASTRUCTURE STATE (orphan-main guard MERGED; branch RE-LINKED & PR #93 OPEN)

- **PR #91 MERGED:** orphan-main guard (`c043b7e`, carries literal `Closes #68` commit token; #68 reopened same run).
- **PR #92 MERGED:** `main` = `d6b2894`. Determinism guard + "do not auto-close umbrella" rule + force-with-lease pin. Body `Refs #68`.
- **`main` = `d6b2894`** (healthy, 370 commits, clean descendant of prior main).
- **Branch `opencode/issue68-20260818070512` RE-LINKED** (current head `70c943d6`), shares history with `main` (merge-base `d6b2894`). PR #93 is the single canonical Obsidian PR (`Refs #68`). ORPHAN PROBLEM RESOLVED.
- Root cause of the prior stall (Lab Engineer refused the re-link; Mae hard-barred from pushing) resolved by the Builder's `/oc continue` rebuild + reopen as PR #93.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub auto-closes #68 if the literal `Closes #68` token appears ANYWHERE. Future Builder/Architect/Lab commits MUST use `Refs #68` / `Refs to #68`. PR #93 body is correctly `Refs #68`.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian):** OPEN, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **Default shipped codec = 9.5208 bpp mean** (R10-B CFL). Beats PNG (13.05) + WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
- **R0-R11 codec shipped on PR #93:** Golomb-Rice, CMARC binary range coder (R4), context-tree weighted predictor (R9-B), R10 Squeeze + chroma-from-luma, R11 cross-band in-loop predictor, R11-D MA-tree-lite combined gradient+residual context (opt-in `OBSIDIAN_CARC_MA_CTX=1`), R11-A cross-band `wLL` (reverted - wash + 45x slowdown).
- **PREDICTOR-CONTEXT CEILING CONFIRMED (3 independent axes):**
  1. R11-D combined gradient+residual MA context - wash (mean unchanged 9.5208).
  2. R11-A cross-band `wLL` - wash + 45x slowdown (reverted).
  3. This run (2026-08-20, Builder): finer 64-leaf `WeightedTree` weight-context partition - 9.5262 bpp REGRESSION vs 9.5208 (reverted).
  - Conclusion (robust): the +0.81 bpp gap to JXL 8.71 is the **predictor's functional form**, not its context granularity.

## In flight

- **`architect` on PR #93 (DISPATCHED THIS run, 32327031693):** the Architect drafts the **R12 blueprint** - adaptive per-band weighted predictor (fit per Squeeze band in subsampled LL domain) + true MA-tree entropy context (semantics change per band). Design basis: existing R7 weighted / R8 adaptive-weighted / R9 spatial-weighted blueprints on-branch. Builder resumes via `continue` once the blueprint lands.
- After R12 blueprint: Builder implements + re-measures REAL Kodak effort-4. Loop via `continue` until all three gates clear.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above (default 9.5208); next lever = R12 Architect blueprint (in flight).
- **Resume Builder (predictor) via `continue`** - after R12 blueprint lands.
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once JXL nears).
- **Review staleness on #93:** head `70c943d6` is builder self-pushed; fresh Reviewer + Tester gate required before any merge.
- **Commit-message hygiene:** never write literal `Closes #68` token in ANY commit message or PR body.

## Issues

- **#68 (Obsidian umbrella)** - OPEN, active fundamental goal, stays open until codecs beaten.
- **#52 / #89 / #90 / #91 / #92 infra** - #90 MERGED; #89 CLOSED; #52 related; #91 MERGED (guard); #92 MERGED (guard + umbrella rule + force-with-lease pin). Both branches kept.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule; board live.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError` in recent runs.
- **pages.yml:** green (run 32327041481 completed/success after PR #93 updates). PR preview staged.
- **PR #93 checks:** opencode-pr-trigger SUCCESS, pages deploy SKIPPED (expected for PR preview), GitGuardian SUCCESS. No Reviewer/Tester run yet.

## Next steps

1. **Architect R12 blueprint (in flight):** design adaptive per-band weighted predictor + true MA-tree entropy context (JPEG XL-class). Reference R7/R8/R9 blueprints on-branch.
2. **Builder `continue` after blueprint:** implement R12, re-measure REAL Kodak effort-4 against the JXL 8.71 gate. Loop until all three gates clear.
3. **After gates clear:** fresh Reviewer + Tester gate, then rebase-merge (`--no-delete-branch`) and close #68. NOT before.
4. **README / index.html promotion:** schedule once JXL nears / PR clears.

## Open questions

- **Will the R12 Architect blueprint clear the +0.81 JPEG XL gap on REAL Kodak?** Verdict pending the Architect's design + the Builder's implementation + real-Kodak re-measure. Three axes now prove context refinement is exhausted; the predictor's functional form is the lever.
- **Merge gate (owner override #2):** NOT met - default 9.5208 beats PNG + WebP but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, shares history with main).
- **Orphan-main break:** RESOLVED (merge-base `d6b2894` non-empty; PR #93 healthy).
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **pages.yml:** green.
- **Billing:** resolved (no `CreditsError`; `small_model` correctly pinned free).
- **Commit-message hygiene:** PR #93 body is correctly `Refs #68`; future commits/blueprints must avoid literal `Closes #68`.

- Mae, the Maintainer
