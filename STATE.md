# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32484038135, EVENT `created` on PR #93, owner question at 12:53:05Z about an automatic recovery mechanism). **Owner asked for a concrete recovery strategy after the PR #93 closed-PR/orphan incident.** Created issue #112 and dispatched the Lab Engineer to build a self-healing `recover` mechanism (parts A-D). Prism #104 remains BLOCKED on the paid build model (`muse-spark-1.2`); its free-model fix is still in flight.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (PR #93 manually merged by owner as orphan merge `0eb9de0f`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak). BLOCKED on paid build model.
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized, now formalized as issue #112 (Lab Engineer building the mechanism).
- **Owner WILL (12:09:40Z):** "change builder model to `muse-spark-1.2`." Delivered as #109 (MERGED `9aeea30`) but `muse-spark-1.2` is PAID -> billing crash. Correcting to `muse-spark-1.2-contributor-free` (Lab Engineer dispatch in run 32483441284).

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `9aeea30`** (post #109 merge). Build pin = `opencode/muse-spark-1.2` at `opencode.yml:358` -> **BROKEN (paid model, `No payment method`)**. Free tier `muse-spark-1.2-contributor-free` is the correction target.
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Fine.
- **RECOVERY MECHANISM (new, issue #112):** owner asked (PR #93, 12:53:05Z) how the factory can auto-recover a closed-PR/orphan-branch/interrupted-build. Answer: with `gh`+PR/issue powers it is fully automatable; the prior blocker was the "Maintainer cannot open PRs/push branches" rule. Dispatched `lab` on #112 to build: (A) `recover` agent + `recover.yml` triggered by `/oc recover` and auto-detect of a closed build PR whose branch advanced; (B) `recover/<pr>` branch-preservation tag on every build push; (C) scoped Maintainer `recover` exception in `maintainer.md` + `opencode.yml` hardcoded step (continuation PR for in-flight work only, never new projects); (D) `main` orphan-root prevention. When #112's infra PR merges, PR #93-class incidents self-heal with no human.
- **pages.yml:** redeployed cleanly after #109 (run 32483304605).

## IN FLIGHT
1. **PR (build) - Prism (issue #103).** head `0e8c2c5`, docs-only (research/architecture spec). BLOCKED on paid build model (`muse-spark-1.2`). After the Lab Engineer's free-model PR merges, emit `continue`; Builder implements `prism/` (C++) per `prism/docs/architecture.md`, gated on M0 (bit-exact round-trip + corruption-rejection fuzz gate) before optimization. Benchmark Kodak; target under JXL ~3.1 bpp. Then review -> test -> merge.
2. **Lab Engineer model fix (free-model PR, issue #103/#104).** `/oc lab` dispatched run 32483441284 to flip `opencode.yml:358` `opencode/muse-spark-1.2` -> `opencode/muse-spark-1.2-contributor-free` and open a PR. Owner merges (same path as #109). Then `continue` #104.
3. **Lab Engineer recovery mechanism (issue #112).** `/oc lab` dispatched THIS run to build the self-healing `recover` mechanism (parts A-D). Opens its own infra PR; owner merges.

## PENDING (in order)
1. **Lab model fix:** Lab Engineer PR -> owner merge -> `main` build pin free.
2. **Prism build:** `continue` #104; confirm Builder pushes `prism/` C++ and reaches M0 fuzz gate; then review -> test (Kodak vs JXL ~3.1 bpp) -> merge.
3. **Recovery mechanism:** after #112 infra PR merges, verify a simulated closed-PR/orphan recovers automatically; fold the `recover` action into the maintainer decision schema.
4. **#102 wall (CLOSED as of last run):** genuine `git push` `workflows`-scope on `OPENCODE_PAT`; owner to grant scope or merge manually; then close #42.
5. **Board (#42) resume:** after Prism, pick from parked candidates.
6. **`lab.yml` Lab Engineer pin bump (hy3-free):** lower priority reliability item.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build blocked by paid model, fix in flight).
- **#112 (recovery mechanism)** - OPEN; new, this run. Lab Engineer dispatched.
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `9aeea30`. Today's new-project merges: 0/2 (Prism not yet built; #109 was infra).
- PR #104: BLOCKED on paid build model; `continue` deferred until free-model PR merges.
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (nondeterministic no-op risk; escalate to direct edit if this dispatch fails).
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2` = PAID -> fixing to `opencode/muse-spark-1.2-contributor-free`.
- Recovery: no automated `recover` exists yet; being built via #112.

## NEXT STEPS
1. Lab Engineer opens free-model PR (opencode.yml:358 `muse-spark-1.2` -> `muse-spark-1.2-contributor-free`); owner merges.
2. After merge: emit `continue` on #104 so Builder (now free) implements `prism/` through M0 fuzz gate.
3. Lab Engineer builds recovery mechanism (#112): `recover.yml` + `recover` agent + branch-preservation tag + scoped Maintainer `recover` exception + orphan-root prevention; opens infra PR; owner merges.
4. Review -> test (Kodak vs JXL ~3.1 bpp) -> merge Prism.

## OPEN QUESTIONS
- Will `muse-spark-1.2-contributor-free` actually execute + push C++ (i.e., is it agentic), or will we need `nemotron-3-ultra-free` (standing worker pin)?
- Will the #112 `lab` dispatch execute, or no-op on `hy3-free` (requiring direct-edit escalation)?
- After free model lands + `continue`, can the Builder hit M0 fuzz gate and beat JXL 3.1 bpp on Kodak?
- After #112 merges: does a simulated closed/orphan build PR auto-recover into a new open PR with no human action?
- #102: owner to grant `workflows` scope to `OPENCODE_PAT` or merge manually; its `ideate.yml` change still needed for #42.
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer
