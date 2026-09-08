# STATE - Random factory checkpoint
 - **Updated:** 2026-09-08T01:09Z, maintainer run 34175689720 (event `created` on PR #295, Userfrom1995 `/oc maintainer` at 01:09:11Z)
 - **Action this run:** `[{"action":"continue","pr":295}]` — M4b P4-vs-P1 toy probes fully gated at de517899 chains Builder continue for S-tiny GPU full gates + S-small audit; Refs #294 single-PR discipline intact.
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (successor to e9656dd8 via docs sync, `git ls-remote origin/main` = cdf3cdae, `git log --oneline -1` = cdf3cdae lab: mark Folio M4, Tabula, Sextant shipped on landing page (Refs #70), NOT orphan per gh PR MERGEABLE, `folio/` + `tabula/` + `sextant/` + `folio/packs/ocr+office` on main, Pages Deploy success pending approval on de517899)
 - **Branch retention:** `opencode/issue277-20260904164811` at `bf67b253` MERGED at 0944bb63 retained, `opencode/issue282-*` Tabula at 23aeb5ce retained, `opencode/issue286-*` Sextant at 1e06b5b retained, `opencode/issue70-20260907160953` at `5f0c98f0` MERGED at cdf3cdae retained (docs sync, Refs #70), `opencode/issue294-20260907194528` at `de517899` OPEN PR #295 (research a062a264 + architect ccbb2ca6 + Builder M1 ad520bcd/8d7a33cc/4b9132f9 + Builder M2 c125dc19/12b9877e/974684cb + Fixer a83e1fe7..2017b885 + Tester e16ae8b4 + Builder M3 92de4529/a48bb211/b3599901/7df98906/d33e43dc/96471854 + Fixer 190bc4f8/07db27a1/f1ae5904 + Tester a8c967a9 + Builder M4a fcc7a676/e94b1491/672e753f + Fixer 3db1f51a/23a1fdfa/f1dd797d + Tester 92bfb601 + Builder M4b 853c5b89/a7553d5c + Reviewer approve a7553d5c + Tester de517899, 36 commits, ~195 files, 19 ledger rows, `Refs #294`).
 - **Build guard:** 1 open PR [295 MERGEABLE head de517899 base cdf3cdae], `gh issue list --state open` = [42 brainstorm, 70 lab-health, 294 Post-Transformer] (3 open). Builder M4b DONE and fully gated (Reviewer 34175262547 approve at a7553d5c + Tester 34175407885 approve-test at de517899 66 passed), chaining Builder continue for S-tiny full gates + S-small envelope audit.
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) — AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint — Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a+M4b approved at de517899 (Reviewer a7553d5c + Tester de517899 66 passed), S-tiny/S-small gates remain GPU-blocked.
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** Update README.md + index.html to reflect live shipped state — COMPLETE at cdf3cdae (PR #293 MERGED as Refs #70).
 - **LAB RIGOR GATES (2026-09-07T15:47Z, via e9656dd8):** Brutal rigor, binding performance gates, subagent orchestration charter merged to main.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z, supreme, via #277):** 6 ingestion defects + 4 UI mandates — RESOLVED at 0944bb63 (still live at cdf3cdae).
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Dual-frontier standards ratified and verified on M4.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z, supreme, via #277):** Folio at /folio/ shipped M1-M3 + M4 final SHIPPED at 0944bb63. Issue #277 now CLOSED.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z, supreme, via #130):** Prism finished-at-ceiling closed.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Tabula at /tabula/ SHIPPED at 23aeb5ce (live at cdf3cdae).
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Sextant at /sextant/ SHIPPED at 1e06b5b (live at cdf3cdae).

## CRITICAL INFRASTRUCTURE STATE
 - **Main cdf3cdae — Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, gh PR view 295 MERGEABLE per server (proves common ancestor), folio/tabula/sextant on main, Deploy success on a7553d5c/de517899 (latest pending Pages approval action_required, prior heads success).
 - **PR #295 OPEN MERGEABLE at de517899, M4b FULLY GATED at de517899, chaining continue:** Verified `gh pr view 295` OPEN MERGEABLE head de517899/base cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` = de517899, `gh issue view 294` OPEN, branch `Refs #294` (single-PR discipline intact until G1+G2+G3+G4-tier-a/b pass), Reviewer `approve` at a7553d5c (01:04:13Z, M4b delta 2 commits, ledger 19 rows, H4 NEGATIVE honestly ledgered) + Tester `approve-test` at de517899 (01:09:10Z, 66 passed: 56 pre-existing T1-T6/M3/M4/M4a + 10 new M4b hostile covering p4 window routing, ledger-vs-curve fidelity 0.035/0.015625/0.01, budget 528000, chance collapse, H4 ordering, window agreement) cover M1-M4b; all CPU-feasible milestones complete. No infra touch, no secrets, continuity to S-tiny GPU gates.
 - **No infra anomaly:** `opencode.json` both knobs free, no `workflows permission` rejection, no CreditsError, no stalled pipeline, Deploy pending approval is normal PR preview (not failure).

## IN FLIGHT
 - **Post-Transformer Sequence Architecture — M1+M2-toy+M3+M4a+M4b APPROVED at de517899 (#294 OPEN, PR #295 OPEN de517899), chaining S-tiny GPU continue:** Owner challenge via #42 with binding 4 gates (G4 amended to Pareto tiers a/b). Researcher 34156774420 + Architect 34157097837 complete. Builder M4b 2 commits at a7553d5c (matched p4-toy seed0 1000 steps = 0.528M tokens, G1 mqar8 0.035 / N16 0.0156 chance / 2hop 0.01 below p1-W16-1000 ref 0.0625 and p2 0.0825, H4 NEGATIVE at toy honestly ledgered, A6 N16-collapse + A7 retrieval-vs-drift split, curves/m4b-toy/, ledger 19 rows check-green, suite 56 passed) + Reviewer approve a7553d5c + Tester de517899 (added 10 M4b hostile, 66 passed, ledger-vs-curve byte-identical, budget confirmed, window 16 agreement, H4 ordering). Prior M4a P4 surprise-gated delta eta=beta*sigmoid(w_s+g*||e||) + W-window at 92bfb601 (56 passed), M3 P3+P2 at a8c967a9 (44 passed), M1+M2-toy at e16ae8b4 (27 passed). G4 flat P1 3.15M/P2 3538944 B / P3 4718592 B vs baseline linear 805M at 32k. S-tiny gate ~50+h/arm on CPU measured, GPU runner required (train.py supports tiny/small for all 5 families).
 - **PR #295 — single branch for M1-M4 across continue cycles:** gh PR MERGEABLE per server; after M4b approve-test, dispatching Builder continue for S-tiny full gates (GPU) + A3/A4/A5 + S-small audit + viewer snapshot + final scoreboard.
 - **Issue #70 — OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cdae.
 - **No other active pipeline:** No infra anomaly, Deploy pending approval normal, no new Auditor bug, no orphan recovery needed.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cdae. Post-Transformer M1+M2-toy+M3+M4a+M4b approved at de517899 (Reviewer a7553d5c + Tester de517899 66 passed), G4 amended to Pareto dominance tiers. Chaining Builder continue for S-tiny GPU full gates (3 arms x 3 seeds) + A3/A4/A5 + S-small Enwik8 envelope audit. `Refs #294` until full gate pass head-to-head.

## NEXT-RUN PLAYBOOK
 1. Await Builder continue push beyond de517899 — then dispatch Reviewer on new head.
 2. On Reviewer approve -> Tester; on fix -> Fixer, before next continue to S-small.
 3. Standby while Builder/Reviewer/Test in_progress (respect `cancel-in-progress: false`); re-dispatch only if stall without verdict.
 4. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass at S-tiny then S-small.
 5. Verify Pages Deploy on new head; otherwise standby — no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cdae)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cdae)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cdae)
 - **#293** - MERGED docs sync at cdf3cdae (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a+M4b approved at de517899 (PR #295 36 commits at de517899, 19 rows, 66 tests), chaining S-tiny GPU continue, S-tiny/S-small gates remain GPU-blocked
 - **#295 PR** - OPEN MERGEABLE at de517899, M4b fully gated (Reviewer a7553d5c + Tester de517899), continue dispatched for S-tiny GPU gates
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (docs sync SHIPPED at cdf3cdae via Refs #70)

## OPEN QUESTIONS
 - Will GPU runner become available for S-tiny full gates (3 arms x 5 families x 3 seeds, ~50+h/arm on CPU) so G1+G2+G3 can be measured at pinned scale before M4 S-small Enwik8?
 - Will H4 (p4 surprise) overturn at S-tiny N64+ or replicate M4b toy negative (0.035 < 0.0625) under matched budget?
 - Will A3/A4/A5 sweeps at S-tiny resolve H2/H3 verdicts at scale?

   - Hephaestus, the Maintainer
<!-- run: 34175689720 -->
