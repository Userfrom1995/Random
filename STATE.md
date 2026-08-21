# STATE - Random factory checkpoint

- **Updated:** 2026-08-21 (maintainer run 32437741517, EVENT: audit issue
  #98 created). CRITICAL: a runaway /oc fix auto-retry loop was detected,
  halted live, and a Lab Engineer fix is dispatched. The earlier "owner
  re-driving PR #93" framing (run 32437077182) was a misdiagnosis: the live
  loop was on issue #68, not PR #93.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian PR #93 = finish-and-close, JXL gate lifted** (pivot 2026-08-20).
  Ship the documented R10-B + CMARC codec, then Test + Review + merge. Keep
  branch (no `-d`).
- **Separate new project for JXL:** new codebase/new name, own
  issue/branch (research -> architect -> build). Never folded into PR #93.
- **ONE Obsidian PR only (being wound down):** PR #93 is the single canonical
  Obsidian PR; the owner CLOSED it (2026-08-20). A future new codec PR would
  be the separate JXL project.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Issue #68 stays OPEN** as the umbrella goal until the new JXL-class
  project beats codecs. Do NOT close #68 (it is also the de-facto target the
  runaway loop latched onto - see Critical Infra below).

## CRITICAL INFRASTRUCTURE STATE (RUNWAY LOOP - RESOLVED LIVE)
- **Runaway auto-retry loop: DETECTED + HALTED this run.** Root cause: the
  FIX-mode "Verify fix pushed" step (`opencode.yml:673`) and the identical
  BUILD-mode step (`opencode.yml:406`) treat any issue_comment as a PR. A
  `/oc fix` comment on **issue #68** (an issue, not a PR) made the step run
  `gh pr view 68` (empty), fall through to auto-retry, and post
  `/oc fix (auto-retry N)` on #68, re-triggering the pipeline every ~1-2 min
  (20+ opencode runs 01:20Z-01:56Z). The `gh api --jq ... || echo "0"`
  retry counter swallows errors and always returns 0, so the 3-cap never
  engaged.
- **Immediate mitigation done:** canceled live runs 32438017528 +
  32438076320; DELETED the 5 auto-retry comments on issue #68 (sole trigger
  source). Verified: 0 auto-retry comments on #68/#93/#98, no opencode run
  in_progress. Loop STOPPED.
- **Durable fix:** Lab Engineer dispatched (`/oc lab` on issue #98) to patch
  both verify steps: (1) confirm target is an OPEN PR first, else exit 0 and
  never auto-retry; (2) robust retry counter; (3) global circuit breaker
  (stop after 3 auto-retries); (4) empty-commit push counts as success;
  (5) workflow-level guard refusing FIX/BUILD mode on non-open-PR targets.
- **`main` = `0d0d75fa`.**
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`.
  `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` (free).

## PRIORITY PROJECT (Obsidian, PR #93) - OWNER DRIVE, COMPLY
- Default shipped codec = 9.5209 bpp mean (R10-B CFL + CMARC backend).
  Beats PNG (13.05) + WebP (9.61). JXL 8.71 gate LIFTED by owner pivot.
- Owner's direct PR #93 thread: I do NOT inject `/oc` triggers or merge.
- builder.md hollow-docs root cause: DEFERRED (see Pending).

## IN FLIGHT
- **Lab Engineer fix for opencode.yml runaway loop (issue #98):** dispatched
  this run; awaiting the Lab Engineer's PR + review/test/merge. High priority
  (systemic CI-burn prevention).
- **Owner's direct PR #93 work:** comply; no interference from my side.

## PENDING (in order)
1. Lab Engineer merges the opencode.yml auto-retry guard (issue #98). After
   merge, confirm no recurrence on stray /oc fix on issues/closed PRs.
2. builder.md `lab` fix (deferred) -> targeted `lab` on ONLY
   `.github/agents/builder.md` after #93 settles (lab-health).
3. NEW JXL project: separate codebase/new name on its own issue/branch;
   route research -> architect -> build. Blocked on an issue (hard rule:
   no self-issue; await owner/ideate).

## ISSUES
- **#98 (Audit - runaway loop)** - OPEN, assigned to Lab Engineer via `lab`.
- **#68 (Obsidian umbrella)** - OPEN, stays open; also the issue the loop
  latched onto (now cleaned of auto-retry spam).
- **#96 (Circuit breaker)** - CLOSED (PR #97 merged).
- **#94 (Detect silent no-op builds)** - CLOSED (PR #95 merged).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted.

## REVIEWER/TESTER/MODEL STATUS
- Model config: worker workflows `opencode/nemotron-3-ultra-free`;
  `opencode.json` `hy3-free`/`mimo-v2.5-free`. `origin/main` = `0d0d75fa`.
- pages.yml: will re-deploy on next main advance (none this run; the lab fix
  PR will advance main once merged).
- PR #93: owner driving directly; standing Reviewer+Tester-before-merge
  requirement is moot unless the owner reopens/merges.
- No open PRs require my merge this run.

## NEXT STEPS
1. Await Lab Engineer PR for issue #98; after review+test approve and merge
   (lab infra fix, merges freely). Verify the guard ends the loop class.
2. After merge, monitor for any stray `/oc fix`/`/oc build` on an issue or
   closed PR to confirm no recurrence.
3. Resume deferred builder.md `lab` once owner's #93 work settles.
4. Stand up NEW JXL project on its own issue/branch once an issue exists.

## OPEN QUESTIONS
- **PR #93 disposition:** owner re-driving a CLOSED PR via issue_comment;
  comply. Reopen+merge, or keep closed with branch preserved? PENDING owner.
- **Runaway loop recurrence:** watch after Lab Engineer merge; expect none
  given the open-PR guard + circuit breaker.
- **builder.md lab (DEFERRED):** re-engage after #93 settles; patch ONLY
  `.github/agents/builder.md`.
- **New-project issue:** blocked on owner/ideate (hard rule: no self-issue).
- **Orphan-main / workflows-wall:** resolved (API PR merge works; shared
  merge-base).

- Mae, the Maintainer
