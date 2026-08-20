# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (maintainer run 32393955210, triggered by PR #95 creation / owner `/oc` activity). **OWNER PIVOT (2026-08-20T14:52:11Z) REMAINS THE STANDING LAW.**
- **OWNER PIVOT DIRECTIVE (2026-08-20T14:52:11Z):** "keep the two projects separate. For the current project, finish the documentation, testing, and review, then close it. There is no need to continue developing the new codec in this project. I lift the JPEG XL gate for this one. After that, start a new project with a new codebase and a new name. That new project will have the JPEG XL gate: keep researching, architecting, building toward beating JPEG XL and the other established codecs."
- **Translation:** PR #93 (Obsidian) is a **FINISH-AND-CLOSE** job (docs -> test -> review -> merge). The JPEG XL gate is LIFTED for PR #93. The new JXL-class codec is a SEPARATE project (new codebase + new name) on its OWN issue/branch, NOT inside PR #93.

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted.** Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on Kodak) with full docs; then Test + Review + merge. Keep branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying the JPEG XL 8.71 gate, developed on its OWN issue/branch (research -> architect -> build). Never folded into PR #93.
- **ONE Obsidian PR only (now being wound down):** PR #93 is the single canonical Obsidian PR, branch `opencode/issue68-20260818070512`. After it merges, the "one-PR" rule applies to the new project's PR, not Obsidian.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68 on PR #93 merge; close it only when the JXL gate is cleared by the new project.

## CRITICAL INFRASTRUCTURE STATE (healthy)

- **PR #95 MERGED (run 32393955210):** `main` = `37f0395cfc37c28b8cbe8786d504427422ad91f4`. Branch `opencode/lab-94-no-op-build-detection` kept (NOT deleted). Orphan-main guard verified: `git merge-base origin/main 58ea05e` = `d6b2894` (clean, `main` is the common ancestor, no orphan risk). Reviewer approved 16:46:09Z, Tester approved-test 16:47:12Z, no newer `/oc fix` findings.
- **Issue #94 CLOSED** (silent no-op detection shipped by PR #95).
- **`main` = `37f0395`** (healthy, clean descendant of prior main).

## SYSTEMIC INFRASTRUCTURE BLOCKER (HOLLOW-BUILD) - DETECTION SHIPPED, ROOT-CAUSE LAB NOW DISPATCHED

- **HOLLOW-BUILD CONFIRMED (2nd no-op):** PR #93 docs Builder no-op'd TWICE (opencode 32382581730 @14:50:48Z and 32391993368 @16:26:25Z), both `completed` green but pushed NOTHING (head still `20d1162`, no docs commit). Root cause: the Builder's `/oc continue` resume re-reads the stale progress file (last entry 14:45:38Z "Decision: maintainer", the pre-pivot "beat JXL" task) and does NOT re-task on the owner's 14:52:11Z pivot.
- **DETECTION FIX SHIPPED (PR #95 / issue #94, MERGED):** adds a `Diagnose silent build no-op` step to `opencode.yml` (guard `if: always() && steps.verify.outputs.retry != 'true'`). Surfaces a genuine silent no-op (no push, no decision, no pending retry) without false-positive spam on auto-retries. MERGED this run.
- **ROOT-CAUSE LAB NOW DISPATCHED (run 32393955210):** with PR #95 merged, the Lab Engineer is now clear to (1) fix `.github/agents/builder.md` so `/oc continue` re-tasks on the newest divergent owner/maintainer directive, and (2) upgrade the weak build model (`opencode/hy3-free`) to the strongest free model (nemotron-3-ultra-free / deepseek-v4-flash-free) in `opencode.yml` + `opencode.json`. Own PR/branch (no collision with #95 now that it is merged). This unblocks PR #93's Step 1 (docs).

## PRIORITY PROJECT (Obsidian, PR #93) - FINISH-AND-CLOSE (BLOCKED on root-cause lab fix)

- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL, CMARC backend; R13-A muted, R13-B/R14/R15 gated off). Beats PNG (13.05) + WebP (9.61). JXL gate LIFTED for this project. 152 lib tests pass.

## CURRENT STATE - THIS RUN (32393955210)

