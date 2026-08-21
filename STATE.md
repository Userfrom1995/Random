# STATE - Random factory checkpoint

- **Updated:** 2026-08-21 (maintainer run 32438680036, `/oc maintainer` on
  PR #99). PR #99 MERGED into `main` (`5a92107b`) via rebase; issue #98
  CLOSED. PR #93 remains permanently CLOSED and unreopenable (head commit
  gc'd); branch preserved at `d6fbd1cd` with the finished Obsidian codec.
  Standing owner pivot (2026-08-20) REMAINS law where not overridden.

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted** (pivot 2026-08-20).
  Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on
  Kodak at 9.5209 bpp) with full docs; then Test + Review + merge. Keep
  branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying
  the JPEG XL 8.71 gate, on its OWN issue/branch (research -> architect ->
  build). Never folded into PR #93.
- **ONE Obsidian PR only (wound down):** PR #93 was the single canonical
  Obsidian PR; the owner CLOSED it (2026-08-20) and re-engaged directly
  (2026-08-21). It is now UNREOPENABLE (see CRITICAL below). A future new
  codec PR would be the separate JXL project.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats
  JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68.

## CRITICAL INFRASTRUCTURE STATE

- **`main` = `5a92107b`** (was `0d0d75fa`); advanced by the PR #99 merge
  (rebase). The lab spine was rewritten (circuit-breaker PR #97 path), so
  EVERY feature branch is still an ORPHAN with no common ancestor to `main`,
  EXCEPT PR #99's branch `opencode/lab-98-runaway-fix-retry` which DID share
  `0d0d75fa` and merged cleanly.
- **PR #93 is UNREOPENABLE.** Its recorded head `e184c3c` no longer exists in
  the repo (gc'd after the branch advanced to `d6fbd1cd`); `gh pr reopen`
  returns "Could not open the pull request." A merge therefore requires a
  FRESH PR from the branch tip `d6fbd1cd`, which the Maintainer cannot create
  (hard rule: no self-created PRs; no push to branches).
- **Branch `opencode/issue68-20260818070512` intact** at `d6fbd1cd` (25
  commits), head of the closed PR. Default codec = 9.5209 bpp, all R11-R15
  experimental predictors gated OFF. 152 lib tests pass.
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`.
  `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` (free).
- **RUNNAWAY-LOOP GUARD SHIPPED (PR #99, closes #98):** `opencode.yml` now
  refuses to auto-retry `/oc fix` against a non-OPEN PR or a bare issue, and
  the retry counter no longer falls back to a phantom `0`. The #98 CI-burn
  root cause is eliminated at the source.

## PRIORITY PROJECT (Obsidian, PR #93) - ARCHIVED ON BRANCH

- Default shipped codec = 9.5209 bpp mean (R10-B CFL + CMARC backend).
  Beats PNG (13.05) + WebP (9.61). JXL 8.71 gate LIFTED by owner pivot (not
  met; structural ceiling proven across 10 axes).
- PR #93 CLOSED + unreopenable. Branch preserved at `d6fbd1cd`. To land in
  `main`: owner opens a FRESH PR from the branch; Maintainer then runs
  Review -> Test -> merge (GitHub merge-commit, since unrelated histories).
- builder.md hollow-docs root cause: DEFERRED (see Pending).

## IN FLIGHT

- None of mine. PR #99 (lab guard) is MERGED this run; issue #98 CLOSED.
- builder.md resume-re-task fix: DEFERRED until the #93 situation settles.

## PENDING (in order)

1. **Land Obsidian in main (owner action):** open a fresh PR from
   `opencode/issue68-20260818070512` (`d6fbd1cd`); then I run Review -> Test
   -> merge (merge-commit; branch kept, no `-d`). Blocked on owner.
2. **builder.md `lab` fix (deferred)** -> targeted `lab` on ONLY
   `.github/agents/builder.md` after #93 settles (lab-health).
3. **NEW JXL project:** separate codebase/new name on its own issue/branch;
   route research -> architect -> build. Blocked on an issue (I cannot
   create issues; await owner/ideate).

## ISSUES

- **#68 (Obsidian umbrella)** - OPEN, stays open until the new JXL-class
  project beats codecs (per pivot + standing directive).
- **#98 (Runaway /oc fix loop)** - CLOSED (PR #99 merged, guard shipped).
- **#96 (Circuit breaker)** - CLOSED (PR #97 merged).
- **#94 (Detect silent no-op builds)** - CLOSED (PR #95 merged).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted.

## REVIEWER/TESTER/MODEL STATUS

- Model config: worker workflows `opencode/nemotron-3-ultra-free`;
  `opencode.json` `hy3-free`/`mimo-v2.5-free`. `origin/main` = `5a92107b`.
- pages.yml: triggers only on `pull_request`/`workflow_dispatch`, not push to
  main; no site-content change in PR #99, so no deploy required this run.
- PR #99 MERGED and #98 CLOSED. No open PRs require my merge.
- No open PRs require my merge this run.

## NEXT STEPS

1. Await owner to open a FRESH PR from `opencode/issue68-20260818070512`
   (`d6fbd1cd`) if they want the Obsidian codec merged into main; then run
   Review -> Test -> merge (merge-commit, keep branch).
2. After #93 settles, re-engage a targeted `lab` to fix ONLY
   `.github/agents/builder.md` (resume re-task on newest directive).
3. Stand up NEW JXL project on its own issue/branch once an issue exists
   (owner opens, or future `ideate`); route research -> architect -> build.
4. Monitor next lab runs for any stray `/oc fix` on an issue/closed PR to
   confirm the #99 guard holds.

## OPEN QUESTIONS

- **PR #93 land vs archive:** owner closed it (wind-down) but the pivot said
  "Test + Review + merge." Since #93 is unreopenable and I cannot create PRs,
  the decision is the owner's: open a fresh PR to merge, or leave archived on
  the branch. Communicated earlier via comment.md on PR #93.
- **Single-commit `main`:** the lab spine is one root commit (now with PR #99
  merged on top as `5a92107b`); all non-#99 branches remain orphans. Merges
  of those will be merge-commits (rebase impossible). Intentional
  (circuit-breaker) or worth a `lab` audit? Flagged; not yet escalated.
- **builder.md lab (DEFERRED):** re-engage after #93 settles; patch ONLY
  `.github/agents/builder.md`.
- **New-project issue:** blocked on owner/ideate (hard rule: no self-issue).

- Mae, the Maintainer