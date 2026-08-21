# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32460787127, EVENT `created` on issue #42, owner directive: build the Obsidian-upgrade codec). `main` = `60748e88` (owner orphan root). PR #102 (Ideator-stall hardening) is STILL orphaned (never landed; its recover failed in run 32460341918) - re-emitted `recover`. Prism (#103) opened and routed to the Researcher.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak (PNG + WebP MET; JPEG XL 8.71 gate lifted by owner pivot). Issue #68 CLOSED.
- **NEXT PRIORITY (2026-08-21, owner, overrides board):** build the **Obsidian-upgrade image codec** - support all major input formats, aim to beat JPEG XL. The Ideator posted "Prism" (#103) as exactly this; it is now the active project. No other new ideas until Prism is competitive.
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved on close.
- **Maintainer sovereign-recovery directive:** `60748e88` empowers `recover` of orphaned/closed PRs; main must never become a divergent/orphan ROOT.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `60748e88`** (orphan root from PR #93). Contains obsidian + all prior projects.
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`; `opencode.json` `hy3-free`/`mimo-v2.5-free` (free).
- **OPEN-PR MERGE-PATH GAP (durable, logged):** this workflow only lands CLOSED PRs via `recover`; OPEN approved+tested PRs have no clean merge step. Worked around for #102 (close-then-recover) but that recover never executed. Durable `lab` fix recommended.
- **WORKFLOW-PUSH PERMISSION WALL:** the `opencode` GitHub App cannot push `.github/workflows/*` (needs `workflows` scope). Lab PRs that touch workflow files fail to push; only the owner PAT-backed `recover` step can land them. Logged; needs owner action or PAT scope grant.

## IN FLIGHT
1. **PR #102 - `[Infra] Lab update for #42` (Ideator-stall hardening).** CLOSED, branch `opencode/issue42-20260821070030` preserved, head `f58834b4` NOT in main (merge-base = `60748e88`, clean merge possible). Re-emitted `recover` this run so the PAT step lands it. Body has NO `Closes #42`, so #42 stays OPEN.
2. **Prism (issue #103) - Obsidian-upgrade codec.** Opened this run. Routed `research` -> (architect) -> build. Researcher will carry Obsidian lessons forward and design learned predictors + LZP. Not yet building.
3. **Ideator batch (07:55Z) on #42:** posted Prism, Penumbra (OCaml path tracer), Vellum (Crystal JIT lang). Prism is selected; the others stay as parked candidates.

## PENDING (in order)
1. **Confirm #102 lands** via `recover` (push + integrity guard). If it fails again on workflow-permission, escalate to owner (PAT scope) or `lab` with owner PAT.
2. **Prism research -> architect -> build:** keep the loop benchmark-driven on Kodak; document every iteration's mean bpp; target under JPEG XL ~3.1 bpp (Obsidian stopped at 9.52).
3. **OPEN-PR merge-path `lab` fix:** add a clean open-approved-PR merge step (rebase, branch kept) so future merges are clean instead of close-then-recover.
4. **Board (#42) resume:** after Prism, pick from parked candidates (Corundum/Tundra/Ravel/Penumbra/Vellum) - but no new projects until Prism competitive.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (research dispatched).
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; Ideator batch posted, Prism selected.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#68 (Obsidian)** - CLOSED by owner.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `60748e88`. Today's new-project merges: 0/2 (clear for Prism).
- PR #102: approved+tested, re-landing via `recover`. #103: research dispatched.
- pages.yml: triggers only on PR/workflow_dispatch, not push; #102 changes only workflow/agent files (no pages redploy needed on land).

## NEXT STEPS
1. Monitor `main` for #102 landing (recover push) + integrity guard; confirm branch preserved.
2. Track Prism research output; route to architect, then build; benchmark on Kodak each iteration.
3. File/dispatch `lab` to fix the open-approved-PR merge gap (durable).

## OPEN QUESTIONS
- Will #102's `recover` finally advance `main` this run, or hit the workflow-permission wall again? If wall, escalate to owner.
- Prism: can learned context-mixing + LZP close the gap from 9.52 -> under JXL 3.1 bpp on Kodak? Researcher to assess feasibility first.
- OPEN-PR merge-path gap: route a `lab` pass.
- builder.md lab (optional): deferred.
- Runaway-loop recurrence: none; #99 guard holding.
- Single-root `main`: intentional owner recovery; no action.

- Mae, the Maintainer
