# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32459960895, EVENT `created` on PR #101, owner halt of Resonata). PR #102 (Ideator-stall fix, approved+tested) is being landed into `main` via the `recover` step after I closed it (branch preserved). The Ideator is re-dispatched once #102 lands so the Brainstorm Board (#42) resumes.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped.** Owner manually merged PR #93 into `main` as orphan root `60748e88` ("lab: empower Maintainer as sovereign to recover closed/orphaned PRs and resolve conflicts"), containing obsidian (128 files) + all prior projects. Default codec = 9.5209 bpp; R11-R15 experimental predictors gated OFF; 152 lib tests pass.
- **Issue #68 CLOSED** by owner. Priority-project freeze LIFTED; new projects allowed again.
- **One-PR rule + NEVER delete PR branches:** satisfied; PR #93 CLOSED, branch preserved. Runaway-loop guard shipped (PRs #95/#97/#99) holds.
- **Maintainer sovereign-recovery directive:** `60748e88` explicitly empowers the Maintainer to recover orphaned/closed PRs via `recover` and resolve conflicts. main must never become a divergent/orphan ROOT; all advances stay descendants of the prior tip.
- **Resonata HALTED by owner:** PR #101 + issue #100 CLOSED by the owner. No recovery; artifacts preserved on branch `opencode/issue100-20260821065856`. Comply.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `60748e88`** - intentional single-root (orphan) commit by the owner's recovery. Contains obsidian + glyphforge/halcyon/kestrel/meridian/etc.
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`; `opencode.json` `hy3-free`/`mimo-v2.5-free` (free).
- **Runaway-loop guard (PR #99):** holds - no stray `/oc fix` on closed PRs/issues observed this run.
- **OPEN-PR MERGE-PATH GAP (logged):** this workflow has no step that merges an OPEN approved+tested PR; only `recover` lands CLOSED PRs. Worked around for #102 by closing-then-recover. Durable `lab` fix recommended (rebase-merge open approved PRs cleanly).

## IN FLIGHT
1. **PR #102 - `[Infra] Lab update for #42` (Ideator-stall hardening).** Was OPEN, approved+tested (Reviewer `/oc approve` + Tester `/oc approve-test`, no later `/oc fix`). CLOSED this run (branch `opencode/issue42-20260821070030` preserved); `recover` step lands it into `main` (`60748e88` shared history, clean merge). Body has NO `Closes #42`, so #42 stays OPEN. After landing, `ideate` is re-dispatched.
2. **Ideate re-dispatch (#42):** queued this run via `{"action":"ideate"}`; fires after #102 lands so the hardened `ideator.md` is in effect. Parked candidates Corundum/Tundra/Ravel remain eligible.

## PENDING (in order)
1. **Confirm #102 landed** into `main` (recover step push + integrity guard pass) and pages re-deploy if site content changed (it only changed workflow/agent files, so pages likely no-op).
2. **Ideate resumes (#42):** after #102 lands, the Ideator should post 2-3 fresh candidates against the hardened prompt. If it stalls again, escalate further (deterministic candidate generator).
3. **Next new-project build:** pick from #42 (after Ideator posts) and route research -> architect -> build. Within the 2 new-project PRs/day shipping limit (none merged yet today).
4. **OPEN-PR merge-path `lab` fix:** dispatch `lab` to add a clean open-approved-PR merge step (rebase, branch kept) so future approved PRs merge as "merged" instead of via close-then-recover. Durable improvement.
5. **builder.md hollow-docs `lab` fix** - optional, low priority.

## ISSUES
- **#100 (Resonata project)** - CLOSED by owner (halted). No recovery (directive).
- **#42 (Brainstorm Board)** - OPEN; Ideator fix landing via #102, then re-dispatch `ideate` to resume candidates.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#68 (Obsidian umbrella)** - CLOSED by owner.
- **#98/#96/#94 (runaway/circuit-breaker/no-op)** - CLOSED (guards shipped, PRs #99/#97/#95 merged).

## REVIEWER/TESTER/MODEL STATUS
- Model config: worker workflows `opencode/nemotron-3-ultra-free`; `opencode.json` `hy3-free`/`mimo-v2.5-free`. `origin/main` = `60748e88`.
- PR #102: approved+tested, now landing via `recover` (closed first). #42 preserved.
- PR #101: CLOSED by owner; no action.
- pages.yml: triggers only on PR/workflow_dispatch, not push to main; #102 changes only workflow/agent files, so no pages deploy required (correctly no-op).

## NEXT STEPS
1. Monitor `main` for #102 landing (recover push) + integrity guard; confirm branch preserved.
2. After #102 lands, confirm Ideator re-dispatch posts candidates to #42.
3. Route next new-project build from #42 (research -> architect -> build), respecting 2/day limit.
4. File/dispatch `lab` to fix the open-approved-PR merge gap so future merges are clean.

## OPEN QUESTIONS
- Will #102's recovery push advance `main` and pass the integrity guard? Monitor next run.
- Ideator efficacy post-fix: reliably posts 2-3 candidates? If stalls again, escalate.
- OPEN-PR merge-path gap: route a `lab` pass to merge open approved PRs cleanly.
- builder.md lab (optional): re-engage when convenient.
- Runaway-loop recurrence: none observed; #99 guard holding.
- Single-root `main`: intentional owner recovery (`60748e88`); per directive, no action needed.

- Mae, the Maintainer