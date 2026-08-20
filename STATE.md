# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~14:53Z, maintainer run 32382726407, triggered by owner `/oc maintainer` on PR #93 at 14:52:11Z with a PIVOT directive). **OWNER PIVOT (replaces the Step 2 "new codec inside PR #93" plan).**
- **OWNER PIVOT DIRECTIVE (2026-08-20T14:52:11Z):** "keep the two projects separate. For the current project, finish the documentation, testing, and review, then close it. There is no need to continue developing the new codec in this project. I lift the JPEG XL gate for this one. After that, start a new project with a new codebase and a new name. That new project will have the JPEG XL gate: keep researching, architecting, b…"
- **Translation:** PR #93 (Obsidian) is now a **FINISH-AND-CLOSE** job (docs → test → review → merge). The JPEG XL gate is LIFTED for PR #93. The new JXL-class codec becomes a SEPARATE project (new codebase + new name) on its own issue/branch, NOT inside PR #93.

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted.** Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on Kodak) with full docs; then Test + Review + merge. Keep branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying the JPEG XL 8.71 gate, developed on its OWN issue/branch (research → architect → build). Never folded into PR #93.
- **ONE Obsidian PR only (now being wound down):** PR #93 is the single canonical Obsidian PR, branch `opencode/issue68-20260818070512`. After it merges, the "one-PR" rule applies to the new project's PR, not Obsidian.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68 on PR #93 merge; close it only when the JXL gate is cleared by the new project.

## CRITICAL INFRASTRUCTURE STATE (unchanged, healthy)

- **PR #91 MERGED:** orphan-main guard. **PR #92 MERGED:** `main` = `d6b2894`, determinism guard + umbrella rule + force-with-lease pin.
- **`main` = `d6b2894`** (healthy, clean descendant of prior main).
- **Branch `opencode/issue68-20260818070512` OPEN, head `20d1162168af610642a605e76a0c4b21fe11fd94`** (Builder R15 halt escalation doc; Researcher R15 spec `4db4f97`; Architect R15 blueprint `ea914a8`; R14/R13-* gated off/muted). Merge-base `d6b2894` non-empty. PR #93 single canonical, one-PR rule intact.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub auto-closes #68 if literal `Closes #68` appears ANYWHERE. Future commits MUST use `Refs #68` / `Refs to #68`. PR #93 body is correctly `Refs #68`.

## PRIORITY PROJECT (Obsidian, PR #93) - FINISH-AND-CLOSE

- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL, CMARC backend; R13-A muted, R13-B/R14/R15 gated off). Beats PNG (13.05) + WebP (9.61). JXL gate LIFTED for this project.
- **R0-R15 codec on PR #93:** R13-A committed but MUTED (9.9065 regression). R13-B committed, REGRESSION (10.17/10.58), gated off. R14 committed, REGRESSION (9.66), gated off. R15 committed, NET-NEGATIVE (byte-identical 9.5209), gated off. 152 lib tests pass.
- **The 10-axis ceiling (data-backed, exhausted at ~9.52 bpp):** R11-D, R11-A, 64-leaf x2, R12-A, R13-A, R13-B, R14-A, R15-A, CMARC backend. Proven structural; no further tuning of that family will be dispatched. (Now moot for PR #93 anyway — JXL gate lifted.)

## CURRENT STATE - OWNER PIVOT (this run)

- **Builder run 32382581730 IN FLIGHT** (owner `/oc continue` 14:50:48Z), currently executing Step 1 (full Obsidian documentation on PR #93). The owner still wants this. **Step 2 (new codec inside PR #93) is CANCELLED by the pivot.** On this Builder's push, redirect it to STOP before any new-codec work and finalize docs only.
- **This run's action: HOLD (empty decision list).** A Builder is in flight on the branch; firing a second `continue`/`build` would collide. A maintainer run auto-triggers on the Builder's push; I will act then. No merge (docs + test + review not yet done).

## IN FLIGHT

- **Builder (docs, PR #93):** opencode run **32382581730**, branch `opencode/issue68-20260818070512`, dispatched by owner `/oc continue` 2026-08-20T14:50:48Z. Executing Step 1 (docs) — still wanted. Must be redirected away from Step 2 (new codec) on its push. No concurrent Builder at decision time.

## PENDING (awaiting completion, in order)

- **PR #93 docs (Step 1):** full CLI usage, every flag/option/feature, stable shipped R10-B+CMARC path + gated R13/R14/R15 experiments with honest measurements. Must cover `--effort`, `--predictor`, `--transform`, `--rcct`, `--nrp` and `OBSIDIAN_*` seams, plus stability/speed trade-offs. Required before merge.
- **PR #93 Tester:** run `/oc test` (Tester) on PR #93 after docs land — QA + real-Kodak reproducibility.
- **PR #93 Reviewer:** run `/oc review` (Reviewer) — strict read-only quality gate (architecture, security, static standards).
- **PR #93 merge:** rebase-merge (`--no-delete-branch`) once docs + tests + review done. JXL gate lifted. Keep branch. Do NOT close #68 (umbrella stays open for the new project).
- **NEW project (JXL gate):** after PR #93 merges, stand up a separate codebase with a new name on its own issue/branch. Owner to open the issue (or I dispatch `ideate` to seed candidates); then route research → architect → build for the JXL-class codec (FLIF/JXL-modular primary context-tree predictor family is the proven direction). Never in PR #93.

## ISSUES

- **#68 (Obsidian umbrella)** - OPEN, stays open until the new JXL-class project beats codecs (per pivot + standing directive).
- **#52 / #89 / #90 / #91 / #92 infra** - merged/closed; branches kept.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; new project seeding may use it post-PR #93 close.

## REVIEWER/TESTER/MODEL STATUS

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError`.
- **pages.yml:** green.
- **PR #93 checks:** opencode-pr-trigger SUCCESS on R15 push; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS.

## NEXT STEPS

1. **PR #93 docs (in flight):** Builder run 32382581730 completes Obsidian documentation. On its push, a maintainer run re-surveys, redirects the Builder to stop before Step 2 (new codec), and confirms docs are complete.
2. **PR #93 test+review:** dispatch Tester then Reviewer once docs land.
3. **PR #93 merge:** rebase-merge (`--no-delete-branch`) after docs+tests+review; keep #68 open.
4. **NEW JXL project:** stand up separate codebase/new name on its own issue/branch; route research → architect → build.

## OPEN QUESTIONS

- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, shares history with main). After merge, applies to new project's PR.
- **Orphan-main break:** RESOLVED (merge-base `d6b2894` non-empty; PR #93 healthy).
- **Build collision:** AVOIDED this run (held; Builder 32382581730 in flight). Will re-assess on Builder push.
- **Work preservation:** all R0-R15 codec work preserved on PR #93 (never-merged, branch kept). #68 open as umbrella.
- **New-project issue:** needs an issue. Owner may open it, or I dispatch `ideate` post-PR #93 close. Recorded as pending.
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **pages.yml / billing / commit hygiene:** green; PR #93 body correctly `Refs #68`; future commits avoid literal `Closes #68`.

- Mae, the Maintainer
