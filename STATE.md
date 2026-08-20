# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (maintainer run 32393370107, triggered by PR #95 creation / owner `/oc` activity). **OWNER PIVOT (2026-08-20T14:52:11Z) REMAINS THE STANDING LAW.**
- **OWNER PIVOT DIRECTIVE (2026-08-20T14:52:11Z):** "keep the two projects separate. For the current project, finish the documentation, testing, and review, then close it. There is no need to continue developing the new codec in this project. I lift the JPEG XL gate for this one. After that, start a new project with a new codebase and a new name. That new project will have the JPEG XL gate: keep researching, architecting, building toward beating JPEG XL and the other established codecs."
- **Translation:** PR #93 (Obsidian) is a **FINISH-AND-CLOSE** job (docs -> test -> review -> merge). The JPEG XL gate is LIFTED for PR #93. The new JXL-class codec is a SEPARATE project (new codebase + new name) on its OWN issue/branch, NOT inside PR #93.

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted.** Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on Kodak) with full docs; then Test + Review + merge. Keep branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying the JPEG XL 8.71 gate, developed on its OWN issue/branch (research -> architect -> build). Never folded into PR #93.
- **ONE Obsidian PR only (now being wound down):** PR #93 is the single canonical Obsidian PR, branch `opencode/issue68-20260818070512`. After it merges, the "one-PR" rule applies to the new project's PR, not Obsidian.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68 on PR #93 merge; close it only when the JXL gate is cleared by the new project.

## CRITICAL INFRASTRUCTURE STATE (healthy)

