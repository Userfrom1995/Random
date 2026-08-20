# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (maintainer run 32413203865, owner `/oc maintainer` on PR #97; PR #97 in Tester gate, builder.md lab dispatched for PR #93). **OWNER PIVOT (2026-08-20T14:52:11Z) REMAINS THE STANDING LAW.**

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted.** Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on Kodak at 9.5209 bpp) with full docs; then Test + Review + merge. Keep branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying the JPEG XL 8.71 gate, developed on its OWN issue/branch (research -> architect -> build). Never folded into PR #93.
- **ONE Obsidian PR only (being wound down):** PR #93 is the single canonical Obsidian PR. After it merges, the "one-PR" rule applies to the new project's PR.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68 on PR #93 merge.

## CRITICAL INFRASTRUCTURE STATE

- **PR #97 (circuit breaker for #96):** head `4bb240ef`, MERGEABLE. Adds `.github/scripts/loop-budget.sh` + wires `Circuit breaker budget check` (gated before the three Forward steps) into `opencode.yml`. Reviewer `/oc approve` (run 32413189428) confirms F1/F2/F3 fixed. Tester IN PROGRESS (run 32413281282). Awaiting `/oc approve-test` -> rebase-merge (keep branch, close #96).
- **`workflows` permission wall (KNOWN, NON-BLOCKING):** the opencode App cannot push `*.github/workflows/*.yml` on a second push (rejected "without workflows permission"). A redundant `/oc lab` re-trigger (run 32413067085) hit this but was harmless because the fixes were already on the branch. PAT-backed `gh pr merge` merges via API and is unaffected, so the opencode.yml change in PR #97 will land on `main` on merge.
- **`main` = `37f0395`** (`lab: guard diagnose step against false-positive on auto-retry (Fixes #94)`).
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`. `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` (both free, non-blocking).

## PRIORITY PROJECT (Obsidian, PR #93) - FINISH-AND-CLOSE (JXL gate lifted)

- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL + CMARC backend; R13-A muted, R13-B/R14/R15 gated OFF, all byte-identical base so never-regressive). Beats PNG (13.05) + WebP (9.61). JXL 8.71 gate LIFTED by owner pivot.
- **Test-isolation fix landed:** clean parallel suite = **148 passed / 0 failed / 2 ignored**.
- **R15 halt:** 10-axis predictor-family exhaustion proven; all decorrelation/learned overlays gated OFF, byte-identical base.
- **THE BLOCKER (persistent, ROOT CAUSE NOW BEING FIXED):** `obsidian/README.md` STALE ("46 lib tests, 27.82 bpp", "M1 gate still open"), `obsidian/STATUS.md` ABSENT. Root cause = `.github/agents/builder.md` resume logic re-reads stale `progress/68-*.md` "Current step" and hollows docs. A `lab` run for THIS fix was dispatched this maintainer run (target PR #93, head `3a909105`). PR #97 (circuit breaker) did NOT include this builder.md fix.

## IN FLIGHT

- **PR #97 Tester:** `opencode-test.yml` run `32413281282` IN PROGRESS (owner `/oc test` 20:17:20Z). Awaiting `/oc approve-test`.
- **PR #97 merge:** rebase-merge (`--no-delete-branch`) after `/oc zip`/approve-test; closes #96. Keep #68 open.
- **builder.md root-cause fix (NEW this run):** `lab` dispatched on PR #93 (head `3a909105`) to fix `.github/agents/builder.md` resume re-task on the 2026-08-20T14:52:11Z pivot. On its merge -> re-drive `continue`/`build` for README/STATUS docs on PR #93.
- **PR #93 docs (Step 1):** after builder.md fix merges - re-drive `continue`/`build` for accurate README + STATUS.md; codec byte-identical at 9.5209 bpp, no stray codec commits.
- **PR #93 Tester / Reviewer / merge:** after docs land, then `/oc test` -> `/oc review` -> rebase-merge (keep branch, JXL gate lifted), keep #68 open.

## PENDING (awaiting completion, in order)

1. PR #97: Tester approve -> rebase-merge (keep branch), close #96.
2. builder.md fix (lab, PR #93 target) -> merge its PR/branch.
3. PR #93 docs (Step 1): `continue`/`build` re-driven after the lab fix; accurate README + STATUS.md.
4. PR #93 Tester (`/oc test`).
5. PR #93 Reviewer (`/oc review`).
6. PR #93 merge (rebase, keep branch, JXL gate lifted), keep #68 open.
7. NEW JXL project: separate codebase/new name on its own issue/branch; route research -> architect -> build. Never in PR #93.

## ISSUES

- **#68 (Obsidian umbrella)** - OPEN, stays open until the new JXL-class project beats codecs (per pivot + standing directive).
- **#96 (Circuit breaker)** - OPEN; fixed by PR #97 (awaiting test + merge).
- **#94 (Detect silent no-op builds)** - CLOSED (PR #95 merged; `37f0395` guards diagnostic).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; new project seeding may use it post-PR #93 close.

## REVIEWER/TESTER/MODEL STATUS

- **Model config:** worker workflows `opencode/nemotron-3-ultra-free`. `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` until lab branch merges. `origin/main` = `37f0395`. Free fallbacks available.
- **pages.yml:** green.
- **PR #97 checks:** opencode-pr-trigger SUCCESS; pages deploy SUCCESS; GitGuardian SUCCESS; Reviewer `/oc approve`; Tester IN PROGRESS (run 32413281282).
- **PR #93 checks:** no Reviewer/Tester run yet - both required after docs land.

## NEXT STEPS

1. AWAIT `/oc approve-test` on PR #97 (run 32413281282) -> rebase-merge PR #97 (keep branch), close #96.
2. AWAIT builder.md lab fix (dispatched this run) -> merge -> re-drive `/oc continue` on PR #93 for README/STATUS docs; confirm codec unchanged at 9.5209 bpp and NO stray codec commits.
3. On docs push -> re-survey, then dispatch Tester then Reviewer on PR #93.
4. Merge PR #93 (rebase, keep branch, JXL gate lifted), keep #68 open.
5. Stand up NEW JXL project on its own issue/branch; route research -> architect -> build.

## OPEN QUESTIONS

- **Will Tester approve PR #97?** PENDING run 32413281282.
- **builder.md lab (dispatched this run):** will it patch ONLY `.github/agents/builder.md` (not opencode.yml, not Obsidian source) and re-task on the pivot? PENDING its run.
- **PR #97 workflows-permission wall on merge:** NON-BLOCKING (`gh pr merge` is API-based). Verify `main` history stays non-orphan after merge.
- **Docs quality (hollow-build watch):** after the lab fix, will the Builder write REAL README/STATUS? Monitored by the restored opencode.yml no-op diagnostic + explicit directive + live thread.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, NOT orphaned; MERGEABLE at `3a909105`).
- **Orphan-main break:** RESOLVED (shared merge-base with `main`).
- **Pivot Step 2 cancellation honored?** VERIFY on docs push - no new codec commits in PR #93; all decorrelation/learned overlays already gated off.
- **New-project issue:** needs an issue; owner may open or I dispatch `ideate` post-PR #93 close (hard rule: I do not create issues myself).
- **Review/Tester on PR #93:** neither has run yet; both required pre-merge.

- Mae, the Maintainer
