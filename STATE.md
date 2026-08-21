# STATE - Random factory checkpoint

- **Updated:** 2026-08-21 (maintainer run 32452227155, owner question on PR
  #93 "why couldn't the factory recover"). PR #93's branch was manually merged
  into `main` by the owner (`0eb9de0f`, merge-commit of the orphan history).
  Issue #68 CLOSED by owner. Lab idle; Ideator dispatched to resume normal
  project flow.

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finished + landed.** Owner manually merged the branch
  `opencode/issue68-20260818070512` (`d6fbd1cd`) into `main` as `0eb9de0f`
  ("Merge PR #93: Obsidian lossless codec") on 2026-08-21. The codec (R10-B
  CFL + CMARC backend, 9.5209 bpp: beats PNG 13.05 + WebP 9.61; JPEG XL 8.71
  gate lifted per the 2026-08-20 pivot) is now in `main` (128 obsidian files).
- **Issue #68 CLOSED** by owner (2026-08-21T05:34:05Z). The priority-project
  lock is lifted; new projects are allowed again.
- **ONE Obsidian PR rule:** satisfied historically; PR #93 is now closed/merged
  via manual merge. Branch preserved (no `-d`).
- **NEVER delete PR branches after merge.** Kept.
- **Runaway-loop guard shipped** (PRs #95/#97/#99): `opencode.yml` now refuses
  `/oc fix` against a non-OPEN PR or a bare issue, and the retry counter no
  longer falls back to a phantom `0`.

## CRITICAL INFRASTRUCTURE STATE

- **`main` = `0eb9de0f`** ("Merge PR #93: Obsidian lossless codec"), a
  merge-commit of unrelated histories (`git merge-base origin/main
  origin/opencode/issue68-...` is EMPTY - the branch was an orphan vs the
  single-root main). 128 obsidian files present; build artifacts intact.
- **Branch `opencode/issue68-20260818070512` intact** at `d6fbd1cd` (25
  commits); head of the now-merged PR #93. Default codec = 9.5209 bpp, all
  R11-R15 experimental predictors gated OFF. 152 lib tests pass.
- **PR #93 permanently CLOSED + unreopenable** (head `e184c3c` gc'd), but its
  code is now in `main` via the owner's manual merge - so the unreopenability
  is moot; nothing is stranded.
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`.
  `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` (free).
- **Runaway guard verified shipped** (#99 merged, closes #98). Should prevent
  recurrence; monitor next lab runs for any stray `/oc fix` on a closed PR.

## PRIORITY PROJECT (Obsidian) - LANDED

- Merged into `main` by owner as `0eb9de0f`. Default shipped codec = 9.5209
  bpp mean (R10-B CFL + CMARC backend). Beats PNG (13.05) + WebP (9.61). JXL
  8.71 gate LIFTED by owner pivot (structural ceiling proven across 10 axes
  R11-D/R11-A/64-leaf x2/R12-A/R13-A/R13-B/R14-A/R15 + CMARC).
- All experimental predictors (R11-R15) gated OFF by default; the gated code
  remains in the tree as evidence of the ceiling and as a base for any future
  JXL-class effort.

## IN FLIGHT

- None. PR #93 merged manually by owner. No open PRs. Ideator dispatched this
  run to resume normal flow.

## PENDING (in order)

1. **Resume normal project flow** - Ideator dispatched (this run) to surface
   fresh candidates from the Brainstorm Board (#42) now that #68 is closed.
2. **builder.md hollow-docs fix** - optional `lab` pass to patch ONLY
   `.github/agents/builder.md` (resume re-task on newest directive). Low
   priority; queue when convenient.
3. **NEW JXL-beating project (optional):** a separate codebase/new name on its
   own issue/branch (research -> architect -> build). Issue #68 is closed, so
   a new issue would be needed (owner opens, or future ideate). Not urgent; the
   owner lifted the JXL gate for the shipped Obsidian codec.

## ISSUES

- **#68 (Obsidian umbrella)** - CLOSED by owner (2026-08-21T05:34:05Z).
- **#98 (Runaway /oc fix loop)** - CLOSED (PR #99 merged, guard shipped).
- **#96 (Circuit breaker)** - CLOSED (PR #97 merged).
- **#94 (Detect silent no-op builds)** - CLOSED (PR #95 merged).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Ideator re-engaged
  this run.

## REVIEWER/TESTER/MODEL STATUS

- Model config: worker workflows `opencode/nemotron-3-ultra-free`;
  `opencode.json` `hy3-free`/`mimo-v2.5-free`. `origin/main` = `0eb9de0f`.
- pages.yml: triggers only on `pull_request`/`workflow_dispatch`, not push to
  main; the manual merge of a branch (no site-content change) did not trigger
  a Pages deploy, which is correct.
- No open PRs require merge/review/test this run.

## NEXT STEPS

1. Await Ideator candidates from the Brainstorm Board (#42); pick the next
   build and route research -> architect -> build as appropriate.
2. (Optional) Queue a `lab` pass to fix `.github/agents/builder.md`
   hollow-docs root cause.
3. Monitor next lab runs for any stray `/oc fix` on a closed PR/issue to
   confirm the #99 guard holds.
4. Keep issue #68 closed per the owner's action; do not reopen unless the
   owner directs a new JXL-class effort.

## OPEN QUESTIONS

- **Recovery root cause (answered this run):** PR #93 unrecoverable by the
  factory because (a) its head commit was gc'd -> unreopenable, and (b) the
  Maintainer is forbidden from creating PRs/pushing branches -> could not open
  a fresh PR. The branch `d6fbd1cd` was always preserved, so the owner's
  manual merge landed it cleanly; no work lost. Documented in comment.md on
  PR #93.
- **Single-commit `main`:** main is a single root commit with PR #93 merged as
  a merge-commit of unrelated histories (orphan branch). Intentional
  (circuit-breaker) but worth a `lab` audit note; not escalated.
- **builder.md lab (optional):** re-engage a targeted `lab` when convenient.
- **New-project issue:** now allowed (issue #68 closed); a fresh JXL-class
  project would need its own issue/branch, owner-opened or via ideate.

- Mae, the Maintainer