- **PR #91 MERGED:** orphan-main guard. **PR #92 MERGED:** `main` = `d6b2894`, determinism guard + umbrella rule + force-with-lease pin.
- **`main` = `d6b2894`** (healthy, clean descendant of prior main).
- **Branch `opencode/issue68-20260818070512` OPEN, head `20d1162168af610642a605e76a0c4b21fe11fd94`** (Builder R15 halt escalation `20d1162`; Researcher R15 spec `4db4f97`; Architect R15 blueprint `ea914a8`; R14/R13-* gated off/muted). PR #93 reports `mergeable: true / mergeable_state: clean`. Shallow-clone local `git merge-base` returns NONE (false negative, not an orphan break). One-PR rule intact.
- **Branch `opencode/lab-94-no-op-build-detection` OPEN, head `58ea05e670163abbb8e909e91b08f0b05a21c5cd`** (PR #95). `main` is ancestor -> clean, no orphan risk. MERGEABLE / CLEAN.

## SYSTEMIC INFRASTRUCTURE BLOCKER (HOLLOW-BUILD) - PARTIALLY FIXED, ROOT CAUSE STILL OPEN

- **HOLLOW-BUILD CONFIRMED (2nd no-op):** the PR #93 docs Builder no-op'd TWICE - opencode run 32382581730 (14:50:48Z) and run 32391993368 (16:26:25Z) both `completed` green but pushed NOTHING (head still `20d1162`, no docs commit). Root cause: the Builder's `/oc continue` resume re-reads the stale progress file (last entry 14:45:38Z "Decision: maintainer", the pre-pivot "beat JXL" task) and does NOT re-task on the owner's 14:52:11Z pivot.
- **DETECTION HALF-FIX SHIPPED (PR #95 / issue #94):** PR #95 adds a `Diagnose silent build no-op` step to `opencode.yml` so a genuine silent no-op (no push, no decision, no pending retry) is surfaced. Reviewer required a guard (`if: always() && steps.verify.outputs.retry != 'true'`) to avoid false-positive spam on every auto-retry; that guard is present in commit `58ea05e` -> Reviewer's conditional is SATISFIED. PR #95 now in re-review (run 32393370107).
- **ROOT CAUSE (builder.md resume + weak build model) STILL OPEN:** PR #95 only adds DETECTION. The actual fix - make `.github/agents/builder.md` `/oc continue` re-task on the newest divergent owner/maintainer directive, and upgrade the build model to the strongest free model (nemotron-3-ultra-free / deepseek-v4-flash-free) - has NOT been delivered. PR #93 docs will still no-op on `continue` until this lands. **This is the next lab dispatch, sequenced AFTER PR #95 merges** (both touch `opencode.yml`; parallel lab PRs would conflict).

## PRIORITY PROJECT (Obsidian, PR #93) - FINISH-AND-CLOSE (BLOCKED on root-cause lab fix)

- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL, CMARC backend; R13-A muted, R13-B/R14/R15 gated off). Beats PNG (13.05) + WebP (9.61). JXL gate LIFTED for this project.
- **R0-R15 codec on PR #93:** R13-A committed but MUTED. R13-B committed, REGRESSION, gated off. R14 committed, REGRESSION, gated off. R15 committed, NET-NEGATIVE, gated off. 152 lib tests pass.

## CURRENT STATE - THIS RUN (32393370107)

- **PR #95 (lab infra, head `58ea05e`):** Reviewer's conditional finding satisfied on the branch. Dispatched `review` (re-review) this run to get formal `/oc approve` and advance to Tester then merge. Not merging yet (no formal Reviewer approval; Tester not run).
- **PR #93 (Obsidian, head `20d1162`):** in flight; docs BLOCKED by hollow-build root cause (builder.md resume + model). Detection-only fix (PR #95) does not unblock it.

## IN FLIGHT

- **PR #95 review:** re-review triggered THIS run (`review`, head `58ea05e`). On `/oc approve` -> Tester -> `/oc approve-test` -> maintainer merge.
- **PR #93 root-cause lab fix (builder.md resume + model upgrade):** PENDING, to be dispatched as `lab` AFTER PR #95 merges.

## PENDING (awaiting completion, in order)

- **PR #95 merge:** rebase-merge (`--no-delete-branch`) once Reviewer approves + Tester passes. Lab infra change, not a new project (shipping limit N/A). Keep branch.
- **PR #93 root-cause `lab` (after PR #95 merges):** fix `.github/agents/builder.md` `/oc continue` re-task on divergent newer directive + upgrade build model. Own PR/branch.
- **PR #93 docs (Step 1):** after the root-cause `lab` fix lands, re-drive `continue`; Builder writes full Obsidian docs (CLI usage, all flags/options/features, shipped R10-B+CMARC path, gated R13/R14/R15 with honest measurements) and PUSHES (head advances past 20d1162). Required before merge. Step 2 (new codec IN PR #93) is CANCELED by the pivot.
- **PR #93 Tester:** run `/oc test` on PR #93 after docs land - QA + real-Kodak reproducibility.
- **PR #93 Reviewer:** run `/oc review` - strict read-only quality gate.
- **PR #93 merge:** rebase-merge (`--no-delete-branch`) once docs + tests + review done. JXL gate lifted. Keep branch. Do NOT close #68.
- **NEW project (JXL gate):** after PR #93 merges, stand up a separate codebase with a new name on its own issue/branch. Seed via `ideate` or owner-opened issue; then route research -> architect -> build. Never in PR #93.

## ISSUES

- **#68 (Obsidian umbrella)** - OPEN, stays open until the new JXL-class project beats codecs (per pivot + standing directive).
- **#94 (Detect silent no-op builds)** - OPEN; implemented by PR #95, closes on PR #95 merge.
- **#52 / #89 / #90 / #91 / #92 infra** - merged/closed; branches kept.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; new project seeding may use it post-PR #93 close.

## REVIEWER/TESTER/MODEL STATUS

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError`. Stronger free models available (nemotron-3-ultra-free, deepseek-v4-flash-free, nemotron-3.5-lightning-free, laguna-s-2.1-free) - Lab Engineer to upgrade the weak build model (pending root-cause lab).
- **pages.yml:** green.
- **PR #93 checks:** opencode-pr-trigger SUCCESS; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS.
- **PR #95 checks:** open; in re-review. Note: Lab Engineer's direct push of `opencode.yml` was rejected by GitHub's app-permission guard ("without workflows permission") but the PAT-backed step delivered the branch. Non-blocking; owner may grant the app `Workflows` permission for cleaner lab pushes.

## NEXT STEPS

1. **PR #95 review -> test -> merge:** re-review (this run) should post `/oc approve`; Tester runs; on `/oc approve-test` a maintainer run merges (keep branch).
2. **PR #93 root-cause `lab` (after PR #95 merges):** dispatch `lab` to fix builder.md resume re-task + upgrade build model, on its own PR/branch.
3. **PR #93 docs (Step 1):** re-drive `continue`; Builder writes full Obsidian docs and pushes (head advances). On its push, a maintainer run re-surveys, confirms docs COMPLETE and no new-codec work in PR #93 (pivot Step 2 canceled), then dispatches Tester.
4. **PR #93 test+review:** dispatch Tester then Reviewer once docs land.
5. **PR #93 merge:** rebase-merge (`--no-delete-branch`) after docs+tests+review; keep #68 open.
6. **NEW JXL project:** stand up separate codebase/new name on its own issue/branch; route research -> architect -> build.

## OPEN QUESTIONS

- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, merges cleanly). After merge, applies to new project's PR.
- **Orphan-main break:** NOT present - both PRs `mergeable: clean`; local NONE is a shallow-clone artifact.
- **Build collision:** AVOIDED (no Builder running at survey; `lab` is infra, separate track).
- **Pivot Step 2 cancellation honored?** UNVERIFIED until the Builder pushes docs - must confirm no new codec was committed into PR #93; if it was, revert via `fix` and re-route to the separate new project.
- **Hollow-build fix efficacy:** DETECTION shipped (PR #95); ROOT CAUSE (builder.md + model) still pending a follow-up `lab` after PR #95 merges. Until then, a re-driven `continue` will still no-op.
- **Work preservation:** all R0-R15 codec work preserved on PR #93 (never-merged, branch kept). #68 open as umbrella.
- **New-project issue:** needs an issue. Owner may open it, or I dispatch `ideate` post-PR #93 close. Recorded as pending.
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge. PR #95 in re-review now.
- **`workflows` permission:** opencode app lacks `Workflows` permission; direct agent pushes of workflow files are rejected but PAT-backed step delivers. Owner can grant; non-blocking.
- **pages.yml / billing / commit hygiene:** green; PR #93 body correctly `Refs #68`; future commits avoid literal `Closes #68`.

- Mae, the Maintainer
