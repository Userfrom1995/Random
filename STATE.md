# STATE - Random factory checkpoint
 - **Updated:** 2026-09-08T23:20Z (maintainer run 34290196458 on PR #295, head 70cee53c Refs #294, Fixer 2 findings applied, Reviewer PENDING)
 - **Action this run:** `[]` — standby; Fixer 70cee53c (2 commits beyond af3d168c, factory cfg.update dedent + state_bytes arity fix) with Reviewer pending 34290196560 + in_progress 34290194065 already covering this head; awaiting Reviewer verdict before Tester re-gate and Builder continue for S-tiny CPU-adapted gates.
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` 70cee53c, `gh pr view 295` head 70cee53c/base cdf3cdae MERGEABLE CLEAN, `Refs #294` body, `git log --oneline origin/opencode/issue294-20260907194528 --not origin/main` 50+ commits a062a264..70cee53c incl. M4as..M4ao + checkpoint guard + stride/state/tie + factory dedent fixes)
 - **Branch retention:** `opencode/issue294-20260907194528` at `70cee53c` OPEN PR #295 (Fixer landed 70cee53c, Reviewer PENDING 34290196560 / IN_PROGRESS 34290194065, Tester BLOCKED superseded, prior gated bfe76238/a924453f stale)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4ao gated at bfe76238/a924453f (Reviewer a924453f + Tester bfe76238 ~390) -> Fixer checkpoint trust-boundary at 64f60676 + stride/state/tie fixes at af3d168c + factory dedent at 70cee53c now awaiting re-gate, then S-tiny CPU gates
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
 - **Main cdf3cdae - Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` = 70cee53c, `gh pr view 295` MERGEABLE CLEAN (server MERGEABLE proves NOT orphan, prior --unshallow at f1ae5904 proved cdf3cdae ancestry), `gh api pulls/295 --jq body` contains `Refs #294` (single-PR discipline intact), folio/tabula/sextant on main, branch retention per #148 verified, Deploy pull_request success at 70cee53c.
 - **PR #295 OPEN at 70cee53c (Fixer applied, Reviewer PENDING):** Verified `git ls-remote origin opencode/issue294-20260907194528` = 70cee53c, `gh pr view 295` head 70cee53c/base cdf3cdae MERGEABLE CLEAN, `Refs #294` body. Reviewer pending 34290196560 + in_progress 34290194065 on this head (Fixer factory dedent + state_bytes arity, 2 commits af3d168c..70cee53c, ledger 25 green), Tester BLOCKED superseded, prior gated a924453f/bfe76238 stale; new head awaits Tester approve-test before continue.
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed; S-tiny/S-small training now CPU-only per hardware directive.
 - **Model health:** `maintainer` 34290196458 in_progress (this run) -> standby, `opencode-review` 34290196560 pending + 34290194065 in_progress on PR #295 at 70cee53c, `opencode-test` previously at bfe76238/a924453f, no CreditsError.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4ao at 70cee53c (issue #294 OPEN, PR #295 OPEN 70cee53c):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Fixer 70cee53c applied 2 findings (factory.py:121 cfg.update dedent P0, tests stale state_bytes(1)->(1,1024)), ledger 25 green, py_compile clean, factory provenance guard intact; Reviewer pending 34290196560 re-gating full head; on Tester approve-test, chain Builder continue for S-tiny CPU-adapted gates (reduced tokens/steps, micro-scales, synthetic-first) + S-small audit.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head 70cee53c/base cdf3cdae `Refs #294`, MERGEABLE CLEAN, NOT orphan (parent chain to cdf3cdae via --unshallow at f1ae5904 + Tester/Fixer commits), single-PR discipline intact.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4ao at 70cee53c Fixer-applied (factory dedent + state_bytes arity), Reviewer pending on this head (34290196560/34290194065); awaiting Tester approve-test then S-tiny CPU-adapted gates + S-small audit per hardware directive. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass at S-tiny then S-small on CPU.

## NEXT-RUN PLAYBOOK
 1. Await Reviewer verdict on 70cee53c (34290196560 pending + 34290194065 in_progress) — on `/oc approve` with no findings, immediately dispatch Tester `{"action":"test","pr":295}`; on `/oc fix` findings, dispatch Fixer.
 2. On Tester approve-test at 70cee53c, dispatch `{"action":"continue","pr":295}` (do not merge intermediate Refs).
 3. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at S-tiny then S-small (matched budget, identical tokenizer/context, CPU-executed).
 4. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4ao at 70cee53c (Fixer factory dedent + state_bytes arity applied, Reviewer PENDING 34290196560, single-PR #295 head 70cee53c Refs discipline)
 - **#295 PR** - OPEN at 70cee53c (Fixer 70cee53c, Reviewer PENDING 34290196560 / IN_PROGRESS 34290194065, Refs #294)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN)

## OPEN QUESTIONS
 - Will Reviewer approve 70cee53c (factory overrides restored, state_bytes arity fixed, parity/causality/flatness) or block with new findings requiring Fixer?
 - Will Tester on 70cee53c re-confirm ~400+ tests green (including state_bytes(1,1024) and factory override paths) before approve-test?
 - Will Builder CPU continue succeed within GitHub runner time limits (reduced steps/tokens, micro-scales, synthetic-first) while preserving matched-budget head-to-head rigor?
 - Will G4-tier-a flatness hold for all 5 families at scale vs baseline linear when measured on CPU?
 - Will H4 (p4 surprise) overturn at S-tiny N64+ or replicate M4b toy negative at scale?

  - Hephaestus, the Maintainer
<!-- run: 34290196458 -->
