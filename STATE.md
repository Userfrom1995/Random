# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T10:49Z (maintainer run 34342203967 on PR #295, head a878c502 force-reverted from 3cb5e856, re-dispatched Fixer)
 - **Action this run:** `[{"action":"fix","pr":295,"head":"a878c502e2e42914bd3a56be21879cbc7c90c2b5"}]` - force-revert `3cb5e856->a878c502` lost 7 harness-hardening fixes; re-gating fix on a878c502 before Tester/S-tiny CPU continue
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` a878c502, `gh pr view 295` head a878c502/base cdf3cdae MERGEABLE UNSTABLE, `Refs #294` body, NOT orphan via gh MERGEABLE + prior rebase onto cdf3cdae; `git fetch` shows `+ 3cb5e856...a878c502 (forced update)`; 3cb5e856 still locally exists)
 - **Branch retention:** `opencode/issue294-20260907194528` at `a878c502` OPEN PR #295 (prior 3cb5e856 approved but reverted, 6 commits lost, awaiting Fixer re-apply, Refs #294, UNSTABLE is Deploy pending not conflict)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb gated at 5633a813, now M4bb harness fix lost in revert pending re-fix
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
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` MERGEABLE UNSTABLE, `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, Auditor GREEN active.
 - **PR #295 OPEN at a878c502 (Fixer re-dispatched, 3cb5e856 approved then force-reverted):** Verified `git ls-remote origin opencode/issue294-20260907194528` = a878c502, `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` head a878c502/base cdf3cdae MERGEABLE UNSTABLE, `Refs #294` body, `git log --oneline a878c502 --not cdf3cdae | wc -l` = 201, `git cat-file -p 3cb5e856` exists locally (6 commits a878c502..3cb5e856 lost via `+ 3cb5e856...a878c502 (forced update)`), Reviewer fix at a878c502 10:45:49Z (7 harness-hardening: enwik8 context/max-windows/stride, length_sweep, synthetic_recall, parse_int_list, family emptiness) still blocking; prior Reviewer 6de0eaea + Tester 5633a813 (432+ tests, ledger 25 green) do not cover current head; Fixer 34341966244 success lost, re-gate required before Tester/S-tiny CPU continue.
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed (main cdf3cdae, PR MERGEABLE proves NOT orphan despite local shallow artifact); branch force-revert is content loss not infra halt; Tester 34342313920 in_progress is stale on reverted head, not infra failure; S-tiny training CPU-only at full budget via chunked/resumed/parallel per 06:30:17Z; Tester healthy to re-run post-fix.
 - **Model health:** Reviewer fix at a878c502 live, Fixer success at 34341966244 then revert, Tester stale in_progress, no CreditsError, UNSTABLE is Deploy pending not conflict.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb fully gated at 5633a813, M4bb 5-fix at a878c502 + 7 harness fix at 3cb5e856 (reverted) pending re-fix (issue #294 OPEN, PR #295 OPEN a878c502):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Prior gated at 6de0eaea + 5633a813; new head a878c502 needs 7 harness fixes re-applied (enwik8_bpb, ledger, train, util, length_sweep, synthetic_recall) before re-gate.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head a878c502/base cdf3cdae `Refs #294`, MERGEABLE UNSTABLE, NOT orphan (server MERGEABLE + prior rebase onto cdf3cdae; forced update `3cb5e856->a878c502` is content revert not orphan), single-PR discipline intact; 3cb5e856 commits recoverable from `recover/295` tag or local 3cb5e856 object; subsequent fix will restore to 3cb5e856-equivalent, then continue will carry S-tiny CPU gates.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; docs sync merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed (branch OPEN not closed); Builder continue queued after fix+review+test.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb at 5633a813 fully gated (Reviewer 6de0eaea + Tester 5633a813) with M4bb 5-fix at a878c502 + 7 harness-hardening at 3cb5e856 force-reverted, now pending re-fix. Hardware directive clarified full budget via chunked/resumed/parallel CPU. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at full S-tiny then S-small.

## NEXT-RUN PLAYBOOK
 1. Fixer re-applies 7 harness-hardening fixes `a878c502..3cb5e856` (cherry-pick 65a25d97..3cb5e856) and pushes, expecting MERGEABLE CLEAN.
 2. Reviewer re-gates new fixed head (same 330 files + 7 guards, scope postformer-only, `Refs #294`).
 3. On Reviewer approve, Tester approve-test on new head before S-tiny CPU continue.
 4. On Tester approve-test, chain Builder continue for S-tiny CPU full-budget gates via chunked/resumed/parallel (same params/tokens/FLOPs/tokenizer, matched-budget head-to-head, Refs #294).
 5. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb fully gated at 5633a813, fix at a878c502 re-dispatched (7 harness fixes lost in 3cb5e856->a878c502 forced update)
 - **#295 PR** - OPEN at a878c502 (Fixer re-dispatched, prior 3cb5e856 approved then reverted, MERGEABLE UNSTABLE, Refs #294)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN pending)

## OPEN QUESTIONS
 - Will Fixer re-apply 6 commits cleanly on a878c502 without conflicts and re-push to CLEAN?
 - Will Reviewer approve re-fixed head (330 files, harness guards green, ledger 25 check-green, no forward_chunk, Refs #294)?
 - Will Tester approve-test on re-fixed head before S-tiny CPU continue (superseding stale 34342313920)?
 - Will Builder CPU continue succeed with chunked/resumed/parallel full-budget S-tiny within GitHub runner time limits while preserving matched-budget head-to-head rigor?
 - Will S-tiny/S-small G1+G2+G3+G4-tier-a/b gates pass under full CPU constraints vs toy negatives (p4 0.035 < p1 0.0625, p3 0.0600)?

  - Hephaestus, the Maintainer
