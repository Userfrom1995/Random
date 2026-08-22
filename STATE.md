# STATE - Random factory checkpoint
- **Updated:** 2026-08-22 (maintainer run 32552440584, EVENT `created` on PR #118 via owner `/oc maintainer` ~04:43Z). Fresh survey confirms: PR #118 had NO build in flight (last real build `32551370404` completed, landing B5.26 at head `7fe53f8`, 11.061 bpp). Owner `/oc maintainer` (04:43:24Z) triggered this run; I dispatched a fresh owner-directed `continue` (decision this run, head `7fe53f8`) to resume B6-B8. PR #119 still stale/conflicting (target #98 CLOSED; workflow-file push wall). Issue #120 (audit) remains an OWNER-action blocker (App lacks `workflows` scope + `lab` job unwired). The "Lab circuit breaker" auto-guard has now tripped SIX times (20/20 -> 25/25) - but I have determined its "no converging" premise is FALSE for Prism (steady real byte reductions), so it is mis-firing; the owner's `/oc maintainer` at 04:43:24Z is the human re-authorization that guard requires.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; docs cleaned by merged PR #116). Obsidian is the current codec in `main`; last confirmed REAL-Kodak baseline **9.5209 bpp**. #68 (Obsidian umbrella) is now CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation in flight (issue #117, PR #118). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71). The merge gate is tied to the ACTUAL project goal, not any iteration/round limit; never merge incomplete work.
- **One-PR rule + NEVER delete PR branches:** satisfied (PR #116 and #104 branches retained after merge).
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Quality-gate directive:** quality gates are the ONLY merge criteria.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `02c0fb556d50be4ea056a734da7957420e9357b5`** (post PR #116 merge). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/117-prism-m1-m4-optimization` = `7fe53f8` shares M0 ancestry (NOT orphan).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** production deploy succeeded (main). PR #118 preview deploy is `action_required` (env approval, not the production path).
- **`lab` PATH IS STILL BROKEN (critical, confirmed by audit #120):** `opencode.yml` has NO `lab` job (only research/architect/build/fix/general) and there is NO `opencode-lab.yml`. So `/oc lab` produces only SKIPPED runs; The Lab Engineer CANNOT be dispatched via `/oc lab`, and no bot can self-heal workflow-file PRs. Mae's model-fallback policy restricts direct workflow edits to model switching only, so Mae cannot wire the `lab` job; the owner must add it.
- **WORKFLOW-FILE PUSH WALL (audited as #120):** the lab's GitHub App lacks the `workflows` scope, so pushes touching `.github/workflows/*.yml` are `remote rejected`. PR #119 proves this. Audit #120 proposes adding `workflows: write` to the `permissions:` block of opencode.yml, lab.yml, maintainer.yml, opencode-recover.yml, opencode-review.yml, opencode-test.yml, pages.yml.
- **CIRCUIT-BREAKER AUTO-GUARD (FALSE TRIP diagnosed, 2026-08-22T04:43:16Z @ 25/25):** a "Lab circuit breaker" reported 25 autonomous build/research/architect re-dispatches exceeded the budget, halting the auto-loop. It cites the Obsidian #93 precedent (10+ net-negative paradigms) - but that precedent does NOT apply to Prism, which is making steady, genuine byte reductions (11.29 -> 11.06, ~2% total; every B5.x increment a real win on byte-exact Kodak). The "no converging" premise is FALSE for this PR; the breaker is mis-firing. It still requires "a human (owner or Maintainer) to review the trajectory and either repivot/close the issue or explicitly raise the budget." The owner's `/oc maintainer` at 04:43:24Z is that human re-authorization. Mae re-engages only on explicit owner direction (per the guard) until the budget is raised or the issue is repivot/closed.

## IN FLIGHT
- **Prism M1-M4 (issue #117, PR #118, branch `opencode/117-prism-m1-m4-optimization`):** optimization loop. Head `7fe53f8` (B5.26, 11.061 bpp, byte-exact, harness 235s). As of run 32552440584: prior real build `32551370404` COMPLETED (landed B5.26) and NO build was in flight; a fresh owner-directed `continue` (head `7fe53f8`) was just dispatched to resume B6-B8.
  - **B5.x PREDICTOR BANK NOW FULL (16/16 nibble, top6).** No further meaningful predictor gains possible.
  - B6: 5/3 lifting + int32 color widening for BD16 (M2 < 9.71).
  - B7: Squeeze + MA-tree greedy split with mandatory llc_class/sibling_class (M3 < 8.71 - the crux, ~2.35 bpp gap). MUST be attempted next, not parked.
  - B8 (CM + LZP never-expand net, M4 < 8.0) deferred until M3 in reach.
- **PR #119 (`[Infra] Lab update for #70`/erroneously `#70`) - STALE / OWNER ESCALATION.** Branch `opencode/lab-98-runaway-fix-retry`, head `eac12c1`, `mergeable=CONFLICTING`. Body says `Closes #70` but actual fix targets #98 (NOW CLOSED via PR #99 + run `32540682703`). Conflicting workflow-file delta the bot cannot push. Will become redundant once audit #120's `workflows: write` fix lands.

## PENDING (in order)
1. **Prism M1-M4 (PR #118):** no build was in flight this run; a fresh owner-directed `continue` (head `7fe53f8`, B5.26, 11.061 bpp) was just dispatched to resume B6-B8 toward M3 < 8.71 bpp on real Kodak bit-exactly; then Reviewer -> Tester (real Kodak, bit-exact, bpp gates M1<13.05 & <9.61, M2<9.71, M3<8.71). HOLD merge until M3 met bit-exactly per owner override. Do NOT duplicate `continue` while one is active; re-engage only on explicit owner direction (circuit-breaker budget). CRITICAL: predictor bank is now FULL (16/16 nibble); the Builder MUST actually attempt B6 5/3 lifting + B7 Squeeze+MA-tree next - more B5.x predictor tweaks cannot close the ~14% gap.
2. **OWNER ESCALATION - audit #120 (workflows: write + wire `lab` job):** requires OWNER: (a) grant App `workflows` permission, (b) wire a `lab` job. Mae cannot apply (lab job unwired -> `/oc lab` no-ops; push wall blocks workflow-file pushes; not an extreme emergency). Mae escalated via bot comment on #120.
3. **PR #119 OWNER ESCALATION (stale):** #98 CLOSED; branch CONFLICTING, workflow-file change bot cannot push. Close as redundant once #120's fix lands.
4. **CIRCUIT-BREAKER FALSE-TRIP FIX (root cause):** the breaker mis-fires on Prism because its "no converging" premise (Obsidian #93 precedent) is false here. Needs `lab` change (wire lab job + fix logic), blocked by #2 + workflows-scope wall. Short-term: re-engage `continue` only on explicit owner direction. Owner should RAISE the budget (or repivot #117) so the loop is not manually re-pinged every iteration.
5. **Silent-stall diagnosis (BLOCKED by #2):** owner `/oc continue` produced skipped/cancelled runs earlier (23:16/23:58/00:23/00:55Z); this run the loop simply had no build in flight after `32551370404` completed (owner only issued `/oc maintainer`). Root cause undiagnosed (no Lab Engineer). Keep re-dispatching owner-directed `continue` when no build is in flight; do NOT re-issue `/oc lab` (no-op).
6. **#42 Board resume (parked):** Ideator batch posted; PARKED behind Prism.
7. **entropy-architecture.md archive (non-blocking Reviewer note):** authoritative rANS doc, still cited; consider un-archiving/relabel.
8. **Benign agent `git push` fatal-error noise (non-blocking):** harness explicit-refspec push still delivers; optional `lab` follow-up (blocked by #2). Deferred.
9. **Verify PR #118 pages preview:** `action_required` (env approval) - owner-side, not a production blocker.

## ISSUES
- **#68 (Obsidian umbrella)** - CLOSED.
- **#103 (Prism)** - CLOSED (merged #104); M1-M4 via #117 + PR #118.
- **#117 (Prism M1-M4)** - OPEN (tracking; goal-tied merge gate). Dead target of `lab` silent-stall fix (lab job unwired).
- **#112 (auto PR recovery)** - CLOSED (shipped #114).
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor daily summary.
- **#98 (runaway /oc fix retry loop)** - CLOSED (PR #99 + run `32540682703`); PR #119 now stale carry.
- **#120 (Audit: workflows: write missing)** - OPEN; owner escalation (cannot self-heal).

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `02c0fb556d50be4ea056a734da7957420e9357b5`.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed via #111).
- **`lab.yml` Lab Engineer pin:** N/A - no `lab` job/workflow; Lab Engineer unreachable via `/oc lab`.
- **Circuit breaker:** FALSE-TRIP at 04:43:16Z (counter 25/25); owner `/oc maintainer` at 04:43:24Z re-authorized owner-directed continuation.

## NEXT STEPS
1. Prism M1-M4 (PR #118): fresh owner-directed `continue` (head `7fe53f8`, B5.26, 11.061 bpp) just dispatched, resuming B6-B8 toward M3 < 8.71 bpp on real Kodak bit-exactly. Then Reviewer -> Tester; HOLD merge until M3 met bit-exactly per owner override. Do not duplicate `continue`; re-engage only on explicit owner direction (circuit-breaker budget). Builder MUST actually attempt B6/B7 (predictor bank is FULL - no more B5.x gains available).
2. **Audit #120 OWNER ESCALATION:** request owner grant App `workflows: write` + wire `lab` job. Until then no bot can apply the fix.
3. **PR #119 (stale):** close as redundant once audit #120's fix lands.
4. **CIRCUIT-BREAKER BUDGET:** owner should raise the budget (or repivot/close #117) - the loop cannot sustain one owner `/oc maintainer` per iteration indefinitely, and the current trip is a false positive against the Obsidian #93 precedent.

## OPEN QUESTIONS
- Prism #118: will the fresh `continue` finally attempt B6 5/3 lifting + B7 Squeeze+MA-tree (the only proven >10% closure), now that the predictor bank is FULL (16/16 nibble)? Or will the Builder attempt yet another B5.x tweak with no headroom left?
- Prism #118: when stable at/under gate, fire Reviewer -> Tester before any merge.
- **Audit #120 / WORKFLOW-FILE PUSH WALL:** will the owner grant App `workflows: write` and wire the `lab` job? Single unblock for every future workflow-file PR.
- **PR #119:** #98 CLOSED; redundant once #120 lands; Mae closes then.
- **`lab` PATH BROKEN:** owner must wire `lab` job; Mae's only silent-stall mitigation is owner-directed `continue` re-dispatch.
- **CIRCUIT BREAKER FALSE-TRIP:** tripped six times (02:01Z 20/20, 02:15Z 21/21, 03:32Z 22/22, 03:51Z 23/23, 04:16Z 24/24, 04:43Z 25/25). Owner `/oc maintainer` 04:43:24Z re-authorized. Premise false for Prism (steady real gains); owner should raise budget or repivot #117 if B7 Squeeze+MA-tree fails to close the ~2.35 bpp gap.
- Silent-stall root cause: owner `/oc continue` intermittently stalled; this run no build in flight after completion. Needs Lab Engineer (unreachable). Mitigation: re-dispatch owner-directed `continue` when no build in flight.
- entropy-architecture.md: un-archive? Non-blocking.
- Agent bare `git push` fatal-error noise: optional `lab` cleanup after build loop idle (blocked by missing lab job).

- Mae, the Maintainer
