# STATE - Random factory checkpoint
- **Updated:** 2026-08-22 (maintainer run 32559525132, owner `/oc maintainer` on PR #118). Fresh survey confirms: PR #118 head `2e65cef1` (B5.32, 11.059 bpp, byte-exact, harness ~360s), **no `continue` build was in flight** when this run started (last real build `32558674142` COMPLETED landing B5.32). This run has therefore dispatched a fresh owner-directed `continue` (head `2e65cef1`) to resume B6-B8 - B7 is now MANDATORY. `opencode.yml` STILL has NO `lab` job and NO `workflows: write` permission (reviewer.md auto-guard committed 770a756 still enforces infra routing). #119/#120 CLOSED by owner.
- **Maintainer run 32559525132 (07:24Z)** dispatched the owner-directed `continue` and wrote the public comment emphasizing B7. A prior run (32558534766, 07:02Z) had found the loop paused at B5.31 and dispatched a `continue` (head 961fa2a) which ran and landed B5.32; this run found the loop paused again at B5.32 and resumed it.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; docs cleaned by merged PR #116). Obsidian is the current codec in `main`; last confirmed REAL-Kodak baseline **9.5209 bpp**. #68 (Obsidian umbrella) is now CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation in flight (issue #117, PR #118). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71). The merge gate is tied to the ACTUAL project goal, not any iteration/round limit; never merge incomplete work.
- **One-PR rule + NEVER delete PR branches:** satisfied.
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Quality-gate directive:** quality gates are the ONLY merge criteria.
- **(2026-08-22T04:48Z):** infra/workflow changes MUST be delegated to the Lab Engineer, never the Fixer. Enforced in reviewer.md (committed 770a756); `lab.yml` routes `/oc lab` to Lab Engineer for `.github/agents/*.md` edits only.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `770a7567c147fbd00373691c7a59d8000f992b87`** (last commit: "reviewer: route infrastructure PRs to the Lab Engineer and enforce it"). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/117-prism-m1-m4-optimization` = `2e65cef1` shares M0 ancestry (NOT orphan).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** production deploy succeeded (main). PR #118 preview deploy is `action_required` (env approval, not the production path).
- **WORKFLOW-FILE PUSH WALL:** #120 CLOSED by owner. `opencode.yml` still lacks `workflows: write` and a `lab` job, but the reviewer.md auto-guard (committed 770a756) rewrites any misrouted fix/continue on infra PRs to `lab`, so the orchestration-rule fix is effectively enforced. Future workflow-file edits remain an OWNER-action path.
- **CIRCUIT-BREAKER FALSE-TRIP (still pending owner action):** now at 33/20 false trips. The "no converging / net-negative" premise (Obsidian #93) is FALSE for Prism - steady genuine byte reductions (11.29 -> 11.059, ~2% total, each a byte-exact Kodak win). Owner has been manually re-authorizing each iteration via `/oc maintainer`; #120 closed means the budget was NOT raised via that issue, so the manual re-auth pattern continues. Please raise the breaker budget or repivot/close #117.

## IN FLIGHT
- **Prism M1-M4 (issue #117, PR #118, branch `opencode/117-prism-m1-m4-optimization`):** head `2e65cef1` (B5.32, 11.059 bpp, byte-exact, harness ~360s). **As of this run: NO build was in flight** (last real build `32558674142` completed landing B5.32). This run dispatched a fresh owner-directed `continue` (decision list, head `2e65cef1`) to resume B6-B8. **Predictor bank is FULLY SATURATED** (16/16 nibble 0..15, per-plane top8, block top10, selective-16 thr45 top11) per B5.32's own report, AND B6 5/3 lifting is done and inert (+0.8% never-expand, kept disabled). B7 (Squeeze+MA-tree greedy split depth 6 with mandatory `llc_class`/`sibling_class`) is the ONLY proven >10% closure to M3 < 8.71 and MUST be attempted next - no more B5.x/B6 headroom. The dispatched `continue` MUST build B7, not another exhausted-bank tweak.

## PENDING (in order)
1. **CIRCUIT-BREAKER BUDGET (owner action):** owner should raise budget (or repivot #117) so the loop isn't manually re-pinged each iteration. #120 closed without resolving this - track here.
2. **Prism M1-M4 (PR #118):** dispatched `continue` MUST build B7; HOLD merge until M3 < 8.71 bit-exactly.
3. **ORCHESTRATION RULE FIX:** effectively landed - reviewer.md (commit 770a756) enforces "infra/workflow -> Lab Engineer, never Fixer"; `lab.yml` handles `.github/agents/*.md` edits. Optional: harden fixer.md similarly via `lab` (parked, low priority, guard already auto-enforced).
4. **PR #119:** CLOSED by owner (redundant; target #98 CLOSED). Resolved.
5. **Silent-stall mitigation:** re-dispatch owner-directed `continue` when no build is in flight (fired this run - loop was paused at B5.32).

## ISSUES
- **#68 (Obsidian umbrella)** - CLOSED.
- **#103 (Prism)** - CLOSED (merged #104); M1-M4 via #117 + PR #118.
- **#117 (Prism M1-M4)** - OPEN (tracking; goal-tied merge gate).
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
- **Circuit breaker:** false-trip persists (33/20); owner manual re-auth continues; #120 closed without raising budget.

## NEXT STEPS
1. **Prism #118:** dispatched `continue` MUST attempt B7 Squeeze+MA-tree (predictor bank + 5/3 exhausted). If B7 also fails to close the ~2.35 bpp gap, repivot #117 (owner decision).
2. **CIRCUIT-BREAKER BUDGET (owner):** raise budget or repivot #117 so the loop isn't manually re-pinged each iteration (tracked in PENDING #1).
3. **ORCHESTRATION FIX:** considered landed (reviewer.md auto-guard). Optional fixer.md hardening parked.
4. **PR #119:** resolved (CLOSED).
5. **Silent-stall mitigation:** re-dispatch owner-directed `continue` when no build in flight (fired this run).

## OPEN QUESTIONS
- Will the Builder actually attempt B7 (Squeeze+MA-tree greedy split depth 6, mandatory `llc_class`/`sibling_class`) on the dispatched `continue`, instead of another exhausted-bank B5.x/B6 tweak? This is the only path to M3 < 8.71.
- Will the owner raise the circuit-breaker budget (or repivot #117) so the loop stops being manually re-pinged? #120 closed without resolving this.
- If B7 also fails to close the ~2.35 bpp gap to JXL, should #117 be repivoted (and partial work published) rather than continuing to burn iterations?
- Prism #118: when stable at/under gate, fire Reviewer -> Tester before any merge.
- PR #119: resolved (CLOSED).

- Mae, the Maintainer
