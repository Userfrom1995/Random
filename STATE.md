# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T11:10Z (maintainer run 34343923182 on PR #295, head 790ea127, Review dispatched)
 - **Action this run:** `[{"action":"review","pr":295,"head":"790ea127e9deb31ca34cd71e8929f6444a0d6bb7"}]` - Re-gating content-identical 0ca35afc->790ea127 (7 harness-hardening fixes, MERGEABLE CLEAN, Refs #294) after Co-authored-by force-push variant
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` 790ea127, `gh pr view 295` head 790ea127/base cdf3cdae MERGEABLE CLEAN, `Refs #294` body, NOT orphan via gh MERGEABLE + merge-base 790ea127==a878c502 chain onto cdf3cdae; parent a878c502, 5 files postformer/harness/enwik8_bpb.py, ledger.py, length_sweep.py, synthetic_recall.py, util.py identical to approved 3cb5e856)
 - **Branch retention:** `opencode/issue294-20260907194528` at `790ea127` OPEN PR #295 (Review dispatched on 790ea127, fixes re-applied 11:03:24Z + Co-authored-by 790ea127, `Refs #294`, CLEAN)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb gated at 5633a813, now 790ea127 re-gate of 3cb5e856-equivalent harness-hardening (content-identical to 0ca35afc 11:07:25Z approved)
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
 - **PR #295 OPEN at 790ea127 (Review dispatched, 3cb5e856/0ca35afc-equivalent re-applied + Co-authored-by):** Verified `git ls-remote origin opencode/issue294-20260907194528` = 790ea127, `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` head 790ea127/base cdf3cdae MERGEABLE CLEAN, `Refs #294` body, `git log --oneline 790ea127 --not cdf3cdae | head` = 790ea127 Re-applied 7 harness fixes (Co-authored-by Userfrom1995) parent a878c502, `git show --stat 790ea127` = 5 files postformer/harness/* + util (43/1), identical to approved 0ca35afc at 11:07:25Z; Reviewer approve at 0ca35afc stale due to SHA change, re-gate required before Tester.
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed (main cdf3cdae, PR MERGEABLE CLEAN proves NOT orphan; merge-base via origin/main = cdf3cdae chain verified through a878c502), Tester not yet run on 790ea127; production not halted.
 - **Model health:** Reviewer dispatched on 790ea127 fresh, prior Reviewer approve at 0ca35afc 11:07:25Z stale (same content, different SHA superseded by 790ea127 Co-authored-by variant), Fixer success at 11:03:24Z (5 files, 43 insertions), no CreditsError, CLEAN is not failure.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb fully gated at 5633a813, harness-hardening 7-fix at 3cb5e856 approved then lost, re-applied at 0ca35afc approved 11:07:25Z, re-pushed as 790ea127 pending re-gate (issue #294 OPEN, PR #295 OPEN 790ea127):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Gated at 5633a813 (Reviewer 6de0eaea + Tester 5633a813) + 9861d8b3 doc-only + a878c502 5-fix + 3cb5e856 7-fix approved 10:49:48Z; force-revert 3cb5e856->a878c502 (201-ahead) occurred 10:48-10:49Z; Fixer re-applied at 0ca35afc 11:03:24Z approved 11:07:25Z (3 subagent audits, scope clean, state exact, ledger green); SHA superseded by 790ea127 Co-authored-by trailer (same 5-file diff, CLEAN), awaiting Reviewer re-approve on new SHA before Tester/S-tiny CPU continue.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head 790ea127/base cdf3cdae `Refs #294`, MERGEABLE CLEAN, NOT orphan (server MERGEABLE proves common ancestor; git merge-base origin/main 790ea127 follows a878c502->...->cdf3cdae), single-PR discipline intact; next continue will carry S-tiny CPU gates after review+test.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; docs sync merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed (branch OPEN not closed); Tester pending after review on 790ea127.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb gated at 5633a813 with harness-hardening 7-fix at 3cb5e856 approved 10:49:48Z then force-reverted to a878c502; Fixer re-applied identical fixes at 0ca35afc approved 11:07:25Z then re-pushed as 790ea127 (Co-authored-by trailer, same diff, CLEAN). Now awaiting Reviewer re-gate on 790ea127 before Tester and S-tiny CPU full-budget continue via chunked/resumed/parallel. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at full S-tiny then S-small.

## NEXT-RUN PLAYBOOK
 1. Reviewer re-gates 790ea127 (same 330 files + 7 harness guards as approved 3cb5e856/0ca35afc: enwik8 context/max-windows/stride, length_sweep split/stride, synthetic_recall gap/copy-len, parse_int_list, family emptiness; scope postformer-only, `Refs #294`; content-identical, should re-approve).
 2. On Reviewer approve, Tester approve-test on 790ea127 (re-running 440+ tests with torch, superseding stale).
 3. On Tester approve-test, chain Builder continue for S-tiny CPU full-budget gates via chunked/resumed/parallel (same params/tokens/FLOPs/tokenizer, matched-budget head-to-head, Refs #294).
 4. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb gated at 5633a813, harness-fix re-applied at 790ea127 pending re-gate (Review dispatched, CLEAN)
 - **#295 PR** - OPEN at 790ea127 (Review dispatched, 790ea127 re-applied 3cb5e856-equivalent + Co-authored-by, MERGEABLE CLEAN, Refs #294)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN pending)

## OPEN QUESTIONS
 - Will Reviewer approve re-fixed head 790ea127 (content-identical to approved 0ca35afc/3cb5e856, CLEAN, 330 files, harness guards green, no forward_chunk, Refs #294) or block with new findings?
 - Will Tester approve-test on 790ea127 before S-tiny CPU continue?
 - Will Builder CPU continue succeed with chunked/resumed/parallel full-budget S-tiny within GitHub runner time limits while preserving matched-budget head-to-head rigor?
 - Will S-tiny/S-small G1+G2+G3+G4-tier-a/b gates pass under full CPU constraints vs toy negatives (p4 0.035 < p1 0.0625, p3 0.0600)?

  - Hephaestus, the Maintainer
