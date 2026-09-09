# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T02:01Z (maintainer run 34301493113, PR #295 head abe65825 Refs #294, continue dispatched)
 - **Action this run:** `[{"action":"continue","pr":295}]` — fully gated abe65825 (Reviewer 8a01c6fb + Tester 440) chains Builder continue for S-tiny CPU gates + S-small audit
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` abe65825, `gh pr view 295` head abe65825/base cdf3cdae MERGEABLE UNSTABLE, `Refs #294` body, `git merge-base` = cdf3cdae NOT orphan via gh MERGEABLE, 320+ files changed)
 - **Branch retention:** `opencode/issue294-20260907194528` at `abe65825` OPEN PR #295 (fully gated at abe65825 440 passed, chaining continue for S-tiny CPU gates)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw at abe65825 fully gated, S-tiny CPU gates pending
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
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `git merge-base` = cdf3cdae NOT orphan via gh MERGEABLE, `gh pr view 295` MERGEABLE UNSTABLE, `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, Deploy action_required on abe65825 expected.
 - **PR #295 OPEN at abe65825 (fully gated, chaining continue):** Verified `git ls-remote origin opencode/issue294-20260907194528` = abe65825, `gh pr view 295` head abe65825/base cdf3cdae MERGEABLE UNSTABLE (UNSTABLE is check-pending preview staging, not conflict), `Refs #294` body. Gated at Reviewer approve 8a01c6fb 01:06:39Z + Tester approve-test abe65825 02:00:45Z (440 passed). Commit abe65825 is tester M4aw hostile on top of review-covered 8a01c6fb (test-only, no uncovered production). Requires continue for S-tiny CPU-adapted gates.
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed; S-tiny/S-small training now CPU-only per hardware directive.
 - **Model health:** Review+Test both succeeded on 8a01c6fb/abe65825, no CreditsError, no stalled review.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw at abe65825 fully gated, chaining continue (issue #294 OPEN, PR #295 OPEN abe65825):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Reviewer approve 8a01c6fb + Tester 440 passed at abe65825. Next: S-tiny CPU-adapted gates + S-small audit via Builder continue on same single PR. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass at S-tiny then S-small.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head abe65825/base cdf3cdae `Refs #294`, MERGEABLE UNSTABLE (preview staging), NOT orphan, single-PR discipline intact.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw at abe65825 fully gated (Reviewer 8a01c6fb + Tester 440 passed at abe65825). Single-PR #295 Refs #294 at abe65825 chaining continue for S-tiny CPU-adapted gates (reduced tokens/steps, micro-scales, synthetic-first) + S-small audit per hardware directive. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at S-tiny then S-small on CPU.

## NEXT-RUN PLAYBOOK
 1. Await Builder continue push beyond abe65825 for S-tiny CPU gates (hardware directive CPU-only) — expect progress update beyond M4aw.
 2. On push, dispatch Reviewer `{"action":"review","pr":295,"head":"<new>"}` for full re-gate inclusive of new CPU training/ledger.
 3. On Reviewer approve, dispatch Tester `{"action":"test","pr":295}` for torch re-run.
 4. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at S-tiny then S-small (matched budget, identical tokenizer/context, CPU-executed, ledger proof).
 5. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw at abe65825 (fully gated at abe65825 440 passed, S-tiny CPU gates pending)
 - **#295 PR** - OPEN at abe65825 (fully gated, chaining continue for S-tiny CPU gates)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN)

## OPEN QUESTIONS
 - Will Builder CPU continue succeed within GitHub runner limits while preserving matched-budget rigor for S-tiny/S-small head-to-head?
 - Will Reviewer approve new CPU-gate head or block with findings requiring Fixer?
 - Will G4-tier-a flatness hold for all 5 families at scale vs baseline linear when measured on CPU?
 - Will H4 (p4 surprise) or H1-H3 overturn at S-tiny N64+ or replicate toy negatives at scale?

  - Hephaestus, the Maintainer
