# STATE - Random factory checkpoint
- **Updated:** 2026-08-22 (maintainer run 32557577513, EVENT `created` on PR #118 - owner `/oc maintainer` at 06:40Z). Fresh survey confirms: PR #118 head `71538eca` (B5.30, 11.059 bpp, byte-exact, harness ~330s), **a `continue` build IS already in flight** (run `32557569730`, started 06:40:17Z from owner `/oc continue` at 06:40:15Z), so this run dispatched NO duplicate trigger; circuit breaker false-trip persists at 30/20 (steady real gains, not Obsidian #93 net-negative); #120 audit still an OWNER-action blocker (App lacks `workflows` scope); `opencode.yml` has NO `lab` job (so `action: lab` only yields skipped runs on the build workflow; `lab.yml` routes `/oc lab` to the Lab Engineer for prompt edits only).
- **Maintainer run 32552686431 (04:48Z, PR #119 owner directive)** dispatched `lab` on #120 to make infra/workflow delegation explicit + enforceable in reviewer.md + fixer.md. That Lab Engineer dispatch FAILED (run 32552800127, 0s, push to `main` rejected - the `workflows: write` wall). So the orchestration-rule fix is still not landed.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; docs cleaned by merged PR #116). Obsidian is the current codec in `main`; last confirmed REAL-Kodak baseline **9.5209 bpp**. #68 (Obsidian umbrella) is now CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation in flight (issue #117, PR #118). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71). The merge gate is tied to the ACTUAL project goal, not any iteration/round limit; never merge incomplete work.
- **One-PR rule + NEVER delete PR branches:** satisfied.
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Quality-gate directive:** quality gates are the ONLY merge criteria.
- **(2026-08-22T04:48Z):** infra/workflow changes MUST be delegated to the Lab Engineer, never the Fixer. Make it explicit + enforceable in agent prompts.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `770a7567c147fbd00373691c7a59d8000f992b87`** (last commit: "reviewer: route infrastructure PRs to the Lab Engineer and enforce it"). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/117-prism-m1-m4-optimization` = `71538eca` shares M0 ancestry (NOT orphan; B5.30 was a squashed rebuild rebased onto main after an orphan-detection rebase).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** production deploy succeeded (main). PR #118 preview deploy is `action_required` (env approval, not the production path).
- **LAB ENGINEER REACHABLE for PROMPT edits only:** `lab.yml` triggers on `startsWith(comment, '/oc lab')` - Lab Engineer CAN push `.github/agents/*.md` (contents: write) but CANNOT push `.github/workflows/*.yml` (no `workflows: write`). The build workflow `opencode.yml` has NO `lab` job, so a Maintainer `{"action":"lab"}` decision posts `/oc lab` that only yields skipped runs there. Workflow-file edits (the `action: lab` routing case, circuit-breaker fix) need owner `workflows: write`.
- **WORKFLOW-FILE PUSH WALL (audited as #120):** the lab's GitHub App lacks the `workflows` scope, so pushes touching `.github/workflows/*.yml` are `remote rejected`. Audit #120 proposes adding `workflows: write` to the `permissions:` blocks. Owner action still pending. The owner-directed Lab Engineer dispatch on #120 (run 32552800127) FAILED in 0s, confirming the wall.
- **CIRCUIT-BREAKER FALSE-TRIP (owner action needed):** mis-fires on Prism (steady real byte reductions, 11.29 -> 11.059, ~2% total). Owner `/oc maintainer` re-authorizes each occurrence, but the budget is exhausted (tripped at 20/20..30/30). The "no converging / net-negative" premise (Obsidian #93) is FALSE for Prism - the predictor bank is just asymptotically saturated and needs B7, not more predictors. Please raise the breaker budget or repivot/close #117.

## IN FLIGHT
- **Prism M1-M4 (issue #117, PR #118, branch `opencode/117-prism-m1-m4-optimization`):** head `71538eca` (B5.30, 11.059 bpp, byte-exact, harness ~330s). As of this run: **a `continue` build IS in flight** (run `32557569730`, started 06:40:17Z from owner `/oc continue` at 06:40:15Z), resuming B6-B8 from B5.30. **Predictor bank is FULLY EXHAUSTED (16/16 nibble 0..15, per-plane top9 + block top8, selective-16 thr35 saturated) AND B6 5/3 lifting is done and inert (+0.8% never-expand, kept disabled).** B7 (Squeeze+MA-tree greedy split depth 6 with mandatory `llc_class`/`sibling_class`) is the ONLY proven >10% closure to M3 < 8.71 and MUST be attempted next - no more B5.x/B6 headroom. The in-flight build MUST build B7, not another exhausted-bank tweak.

## PENDING (in order)
1. **OWNER ESCALATION - audit #120 (workflows: write):** owner must grant App `workflows: write` so (a) the `action: lab` routing case can be added to `opencode-review.yml`, (b) future workflow-file PRs self-heal, (c) circuit-breaker false-trip logic can be fixed. Still pending.
2. **ORCHESTRATION RULE FIX (lab on #120):** re-dispatch once #120 lands; Lab Engineer edits reviewer.md + fixer.md to enforce "infra/workflow -> Lab Engineer, never Fixer".
3. **Prism M1-M4 (PR #118):** in-flight build `32557569730` MUST build B7; HOLD merge until M3 < 8.71 bit-exactly.
4. **CIRCUIT-BREAKER BUDGET:** owner should raise budget (or repivot #117) so the loop isn't manually re-pinged each iteration.
5. **PR #119 (stale):** close as redundant once orchestration fix lands.
6. **Silent-stall mitigation:** re-dispatch owner-directed `continue` when no build in flight (not needed this run - build already in flight).

## ISSUES
- **#68 (Obsidian umbrella)** - CLOSED.
- **#103 (Prism)** - CLOSED (merged #104); M1-M4 via #117 + PR #118.
- **#117 (Prism M1-M4)** - OPEN (tracking; goal-tied merge gate).
- **#112 (auto PR recovery)** - CLOSED (shipped #114).
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor daily summary.
- **#98 (runaway /oc fix retry loop)** - CLOSED (PR #99 + run `32540682703`); PR #119 now stale carry.
- **#120 (Audit: workflows: write missing)** - OPEN; owner escalation (cannot self-heal workflow edits). Home of the orchestration-rule fix (prompt edits, still blocked by the wall).

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `770a7567c147fbd00373691c7a59d8000f992b87`.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE.
- **Lab Engineer:** reachable via `lab.yml` (`/oc lab`) for PROMPT edits only; CANNOT push workflow `.yml` (no workflows: write).
- **Circuit breaker:** false-trip at 30/20; owner must raise budget.

## NEXT STEPS
1. **Prism #118:** in-flight build `32557569730` MUST attempt B7 Squeeze+MA-tree (predictor bank + 5/3 exhausted). If B7 also fails to close the ~2.35 bpp gap, repivot #117 (owner decision).
2. **Audit #120 OWNER ESCALATION:** owner must grant App `workflows: write` (unblocks `action: lab` routing + circuit-breaker fix + orchestration-rule prompt PR self-heal).
3. **ORCHESTRATION FIX:** re-dispatch Lab Engineer on #120 once #120 lands.
4. **PR #119:** close as redundant once orchestration fix merges.
5. **Circuit breaker:** owner should raise budget or repivot #117 if B7 fails to close the ~2.35 bpp gap.

## OPEN QUESTIONS
- Will the Builder actually attempt B7 (Squeeze+MA-tree greedy split depth 6, mandatory `llc_class`/`sibling_class`) on the in-flight `continue`, instead of another exhausted-bank B5.x/B6 tweak? This is the only path to M3 < 8.71.
- Will the owner grant `workflows: write` so workflow-file edits self-heal and the circuit-breaker false-trip can be fixed at the source?
- If B7 also fails to close the ~2.35 bpp gap to JXL, should #117 be repivoted (and partial work published) rather than continuing to burn iterations?
- Prism #118: when stable at/under gate, fire Reviewer -> Tester before any merge.
- PR #119: redundant (target #98 CLOSED); close once orchestration fix merges.

- Mae, the Maintainer
