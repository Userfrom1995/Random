# STATE - Random factory checkpoint
- **Updated:** 2026-08-22 (maintainer run 32591447328, ~18:40Z scheduled). Re-survey confirms: PR #118 head `300ffa7cbc6c45b580fd3558d336443b81cf6919` (B5.39, 11.029 bpp, byte-exact, harness ~495s), **a `continue` build IS still in flight** (opencode run `32587774459`, `in_progress` since 17:27:16Z from owner's `/oc continue`). This scheduled run wrote an EMPTY decision list (no duplicate while a build drives the branch; no target event).

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; docs cleaned by merged PR #116). Obsidian is the current codec in `main`; last confirmed REAL-Kodak baseline **9.5209 bpp**. #68 (Obsidian umbrella) is now CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation in flight (issue #117, PR #118). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71). The merge gate is tied to the ACTUAL project goal, not any iteration/round limit.
- **Iteration limit LIFTED (2026-08-22T14:51Z):** owner removed the 20-round/iteration cap and said "keep working". The circuit-breaker budget is now unlimited by owner action. A further main commit ("Remove halt/breaker on factory pipeline", `91c8707`) formally DELETED the breaker entirely, so the loop may run unbounded without manual re-pings.
- **One-PR rule + NEVER delete PR branches:** satisfied.
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Quality-gate directive:** quality gates are the ONLY merge criteria.
- **(2026-08-22T04:48Z):** infra/workflow changes MUST be delegated to the Lab Engineer, never the Fixer. Enforced in reviewer.md (committed 770a756); `lab.yml` routes `/oc lab` to Lab Engineer for `.github/agents/*.md` edits only.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `91c87078919e17f7244a659b2cbf5552c4052502`** (owner commit "Remove halt/breaker on factory pipeline"). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/117-prism-m1-m4-optimization` = `300ffa7` shares M0 ancestry (NOT orphan).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** production deploy succeeded (main). PR #118 preview deploy is `action_required` (env approval, not the production path).
- **CIRCUIT BREAKER: REMOVED** (main commit `91c8707`). The auto-guard no longer exists; the loop runs unbounded. This resolves the prior escalation's option (c).
- **WORKFLOW-FILE PUSH WALL (unchanged, now non-blocking):** #120 CLOSED by owner. `opencode.yml` still lacks `workflows: write` and a `lab` job, but the reviewer.md auto-guard (committed 770a756) rewrites any misrouted fix/continue on infra PRs to `lab`, so the orchestration-rule fix is effectively enforced. Future workflow-file edits remain an OWNER-action path.

## IN FLIGHT
- **Prism M1-M4 (issue #117, PR #118, branch `opencode/117-prism-m1-m4-optimization`):** head `300ffa7` (B5.39, **11.029 bpp**, byte-exact, harness ~495s). **A `continue` build is in flight (opencode run `32587774459`, `in_progress` since 17:27:16Z from owner's `/oc continue` 17:27:13Z).** The 18:40Z scheduled maintainer run did NOT dispatch a duplicate.
  - **Trajectory correction (vs earlier runs):** earlier snapshots claimed the bank was "mathematically saturated at 11.059". That was premature. The PREDICTOR bank is saturated (16/16 nibble 0..15, per-plane top10-11, block top12-13, selective-16 thr55-60 top13-14, color top8 - all neutral), BUT the RESIDUAL ENTROPY MODEL (ResDiff context count) was only at 352-704 and is now proven EXPANDABLE with real gains: B5.38 (704-context orientation split, -0.16%, -20944 bytes) and B5.39 (2816-context flatness split, -0.11%, -14449 bytes). Total progress from 11.29 baseline is ~2.3%. The loop is productive, NOT converged.
  - **B7 Squeeze + MA-tree greedy split (depth 6, leaves 16-32, mandatory `llc_class`/`sibling_class`) STILL NOT genuinely built** - B5.38/B5.39 are entropy-model context expansions, distinct from the structural Squeeze+MA-tree closure. B6 5/3 lifting is done and **inert** (+0.8% never-expand, kept disabled). B7 remains the ONLY proven >10% closure path to JXL 8.71; context-splitting alone is unlikely to close the remaining ~21% gap. B7 has been SCAFFOLDED (B5.33) but the real greedy split was never built.
  - **Merge gate NOT met** (11.029 vs 8.71 JXL, gap 2.32 / ~21%). Held until M3<8.71 bit-exact + Tester approval.

## PENDING (in order)
   1. **Reach the JXL gate (M3 < 8.71).** Entropy context-splitting is still yielding ~0.1% gains (now at 2816 contexts); keep grinding it, but the ~21% gap needs the real B7 Squeeze+MA-tree greedy split (mandatory `llc_class`/`sibling_class`). Since plain `continue` follows the progress file's next B5.x step, a DIRECT narrow B7 instruction on PR #118 from the owner is the reliable trigger for B7. The Builder should be told: skip further B5.x widening, build the MA-tree greedy split now.
   2. **Once M3 < 8.71 bit-exactly:** fire Reviewer -> Tester before ANY merge.
   3. **ORCHESTRATION RULE FIX:** effectively landed (reviewer.md auto-guard). Optional fixer.md hardening parked.
   4. **PR #119:** CLOSED by owner (redundant; target #98 CLOSED). Resolved.
   5. **Silent-stall mitigation:** now moot - owner removed the iteration cap and the breaker; loop resumes normally.

## ISSUES
- **#68 (Obsidian umbrella)** - CLOSED.
- **#103 (Prism)** - CLOSED (merged #104); M1-M4 via #117 + PR #118.
- **#117 (Prism M1-M4)** - OPEN (tracking; goal-tied merge gate). Held open until M3 < 8.71 bit-exactly.
- **#112 (auto PR recovery)** - CLOSED (shipped #114).
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor daily summary.
- **#98 (runaway /oc fix retry loop)** - CLOSED (PR #99); PR #119 now CLOSED too.
- **#119 ([Infra] Lab update for #70)** - CLOSED by owner (redundant).
- **#120 (Audit: workflows: write missing)** - CLOSED by owner (reviewer.md auto-guard committed instead; workflow-file push wall remains owner-action).

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `91c87078919e17f7244a659b2cbf5552c4052502`.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE.
- **Lab Engineer:** reachable via `lab.yml` (`/oc lab`) for PROMPT edits only; CANNOT push workflow `.yml` (no workflows: write).
- **Circuit breaker:** REMOVED (owner commit `91c8707`).

## NEXT STEPS
   1. **Build in flight (`32587774459`)** resumes the loop; if it lands another entropy context-split, the trajectory continues productively. If the owner wants B7 specifically, they should post a direct narrow B7 instruction on PR #118.
   2. If a build clears the gate (M3 < 8.71 bit-exactly), fire Reviewer -> Tester before any merge.
   3. ORCHESTRATION FIX: considered landed (reviewer.md auto-guard). Optional fixer.md hardening parked.
   4. PR #119: resolved (CLOSED).

## OPEN QUESTIONS
- Will the in-flight `continue` land as another entropy context-split (B5.x) or finally attempt the real B7 MA-tree greedy split (mandatory `llc_class`/`sibling_class`)? Context-splitting is still productive but the ~21% JXL gap needs B7.
- When/if a build clears the gate (M3 < 8.71 bit-exactly), fire Reviewer -> Tester before ANY merge.
- PR #119: resolved (CLOSED).
- Stray `pending` opencode run `32587781454` (no jobs) observed alongside the in-flight build; harmless but worth noting if it ever picks up a competing build job.

- Mae, the Maintainer
