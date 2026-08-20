# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (maintainer run 32407789566, owner `/oc maintainer` on PR #93). **OWNER PIVOT (2026-08-20T14:52:11Z) REMAINS THE STANDING LAW.**

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted.** Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on Kodak, 9.5209 bpp) with full docs; then Test + Review + merge. Keep branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying the JPEG XL 8.71 gate, developed on its OWN issue/branch (research -> architect -> build). Never folded into PR #93.
- **ONE Obsidian PR only (being wound down):** PR #93 is the single canonical Obsidian PR. After it merges, the "one-PR" rule applies to the new project's PR.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68 on PR #93 merge.

## CRITICAL INFRASTRUCTURE STATE

- **PR #93 ORPHAN-MAIN RE-OPENED THIS RUN (32407789566):** `git merge-base origin/main e0855623` = EMPTY. The re-link attempt in run 32407393606 rebased locally but its `git push --force-with-lease` was REJECTED on the remote (opencode app lacks force-push permission), so the remote branch is still the orphan-rooted history (root `bbaf952`, no parent in `origin/main` = `37f0395`). The re-link is being delegated to the Builder via `continue` (the Builder can push to its own branch), which is the compliant path given Mae may not push.
- **PR #95 MERGED:** `main` = `37f0395`. Orphan-main guard + hollow-build detection (PR #94) live.
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`. `opencode.json` still `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` on main until the lab updates it on its branch. `maintainer.yml` keeps `hy3-free`. All free, no CreditsError.
- **ROOT-CAUSE LAB:** the Lab Engineer scoped itself OUT of PR #93 product source (lab domain only); hollow-build DETECTION (PR #95) is the mitigation.

## PRIORITY PROJECT (Obsidian, PR #93) - FINISH-AND-CLOSE (JXL gate lifted)

- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL + CMARC backend; R13-A muted, R13-B/R14/R15 gated OFF, all byte-identical base so never-regressive). Beats PNG (13.05) + WebP (9.61). JXL gate LIFTED.
- **Test-isolation fix landed (head `e085562`):** prior "152 tests pass" were false (shared process-global Mutexes poisoned parallel `cargo test`). Clean parallel suite = **148 passed / 0 failed / 2 ignored**. R15 stays net-negative; 9.5209 bpp production unchanged.
- **R15 halt (head `20d1162`/`f1dcb4b`):** 10-axis predictor-family exhaustion proven; residual near-incompressible after R9-B. All gated OFF.
- **Step 1 (full docs) STILL INCOMPLETE:** `obsidian/README.md` stale (27.82 bpp / 46 tests / "M1 gate still open" from 2026-08-17); `obsidian/STATUS.md` MISSING. A `continue` is dispatched this run (head `e0855623`) with an explicit re-link + docs checklist.

## CURRENT STATE - THIS RUN (32407789566)

- **PR #93 (head `e0855623`):** OPEN, `mergeable: clean`, but ORPHANED from `origin/main` (merge-base EMPTY). One-PR rule intact; all codec work preserved.
- **Two blockers:** (1) orphan-main recurrence (remote force-push rejected in 32407393606); (2) docs incomplete. Both addressed by the dispatched `continue`.
- **No Builder in flight** at dispatch (last builder run 32407676618 completed 19:16:27Z); the `continue` is collision-safe.

## IN FLIGHT

- **PR #93 re-link + Step 1 docs:** `continue` dispatched this run (head `e0855623`). Builder must (a) re-link the branch onto `origin/main` (force-push `opencode/issue68-20260818070512`, prefer `origin/main` for `.github/workflows/*`), confirming non-empty merge-base, then (b) write accurate README + STATUS.md, keep codec byte-identical at 9.5209 bpp, remove stray `err.txt`, and push. On its push, a maintainer run re-surveys.
- **PR #93 Tester:** `/oc test` after re-link + docs land - QA + real-Kodak reproducibility.
- **PR #93 Reviewer:** `/oc review` - strict read-only quality gate.
- **PR #93 merge:** rebase-merge (`--no-delete-branch`) after re-link + docs + tests + review; JXL gate lifted. Keep #68 open.

## PENDING (awaiting completion, in order)

1. PR #93 re-link (Builder, this run's `continue`).
2. PR #93 docs (Step 1) - `continue` just dispatched (head `e0855623`).
3. PR #93 Tester (`/oc test`).
4. PR #93 Reviewer (`/oc review`).
5. PR #93 merge (rebase, keep branch, do NOT close #68).
6. NEW JXL project: separate codebase/new name on its own issue/branch; route research -> architect -> build. Never in PR #93. (Post-merge; I will not create its issue myself.)

## ISSUES

- **#68 (Obsidian umbrella)** - OPEN, stays open until the new JXL-class project beats codecs (per pivot + standing directive).
- **#94 (Detect silent no-op builds)** - CLOSED (PR #95 merged).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; new project seeding may use it post-PR #93 close.

## REVIEWER/TESTER/MODEL STATUS

- **Model config:** worker workflows `opencode/nemotron-3-ultra-free`. `opencode.json` still `hy3-free`/`mimo-v2.5-free` on main until lab branch merges. `origin/main` = `37f0395`. Free-model fallbacks available (deepseek-v4-flash-free / nemotron-3.5-lightning-free / laguna-s-2.1-free).
- **pages.yml:** green.
- **PR #93 checks:** opencode-pr-trigger SUCCESS; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS.
- **PR #95 checks:** merged; Reviewer + Tester approved; issue #94 closed.

## NEXT STEPS

1. PR #93 re-link + docs: `continue` dispatched (head `e0855623`/`e085562` lineage); await Builder push with non-empty merge-base + real docs.
2. On push -> re-survey, confirm (a) merge-base non-empty, (b) no stray codec commits (pivot Step 2 canceled); then dispatch Tester then Reviewer.
3. Merge PR #93 (rebase, keep branch, JXL gate lifted), keep #68 open.
4. Stand up NEW JXL project on its own issue/branch; route research -> architect -> build.

## OPEN QUESTIONS

- **Orphan-main recurrence:** delegated to Builder `continue` (Mae cannot force-push; remote rejects). Will the Builder's re-link land with a non-empty merge-base? Pending its push.
- **Hollow-build recurrence:** monitored by PR #95 detection + this run's explicit directive + live comment thread. Will the Builder write real docs this time?
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN). Applies to new project's PR post-merge.
- **Orphan-main break:** RE-OPENED this run (remote push rejected); delegated re-link via Builder.
- **Build collision:** AVOIDED (no Builder in flight at dispatch).
- **Pivot Step 2 cancellation honored?** VERIFY on docs push - no new codec commits in PR #93; all decorrelation/learned overlays already gated off.
- **Model bump success:** PENDING - verify next build/lab runs execute on `nemotron-3-ultra-free`.
- **Work preservation:** all R0-R15 codec work preserved on PR #93 (branch kept). #68 open as umbrella.
- **New-project issue:** needs an issue; owner may open or I dispatch `ideate` post-PR #93 close (hard rule: I do not create issues myself).
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **`workflows` permission:** opencode app lacks `Workflows` permission; direct agent workflow pushes rejected but PAT-backed step delivers. Non-blocking.

- Mae, the Maintainer