- **PR #95 (lab infra, head `58ea05e`):** MERGED (rebase, branch kept; `main` now `37f0395`). Reviewer + Tester approved; issue #94 closed.
- **PR #93 (Obsidian, head `20d1162`):** in flight; docs BLOCKED by hollow-build root cause (builder.md resume + model). Detection-only fix (PR #95) merged; root-cause `lab` now dispatched.
- **Root-cause `lab` DISPATCHED** (decision entry, target PR/issue #93) to fix builder.md resume re-task + upgrade build model.

## IN FLIGHT

- **PR #93 root-cause lab fix (builder.md resume re-task + model upgrade):** DISPATCHED THIS run (`lab`, target #93). On its PR/branch, sequenced after PR #95 merge.
- **PR #93 docs (Step 1):** PENDING the root-cause `lab` fix. After it lands, re-drive `continue`; Builder writes full Obsidian docs (CLI usage, all flags/options/features, shipped R10-B+CMARC path, gated R13/R14/R15 with honest measurements) and PUSHES (head advances past 20d1162). Required before merge. Step 2 (new codec IN PR #93) is CANCELED by the pivot.

## PENDING (awaiting completion, in order)

- **PR #93 root-cause `lab` (dispatched):** fix `.github/agents/builder.md` `/oc continue` re-task on divergent newer directive + upgrade build model. Own PR/branch.
- **PR #93 docs (Step 1):** after the root-cause `lab` fix lands, re-drive `continue`; Builder writes full Obsidian docs and pushes (head advances). On its push, a maintainer run re-surveys, confirms docs COMPLETE and no new-codec work in PR #93 (pivot Step 2 canceled), then dispatches Tester.
- **PR #93 Tester:** run `/oc test` on PR #93 after docs land - QA + real-Kodak reproducibility.
- **PR #93 Reviewer:** run `/oc review` - strict read-only quality gate.
- **PR #93 merge:** rebase-merge (`--no-delete-branch`) once docs + tests + review done. JXL gate lifted. Keep branch. Do NOT close #68.
- **NEW project (JXL gate):** after PR #93 merges, stand up a separate codebase with a new name on its own issue/branch. Seed via `ideate` or owner-opened issue; then route research -> architect -> build. Never in PR #93.

## ISSUES

- **#68 (Obsidian umbrella)** - OPEN, stays open until the new JXL-class project beats codecs (per pivot + standing directive).
- **#94 (Detect silent no-op builds)** - CLOSED (implemented by merged PR #95).
- **#52 / #89 / #90 / #91 / #92 infra** - merged/closed; branches kept.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; new project seeding may use it post-PR #93 close.

## REVIEWER/TESTER/MODEL STATUS

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). After the root-cause `lab`, the build model will be upgraded to the strongest free model (nemotron-3-ultra-free / deepseek-v4-flash-free). `origin/main` = `37f0395`. No `CreditsError`. Stronger free models available - Lab Engineer to upgrade the weak build model.
- **pages.yml:** re-triggered post-merge this run (run 32394126388); historically green. Verify deploy succeeded.
- **PR #93 checks:** opencode-pr-trigger SUCCESS; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS.
- **PR #95 checks:** merged; Reviewer + Tester approved.

## NEXT STEPS

1. **PR #93 root-cause `lab` (DISPATCHED):** Lab Engineer fixes builder.md resume re-task + upgrades build model on its own PR/branch.
2. **PR #93 docs (Step 1):** re-drive `continue` after the lab fix lands; Builder writes full Obsidian docs and pushes (head advances). On its push, a maintainer run re-surveys, confirms docs COMPLETE and no new-codec work in PR #93 (pivot Step 2 canceled), then dispatches Tester.
3. **PR #93 test+review:** dispatch Tester then Reviewer once docs land.
4. **PR #93 merge:** rebase-merge (`--no-delete-branch`) after docs+tests+review; keep #68 open.
5. **NEW JXL project:** stand up separate codebase/new name on its own issue/branch; route research -> architect -> build.

## OPEN QUESTIONS

- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, merges cleanly). After merge, applies to new project's PR.
- **Orphan-main break:** NOT present - both PRs `mergeable: clean`; local NONE was a shallow-clone artifact.
- **Build collision:** AVOIDED (no Builder running at survey; `lab` is infra, separate track).
- **Pivot Step 2 cancellation honored?** UNVERIFIED until the Builder pushes docs - must confirm no new codec was committed into PR #93; if it was, revert via `fix` and re-route to the separate new project.
- **Hollow-build fix efficacy:** DETECTION shipped + MERGED (PR #95); ROOT CAUSE (builder.md + model) now being fixed by the dispatched `lab`. Until then, a re-driven `continue` will still no-op.
- **Work preservation:** all R0-R15 codec work preserved on PR #93 (never-merged, branch kept). #68 open as umbrella.
- **New-project issue:** needs an issue. Owner may open it, or I dispatch `ideate` post-PR #93 close. Recorded as pending.
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge. PR #95 in re-review now.
- **`workflows` permission:** opencode app lacks `Workflows` permission; direct agent pushes of workflow files are rejected but PAT-backed step delivers. Owner can grant; non-blocking.
- **pages.yml / billing / commit hygiene:** green; PR #93 body correctly `Refs #68`; future commits avoid literal `Closes #68`.

- Mae, the Maintainer
