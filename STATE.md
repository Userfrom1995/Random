# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T07:36Z (maintainer run 34324571802 on PR #295, dispatch Reviewer on new verification head a915477a)
 - **Action this run:** `[{"action":"review","pr":295,"head":"a915477ae8123a60ae6cb4e4791da1c7eb0b1bc8"}]` - PR #295 doc-only verification at a915477a (1 commit beyond fully-gated aedf65f6, ledger 25 check-green, py_compile clean, scope clean, NOT orphan) needs re-gate before Tester/continue for S-tiny CPU full-budget
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` a915477a, `gh pr view 295` head a915477a/base cdf3cdae MERGEABLE (Deploy/opencode-pr-trigger queued action_required on new head, normal preview staging), `Refs #294` body, NOT orphan via server MERGEABLE + prior --unshallow merge-base cdf3cdae)
 - **Branch retention:** `opencode/issue294-20260907194528` at `a915477a` OPEN PR #295 (Reviewer APPROVED 03:09:29Z on c36014bb + Tester APPROVED 07:29:38Z on aedf65f6 covering production; new head a915477a doc-only pending review)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k..32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az at a915477a verification pending review (prior aedf65f6 fully gated)
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
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` MERGEABLE (queued Deploy action_required on new head is normal preview staging, not conflict), `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, Auditor GREEN active.
 - **PR #295 OPEN at a915477a (Reviewer pending on new doc-only head, prior aedf65f6 fully gated):** Verified `git ls-remote origin opencode/issue294-20260907194528` = a915477a, `git ls-remote origin/main` = cdf3cdae, `gh pr view 295` head a915477a/base cdf3cdae MERGEABLE (Deploy/opencode-pr-trigger queued), `Refs #294` body, `git diff --name-only aedf65f6..a915477a` = progress doc only, `py_compile` clean claimed, `ledger check` green on 25 rows 26-col, NOT orphan via prior --unshallow merge-base cdf3cdae + server MERGEABLE, 324 changed files scope `postformer/|ideas/|docs/research/issue-294|progress/294-` clean. Prior gated aedf65f6 (Reviewer c36014bb 03:09Z 323 files scope clean p1/p4 3145728/p2 3538944/p3 4718592 + Tester aedf65f6 07:29Z 406 passed +5 M4az 451 full suite 79%+ green) covers production; new head doc-only pending review. Builder 34324557354 success at a915477a verification (NOT orphan).
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed; S-tiny training CPU-only at full budget via chunked/resumed/parallel per 06:30:17Z clarification; Review workflow healthy (prior approve CLEAN, new review queued), Tester pending after review.
 - **Model health:** Reviewer success on c36014bb, Tester approve-test success on aedf65f6 (no CreditsError), no stall; auditor schedule pending. New Reviewer dispatch queued 34324671056 on cdf3cdae artifact; explicit head-targeted review on a915477a ensures correct scope.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az at a915477a verification pending review (issue #294 OPEN, PR #295 OPEN a915477a):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Reviewer APPROVED at c36014bb 03:09:29Z + Tester APPROVED at aedf65f6 07:29:38Z (406 passed +5 M4az, ledger 25 green, parity within 2% all families/scales, causality flat) covering production through aedf65f6. New head a915477a is doc-only verification (M4az post-ledger, progress log) pending Reviewer re-gate (`Refs #294` intact, zero Closes, toy rows honestly labeled NOT gate results, G2/G3 empty by design, H4 NEGATIVE 0.035 < p1 0.0625 disclosed). Next after review: Tester on new head, then `continue` for S-tiny/S-small CPU full-budget gates via chunked/resumed/parallel.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head a915477a/base cdf3cdae `Refs #294`, MERGEABLE, Deploy/opencode-pr-trigger queued action_required (normal), NOT orphan via server MERGEABLE, single-PR discipline intact; a915477a is 1 doc-only commit beyond c36014bb/aedf65f6 fully-gated production.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; docs sync merged as Refs #70 at cdf3cda, Auditor GREEN pending.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed; Reviewer is active lane on new head a915477a.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az at a915477a verification pending review (prior aedf65f6 fully gated Reviewer c36014bb + Tester aedf65f6 406 passed +5 M4az, 451 suite 79%+). Hardware directive clarified full S-tiny/S-small budget via chunked/resumed/parallel CPU, not reduced scope. Awaiting Reviewer verdict on a915477a before Tester and S-tiny CPU full-budget continue. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at full S-tiny then S-small on CPU.

## NEXT-RUN PLAYBOOK
 1. Await Reviewer verdict on a915477a (doc-only verification, ledger 25 green, scope clean, NOT orphan, Refs #294). If `approve`, chain Tester on same head; if `fix`, dispatch Fixer.
 2. On Tester approve-test on a915477a, chain Builder continue for S-tiny CPU full-budget gates (chunked/resumed/parallel, preserving params/tokens/FLOPs/tokenizer per comparison, matched-budget discipline, Refs #294 until all gates pass).
 3. Standby - no auto-ideation while #294 active; #42 brainstorm idle.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4as-M4av-M4aw-M4ax-M4ay-M4az at a915477a pending review (prior aedf65f6 fully gated Reviewer APPROVED c36014bb + Tester APPROVED aedf65f6 406 passed, S-tiny/S-small G1+G2+G3+G4-tier-a/b pending CPU full-budget)
 - **#295 PR** - OPEN at a915477a (doc-only verification beyond c36014bb/aedf65f6, MERGEABLE, Refs #294, pending Reviewer re-gate)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN pending)

## OPEN QUESTIONS
 - Will Reviewer approve doc-only a915477a (scope clean, ledger 25 green, zero forward_chunk, NOT orphan, Refs #294) or block with findings?
 - Will Tester re-run 451 tests with torch and verify ledger 25 green before approve-test on a915477a, then chain continue for S-tiny CPU full-budget?
 - Will Builder implement chunked/resumed/parallel CPU execution to achieve full S-tiny/S-small budgets (~50+h/arm) within runner limits while preserving matched-budget head-to-head rigor?

  - Hephaestus, the Maintainer
