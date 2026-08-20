# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (maintainer run 32392140959, triggered by owner issue_comment on PR #93). **OWNER PIVOT (2026-08-20T14:52:11Z) REMAINS THE STANDING LAW.**
- **OWNER PIVOT DIRECTIVE (2026-08-20T14:52:11Z):** "keep the two projects separate. For the current project, finish the documentation, testing, and review, then close it. There is no need to continue developing the new codec in this project. I lift the JPEG XL gate for this one. After that, start a new project with a new codebase and a new name. That new project will have the JPEG XL gate: keep researching, architecting, building toward beating JPEG XL and the other established codecs."
- **Translation:** PR #93 (Obsidian) is a **FINISH-AND-CLOSE** job (docs -> test -> review -> merge). The JPEG XL gate is LIFTED for PR #93. The new JXL-class codec is a SEPARATE project (new codebase + new name) on its OWN issue/branch, NOT inside PR #93.

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted.** Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on Kodak) with full docs; then Test + Review + merge. Keep branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying the JPEG XL 8.71 gate, developed on its OWN issue/branch (research -> architect -> build). Never folded into PR #93.
- **ONE Obsidian PR only (now being wound down):** PR #93 is the single canonical Obsidian PR, branch `opencode/issue68-20260818070512`. After it merges, the "one-PR" rule applies to the new project's PR, not Obsidian.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68 on PR #93 merge; close it only when the JXL gate is cleared by the new project.

## CRITICAL INFRASTRUCTURE STATE (unchanged, healthy)

- **PR #91 MERGED:** orphan-main guard. **PR #92 MERGED:** `main` = `d6b2894`, determinism guard + umbrella rule + force-with-lease pin.
- **`main` = `d6b2894`** (healthy, clean descendant of prior main).
- **Branch `opencode/issue68-20260818070512` OPEN, head `20d1162168af610642a605e76a0c4b21fe11fd94`** (Builder R15 halt escalation `20d1162`; Researcher R15 spec `4db4f97`; Architect R15 blueprint `ea914a8`; R14/R13-* gated off/muted). PR #93 reports `mergeable: true / mergeable_state: clean`. Shallow-clone local `git merge-base` returns NONE (false negative, not an orphan break). One-PR rule intact.

## SYSTEMIC INFRASTRUCTURE BLOCKER (HOLLOW-BUILD) - NOW ACTIVELY FIXED

- **HOLLOW-BUILD CONFIRMED (2nd no-op):** the PR #93 docs Builder no-op'd TWICE - opencode run 32382581730 (14:50:48Z) and run 32391993368 (16:26:25Z) both `completed` green but pushed NOTHING (head still `20d1162`, no docs commit). Root cause: the Builder's `continue` resume re-reads the stale progress file (last entry 14:45:38Z "Decision: maintainer", the pre-pivot "beat JXL" task) and does NOT re-task on the owner's 14:52:11Z pivot. Weak build model (`opencode/hy3-free`) compounds the misread.
- **DISPATCHED `lab` (run 32392140959):** the Lab Engineer will (1) fix `.github/agents/builder.md` so `/oc continue` re-tasks on a divergent newer owner/maintainer directive; (2) audit `opencode.yml` "Verify build pushed" / "Forward builder decision"; (3) upgrade the build model to the strongest free model (nemotron-3-ultra-free / deepseek-v4-flash-free). Do NOT loop `continue` endlessly (forbidden by my own rule; escalation now fired).

## PRIORITY PROJECT (Obsidian, PR #93) - FINISH-AND-CLOSE

- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL, CMARC backend; R13-A muted, R13-B/R14/R15 gated off). Beats PNG (13.05) + WebP (9.61). JXL gate LIFTED for this project.
- **R0-R15 codec on PR #93:** R13-A committed but MUTED. R13-B committed, REGRESSION, gated off. R14 committed, REGRESSION, gated off. R15 committed, NET-NEGATIVE, gated off. 152 lib tests pass.
- **The 10-axis ceiling (data-backed, exhausted at ~9.52 bpp):** R11-D, R11-A, 64-leaf x2, R12-A, R13-A, R13-B, R14-A, R15-A, CMARC backend. Proven structural; no further tuning of that family will be dispatched. (Moot for PR #93 anyway - JXL gate lifted.)

## CURRENT STATE - THIS RUN (32392140959)

- **Dispatched `lab` (head `20d1162`) to fix the hollow-build root cause** so the next `continue` writes PR #93's documentation and pushes. The Lab Engineer works on its OWN PR (infra changes to builder.md / opencode.yml / opencode.json); it does NOT write project docs.
- **No Builder in flight at survey time:** run 32391993368 `completed` (no-op); no other `in_progress`/`queued` opencode runs on the branch.

## IN FLIGHT

- **Lab Engineer (fix hollow-build):** dispatched THIS run via `lab` (head `20d1162`). Must fix builder.md resume/re-task + audit opencode.yml verify-pushed + upgrade build model. Creates its own PR.

## PENDING (awaiting completion, in order)

- **PR #93 docs (Step 1):** after the `lab` fix lands, re-drive `continue`; Builder writes full Obsidian docs (CLI usage, all flags/options/features, shipped R10-B+CMARC path, gated R13/R14/R15 with honest measurements) and PUSHES (head advances past 20d1162). Must cover `--effort`, `--predictor`, `--transform`, `--rcct`, `--nrp` and `OBSIDIAN_*` seams, plus stability/speed trade-offs. Required before merge. Step 2 (new codec IN PR #93) is CANCELED by the pivot.
- **PR #93 Tester:** run `/oc test` (Tester) on PR #93 after docs land - QA + real-Kodak reproducibility.
- **PR #93 Reviewer:** run `/oc review` (Reviewer) - strict read-only quality gate (architecture, security, static standards).
- **PR #93 merge:** rebase-merge (`--no-delete-branch`) once docs + tests + review done. JXL gate lifted. Keep branch. Do NOT close #68 (umbrella stays open for the new project).
- **NEW project (JXL gate):** after PR #93 merges, stand up a separate codebase with a new name on its own issue/branch. Seed via `ideate` or owner-opened issue; then route research -> architect -> build for the JXL-class codec (FLIF/JXL-modular context-tree predictor family is the proven direction). Never in PR #93.

## ISSUES

- **#68 (Obsidian umbrella)** - OPEN, stays open until the new JXL-class project beats codecs (per pivot + standing directive).
- **#52 / #89 / #90 / #91 / #92 infra** - merged/closed; branches kept.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; new project seeding may use it post-PR #93 close.

## REVIEWER/TESTER/MODEL STATUS

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError`. Stronger free models available (nemotron-3-ultra-free, deepseek-v4-flash-free, nemotron-3.5-lightning-free, laguna-s-2.1-free) - Lab Engineer to upgrade the weak build model.
- **pages.yml:** green.
- **PR #93 checks:** opencode-pr-trigger SUCCESS; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS.

## NEXT STEPS

1. **Lab Engineer fix (in flight):** wait for the `lab` PR; it fixes builder.md resume/re-task + opencode.yml verify-pushed + build model. On its merge, the hollow-build is closed.
2. **PR #93 docs (Step 1):** re-drive `continue`; Builder writes full Obsidian docs and pushes (head advances). On its push, a maintainer run re-surveys, confirms docs COMPLETE and no new-codec work in PR #93 (pivot Step 2 canceled), then dispatches Tester.
3. **PR #93 test+review:** dispatch Tester then Reviewer once docs land.
4. **PR #93 merge:** rebase-merge (`--no-delete-branch`) after docs+tests+review; keep #68 open.
5. **NEW JXL project:** stand up separate codebase/new name on its own issue/branch; route research -> architect -> build.

## OPEN QUESTIONS

- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, merges cleanly with main). After merge, applies to new project's PR.
- **Orphan-main break:** NOT present - PR `mergeable: clean`; local NONE is a shallow-clone artifact.
- **Build collision:** AVOIDED (no Builder running at survey; `lab` is infra, separate track).
- **Pivot Step 2 cancellation honored?** UNVERIFIED until the Builder pushes docs - must confirm no new codec was committed into PR #93; if it was, revert via `fix` and re-route to the separate new project.
- **Hollow-build fix efficacy:** PENDING the `lab` PR; after it merges, a re-driven `continue` must actually push docs (head advances past 20d1162) - otherwise the Lab Engineer's fix was insufficient and I escalate further.
- **Work preservation:** all R0-R15 codec work preserved on PR #93 (never-merged, branch kept). #68 open as umbrella.
- **New-project issue:** needs an issue. Owner may open it, or I dispatch `ideate` post-PR #93 close. Recorded as pending.
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **pages.yml / billing / commit hygiene:** green; PR #93 body correctly `Refs #68`; future commits avoid literal `Closes #68`.

- Mae, the Maintainer