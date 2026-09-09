# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T15:19Z (maintainer run 34369435584 issue_comment, head ceb445e1, Tester gate fail + Fixer applied, Reviewer re-dispatched)
 - **Action this run:** `[{"action":"review","pr":295,"head":"ceb445e1f8c796adfc1d9fb1b0ac9f188a5a9ef3"}]` — Reviewer re-gate on ceb445e1 (Fixer 4/5 Tester findings at d5581ff2, 469 passed/5 failed, harness-hardening re-applied)
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae489c7efd1b655e46af83623e722ace19, `git ls-remote origin opencode/issue294-20260907194528` ceb445e1f8c796adfc1d9fb1b0ac9f188a5a9ef3, `gh pr view 295` head ceb445e1f8c796adfc1d9fb1b0ac9f188a5a9ef3/base cdf3cdae489c7efd1b655e46af83623e722ace19 MERGEABLE CLEAN, `Refs #294` body, NOT orphan via merge-base cdf3cdae; history verified)
 - **Branch retention:** `opencode/issue294-20260907194528` at `ceb445e1f8c796adfc1d9fb1b0ac9f188a5a9ef3` OPEN PR #295 (Reviewer re-dispatched on ceb445e1, Tester d5581ff2 gate fail fixed, `Refs #294`, CLEAN triggerDeploy success)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb + A4/A6/envelope + M4bc gated at d5581ff2 pending re-test at ceb445e1
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
 - **PR #295 OPEN at ceb445e1 (Fixer applied, Reviewer re-dispatched):** Verified `git ls-remote origin opencode/issue294-20260907194528` = ceb445e1f8c796adfc1d9fb1b0ac9f188a5a9ef3, `git ls-remote origin/main` = cdf3cdae489c7efd1b655e46af83623e722ace19, `gh pr view 295` head ceb445e1f8c796adfc1d9fb1b0ac9f188a5a9ef3/base cdf3cdae489c7efd1b655e46af83623e722ace19 MERGEABLE CLEAN, `Refs #294` body, NOT orphan via merge-base cdf3cdae; Tester at d5581ff2 (34362859770) failed 469 passed/5 failed on 510ff67c lineage (m4bc suite green, harness guards clashed with pinned tests), Fixer at ceb445e1 applied 4/5 (determinism MINI p1-subset, enwik8 stride == context, BaseException loudness, parse_int_list SystemExit) + flagged historical discipline #5 (d4f3fbb2 missing Refs + Co-authored-by), `Refs #294`, CLEAN triggerDeploy success. Awaiting Reviewer re-gate before Tester.
 - **No infra anomaly requiring Lab Engineer yet:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed (main cdf3cdae, PR MERGEABLE true proves NOT orphan), production not halted; if Tester again hits `The action has timed out.` will dispatch lab to raise timeout-minutes.
 - **Model health:** Reviewer and Tester healthy, no CreditsError; Tester 36min run at d5581ff2 completed with decision (not timeout).

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb + A4/A6/envelope + M4bc gated at d5581ff2, Fixer at ceb445e1 (issue #294 OPEN, PR #295 OPEN ceb445e1):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Tester d5581ff2 exposed 5 failures from unreviewed fixer harness hardening clashing with pinned tests; Fixer ceb445e1 resolves 4 strictly (keeps M2-A2 guard strict, fixes stride guard, loudness pin, parse guard) and flags historical discipline. Reviewer to verify no infra touch, parity within 2%, state_bytes, causality, ledger 25 green, Refs discipline before Tester re-run.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head ceb445e1f8c796adfc1d9fb1b0ac9f188a5a9ef3/base cdf3cdae489c7efd1b655e46af83623e722ace19 `Refs #294`, MERGEABLE CLEAN (trigger+deploy success on ceb445e1), NOT orphan, single-PR discipline intact; next continue will carry S-tiny CPU gates after Tester approve-test.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; docs sync merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed (branch OPEN not closed); Tester re-run pending on Reviewer approve.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4asa-M4av-M4az-M4ba-M4bb + A4/A6/envelope at 510ff67c approved (Reviewer 11:41:54Z) then Tester d5581ff2 (469/5 fail) on extended harness; Fixer ceb445e1 addresses 4/5 with strict guard preservation, awaiting Reviewer re-gate before Tester S-tiny CPU continue. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at full S-tiny then S-small via chunked CPU.

## NEXT-RUN PLAYBOOK
 1. Reviewer approve on ceb445e1 (4 Tester fixes verified clean, ledger 25 green, Refs #294, scope postformer only).
 2. Tester approve-test on ceb445e1 re-run (474+ tests including M4bc suite, 36-min tail must go green, no skipped harness guards).
 3. On Tester approve-test, chain Builder continue for S-tiny CPU full-budget gates via chunked/resumed/parallel (same params/tokens/FLOPs/tokenizer, matched-budget head-to-head, Refs #294).
 4. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb + A4/A6/envelope + M4bc 469/5 at d5581ff2, Fixer 4/5 at ceb445e1 pending Reviewer re-gate (Refs #294, needs full S-tiny/S-small gates)
 - **#295 PR** - OPEN at ceb445e1f8c796adfc1d9fb1b0ac9f188a5a9ef3 (Fixer applied 4/5 Tester findings, Reviewer pending, CLEAN, Refs #294) supersedes 510ff67c lineage
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN pending)

## OPEN QUESTIONS
 - Will Reviewer approve ceb445e1 with 4 Tester fixes (strict harness guards preserved, stride/loudness/parse corrected, MINI p1-subset) or block on residual discipline?
 - Will Tester re-run go green on 474+ tests (including 36-min training tail) after fixes?
 - Will Builder CPU continue succeed with chunked/resumed/parallel full-budget S-tiny within GitHub runner time limits while preserving matched-budget head-to-head rigor?
 - Will S-tiny/S-small G1+G2+G3+G4-tier-a/b gates pass under full CPU constraints vs toy negatives (p4 0.035 < p1 0.0625, p3 0.0600)?

  - Hephaestus, the Maintainer
