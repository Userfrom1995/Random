# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (maintainer run 32405124330, scheduled; lab hollow'd, emergency model bump + re-dispatch lab). **OWNER PIVOT (2026-08-20T14:52:11Z) REMAINS THE STANDING LAW.**

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted.** Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on Kodak) with full docs; then Test + Review + merge. Keep branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying the JPEG XL 8.71 gate, developed on its OWN issue/branch (research -> architect -> build). Never folded into PR #93.
- **ONE Obsidian PR only (now being wound down):** PR #93 is the single canonical Obsidian PR. After it merges, the "one-PR" rule applies to the new project's PR.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68 on PR #93 merge.

## CRITICAL INFRASTRUCTURE STATE

- **PR #95 MERGED (run 32393955210):** `main` = `37f0395cfc37c28b8cbe8786d504427422ad91f4`. Branch `opencode/lab-94-no-op-build-detection` kept. Orphan-main guard verified clean. Issue #94 closed.
- **MODEL BUMP (this run 32405124330, EMERGENCY):** all worker workflow `model:` pins bumped `opencode/hy3-free` -> `opencode/nemotron-3-ultra-free` in `opencode.yml`, `opencode-review.yml`, `opencode-test.yml`, `auditor.yml`, `lab.yml`, `ideate.yml`. `maintainer.yml` kept at `hy3-free`. The PAT-backed step (maintainer.yml:149) commits/pushes to `main` before the `/oc lab` trigger posts, so the re-dispatched lab runs on the strong model. `opencode.json` still `hy3-free`/`mimo-v2.5-free` until the lab updates it on its branch.
- **WHY:** the root-cause `lab` (run 32394291588) hollow'd - the Lab Engineer on `hy3-free` produced no decision file and changed nothing. With the model now strong, the re-dispatched lab can complete the fix.

## HOLLOW-BUILD ROOT CAUSE - STILL OPEN, LAB RE-DISPATCHED ON STRONG MODEL

- **HOLLOW-BUILD CONFIRMED:** PR #93 docs Builder no-op'd twice (runs 32382581730 @14:50:48Z and 32391993368 @16:26:25Z), both `completed` green but pushed NOTHING (head still `20d1162`, no docs commit). The dispatched root-cause `lab` (run 32394291588) then ALSO hollow'd (no decision file) because it ran on the same weak model.
- **FIX IN FLIGHT (re-dispatched this run):** `lab` on issue #93, now on `nemotron-3-ultra-free`, to (1) repair `builder.md` so `/oc continue` re-tasks on the newest divergent owner/maintainer directive (the 14:52:11Z pivot), (2) update `opencode.json` model+small_model to free models, (3) confirm the `opencode.yml` pin. Own PR/branch (`opencode/lab-93-...`).

## PRIORITY PROJECT (Obsidian, PR #93) - FINISH-AND-CLOSE (BLOCKED on root-cause lab fix)

- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL, CMARC backend; R13-A muted, R13-B/R14/R15 gated off). Beats PNG (13.05) + WebP (9.61). JXL gate LIFTED for this project. 152 lib tests pass (per earlier runs; re-verify on merge).

## CURRENT STATE - THIS RUN (32405124330)

- **Worker model pins:** bumped to `opencode/nemotron-3-ultra-free` (6 workflow files); commit/push pending the PAT step. `opencode.json` still old until lab updates it.
- **PR #93 (Obsidian, head `20d1162`):** in flight; docs BLOCKED by hollow-build root cause. Emergency model bump done; root-cause `lab` RE-DISPATCHED this run (now on strong model).
- **PR #95 (lab infra):** MERGED (main `37f0395`). Issue #94 closed.

## IN FLIGHT

- **PR #93 root-cause lab fix (builder.md resume re-task + opencode.json model):** RE-DISPATCHED THIS run (`lab`, target #93) on `nemotron-3-ultra-free`. On its own PR/branch, sequenced after the merged #95.
- **PR #93 docs (Step 1):** PENDING the root-cause `lab` fix. After it lands, re-drive `continue`; Builder writes full Obsidian docs (CLI usage, all flags/options/features, shipped R10-B+CMARC path, gated R13/R14/R15 with honest measurements) and PUSHES (head advances past 20d1162). Required before merge. Step 2 (new codec IN PR #93) is CANCELED by the pivot.

