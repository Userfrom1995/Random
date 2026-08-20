# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (maintainer run 32408288123, owner `/oc maintainer` on PR #93, re-surfaced at 19:22:08Z). **OWNER PIVOT (2026-08-20T14:52:11Z) REMAINS THE STANDING LAW.**

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted.** Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on Kodak at 9.5209 bpp) with full docs; then Test + Review + merge. Keep branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying the JPEG XL 8.71 gate, developed on its OWN issue/branch (research -> architect -> build). Never folded into PR #93.
- **ONE Obsidian PR only (being wound down):** PR #93 is the single canonical Obsidian PR. After it merges, the "one-PR" rule applies to the new project's PR.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68 on PR #93 merge.

## CRITICAL INFRASTRUCTURE STATE

- **PR #93 ORPHAN-MAIN ALARM WAS A FALSE POSITIVE (confirmed this run 32408288123):** prior runs reported `git merge-base origin/main <head>` EMPTY. This run verified via the GitHub compare API that `opencode/issue68-20260818070512` is `status: ahead` of `origin/main` (shared merge-base `37f0395`), `mergeable: MERGEABLE`. The empty local merge-base was a shallow-clone artifact. No re-link is required.
- **PR #95 MERGED:** `main` = `37f0395`. Orphan-main guard + hollow-build detection live.
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`. `opencode.json` still `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` on main until the lab updates it on its branch. `maintainer.yml` keeps `hy3-free`. All free, no CreditsError.
- **ROOT-CAUSE LAB:** the Lab Engineer scoped itself OUT of PR #93 product source (lab domain only); hollow-build DETECTION (PR #95) is the mitigation.

## PRIORITY PROJECT (Obsidian, PR #93) - FINISH-AND-CLOSE (JXL gate lifted)

- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL + CMARC backend; R13-A muted, R13-B/R14/R15 gated OFF, all byte-identical base so never-regressive). Beats PNG (13.05) + WebP (9.61). JXL gate LIFTED.
- **Test-isolation fix landed (head `e085562`):** prior "152 tests pass" were false (shared process-global Mutexes poisoned parallel `cargo test`). Clean parallel suite = **148 passed / 0 failed / 2 ignored**. R15 stays net-negative; 9.5209 bpp production unchanged.
- **R15 halt (head `20d1162`/`f1dcb4b`):** 10-axis predictor-family exhaustion proven; residual near-incompressible after R9-B. All gated OFF.
- **ONLY REMAINING BLOCKER = Step 1 docs.** `obsidian/README.md` stale (27.82 bpp / 46 tests / "M1 gate still open" from 2026-08-17); `obsidian/STATUS.md` MISSING. A `continue` is dispatched this run (head `e0855623`) with an explicit docs checklist. No re-link needed (orphan alarm false positive).

## CURRENT STATE - THIS RUN (32408288123)

- **PR #93 (head `e0855623acd25ce3a4a2776e5e68a78942cbb7b0`):** OPEN, `mergeable: MERGEABLE`, `status: ahead` of `origin/main` with shared merge-base `37f0395` (NOT orphaned). One-PR rule intact; all codec work preserved.
- **Single blocker:** stale docs (README + missing STATUS.md). Codec byte-identical at 9.5209 bpp.
- **No Builder in flight** at dispatch (no in_progress/queued opencode run on the branch). The `continue` dispatched this run is collision-safe.

## IN FLIGHT

- **PR #93 Step 1 docs:** `continue` dispatched this run (head `e0855623`). Builder must rewrite `obsidian/README.md` to accurate 9.5209 bpp / 148 tests / PNG+WebP MET / JXL gate lifted, add `obsidian/STATUS.md`, remove stray `err.txt`, and keep the codec byte-identical. On its push, a maintainer run re-surveys.
- **PR #93 Tester:** `/oc test` after docs land - QA + real-Kodak reproducibility.
- **PR #93 Reviewer:** `/oc review` - strict read-only quality gate.
- **PR #93 merge:** rebase-merge (`--no-delete-branch`) after docs + tests + review; JXL gate lifted. Keep #68 open.

## PENDING (awaiting completion, in order)

1. PR #93 docs (Step 1) - `continue` just dispatched (head `e0855623`).
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

1. PR #93 docs (Step 1): `continue` dispatched (head `e0855623`); await Builder push with accurate README + STATUS.md and NO codec changes.
2. On push -> re-survey, confirm (a) README/STATUS accurate, (b) head still `e0855623` lineage / codec unchanged at 9.5209 bpp; then dispatch Tester then Reviewer.
3. Merge PR #93 (rebase, keep branch, JXL gate lifted), keep #68 open.
4. Stand up NEW JXL project on its own issue/branch; route research -> architect -> build.

## OPEN QUESTIONS

- **Docs quality (hollow-build watch):** will the Builder write REAL docs (not just `err.txt`)? Monitored by PR #95 hollow-build detection + this run's explicit directive + the live comment thread.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN). Applies to new project's PR post-merge.
- **Orphan-main break:** RESOLVED this run (false positive; shared merge-base `37f0395` confirmed via API).
- **Build collision:** AVOIDED (no Builder in flight at dispatch; `continue` re-dispatch safe).
- **Pivot Step 2 cancellation honored?** VERIFY on docs push - no new codec commits in PR #93; all decorrelation/learned overlays already gated off.
- **Model bump success:** PENDING - verify next build/lab runs execute on `nemotron-3-ultra-free`.
- **Work preservation:** all R0-R15 codec work preserved on PR #93 (branch kept). #68 open as umbrella.
- **New-project issue:** needs an issue; owner may open or I dispatch `ideate` post-PR #93 close (hard rule: I do not create issues myself).
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **`workflows` permission:** opencode app lacks `Workflows` permission; direct agent workflow pushes rejected but PAT-backed step delivers. Non-blocking.

- Mae, the Maintainer
