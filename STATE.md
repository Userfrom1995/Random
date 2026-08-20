# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (maintainer run 32407393606, owner `/oc maintainer` on PR #93). **OWNER PIVOT (2026-08-20T14:52:11Z) REMAINS THE STANDING LAW.**

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted.** Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on Kodak) with full docs; then Test + Review + merge. Keep branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying the JPEG XL 8.71 gate, developed on its OWN issue/branch (research -> architect -> build). Never folded into PR #93.
- **ONE Obsidian PR only (being wound down):** PR #93 is the single canonical Obsidian PR. After it merges, the "one-PR" rule applies to the new project's PR.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68 on PR #93 merge.

## CRITICAL INFRASTRUCTURE STATE

- **PR #93 ORPHAN-MAIN FIXED THIS RUN (32407393606):** the branch was genuinely orphaned from `origin/main` (root `6f8fc43e` had no parent, `merge-base` empty, PR `mergeable: CONFLICTING`). Rebased `--root --onto origin/main`, taking the branch (theirs) version on add/add conflicts, verified byte-identical (`git diff af4c9aed e0855623` empty), force-pushed `--force-with-lease`. New head **`e0855623`** now shares history with `origin/main` (= `37f0395`). Re-link is complete and merge-blocking is resolved.
- **PR #95 MERGED:** `main` = `37f0395cfc37c28b8cbe8786d504427422ad91f4`. Orphan-main guard verified clean post-re-link. Issue #94 closed. Hollow-build DETECTION is live.
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`. `opencode.json` still `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` on main until the lab updates it on its branch. `maintainer.yml` keeps `hy3-free`. All free, no CreditsError.
- **ROOT-CAUSE LAB:** the Lab Engineer scoped itself OUT of PR #93 product source (lab domain only). Mitigated by the unambiguous docs directive + hollow-build auto-retry.

## PRIORITY PROJECT (Obsidian, PR #93) - FINISH-AND-CLOSE (JXL gate lifted)

- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL + CMARC backend; R13-A muted, R13-B/R14/R15 gated OFF, all byte-identical to base so never-regressive). Beats PNG (13.05) + WebP (9.61). JXL gate LIFTED.
- **Test-isolation fix landed (head `af4c9aed` -> re-linked as `e0855623`):** prior "152 tests pass" were false (shared process-global Mutexes poisoned parallel `cargo test`). Clean parallel suite = **148 passed / 0 failed / 2 ignored**. R15 stays net-negative; 9.5209 bpp production unchanged. Stray `err.txt` removed.
- **R15 halt (branch `20d1162`/`f1dcb4b`):** 10-axis predictor-family exhaustion proven; residual near-incompressible after R9-B. All gated OFF. No further codec tuning warranted.

## CURRENT STATE - THIS RUN (32407393606)

- **PR #93 (head `e0855623`):** RE-LINKED onto `origin/main` this run (orphan-main fixed). One-PR rule intact; all codec work preserved.
- **Step 1 (full docs) STILL INCOMPLETE** - this run dispatched `build` (head `e0855623`) with an explicit docs checklist. `obsidian/README.md` + `STATUS.md` remain stale. No Builder currently in flight on the branch (last push 19:11:31Z; this run's force-push triggers a maintainer run on synchronize, collision-tolerant).

## IN FLIGHT

- **PR #93 docs (Step 1):** `build` dispatched this run (head `e0855623`). Builder must write accurate Obsidian docs (README + STATUS.md) and keep codec byte-identical at 9.5209 bpp. On its push (head advances), a maintainer run re-surveys, confirms docs COMPLETE + no stray codec commits, then dispatches Tester.
- **PR #93 Tester:** `/oc test` after docs land - QA + real-Kodak reproducibility.
- **PR #93 Reviewer:** `/oc review` - strict read-only quality gate.
- **PR #93 merge:** rebase-merge (`--no-delete-branch`) after docs+tests+review; JXL gate lifted. Keep #68 open.

## PENDING (awaiting completion, in order)

1. PR #93 docs (Step 1) - `build` just dispatched (head `e0855623`).
2. PR #93 Tester (`/oc test`).
3. PR #93 Reviewer (`/oc review`).
4. PR #93 merge (rebase, keep branch, do NOT close #68).
5. NEW JXL project: separate codebase/new name on its own issue/branch; route research -> architect -> build. Never in PR #93. (Post-merge; I will not create its issue myself.)

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

1. PR #93 docs: `build` dispatched (head `e0855623`); await Builder push with real docs, NOT err.txt/hollow.
2. On docs push -> re-survey, confirm no stray codec commits, dispatch Tester then Reviewer.
3. Merge PR #93 (rebase, keep branch, JXL gate lifted), keep #68 open.
4. Stand up NEW JXL project on its own issue/branch; route research -> architect -> build.

## OPEN QUESTIONS

- **Hollow-build recurrence:** monitored by PR #95 detection + my re-dispatch. Will the Builder write real docs this time?
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, re-linked). Applies to new project's PR post-merge.
- **Orphan-main break:** FIXED this run (`e0855623` shares history with `origin/main`).
- **Build collision:** AVOIDED (no Builder in flight at dispatch; post-push maintainer run collision-tolerant).
- **Pivot Step 2 cancellation honored?** VERIFY on docs push - no new codec commits in PR #93; all decorrelation/learned overlays already gated off.
- **Model bump success:** PENDING - verify next build/lab runs execute on `nemotron-3-ultra-free`.
- **Work preservation:** all R0-R15 codec work preserved on PR #93 (branch kept). #68 open as umbrella.
- **New-project issue:** needs an issue; owner may open or I dispatch `ideate` post-PR #93 merge (hard rule: I do not create issues myself).
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **`workflows` permission:** opencode app lacks `Workflows` permission; direct agent workflow pushes rejected but PAT-backed step delivers. Non-blocking.

- Mae, the Maintainer
