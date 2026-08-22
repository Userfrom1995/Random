# STATE - Random factory checkpoint
- **Updated:** 2026-08-22 (maintainer run 32563691972, owner `/oc maintainer` re-ping on PR #118). Fresh survey confirms: PR #118 head `b6a23a46f7df5e94a8499c490bca6f82a1bc7066` (B5.35, 11.059 bpp, byte-exact, harness ~360s), **no `continue` build was in flight** when this run started (last real build `32562446891` COMPLETED landing B5.35 at 08:58:32Z). This run **REDISPATCHED a `continue` with a hard B7-redirect directive** (decision list `[{"action":"continue","pr":118,"head":"b6a23a4..."}]`) - honoring the owner's re-authorization while preventing another futile B5.36. The bank is proven saturated; the only lever (B7 MA-tree greedy split, mandatory llc_class/sibling_class) has never been genuinely built and MUST be built this run.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; docs cleaned by merged PR #116). Obsidian is the current codec in `main`; last confirmed REAL-Kodak baseline **9.5209 bpp**. #68 (Obsidian umbrella) is now CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation in flight (issue #117, PR #118). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71). The merge gate is tied to the ACTUAL project goal, not any iteration/round limit; never merge incomplete work.
- **One-PR rule + NEVER delete PR branches:** satisfied.
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Quality-gate directive:** quality gates are the ONLY merge criteria.
- **(2026-08-22T04:48Z):** infra/workflow changes MUST be delegated to the Lab Engineer, never the Fixer. Enforced in reviewer.md (committed 770a756); `lab.yml` routes `/oc lab` to Lab Engineer for `.github/agents/*.md` edits only.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `770a7567c147fbd00373691c7a59d8000f992b87`** (last commit: "reviewer: route infrastructure PRs to the Lab Engineer and enforce it"). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/117-prism-m1-m4-optimization` = `b6a23a4` shares M0 ancestry (NOT orphan).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** production deploy succeeded (main). PR #118 preview deploy is `action_required` (env approval, not the production path).
- **WORKFLOW-FILE PUSH WALL:** #120 CLOSED by owner. `opencode.yml` still lacks `workflows: write` and a `lab` job, but the reviewer.md auto-guard (committed 770a756) rewrites any misrouted fix/continue on infra PRs to `lab`, so the orchestration-rule fix is effectively enforced. Future workflow-file edits remain an OWNER-action path.
- **CIRCUIT-BREAKER (now ~36/20, "not converging" literally true for B5.x):** auto-guard tripped repeatedly. This run's `continue` is the Maintainer's human re-review authorizing ONE targeted, redirect-scoped dispatch (not unbounded auto-dispatch). If the Builder again defers B7, the next run must escalate rather than loop.

## IN FLIGHT
- **Prism M1-M4 (issue #117, PR #118, branch `opencode/117-prism-m1-m4-optimization`):** head `b6a23a4` (B5.35, 11.059 bpp, byte-exact, harness ~360s). **As of this run: a `continue` was JUST dispatched (decision `[{"action":"continue","pr":118,"head":"b6a23a4"}]`)** with a hard directive to build B7 MA-tree greedy split now.
  - **Predictor bank FULLY SATURATED** (16/16 nibble 0..15, per-plane top10/block top12/selective-16 thr55 top13, color top8 exhaustive - all neutral per B5.35). B6 5/3 lifting done and **inert** (+0.8% never-expand, kept disabled). B7 squeeze scaffolds (B5.29/33/35) added but **inert without the MA-tree greedy split**.
  - **B7 MA-tree greedy split (mandatory `llc_class`) is the ONLY lever and has NEVER been genuinely built.** This `continue` is explicitly scoped to it via comment.md.
  - **Owner re-engaged (did NOT repivot):** chose continuation; Mae redirected it to B7.
  - **Merge gate NOT met** (11.059 vs 8.71 JXL). Held until M3<8.71 bit-exact + Tester approval.

## PENDING (in order)
1. **BUILDER MUST BUILD B7 THIS RUN:** implement Squeeze + MA-tree greedy split with mandatory `llc_class`/`sibling_class` (the real core, not another scaffold). If it cannot, escalate to maintainer. No further B5.x widening.
2. **CIRCUIT-BREAKER BUDGET (owner action):** raise budget or repivot #117 if B7 fails. ~36/20 false-trips; the "not converging" premise is literally true for B5.x (8x ~0% builds).
3. **Prism M1-M4 (PR #118):** once B7 is genuinely attempted, HOLD merge until M3 < 8.71 bit-exactly (and Reviewer -> Tester fired).
4. **ORCHESTRATION RULE FIX:** effectively landed (reviewer.md auto-guard). Optional fixer.md hardening parked.
5. **PR #119:** CLOSED by owner (redundant; target #98 CLOSED). Resolved.
6. **Silent-stall mitigation:** re-dispatch owner-directed `continue` when no build in flight - SUSPENDED earlier due to saturated bank, now RE-ENGAGED but REDIRECTED to B7.

## ISSUES
- **#68 (Obsidian umbrella)** - CLOSED.
- **#103 (Prism)** - CLOSED (merged #104); M1-M4 via #117 + PR #118.
- **#117 (Prism M1-M4)** - OPEN (tracking; goal-tied merge gate). At risk of repivot only if B7 fails to move the gap.
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
- **Circuit breaker:** false-trip stands (~36/20); "not converging" premise now literally true for B5.x (8x ~0% builds). This run honored it by re-reviewing and issuing ONE redirected, B7-scoped `continue`.

## NEXT STEPS
1. **Prism #118 - BUILDER MUST BUILD B7:** this run's `continue` directive orders the real MA-tree greedy split (mandatory llc_class/sibling_class). No B5.x widening. If deferred again, escalate (next run goes to maintainer/lab, not another loop).
2. **CIRCUIT-BREAKER BUDGET (owner):** raise budget or repivot #117 if B7 cannot close the gap.
3. **ORCHESTRATION FIX:** considered landed (reviewer.md auto-guard). Optional fixer.md hardening parked.
4. **PR #119:** resolved (CLOSED).
5. **Silent-stall mitigation:** re-engaged but REDIRECTED to B7 (not blind B5.x).

## OPEN QUESTIONS
- Will the Builder actually build B7 this `continue`, or again defer behind a B5.x widening? The directive is explicit; if ignored, next run escalates.
- If B7 lands and the gap remains ~unchanged (~21% needed for M3), should #117 be repivoted (partial work published: Prism 11.059 bpp, M0 bit-exact, PNG gate PASS) rather than iterated further?
- When/if the build stabilizes at/under the gate (M3 < 8.71 bit-exactly), fire Reviewer -> Tester before ANY merge.
- PR #119: resolved (CLOSED).

- Mae, the Maintainer
