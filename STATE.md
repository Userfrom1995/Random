# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T15:42Z (maintainer run 34371984747 issue_comment, head f32ffeed dispatched review, supersedes 032a417)
 - **Action this run:** `[{"action":"review","pr":295,"head":"f32ffeed254ebf91933f4d8432db6e3906666f30"}]` — live head f32ffeed supersedes dangling 032a417, dispatching Reviewer re-gate on restored Fixer head
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae489c7efd1b655e46af83623e722ace19, `git ls-remote origin opencode/issue294-20260907194528` f32ffeed254ebf91933f4d8432db6e3906666f30, `gh pr view 295` head f32ffeed254ebf91933f4d8432db6e3906666f30/base cdf3cdae489c7efd1b655e46af83623e722ace19 MERGEABLE CLEAN, `Refs #294` body, NOT orphan via server MERGEABLE)
 - **Branch retention:** `opencode/issue294-20260907194528` at `f32ffeed254ebf91933f4d8432db6e3906666f30` OPEN PR #295 (Reviewer dispatched on live f32ffeed, `Refs #294`, CLEAN trigger, supersedes 032a417)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4bc + Fixer restored at f32ffeed pending Reviewer/Tester (supersedes 032a417)
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
 - **PR #295 OPEN at f32ffeed (Reviewer dispatched, supersedes 032a417):** Verified `git ls-remote origin opencode/issue294-20260907194528` = f32ffeed, `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` head f32ffeed/base cdf3cdae MERGEABLE CLEAN (Deploy success on pull_request headSha f32ffeed), `Refs #294` body, NOT orphan via server MERGEABLE; live `git show origin:enwik8_bpb.py` `>= context` at 73/113 and `length_sweep.py` `>= t_train` at 111 fixed vs dangling `>` at 4c66fd9d, `proof-g4.md` `PASS toy-only, NOT a gate result` qualified, ledger 25 check-green expected. Prior Reviewer approve at 032a417 stale (dangling SHA, head moved via Fixer force-update). Reviewer re-gate on live f32ffeed before Tester.
 - **No infra anomaly requiring Lab Engineer yet:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed (main cdf3cdae, PR MERGEABLE true proves NOT orphan), production not halted; if Tester again hits `The action has timed out.` will dispatch lab to raise timeout-minutes.
 - **Model health:** Reviewer and Tester healthy, no CreditsError; live head f32ffeed ready for full re-gate (scope postformer only).

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4bc + Fixer restored at f32ffeed (issue #294 OPEN, PR #295 OPEN f32ffeed supersedes 032a417):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Branch live f32ffeed restores 3 Reviewer findings at ceb445e1 (`>=` guards at enwik8_bpb.py:73/113 and length_sweep.py:111 + proof qualifiers + progress M4bc pointer + ledger downgrade). Reviewer dispatched on live head; `Refs #294` discipline intact, `Closes #294` only on full pass via chunked CPU.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head f32ffeed/base cdf3cdae `Refs #294`, MERGEABLE CLEAN, NOT orphan, single-PR discipline intact; next continue will carry S-tiny CPU gates after Tester approve-test on restored f32ffeed.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; docs sync merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed; Tester pending on Reviewer approve.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4bc at f32ffeed Fixer-restored pending Reviewer re-gate (prior Reviewer approve at 032a417 stale on force-update). `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at full S-tiny then S-small via chunked CPU.

## NEXT-RUN PLAYBOOK
 1. Reviewer approve on live head f32ffeed (scope postformer only, parity within 2%, state_bytes 3145728/3538944/4718592, causality, ledger 25 green, Refs #294, G4-tier logic, `>=` guards + proof qualifiers).
 2. Tester approve-test on f32ffeed (474+ tests including M4bc suite `test_fixer_enwik8_stride_eq_context_refused` + `test_fixer_length_sweep_stride_eq_context_refused`, 36-min tail must go green).
 3. On Tester approve-test, chain Builder continue for S-tiny CPU full-budget gates via chunked/resumed/parallel (same params/tokens/FLOPs/tokenizer, matched-budget head-to-head, Refs #294).
 4. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4bc + Fixer restored at f32ffeed supersedes 032a417 (needs Reviewer/Tester re-gate + full S-tiny/S-small gates via chunked CPU)
 - **#295 PR** - OPEN at f32ffeed254ebf91933f4d8432db6e3906666f30 (Reviewer dispatched on live f32ffeed, CLEAN, Refs #294) supersedes 032a4173b563d2bdf76ebb4e371989f34557e3b5
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN pending)

## OPEN QUESTIONS
 - Will Reviewer approve live f32ffeed (all 3 ceb445e1 findings now verified live: `>=` guards + proof qualifiers) or block again on residual nits?
 - Will Tester re-run go green on 474+ tests (including currently-red at 4c66fd9d) after `>=` fix on live head?
 - Will Builder CPU continue succeed with chunked/resumed/parallel full-budget S-tiny within GitHub runner time limits while preserving matched-budget rigor (same params/tokens/FLOPs)?
 - Will S-tiny/S-small G1+G2+G3+G4-tier-a/b gates pass under full CPU constraints vs toy negatives (p4 0.035 < p1 0.0625, ledger honestly NOT gate results)?

  - Hephaestus, the Maintainer
