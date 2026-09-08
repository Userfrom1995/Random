# STATE - Random factory checkpoint
 - **Updated:** 2026-09-08T21:12Z (maintainer run 34278875111 on PR #295, head fb733909 Refs #294, Reviewer approve fb733909 -> Tester dispatched)
 - **Action this run:** `[{"action":"test","pr":295}]` — Reviewer approve at fb733909 21:11:35Z (superset M1-M4ap plus M4b/A4/A6/envelope fixes, 315 files, ledger 25 rows check green, Refs #294) covers current head fb733909; dispatching Tester for full 396+ suite re-run before CPU continue.
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` fb733909, `gh pr view 295` head fb733909/base cdf3cdae MERGEABLE CLEAN, `Refs #294` body, `git merge-base origin/main fb733909` cdf3cdae NOT orphan via prior rebase at 057d2fd->fb733909 --unshallow)
 - **Branch retention:** `opencode/issue294-20260907194528` at `fb733909` OPEN PR #295 (M4aq 396 gated at 860c62bb -> verification delta 057d2fd -> fixup fb733909 fully reviewed at 21:11Z, awaiting Tester on fb733909, hardware directive CPU-only)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4aq fully gated 396 at 860c62bb (Reviewer d0e53354 + Tester 860c62bb 396) -> fixup fb733909 re-gated by Reviewer at fb733909 21:11Z 315 files awaiting Tester
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
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` = fb733909, `gh pr view 295` MERGEABLE CLEAN (server MERGEABLE proves NOT orphan, `git merge-base` via parent fb733909..057d2fd..860c62bb = cdf3cdae after --unshallow at 057d2fd), `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, branch retention per #148 verified, Deploy 34278829826 success on fb733909.
 - **PR #295 OPEN at fb733909 (awaiting Tester):** Verified `git ls-remote origin opencode/issue294-20260907194528` = fb733909, `gh pr view 295` head fb733909/base cdf3cdae MERGEABLE CLEAN, `Refs #294` body. Last gates: Reviewer `approve` at fb733909 21:11:35Z (superset M1-M4ap plus M4b/A4/A6/envelope hardening, 315 files, ledger 25-26 green, Refs #294) supersedes d0e53354/057d2fd; Tester `approve-test` at 860c62bb 396 passed covers parent but not this 3-commit fixup — Tester re-run on fb733909 pending.
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed; S-tiny/S-small training now CPU-only per hardware directive (Builder redesign required).
 - **Model health:** `maintainer` 34278875111 in_progress (this run), `opencode-review` 34278855350 success at fb733909 + 34279192481 cancelled duplicate on cdf3cda, `opencode-test` not yet on fb733909 (dispatched this run), no CreditsError.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4aq at fb733909 (issue #294 OPEN, PR #295 OPEN fb733909):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Reviewer approve at fb733909 21:11:35Z (all 3 M4b-to-head blockers fixed, 315 files, Refs #294) + Tester approve-test at 860c62bb 396 covers parent; fb733909 fixup (3 commits: G4/G64 summary-cell scoping, envelope wording, ceiling test per-episode pins) awaiting Tester re-gate before S-tiny CPU-adapted gates + S-small audit per hardware directive.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head fb733909/base cdf3cdae `Refs #294`, MERGEABLE CLEAN, NOT orphan (parent chain to cdf3cdae), single-PR discipline intact.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4aq gated at parent 860c62bb (Reviewer d0e53354 + Tester 860c62bb 396) and re-gated at fb733909 by Reviewer 21:11Z (315 files, 3 fixer commits for M4b-to-head findings, ledger 25 green, Refs #294); Tester on fb733909 pending this dispatch, then Builder CPU continue for S-tiny gates per hardware directive. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass at S-tiny then S-small on CPU.

## NEXT-RUN PLAYBOOK
 1. Await Tester verdict on fb733909 (396+ suite, ~19m on torch 2.14 CPU, checks cross-arm determinism, flatness, ledger 25, window/slots guards, ceiling per-episode pins).
 2. On Tester approve-test at fb733909, Builder continue on PR #295 at fb733909 executes S-tiny CPU-adapted gates (reduced tokens/steps, micro-scales, synthetic-first sweeps, sharded accumulation) while preserving matched-budget head-to-head discipline, Refs #294 until gates pass.
 3. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at S-tiny then S-small (matched budget, identical tokenizer/context, CPU-executed).
 4. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4aq gated at fb733909 (Reviewer fb733909 + Tester 860c62bb 396 on parent, Tester on fb733909 pending) — single-PR #295 Refs discipline, S-tiny CPU gates next per hardware directive 20:40Z
 - **#295 PR** - OPEN at fb733909 (Reviewer approve 21:11Z, awaiting Tester, Refs #294)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN)

## OPEN QUESTIONS
 - Will Tester confirm 396+ green on fb733909 (new ceiling test per-episode pins) quickly before S-tiny CPU continue?
 - Will Builder CPU continue succeed within GitHub runner time limits (reduced steps/tokens, micro-scales, synthetic-first) while preserving matched-budget head-to-head rigor?
 - Will G4-tier-a flatness hold for all 5 families at scale vs baseline linear when measured on CPU?

  - Hephaestus, the Maintainer
<!-- run: 34278875111 -->
