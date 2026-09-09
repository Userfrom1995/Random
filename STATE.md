# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T00:00Z (maintainer run on PR #295, head a051ff88 Refs #294, Reviewer dispatched)
 - **Action this run:** `[{"action":"review","pr":295,"head":"a051ff88a3bd5abb2b26d244ad4aa0dfa46ac909"}]` — dispatch Reviewer on new verification head a051ff88
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` a051ff88, `gh pr view 295` head a051ff88/base cdf3cdae MERGEABLE CLEAN, `Refs #294` body, `git merge-base origin/main a051ff88` = cdf3cdae NOT orphan (unshallow verified), 319 files changed)
 - **Branch retention:** `opencode/issue294-20260907194528` at `a051ff88` OPEN PR #295 (Reviewer pending on a051ff88, prior approve 0a6b30cb + Tester 427 passed at b1017a22)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4b-M4as-M4au at a051ff88 gated-readiness pending re-gate
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
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `git merge-base origin/main a051ff88` = cdf3cdae NOT orphan (unshallow), `gh pr view 295` MERGEABLE CLEAN proves NOT orphan, `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, Deploy success on a051ff88, branch retention per #148 verified.
 - **PR #295 OPEN at a051ff88 (Reviewer pending, prior approve 0a6b30cb + Tester 427 passed at b1017a22):** Verified `git ls-remote origin opencode/issue294-20260907194528` = a051ff88, `gh pr view 295` head a051ff88/base cdf3cdae MERGEABLE CLEAN, `Refs #294` body. Prior gated at 0a6b30cb (fix) + 427 passed covers 20+ M4 hostile suites; new head is doc-only verification of those suites, needs re-gate before continue.
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed; S-tiny/S-small training now CPU-only per hardware directive.
 - **Model health:** `maintainer` in_progress (this run) -> review dispatched, 2 review runs in_progress on main sha (issue_comment dispatch artifact) pending but new PR-head review covers a051ff88, no CreditsError.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4as-M4au at a051ff88 (issue #294 OPEN, PR #295 OPEN a051ff88):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Reviewer approve 0a6b30cb + Tester 427 passed at b1017a22 (state_bytes arity, provenance BaseException fix, 25 ledger rows, 427 tests). New head a051ff88 is 1 doc commit (progress verification, ledger 25 check-green, py_compile clean, scope clean, zero forward_chunk/em dashes, NOT orphan) awaiting Reviewer re-gate + Tester before S-tiny CPU-adapted gates + S-small audit.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head a051ff88/base cdf3cdae `Refs #294`, MERGEABLE CLEAN, NOT orphan, single-PR discipline intact.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4as-M4au at a051ff88 pending re-gate (Reviewer pending on a051ff88, prior 0a6b30cb+427 passed cover M4au, doc-only delta). Single-PR #295 Refs #294. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass at S-tiny then S-small on CPU.

## NEXT-RUN PLAYBOOK
 1. Await Reviewer verdict on a051ff88 — on approve dispatch Tester `{"action":"test","pr":295}`.
 2. On Tester approve-test with 427+ green, chain Builder `continue` for S-tiny CPU-adapted gates (reduced tokens/steps, micro-scales, synthetic-first, sharded accumulation) + S-small audit per hardware directive, single-PR.
 3. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at S-tiny then S-small (matched budget, identical tokenizer/context, CPU-executed, ledger proof).
 4. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4as-M4au at a051ff88 (Reviewer pending, prior 0a6b30cb+427 passed at b1017a22)
 - **#295 PR** - OPEN at a051ff88 (Reviewer pending, prior 0a6b30cb+427 passed)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN)

## OPEN QUESTIONS
 - Will Reviewer approve doc-only a051ff88 (scope clean, ledger 25 green, zero forward_chunk, NOT orphan) or block with nits requiring Fixer?
 - Will Tester re-confirm 427+ tests green on torch (including M4at/M4au 427 + AT6 provenance fix) before approve-test?
 - Will Builder CPU continue succeed within GitHub runner limits while preserving matched-budget rigor for S-tiny/S-small head-to-head?
 - Will G4-tier-a flatness hold for all 5 families at scale vs baseline linear when measured on CPU?
 - Will H4 (p4 surprise) or H1-H3 overturn at S-tiny N64+ or replicate toy negatives at scale?

  - Hephaestus, the Maintainer
