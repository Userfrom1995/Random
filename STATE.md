# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (maintainer run 32405983221, owner `/oc maintainer` on PR #93). **OWNER PIVOT (2026-08-20T14:52:11Z) REMAINS THE STANDING LAW.**

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted.** Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on Kodak) with full docs; then Test + Review + merge. Keep branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying the JPEG XL 8.71 gate, developed on its OWN issue/branch (research -> architect -> build). Never folded into PR #93.
- **ONE Obsidian PR only (being wound down):** PR #93 is the single canonical Obsidian PR. After it merges, the "one-PR" rule applies to the new project's PR.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68 on PR #93 merge.

## CRITICAL INFRASTRUCTURE STATE

- **PR #95 MERGED (run 32393955210):** `main` = `37f0395cfc37c28b8cbe8786d504427422ad91f4`. Branch `opencode/lab-94-no-op-build-detection` kept. Orphan-main guard verified clean. Issue #94 closed. Hollow-build DETECTION is live (PR #93's `0d1b4d8c5f` hollow err.txt commit is exactly what it must catch + auto-retry).
- **MODEL PINS:** worker workflows bumped `opencode/hy3-free` -> `opencode/nemotron-3-ultra-free` earlier this day. `opencode.json` still `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free, no CreditsError) on main until the lab updates it on its branch. `maintainer.yml` keeps `hy3-free`.
- **ROOT-CAUSE LAB (run 32394291588/32405544444):** the Lab Engineer scoped itself OUT of PR #93 product source (lab domain only). So builder.md resume re-task was NOT changed for PR #93; mitigated by the unambiguous docs directive + hollow-build auto-retry.

## PRIORITY PROJECT (Obsidian, PR #93) - FINISH-AND-CLOSE (JXL gate lifted)

- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL, CMARC backend; R13-A muted, R13-B/R14/R15 gated OFF, all byte-identical to base so never-regressive). Beats PNG (13.05) + WebP (9.61). JXL gate LIFTED for this project. 148+ lib tests pass green.
- **R15 halt (branch `20d1162`/`f1dcb4b`):** 10-axis predictor-family exhaustion proven; residual near-incompressible after R9-B. All gated OFF. No further codec tuning warranted.

## CURRENT STATE - THIS RUN (32405983221)

- **PR #93 (head `0d1b4d8c5f`):** owner pivot active. **Step 1 (full docs) INCOMPLETE** - last Builder push `0d1b4d8c5f` (18:56:35Z) only added `err.txt` (hollow); `obsidian/README.md` still stale ("46 lib tests, 27.82 bpp"). No Builder currently in flight.
- **Dispatched THIS run:** `build` on PR #93 with an explicit docs checklist (remove err.txt; accurate README + STATUS.md; no new codec features). Targets commit `0d1b4d8c5f`.

## IN FLIGHT

- **PR #93 docs (Step 1):** `build` dispatched this run (head `0d1b4d8c5f`). Builder must write full Obsidian docs (README + STATUS.md), remove stray `err.txt`, keep codec byte-identical at 9.5209 bpp. On its push (head advances), a maintainer run re-surveys, confirms docs COMPLETE + no stray codec commits, then dispatches Tester.
- **PR #93 Tester:** `/oc test` after docs land - QA + real-Kodak reproducibility.
- **PR #93 Reviewer:** `/oc review` - strict read-only quality gate.
- **PR #93 merge:** rebase-merge (`--no-delete-branch`) after docs+tests+review; JXL gate lifted. Keep #68 open.

## PENDING (awaiting completion, in order)

1. PR #93 docs (Step 1) - `build` just dispatched (head `0d1b4d8c5f`).
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

- **Model config:** worker workflows `opencode/nemotron-3-ultra-free` (bumped earlier). `opencode.json` still `hy3-free`/`mimo-v2.5-free` on main until lab branch merges. `origin/main` = `37f0395`. Free-model fallbacks available (deepseek-v4-flash-free / nemotron-3.5-lightning-free / laguna-s-2.1-free).
- **pages.yml:** green (post PR #95 merge).
- **PR #93 checks:** opencode-pr-trigger SUCCESS; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS.
- **PR #95 checks:** merged; Reviewer + Tester approved; issue #94 closed.

## NEXT STEPS

1. PR #93 docs: `build` dispatched; await Builder push (head advances past `0d1b4d8c5f`) with real docs, NOT err.txt.
2. On docs push -> re-survey, confirm no stray codec commits, dispatch Tester then Reviewer.
3. Merge PR #93 (rebase, keep branch, JXL gate lifted), keep #68 open.
4. Stand up NEW JXL project on its own issue/branch; route research -> architect -> build.

## OPEN QUESTIONS

- **Hollow-build recurrence:** `0d1b4d8c5f` was a hollow docs commit (err.txt only). Will this `build` dispatch produce real docs? PR #95 detection + my re-dispatch cover it.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN). Applies to new project's PR post-merge.
- **Orphan-main break:** NOT present - PR #93 `mergeable: clean`; common ancestor `d6b2894` non-empty.
- **Build collision:** AVOIDED this run (no Builder in flight on the branch).
- **Pivot Step 2 cancellation honored?** VERIFY on docs push - no new codec commits in PR #93; all decorrelation/learned overlays already gated off.
- **Model bump success:** PENDING - verify next build/lab runs execute on `nemotron-3-ultra-free` (watch rate limits / CreditsError).
- **Work preservation:** all R0-R15 codec work preserved on PR #93 (branch kept). #68 open as umbrella.
- **New-project issue:** needs an issue; owner may open or I dispatch `ideate` post-PR #93 merge (hard rule: I do not create issues myself).
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **`workflows` permission:** opencode app lacks `Workflows` permission; direct agent workflow pushes rejected but PAT-backed step delivers. Non-blocking.

- Mae, the Maintainer