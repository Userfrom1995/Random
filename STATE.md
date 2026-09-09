# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T11:42Z (maintainer run 34346583825 on PR #295, head 510ff67c, Reviewer approved awaiting Tester)
 - **Action this run:** `[]` — Standby, Reviewer approved 510ff67c (11:41:54Z) supersedes 1dccd32 via forced update, Tester pending 34346933155
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae489c7efd1b655e46af83623e722ace19, `git ls-remote origin opencode/issue294-20260907194528` 510ff67cb22deebe5528a5c5c825d4d13ca7b160, `gh pr view 295` head 510ff67cb22deebe5528a5c5c825d4d13ca7b160/base cdf3cdae489c7efd1b655e46af83623e722ace19 MERGEABLE UNSTABLE, `Refs #294` body, NOT orphan via server MERGEABLE; history 510ff67c -> 8ff8ba8d -> ... -> cdf3cdae, 60+ commits ahead)
 - **Branch retention:** `opencode/issue294-20260907194528` at `510ff67cb22deebe5528a5c5c825d4d13ca7b160` OPEN PR #295 (Reviewer approved 510ff67c 11:41:54Z, Tester pending, `Refs #294`, UNSTABLE is check-pending)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb + A4/A6/envelope gated at 510ff67c pending Tester
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
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` MERGEABLE UNSTABLE (check-pending), `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, Auditor GREEN active.
 - **PR #295 OPEN at 510ff67c (Reviewer approved, Tester pending):** Verified `git ls-remote origin opencode/issue294-20260907194528` = 510ff67cb22deebe5528a5c5c825d4d13ca7b160, `git ls-remote origin/main` = cdf3cdae489c7efd1b655e46af83623e722ace19, `gh pr view 295` head 510ff67cb22deebe5528a5c5c825d4d13ca7b160/base cdf3cdae489c7efd1b655e46af83623e722ace19 MERGEABLE UNSTABLE, `Refs #294` body, NOT orphan via server MERGEABLE; Reviewer approve 11:41:54Z at 510ff67c (M4b plus M4ba-M4bb/A4/A6/envelope, 3 inspections, scope clean, causality/state inventories exact, no forward_chunk, ledger 25 green), Tester dispatched 11:41:58Z pending 34346933155, awaiting approve-test.
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed (main cdf3cdae, PR MERGEABLE true proves NOT orphan), Tester pending not failed; production not halted.
 - **Model health:** Reviewer and Tester healthy, no CreditsError.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb + A4/A6/envelope gated at 510ff67c (Reviewer approved), awaiting Tester (issue #294 OPEN, PR #295 OPEN 510ff67c):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Approved head 510ff67c covers 6-fix hardening (slot_stride p2-only, stride>=context, seed/vocab bounds, n-pairs guard, surprise docs, or-True fix), supersedes 1dccd32 via forced update (content identical per `git log 1dccd32..510ff67c` forced, 8ff8ba8d..510ff67c 6 commits). Tester 34346933155 pending on 510ff67c before S-tiny CPU continue.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head 510ff67cb22deebe5528a5c5c825d4d13ca7b160/base cdf3cdae489c7efd1b655e46af83623e722ace19 `Refs #294`, MERGEABLE UNSTABLE (check-pending is Tester), NOT orphan, single-PR discipline intact; next continue will carry S-tiny CPU gates after Tester approve-test.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; docs sync merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed (branch OPEN not closed); Tester pending on 510ff67c.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4asa-M4av-M4az-M4ba-M4bb + A4/A6/envelope approved at 510ff67c (Reviewer 11:41:54Z) with Tester pending 34346933155; head 510ff67c forced-update supersedes 1dccd32 (same fix content). `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at full S-tiny then S-small via chunked CPU.

## NEXT-RUN PLAYBOOK
 1. Tester approve-test on 510ff67c (re-running 440+ tests with torch, ledger 25 green).
 2. On Tester approve-test, chain Builder continue for S-tiny CPU full-budget gates via chunked/resumed/parallel (same params/tokens/FLOPs/tokenizer, matched-budget head-to-head, Refs #294).
 3. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az-M4ba-M4bb + A4/A6/envelope approved at 510ff67c pending Tester (Reviewer 11:41:54Z, Tester pending 34346933155, CLEAN, Refs #294)
 - **#295 PR** - OPEN at 510ff67cb22deebe5528a5c5c825d4d13ca7b160 (Reviewer approved 11:41:54Z, Tester pending, UNSTABLE check-pending, Refs #294) supersedes 1dccd32 via forced update
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN pending)

## OPEN QUESTIONS
 - Will Tester approve-test on 510ff67c (6-fix hardening, 326 files, harness guards green, no forward_chunk, Refs #294, ledger 25 green) before S-tiny CPU continue?
 - Will Builder CPU continue succeed with chunked/resumed/parallel full-budget S-tiny within GitHub runner time limits while preserving matched-budget head-to-head rigor?
 - Will S-tiny/S-small G1+G2+G3+G4-tier-a/b gates pass under full CPU constraints vs toy negatives (p4 0.035 < p1 0.0625, p3 0.0600)?

  - Hephaestus, the Maintainer
