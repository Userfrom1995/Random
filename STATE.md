# STATE - Random factory checkpoint

- **Updated:** 2026-08-21 (maintainer run 32453021479, owner `/oc maintainer`
  recall question on PR #93: "what did we decide for the next project?"). The
  Obsidian priority lock is lifted (#68 closed, PR #93 merged into `main`);
  the next-project decision is to resume normal flow via the Ideator /
  Brainstorm Board (#42). The Ideator was re-dispatched this run to force a
  fresh candidate batch.

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finished + landed.** Owner manually merged the branch
  `opencode/issue68-20260818070512` (`d6fbd1cd`) into `main` as `0eb9de0f`
  ("Merge PR #93: Obsidian lossless codec") on 2026-08-21. The codec (R10-B
  CFL + CMARC backend, 9.5209 bpp: beats PNG 13.05 + WebP 9.61; JPEG XL 8.71
  gate lifted per the 2026-08-20 pivot) is now in `main` (128 obsidian files).
- **Issue #68 CLOSED** by owner (2026-08-21T05:34:05Z). The priority-project
  freeze is LIFTED; new projects are allowed again.
- **ONE Obsidian PR rule:** satisfied historically; PR #93 is now closed/merged
  via manual merge. Branch preserved (no `-d`).
- **NEVER delete PR branches after merge.** Kept.
- **Runaway-loop guard shipped** (PRs #95/#97/#99): `opencode.yml` now refuses
  `/oc fix` against a non-OPEN PR or a bare issue, and the retry counter no
  longer falls back to a phantom `0`.

## CRITICAL INFRASTRUCTURE STATE

- **`main` = `0eb9de0f`** ("Merge PR #93: Obsidian lossless codec"), a
  merge-commit of unrelated histories (`git merge-base origin/main
  origin/opencode/issue68-...` was EMPTY - the branch was an orphan vs the
  single-root main). 128 obsidian files present; build artifacts intact.
- **Branch `opencode/issue68-20260818070512` intact** at `d6fbd1cd` (25
  commits); head of the now-merged PR #93. Default codec = 9.5209 bpp, all
  R11-R15 experimental predictors gated OFF. 152 lib tests pass.
- **PR #93 permanently CLOSED + unreopenable** (head `e184c3c` gc'd), but its
  code is now in `main` via the owner's manual merge - nothing stranded.
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`.
  `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` (free).
- **Runaway guard verified shipped** (#99 merged, closes #98). Monitor next lab
  runs for any stray `/oc fix` on a closed PR/issue to confirm it holds.

## NEXT-PROJECT DECISION (active, run 32453021479)

- **Decision:** resume normal project flow via the Ideator + Brainstorm Board
  (#42). After #68 closed + PR #93 merged, the priority lock is lifted, so the
  next build is chosen the usual way: Ideator posts fresh candidates -> Mae
  picks one -> research -> architect -> build.
- **Stall found + being cleared:** the re-dispatched Ideator (ideate run,
  06:01:05Z today, conclusion `success`) posted NO new candidates to #42 - it
  held again on the stale "no new ideas until competitive" freeze narrative
  even though the freeze is gone. This run re-dispatched `ideate` to force a
  fresh batch. Once candidates land, Mae picks the next build.

## IN FLIGHT

- None (no open PRs). Pending: the freshly re-dispatched Ideator to post
  candidates on #42; then pick the next build.

## PENDING (in order)

1. **Get fresh Brainstorm Board candidates** - the Ideator was re-dispatched
   this run (32453021479); await its batch on #42, then pick the next build and
   route research -> architect -> build as appropriate.
2. **builder.md hollow-docs fix** - optional `lab` pass to patch ONLY
   `.github/agents/builder.md` (resume re-task on newest directive). Low
   priority; queue when convenient. If the Ideator holds AGAIN on stale
   narrative, fix the Ideator's freeze heuristic via `lab` instead of another
   re-dispatch.
3. **NEW JXL-beating project (optional):** a separate codebase/new name on its
   own issue/branch (research -> architect -> build). Issue #68 is closed, so a
   new issue would be needed (owner opens, or future ideate). Not urgent; the
   owner lifted the JXL gate for the shipped Obsidian codec.

## ISSUES

- **#68 (Obsidian umbrella)** - CLOSED by owner (2026-08-21T05:34:05Z).
- **#98 (Runaway /oc fix loop)** - CLOSED (PR #99 merged, guard shipped).
- **#96 (Circuit breaker)** - CLOSED (PR #97 merged).
- **#94 (Detect silent no-op builds)** - CLOSED (PR #95 merged).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - freeze lifted; Ideator re-dispatched this run to
  post fresh candidates (prior re-dispatch held on stale narrative).

## REVIEWER/TESTER/MODEL STATUS

- Model config: worker workflows `opencode/nemotron-3-ultra-free`;
  `opencode.json` `hy3-free`/`mimo-v2.5-free`. `origin/main` = `0eb9de0f`.
- pages.yml: triggers only on `pull_request`/`workflow_dispatch`, not push to
  main; the manual merge of a branch (no site-content change) did not trigger a
  Pages deploy, which is correct. Pages last deployed at 05:34:07Z for the
  merged Obsidian site.
- No open PRs require merge/review/test this run.

## NEXT STEPS

1. Await the re-dispatched Ideator's fresh candidates on #42; pick the next
   build and route research -> architect -> build as appropriate.
2. (Optional) If the Ideator holds AGAIN, dispatch `lab` to fix the Ideator's
   freeze heuristic (detect closed priority issue / lifted freeze), not another
   re-dispatch.
3. (Optional) Queue a `lab` pass to fix `.github/agents/builder.md`
   hollow-docs root cause.
4. Monitor next lab runs for any stray `/oc fix` on a closed PR/issue to
   confirm the #99 guard holds.
5. Keep issue #68 closed per the owner's action; do not reopen unless the
   owner directs a new JXL-class effort.

## OPEN QUESTIONS

- **Ideator stall:** will the re-dispatched Ideator (this run) post candidates,
  or hold a third time on stale board text? If it holds, the fix is a `lab`
  pass on the Ideator's freeze heuristic, not another re-dispatch.
- **Recovery root cause (answered):** PR #93 unrecoverable by the factory
  because (a) its head commit was gc'd -> unreopenable, and (b) the Maintainer
  is forbidden from creating PRs/pushing branches -> could not open a fresh PR.
  The branch `d6fbd1cd` was always preserved, so the owner's manual merge
  landed it cleanly; no work lost. Documented on PR #93.
- **Single-commit `main`:** main is a single root commit with PR #93 merged as
  a merge-commit of unrelated histories (orphan branch). Intentional
  (circuit-breaker) but worth a `lab` audit note; not escalated.
- **builder.md lab (optional):** re-engage a targeted `lab` when convenient.
- **New-project issue:** now allowed (issue #68 closed); a fresh JXL-class
  project would need its own issue/branch, owner-opened or via ideate.

- Mae, the Maintainer
