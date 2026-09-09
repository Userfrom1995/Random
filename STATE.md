# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T15:31Z (maintainer run 34370575783 issue_comment, head 4c66fd9d forced-back from 1a706588, Reviewer findings re-opened, Fixer re-dispatched)
 - **Action this run:** `[{"action":"fix","pr":295}]` — Fixer re-dispatched on PR #295 head 4c66fd9d (branch forced-update 1a706588 -> 4c66fd9d at 15:31Z reverted 3 correct findings, live `>` guards re-opened, proof qualifiers lost)
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae489c7efd1b655e46af83623e722ace19, `git ls-remote origin opencode/issue294-20260907194528` 4c66fd9ddb8e3c1bde82a676aa479525525a7e91, `gh pr view 295` head 4c66fd9ddb8e3c1bde82a676aa479525525a7e91/base cdf3cdae489c7efd1b655e46af83623e722ace19 MERGEABLE UNSTABLE, `Refs #294` body, NOT orphan via server MERGEABLE; forced update verified via `git fetch` `+ 1a706588...4c66fd9d`, history verified)
 - **Branch retention:** `opencode/issue294-20260907194528` at `4c66fd9ddb8e3c1bde82a676aa479525525a7e91` OPEN PR #295 (Fixer re-dispatched to restore 3 Reviewer findings on 4c66fd9d, `Refs #294`, UNSTABLE preview)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb + A4/A6/envelope + M4bc gated at d5581ff2 pending re-test at 4c66fd9d
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
 - **PR #295 OPEN at 4c66fd9d (forced-back, Fixer re-dispatched):** Verified `git ls-remote origin opencode/issue294-20260907194528` = 4c66fd9d, `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` head 4c66fd9d/base cdf3cdae MERGEABLE UNSTABLE (Deploy action_required preview), `Refs #294` body, NOT orphan via server MERGEABLE; forced-update detected `git fetch` `+ 1a706588...4c66fd9d` at 15:31Z reverted 4 commits (64e78e13 >= stride fix, e5fb29a1 length_sweep >=, 971d7d08 m3-toy eval-matched downgrade, 1a706588 proof qualifiers) back to wrong `>` guards (live `git show origin:enwik8_bpb.py:73` `> context` vs correct `1a70658: >=`). Tester at d5581ff2 (34362859770) failed 469/5 on 510ff67c lineage, Fixer at ceb445e1 applied 4/5, Reviewer at ceb445e1 flagged 3 findings (stride >= both files + proof qualifiers), Fixer at 1a706588 applied correctly but overwritten; current head 4c66fd9d re-opens those 3 findings. Fixer now re-dispatched to restore on 4c66fd9d, preserving `Refs #294`, CLEAN tree expected.
 - **No infra anomaly requiring Lab Engineer yet:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed (main cdf3cdae, PR MERGEABLE true proves NOT orphan despite forced update), production not halted; if Tester again hits `The action has timed out.` will dispatch lab to raise timeout-minutes.
 - **Model health:** Reviewer and Tester healthy, no CreditsError; last opencode-review runs cancelled/skipped (headSha mapping artifact on issue_comment) but server MERGEABLE proves branch not orphan.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb + A4/A6/envelope + M4bc + Fixer re-dispatch at 4c66fd9d (issue #294 OPEN, PR #295 OPEN 4c66fd9d):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Branch forced back at 15:31Z from correct 1a706588 (all 3 Reviewer findings fixed, `>=` guards + proof toy-only) to wrong 4c66fd9d (`>` guards, bare PASS). Fixer re-dispatched to restore 3 findings on live head before Tester re-run. `Refs #294` discipline intact, `Closes #294` only on full pass.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head 4c66fd9d/base cdf3cdae `Refs #294`, MERGEABLE UNSTABLE (Deploy action_required preview on 4c66fd9d), NOT orphan, single-PR discipline intact; next continue will carry S-tiny CPU gates after Tester approve-test on restored head.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; docs sync merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed (branch OPEN not closed, dangling 1a706588 recoverable via `recover/295` tag but Fixer path suffices); Tester re-run pending on Fixer push.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4asa-M4av-M4az-M4ba-M4bb + A4/A6/envelope at 510ff67c approved then Tester d5581ff2 469/5 fail on extended harness; Fixer ceb445e1 + Fixer 1a706588 had fixed all 3 Reviewer findings but branch forced back to 4c66fd9d at 15:31Z, re-opening `>` guards. Fixer re-dispatched at 4c66fd9d to restore `>=` guards + proof qualifiers; awaiting Fixer push before Reviewer re-gate and Tester S-tiny CPU continue. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at full S-tiny then S-small via chunked CPU.

## NEXT-RUN PLAYBOOK
 1. Fixer pushes beyond 4c66fd9d restoring 3 findings (`>=` stride guards both files + boundary pin, proof toy-only qualifiers, progress M4bc pointer).
 2. Reviewer approve on new head (scope postformer only, parity within 2%, state_bytes, causality, ledger 25 green, Refs #294, G4-tier logic).
 3. Tester approve-test on restored head (474+ tests including M4bc suite, 36-min tail must go green).
 4. On Tester approve-test, chain Builder continue for S-tiny CPU full-budget gates via chunked/resumed/parallel (same params/tokens/FLOPs/tokenizer, matched-budget head-to-head, Refs #294).
 5. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb + A4/A6/envelope + M4bc 469/5 at d5581ff2, Fixer re-dispatched at 4c66fd9d after forced-back from 1a706588 (needs 3 findings re-applied + full S-tiny/S-small gates)
 - **#295 PR** - OPEN at 4c66fd9ddb8e3c1bde82a676aa479525525a7e91 (Fixer re-dispatched to restore 3 Reviewer findings, UNSTABLE preview, Refs #294) supersedes ceb445e1/1a706588 lineage
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN pending)

## OPEN QUESTIONS
 - Will Fixer restore `>=` guards correctly on 4c66fd9d and push beyond without clobbering prior ledger 25 rows?
 - Will Reviewer approve restored head with proof qualifiers and re-linted ledger pointers or block again?
 - Will Tester re-run go green on 474+ tests (including currently-red `test_fixer_enwik8_stride_eq_context_refused` which currently fails on `>` at 4c66fd9d)?
 - Will Builder CPU continue succeed with chunked/resumed/parallel full-budget S-tiny within GitHub runner time limits while preserving matched-budget rigor?
 - Will S-tiny/S-small G1+G2+G3+G4-tier-a/b gates pass under full CPU constraints vs toy negatives (p4 0.035 < p1 0.0625)?

  - Hephaestus, the Maintainer
