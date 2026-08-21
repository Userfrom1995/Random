# STATE - Random factory checkpoint

- **Updated:** 2026-08-21 (maintainer run 32437077182, scheduled/empty
  payload). No merge this run; the owner is actively re-driving PR #93
  directly. Standing owner pivot (2026-08-20T14:52:11Z) REMAINS the law
  where not overridden by a later owner action.

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finish-and-close, JXL gate lifted** (pivot 2026-08-20).
  Ship the documented R10-B + CMARC codec (beats PNG 13.05 + WebP 9.61 on
  Kodak at 9.5209 bpp) with full docs; then Test + Review + merge. Keep
  branch (no `-d`).
- **Separate new project for JXL:** a new codebase with a new name, carrying
  the JPEG XL 8.71 gate, on its OWN issue/branch (research -> architect ->
  build). Never folded into PR #93.
- **ONE Obsidian PR only (being wound down):** PR #93 was the single canonical
  Obsidian PR; the owner CLOSED it (2026-08-20) but is now RE-DRIVING it
  directly (2026-08-21) - see below. A future new codec PR would be the
  separate JXL project.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new project beats
  JXL (PNG + WebP + JPEG XL lossless on Kodak). Do NOT close #68.

## CRITICAL INFRASTRUCTURE STATE

- **PR #97 (circuit breaker for #96): MERGED 2026-08-20 (rebase, branch
  KEPT).** `main` = `0d0d75fa`. Issue #96 CLOSED.
- **`workflows` permission wall (KNOWN, NON-BLOCKING):** API PR merge
  succeeded for PR #97; only direct `git push` of workflow files is blocked.
- **PR #93 status flip:** CLOSED by owner 2026-08-20, but the owner RE-ENGAGED
  it directly on 2026-08-21 via issue_comment (`/oc fix (auto-retry 1)` at
  01:32:58Z). Fixer run 32436674387 SUCCEEDED (findings already resolved,
  rebuttal posted). Builder run 32436908531 IN_PROGRESS (headSha = main
  because the PR is closed). Branch `opencode/issue68-20260818070512`
  retained (head `e184c3c`; ls-remote `3bf9a1c551...`).
- **`main` = `0d0d75fa`.**
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`.
  `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` (free).

## PRIORITY PROJECT (Obsidian, PR #93) - OWNER RE-DRIVING DIRECTLY

- Default shipped codec = 9.5209 bpp mean (R10-B CFL + CMARC backend).
  Beats PNG (13.05) + WebP (9.61). JXL 8.71 gate LIFTED by owner pivot.
- Owner is personally running the review/fix loop on the retained branch.
  **Maintainer complies: no `/oc` triggers, no merge from my side.**
- builder.md hollow-docs root cause: DEFERRED (see Pending).

## IN FLIGHT

- **Owner's direct work on PR #93 branch (`e184c3c`):** re-engaged
  2026-08-21 with `/oc fix (auto-retry 1)`, fixer run succeeded, builder run
  in_progress. Owner driving directly; I do not interfere.
- **builder.md resume-re-task fix:** DEFERRED until owner's #93 work settles.

## PENDING (in order)

1. Owner's direct PR #93 disposition (reopen+merge, or keep closed) - comply.
2. builder.md `lab` fix (deferred) -> targeted `lab` on ONLY
   `.github/agents/builder.md` after #93 settles (lab-health).
3. NEW JXL project: separate codebase/new name on its own issue/branch;
   route research -> architect -> build. Blocked on an issue (I cannot
   create issues; await owner/ideate).

## ISSUES

- **#68 (Obsidian umbrella)** - OPEN, stays open until the new JXL-class
  project beats codecs (per pivot + standing directive).
- **#96 (Circuit breaker)** - CLOSED (PR #97 merged).
- **#94 (Detect silent no-op builds)** - CLOSED (PR #95 merged).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted.

## REVIEWER/TESTER/MODEL STATUS

- Model config: worker workflows `opencode/nemotron-3-ultra-free`;
  `opencode.json` `hy3-free`/`mimo-v2.5-free`. `origin/main` = `0d0d75fa`.
- pages.yml: will re-deploy on next main advance (none this run).
- PR #93: owner driving directly; standing Reviewer+Tester-before-merge
  requirement is moot unless the owner reopens/merges.
- No open PRs require my merge this run.

## NEXT STEPS

1. COMPLY with the owner's direct PR #93 re-drive; do not inject `/oc`
   triggers or merge. Monitor the in_progress builder run 32436908531.
2. After the owner's PR #93 work settles, re-engage a targeted `lab` to fix
   ONLY `.github/agents/builder.md` (resume re-task on newest directive).
3. Stand up NEW JXL project on its own issue/branch once an issue exists
   (owner opens, or future `ideate`); route research -> architect -> build.

## OPEN QUESTIONS

- **PR #93 disposition:** owner re-driving a CLOSED PR via issue_comment.
  Reopen+merge, or keep closed with branch preserved? PENDING owner - comply.
- **builder.md lab (DEFERRED):** re-engage after #93 settles; patch ONLY
  `.github/agents/builder.md`.
- **New-project issue:** blocked on owner/ideate (hard rule: no self-issue).
- **In_progress build 32436908531:** confirm it no-ops cleanly on the closed
  PR (headSha = main) or attempts a push; monitor next survey.
- **Orphan-main / workflows-wall:** resolved (API PR merge works; shared
  merge-base).

- Mae, the Maintainer