## PENDING (awaiting completion, in order)

- **PR #93 root-cause `lab` (re-dispatched):** fix `builder.md` `/oc continue` re-task on divergent newer directive + update `opencode.json` model/small_model. Own PR/branch.
- **PR #93 docs (Step 1):** after the root-cause `lab` fix lands, re-drive `continue`; Builder writes full Obsidian docs and pushes. On its push, a maintainer run re-surveys, confirms docs COMPLETE and no new-codec work in PR #93, then dispatches Tester.
- **PR #93 Tester:** run `/oc test` on PR #93 after docs land - QA + real-Kodak reproducibility.
- **PR #93 Reviewer:** run `/oc review` - strict read-only quality gate.
- **PR #93 merge:** rebase-merge (`--no-delete-branch`) once docs + tests + review done. JXL gate lifted. Keep branch. Do NOT close #68.
- **NEW project (JXL gate):** after PR #93 merges, stand up a separate codebase with a new name on its own issue/branch. Seed via `ideate` or owner-opened issue; then route research -> architect -> build. Never in PR #93.

## ISSUES

- **#68 (Obsidian umbrella)** - OPEN, stays open until the new JXL-class project beats codecs (per pivot + standing directive).
- **#94 (Detect silent no-op builds)** - CLOSED (implemented by merged PR #95).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; new project seeding may use it post-PR #93 close.

## REVIEWER/TESTER/MODEL STATUS

- **Model config:** worker workflows now `opencode/nemotron-3-ultra-free` (bumped this run). `opencode.json` still `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free; no `CreditsError`) until the lab updates it. `origin/main` = `37f0395`. STRONGER free models confirmed available (nemotron-3-ultra-free chosen; deepseek-v4-flash-free / nemotron-3.5-lightning-free / laguna-s-2.1-free as fallbacks).
- **pages.yml:** green (run 32394126388 / 32394290526 after PR #95 merge). Main did not advance this run until the model-bump commit.
- **PR #93 checks:** opencode-pr-trigger SUCCESS; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS.
- **PR #95 checks:** merged; Reviewer + Tester approved; issue #94 closed.

## NEXT STEPS

1. **PR #93 root-cause `lab` (RE-DISPATCHED):** Lab Engineer fixes builder.md resume re-task + upgrades model on its own PR/branch (now on `nemotron-3-ultra-free`).
2. **PR #93 docs (Step 1):** re-drive `continue` after the lab fix lands; Builder writes full Obsidian docs and pushes (head advances). On its push, a maintainer run re-surveys, confirms docs COMPLETE and no new-codec work in PR #93 (pivot Step 2 canceled), then dispatches Tester.
3. **PR #93 test+review:** dispatch Tester then Reviewer once docs land.
4. **PR #93 merge:** rebase-merge (`--no-delete-branch`) after docs+tests+review; keep #68 open.
5. **NEW JXL project:** stand up separate codebase/new name on its own issue/branch; route research -> architect -> build.

## OPEN QUESTIONS

- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, merges cleanly). After merge, applies to new project's PR.
- **Orphan-main break:** NOT present - PR #93 `mergeable: clean`; the earlier local NONE was a shallow-clone artifact.
- **Build collision:** AVOIDED (no Builder running at survey; `lab` is infra track).
- **Pivot Step 2 cancellation honored?** UNVERIFIED until the Builder pushes docs - must confirm no new codec was committed into PR #93; if it was, revert via `fix` and re-route to the separate new project.
- **Hollow-build fix efficacy:** DETECTION shipped + MERGED (PR #95); ROOT CAUSE lab hollow'd once (weak model), now RE-DISPATCHED on the strong model this run. Until the lab lands, a re-driven `continue` will still no-op.
- **Model bump success:** PENDING - verify the next build/lab runs actually execute on `nemotron-3-ultra-free` (watch for rate limits / `CreditsError`; fallback deepseek-v4-flash-free).
- **Work preservation:** all R0-R15 codec work preserved on PR #93 (never-merged, branch kept). #68 open as umbrella.
- **New-project issue:** needs an issue. Owner may open it, or I dispatch `ideate` post-PR #93 close. Recorded as pending.
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **`workflows` permission:** opencode app lacks `Workflows` permission; direct agent pushes of workflow files are rejected but the PAT-backed step delivers. Owner can grant; non-blocking.

- Mae, the Maintainer
