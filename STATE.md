# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T08:32Z (maintainer run 34329626008 on PR #295, review dispatched at 6de0eaea)
 - **Action this run:** `[{"action":"review","pr":295,"head":"6de0eaea4f347dbf3cc5473dc2bd7f8aca3ad7dd"}]` - M4ba verification doc-only at 6de0eaea dispatched to Reviewer (1 commit beyond fully-gated b0c52626, progress-only, Refs #294 intact, awaiting re-gate before Tester/S-tiny CPU continue)
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` 6de0eaea, `gh pr view 295` head 6de0eaea/base cdf3cdae MERGEABLE CLEAN, `Refs #294` body, NOT orphan via merge-base cdf3cdae 193 commits)
 - **Branch retention:** `opencode/issue294-20260907194528` at `6de0eaea` OPEN PR #295 (review dispatched, prior fully gated b0c52626 Reviewer a915477a + Tester b0c52626, Refs #294, MERGEABLE)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba at 6de0eaea verification pending re-gate
 - **HARDWARE DIRECTIVE (2026-09-08T20:40:31Z, supreme, via #294) - CLARIFIED 2026-09-09T06:30:17Z via #294 (supreme):** No GPU runner is coming. All S-tiny/S-small training must run on standard GitHub CPU runners. Training scope is **not** reduced: same S-tiny/S-small budgets, same matched-budget discipline (params, training FLOPs/tokens, optimizer, tokenizer/context). Change the execution method (chunked, resumed, parallel), not the experiment size. Prior "reduced steps/tokens, micro-scales" interpretation is superseded - Builder must redesign for CPU feasibility via chunked/resumed/parallel execution while preserving full-budget head-to-head rigor and Refs #294 until all four gates pass. `Closes #294` only on G1+G2+G3+G4-tier-a/b green at full budget.
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** Update README.md + index.html to reflect live shipped state - COMPLETE at cdf3cda (PR #293 MERGED as Refs #70, verified README 48-54 + index.html cards Shipped).
 - **LAB RIGOR GATES (2026-09-07T15:47Z, via e9656dd8):** Brutal rigor, binding performance gates, subagent orchestration charter merged to main.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z, supreme, via #277):** 6 ingestion defects + 4 UI mandates - RESOLVED at 0944bb63 (still live at cdf3cda).
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Dual-frontier standards ratified and verified on M4.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z, supreme, via #277):** Folio at /folio/ shipped M1-M3 + M4 final SHIPPED at 0944bb63. Issue #277 now CLOSED.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z, supreme, via #130):** Prism finished-at-ceiling closed.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Tabula at /tabula/ SHIPPED at 23aeb5ce (live at cdf3cda).
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Sextant at /sextant/ SHIPPED at 1e06b5b (live at cdf3cda).

## CRITICAL INFRASTRUCTURE STATE
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` MERGEABLE CLEAN, `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, Auditor GREEN active.
 - **PR #295 OPEN at 6de0eaea (review dispatched, prior fully gated b0c52626):** Verified `git ls-remote origin opencode/issue294-20260907194528` = 6de0eaea, `git ls-remote origin/main` = cdf3cdae, `git merge-base origin/main 6de0eaea` = cdf3cdae NOT orphan (193 commits via gh MERGEABLE + prior --unshallow at b0c52626), `gh pr view 295` head 6de0eaea/base cdf3cdae MERGEABLE CLEAN, `Refs #294` body, `git show --stat 6de0eaea` = progress/294-post-transformer-sequence-architecture.md only (doc-only verification handoff, 8 insertions), `git diff --name-only b0c52626..6de0eaea` = progress only, scope clean `postformer/|ideas/|docs/research/issue-294|progress/294-`, zero forward_chunk in shipped code. Prior gated head b0c52626 is Tester commit on review-covered a915477a (test-only fully gated).
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed; S-tiny training CPU-only at full budget via chunked/resumed/parallel per 06:30:17Z; Tester healthy.
 - **Model health:** Reviewer success at a915477a, Tester success at b0c52626, no CreditsError, review dispatched on 6de0eaea with correct head targeting (prior pending reviews on cdf3cda were mis-targeted main-sha artifacts).

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba at 6de0eaea verification pending re-gate (issue #294 OPEN, PR #295 OPEN 6de0eaea):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Prior Reviewer APPROVED at a915477a 07:41:20Z + Tester APPROVED at b0c52626 08:27:01Z covering production through a915477a. New doc-only head 6de0eaea (M4ba verification handoff) dispatched to Reviewer; next Tester then Builder continue for S-tiny/S-small CPU full-budget gates via chunked/resumed/parallel.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head 6de0eaea/base cdf3cdae `Refs #294`, MERGEABLE CLEAN, NOT orphan, single-PR discipline intact; 6de0eaea is doc-only on gated b0c52626, awaiting Reviewer re-gate; subsequent continue will carry S-tiny CPU gates.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; docs sync merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed; review in_progress on correct head.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba at 6de0eaea verification pending Reviewer re-gate (prior gated at b0c52626). Hardware directive clarified full budget via chunked/resumed/parallel CPU. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at full S-tiny then S-small.

## NEXT-RUN PLAYBOOK
 1. Await Reviewer verdict on 6de0eaea (scope clean, state inventories exact, ledger 25 green, Refs discipline).
 2. On approve, dispatch Tester on 6de0eaea (full 451+ suite).
 3. On Tester approve-test, chain Builder continue for S-tiny CPU full-budget gates chunked/resumed/parallel.
 4. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba at 6de0eaea verification pending re-gate (prior Reviewer a915477a + Tester b0c52626 gated)
 - **#295 PR** - OPEN at 6de0eaea (review dispatched, prior fully gated b0c52626, MERGEABLE, Refs #294)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN pending)

## OPEN QUESTIONS
 - Will Reviewer approve doc-only 6de0eaea (scope clean, ledger 25 green, NOT orphan, Refs #294) or block with findings requiring Fixer?
 - Will Tester re-run 451+ tests and verify ledger before approve-test, then chain continue for S-tiny CPU full-budget?
 - Will S-tiny/S-small G1+G2+G3+G4-tier-a/b gates pass under full CPU constraints vs toy negatives?

  - Hephaestus, the Maintainer
