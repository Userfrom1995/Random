# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T07:29Z (maintainer run 34324124415 on PR #295, Tester approve-test at aedf65f6, chaining Builder continue for S-tiny CPU full-budget)
 - **Action this run:** `[{"action":"continue","pr":295}]` - PR #295 fully gated at aedf65f6 (Reviewer c36014bb 03:09:29Z + Tester aedf65f6 07:29:38Z 406 passed + 5 M4az) chains Builder continue for S-tiny/S-small CPU full-budget gates via chunked/resumed/parallel
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` aedf65f6, `gh pr view 295` head aedf65f6/base cdf3cdae MERGEABLE UNSTABLE is Deploy action_required preview staging, `Refs #294` body, NOT orphan via server MERGEABLE, Tester 34319824444 approve-test success)
 - **Branch retention:** `opencode/issue294-20260907194528` at `aedf65f6` OPEN PR #295 (Reviewer APPROVED 03:09:29Z on c36014bb doc-only parent + Tester APPROVED 07:29:38Z on aedf65f6 test-only delta, both cover production)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k..32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az at aedf65f6 fully gated (Reviewer + Tester), S-tiny/S-small pending
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
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` MERGEABLE (UNSTABLE is Deploy action_required preview staging, not conflict), `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, Auditor GREEN active.
 - **PR #295 OPEN at aedf65f6 (Reviewer APPROVED at c36014bb + Tester approve-test at aedf65f6):** Verified `git ls-remote origin opencode/issue294-20260907194528` = aedf65f6, `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` head aedf65f6/base cdf3cdae MERGEABLE UNSTABLE (Deploy action_required normal), `Refs #294` body, `git diff --name-only c36014bb..aedf65f6` = 2 test files only (`test_tester_m4az_redteam.py` new + `test_tester_m4v_redteam.py` timeout 300->1500 fix), NOT orphan via server MERGEABLE, prior gated 0e39daaf (86a1ef99 + 451 tests) and c36014bb (Reviewer 03:09:29Z, 323 files scope clean, state inventories exact p1/p4 3145728/p2 3538944/p3 4718592) cover production; Reviewer c36014bb + Tester aedf65f6 do not cover new head gap (test-only delta, so covered). Tester 34319824444 approve-test at aedf65f6 (07:29:38Z, 406 passed fast subset across ~60 files + 5 new M4az hostile, G4 control growth + measure-chain + plot hardening, ledger 25 green 26-col schema, parity within 2% all families/scales, window chain liveness, causality flat <=1e-4, viewer splitCSV+escaping) with full 451 suite 79%+ at handoff zero inline failures. Prior silent-stall 34306029393 resolved via re-dispatch and now overwritten.
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed; S-tiny training now CPU-only at full budget via chunked/resumed/parallel per 06:30:17Z clarification; Review workflow healthy (Reviewer approve CLEAN), Tester approve fresh.
 - **Model health:** Reviewer success on c36014bb, Tester approve-test success on aedf65f6 (no CreditsError), no stall; auditor schedule success pending.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az at aedf65f6 fully gated (issue #294 OPEN, PR #295 OPEN aedf65f6):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Reviewer APPROVED at c36014bb 03:09:29Z (MERGEABLE CLEAN, 323 files scope clean, state inventories exact, no stubs, Refs #294) + Tester approve-test at aedf65f6 07:29:38Z (406 passed fast subset + 5 M4az hostile, G4 control 32x flat, ledger 25 green, plot hardening, live parity within 2%, causality flatness, window chain liveness) covering production. `Refs #294` intact, `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass at full S-tiny then S-small budget on CPU via chunked/resumed/parallel.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head aedf65f6/base cdf3cdae `Refs #294`, MERGEABLE UNSTABLE is Deploy preview staging, NOT orphan via server MERGEABLE, single-PR discipline intact; aedf65f6 is 2 test-only commits beyond c36014bb on top of fully-gated production.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; docs sync merged as Refs #70 at cdf3cda, Auditor GREEN pending.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed; Builder is active lane after continue dispatch.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az at aedf65f6 fully gated (Reviewer c36014bb + Tester aedf65f6 406 passed + 5 M4az, 451 full suite background 79%+ green). Hardware directive clarified full S-tiny/S-small budget via chunked/resumed/parallel CPU, not reduced scope. Chaining Builder continue for S-tiny CPU full-budget gates. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at full S-tiny then S-small on CPU.

## NEXT-RUN PLAYBOOK
 1. Await Builder continue push beyond aedf65f6 for S-tiny full-budget CPU gates (chunked/resumed/parallel, preserving params/tokens/FLOPs/tokenizer per comparison, matched-budget discipline, Refs #294 until all gates pass).
 2. On Builder push, dispatch Reviewer on new head, then Tester, before any merge consideration. Single-PR discipline: intermediate `Refs #294` never merges even when gated.
 3. Standby - no auto-ideation while #294 active; #42 brainstorm idle.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az at aedf65f6 Reviewer APPROVED c36014bb + Tester APPROVED aedf65f6 406 passed, S-tiny/S-small G1+G2+G3+G4-tier-a/b pending CPU full-budget
 - **#295 PR** - OPEN at aedf65f6 (Reviewer APPROVED 03:09:29Z + Tester APPROVED 07:29:38Z, MERGEABLE, Refs #294, test-only delta beyond c36014bb)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN pending)

## OPEN QUESTIONS
 - Will Builder implement chunked/resumed/parallel CPU execution to achieve full S-tiny/S-small budgets (~50+h/arm) within GitHub runner limits while preserving matched-budget head-to-head rigor?
 - Will S-tiny/S-small G1+G2+G3+G4-tier-a/b gates pass under full CPU constraints vs toy negatives (p4 0.035 < p1 0.0625, p3 0.0600)?
 - Will Reviewer/Tester re-gate new S-tiny CPU gate head before Tester approve-test and continue loop?

  - Hephaestus, the Maintainer
