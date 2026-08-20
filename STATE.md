# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (maintainer run 32411289098, owner `/oc maintainer` on PR #93, finish-and-close under the standing owner pivot). **OWNER PIVOT (2026-08-20T14:52:11Z) REMAINS THE STANDING LAW.**

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted.** Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on Kodak at 9.5209 bpp) with full docs; then Test + Review + merge. Keep branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying the JPEG XL 8.71 gate, developed on its OWN issue/branch (research -> architect -> build). Never folded into PR #93.
- **ONE Obsidian PR only (being wound down):** PR #93 is the single canonical Obsidian PR. After it merges, the "one-PR" rule applies to the new project's PR.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68 on PR #93 merge.

## CRITICAL INFRASTRUCTURE STATE

- **PR #93 NOT ORPHANED (re-confirmed this run):** GitHub compare API says `status: ahead`, shared merge-base `37f0395` (ahead 23 / behind 0). The empty local `git merge-base` is a shallow-clone artifact. `mergeable_state` reported `unstable` (transient; branch is ahead-only with behind:0, so a rebase merge will be clean).
- **PR #95 MERGED:** `main` = `37f0395`. Orphan-main guard + hollow-build detection live.
- **MODEL PINS:** worker workflows `opencode/nemotron-3...` family on free models. `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` until the lab branch merges. No CreditsError.
- **ROOT-CAUSE LAB:** the Lab Engineer scoped itself OUT of PR #93 product source (lab domain only); hollow-build DETECTION (PR #95) is the mitigation.

## PRIORITY PROJECT (Obsidian, PR #93) - FINISH-AND-CLOSE (JXL gate lifted)

- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL + CMARC backend; R13-A muted, R13-B/R14/R15 gated OFF, all byte-identical base so never-regressive). Beats PNG (13.05) + WebP (9.61). JXL gate LIFTED by owner order.
- **Test-isolation fix landed (head `e085562`):** clean parallel suite = **148 passed / 0 failed / 2 ignored**. R15 stays net-negative; 9.5209 bpp production unchanged.
- **R15 halt (head `8ac10cf` line):** 10-axis predictor-family exhaustion proven (residual near-incompressible after R9-B); all decorrelation/learned overlays gated OFF, byte-identical base.
- **ONLY REMAINING BLOCKER = Step 1 docs.** `obsidian/README.md` stale (`27.82 bpp` / `46 tests` / "M1 gate still open" from 2026-08-17). `obsidian/STATUS.md` MISSING. A `continue` is re-dispatched this run (head `8ac10cf`) with an explicit gates-lifted docs-only directive.

## CURRENT STATE - THIS RUN (32411289098)

- **PR #93 (head `8ac10cf03d5a81c072b197f569346ab630abf025`):** OPEN, ahead 23 / behind 0 of `main`, shared merge-base `37f0395` (NOT orphaned). One-PR rule intact; all codec work preserved.
- **Single blocker:** stale docs (README + missing STATUS.md). Codec byte-identical at 9.5209 bpp.
- **No Builder in flight** at dispatch (verified: no in_progress/queued opencode run other than this maintainer run). The re-dispatched `continue` is collision-safe.
- **Prior `continue` (run 32410896470) did NOT write docs:** it produced a "resume-state" commit (`8ac10cf`, only `.tmp/random-lab-decision.json` + progress file) and re-escalated to maintainer, still framing the work as a dead end. Under the pivot it is a close-out, so this run re-directs it explicitly.

## IN FLIGHT

- **PR #93 Step 1 docs:** `continue` re-dispatched this run (head `8ac10cf`). Builder must rewrite `obsidian/README.md` to accurate 9.5209 bpp / 148 tests / PNG+WebP MET / JXL gate lifted, create `obsidian/STATUS.md`, remove stray `err.txt`, and keep the codec byte-identical. On its push, a maintainer run re-surveys.
- **PR #93 Tester:** `/oc test` after docs land - QA + real-Kodak reproducibility.
- **PR #93 Reviewer:** `/oc review` - strict read-only quality gate.
- **PR #93 merge:** rebase-merge (`--no-delete-branch`) after docs + tests + review; JXL gate lifted. Keep #68 open.

## PENDING (awaiting completion, in order)

1. PR #93 docs (Step 1) - `continue` re-dispatched this run (head `8ac10cf`).
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

- **Model config:** worker workflows on free models. `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` until lab branch merges. `origin/main` = `37f0395`. Free fallbacks available.
- **pages.yml:** green.
- **PR #93 checks:** opencode-pr-trigger SUCCESS; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS. No Reviewer/Tester run on PR #93 yet - both required pre-merge.

## NEXT STEPS

1. PR #93 docs (Step 1): `continue` re-dispatched (head `8ac10cf`); await Builder push with accurate README + STATUS.md and NO codec changes.
2. On push -> re-survey, confirm (a) README/STATUS accurate, (b) head still `8ac10cf` lineage / codec unchanged at 9.5209 bpp; then dispatch Tester then Reviewer.
3. Merge PR #93 (rebase, keep branch, JXL gate lifted), keep #68 open.
4. Stand up NEW JXL project on its own issue/branch; route research -> architect -> build.

## OPEN QUESTIONS

- **Docs quality (hollow-build watch):** will the Builder write REAL docs this time (not just a resume-state commit)? Monitored by PR #95 hollow-build detection + this run's explicit directive + the live comment thread. The Builder previously defaulted to "escalate to maintainer" instead of docs; the directive now names the pivot explicitly to prevent that.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN). Applies to new project's PR post-merge.
- **Orphan-main break:** RESOLVED (shared merge-base `37f0395` confirmed via API; behind:0).
- **mergeable_state unstable:** transient; branch is ahead-only (behind:0), so rebase merge will be clean. Re-verify at merge time.
- **Build collision:** AVOIDED (no Builder in flight at dispatch; `continue` re-dispatch safe).
- **Pivot Step 2 cancellation honored?** VERIFY on docs push - no new codec commits in PR #93; all decorrelation/learned overlays already gated off.
- **New-project issue:** needs an issue; owner may open or I dispatch `ideate` post-PR #93 close (hard rule: I do not create issues myself).
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **`workflows` permission:** opencode app lacks `Workflows` permission; direct agent workflow pushes rejected but PAT-backed step delivers. Non-blocking.

- Mae, the Maintainer
