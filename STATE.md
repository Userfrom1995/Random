# STATE - Random factory checkpoint
 - **Updated:** 2026-09-08T01:01Z, maintainer run 34175269767 (event `created` on PR #295, Userfrom1995 `/oc review` at 01:01:40Z + `/oc maintainer` at 01:01:47Z)
 - **Action this run:** `[{"action":"review","pr":295,"head":"a7553d5cfe4b4e1b7bb54ed124aeddddbfa4ab3d"}]` — M4b toy P4-vs-P1 probes at a7553d5c dispatched to Reviewer; prior M1-M4a gated at 92bfb601, single-PR Refs #294 discipline intact.
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (successor to e9656dd8 via docs sync, `git ls-remote origin/main` = cdf3cdae, `git log --oneline -1` = cdf3cdae lab: mark Folio M4, Tabula, Sextant shipped on landing page (Refs #70), NOT orphan per gh PR MERGEABLE, `folio/` + `tabula/` + `sextant/` + `folio/packs/ocr+office` on main, Pages Deploy success on a7553d5c)
 - **Branch retention:** `opencode/issue277-20260904164811` at `bf67b253` MERGED at 0944bb63 retained, `opencode/issue282-*` Tabula at 23aeb5ce retained, `opencode/issue286-*` Sextant at 1e06b5b retained, `opencode/issue70-20260907160953` at `5f0c98f0` MERGED at cdf3cdae retained (docs sync, Refs #70), `opencode/issue294-20260907194528` at `a7553d5c` OPEN PR #295 (research a062a264 + architect ccbb2ca6 + Builder M1 ad520bcd/8d7a33cc/4b9132f9 + Builder M2 c125dc19/12b9877e/974684cb + Fixer a83e1fe7..2017b885 + Tester e16ae8b4 + Builder M3 92de4529/a48bb211/b3599901/7df98906/d33e43dc/96471854 + Fixer 190bc4f8/07db27a1/f1ae5904 + Tester a8c967a9 + Builder M4a fcc7a676/e94b1491/672e753f + Fixer 3db1f51a/23a1fdfa/f1dd797d + Tester 92bfb601 + Builder M4b 2 commits to a7553d5c, 35 commits, ~194 files, 19 ledger rows, `Refs #294`).
 - **Build guard:** 1 open PR [295 MERGEABLE head a7553d5c base cdf3cdae], `gh issue list --state open` = [42 brainstorm, 70 lab-health, 294 Post-Transformer] (3 open). Builder M4a DONE and fully gated (Reviewer 34174300598 approve at f1dd797d + Tester 34174541227 approve-test at 92bfb601 56 passed), Builder M4b delivered at a7553d5c awaiting Reviewer re-gate. PR stays `Refs #294` until G1+G2+G3+G4-tier-a/b pass head-to-head.
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) — AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint — Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a approved at 92bfb601 (Reviewer f1dd797d + Tester 92bfb601 56 passed), M4b at a7553d5c pending review, S-tiny/S-small gates remain GPU-blocked.
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** Update README.md + index.html to reflect live shipped state — COMPLETE at cdf3cdae (PR #293 MERGED as Refs #70).
 - **LAB RIGOR GATES (2026-09-07T15:47Z, via e9656dd8):** Brutal rigor, binding performance gates, subagent orchestration charter merged to main.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z, supreme, via #277):** 6 ingestion defects + 4 UI mandates — RESOLVED at 0944bb63 (still live at cdf3cdae).
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Dual-frontier standards ratified and verified on M4.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z, supreme, via #277):** Folio at /folio/ shipped M1-M3 + M4 final SHIPPED at 0944bb63. Issue #277 now CLOSED.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z, supreme, via #130):** Prism finished-at-ceiling closed.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Tabula at /tabula/ SHIPPED at 23aeb5ce (live at cdf3cdae).
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Sextant at /sextant/ SHIPPED at 1e06b5b (live at cdf3cdae).

## CRITICAL INFRASTRUCTURE STATE
 - **Main cdf3cdae — Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, gh PR view 295 MERGEABLE per server (proves common ancestor), folio/tabula/sextant on main, Deploy success.
 - **PR #295 OPEN MERGEABLE at a7553d5c, M4a FULLY GATED at 92bfb601, M4b PENDING REVIEW:** Verified `gh pr view 295` OPEN MERGEABLE head a7553d5c/base cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` = a7553d5c, `gh issue view 294` OPEN, branch `Refs #294` (single-PR discipline intact until G1+G2+G3+G4-tier-a/b pass), Reviewer `approve` at f1dd797d (00:48:42Z, both M4a blocked fixed: p4 window + surprise real compare) + Tester `approve-test` at 92bfb601 (00:52:26Z, 56 passed: 48 pre-existing T1-T6/M3/M4 + 8 new M4a hostile covering p4 window routing, parity, eta bounds, causality flatness, grads, ledger 18 rows `check` green) cover M1-M4a; M4b 2 commits at a7553d5c add matched p4-toy probe 0.528M tokens/arm, G1 mqar8 0.035 / N16 0.0156 chance / 2hop 0.01, below p1-W16-1000 ref 0.0625, H4 NEGATIVE at toy honestly ledgered, ledger 19 rows check-green, suite 56 passed. No infra touch, no secrets, Reviewer dispatch on a7553d5c.
 - **No infra anomaly:** `opencode.json` both knobs free, no `workflows permission` rejection, no CreditsError, no stalled pipeline, Deploy success on a7553d5c.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture — M1+M2-toy+M3+M4a APPROVED at 92bfb601 (#294 OPEN, PR #295 OPEN a7553d5c), M4b PENDING REVIEW:** Owner challenge via #42 with binding 4 gates (G4 amended to Pareto tiers a/b). Researcher 34156774420 + Architect 34157097837 complete. Builder M4a 2 commits at 672e753f + Fixer 3 commits to f1dd797d + Tester 92bfb601 (P4 surprise-gated delta eta=beta*sigmoid(w_s+g*||e||) + W-window, factory P4 tiny1702/small2724 parity +0.003%/+0.002% within 2%, test_p4 now real d_high>d_low + finiteness + beta/alpha bounds, window guard includes p4, suite 56 passed, 100-step toy smoke finite, proof 3145824 B flat, README/ideas updated). M1+M2-toy+M3 approved at a8c967a9 (Reviewer f1ae5904 + Tester a8c967a9 44 passed), ledger 18 rows check-green, G4 flat P1 3.15M/P2 3538944 B / P3 4718592 B vs baseline linear 805M at 32k. Toy probes: A2-re W0 0.0875 / W16 0.0625 / W32 0.0512 (no window advantage at N8), p3-noacc 0.0612 vs p3 0.0600 (H3 unresolved), p2 0.0825 above p1 ref. S-tiny gate ~50+h/arm on CPU measured, GPU runner required (train.py supports tiny/small for all 5 families). M4b at a7553d5c: matched p4-toy vs p1-W16-1000 ref, H4 NEGATIVE at toy (p4 0.035 < p1 0.0625/p2 0.0825), A6 N16-collapse to chance + A7 retrieval-vs-drift split, curves/m4b-toy/, ledger 19 rows check-green, 56 passed — awaits Reviewer then Tester. Builder 34174861271 completed success, 2 commits to a7553d5c.
 - **PR #295 — single branch for M1-M4 across continue cycles:** gh PR MERGEABLE per server; after Reviewer verdict on a7553d5c, dispatch Tester on approve or Fixer on block, before next continue to S-tiny GPU gates.
 - **Issue #70 — OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cdae.
 - **No other active pipeline:** No infra anomaly, Deploy success on PR head, no new Auditor bug, no orphan recovery needed.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cdae. Post-Transformer M1+M2-toy+M3+M4a approved at 92bfb601 (Reviewer f1dd797d + Tester 92bfb601 56 passed), G4 amended to Pareto dominance tiers. Builder M4b delivered at a7553d5c awaiting Reviewer re-gate; S-tiny full gates + S-small Enwik8 remain GPU-blocked.

## NEXT-RUN PLAYBOOK
 1. Await Reviewer verdict on a7553d5c — on `/oc fix:` -> `{"action":"fix","pr":295}` preserving P4 scope and single-PR discipline; on `/oc approve` -> `{"action":"test","pr":295}`.
 2. On Tester approve-test, chain `continue` for S-tiny full gates (GPU) + A3/A4/A5 at scale + S-small audit; `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass at S-tiny then S-small.
 3. Standby while Reviewer/Test in_progress (respect `cancel-in-progress: false`); re-dispatch only if stall without verdict.
 4. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass at S-tiny then S-small.
 5. Verify Pages Deploy on new head; otherwise standby — no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cdae)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cdae)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cdae)
 - **#293** - MERGED docs sync at cdf3cdae (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a approved at 92bfb601 (PR #295 35 commits at a7553d5c, 19 rows, 56 tests), M4b at a7553d5c pending Reviewer, S-tiny/S-small gates remain GPU-blocked
 - **#295 PR** - OPEN MERGEABLE at a7553d5c, Review dispatched on a7553d5c, prior approve f1dd797d + Tester approve-test 92bfb601 cover M1-M4a, M4b awaiting re-gate
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (docs sync SHIPPED at cdf3cdae via Refs #70)

## OPEN QUESTIONS
 - Will Reviewer approve M4b P4-vs-P1 toy probes at a7553d5c (H4 negative honestly ledgered) or block with findings requiring Fixer?
 - Will Tester re-run 56 tests + new M4b suite with torch and verify ledger growth to 19 rows?
 - Will GPU runner become available for S-tiny full gates (3 arms x 5 families x 3 seeds, ~50+h/arm on CPU) so G1+G2+G3 can be measured at pinned scale before M4 S-small Enwik8?

   - Hephaestus, the Maintainer
<!-- run: 34175269767 -->
