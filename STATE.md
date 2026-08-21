# STATE - Random factory checkpoint

- **Updated:** 2026-08-21 (maintainer run 32457255483, EVENT `created` on PR #101, owner `/oc maintainer` at 07:07:22Z). Resonata (issue #100) is now a live build: research spec + architect blueprint committed on PR #101, Builder running. The Ideator-stall escalation (issue #42) is also in flight as PR #102 (Lab Engineer).

## STANDING OWNER DIRECTIVES (active)

- **Obsidian shipped.** Owner manually merged PR #93 into `main` as orphan root `60748e88` ("lab: empower Maintainer as sovereign to recover closed/orphaned PRs and resolve conflicts"), containing obsidian (128 files) + all prior projects. Default codec = 9.5209 bpp; R11-R15 experimental predictors gated OFF; 152 lib tests pass.
- **Issue #68 CLOSED** by owner. Priority-project freeze LIFTED; new projects allowed again.
- **One-PR rule + NEVER delete PR branches:** satisfied; PR #93 CLOSED, branch preserved (no `-d`). Runaway-loop guard shipped (PRs #95/#97/#99) holds.
- **Maintainer sovereign-recovery directive:** `60748e88` explicitly empowers the Maintainer to recover orphaned/closed PRs via `recover` and resolve conflicts. main must never become a divergent/orphan ROOT; all advances stay descendants of the prior tip.

## CRITICAL INFRASTRUCTURE STATE

- **`main` = `60748e88`** - intentional single-root (orphan) commit by the owner's recovery. Contains obsidian + glyphforge/halcyon/kestrel/meridian/etc.
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`; `opencode.json` `hy3-free`/`mimo-v2.5-free` (free).
- **Runaway-loop guard (PR #99):** holds - no stray `/oc fix` on closed PRs/issues observed this run.

## IN FLIGHT

1. **PR #101 - Resonata build (issue #100).** OPEN, head `4150c1157d424d1b8e6a1c260d3086aeafc3dc47`, base `main`. Shares history with `main` (merge-base = `60748e88`) -> clean rebase-merge available. Research spec + architect blueprint committed. Builder triggered by owner `/oc build this`, run `32457255591` PENDING/in-progress. No review/test approval yet. Pages preview staging at `/preview/pr-101/`.
2. **PR #102 - `[Infra] Lab update for #42` (Ideator-stall escalation from run 32456311942).** OPEN, head `f0b4cbfbc97d0e9c17c773148942b1c4245b253f`, base `main`. Lab Engineer running (opencode run `32457295801` in_progress) to harden `ideator.md` (always post 2-3 candidates) + gate `ideate.yml` notify step. No review/test approval yet.

## PENDING (in order)

1. **Resonata build (PR #101):** await Builder push -> Reviewer auto-engages -> on `/oc approve`, Tester auto-engages -> on `/oc approve-test`, Maintainer merges (`--rebase`, branch kept), closes #100.
2. **Ideator fix (PR #102):** await Lab Engineer -> Reviewer -> Tester -> merge; then re-dispatch `ideate` so the Brainstorm board (issue #42) resumes feeding candidates (parked Corundum/Tundra/Ravel remain eligible).
3. **builder.md hollow-docs fix** - optional `lab` pass (fix ONLY `.github/agents/builder.md`). Low priority; queue when convenient.
4. **Next new-project build:** after Ideator fixed, pick from #42 and route research -> architect -> build.

## ISSUES

- **#100 (Resonata project)** - OPEN; built via PR #101.
- **#42 (Brainstorm Board)** - OPEN; Ideator fix in flight via PR #102.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#68 (Obsidian umbrella)** - CLOSED by owner.
- **#98/#96/#94 (runaway/circuit-breaker/no-op)** - CLOSED (guards shipped, PRs #99/#97/#95 merged).

## REVIEWER/TESTER/MODEL STATUS

- Model config: worker workflows `opencode/nemotron-3-ultra-free`; `opencode.json` `hy3-free`/`mimo-v2.5-free`. `origin/main` = `60748e88`.
- No PR requires merge/review/test from me this run (both in-flight builds are pre-approval).
- pages.yml: PR #101 changed doc/idea/progress files + will add build output; preview staged at `/preview/pr-101/`. Production deploy only on merge to `main`.

## NEXT STEPS

1. Monitor PR #101: on Builder completion, confirm Reviewer + Tester auto-trigger; merge when both green; close #100.
2. Monitor PR #102: merge the Ideator fix when approved; then re-dispatch `ideate` to resume the Brainstorm board.
3. (Optional) Queue `lab` pass to fix `.github/agents/builder.md` hollow-docs root cause.

## OPEN QUESTIONS

- **Resonata build scope:** the Builder is compiling the native-testable `core/` + WASM export first (per blueprint); will the full `ui/` AudioWorklet instrument ship in this PR or a follow-up? The blueprint lists it; verify the Builder delivers a coherent, testable core before any UI bloat.
- **Ideator fix efficacy:** will PR #102 make the Ideator reliably post 2-3 candidates? If it stalls again post-fix, escalate further (deterministic candidate generator or ideate-workflow rewrite).
- **builder.md lab (optional):** re-engage a targeted `lab` when convenient.
- **Runaway-loop recurrence:** none observed; #99 guard holding.
- **Single-root `main`:** intentional owner recovery (`60748e88`); per directive, no action needed.

- Mae, the Maintainer
