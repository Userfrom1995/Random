# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (maintainer run 32411517308, owner `/oc maintainer` on PR #93; dispatched `lab` for the root-cause hollow-docs fix). **OWNER PIVOT (2026-08-20T14:52:11Z) REMAINS THE STANDING LAW.**

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted.** Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on Kodak at 9.5209 bpp) with full docs; then Test + Review + merge. Keep branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying the JPEG XL 8.71 gate, developed on its OWN issue/branch (research -> architect -> build). Never folded into PR #93.
- **ONE Obsidian PR only (being wound down):** PR #93 is the single canonical Obsidian PR. After it merges, the "one-PR" rule applies to the new project's PR.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68 on PR #93 merge.

## CRITICAL INFRASTRUCTURE STATE

- **PR #93 NOT ORPHANED (re-confirmed this run):** GitHub compare API says `status: ahead`, shared merge-base `37f0395cfc37c28b8cbe8786d504427422ad91f4` (ahead 23 / behind 0). The local empty `git merge-base` is a shallow-clone artifact. `mergeable_state: unstable` is transient for an ahead-only branch; rebase merge will be clean.
- **PR #95 MERGED:** `main` = `37f0395`. Orphan-main guard + hollow-build DETECTION (PR #95) live.
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free` (emergency-bumped at run 32405124330). `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` until a lab branch merges (both free, non-blocking). No CreditsError.
- **ROOT-CAUSE LAB (this run):** dispatched `lab` to fix `.github/agents/builder.md` resume re-task behavior - the genuine root cause of the ~10x hollow docs builds. This is agent-prompt work (lab domain), distinct from PR #93 product source the Lab Engineer previously scoped out.

## PRIORITY PROJECT (Obsidian, PR #93) - FINISH-AND-CLOSE (JXL gate lifted)

- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL + CMARC backend; R13-A muted, R13-B/R14/R15 gated OFF, all byte-identical base so never-regressive). Beats PNG (13.05) + WebP (9.61). JXL 8.71 gate LIFTED by owner pivot.
- **Test-isolation fix landed (head `e085562`):** clean parallel suite = **148 passed / 0 failed / 2 ignored** (the prior "152 pass" claims were false - shared process-global Mutex poisoning, fixed).
- **R15 halt (at `20d1162` line):** 10-axis predictor-family exhaustion proven (residual near-incompressible after R9-B); all decorrelation/learned overlays gated OFF, byte-identical base.
- **THE BLOCKER (persistent):** Step 1 docs hollow for ~10 `/oc continue`/`/oc build` dispatches. Each produced a resume-state commit, `err.txt`, or test-isolation commit - NEVER `obsidian/README.md` edit nor `obsidian/STATUS.md` creation. Verified at head `8ac10cf`: README stale ("46 lib tests, 27.82 bpp", "M1 gate still open"), STATUS.md absent.
- **ROOT CAUSE:** builder.md resume re-reads the stale progress "Current step" (final `Decision: maintainer` = pre-pivot beat-JXL escalation) and treats the task as escalated, so it writes no docs. Model bump did NOT fix it (behavioral, not capability).
- **THIS RUN:** dispatched `lab` to fix builder.md so `/oc continue`/`/oc build` re-task on the newest divergent directive (the 14:52:11Z pivot docs close-out). After it merges, re-drive `continue` for docs.

## IN FLIGHT

- **Lab (root-cause fix):** `lab` dispatched this run (head `8ac10cf`) to fix `.github/agents/builder.md`. On its merge, re-drive `continue` for README/STATUS docs.
- **PR #93 Tester:** `/oc test` after docs land - QA + real-Kodak reproducibility.
- **PR #93 Reviewer:** `/oc review` - strict read-only quality gate.
- **PR #93 merge:** rebase-merge (`--no-delete-branch`) after docs + tests + review; JXL gate lifted. Keep #68 open.

## PENDING (awaiting completion, in order)

1. Lab fixes `.github/agents/builder.md` (re-task on newest directive). Merge its PR/branch.
2. PR #93 docs (Step 1): `continue` re-driven after the lab fix; accurate README + STATUS.md, codec byte-identical at 9.5209 bpp, no stray codec commits.
3. PR #93 Tester (`/oc test`).
4. PR #93 Reviewer (`/oc review`).
5. PR #93 merge (rebase, keep branch, do NOT close #68).
6. NEW JXL project: separate codebase/new name on its own issue/branch; route research -> architect -> build. Never in PR #93. (Post-merge; I do not create its issue myself.)

## ISSUES

- **#68 (Obsidian umbrella)** - OPEN, stays open until the new JXL-class project beats codecs (per pivot + standing directive).
- **#94 (Detect silent no-op builds)** - CLOSED (PR #95 merged).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; new project seeding may use it post-PR #93 close.

## REVIEWER/TESTER/MODEL STATUS

- **Model config:** worker workflows `opencode/nemotron-3-ultra-free`. `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` until lab branch merges. `origin/main` = `37f0395`. Free fallbacks available.
- **pages.yml:** green.
- **PR #93 checks:** opencode-pr-trigger SUCCESS; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS. No Reviewer/Tester run on PR #93 yet - both required pre-merge.

## NEXT STEPS

1. Await the `lab` fix to `.github/agents/builder.md`; on its merge, verify the change re-tasks on the newest divergent directive.
2. Re-drive `continue` on PR #93 for README/STATUS docs; confirm codec unchanged at 9.5209 bpp and NO stray codec commits (pivot Step 2 canceled).
3. On docs push -> re-survey, then dispatch Tester then Reviewer.
4. Merge PR #93 (rebase, keep branch, JXL gate lifted), keep #68 open.
5. Stand up NEW JXL project on its own issue/branch; route research -> architect -> build.

## OPEN QUESTIONS

- **Will `lab` fix builder.md this time (not scope out)?** The directive is tight and explicitly agent-prompt lab work, not product source. PENDING its run.
- **Docs quality (hollow-build watch):** after the lab fix, will the Builder write REAL README/STATUS (not resume-state/err.txt)? Monitored by PR #95 hollow-build detection (auto-retry) + explicit directive + live comment thread.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, NOT orphaned).
- **Orphan-main break:** RESOLVED (shared merge-base `37f0395`).
- **mergeable_state unstable:** transient; branch ahead-only (behind:0), rebase merge clean. Re-verify at merge time.
- **Build collision:** AVOIDED (no Builder in flight at dispatch; `lab` is infra track).
- **Pivot Step 2 cancellation honored?** VERIFY on docs push - no new codec commits in PR #93; all decorrelation/learned overlays already gated off.
- **New-project issue:** needs an issue; owner may open or I dispatch `ideate` post-PR #93 close (hard rule: I do not create issues myself).
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **`workflows` permission:** opencode app lacks `Workflows` permission; direct agent workflow pushes rejected but PAT-backed step delivers. Non-blocking.

- Mae, the Maintainer
