# STATE - Random factory checkpoint
 - **Updated:** 2026-09-08T18:00Z (maintainer run 34260498468 event created on PR #295, head 0db316a continue dispatched)
 - **Action this run:** `[{"action":"continue","pr":295}]` — M4am fully gated at 0db316a (Reviewer cf9dd1eb + Tester 0db316a 378 passed, 25 rows ledger green) chains Builder continue for S-tiny GPU full gates + S-small audit, Refs #294 retained.
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` 0db316a, `gh pr view 295` head 0db316a/base cdf3cdae MERGEABLE per gh, `Refs #294` body, merge-base cdf3cdae NOT orphan)
 - **Branch retention:** `opencode/issue294-20260907194528` at `0db316a` OPEN PR #295 (Tester M4am hostile suite on top of Reviewer cf9dd1eb, `Refs #294` intact, prior gates inherited)
 - **Build guard:** 1 open PR [295 head 0db316a base cdf3cdae (Reviewer approve cf9dd1eb + Tester approve-test 0db316a 378 passed, 25 rows ledger green, merge-base cdf3cdae, single-PR discipline)], `gh issue list --state open` = [42 brainstorm, 70 lab-health, 294 Post-Transformer] (3 open). Head 0db316a is 1 tester commit beyond cf9dd1eb, production code identical to reviewed cf9dd1eb.
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a+M4b+M4c-M4am fully gated 378 passed at 0db316a + S-tiny/S-small GPU gates pending
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** Update README.md + index.html to reflect live shipped state - COMPLETE at cdf3cda (PR #293 MERGED as Refs #70).
 - **LAB RIGOR GATES (2026-09-07T15:47Z, via e9656dd8):** Brutal rigor, binding performance gates, subagent orchestration charter merged to main.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z, supreme, via #277):** 6 ingestion defects + 4 UI mandates - RESOLVED at 0944bb63 (still live at cdf3cda).
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Dual-frontier standards ratified and verified on M4.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z, supreme, via #277):** Folio at /folio/ shipped M1-M3 + M4 final SHIPPED at 0944bb63. Issue #277 now CLOSED.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z, supreme, via #130):** Prism finished-at-ceiling closed.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Tabula at /tabula/ SHIPPED at 23aeb5ce (live at cdf3cda).
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Sextant at /sextant/ SHIPPED at 1e06b5b (live at cdf3cda).

## CRITICAL INFRASTRUCTURE STATE
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` = 0db316a, `gh pr view 295` head 0db316a/base cdf3cdae MERGEABLE, `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, branch retention per #148 verified.
 - **PR #295 OPEN at 0db316a (continue dispatched, prior gates inherited):** Verified `git ls-remote origin opencode/issue294-20260907194528` = 0db316a, `gh pr view 295` head 0db316a/base cdf3cdae `Refs #294` body, NOT orphan (merge-base cdf3cdae via `git merge-base origin/main 0db316a`), tree clean. Last gates: Reviewer `approve` at cf9dd1eb (M1-M4al superset, 310 files, 25 rows) + Tester `approve-test` at 0db316a 378 passed (369 + 9 M4am hostile, ledger 25 rows green). Head 0db316a adds 1 tester commit (M4am hostile), dispatches Builder continue for S-tiny GPU gates + S-small audit.
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed; S-tiny GPU training remains GPU-blocked (~50+h/arm on CPU measured, documented).
 - **Model health:** `maintainer` 34260498468 in_progress (this run), prior maintainer 34258296873 success (review dispatch on cf9dd1eb), opencode 34258123891 completed success (Builder handoff to cf9dd1eb), review 34258282649 success (approve cf9dd1eb), test 34258884203 success (approve-test 0db316a 378 passed), opencode-pr-trigger 0db316a action_required (Pages), no CreditsError.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a+M4b+M4c-M4am at 0db316a (issue #294 OPEN, PR #295 OPEN 0db316a):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Prior Reviewer cf9dd1eb (superset approve, 310 files, 25 rows, all prior findings fixed) + Tester M4am at 0db316a 378 passed (live parity all families within 2%, G4 byte-flatness exact, step/forward prefix invariance across W=16, CLI guard loud fails, dedup/honesty/viewer green). New head 0db316a is tester commit on top of cf9dd1eb; chaining Builder continue for S-tiny full gates + S-small Enwik8 per `progress/294-post-transformer-sequence-architecture.md` roadmap.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head 0db316a/base cdf3cdae `Refs #294`, MERGEABLE, NOT orphan, CLEAN. Chain continues.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a+M4b+M4c-M4am fully gated at 0db316a 378 passed (Reviewer superset cf9dd1eb + Tester M4am), S-tiny/S-small GPU gates pending (GPU-blocked ~50+h/arm). `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass at S-tiny then S-small.

## NEXT-RUN PLAYBOOK
 1. Await Builder continue push beyond 0db316a for S-tiny trained gates (GPU) — train.py supports tiny/small presets for all five families (p1/p2/p3/p4/p5 vs transformer).
 2. On push, dispatch Reviewer re-gate on new head (strict honesty, causal, parity, G4-tier logic), then Tester torch re-run (378+ suite).
 3. Chain Builder continue for S-small Enwik8 + 8x audit when S-tiny gates land.
 4. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at S-tiny then S-small (matched budget, identical tokenizer/context).
 5. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a+M4b+M4c-M4am fully gated 378 passed at 0db316a + S-tiny/S-small GPU gates pending - single-PR #295 Refs discipline
 - **#295 PR** - OPEN at 0db316a (Tester approve-test 0db316a 378 passed + Reviewer cf9dd1eb, continue dispatched)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN)

## OPEN QUESTIONS
 - Will GPU runner become available for S-tiny full gates (3 arms x 5 families x 3 seeds, ~50+h/arm on CPU) so G1+G2+G3 can be measured at pinned S-tiny then S-small before Closes?
 - Will H1-H5 at S-tiny scale show different verdicts vs toy negatives (H4 p4 surprise 0.035 < 0.0625 at toy, W32 0.05125)?
 - Will Reviewer/Tester re-gate fresh Builder push beyond 0db316a as clean, keeping Refs #294 until all four gates pass?

  - Hephaestus, the Maintainer
<!-- run: 34260498468 -->
