# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32484355188, scheduled `maintainer` run, no event payload). **Paid-model wall is DOWN:** PR #111 (free-model fix for #110) MERGED into `main` (`043bd6d`); build pin now `opencode/muse-spark-1.2-contributor-free` (free). Prism #104 is UNBLOCKED and `/oc continue` re-dispatched this run.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (PR #93 closed by owner; orphan merge `0eb9de0f` into main). Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak). Now UNBLOCKED: build agent is free (`muse-spark-1.2-contributor-free`).
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; mechanism being built via issue #112 (Lab Engineer in flight this run).
- **Owner WILL (12:09:40Z):** "change builder model to `muse-spark-1.2`." Delivered as #109 (paid, crashed) then corrected via #110/#111 to `opencode/muse-spark-1.2-contributor-free` (free). Resolved.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `043bd6d`** (post #111 merge). Build pin = `opencode/muse-spark-1.2-contributor-free` (FREE) at `opencode.yml:358` -> wall removed.
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Fine.
- **RECOVERY MECHANISM (issue #112):** owner fired `/oc lab` at 12:57:03Z; a Lab Engineer run (32484363747) is IN PROGRESS building the self-healing `recover` mechanism (parts A-D from the #112 spec). No duplicate dispatch this run. When its infra PR merges, PR #93-class incidents self-heal with no human.
- **pages.yml:** redeployed cleanly after #111.

## IN FLIGHT
1. **PR (build) - Prism (issue #103).** head `b0a83112` (docs-only: research + architecture blueprint). NOW UNBLOCKED. This run re-dispatched `continue` (action in decision.json) so the Builder implements `prism/` C++ (B0 scaffold -> M0 fuzz gate) per `prism/docs/architecture.md`. Branch is NOT orphaned (GitHub compare merge_base_commit `0eb9de0f`; empty local merge-base is the shallow-clone artifact). After code lands: review -> test (Kodak vs JXL ~3.1 bpp) -> merge.
2. **Lab Engineer recovery mechanism (issue #112).** `/oc lab` fired by owner (12:57:03Z); Lab Engineer run IN PROGRESS (32484363747). Will open its own infra PR; owner merges.

## PENDING (in order)
1. **Prism build:** `continue` dispatched this run; confirm Builder pushes `prism/` C++ and reaches M0 fuzz gate; then review -> test -> merge.
2. **Recovery mechanism:** after #112 infra PR merges, verify a simulated closed-PR/orphan recovers automatically; fold the `recover` action into the maintainer decision schema.
3. **#102 wall:** `OPENCODE_PAT` lacks `workflows` scope (blocks `ideate.yml` push). Owner to grant scope or merge manually; then close #42's dependency.
4. **Board (#42) resume:** after Prism, pick from parked candidates.
5. **`lab.yml` Lab Engineer pin bump (hy3-free):** lower-priority reliability item (recent `/oc lab` runs nondeterministic on `hy3-free`).

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build unblocked this run).
- **#112 (recovery mechanism)** - OPEN; Lab Engineer in flight (owner `/oc lab` 12:57:03Z).
- **#110 (model switch to free)** - CLOSED by #111 merge.
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt).
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `043bd6d`. Today's new-project merges: 0/2 (Prism not yet built; #109/#111 were infra).
- PR #104: UNBLOCKED; `continue` re-dispatched this run. Branch NOT orphaned (shared merge-base `0eb9de0f`).
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (wall removed).
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (nondeterministic no-op risk; escalate to direct edit if #112's lab run no-ops).
- Recovery: no automated `recover` exists yet; being built via #112 (in flight).

## NEXT STEPS
1. Builder (via `continue`) implements `prism/` C++ through M0 fuzz gate on PR #104.
2. Review -> test (Kodak vs JXL ~3.1 bpp) -> merge Prism.
3. Lab Engineer completes #112 recovery mechanism; infra PR -> owner merge -> verify self-heal.

## OPEN QUESTIONS
- Will `muse-spark-1.2-contributor-free` actually execute + push C++ (agentic), or will it green-no-op like `hy3-free` did earlier (requiring escalation to `nemotron-3-ultra-free`)?
- After `continue`, can the Builder hit M0 fuzz gate and beat JXL 3.1 bpp on Kodak?
- Will the #112 `lab` run (in flight) deliver the `recover` mechanism, or no-op on `hy3-free` (requiring direct-edit escalation)?
- After #112 merges: does a simulated closed/orphan build PR auto-recover into a new open PR with no human action?
- #102: owner to grant `workflows` scope to `OPENCODE_PAT` or merge manually; its `ideate.yml` change still needed for #42.
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer
