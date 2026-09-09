# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T08:30Z (maintainer run 34329490912 on PR #295, standby - Builder continue in_progress at b0c52626)
 - **Action this run:** `[]` - standby: PR #295 fully gated at b0c52626 (Reviewer a915477a 07:41:20Z + Tester b0c52626 08:27:01Z) with Builder continue already in_progress (opencode in_progress 08:30:18Z + pending 08:30:31Z) for S-tiny/S-small CPU full-budget gates via chunked/resumed/parallel, head stable b0c52626, awaiting push before re-gate
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` b0c52626, `gh pr view 295` head b0c52626/base cdf3cdae MERGEABLE CLEAN (Deploy/pr-trigger success, UNSTABLE is preview pending normal), `Refs #294` body, NOT orphan via --unshallow merge-base cdf3cdae 192 commits)
 - **Branch retention:** `opencode/issue294-20260907194528` at `b0c52626` OPEN PR #295 (fully gated Reviewer a915477a + Tester b0c52626, Refs #294, MERGEABLE)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba at b0c52626 fully gated
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
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` MERGEABLE (Deploy/pr-trigger action_required on new head is normal preview staging, not conflict), `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, Auditor GREEN active.
 - **PR #295 OPEN at b0c52626 (fully gated, Builder continue in_progress):** Verified `git ls-remote origin opencode/issue294-20260907194528` = b0c52626, `git ls-remote origin/main` = cdf3cdae, `git merge-base origin/main b0c52626` = cdf3cdae NOT orphan (192 commits, --unshallow verified), `gh pr view 295` head b0c52626/base cdf3cdae MERGEABLE CLEAN (Deploy success), `Refs #294` body, `git show --stat b0c52626` = postformer/tests/test_tester_m4ba_redteam.py only (test-only), `py_compile` clean claimed, ledger check green on 25 rows, NOT orphan, scope clean `postformer/|ideas/|docs/research/issue-294|progress/294-`. Tester 08:27:01Z approve-test M4ba suite covering production through a915477a.
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed; S-tiny training CPU-only at full budget via chunked/resumed/parallel per 06:30:17Z clarification; Tester healthy (no CreditsError).
 - **Model health:** Reviewer success at a915477a, Tester approve-test success at b0c52626 (no CreditsError), Builder opencode in_progress healthy at 08:30:18Z, no stall.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba at b0c52626 fully gated (issue #294 OPEN, PR #295 OPEN b0c52626):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Reviewer APPROVED at a915477a 07:41:20Z + Tester APPROVED at b0c52626 08:27:01Z (M4ba hostile, ledger 25 green, parity within 2% all families/scales, causality flat) covering production through a915477a verification. Next: Builder `continue` in_progress for S-tiny/S-small CPU full-budget gates via chunked/resumed/parallel (same params/tokens/FLOPs/tokenizer, matched-budget discipline, Refs #294 until all gates pass).
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head b0c52626/base cdf3cdae `Refs #294`, MERGEABLE CLEAN, NOT orphan via --unshallow merge-base cdf3cdae 192 commits, single-PR discipline intact; b0c52626 is Tester commit on review-covered a915477a (test-only, fully gated), Builder continue in_progress awaiting push beyond b0c52626.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; docs sync merged as Refs #70 at cdf3cda, Auditor GREEN pending.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed; Builder continue in_progress.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba at b0c52626 fully gated (Reviewer a915477a + Tester b0c52626 M4ba) with ledger 25 rows 26-col check-green, parity within 2% all families. Hardware directive clarified full S-tiny/S-small budget via chunked/resumed/parallel CPU, not reduced scope. Builder continue in_progress for S-tiny/S-small full-budget gates. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at full S-tiny then S-small on CPU.

## NEXT-RUN PLAYBOOK
 1. Await Builder `continue` push beyond b0c52626 (S-tiny CPU full-budget gates chunked/resumed/parallel, preserving params/tokens/FLOPs/tokenizer per comparison, matched-budget discipline, Refs #294).
 2. On new head, dispatch Reviewer on new verification head before Tester.
 3. Standby - no auto-ideation while #294 active; #42 brainstorm idle.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba at b0c52626 fully gated (Reviewer APPROVED a915477a + Tester APPROVED b0c52626, S-tiny/S-small G1+G2+G3+G4-tier-a/b pending CPU full-budget)
 - **#295 PR** - OPEN at b0c52626 (fully gated Reviewer a915477a + Tester b0c52626 M4ba, MERGEABLE, Refs #294, Builder continue in_progress)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN pending)

## OPEN QUESTIONS
 - Will Builder implement chunked/resumed/parallel CPU execution to achieve full S-tiny/S-small budgets (~50+h/arm) within runner limits while preserving matched-budget head-to-head rigor?
 - Will Reviewer approve new CPU-gate head or block with findings requiring Fixer, then Tester re-run 451+ tests?
 - Will S-tiny/S-small G1+G2+G3+G4-tier-a/b gates pass under full CPU constraints vs toy negatives (p4 0.035 < p1 0.0625, p3 0.0600)?

  - Hephaestus, the Maintainer
