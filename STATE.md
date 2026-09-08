# STATE - Random factory checkpoint
 - **Updated:** 2026-09-08T21:40Z (maintainer run 34281800796 on PR #295, head a875e682 Refs #294, Reviewer dispatched on a875e682)
 - **Action this run:** `[{"action":"review","pr":295,"head":"a875e6820491f53b9b566c1250bcb752aaa9b9ab"}]` — M4ar verification handoff at a875e682 (1 commit beyond e31a8937) dispatched to Reviewer; prior dual gate fb733909 + e31a8937 402 no longer covers new Builder commit, awaiting re-gate before Tester and S-tiny CPU continue.
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` a875e682, `gh pr view 295` head a875e682/base cdf3cdae MERGEABLE CLEAN, `Refs #294` body, `git log --oneline origin/opencode/issue294-20260907194528 --not origin/main` 48 commits a062a264..a875e682 incl. M4ar handoff)
 - **Branch retention:** `opencode/issue294-20260907194528` at `a875e682` OPEN PR #295 (fb733909 Reviewer approve + e31a8937 Tester 402 passed stale vs new head, new Reviewer 34281800796 dispatched, ledger 25 rows 26-col check green per handoff, hardware directive CPU-only)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4ar fully gated 402 at e31a8937 (Reviewer fb733909 + Tester e31a8937 402) -> new head a875e682 awaiting re-gate then S-tiny CPU gates
 - **HARDWARE DIRECTIVE (2026-09-08T20:40:31Z, supreme, via #294):** No GPU runner is coming. All S-tiny/S-small training must run on standard GitHub CPU runners. Prior GPU-blocked assumption (~50+h/arm at batch2/seq33 measured 2026-09-08) superseded — Builder must redesign training for CPU feasibility (reduced steps/tokens, micro-scales, synthetic-first sweeps, sharded accumulation) while preserving matched param/FLOP/data budget head-to-head discipline and identical tokenizer/context per comparison.
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** Update README.md + index.html to reflect live shipped state - COMPLETE at cdf3cda (PR #293 MERGED as Refs #70).
 - **LAB RIGOR GATES (2026-09-07T15:47Z, via e9656dd8):** Brutal rigor, binding performance gates, subagent orchestration charter merged to main.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z, supreme, via #277):** 6 ingestion defects + 4 UI mandates - RESOLVED at 0944bb63 (still live at cdf3cda).
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Dual-frontier standards ratified and verified on M4.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z, supreme, via #277):** Folio at /folio/ shipped M1-M3 + M4 final SHIPPED at 0944bb63. Issue #277 now CLOSED.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z, supreme, via #130):** Prism finished-at-ceiling closed.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Tabula at /tabula/ SHIPPED at 23aeb5ce (live at cdf3cda).
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Sextant at /sextant/ SHIPPED at 1e06b5b (live at cdf3cda).

## CRITICAL INFRASTRUCTURE STATE
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` = a875e682, `gh pr view 295` MERGEABLE CLEAN (server MERGEABLE proves NOT orphan, prior --unshallow at 057d2fd+f1ae5904 proved cdf3cdae ancestry), `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, branch retention per #148 verified, Deploy 34281771075 success on a875e682.
 - **PR #295 OPEN at a875e682 (Reviewer dispatched):** Verified `git ls-remote origin opencode/issue294-20260907194528` = a875e682, `gh pr view 295` head a875e682/base cdf3cdae MERGEABLE CLEAN, `Refs #294` body. Last gates: Reviewer `approve` at fb733909 21:11:35Z (superset M1-M4ar + A4 G4/G64 + envelope hardening, 315 files, ledger 25-26 green, Refs #294) + Tester `approve-test` at e31a8937 21:34:23Z (402 passed + 7 new hostile on A4 divergence, ledger 25 green, Refs #294) stale vs new head a875e682; new Reviewer dispatched 34281800796 on a875e682 for re-gate.
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed; S-tiny/S-small training now CPU-only per hardware directive (Builder redesign required).
 - **Model health:** `maintainer` 34281800796 in_progress (this run) -> review dispatched, `opencode-pr-trigger` 34281771093 success + `Deploy` 34281771075 success on a875e682, no CreditsError.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4ar at a875e682 (issue #294 OPEN, PR #295 OPEN a875e682):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Reviewer approve at fb733909 21:11:35Z + Tester approve-test at e31a8937 21:34:23Z (402 passed: 396+ prior + 7 hostile on A4 G4/G64 eviction/divergence + 402 M4ar, ledger 25 green, Refs #294) covers pre-handoff e31a8937; new Builder commit a875e682 (M4ar verification handoff, ledger 25 green, 48 commits) awaiting re-gate before Tester and S-tiny CPU continue.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head a875e682/base cdf3cdae `Refs #294`, MERGEABLE CLEAN, NOT orphan (parent chain to cdf3cdae via --unshallow at 057d2fd+f1ae5904), single-PR discipline intact.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4ar fully gated at e31a8937 (Reviewer fb733909 + Tester e31a8937 402) with 25 ledger rows 26-col, 315 files, Refs #294; new Builder verification handoff pushed to a875e682 (1 commit) - Reviewer re-gate dispatched, then Tester, then Builder continue for S-tiny CPU-adapted gates (reduced tokens/steps, micro-scales, synthetic-first sweeps, sharded accumulation) per hardware directive 20:40Z. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass at S-tiny then S-small on CPU.

## NEXT-RUN PLAYBOOK
 1. Await Reviewer verdict on a875e682 (parity within 2%, causality, ledger 25 green, G4-tier logic, no SiLU/hidden T) - `fix` if findings, `test` if approve.
 2. On Tester approve-test on a875e682, dispatch Builder `continue` for S-tiny CPU-adapted gates preserving matched-budget head-to-head discipline (identical tokenizer/context/budget per comparison).
 3. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at S-tiny then S-small (matched budget, identical tokenizer/context, CPU-executed).
 4. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4ar fully gated at e31a8937 (Reviewer fb733909 + Tester e31a8937 402) — single-PR #295 head a875e682 Refs discipline, awaiting re-gate on new handoff commit before S-tiny CPU gates per hardware directive 20:40Z
 - **#295 PR** - OPEN at a875e682 (Reviewer fb733909 stale + Tester e31a8937 402 stale, new Reviewer dispatched 34281800796 on a875e682, Refs #294)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN)

## OPEN QUESTIONS
 - Will Reviewer approve M4ar handoff at a875e682 quickly or block with findings requiring Fixer?
 - Will Builder CPU continue succeed within GitHub runner time limits (reduced steps/tokens, micro-scales, synthetic-first) while preserving matched-budget head-to-head rigor?
 - Will G4-tier-a flatness hold for all 5 families at scale vs baseline linear when measured on CPU?
 - Will H4 (p4 surprise) overturn at S-tiny N64+ or replicate M4b toy negative (0.035 < 0.0625) at scale?

  - Hephaestus, the Maintainer
<!-- run: 34281800796 -->
