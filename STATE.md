# STATE - Random factory checkpoint
- **Updated:** 2026-08-22 (maintainer run 32554896970, EVENT `issue_comment` on PR #118 - owner `/oc continue` ~05:39Z; no build in flight, resumed loop via owner-directed `continue`). Fresh survey confirms: PR #118 head `b571d1b` (B5.28, 11.059 bpp, byte-exact, harness ~310s), NO build currently in flight (last real build `32553898957` success at 05:16Z landed B5.28); circuit breaker tripped at 27/20 (FALSE trip - steady real gains, not Obsidian #93 net-negative case); #120 audit still an OWNER-action blocker (App lacks `workflows` scope); opencode.yml has NO `lab` job (so `action: lab` only yields skipped runs on the build workflow; the separate `lab.yml` routes `/oc lab` to the Lab Engineer for prompt edits only).
- **Maintainer run 32552686431 (04:48Z, PR #119 owner directive)** dispatched `lab` on #120 to make infra/workflow delegation explicit + enforceable in reviewer.md + fixer.md. That Lab Engineer dispatch FAILED (run 32552800127, 0s, push to `main` rejected - the `workflows: write` wall). So the orchestration-rule fix is still not landed.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; docs cleaned by merged PR #116). Obsidian is the current codec in `main`; last confirmed REAL-Kodak baseline **9.5209 bpp**. #68 (Obsidian umbrella) is now CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation in flight (issue #117, PR #118). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71). The merge gate is tied to the ACTUAL project goal, not any iteration/round limit; never merge incomplete work.
- **One-PR rule + NEVER delete PR branches:** satisfied.
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Quality-gate directive:** quality gates are the ONLY merge criteria.
- **(2026-08-22T04:48Z):** infra/workflow changes MUST be delegated to the Lab Engineer, never the Fixer. Make it explicit + enforceable in agent prompts.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `770a7567c147fbd00373691c7a59d8000f992b87`** (advanced past `02c0fb55`). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/117-prism-m1-m4-optimization` = `b571d1b` shares M0 ancestry (NOT orphan).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** production deploy succeeded (main). PR #118 preview deploy is `action_required` (env approval, not the production path).
- **LAB ENGINEER REACHABLE for PROMPT edits only:** `lab.yml` triggers on `startsWith(comment, '/oc lab')` - Lab Engineer CAN push `.github/agents/*.md` (contents: write) but CANNOT push `.github/workflows/*.yml` (no `workflows: write`). The build workflow `opencode.yml` has NO `lab` job, so a Maintainer `{"action":"lab"}` decision posts `/oc lab` that only yields skipped runs there. Workflow-file edits (the `action: lab` routing case, circuit-breaker fix) need owner `workflows: write`.
- **WORKFLOW-FILE PUSH WALL (audited as #120):** the lab's GitHub App lacks the `workflows` scope, so pushes touching `.github/workflows/*.yml` are `remote rejected`. Audit #120 proposes adding `workflows: write` to the `permissions:` blocks. Owner action still pending. The owner-directed Lab Engineer dispatch on #120 (run 32552800127) FAILED in 0s, confirming the wall.
- **CIRCUIT-BREAKER FALSE-TRIP (owner action needed):** mis-fires on Prism (steady real byte reductions, 11.29 -> 11.059, ~2% total). Owner `/oc continue` re-authorizes each occurrence, but the budget is exhausted (tripped at 20/20..27/27). The "no converging / net-negative" premise (Obsidian #93) is FALSE for Prism. Please raise the breaker budget or repivot/close #117.

## IN FLIGHT
- **Prism M1-M4 (issue #117, PR #118, branch `opencode/117-prism-m1-m4-optimization`):** head `b571d1b` (B5.28, 11.059 bpp, byte-exact, harness ~310s). As of this run: NO build in flight (last run `32553898957` success at 05:16Z landed B5.28). **Predictor bank is now FULLY EXHAUSTED (16/16 nibble 0..15, per-plane top6 + block top7/8, selective-16 threshold saturation). B7 (Squeeze+MA-tree greedy split depth 6 with mandatory `llc_class`/`sibling_class`) is the ONLY proven >10% closure to M3 < 8.71 and MUST be attempted next - no more B5.x headroom.** This run dispatches owner-directed `continue` to resume B6-B8 with an explicit directive that the Builder MUST build B7, not another B5.x tweak.
- **ORCHESTRATION RULE FIX (owner directive on PR #119, 04:48Z):** dispatched Lab Engineer via `/oc lab` on #120 to edit reviewer.md + fixer.md (pushable prompt edits). The dispatch FAILED (run 32552800127, `workflows: write` wall). NOT landed. Fixer refusal guard + reviewer routing rule still absent.

## PENDING (in order)
1. **OWNER ESCALATION - audit #120 (workflows: write):** owner must grant App `workflows: write` so (a) the `action: lab` routing case can be added to `opencode-review.yml`, (b) future workflow-file PRs self-heal, (c) circuit-breaker false-trip logic can be fixed. Still pending.
2. **ORCHESTRATION RULE FIX (lab on #120):** re-dispatch once #120 lands; Lab Engineer edits reviewer.md + fixer.md to enforce "infra/workflow -> Lab Engineer, never Fixer".
3. **Prism M1-M4 (PR #118):** resume B6-B8 via `continue`; Builder MUST attempt B7 (Squeeze+MA-tree) - predictor bank exhausted. HOLD merge until M3 < 8.71 bit-exactly.
4. **CIRCUIT-BREAKER BUDGET:** owner should raise budget (or repivot #117) so the loop isn't manually re-pinged each iteration.
5. **PR #119 (stale):** close as redundant once orchestration fix lands.
6. **Silent-stall mitigation:** re-dispatch owner-directed `continue` when no build in flight (done this run).

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
- **Circuit breaker:** false-trip at 27/20; owner must raise budget.

## NEXT STEPS
1. **Prism #118:** owner-directed `continue` dispatched this run (head `b571d1b`); Builder MUST attempt B7 Squeeze+MA-tree (predictor bank exhausted - no more B5.x headroom).
2. **Audit #120 OWNER ESCALATION:** owner must grant App `workflows: write` (unblocks `action: lab` routing + circuit-breaker fix + orchestration-rule prompt PR self-heal).
3. **ORCHESTRATION FIX:** re-dispatch Lab Engineer on #120 once #120 lands.
4. **PR #119:** close as redundant once orchestration fix merges.
5. **Circuit breaker:** owner should raise budget or repivot #117 if B7 fails to close the ~2.35 bpp gap.

## OPEN QUESTIONS
- Will the owner grant `workflows: write` so workflow-file edits self-heal and the circuit-breaker false-trip can be fixed at the source?
- Will the Builder actually attempt B7 (Squeeze+MA-tree) on the next `continue`, instead of yet another exhausted-bank B5.x tweak? This is the only path to M3 < 8.71.
- Prism #118: when stable at/under gate, fire Reviewer -> Tester before any merge.
- PR #119: redundant (target #98 CLOSED); close once orchestration fix merges.
- Circuit breaker: false-positive; owner should raise budget or repivot #117 if B7 Squeeze+MA-tree fails to close the ~2.35 bpp gap.

- Mae, the Maintainer
