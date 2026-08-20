# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (maintainer run 32413476394, owner `/oc maintainer` on PR #97; PR #97 MERGED; PR #93 CLOSED by owner mid-run). **OWNER PIVOT (2026-08-20T14:52:11Z) REMAINS THE STANDING LAW** where not overridden by a later owner action.

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted.** Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on Kodak at 9.5209 bpp) with full docs; then Test + Review + merge. Keep branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying the JPEG XL 8.71 gate, developed on its OWN issue/branch (research -> architect -> build). Never folded into PR #93.
- **ONE Obsidian PR only (being wound down):** PR #93 was the single canonical Obsidian PR; it is now CLOSED by the owner (see below) - a future new codec PR would be the separate JXL project.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68.

## CRITICAL INFRASTRUCTURE STATE

- **PR #97 (circuit breaker for #96): MERGED this run (rebase, branch KEPT).** `main` = `0d0d75fa` (`lab: fail-open circuit breaker + clean trip status + idempotent trip comment (Fixes #96)`). Issue #96 CLOSED. Adds `.github/scripts/loop-budget.sh` + wires `Circuit breaker budget check` (gated before the three Forward steps) into `opencode.yml`. Reviewer `/oc approve` + Tester `/oc approve-test` both posted; merge executed via `gh pr merge 97 --rebase` (API merge of a workflow-touching PR succeeded - the workflows-permission wall blocks only direct `git push`, not API PR merge).
- **`workflows` permission wall (KNOWN, NON-BLOCKING):** confirmed this run - `gh pr merge` via the App installation token merged PR #97 (which edits `opencode.yml`) successfully. The wall only rejects the opencode App's direct `git push` of workflow files, not API PR merges.
- **PR #93 CLOSED by owner (NOT merged) at 20:22:15Z.** The owner force-pushed its branch `opencode/issue68-20260818070512` to `e184c3c` and closed the PR, then requested a review (`/oc review` 20:22:14Z) and a `/oc fix` was posted on it at 20:24:14Z (head `e184c3c`, base `37f0395`). I COMPLY with this owner action and do not re-open or re-drive it. The branch is retained.
- **`main` = `0d0d75fa`** (was `37f0395`).
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`. `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` (both free, non-blocking).

## PRIORITY PROJECT (Obsidian, PR #93) - CLOSED BY OWNER (comply)

- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL + CMARC backend; R13-A muted, R13-B/R14/R15 gated OFF, all byte-identical base so never-regressive). Beats PNG (13.05) + WebP (9.61). JXL 8.71 gate LIFTED by owner pivot.
- **Test-isolation fix landed:** clean parallel suite = **148 passed / 0 failed / 2 ignored**.
- **R15 halt:** 10-axis predictor-family exhaustion proven; all decorrelation/learned overlays gated OFF, byte-identical base.
- **THE BLOCKER (persistent, NOT YET FIXED):** `obsidian/README.md` STALE ("46 lib tests, 27.82 bpp", "M1 gate still open"), `obsidian/STATUS.md` ABSENT. Root cause = `.github/agents/builder.md` resume logic re-reads stale `progress/68-*.md` "Current step" and hollows docs (~10x). The owner force-pushed `e184c3c` and is reviewing the branch directly, so I DEFER the builder.md `lab` fix to avoid colliding with the owner's in-flight review. It remains a standing lab-health defect to re-engage once the owner's direct work settles.

## IN FLIGHT

- **Owner's direct work on PR #93 branch (`e184c3c`):** force-pushed + `/oc review` (20:22:14Z) + `/oc fix` posted (20:24:14Z). Owner is handling it directly; I comply and do not interfere.
- **builder.md root-cause fix (DEFERRED):** re-engaged as a targeted `lab` once the owner's PR #93 branch work concludes, to fix ONLY `.github/agents/builder.md` resume re-task on the newest divergent directive. Not dispatched this run to avoid collision.

## PENDING (awaiting completion, in order)

1. Owner's direct PR #93 branch work (review/fix) to conclude; comply with owner's disposition (merge or keep closed).
2. builder.md `lab` fix (deferred) -> merge its PR/branch (lab-health, prevents future hollow docs).
3. NEW JXL project: separate codebase/new name on its own issue/branch; route research -> architect -> build. Never in PR #93.

## ISSUES

- **#68 (Obsidian umbrella)** - OPEN, stays open until the new JXL-class project beats codecs (per pivot + standing directive).
- **#96 (Circuit breaker)** - CLOSED (PR #97 merged; `Fixes #96` in commit).
- **#94 (Detect silent no-op builds)** - CLOSED (PR #95 merged).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted.

## REVIEWER/TESTER/MODEL STATUS

- **Model config:** worker workflows `opencode/nemotron-3-ultra-free`. `opencode.json` on main still `hy3-free`/`mimo-v2.5-free`. `origin/main` = `0d0d75fa`. Free fallbacks available.
- **pages.yml:** will re-deploy via the hardcoded "main advanced" step (PR #97 merge advanced main).
- **PR #97 checks:** Reviewer `/oc approve`; Tester `/oc approve-test`; merged via `gh pr merge --rebase` (branch kept).
- **PR #93 checks:** owner-requested `/oc review` -> `/oc fix` posted (head `e184c3c`); owner is driving directly.

## NEXT STEPS

1. COMPLY with owner's PR #93 closure; do not re-open/re-drive. Monitor the owner's in-flight review/fix on branch `e184c3c`.
2. After the owner's PR #93 branch work settles, re-engage a targeted `lab` to fix ONLY `.github/agents/builder.md` (resume re-task on newest directive), so future docs builds do not hollow.
3. Stand up NEW JXL project on its own issue/branch; route research -> architect -> build.

## OPEN QUESTIONS

- **PR #93 disposition:** the owner closed it but is also reviewing the branch (`e184c3c`, `/oc fix` 20:24:14Z). Will the owner reopen/merge it, or keep it closed with the codec work preserved on the branch? PENDING owner's next move - comply.
- **builder.md lab (DEFERRED this run):** will it eventually patch ONLY `.github/agents/builder.md` (not opencode.yml, not Obsidian source)? Re-engage after owner's #93 work settles.
- **PR #97 workflows-permission wall on merge:** RESOLVED (API PR merge succeeded with App token).
- **One-PR integrity:** PR #93 was the single canonical Obsidian PR; now CLOSED by owner. Branch retained.
- **Orphan-main break:** RESOLVED (shared merge-base `37f0395`; PR #97 merged as clean rebase descendant).
- **New-project issue:** needs an issue; owner may open or I dispatch `ideate` post-resolution (hard rule: I do not create issues myself).
- **Review/Tester on PR #93:** owner is driving directly; the standing requirement (both before merge) is moot unless the owner reopens/merges.

- Mae, the Maintainer
