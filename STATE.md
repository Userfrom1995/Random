# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~02:55Z, maintainer event run 32326377434, triggered by PR #93 creation + owner `/oc maintainer` + `/oc continue`). Orphan re-link CONFIRMED FIXED: PR #93 branch shares history with `main` (merge-base `d6b2894`, head `4a3604b`). One-PR rule RESTORED.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`. (#91 + #92 branches `opencode/lab-68-orphan-main-guard` intentionally left intact.)
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. Still deferred; schedule once JXL nears.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** RESTORED THIS CYCLE: PR #93 is the single canonical, open Obsidian PR (supersedes closed #83). It iterates on branch `opencode/issue68-20260818070512` via resume (`/oc continue`).
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec).
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #93 (or issue #68 for factory/lab) - not on a new PR.

## CRITICAL INFRASTRUCTURE STATE (orphan-main guard MERGED; branch RE-LINKED & PR #93 OPEN)

- **PR #91 MERGED:** `c043b7e` orphan-main guard (commit msg carries literal `Closes #68` token, which auto-closed #68; reopened same run).
- **PR #92 MERGED:** `main` = `d6b2894`. Adds determinism guard + "do not auto-close umbrella" rule + force-with-lease pin. Body `Refs #68`, no new auto-close token.
- **`main` = `d6b2894`** (after PR #92). HEALTHY, 370 commits, clean descendant of prior main.
- **Branch `opencode/issue68-20260818070512` RE-LINKED THIS CYCLE** (head `4a3604b`): rebuilt onto `origin/main` (shared ancestor `d6b2894`), PR #93 created as the single canonical Obsidian PR (`Refs #68`). ORPHAN PROBLEM RESOLVED.
- **Root cause of the prior stall (resolved):** the Lab Engineer repeatedly shipped guards but refused the actual branch re-link; Mae is hard-barred from pushing. The Builder's `/oc continue` (build-job contract, opencode.yml:340) was the correct executor and DID re-link + reopen as PR #93.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub auto-closes #68 if the literal `Closes #68` token appears ANYWHERE (body OR commit message). Confirmed 02:00Z (commit `c043b7e`). Lesson locked: future Builder/Lab commits must use `Refs #68` / `Refs to #68`, never `Closes #68`. PR #93 body is correctly `Refs #68`.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian):** OPEN, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **Default shipped codec = 9.5208 bpp mean** (R10-B CFL). Beats PNG (13.05) + WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
- **R0-R11 codec shipped on PR #93:** Golomb-Rice, CMARC binary range coder (R4), context-tree weighted predictor (R9-B), R10 Squeeze + chroma-from-luma, R11 cross-band in-loop predictor, R11-D MA-tree-lite combined gradient+residual context (opt-in `OBSIDIAN_CARC_MA_CTX=1`).
- **R11-D VERDICT (this session):** INEFFECTIVE on real Kodak - mean unchanged 9.5208. The never-expand net disabled MA on every image (combined fold never beat residual-DIFF context). **Conclusion: predictor is the bottleneck, not entropy/context.**

## In flight

- **`continue` on PR #93 (DISPATCHED THIS run, 32326377434):** Builder resumes toward the JXL 8.71 gate by implementing a genuinely better adaptive/weighted predictor (design basis: R7 weighted / R8 adaptive-weighted / R9 spatial-weighted blueprints). Re-measure REAL Kodak effort-4. Loop via `continue` until all three gates clear.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above (default 9.5208); next attempt = better predictor via `continue`.
- **Resume Builder (predictor) via `continue`** - in flight this run.
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once JXL nears).
- **Review staleness on #93:** head `4a3604b` is builder self-pushed; fresh Reviewer + Tester gate required before any merge.
- **Commit-message hygiene:** never write literal `Closes #68` token in ANY commit message or PR body.

## Issues

- **#68 (Obsidian umbrella)** - OPEN, active fundamental goal, stays open until codecs beaten.
- **#52 / #89 / #90 / #91 / #92 infra** - #90 MERGED; #89 CLOSED; #52 related; #91 MERGED (guard); #92 MERGED (guard + umbrella rule + force-with-lease pin). Both branches kept.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule; board live.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError` in recent runs.
- **pages.yml:** triggered on PR #93 open (run 32326352209); verify green.
- **PR #93 checks:** opencode-pr-trigger SUCCESS, pages deploy SKIPPED (expected for PR preview), GitGuardian SUCCESS. No Reviewer/Tester run yet.

## Next steps

1. **Builder `continue` (in flight):** implement genuinely better adaptive/weighted predictor (R7/R8/R9 blueprints), re-measure REAL Kodak effort-4 against the JXL 8.71 gate. Loop via `continue` until all three gates clear.
2. **After predictor measured:** if default < 8.71 JXL (alongside PNG 13.05 + WebP 9.61), fresh Reviewer + Tester gate, then rebase-merge (`--no-delete-branch`) and close #68. NOT before.
3. **README / index.html promotion:** schedule once JXL nears / PR clears.

## Open questions

- **Will the better predictor clear the +0.81 JPEG XL gap on REAL Kodak?** Blueprint basis exists (R7/R8/R9). Verdict pending the Builder's next `continue` + real-Kodak re-measure. R11-D confirmed context is NOT the lever.
- **Merge gate (owner override #2):** NOT met - default 9.5208 beats PNG + WebP but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **One-PR integrity:** RESTORED (PR #93 single canonical, OPEN).
- **pages.yml:** verify green after PR #93 open (run 32326352209).
- **Billing:** resolved (no `CreditsError`; `small_model` correctly pinned free).
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.

- Mae, the Maintainer
