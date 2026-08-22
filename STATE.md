# STATE - Random factory checkpoint
- **Updated:** 2026-08-22 (maintainer run 32552686431, EVENT `issue_comment` on PR #119 - owner directive at 04:48:42Z: "reviewer keeps calling the fixer for infra; make the rule explicit and enforceable: infra/workflow changes go to the Lab Engineer, never the Fixer"). Fresh survey confirms: PR #119 still CONFLICTING (head `eac12c1`, target #98 CLOSED - dead weight); PR #118 (Prism) has NO build in flight (last run `32552421303` success at 04:42Z); #120 audit still an OWNER-action blocker (App lacks `workflows` scope). Lab Engineer IS reachable via `lab.yml` (`/oc lab` triggers it) - prior STATE claim that the lab path was broken was STALE/WRONG; only workflow-file EDITS are blocked (no `workflows: write`), prompt edits are pushable.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; docs cleaned by merged PR #116). Obsidian is the current codec in `main`; last confirmed REAL-Kodak baseline **9.5209 bpp**. #68 (Obsidian umbrella) is now CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation in flight (issue #117, PR #118). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71). The merge gate is tied to the ACTUAL project goal, not any iteration/round limit; never merge incomplete work.
- **One-PR rule + NEVER delete PR branches:** satisfied (PR #116 and #104 branches retained after merge).
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Quality-gate directive:** quality gates are the ONLY merge criteria.
- **NEW (2026-08-22T04:48Z):** infra/workflow changes MUST be delegated to the Lab Engineer, never the Fixer. Make it explicit + enforceable in agent prompts.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `02c0fb556d50be4ea056a734da7957420e9357b5`** (post PR #116 merge). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/117-prism-m1-m4-optimization` = `7fe53f8` shares M0 ancestry (NOT orphan).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** production deploy succeeded (main). PR #118 preview deploy is `action_required` (env approval, not the production path).
- **LAB ENGINEER REACHABLE (corrected):** `lab.yml` triggers on `startsWith(comment, '/oc lab')`, so `/oc lab` DOES run the Lab Engineer (prior STATE claim of "lab path broken" was stale). The Lab Engineer CAN push `.github/agents/*.md` prompt edits (contents: write) but CANNOT push `.github/workflows/*.yml` (no `workflows: write`). So prompt-level orchestration fixes are self-healable NOW; workflow-file edits still need the owner to grant `workflows: write`.
- **WORKFLOW-FILE PUSH WALL (audited as #120):** the lab's GitHub App lacks the `workflows` scope, so pushes touching `.github/workflows/*.yml` are `remote rejected`. Audit #120 proposes adding `workflows: write` to the `permissions:` blocks. Owner action still pending.
- **CIRCUIT-BREAKER FALSE-TRIP (diagnosed 04:43Z):** mis-fired on Prism (steady real byte reductions). Owner `/oc maintainer` at 04:43:24Z re-authorized the loop. No new trip this run.

## IN FLIGHT
- **Prism M1-M4 (issue #117, PR #118, branch `opencode/117-prism-m1-m4-optimization`):** head `7fe53f8` (B5.26, 11.061 bpp, byte-exact, harness 235s). As of run 32552686431: NO build currently in flight (last run `32552421303` success 04:42Z). Predictor bank FULL (16/16 nibble); B6 5/3 lifting + B7 Squeeze+MA-tree still required to close the ~2.35 bpp gap to M3 < 8.71. No owner `continue` this run; re-engage only on explicit owner direction (circuit-breaker budget).
- **ORCHESTRATION RULE FIX (owner directive on PR #119, 04:48Z):** dispatched the Lab Engineer via `/oc lab` on issue #120 to make the infra/workflow delegation explicit + enforceable in reviewer.md + fixer.md (pushable prompt edits). The fixer gets a hard refusal guard for `.github/workflows/**` PRs; the reviewer gets an explicit "lab territory, never fixer" rule. In flight once the lab run starts.
- **PR #119 (`[Infra] Lab update for #70`/erroneously `#70`) - STALE / REDUNDANT.** Branch `opencode/lab-98-runaway-fix-retry`, head `eac12c1`, `mergeable=CONFLICTING`. Target #98 CLOSED via PR #99 + run `32540682703`. Dead weight; recommend owner close once the orchestration fix lands. The substantive #98 pagination fix is already in `main`.

## PENDING (in order)
1. **ORCHESTRATION RULE FIX (lab on #120, owner directive):** Lab Engineer edits reviewer.md + fixer.md to enforce "infra/workflow -> Lab Engineer, never Fixer". Pushable now. Track via the lab run triggered this run.
2. **OWNER ESCALATION - audit #120 (workflows: write):** owner must grant App `workflows: write` so (a) the `action: lab` routing case can be added to `opencode-review.yml` and (b) future workflow-file PRs self-heal. Still pending.
3. **Prism M1-M4 (PR #118):** resume B6-B8 on explicit owner `continue`; HOLD merge until M3 < 8.71 bit-exactly.
4. **PR #119 (stale):** close as redundant once orchestration fix lands.
5. **CIRCUIT-BREAKER BUDGET:** owner should raise budget (or repivot #117) so the loop isn't manually re-pinged each iteration; current trip was a false positive.
6. **Silent-stall diagnosis:** owner `/oc continue` intermittently stalled earlier; mitigation is owner-directed `continue` re-dispatch when no build in flight.
7. **#42 Board resume (parked)** behind Prism.
8. **entropy-architecture.md archive (non-blocking).**
9. **Benign agent `git push` fatal-error noise (non-blocking `lab` follow-up).**
10. **Verify PR #118 pages preview:** `action_required` (env approval) - owner-side.

## ISSUES
- **#68 (Obsidian umbrella)** - CLOSED.
- **#103 (Prism)** - CLOSED (merged #104); M1-M4 via #117 + PR #118.
- **#117 (Prism M1-M4)** - OPEN (tracking; goal-tied merge gate).
- **#112 (auto PR recovery)** - CLOSED (shipped #114).
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor daily summary.
- **#98 (runaway /oc fix retry loop)** - CLOSED (PR #99 + run `32540682703`); PR #119 now stale carry.
- **#120 (Audit: workflows: write missing)** - OPEN; owner escalation (cannot self-heal workflow edits). Now also the home of the orchestration-rule fix (prompt edits, pushable).

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `02c0fb556d50be4ea056a734da7957420e9357b5`.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed via #111).
- **Lab Engineer:** reachable via `lab.yml` (`/oc lab`). Pin `opencode/hy3-free`. CAN push prompt `.md` edits; CANNOT push workflow `.yml` (no workflows: write).
- **Circuit breaker:** false-trip diagnosed 04:43Z; owner re-authorized 04:43:24Z.

## NEXT STEPS
1. ORCHESTRATION RULE FIX: Lab Engineer run (triggered this run on #120) edits reviewer.md + fixer.md. Verify the fixer refusal guard and reviewer routing rule land, then Reviewer -> Tester per normal loop.
2. **Audit #120 OWNER ESCALATION:** owner must grant App `workflows: write` (unblocks `action: lab` routing + future workflow-file self-heal).
3. **Prism #118:** resume B6-B8 on explicit owner `continue`; HOLD merge until M3 < 8.71 bit-exactly.
4. **PR #119:** close as redundant once orchestration fix lands.

## OPEN QUESTIONS
- Will the owner grant `workflows: write` so `action: lab` routing + future workflow-file PRs self-heal? (Single unblock for every future workflow-file PR.)
- ORCHESTRATION FIX: will the Lab Engineer's prompt edits (fixer refusal + reviewer routing) actually stop the reviewer/fixer misrouting on infra PRs? The fixer guard is the key enforceable point.
- Prism #118: when stable at/under gate, fire Reviewer -> Tester before any merge. Predictor bank FULL - Builder MUST attempt B6/B7 (no more B5.x headroom).
- PR #119: redundant (target #98 CLOSED); close once orchestration fix merges.
- Circuit breaker: false-positive resolved; owner should raise budget or repivot #117 if B7 Squeeze+MA-tree fails to close the ~2.35 bpp gap.

- Mae, the Maintainer
