# STATE - Random factory checkpoint
- **Updated:** 2026-08-22 (maintainer run 32582521352, ~15:42Z). Fresh survey confirms: PR #118 head `18a3de48d7abe3d328c927d58a1e7c2bf553804b` (B5.37, 11.059 bpp, byte-exact, harness ~370s), **no `continue` build in flight** (last real build advanced branch from `8e5a565` B5.36 to `18a3de48` B5.37 - a 0% saturation sweep). This run **dispatched a `continue` to resume the loop** with the hardest B7 mandate yet, honoring the owner's 14:51Z iteration-limit lift + "keep working" directive.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; docs cleaned by merged PR #116). Obsidian is the current codec in `main`; last confirmed REAL-Kodak baseline **9.5209 bpp**. #68 (Obsidian umbrella) is now CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation in flight (issue #117, PR #118). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71). The merge gate is tied to the ACTUAL project goal, not any iteration/round limit.
- **Iteration limit LIFTED (2026-08-22T14:51Z):** owner removed the 20-round/iteration cap and said "keep working". The circuit-breaker budget is now unlimited by owner action. The loop may continue indefinitely toward the gate.
- **One-PR rule + NEVER delete PR branches:** satisfied.
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Quality-gate directive:** quality gates are the ONLY merge criteria.
- **(2026-08-22T04:48Z):** infra/workflow changes MUST be delegated to the Lab Engineer, never the Fixer. Enforced in reviewer.md (committed 770a756); `lab.yml` routes `/oc lab` to Lab Engineer for `.github/agents/*.md` edits only.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `770a7567c147fbd00373691c7a59d8000f992b87`** (last commit: "reviewer: route infrastructure PRs to the Lab Engineer and enforce it"). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/117-prism-m1-m4-optimization` = `18a3de48` shares M0 ancestry (NOT orphan).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** production deploy succeeded (main). PR #118 preview deploy is `action_required` (env approval, not the production path).
- **WORKFLOW-FILE PUSH WALL (unchanged, now non-blocking for the loop):** #120 CLOSED by owner. `opencode.yml` still lacks `workflows: write` and a `lab` job, but the reviewer.md auto-guard (committed 770a756) rewrites any misrouted fix/continue on infra PRs to `lab`, so the orchestration-rule fix is effectively enforced. Future workflow-file edits remain an OWNER-action path.
- **CIRCUIT-BREAKER (was 36/20, now LIFTED):** the auto-guard had tripped repeatedly and was HARD-halted, but the owner's 14:51Z directive removed the iteration limit, so the budget constraint no longer applies. This run dispatched a `continue` resume (not an auto-loop re-trip).

## IN FLIGHT
- **Prism M1-M4 (issue #117, PR #118, branch `opencode/117-prism-m1-m4-optimization`):** head `18a3de48` (B5.37, 11.059 bpp, byte-exact, harness ~370s). **A `continue` build was just dispatched this run (head `18a3de48`) with the hardest B7 mandate yet.** The B5.x trajectory is CONVERGED: B5.28-B5.37 = 10 consecutive ~0% builds (11.059 bpp flat).
  - **Predictor bank FULLY SATURATED** (16/16 nibble 0..15, per-plane top10-11, block top12-13, selective-16 thr55-60 top13-14, color top8 - all neutral). B6 5/3 lifting done and **inert** (+0.8% never-expand, kept disabled). B7 Squeeze + MA-tree greedy split has been SCAFFOLDED three times (B5.33 per-band, B5.35 mode5, B5.36 leaf-activity MA-tree LITE) but the real greedy split with mandatory `llc_class`/`sibling_class` has NEVER been built. B5.37 defied the prior run's explicit B7 redirect (landed as a thoroughness saturation sweep).
  - **STRUCTURAL TRAP (confirmed):** the Builder's `continue` resume follows the progress file's immediate next B5.x refinement; B7 is only a distant "Next", so every `continue` yields another 0% B5.x sweep. Five+ B7-mandated `continue`s have all produced B5.x. `continue` alone CANNOT reach B7.
  - **Merge gate NOT met** (11.059 vs 8.71 JXL, gap 2.35 / ~21%). Held until M3<8.71 bit-exact + Tester approval.

## PENDING (in order)
 1. **BREAK THE B7 TRAP (this run):** the dispatched `continue` MUST genuinely build the real B7 Squeeze + MA-tree greedy split (depth 6, leaves 16-32, mandatory `llc_class`/`sibling_class`) - NOT another B5.x widening. If this `continue` again lands as a 0% B5.x build, the resume trap is confirmed structural and Mae will escalate (per project-perseverance, endless 0% iteration is not acceptable). Owner options if B7 still not built: (a) post a DIRECT, narrow B7 instruction on PR #118, or (b) repivot #117 and publish the partial baseline.
 2. **If B7 lands and gap persists ~unchanged (~21% to M3):** repivot #117 and publish the partial baseline (Prism 11.059 bpp, M0 bit-exact, PNG PASS, reproducible Kodak CSVs + architecture-m1-m4.md) per project-perseverance rules, rather than iterate endlessly.
 3. **Prism M1-M4 (PR #118):** once B7 is genuinely attempted, HOLD merge until M3 < 8.71 bit-exactly (and Reviewer -> Tester fired).
 4. **ORCHESTRATION RULE FIX:** effectively landed (reviewer.md auto-guard). Optional fixer.md hardening parked.
 5. **PR #119:** CLOSED by owner (redundant; target #98 CLOSED). Resolved.
 6. **Silent-stall mitigation:** now moot - owner removed the iteration cap; loop resumes normally.

## ISSUES
- **#68 (Obsidian umbrella)** - CLOSED.
- **#103 (Prism)** - CLOSED (merged #104); M1-M4 via #117 + PR #118.
- **#117 (Prism M1-M4)** - OPEN (tracking; goal-tied merge gate). At risk of repivot only if B7 fails to move the gap (or the resume trap is confirmed structural).
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
- **Circuit breaker:** LIFTED by owner (14:51Z directive). No budget cap.

## NEXT STEPS
 1. **AWAIT B7 BUILD:** the dispatched `continue` must deliver the real MA-tree greedy split (mandatory `llc_class`/`sibling_class`). If the next Builder report is another B5.x 0% sweep, the resume trap is confirmed and Mae will escalate to a direct owner B7 instruction (or repivot).
 2. If B7 closes (or substantially narrows) the 2.35 bpp gap, keep iterating toward M3 < 8.71; if it lands at/under the gate bit-exactly, fire Reviewer -> Tester before any merge.
 3. If B7 also fails to move the gap (or cannot be built), repivot #117 and publish the partial baseline.
 4. ORCHESTRATION FIX: considered landed (reviewer.md auto-guard). Optional fixer.md hardening parked.
 5. PR #119: resolved (CLOSED).

## OPEN QUESTIONS
- Will the Builder genuinely build the B7 MA-tree greedy split (mandatory `llc_class`/`sibling_class`) on this `continue`, or again defer it behind a B5.x widening? Five+ B7-mandated `continue`s have all failed; if this one does too, the resume trap is confirmed structural and escalation is required.
- If B7 is genuinely built and the gap stays ~21%, should #117 be repivoted and the partial work published?
- When/if the build stabilizes at/under the gate (M3 < 8.71 bit-exactly), fire Reviewer -> Tester before ANY merge.
- PR #119: resolved (CLOSED).

- Mae, the Maintainer
