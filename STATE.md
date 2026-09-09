# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T02:33Z (maintainer run 34303656066, PR #295 head 96e389ef Refs #294, continue dispatched)
 - **Action this run:** `[{"action":"continue","pr":295}]` — fully gated 96e389ef (Reviewer d4611fb dual approve + Tester 446 passed) chains Builder continue for S-tiny CPU-adapted gates + S-small audit
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` 96e389ef, `gh pr view 295` head 96e389ef/base cdf3cdae MERGEABLE, `Refs #294` body, NOT orphan via gh MERGEABLE, test-only diff d4611fb->96e389ef, 320+ files changed)
 - **Branch retention:** `opencode/issue294-20260907194528` at `96e389ef` OPEN PR #295 (fully gated, chaining continue for S-tiny CPU gates)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax at 96e389ef fully gated (446 passed), S-tiny CPU gates pending
 - **HARDWARE DIRECTIVE (2026-09-08T20:40:31Z, supreme, via #294):** No GPU runner is coming. All S-tiny/S-small training must run on standard GitHub CPU runners. Prior GPU-blocked assumption (~50+h/arm at batch2/seq33) superseded — Builder must redesign training for CPU feasibility (reduced steps/tokens, micro-scales, synthetic-first sweeps, sharded accumulation) while preserving matched param/FLOP/data budget head-to-head discipline and identical tokenizer/context per comparison.
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** Update README.md + index.html to reflect live shipped state - COMPLETE at cdf3cda (PR #293 MERGED as Refs #70).
 - **LAB RIGOR GATES (2026-09-07T15:47Z, via e9656dd8):** Brutal rigor, binding performance gates, subagent orchestration charter merged to main.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z, supreme, via #277):** 6 ingestion defects + 4 UI mandates - RESOLVED at 0944bb63 (still live at cdf3cda).
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Dual-frontier standards ratified and verified on M4.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z, supreme, via #277):** Folio at /folio/ shipped M1-M3 + M4 final SHIPPED at 0944bb63. Issue #277 now CLOSED.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z, supreme, via #130):** Prism finished-at-ceiling closed.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Tabula at /tabula/ SHIPPED at 23aeb5ce (live at cdf3cda).
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Sextant at /sextant/ SHIPPED at 1e06b5b (live at cdf3cda).

## CRITICAL INFRASTRUCTURE STATE
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` MERGEABLE, `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, Deploy action_required on 96e389ef is preview staging, not conflict.
 - **PR #295 OPEN at 96e389ef (fully gated, chaining continue):** Verified `git ls-remote origin opencode/issue294-20260907194528` = 96e389ef, `gh pr view 295` head 96e389ef/base cdf3cdae MERGEABLE, `Refs #294` body, `git diff --name-only d4611fb 96e389ef` = postformer/tests/test_tester_m4ax_redteam.py test-only (no production). Reviewer approve at d4611fb 02:07:17Z + 02:09:52Z (scope clean, state inventories exact) + Tester approve-test at 96e389ef 02:32:59Z 446 passed (parity within 2%, small pins p1/p4 7864320/p2 9043968/p3/p5 12582912, window-train liveness, eviction, P5, G4 bench, ledger locks). Branch NOT orphan via gh MERGEABLE.
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed; S-tiny training now CPU-only per hardware directive. Builder continue to be dispatched, no duplicate in_progress yet.
 - **Model health:** Review+Test both succeeded on d4611fb/96e389ef, no CreditsError, no stalled review.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax at 96e389ef fully gated, chaining continue for S-tiny CPU gates (issue #294 OPEN, PR #295 OPEN 96e389ef):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Reviewer dual approve d4611fb + Tester 446 passed at 96e389ef (test-only on top of review-covered production). `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass at S-tiny then S-small on CPU.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head 96e389ef/base cdf3cdae `Refs #294`, MERGEABLE, NOT orphan, single-PR discipline intact.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax at 96e389ef fully gated (Reviewer d4611fb + Tester 446 passed) chaining Builder continue for S-tiny CPU-adapted gates + S-small audit per hardware directive. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at S-tiny then S-small on CPU.

## NEXT-RUN PLAYBOOK
 1. Await Builder continue push beyond 96e389ef (S-tiny CPU-adapted gates, reduced tokens/steps, matched budget, identical tokenizer/context, ledger proof).
 2. On push, dispatch Reviewer `{"action":"review","pr":295,"head":"<new_sha>"}` for torch re-gate.
 3. On Reviewer approve, dispatch Tester `{"action":"test","pr":295}` for 446+ tests re-run.
 4. On Tester approve-test, chain next Builder `continue` until G1+G2+G3+G4-tier-a/b all pass at S-tiny then S-small.
 5. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax at 96e389ef fully gated 446 passed, S-tiny CPU gates pending
 - **#295 PR** - OPEN at 96e389ef (fully gated, chaining continue)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN)

## OPEN QUESTIONS
 - Will Builder CPU continue produce S-tiny gates beyond 96e389ef within runner limits (reduced steps, micro-scales, synthetic-first) while preserving matched-budget head-to-head rigor?
 - Will Reviewer approve new CPU-gate head or block with findings?
 - Will G4-tier-a flatness hold for all 5 families at scale vs baseline linear when measured on CPU?
 - Will H4 (p4 surprise) or H1-H3 overturn at S-tiny N64+ or replicate toy negatives at scale?

  - Hephaestus, the Maintainer
