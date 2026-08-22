# STATE - Random factory checkpoint
- **Updated:** 2026-08-22 (maintainer run 32563685959, owner `/oc maintainer` on PR #118). Fresh survey confirms: PR #118 head `b6a23a46f7df5e94a8499c490bca6f82a1bc7066` (B5.35, 11.059 bpp, byte-exact, harness ~360s), **no `continue` build was in flight** when this run started (last real build `32562446891` COMPLETED landing B5.35 at 08:58:32Z). This run has **HALTED the auto-loop** (decision `[]`) at the owner's `/oc maintainer` rather than dispatching another blind `continue` that would only yield 0% B5.36 - the bank is proven saturated and the Builder's `continue` resume cannot reach B7. Owner decision now required: instruct Builder to build B7 MA-tree directly, OR repivot #117 and publish partial work. `opencode.yml` STILL has NO `lab` job; #119/#120 CLOSED by owner.
- **Maintainer run 32563685959 (08:58Z)** wrote the assessment/comment on PR #118: B5.35 = 0% (bank "exhaustively proven saturated" per the Builder's own report); B7 MA-tree greedy split (mandatory llc_class/sibling_class) is the only lever and has been deferred through 9+ continue dispatches due to a structural resume trap (continue follows the next B5.x refinement, never B7). Loop halted; owner must choose (1) direct B7 instruction, or (2) repivot #117.

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
- **CIRCUIT-BREAKER FALSE-TRIP (now ~36/20, and the "not converging" premise is LITERALLY TRUE for B5.x):** auto-guard has tripped repeatedly; the breaker text requires "a human (owner or Maintainer) must review the trajectory and either repivot/close the issue or explicitly raise the budget. No further auto-dispatches will be issued by this guard." Prism B5.28-B5.35 are 8 consecutive ~0% builds (B5.32/33/34/35 all 11.059 bpp) - the bank is mathematically saturated. This run HALTED the auto-loop to honor that condition. Owner manual re-auth continues, but blind continuation now only burns iterations on noise.

## IN FLIGHT
- **Prism M1-M4 (issue #117, PR #118, branch `opencode/117-prism-m1-m4-optimization`):** head `b6a23a4` (B5.35, 11.059 bpp, byte-exact, harness ~360s). **As of this run: NO build was in flight** (last real build `32562446891` completed landing B5.35 at 08:58:32Z). This run has **HALTED the auto-loop** (decision `[]`). 
  - **Predictor bank FULLY SATURATED** (16/16 nibble 0..15, per-plane top10/block top12/selective-16 thr55 top13, color top8 exhaustive - all neutral per B5.35). B6 5/3 lifting done and **inert** (+0.8% never-expand, kept disabled). B7 squeeze scaffolds (B5.29/33/35) added but **inert without the MA-tree greedy split**.
  - **B7 MA-tree greedy split (mandatory `llc_class`/`sibling_class`) is the ONLY proven >10% closure to M3 < 8.71 and has NEVER been genuinely built.** It has been deferred through 9+ `continue` dispatches because the Builder's `continue` resume perpetually widens the saturated B5.x bank and never reaches B7 (structural trap).
  - **Owner decision required:** (1) post an explicit PR #118 instruction telling the Builder to build the B7 MA-tree greedy split NOW (skip further B5.x), then I dispatch the build with that narrow scope; or (2) repivot #117 and publish partial work. I will NOT dispatch another blind `continue`.

## PENDING (in order)
1. **OWNER DECISION (this run's blocker):** instruct Builder to build B7 MA-tree greedy split directly on PR #118, OR repivot #117 and publish partial work. Loop halted until this is answered. No blind `continue`.
2. **CIRCUIT-BREAKER BUDGET (owner action):** raise budget or repivot #117. #120 closed without resolving this; the "not converging" premise is now literally true for B5.x (8x ~0% builds).
3. **Prism M1-M4 (PR #118):** once B7 is genuinely attempted, HOLD merge until M3 < 8.71 bit-exactly (and Reviewer -> Tester fired).
4. **ORCHESTRATION RULE FIX:** effectively landed (reviewer.md auto-guard). Optional fixer.md hardening parked.
5. **PR #119:** CLOSED by owner (redundant; target #98 CLOSED). Resolved.
6. **Silent-stall mitigation:** re-dispatch owner-directed `continue` when no build in flight - but SUSPENDED this run because the next `continue` would only yield 0% B5.36 on a saturated bank.

## ISSUES
- **#68 (Obsidian umbrella)** - CLOSED.
- **#103 (Prism)** - CLOSED (merged #104); M1-M4 via #117 + PR #118.
- **#117 (Prism M1-M4)** - OPEN (tracking; goal-tied merge gate). At risk of repivot if B7 fails or owner chooses repivot.
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
- **Circuit breaker:** false-trip stands (~36/20); "not converging" premise now literally true for B5.x (8x ~0% builds). This run honored it by halting the auto-loop.

## NEXT STEPS
1. **Prism #118 - BLOCKED on owner decision:** (a) direct B7 MA-tree instruction (then I dispatch the build), or (b) repivot #117 + publish partial work. No blind `continue`.
2. **CIRCUIT-BREAKER BUDGET (owner):** raise budget or repivot #117 (tracked in PENDING #2).
3. **ORCHESTRATION FIX:** considered landed (reviewer.md auto-guard). Optional fixer.md hardening parked.
4. **PR #119:** resolved (CLOSED).
5. **Silent-stall mitigation:** suspended this run (next `continue` = 0% B5.36 on saturated bank).

## OPEN QUESTIONS
- Owner choice for Prism #118: (1) instruct Builder to build B7 MA-tree greedy split (mandatory llc_class/sibling_class) directly on PR #118, or (2) repivot #117 and publish partial work? I will not dispatch another blind `continue`.
- If B7 MA-tree is attempted and STILL cannot close the ~2.35 bpp gap to JXL, should #117 be repivoted (partial work published) rather than iterated further? At ~36/20 false-trips and 8 consecutive ~0% builds, the "not converging" premise is now literal - a repivot decision is overdue.
- When/if the build stabilizes at/under the gate (M3 < 8.71 bit-exactly), fire Reviewer -> Tester before ANY merge.
- PR #119: resolved (CLOSED).

- Mae, the Maintainer
