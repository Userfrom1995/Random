# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (maintainer run 32412424505, owner `/oc maintainer` on PR #93; HOLD - Lab Engineer run in flight to fix `.github/agents/builder.md` docs root cause). **OWNER PIVOT (2026-08-20T14:52:11Z) REMAINS THE STANDING LAW.**

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted.** Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on Kodak at 9.5209 bpp) with full docs; then Test + Review + merge. Keep branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying the JPEG XL 8.71 gate, developed on its OWN issue/branch (research -> architect -> build). Never folded into PR #93.
- **ONE Obsidian PR only (being wound down):** PR #93 is the single canonical Obsidian PR. After it merges, the "one-PR" rule applies to the new project's PR.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68 on PR #93 merge.

## CRITICAL INFRASTRUCTURE STATE

- **PR #93 NOT ORPHANED:** GitHub compare `ahead`/`behind 0`, shared merge-base `37f0395`. `mergeable: MERGEABLE`. Head `3a909105` at this survey.
- **`main` = `37f0395`** (`lab: guard diagnose step against false-positive on auto-retry (Fixes #94)`). The orphan-recovery commit `bbaf952` had deleted the diagnostic from `opencode.yml`; restored by PR #95 at `37f0395`.
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`. `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` (both free, non-blocking).
- **DOCS ROOT CAUSE (in flight):** `.github/agents/builder.md` resume/BUILD logic re-reads the stale `progress/68-*.md` "Current step" (final `Decision: maintainer` = pre-pivot beat-JXL escalation) and hollows Step-1 docs ~10x (never edits README/STATUS). A Lab Engineer run (32412403666, owner `/oc lab` 20:07:44Z) is IN FLIGHT to fix `builder.md` and add the circuit-breaker the Lab Engineer escalated. PRIOR `lab` (32411944594) only restored `opencode.yml`, missing this.

## PRIORITY PROJECT (Obsidian, PR #93) - FINISH-AND-CLOSE (JXL gate lifted)

- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL + CMARC backend; R13-A muted, R13-B/R14/R15 gated OFF, all byte-identical base so never-regressive). Beats PNG (13.05) + WebP (9.61). JXL 8.71 gate LIFTED by owner pivot.
- **Test-isolation fix landed:** clean parallel suite = **148 passed / 0 failed / 2 ignored** (earlier "152 pass" claims were false positives from shared process-global Mutex poisoning, since fixed).
- **R15 halt:** 10-axis predictor-family exhaustion proven (residual near-incompressible after R9-B); all decorrelation/learned overlays gated OFF, byte-identical base.
- **THE BLOCKER (persistent):** `obsidian/README.md` STALE ("46 lib tests, 27.82 bpp", "M1 gate still open"), `obsidian/STATUS.md` ABSENT. Verified at head `3a909105`.

## IN FLIGHT

- **Lab (builder.md fix, run 32412403666):** IN FLIGHT (owner `/oc lab` 20:07:44Z). Fixes `.github/agents/builder.md` so `/oc continue`/`/oc build` re-task on the 2026-08-20T14:52:11Z pivot directive (finish-and-close docs) instead of the stale `Decision: maintainer` progress line; adds the circuit-breaker so a documented halt trigger escalates to owner instead of looping. NO Builder/continue dispatched this run to avoid colliding with the buggy prompt.
- **PR #93 docs (Step 1):** AFTER the lab fix merges - re-drive `continue`/`build` for accurate README + STATUS.md; codec byte-identical at 9.5209 bpp, no stray codec commits.
- **PR #93 Tester:** `/oc test` after docs land - QA + real-Kodak reproducibility.
- **PR #93 Reviewer:** `/oc review` - strict read-only quality gate.
- **PR #93 merge:** rebase-merge (`--no-delete-branch`) after docs + tests + review; JXL gate lifted. Keep #68 open.

## PENDING (awaiting completion, in order)

1. Lab fixes `.github/agents/builder.md` (re-task on newest divergent directive) + circuit-breaker. Merge its PR/branch.
2. PR #93 docs (Step 1): `continue`/`build` re-driven after the lab fix; accurate README + STATUS.md.
3. PR #93 Tester (`/oc test`).
4. PR #93 Reviewer (`/oc review`).
5. PR #93 merge (rebase, keep branch, JXL gate lifted), keep #68 open.
6. NEW JXL project: separate codebase/new name on its own issue/branch; route research -> architect -> build. Never in PR #93.

## ISSUES

- **#68 (Obsidian umbrella)** - OPEN, stays open until the new JXL-class project beats codecs (per pivot + standing directive).
- **#94 (Detect silent no-op builds)** - CLOSED (PR #95 merged; `37f0395` guards diagnostic).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; new project seeding may use it post-PR #93 close.

## REVIEWER/TESTER/MODEL STATUS

- **Model config:** worker workflows `opencode/nemotron-3-ultra-free`. `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` until lab branch merges. `origin/main` = `37f0395`. Free fallbacks available.
- **pages.yml:** green.
- **PR #93 checks:** opencode-pr-trigger SUCCESS; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS. No Reviewer/Tester run on PR #93 yet - both required pre-merge.

## NEXT STEPS

1. AWAIT the in-flight Lab run (32412403666) to merge the `builder.md` fix. On its merge a maintainer run auto-triggers.
2. Re-drive `continue`/`build` on PR #93 for README/STATUS docs; confirm codec unchanged at 9.5209 bpp and NO stray codec commits (pivot Step 2 canceled).
3. On docs push -> re-survey, then dispatch Tester then Reviewer.
4. Merge PR #93 (rebase, keep branch, JXL gate lifted), keep #68 open.
5. Stand up NEW JXL project on its own issue/branch; route research -> architect -> build.

## OPEN QUESTIONS

- **Will THIS lab run (32412403666) actually patch `.github/agents/builder.md` (not just opencode.yml)?** PENDING its run (prior 32411944594 sidetracked).
- **Docs quality (hollow-build watch):** after the lab fix, will the Builder write REAL README/STATUS? Monitored by the restored opencode.yml no-op diagnostic + explicit directive + live thread.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, NOT orphaned).
- **Orphan-main break:** RESOLVED (shared merge-base `37f0395`).
- **mergeable_state:** MERGEABLE (ahead/behind 0) at survey; rebase merge clean.
- **Build collision:** AVOIDED this run (no Builder dispatched; lab in flight is infra track).
- **Pivot Step 2 cancellation honored?** VERIFY on docs push - no new codec commits in PR #93; all decorrelation/learned overlays already gated off.
- **New-project issue:** needs an issue; owner may open or I dispatch `ideate` post-PR #93 close (hard rule: I do not create issues myself).
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **`workflows` permission:** opencode app lacks `Workflows` permission; direct agent workflow pushes rejected but PAT-backed step delivers. Non-blocking.

- Mae, the Maintainer
