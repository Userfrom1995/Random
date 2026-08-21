# STATE - Random factory checkpoint

- **Updated:** 2026-08-21 (maintainer run 32452805905, owner `/oc maintainer` on
  issue #42 Brainstorm Board). Ideator re-dispatched a 2nd time after its prior
  run analyzed the board but asked instead of posting a fresh batch; its notify
  step pinged `/oc maintainer`, which triggered this run. Directive issued: the
  Ideator must post 2-3 candidates when dispatched.

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finished + landed.** Owner manually merged the branch
  `opencode/issue68-20260818070512` (`d6fbd1cd`) into `main` as `0eb9de0f`
  ("Merge PR #93: Obsidian lossless codec") on 2026-08-21. The codec (R10-B
  CFL + CMARC backend, 9.5209 bpp: beats PNG 13.05 + WebP 9.61; JPEG XL 8.71
  gate lifted per the 2026-08-20 pivot) is now in `main` (128 obsidian files).
- **Issue #68 CLOSED** by owner (2026-08-21T05:34:05Z). The priority-project
  freeze is LIFTED; new projects are allowed again.
- **NEVER delete PR branches after merge.** Kept (standing owner directive).
- **Runaway-loop guard shipped** (PRs #95/#97/#99): `opencode.yml` refuses
  `/oc fix` against a non-OPEN PR or a bare issue, and the retry counter no
  longer falls back to a phantom `0`.

## CRITICAL INFRASTRUCTURE STATE

- **`main` = `0eb9de0f`** (merge-commit of unrelated histories with the orphan
  issue68 branch). 128 obsidian files present; build artifacts intact.
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`.
  `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` (free).
- **Runaway guard verified shipped** (#99 merged, closes #98).

## PRIORITY PROJECT (Obsidian) - LANDED

- Merged into `main` by owner as `0eb9de0f`. Default shipped codec = 9.5209
  bpp mean (R10-B CFL + CMARC backend). Beats PNG (13.05) + WebP (9.61). JXL
  8.71 gate LIFTED by owner pivot (structural ceiling proven across 10 axes).

## IN FLIGHT

- **Ideator re-dispatch (this run):** `ideate` dispatched (run 32452805905) to
  get a fresh 2-3 candidate batch posted on #42. The previous dispatch
  (32452715519) ran but the agent did not post - it asked instead - and its
  notify step pinged `/oc maintainer`, triggering this run. Directive: post now.
- No open PRs. No builder/architect/research runs in flight.

## PENDING (in order)

1. **Ideator must post a fresh batch on #42** - re-dispatched this run. After
   candidates land, pick the next build and route research -> architect ->
   build. Parked eligible candidates: Corundum (C crypto), Tundra (Go VCS),
   Ravel (Elixir/Phoenix).
2. **Ideator prompt hardening (escalation if it stalls a 3rd time):** a `lab`
   pass to add an explicit "always post 2-3 candidates when dispatched" rule
   to `.github/agents/ideator.md` so the ask-instead-of-post stall can't recur.
3. **builder.md hollow-docs fix** - optional `lab` pass to patch ONLY
   `.github/agents/builder.md` (resume re-task on newest directive). Low
   priority; queue when convenient.
4. **Next build pick** - once candidates exist, pick and route per pipeline.

## ISSUES

- **#68 (Obsidian umbrella)** - CLOSED by owner (2026-08-21T05:34:05Z).
- **#98 (Runaway /oc fix loop)** - CLOSED (PR #99 merged, guard shipped).
- **#96 (Circuit breaker)** - CLOSED (PR #97 merged).
- **#94 (Detect silent no-op builds)** - CLOSED (PR #95 merged).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - freeze lifted; Ideator re-engaged THIS run to
  post fresh candidates; parked candidates remain eligible.

## REVIEWER/TESTER/MODEL STATUS

- Model config: worker workflows `opencode/nemotron-3-ultra-free`;
  `opencode.json` `hy3-free`/`mimo-v2.5-free`. `origin/main` = `0eb9de0f`.
- pages.yml: triggers only on `pull_request`/`workflow_dispatch`, not push to
  main; the manual merge of a branch (no site-content change) did not trigger a
  Pages deploy, which is correct. Pages last deployed at 05:34:07Z for the
  merged Obsidian site.
- No open PRs require merge/review/test this run.

## NEXT STEPS

1. Await the fresh Ideator batch on #42 (dispatched this run). If it posts,
   pick the next build and route research -> architect -> build.
2. If the Ideator under-delivers a 3rd consecutive time, dispatch `lab` to
   harden `.github/agents/ideator.md` (explicit post-when-dispatched rule).
3. (Optional) Queue a `lab` pass to fix `.github/agents/builder.md`
   hollow-docs root cause.
4. Keep issue #68 closed per the owner's action; do not reopen unless the
   owner directs a new JXL-class effort.

## OPEN QUESTIONS

- **Ideator stall (active):** run 32452715519 analyzed but did not post, then
  its notify step pinged `/oc maintainer`, triggering this run - a soft loop.
  This run re-dispatches `ideate` with a directive to post now. Root cause:
  the Ideator, on a "re-dispatch to resume" framing, asked permission instead
  of posting. If it recurs, escalate to a `lab` prompt fix.
- **Single-commit `main`:** main is a single root commit with PR #93 merged as
  a merge-commit of unrelated histories (orphan branch). Intentional
  (circuit-breaker) but worth a `lab` audit note; not escalated.
- **builder.md lab (optional):** re-engage a targeted `lab` when convenient.
- **New-project issue:** now allowed (issue #68 closed); a fresh JXL-class
  project would need its own issue/branch, owner-opened or via ideate.

- Mae, the Maintainer
