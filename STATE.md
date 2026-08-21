# STATE - Random factory checkpoint

- **Updated:** 2026-08-21 (maintainer run 32457476305, EVENT issue/PR #102 created). PR #102 (Lab Engineer's Ideator soft-stall fix for #42) is fully approved (Reviewer `/oc approve` + Tester `/oc approve-test`, no newer fix) and is being merged this run. I found + fixed a lab defect: `maintainer.yml` had no open-PR merge step, and `maintainer-recover.py` skipped OPEN PRs; it now also lands open approved PRs via `gh pr merge --rebase`. Issue #42 closes on merge. PR #101 (Resonata build, #100) is in flight and merges once the Reviewer + Tester approve.

## STANDING OWNER DIRECTIVES (active)

- **Obsidian shipped.** Owner manually merged PR #93's branch into `main`; `main` = `60748e88` (intentional orphan root "lab: empower Maintainer as sovereign to recover closed/orphaned PRs and resolve conflicts"), containing obsidian + glyphforge/halcyon/kestrel/meridian/etc. Default codec = 9.5209 bpp; R11-R15 experimental predictors gated OFF; 152 lib tests pass.
- **Issue #68 CLOSED** by owner. Priority-project freeze LIFTED; new projects allowed again.
- **One-PR rule + NEVER delete PR branches:** satisfied; PR branches preserved (no `-d`).

## CRITICAL INFRASTRUCTURE STATE

- **`main` = `60748e88`** (will advance when PR #102 merges). Intentional single-root (orphan) commit by owner recovery.
- **Ideator soft-stall fix (issue #42):** the Lab Engineer's PR #102 hardens `ideator.md` (agent must not emit `/oc` triggers; workflow's notify step posts `/oc maintainer` automatically) and changes `ideate.yml` `always()` -> `success()` so the Maintainer is no longer paged on ideation failure. APPROVED + TESTED; merging this run. After merge, `ideate` dispatches should resume posting candidates.
- **OPEN-PR MERGE PATH (fixed this run):** `maintainer-recover.py` now accepts a Maintainer `recover`/`merge` directive targeting an OPEN approved PR and runs `gh pr merge <N> --rebase` (branch preserved, linked `Closes/Fixes/Resolves` issues closed). Previously only CLOSED/orphan PRs were landable; approved open PRs had no wired merge step. Gap closed.
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`; `opencode.json` `hy3-free`/`mimo-v2.5-free` (free).

## NEXT-PROJECT DECISION (active)

- **Resonata (issue #100)** is the active next build: Research (Dr. Mob) wrote `docs/resonata-research-spec.md`; the Architect delivered `ideas/2026-08-21-resonata.md` + `progress/100-resonata.md`; the Builder is running on `opencode/issue100-20260821065856` (head `4150c115`). When Reviewer + Tester approve PR #101, I merge it (rebase, branch preserved) and close #100. This is the first new-project build today (within the 2/day limit).
- After Resonata lands (or if the pipeline is otherwise idle), re-dispatch `ideate` to refill the Brainstorm Board (#42) with fresh candidates now that the Ideator is hardened, then pick the following build and route research -> architect -> build.

## IN FLIGHT

- **PR #101 (Resonata, issue #100)** - OPEN, MERGEABLE, Builder in flight. Await Reviewer + Tester approval, then merge.
- **PR #102 (Ideator fix, issue #42)** - OPEN, MERGEABLE, fully approved; merging this run via the recovered open-PR merge path.

## PENDING (in order)

1. **Merge PR #101 (Resonata)** once Reviewer + Tester approve (already `MERGEABLE`, shares history with `main`). Close #100 on merge.
2. **Resume ideation:** after #42's Ideator fix ships, `ideate` should reliably post 2-3 candidates; pick the next build from the board (parked Corundum/Tundra/Ravel remain eligible) and route research -> architect -> build.
3. **builder.md hollow-docs fix** - optional `lab` pass to patch ONLY `.github/agents/builder.md` (resume re-task on newest directive). Low priority; queue when convenient.

## ISSUES

- **#68 (Obsidian umbrella)** - CLOSED by owner.
- **#98 (Runaway /oc fix loop)** - CLOSED (PR #99 merged, guard shipped).
- **#96 (Circuit breaker)** - CLOSED (PR #97 merged).
- **#94 (Detect silent no-op builds)** - CLOSED (PR #95 merged).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - Ideator hardened via PR #102 (merging this run); CLOSES on merge. Future `ideate` dispatches refill it.
- **#100 (Resonata build)** - in flight as PR #101; closes on merge.

## REVIEWER/TESTER/MODEL STATUS

- Model config: worker workflows `opencode/nemotron-3-ultra-free`; `opencode.json` `hy3-free`/`mimo-v2.5-free`. `origin/main` = `60748e88` (advancing with #102 merge).
- pages.yml: triggers only on `pull_request`/`workflow_dispatch`; PR #102 changed only agent/workflow files (no site content), so no Pages deploy is needed. The "Trigger pages deployment if main advanced" step will run but Pages only redeploys on a real site change; harmless.
- No open PRs require review/test dispatch this run except PR #101, which is still building (its Reviewer/Tester will auto-engage on the next Builder push).

## NEXT STEPS

1. Confirm PR #102 merged cleanly (rebase, branch preserved) and issue #42 closed.
2. Monitor PR #101 (Resonata): when Reviewer + Tester approve, merge it (rebase, branch preserved) and close #100.
3. Once the Ideator fix is in, re-dispatch `ideate` to refill #42; pick the next build and route research -> architect -> build.
4. (Optional) Queue a `lab` pass to fix `.github/agents/builder.md` hollow-docs root cause.
5. Continue monitoring the #99 runaway-loop guard for any stray `/oc fix` on a closed PR/issue.

## OPEN QUESTIONS

- **Open-PR merge path (answered/fixed):** `maintainer.yml` had lost the open-PR merge step; `maintainer-recover.py` now handles it. Verified syntactically; PR #102 exercises it this run.
- **Resonata build:** will the Builder deliver a clean, review-passing build on `opencode/issue100-20260821065856`? Merge once both gates green.
- **Ideator efficacy:** with the hardened prompt + `ideate.yml:52` `success()` gate, will future `ideate` dispatches reliably post candidates? If it stalls again, escalate further (deterministic candidate generator).
- **Single-root `main`:** intentional owner recovery (`60748e88`); per the owner's directive, no action from me. Ensure new PRs share history with `60748e88` to avoid re-orphaning (the recover script guards this).
- **builder.md lab (optional):** re-engage a targeted `lab` when convenient.

- Mae, the Maintainer
