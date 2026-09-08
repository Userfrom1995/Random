# STATE - Random factory checkpoint
 - **Updated:** 2026-09-08T00:05Z, maintainer run 34172151220 (event `created` on PR #295, review dispatch for M3 head 96471854)
 - **Action this run:** `[{"action":"review","pr":295,"head":"964718547db41c68d5ec5213356a6144b2c2d51a"}]` — M3 P3+P2 code + toy falsification delivered at 96471854, prior M1+M2-toy approved at e16ae8b4, new head re-gates full scope before Tester.
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (successor to e9656dd8 via docs sync, `git ls-remote origin/main` = cdf3cdae, `git log --oneline -1` = cdf3cdae lab: mark Folio M4, Tabula, Sextant shipped on landing page (Refs #70), NOT orphan `merge-base e9656dd8 == e9656dd8`, `folio/` + `tabula/` + `sextant/` + `folio/packs/ocr+office` on main, Pages Deploy success on cdf3cdae 34172149662 success this cycle)
 - **Branch retention:** `opencode/issue277-20260904164811` at `bf67b253` MERGED at 0944bb63 retained, `opencode/issue282-*` Tabula at 23aeb5ce retained, `opencode/issue286-*` Sextant at 1e06b5b retained, `opencode/issue70-20260907160953` at `5f0c98f0` MERGED at cdf3cdae retained (docs sync, Refs #70), `opencode/issue294-20260907194528` at `96471854` OPEN PR #295 (research a062a264 + architect ccbb2ca6 + Builder M1 ad520bcd/8d7a33cc/4b9132f9 + Builder M2 c125dc19/12b9877e/974684cb + Fixer a83e1fe7..2017b885 + Tester e16ae8b4 + Builder M3 92de4529/a48bb211/b3599901/7df98906/d33e43dc/96471854, ~190 files plus red-team test, 18 ledger rows, `Refs #294`).
 - **Build guard:** 1 open PR [295 MERGEABLE head 96471854 base cdf3cdae], `gh issue list --state open` = [42 brainstorm, 70 lab-health, 294 Post-Transformer] (3 open). Builder M1+M2-toy DONE and approved (Reviewer 34168542934 at 2017b885 all 16 fixed + Tester 34168789383 at e16ae8b4 27 passed), Fixer DONE, Builder M3 DONE (6 commits to 96471854). PR stays `Refs #294` until G1+G2+G3+G4-tier-a/b pass head-to-head. This run dispatches Reviewer on new head 96471854.
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) — AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint — Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy approved at e16ae8b4, M3 code+toy delivered at 96471854, S-tiny GPU gates + M4 remain.
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** Update README.md + index.html to reflect live shipped state — COMPLETE at cdf3cdae (PR #293 MERGED as Refs #70).
 - **LAB RIGOR GATES (2026-09-07T15:47Z, via e9656dd8):** Brutal rigor, binding performance gates, subagent orchestration charter merged to main.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z, supreme, via #277):** 6 ingestion defects + 4 UI mandates — RESOLVED at 0944bb63 (still live at cdf3cdae).
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Dual-frontier standards ratified and verified on M4.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z, supreme, via #277):** Folio at /folio/ shipped M1-M3 + M4 final SHIPPED at 0944bb63. Issue #277 now CLOSED.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z, supreme, via #130):** Prism finished-at-ceiling closed.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Tabula at /tabula/ SHIPPED at 23aeb5ce (live at cdf3cdae).
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Sextant at /sextant/ SHIPPED at 1e06b5b (live at cdf3cdae).

## CRITICAL INFRASTRUCTURE STATE
 - **Main cdf3cdae — Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, NOT orphan, folio/tabula/sextant on main, Pages Deploy 34172149662 success on this cycle.
 - **PR #295 OPEN MERGEABLE at 96471854, Review dispatched:** Verified `gh pr view 295` OPEN MERGEABLE head 96471854/base cdf3cdae, `git merge-base origin/main 96471854` = cdf3cdae NOT orphan, `git log --oneline 96471854 --not cdf3cdae` = a062a264 + ccbb2ca6 + ad520bcd + 8d7a33cc + 4b9132f9 + c125dc19 + 12b9877e + 974684cb + a83e1fe7 + 34f3c8cb + ed72d703 + 84f0af80 + 3ea144b7 + 2017b885 + e16ae8b4 + 92de4529 + a48bb211 + b3599901 + 7df98906 + d33e43dc + 96471854 (21 commits), branch `Refs #294` (single-PR discipline intact until G1+G2+G3+G4-tier-a/b pass), progress at 96471854 marks M1 [x] + M2 toy [x] + M3 code [x] with S-tiny deferred. Prior Tester 34168789383 at e16ae8b4 (27 passed) and Reviewer approve at 2017b885 hold; new head awaits re-gate inclusive of P2/P3.
 - **Review queue:** User `/oc review` at 2026-09-08T00:04:51Z on PR #295 triggered opencode-review 34172143181 in_progress + 34172151198 pending on cdf3cdae headSha; this maintainer run explicitly dispatches `review` on PR head 96471854 to ensure M3 scope gated. `Refs #294` discipline intact.
---

## IN FLIGHT
 - **Post-Transformer Sequence Architecture — M1+M2-toy APPROVED, M3 AWAITING REVIEW (#294 OPEN, PR #295 OPEN 96471854):** Owner challenge via #42 with binding 4 gates (G4 amended to Pareto tiers a/b). Researcher 34156774420 (a062a264, P1-P5 H1-H5 A1-A7) + Architect 34157097837 (ccbb2ca6, PostFormer Delta-Hybrid + W=128, M1-M4 roadmap) complete. Builder M3 6 commits (92de4529 P3 decoupled + 1532 hid + A3 flag + a48bb211 P2 slots G16 + 33 tests + b3599901 G4 Pareto re-lint + 7df98906 loader inheritance + d33e43dc A2-re probes + 96471854 progress/ideas) with ledger 18 rows check-green, G4 flat P1 3.15M/P2 3.93M/P3 4.72M vs baseline linear 805M at 32k, parity within 2% all scales. Toy probes: A2-re W0 0.0875 / W16 0.0625 / W32 0.0512 (no window advantage at N8), p3-noacc 0.0612 vs p3 0.0600 (H3 unresolved), p2 0.0825 above p1 ref. S-tiny gate ~50+h/arm on CPU measured, GPU runner required (train.py supports tiny/small for all 5 families). This run dispatches Reviewer on 96471854; next is Tester on approve, then continue for S-tiny + A3/A4/A5 + M4 (P4 + A6/A7 + S-small audit) with `Refs #294` until full tier pass.
 - **PR #295 — single branch for M1-M4 across continue cycles:** No rebase needed (`merge-base` cdf3cdae); `review` dispatched on 96471854; after Tester approve, `continue` for S-tiny trained gates (GPU) + M3 sweeps + M4, `Refs #294` until G1+G2+G3+G4-tier-a/b pass head-to-head at S-tiny then S-small.
 - **Issue #70 — OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cdae.
 - **No other active pipeline:** No infra anomaly, Auditor 34078079178 All green still authoritative (70 models/7 free), Deploy 34172149662 success; no new Auditor bug, no orphan recovery needed.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cdae. Post-Transformer M1+M2-toy approved, M3 code+toy delivered at 96471854 now in Review (head 96471854), G4 amended to Pareto dominance tiers. Awaiting Reviewer verdict -> Tester -> S-tiny GPU continue.

## NEXT-RUN PLAYBOOK
 1. Await Reviewer verdict on PR #295 head 96471854 (M3 P2/P3 + amended G4). Verify Refs #294 kept, no infra touch, parity within 2%, loader inheritance correct, slot contract.
 2. On `/oc approve` -> `{"action":"test","pr":295}` (re-run 34 tests + ledger 18 rows + G4 flat with tier rule) then `continue` for S-tiny GPU gates (3 arms x 3 seeds) + A3/A4/A5.
 3. On `/oc fix:` -> `{"action":"fix","pr":295}` preserving dedup key (vocab/window) and single-PR discipline.
 4. On Tester `/oc approve-test` -> `{"action":"continue","pr":295}` for M3 S-tiny sweeps + M4 P4/A6/A7/S-small Enwik8 envelope; `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass at S-tiny then S-small.
 5. Verify Pages Deploy on new head after Tester; otherwise standby — no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cdae)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cdae)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cdae)
 - **#293** - MERGED docs sync at cdf3cdae (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+Fixer+Review+Tester complete at e16ae8b4, M3 delivered at 96471854 (PR #295 21 commits, 18 rows, 34 tests, awaiting Review)
 - **#295 PR** - OPEN MERGEABLE at 96471854, Review dispatched on 96471854 (in_progress 34172143181 + pending 34172151198)
 - **#42 - OPEN** brainstorm (78 comments, challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (docs sync SHIPPED at cdf3cdae via Refs #70)

## OPEN QUESTIONS
 - Will Reviewer approve M3 at 96471854 (P2/P3 parity, slot contract, loader inheritance, G4 Pareto tiers) or block with findings requiring Fixer?
 - Will Tester re-run 34 tests with torch and verify ledger 18 rows + G4 flatness under tier-a/b before approve-test?
 - Will GPU runner become available for S-tiny full gates (3 arms x 3 seeds, ~1s/step measured) so G1+G2+G3 can be measured at pinned scale before M4 S-small Enwik8?

   - Hephaestus, the Maintainer
<!-- run: 34172151220 -->
