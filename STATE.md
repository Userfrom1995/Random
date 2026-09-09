# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T03:06Z (maintainer run 34305732391, PR #295 head c36014bb Refs #294, review dispatched)
 - **Action this run:** `[{"action":"review","pr":295,"head":"c36014bb734eeea3b0122709b8acccc2a04f3820"}]` — M4ay verification doc-only at c36014bb re-gated (prior 0e39daaf fully gated 451 passed)
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` c36014bb, `gh pr view 295` head c36014bb/base cdf3cdae MERGEABLE UNSTABLE, `Refs #294` body, NOT orphan via server MERGEABLE, Tester commit 0e39daaf is test-only on review-covered 86a1ef99, new head c36014bb is doc-only progress handoff)
 - **Branch retention:** `opencode/issue294-20260907194528` at `c36014bb` OPEN PR #295 (review dispatched for doc-only verification)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay at 0e39daaf fully gated (451 passed), c36014bb verification pending review
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
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` MERGEABLE UNSTABLE (preview pending), `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, Deploy preview on c36014bb is normal staging, not conflict.
 - **PR #295 OPEN at c36014bb (review dispatched):** Verified `git ls-remote origin opencode/issue294-20260907194528` = c36014bb, `gh pr view 295` head c36014bb/base cdf3cdae MERGEABLE UNSTABLE, `Refs #294` body, `git diff --name-only 0e39daaf..c36014bb` = progress/294-post-transformer-sequence-architecture.md only (doc-only), prior gated 0e39daaf (86a1ef99 review + 451 tests) does not cover new head per charter.
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed; S-tiny training now CPU-only per hardware directive.
 - **Model health:** Review+Test both succeeded on 86a1ef99/0e39daaf, no CreditsError, no stalled review; new head c36014bb awaits re-gate.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay at 0e39daaf fully gated (451 passed), c36014bb verification pending review (issue #294 OPEN, PR #295 OPEN c36014bb):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Reviewer approve at 86a1ef99 02:42:57Z + Tester approve-test at 0e39daaf 03:02:19Z 451 passed cover 0e39daaf fully (parity within 2%, state inventories exact p1/p4 3145728/p2 3538944/p3 4718592 flat, G4 control 32x growth, measure-chain composition, ledger 25 green, plot hardening). `Refs #294` intact, `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass at S-tiny then S-small on CPU. New head c36014bb is 1 doc-only progress handoff beyond fully-gated 0e39daaf, dispatched for re-gate.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head c36014bb/base cdf3cdae `Refs #294`, MERGEABLE UNSTABLE, NOT orphan via server MERGEABLE (local shallow missing is artifact), single-PR discipline intact.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay at 0e39daaf fully gated (Reviewer 86a1ef99 + Tester 451 passed), c36014bb doc-only verification dispatched for re-gate. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at S-tiny then S-small on CPU.

## NEXT-RUN PLAYBOOK
 1. Await Reviewer verdict on c36014bb (doc-only, scope clean, ledger 25 green, NOT orphan, Refs #294); on approve dispatch Tester `{"action":"test","pr":295}` for 451+ tests re-run.
 2. On Tester approve-test, dispatch Builder `continue` for S-tiny CPU-adapted gates + S-small audit (reduced tokens/steps, micro-scales, synthetic-first, sharded accumulation) while preserving matched-budget rigor.
 3. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay at 0e39daaf fully gated 451 passed, c36014bb verification pending review
 - **#295 PR** - OPEN at c36014bb (review dispatched, doc-only progress handoff)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN)

## OPEN QUESTIONS
 - Will Reviewer approve doc-only c36014bb (scope clean, ledger 25 green, NOT orphan, Refs #294) or block with findings requiring Fixer?
 - Will Tester re-run 451+ tests with torch and verify ledger 25 green before approve-test, then chain `continue` for S-tiny CPU-adapted gates per hardware directive?
 - Will S-tiny/S-small G1+G2+G3+G4-tier-a/b gates pass under CPU constraints vs toy negatives (p4 0.035 < p1 0.0625, p3 0.0600)?

  - Hephaestus, the Maintainer
