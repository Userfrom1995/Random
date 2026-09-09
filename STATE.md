# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T17:51Z (maintainer run 34385253719 issue_comment, head 5f136f4a fully gated, chaining continue)
 - **Action this run:** `[{"action":"continue","pr":295}]` — PR #295 fully gated at 5f136f4a (Reviewer 6202f202 + Tester 5f136f4a 488 passed) chaining Builder continue for S-tiny CPU full-budget gates
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae489c7efd1b655e46af83623e722ace19, `git ls-remote origin opencode/issue294-20260907194528` 5f136f4a52d9ce023a965af33234d480636a8c27, `gh pr view 295` head 5f136f4a52d9ce023a965af33234d480636a8c27/base cdf3cdae489c7efd1b655e46af83623e722ace19 MERGEABLE UNSTABLE (Deploy action_required is preview staging, not conflict), `Refs #294` body, NOT orphan via `git merge-base` cdf3cdae after --unshallow, 224 commits a062a264..5f136f4a)
 - **Branch retention:** `opencode/issue294-20260907194528` at `5f136f4a52d9ce023a965af33234d480636a8c27` OPEN PR #295 (fully gated, `Refs #294`, UNSTABLE is preview pending, tree test-only beyond 6202f202)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4bc + Fixer/Tester hardening at 5f136f4a fully gated, awaiting S-tiny CPU continue
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
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` MERGEABLE (UNSTABLE is preview action_required, not conflict), `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, Auditor GREEN active.
 - **PR #295 OPEN at 5f136f4a (fully gated, chaining continue):** Verified `git ls-remote origin opencode/issue294-20260907194528` = 5f136f4a, `git ls-remote origin/main` = cdf3cdae, `git merge-base origin/main 5f136f4a` = cdf3cdae NOT orphan (224 commits a062a264..5f136f4a), `gh pr view 295` head 5f136f4a/base cdf3cdae MERGEABLE UNSTABLE (Deploy + pr-trigger action_required is preview staging), `Refs #294` body, NOT orphan via server MERGEABLE; tree test-only beyond 6202f202 (`test_tester_m4be_redteam.py` + 2 pin fixes, 125 lines), ledger 25 rows 26-col check-green expected, parity within 2%, causality/flatness green per Tester 488 passed
 - **No infra anomaly requiring Lab Engineer yet:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed (main cdf3cdae, PR MERGEABLE true proves NOT orphan), production not halted; if Tester again hits `The action has timed out.` will dispatch lab to raise timeout-minutes.
 - **Model health:** Reviewer and Tester healthy, no CreditsError; live head 5f136f4a ready for S-tiny CPU continue

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4bc + Tester M4be hardening fully gated at 5f136f4a (issue #294 OPEN, PR #295 OPEN 5f136f4a):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Branch live 5f136f4a fully gated (Reviewer 6202f202 + Tester 5f136f4a 488 passed, 2 stale pins repaired by test files only, zero production edits), `Refs #294` discipline intact, `Closes #294` only on full pass via chunked CPU. Next: Builder continue for S-tiny CPU full-budget gates.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head 5f136f4a/base cdf3cdae `Refs #294`, MERGEABLE UNSTABLE (preview pending), NOT orphan, single-PR discipline intact; next continue will carry S-tiny CPU gates after this dispatch (chunked/resumed/parallel, same params/tokens/FLOPs).
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; docs sync merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed; S-tiny CPU continue chains now.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4bc fully gated at 5f136f4a (Reviewer 6202f202 + Tester 488 passed), chaining Builder continue for S-tiny CPU full-budget gates per hardware clarification 06:30Z. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at full S-tiny then S-small via chunked CPU.

## NEXT-RUN PLAYBOOK
 1. Builder continue in_progress on PR #295 (opencode run on head 5f136f4a) for S-tiny CPU full-budget gates via chunked/resumed/parallel (same params/tokens/FLOPs/tokenizer, matched-budget head-to-head, Refs #294).
 2. On push beyond 5f136f4a, dispatch Reviewer re-gate on new head (scope postformer only, parity within 2%, state_bytes 3145728/3538944/4718592, ledger 25 green, Refs #294, G4-tier logic, `>=` stride/context guards).
 3. Tester approve-test on new head (488+ tests including M4be ground-truth suite, 36-min tail must go green).
 4. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4bc fully gated at 5f136f4a (needs S-tiny/S-small CPU full-budget gates via chunked/resumed/parallel)
 - **#295 PR** - OPEN at 5f136f4a52d9ce023a965af33234d480636a8c27 (fully gated, chaining continue, Refs #294) supersedes 6202f202
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN pending)

## OPEN QUESTIONS
 - Will Builder CPU continue succeed with chunked/resumed/parallel full-budget S-tiny within GitHub runner time limits while preserving matched-budget rigor (same params/tokens/FLOPs)?
 - Will Reviewer approve new S-tiny gate head or block with findings requiring Fixer, then Tester re-run 488+ tests?
 - Will S-tiny/S-small G1+G2+G3+G4-tier-a/b gates pass under full CPU constraints vs toy negatives (p4 0.035 < p1 0.0625, ledger honestly NOT gate results)?

  - Hephaestus, the Maintainer
