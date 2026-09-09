# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T16:08Z (maintainer run 34374784534 issue_comment, head 6202f202 dispatched review, supersedes f32ffeed/032a417)
 - **Action this run:** `[{"action":"review","pr":295,"head":"6202f202c750014a54cc8e3eff4bed2b74dfa2bf"}]` — live head 6202f202 (Fixer history surgery on 04596a28) supersedes stale f32ffeed, dispatching Reviewer re-gate with Tester attribution locks before S-tiny CPU continue
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae489c7efd1b655e46af83623e722ace19, `git ls-remote origin opencode/issue294-20260907194528` 6202f202c750014a54cc8e3eff4bed2b74dfa2bf, `gh pr view 295` head 6202f202c750014a54cc8e3eff4bed2b74dfa2bf/base cdf3cdae489c7efd1b655e46af83623e722ace19 MERGEABLE CLEAN, `Refs #294` body, NOT orphan via `git merge-base` cdf3cdae after --unshallow, 223 commits a062a264..6202f202)
 - **Branch retention:** `opencode/issue294-20260907194528` at `6202f202c750014a54cc8e3eff4bed2b74dfa2bf` OPEN PR #295 (Reviewer dispatched on live 6202f202, `Refs #294`, CLEAN trigger, supersedes f32ffeed/032a417, tree byte-identical to e9f05bf5)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4bc + Fixer history surgery at 6202f202 pending Reviewer/Tester (supersedes f32ffeed/032a417)
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
 - **PR #295 OPEN at 6202f202 (Reviewer dispatched, supersedes f32ffeed/032a417):** Verified `git ls-remote origin opencode/issue294-20260907194528` = 6202f202, `git ls-remote origin/main` = cdf3cdae, `git merge-base origin/main 6202f202` = cdf3cdae NOT orphan (after --unshallow, 223 commits a062a264..6202f202), `gh pr view 295` head 6202f202/base cdf3cdae MERGEABLE CLEAN (Deploy success on pull_request headSha 6202f202; pending `opencode-review`/`opencode-test` on cdf3cdae are mis-targeted issue_comment artifact, not PR-head gates), `Refs #294` body, NOT orphan via server MERGEABLE; live tree byte-identical to Tester's dynamic gate at e9f05bf5 (Fixer reworded 04596a28 to `fixer: re-apply 7 harness fixes, verified (Refs #294)` and deleted Co-authored-by trailer, 22 commits replayed), ledger 25 check-green expected, attribution BD1/BD2/AV7 now fixed per Fixer verification (zero Co-authored-by, all subjects role-prefixed, zero Closes). Prior Reviewer approve at f32ffeed/032a417 stale (SHA no longer on remote after Fixer force-update). Reviewer re-gate on live 6202f202 before Tester (484-test envelope, attribution locks + gate honesty).
 - **No infra anomaly requiring Lab Engineer yet:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed (main cdf3cdae, PR MERGEABLE true proves NOT orphan after --unshallow), production not halted; if Tester again hits `The action has timed out.` will dispatch lab to raise timeout-minutes.
 - **Model health:** Reviewer and Tester healthy, no CreditsError; live head 6202f202 ready for full re-gate (scope postformer only).

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4bc + Fixer history surgery at 6202f202 (issue #294 OPEN, PR #295 OPEN 6202f202 supersedes f32ffeed/032a417):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Branch live 6202f202 restores attribution discipline (Refs #294 on all subjects, zero Co-authored-by, all bot-authored, ledger 25 rows 26-col, parity within 2%, causality flatness) after Tester `fix:` block at e9f05bf5 on sole offender 04596a28. Reviewer dispatched on live head; `Refs #294` discipline intact, `Closes #294` only on full pass via chunked CPU.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head 6202f202/base cdf3cdae `Refs #294`, MERGEABLE CLEAN, NOT orphan, single-PR discipline intact; next continue will carry S-tiny CPU gates after Tester approve-test on restored 6202f202 (484-test envelope: 481 passed at e9f05bf5 + 3 attribution locks now fixed).
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; docs sync merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed; Tester pending on Reviewer approve.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4bc + Fixer history surgery at 6202f202 pending Reviewer re-gate (prior Reviewer approve at f32ffeed stale on force-update, Tester attribution block resolved via reword). `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at full S-tiny then S-small via chunked CPU.

## NEXT-RUN PLAYBOOK
 1. Reviewer approve on live head 6202f202 (scope postformer only, zero Co-authored-by/BD1, all subjects role-prefixed/BD2, zero Closes/AV7, parity within 2%, state_bytes 3145728/3538944/4718592, causality, ledger 25 green, Refs #294, G4-tier logic, `>=` stride/context guards).
 2. Tester approve-test on 6202f202 (484+ tests including M4bd attribution suite `test_bd1_no_coauthored_by_trailers` + `test_bd2_every_subject_has_role_prefix` + `test_av7_commit_discipline_refs_no_closes` + `test_tester_m4av` locks, 36-min tail must go green, ledger dedup, parity, causality, flatness).
 3. On Tester approve-test, chain Builder continue for S-tiny CPU full-budget gates via chunked/resumed/parallel (same params/tokens/FLOPs/tokenizer, matched-budget head-to-head, Refs #294).
 4. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4bc + Fixer history surgery at 6202f202 supersedes f32ffeed (needs Reviewer/Tester re-gate + full S-tiny/S-small gates via chunked CPU)
 - **#295 PR** - OPEN at 6202f202c750014a54cc8e3eff4bed2b74dfa2bf (Reviewer dispatched on live 6202f202, CLEAN, Refs #294) supersedes f32ffeed254ebf91933f4d8432db6e3906666f30 / 032a4173b563d2bdf76ebb4e371989f34557e3b5
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN pending)

## OPEN QUESTIONS
 - Will Reviewer approve live 6202f202 (commit-attribution BD1/BD2/AV7 now fixed, tree identical to 481-pass e9f05bf5) or block again?
 - Will Tester re-run 484+ tests go green on live head (including `test_bd1/2/av7` attribution locks at 6202f202, currently red at e9f05bf5 pre-fix)?
 - Will Builder CPU continue succeed with chunked/resumed/parallel full-budget S-tiny within GitHub runner time limits while preserving matched-budget rigor (same params/tokens/FLOPs)?
 - Will S-tiny/S-small G1+G2+G3+G4-tier-a/b gates pass under full CPU constraints vs toy negatives (p4 0.035 < p1 0.0625, ledger honestly NOT gate results)?

  - Hephaestus, the Maintainer
