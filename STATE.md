# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T01:04Z (maintainer run 34297568628, PR #295 head 8a01c6fb Refs #294, review dispatched)
 - **Action this run:** `[{"action":"review","pr":295,"head":"8a01c6fbabf64d0b5010e37b7f2dd3980b9e91a2"}]` — doc-only M4av verification beyond fully-gated cec66b1c dispatched to Reviewer
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` 8a01c6fb, `gh pr view 295` head 8a01c6fb/base cdf3cdae MERGEABLE CLEAN, `Refs #294` body, `git merge-base origin/main 8a01c6fb` = cdf3cdae NOT orphan via gh MERGEABLE, 320+ files changed)
 - **Branch retention:** `opencode/issue294-20260907194528` at `8a01c6fb` OPEN PR #295 (fully gated at cec66b1c, doc-only 8a01c6fb needs re-gate before Tester/S-tiny continue)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4as-M4av at cec66b1c fully gated, doc-only 8a01c6fb pending review
 - **HARDWARE DIRECTIVE (2026-09-08T20:40:31Z, supreme, via #294):** No GPU runner is coming. All S-tiny/S-small training must run on standard GitHub CPU runners. Prior GPU-blocked assumption (~50+h/arm at batch2/seq33 measured 2026-09-08) superseded — Builder must redesign training for CPU feasibility (reduced steps/tokens, micro-scales, synthetic-first sweeps, sharded accumulation) while preserving matched param/FLOP/data budget head-to-head discipline and identical tokenizer/context per comparison.
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** Update README.md + index.html to reflect live shipped state - COMPLETE at cdf3cda (PR #293 MERGED as Refs #70).
 - **LAB RIGOR GATES (2026-09-07T15:47Z, via e9656dd8):** Brutal rigor, binding performance gates, subagent orchestration charter merged to main.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z, supreme, via #277):** 6 ingestion defects + 4 UI mandates - RESOLVED at 0944bb63 (still live at cdf3cda).
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Dual-frontier standards ratified and verified on M4.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z, supreme, via #277):** Folio at /folio/ shipped M1-M3 + M4 final SHIPPED at 0944bb63. Issue #277 now CLOSED.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z, supreme, via #130):** Prism finished-at-ceiling closed.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Tabula at /tabula/ SHIPPED at 23aeb5ce (live at cdf3cda).
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Sextant at /sextant/ SHIPPED at 1e06b5b (live at cdf3cda).

## CRITICAL INFRASTRUCTURE STATE
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `git merge-base origin/main 8a01c6fb` = cdf3cdae NOT orphan (gh MERGEABLE CLEAN proves common ancestor), `gh pr view 295` MERGEABLE CLEAN, `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, Deploy success on 8a01c6fb expected.
 - **PR #295 OPEN at 8a01c6fb (doc-only beyond fully-gated cec66b1c, awaiting Reviewer re-gate):** Verified `git ls-remote origin opencode/issue294-20260907194528` = 8a01c6fb, `gh pr view 295` head 8a01c6fb/base cdf3cdae MERGEABLE CLEAN, `Refs #294` body. Gated at Reviewer approve `a051ff88` 00:05:50Z + Tester approve-test `cec66b1c` 00:57:59Z (432 passed). Commit 8a01c6fb is doc-only `progress/294-post-transformer-sequence-architecture.md` (1 file, builder verification + review handoff, Refs #294). Requires re-gate before Tester/S-tiny continue.
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed; S-tiny/S-small training now CPU-only per hardware directive.
 - **Model health:** Review dispatched on 8a01c6fb, no CreditsError, no stalled review beyond this gating.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4as-M4av at cec66b1c fully gated, doc-only 8a01c6fb pending review (issue #294 OPEN, PR #295 OPEN 8a01c6fb):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Reviewer approve a051ff88 + Tester 432 passed at cec66b1c. New head 8a01c6fb doc-only verification + review handoff needs re-gate; S-tiny CPU-adapted gates + S-small audit via Builder continue on same single PR after Tester approve-test.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head 8a01c6fb/base cdf3cdae `Refs #294`, MERGEABLE CLEAN, NOT orphan, single-PR discipline intact.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4as-M4av at cec66b1c fully gated (Reviewer a051ff88 + Tester 432 passed at cec66b1c). Single-PR #295 Refs #294 at 8a01c6fb doc-only pending review. Builder will continue for S-tiny CPU-adapted gates (reduced tokens/steps, micro-scales, synthetic-first) + S-small audit after review/test. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass at S-tiny then S-small on CPU.

## NEXT-RUN PLAYBOOK
 1. Await Reviewer verdict on 8a01c6fb (doc-only M4av verification, scope clean, NOT orphan, Refs #294) — expect approve (prior 432 coverage), or Fixer if findings.
 2. On Reviewer approve, dispatch Tester `{"action":"test","pr":295}` for torch 432+ suite re-run on 8a01c6fb.
 3. On Tester approve-test, chain Builder continue `{"action":"continue","pr":295}` for S-tiny CPU gates + S-small audit per hardware directive.
 4. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at S-tiny then S-small (matched budget, identical tokenizer/context, CPU-executed, ledger proof).
 5. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4as-M4av at 8a01c6fb (fully gated at cec66b1c, doc-only 8a01c6fb pending review, S-tiny CPU gates pending)
 - **#295 PR** - OPEN at 8a01c6fb (doc-only beyond 432-gated cec66b1c, awaiting Reviewer re-gate)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN)

## OPEN QUESTIONS
 - Will Reviewer approve doc-only 8a01c6fb (scope clean, ledger 25 green, NOT orphan, Refs #294) or block with findings requiring Fixer?
 - Will Builder CPU continue succeed within GitHub runner limits while preserving matched-budget rigor for S-tiny/S-small head-to-head?
 - Will G4-tier-a flatness hold for all 5 families at scale vs baseline linear when measured on CPU?
 - Will H4 (p4 surprise) or H1-H3 overturn at S-tiny N64+ or replicate toy negatives at scale?

  - Hephaestus, the Maintainer
