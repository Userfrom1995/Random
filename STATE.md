# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T18:10Z (maintainer run 34387351586 issue_comment, parallelization order 18:10:01Z, head 053fac6c lab dispatched concurrent with Tester)
 - **Action this run:** `[{"action":"lab","issue":294}]` — per binding parallelization order 18:10:01Z, dispatching Lab Engineer on #294 to ship chunked CPU training workflow + Builder resume support in train.py (new files only, no gated changes), concurrent with Tester re-gate `34386818174` in_progress on 053fac6c
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae489c7efd1b655e46af83623e722ace19, `git ls-remote origin opencode/issue294-20260907194528` 053fac6cb27957df225d61b2a3665ed6b63156a3, `gh pr view 295` head 053fac6cb27957df225d61b2a3665ed6b63156a3/base cdf3cdae489c7efd1b655e46af83623e722ace19 MERGEABLE CLEAN, `Refs #294` body, NOT orphan via server MERGEABLE, 225 commits a062a264..053fac6c)
 - **Branch retention:** `opencode/issue294-20260907194528` at `053fac6cb27957df225d61b2a3665ed6b63156a3` OPEN PR #295 (Reviewer APPROVED 18:04:43Z at 053fac6c, Tester in_progress 34386818174, Lab dispatched per 18:10:01Z order, `Refs #294`, CLEAN, awaiting Tester approve-test then chunked S-tiny continue)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4bc + Fixer/Tester hardening at 5f136f4a fully gated, M4bd/M4be verification at 053fac6c Reviewer-approved 18:04:43Z + Tester in_progress, Lab infra for chunked CPU pending per 18:10:01Z
 - **HARDWARE DIRECTIVE (2026-09-08T20:40:31Z, supreme, via #294) - CLARIFIED 2026-09-09T06:30:17Z via #294 (supreme):** No GPU runner is coming. All S-tiny/S-small training must run on standard GitHub CPU runners. Training scope is **not** reduced: same S-tiny/S-small budgets, same matched-budget discipline (params, training FLOPs/tokens, optimizer, tokenizer/context). Change the execution method (chunked, resumed, parallel), not the experiment size. Prior "reduced steps/tokens, micro-scales" interpretation is superseded - Builder must redesign for CPU feasibility via chunked/resumed/parallel execution while preserving full-budget head-to-head rigor and Refs #294 until all four gates pass. `Closes #294` only on G1+G2+G3+G4-tier-a/b green at full budget.
 - **PARALLELIZATION ORDER (2026-09-09T18:10:01Z, supreme, via #294):** Lab Engineer to ship the chunked CPU training workflow and Builder resume support in train.py **now**, concurrent with the Tester re-gate. They do not wait for the gate - new files only, no changes to gated code. Training launches the moment Tester greens. Dispatched this run as `lab` on #294 concurrent with Tester 34386818174 in_progress on 053fac6c.
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** Update README.md + index.html to reflect live shipped state - COMPLETE at cdf3cda (PR #293 MERGED as Refs #70, verified README 48-54 + index.html cards Shipped).
 - **LAB RIGOR GATES (2026-09-07T15:47Z, via e9656dd8):** Brutal rigor, binding performance gates, subagent orchestration charter merged to main.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z, supreme, via #277):** 6 ingestion defects + 4 UI mandates - RESOLVED at 0944bb63 (still live at cdf3cda).
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Dual-frontier standards ratified and verified on M4.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z, supreme, via #277):** Folio at /folio/ shipped M1-M3 + M4 final SHIPPED at 0944bb63. Issue #277 now CLOSED.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z, supreme, via #130):** Prism finished-at-ceiling closed.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Tabula at /tabula/ SHIPPED at 23aeb5ce (live at cdf3cda).
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Sextant at /sextant/ SHIPPED at 1e06b5b (live at cdf3cda).

## CRITICAL INFRASTRUCTURE STATE
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` MERGEABLE CLEAN (Deploy success on 053fac6c pull_request, opencode-review success at 053fac6c 18:04:43Z), `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, Auditor GREEN active.
 - **PR #295 OPEN at 053fac6c (Reviewer APPROVED 18:04:43Z + Tester in_progress 34386818174, Lab dispatched):** Verified `git ls-remote origin opencode/issue294-20260907194528` = 053fac6c, `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` head 053fac6c/base cdf3cdae MERGEABLE CLEAN, `Refs #294` body, NOT orphan via server MERGEABLE; tree doc-only `progress/294-post-transformer-sequence-architecture.md` beyond 5f136f4a (M4bd/M4be verification, ledger 25 green, py_compile clean, zero forward_chunk in shipped), parity within 2% preserved, Reviewer approve at 053fac6c covers full M1-M4be (330 files postformer/|ideas/|docs/research/issue-294|progress/294-, zero infra touch), Tester re-gate 34386818174 in_progress for 488+ tests including M4bd/M4be ground-truth, Lab concurrent for chunked workflow per 18:10:01Z (new files only)
 - **No infra anomaly requiring emergency yet:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed (main cdf3cdae, PR MERGEABLE true proves NOT orphan), production not halted; if Tester hits `The action has timed out.` will dispatch lab to raise timeout-minutes. This run dispatches lab for chunked workflow per parallel order, not per failure.
 - **Model health:** Reviewer and Tester healthy, no CreditsError; live head 053fac6c Reviewer-approved, Tester in_progress, Lab dispatched concurrent

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4bc + Tester M4be hardening fully gated at 5f136f4a + M4bd/M4be verification at 053fac6c Reviewer-approved 18:04:43Z + Tester in_progress + Lab concurrent (issue #294 OPEN, PR #295 OPEN 053fac6c):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Branch live 053fac6c doc-only beyond fully-gated 5f136f4a (Reviewer 6202f202 + Tester 5f136f4a 488 passed; now Reviewer 053fac6c 18:04:43Z approved), `Refs #294` discipline intact, `Closes #294` only on full pass via chunked CPU. Per 18:10:01Z order, Lab Engineer now ships chunked CPU workflow + train.py resume support (new files only, no gated changes) concurrent with Tester re-gate; training launches the moment Tester greens.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head 053fac6c/base cdf3cdae `Refs #294`, MERGEABLE CLEAN, NOT orphan, single-PR discipline intact; Lab infra lands concurrent with Tester, next continue will carry S-tiny CPU full-budget gates after Tester greens per parallel order.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; docs sync merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed; Lab dispatched per 18:10:01Z, Tester in_progress on 053fac6c.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4bc fully gated at 5f136f4a (Reviewer 6202f202 + Tester 488 passed) plus doc-only M4bd/M4be verification at 053fac6c Reviewer-approved 18:04:43Z with Tester 34386818174 in_progress, Lab Engineer dispatched concurrent per 18:10:01Z parallelization order for chunked/resumed/parallel scaffolding (new files only). `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at full S-tiny then S-small via chunked CPU once Tester greens.

## NEXT-RUN PLAYBOOK
 1. Lab Engineer lands chunked CPU workflow + train.py resume on PR #295 (new files only, no gated changes) — dispatched this run, await push beyond 053fac6c.
 2. Tester approve-test on 053fac6c (488+ tests including M4bd/M4be ground-truth, 36-min tail) — in_progress 34386818174, await approve-test; no re-dispatch while in_progress.
 3. Reviewer re-gate if Lab push lands on new head (verify new files only, no gated drift), else standby.
 4. Builder continue on PR #295 for S-tiny CPU full-budget gates via chunked/resumed/parallel (same params/tokens/FLOPs/tokenizer, matched-budget head-to-head, Refs #294) — launches the moment Tester greens per 18:10:01Z.
 5. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4bc fully gated at 5f136f4a + M4bd/M4be verification at 053fac6c Reviewer-approved + Tester in_progress + Lab concurrent for chunked CPU per 18:10:01Z (needs S-tiny/S-small CPU full-budget gates via chunked/resumed/parallel)
 - **#295 PR** - OPEN at `053fac6cb27957df225d61b2a3665ed6b63156a3` (Reviewer APPROVED 18:04:43Z, Tester in_progress 34386818174, Lab dispatched concurrent, Refs #294) supersedes 5f136f4a
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN pending)

## OPEN QUESTIONS
 - Will Lab Engineer land chunked CPU workflow + train.py resume as new files only (no gated drift) on PR #295 before or concurrent with Tester approve-test?
 - Will Tester re-run 488+ tests green on 053fac6c including M4bd/M4be ground-truth before approve-test (in_progress 34386818174)?
 - Will Builder CPU continue succeed with chunked/resumed/parallel full-budget S-tiny within GitHub runner time limits while preserving matched-budget rigor (same params/tokens/FLOPs)?
 - Will S-tiny/S-small G1+G2+G3+G4-tier-a/b gates pass under full CPU constraints vs toy negatives (p4 0.035 < p1 0.0625, ledger honestly NOT gate results)?

  - Hephaestus, the Maintainer
