# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32483441284, event `created` on issue #104, owner `/oc continue`/`/oc maintainer` 12:45Z). **Prism #104 is BLOCKED by a paid build model** (`opencode/muse-spark-1.2`, no `-free` suffix) that throws `APIError: No payment method`. Lab Engineer dispatched to switch it to the free `opencode/muse-spark-1.2-contributor-free`. `continue` deferred until that lands.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak).
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run.
- **Owner WILL (12:09:40Z):** "change builder model to `muse-spark-1.2`, open a pr for it." DONE as PR #109 (MERGED 12:43Z, `9aeea30`) but `muse-spark-1.2` is PAID -> billing crash. Now correcting to its free tier `muse-spark-1.2-contributor-free`.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `9aeea30`** (post #109 merge). BUILD pin now `opencode/muse-spark-1.2` at `opencode.yml:358` -> **BROKEN (paid model, no billing)**. Must become `opencode/muse-spark-1.2-contributor-free`.
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine; only the workflow `model:` input is paid.
- **MODEL SWITCH CORRECTION:** Lab Engineer dispatched this run (`/oc lab` on #104) to flip `opencode.yml:358` `opencode/muse-spark-1.2` -> `opencode/muse-spark-1.2-contributor-free` and open a PR. Owner merges (same path as #109). Then `continue` #104.
- **pages.yml:** redeployed cleanly after #109 (run 32483304605), benign.

## IN FLIGHT
1. **PR (build) - Prism (issue #103).** head `0e8c2c5`, docs-only (research/architecture spec). Blocked on paid build model. After the Lab Engineer's free-model PR merges, emit `continue`; Builder implements `prism/` (C++) per `prism/docs/architecture.md`, gated on M0 (bit-exact round-trip + corruption-rejection fuzz gate) before optimization. Benchmark Kodak; target under JXL ~3.1 bpp. Then review -> test -> merge.
2. **Lab Engineer model fix (new infra PR, issue #103/#104).** `/oc lab` dispatched this run to switch build pin to `opencode/muse-spark-1.2-contributor-free`. Risk: `lab.yml` still pins Lab Engineer on `opencode/hy3-free` (nondeterministic no-op). If it no-ops, escalate to direct edit of `opencode.yml:358` (emergency model-management policy).

## PENDING (in order)
1. **Lab model fix:** Lab Engineer PR -> owner merge -> `main` build pin free.
2. **Prism build:** `continue` #104; confirm Builder pushes `prism/` C++ and reaches M0 fuzz gate; then review -> test (Kodak vs JXL ~3.1 bpp) -> merge.
3. **#102 wall (CLOSED as of last run):** genuine `git push` `workflows`-scope on `OPENCODE_PAT`; owner to grant scope or merge manually; then close #42.
4. **Board (#42) resume:** after Prism, pick from parked candidates.
5. **`recover.py` hardening / `lab.yml` Lab Engineer pin bump:** lower priority, not blocking Prism.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build blocked by paid model, fix in flight).
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `9aeea30`. Today's new-project merges: 0/2 (Prism not yet built; #109 was infra).
- PR #104: BLOCKED on paid build model; `continue` deferred until free-model PR merges.
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (nondeterministic no-op risk; escalate to direct edit if this dispatch fails).
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2` = PAID -> fixing to `opencode/muse-spark-1.2-contributor-free`.

## NEXT STEPS
1. Lab Engineer opens free-model PR (opencode.yml:358 `muse-spark-1.2` -> `muse-spark-1.2-contributor-free`); owner merges.
2. After merge: emit `continue` on #104 so Builder (now free) implements `prism/` through M0 fuzz gate.
3. Review -> test (Kodak vs JXL ~3.1 bpp) -> merge Prism.

## OPEN QUESTIONS
- Will `muse-spark-1.2-contributor-free` actually execute + push C++ (i.e., is it agentic), or will we need `nemotron-3-ultra-free` (standing worker pin)?
- Will this `/oc lab` dispatch execute, or no-op on `hy3-free` (requiring direct edit escalation)?
- After free model lands + `continue`, can the Builder hit M0 fuzz gate and beat JXL 3.1 bpp on Kodak?
- #102: owner to grant `workflows` scope to `OPENCODE_PAT` or merge manually; its `ideate.yml` change still needed for #42.
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer
