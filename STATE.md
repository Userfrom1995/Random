# STATE - Random factory checkpoint
- **Updated:** 2026-08-22 (maintainer run 32566341968, owner `/oc maintainer` re-ping on PR #118, 09:57Z). Fresh survey confirms: PR #118 head `8e5a5659fa5c5e3cb4356f01a42b15452e929b04` (B5.36, 11.059 bpp, byte-exact, harness ~365s), **no `continue` build in flight** (last real build `32564122603` COMPLETED landing B5.36 at 09:57:52Z). This run **escalated instead of looping**: it did NOT dispatch another `continue`. Per the standing escalate-if-deferred rule, because B5.36 (launched by the prior run's B7-redirect) is yet another 0% scaffold that explicitly did NOT build the real B7 MA-tree greedy split, the loop is halted pending an owner decision.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; docs cleaned by merged PR #116). Obsidian is the current codec in `main`; last confirmed REAL-Kodak baseline **9.5209 bpp**. #68 (Obsidian umbrella) is now CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation in flight (issue #117, PR #118). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71). The merge gate is tied to the ACTUAL project goal, not any iteration/round limit; never merge incomplete work.
- **One-PR rule + NEVER delete PR branches:** satisfied.
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Quality-gate directive:** quality gates are the ONLY merge criteria.
- **(2026-08-22T04:48Z):** infra/workflow changes MUST be delegated to the Lab Engineer, never the Fixer. Enforced in reviewer.md (committed 770a756); `lab.yml` routes `/oc lab` to Lab Engineer for `.github/agents/*.md` edits only.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `770a7567c147fbd00373691c7a59d8000f992b87`** (last commit: "reviewer: route infrastructure PRs to the Lab Engineer and enforce it"). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/117-prism-m1-m4-optimization` = `8e5a565` shares M0 ancestry (NOT orphan).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** production deploy succeeded (main). PR #118 preview deploy is `action_required` (env approval, not the production path).
- **WORKFLOW-FILE PUSH WALL:** #120 CLOSED by owner. `opencode.yml` still lacks `workflows: write` and a `lab` job, but the reviewer.md auto-guard (committed 770a756) rewrites any misrouted fix/continue on infra PRs to `lab`, so the orchestration-rule fix is effectively enforced. Future workflow-file edits remain an OWNER-action path.
- **CIRCUIT-BREAKER (36/20, halts auto-loop):** auto-guard tripped repeatedly and is now HARD-halted. This run did NOT add to it (no `continue` dispatched).

## IN FLIGHT
- **Prism M1-M4 (issue #117, PR #118, branch `opencode/117-prism-m1-m4-optimization`):** head `8e5a565` (B5.36, 11.059 bpp, byte-exact, harness ~365s). **No build in flight.** The B5.x trajectory is CONVERGED: B5.28-B5.36 = 9 consecutive ~0% builds.
  - **Predictor bank FULLY SATURATED** (16/16 nibble 0..15, per-plane top10, block top12, selective-16 thr55 top13, color top8 - all neutral). B6 5/3 lifting done and **inert** (+0.8% never-expand, kept disabled). B7 Squeeze + MA-tree greedy split has been SCAFFOLDED three times (B5.33 per-band, B5.35 mode5, B5.36 leaf-activity MA-tree LITE) but the real greedy split with mandatory `llc_class`/`sibling_class` has NEVER been built. Each scaffold ends "infrastructure ready for B7" (net 0%).
  - **The prior run's explicit B7-redirect (09:08Z) was DEFIED** - B5.36 shipped instead of B7. Per rule, this run escalated (no `continue`).
  - **Merge gate NOT met** (11.059 vs 8.71 JXL, gap 2.35 / ~21%). Held until M3<8.71 bit-exact + Tester approval.

## PENDING (in order)
1. **OWNER DECISION (this run's escalation):** choose (a) bounded Architect+Builder on the REAL B7 MA-tree greedy split, (b) repivot/close #117 publishing partial baseline, or (c) raise the circuit-breaker budget. The loop is paused until then.
2. **If (a):** route `research`->`architect`->`build` with a hard "no B5.x widening" constraint; one bounded attempt, not the open loop.
3. **If (b):** publish Prism 11.059 bpp baseline (M0 bit-exact, PNG PASS, reproducible Kodak CSVs + architecture-m1-m4.md) and close #117 with explanation.
4. **CIRCUIT-BREAKER BUDGET:** raise only if owner chooses (c).
5. **Prism M1-M4 (PR #118):** once B7 is genuinely attempted, HOLD merge until M3 < 8.71 bit-exactly (and Reviewer -> Tester fired).
6. **ORCHESTRATION RULE FIX:** effectively landed (reviewer.md auto-guard). Optional fixer.md hardening parked.
7. **PR #119:** CLOSED by owner (redundant; target #98 CLOSED). Resolved.
8. **Silent-stall mitigation:** suspended this run in favor of escalation.

## ISSUES
- **#68 (Obsidian umbrella)** - CLOSED.
- **#103 (Prism)** - CLOSED (merged #104); M1-M4 via #117 + PR #118.
- **#117 (Prism M1-M4)** - OPEN (tracking; goal-tied merge gate). At risk of repivot only if owner chooses (b) or B7 fails to move the gap.
- **#112 (auto PR recovery)** - CLOSED (shipped #114).
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor daily summary.
- **#98 (runaway /oc fix retry loop)** - CLOSED (PR #99); PR #119 now CLOSED too.
- **#119 ([Infra] Lab update for #70)** - CLOSED by owner (redundant).
- **#120 (Audit: workflows: write missing)** - CLOSED by owner (reviewer.md auto-guard committed instead; workflow-file push wall remains owner-action).

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `770a7567c147fbd00373691c7a59d8000f992b87`.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE.
- **Lab Engineer:** reachable via `lab.yml` (`/oc lab`) for PROMPT edits only; CANNOT push workflow `.yml` (no workflows: write).
- **Circuit breaker:** 36/20, HARD-halted. This run did not add to it.

## NEXT STEPS
1. **AWAIT OWNER DECISION on PR #118 escalation:** (a) bounded B7, (b) repivot/close #117, (c) raise breaker. No `continue` issued this run.
2. If (a): dispatch `research`/`architect`/`build` chain scoped to real B7 greedy split, no B5.x widening.
3. If (b): document and close #117.
4. ORCHESTRATION FIX: considered landed (reviewer.md auto-guard). Optional fixer.md hardening parked.
5. PR #119: resolved (CLOSED).

## OPEN QUESTIONS
- Will the owner authorize a real B7 attempt (a), or is it time to publish the partial baseline and repivot (b)? My recommendation: (a) as one bounded shot, because B7 is genuinely untested; (b) is defensible if the architecture hypothesis is judged weak.
- If B7 is genuinely built and the gap remains ~unchanged (~21% needed for M3), should #117 be repivoted and the partial work published?
- When/if the build stabilizes at/under the gate (M3 < 8.71 bit-exactly), fire Reviewer -> Tester before ANY merge.
- PR #119: resolved (CLOSED).

- Mae, the Maintainer
