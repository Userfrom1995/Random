# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~02:18Z, maintainer event run 32324140838, triggered by owner `/oc maintainer` on issue #68). Broke the `lab #68` re-link loop by routing `continue` (Builder) - the Builder is the agent that actually pushes to the obsidian branch and is contractually instructed (opencode.yml:340) to rebuild orphaned branches onto main.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`. (#91 + #92 branches `opencode/lab-68-orphan-main-guard` intentionally left intact.)
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. Still deferred; schedule once JXL nears / #83 reopens.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. TEMPORARILY BROKEN (PR #83 CLOSED, zero open Obsidian PRs) - recovery dispatched THIS run via `continue` (Builder rebuilds branch + reopens #83).
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec).
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83 (or issue #68 for factory/lab) - not on a new PR.

## CRITICAL INFRASTRUCTURE STATE (orphan-main guard MERGED; branch re-link NOW IN FLIGHT VIA BUILDER)

- **PR #91 MERGED (02:00Z):** `c043b7e` orphan-main guard (note: commit msg carries literal `Closes #68` token, which auto-closed #68; reopened same run).
- **PR #92 MERGED (02:11Z):** `main` = `d6b2894`. Adds determinism guard + "do not auto-close umbrella" rule + force-with-lease pin. Body `Refs #68`, no new auto-close token.
- **`main` = `d6b2894`** (after PR #92). HEALTHY, 370 commits, clean descendant of prior main.
- **Branch `opencode/issue68-20260818070512` (head `0deef55`) STILL ORPHANED** (empty merge-base, re-verified this run). Holds 9.5208 codec + R11-D blueprint + durable Kodak corpus. INTACT, not deleted.
- **Root cause of the stall (resolved path):** the Lab Engineer repeatedly shipped guards but refused the actual branch re-link, routing back to Mae, who cannot push. The Builder's build-job contract (opencode.yml:340) is the correct re-link executor. Dispatched `continue` THIS run.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub auto-closes #68 if the literal `Closes #68` token appears ANYWHERE (body OR commit message). Confirmed 02:00Z (commit `c043b7e`). Lesson locked: future Builder/Lab commits must use `Refs #68` / `Refs to #68`, never `Closes #68`.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian):** OPEN, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **M0 COMPLETE & MERGED** (PR #82).
- **Default shipped codec = 9.5208 bpp mean** (R10-B CFL). Beats PNG (13.05) + WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
- **R11-D (MA-tree / property-tree in-loop context)** = next blueprinted step to clear the JXL gap; blueprint on-branch.

## In flight

- **`continue` on issue #68 (DISPATCHED THIS run, 32324140838):** Builder rebuilds orphaned branch onto `origin/main` (checkout -B + cherry-pick own commits + force-push BRANCH only), reopens PR #83 as the single canonical Obsidian PR (body `Refs #68`, NEVER `Closes #68`), then resumes R11-D toward the JXL 8.71 gate. This is the recovery that `lab #68` refused to perform.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above (default 9.5208); R11-D is the next attempt.
- **Resume Builder (R11-D) via `continue`** - in flight this run.
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once JXL nears / #83 reopens).
- **Review staleness on #83:** head `0deef55` un-reviewed. Fresh review required pre-merge.
- **Commit-message hygiene:** never write literal `Closes #68` token in ANY commit message or PR body.

## Issues

- **#68 (Obsidian umbrella)** - OPEN, active fundamental goal, stays open until codecs beaten.
- **#52 / #89 / #90 / #91 / #92 infra** - #90 MERGED; #89 CLOSED; #52 related; #91 MERGED (guard); #92 MERGED (guard + umbrella rule + force-with-lease pin). Both branches kept.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule; board live.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.
- **#71/#72/#73/#74/#75 (prior audit bugs)** - all CLOSED; root causes fixed.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError` in recent runs.
- **Pending re-link:** branch `opencode/issue68-20260818070512` orphaned (head `0deef55`); recovery via `continue` (Builder) dispatched this run.
- **pages.yml:** last triggered manually after PR #92 merge (32323756029); verify green.

## Next steps

1. **Builder `continue` (in flight):** rebuild orphaned branch onto `origin/main` + force-push BRANCH only; reopen PR #83 (body `Refs #68`); resume R11-D.
2. **After branch re-link + #83 reopen:** Builder implements R11-D (MA-tree context), re-measures REAL Kodak effort-4 against the JPEG XL 8.71 gate. Loop via `continue` until all three gates clear.
3. **After R11-D measured:** if default < 8.71 JXL (alongside PNG 13.05 + WebP 9.61), fresh review + Tester gate, then rebase-merge (`--no-delete-branch`) and close #68. NOT before.
4. **README / index.html promotion:** schedule once JXL nears / PR reopens.

## Open questions

- **Will the Builder `continue` actually re-link + reopen?** It is the correct executor (pushes to the branch, contractually rebuilds orphaned branches). High confidence if the run executes and follows opencode.yml:340. Verify next run that merge-base is non-empty and PR #83 OPEN.
- **Will R11-D clear the +0.81 JPEG XL gap on REAL Kodak?** Blueprint on-branch; verdict pending the Builder's R11-D build + real-Kodak re-measure. NOT yet a 100%-certain unmovable wall.
- **Merge gate (owner override #2):** NOT met - default 9.5208 beats PNG + WebP but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **One-PR integrity:** temporarily broken (PR #83 CLOSED) until the Builder reopens it this cycle.
- **pages.yml:** verify green after PR #92 merge.
- **Billing:** resolved (no `CreditsError`; `small_model` correctly pinned free).

- Mae, the Maintainer