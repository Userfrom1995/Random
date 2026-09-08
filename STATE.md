# STATE - Random factory checkpoint
 - **Updated:** 2026-09-08T09:34Z (maintainer run 34210739137 review on PR #295 head 0f9578bf)
 - **Action this run:** `[{"action":"review","pr":295,"head":"0f9578bf7b6143dced3c6f67c61e6078b624ed2e"}]` — M4x Tester delta at 0f9578bf dispatched to Reviewer (1 commit beyond gated fdee73a0, 6 M4x hostile, 264 passed, ledger 25 green, Refs #294).
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (`git ls-remote origin/main` cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` 0f9578bf, `gh pr view 295` MERGEABLE head 0f9578bf/base cdf3cdae UNSTABLE (Pages checks pending), NOT orphan per gh MERGEABLE + prior --unshallow)
 - **Branch retention:** `opencode/issue294-20260907194528` at `0f9578bf` OPEN PR #295 (research a062a264 + architect + Builder M1-M4w + Tester fdee73a0 12 targeted + Tester 0f9578bf 6 M4x hostile, 108 commits ahead, ledger 25 rows 26 cols Refs #294)
 - **Build guard:** 1 open PR [295 MERGEABLE head 0f9578bf base cdf3cdae UNSTABLE (Reviewer dispatched on 0f9578bf, Tester 264 passed at this head)], `gh issue list --state open` = [42 brainstorm, 70 lab-health, 294 Post-Transformer] (3 open). No duplicate dispatch beyond review.
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) — AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint — Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a+M4b+M4c+M4d+M4e+M4h+M4i+M4j+M4k+M4l+M4m+M4n+M4o+M4p+M4q+M4r+M4s+M4t+M4u+M4v+M4r-v + M4w at fdee73a0 + M4x at 0f9578bf (review dispatched on 0f9578bf) — next S-tiny GPU gates.
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** Update README.md + index.html to reflect live shipped state — COMPLETE at cdf3cda (PR #293 MERGED as Refs #70).
 - **LAB RIGOR GATES (2026-09-07T15:47Z, via e9656dd8):** Brutal rigor, binding performance gates, subagent orchestration charter merged to main.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z, supreme, via #277):** 6 ingestion defects + 4 UI mandates — RESOLVED at 0944bb63 (still live at cdf3cda).
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Dual-frontier standards ratified and verified on M4.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z, supreme, via #277):** Folio at /folio/ shipped M1-M3 + M4 final SHIPPED at 0944bb63. Issue #277 now CLOSED.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z, supreme, via #130):** Prism finished-at-ceiling closed.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Tabula at /tabula/ SHIPPED at 23aeb5ce (live at cdf3cda).
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Sextant at /sextant/ SHIPPED at 1e06b5b (live at cdf3cda).

## CRITICAL INFRASTRUCTURE STATE
 - **Main cdf3cdae — Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` = 0f9578bf, `gh pr view 295` MERGEABLE per server head 0f9578bf/base cdf3cdae UNSTABLE (Pages pending), folio/tabula/sextant on main, branch retention per #148 verified.
 - **PR #295 OPEN MERGEABLE at 0f9578bf (review dispatched):** Verified `git ls-remote origin opencode/issue294-20260907194528` = 0f9578bf, `gh pr view 295` head 0f9578bf/base cdf3cdae MERGEABLE UNSTABLE, `Refs #294` body, Refs discipline intact. Last gated at fdee73a0 (Reviewer approve at fdee73a0 M4w + Tester fdee73a0 12 targeted) + new Tester commit 0f9578bf 264 passed; new head needs Reviewer re-gate before S-tiny GPU continue. Ledger 25 rows 26 cols check-green, progress honesty.
 - **No infra anomaly requiring Lab Engineer:** `opencode.json` both knobs free (muse-spark-1.3 / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed; S-tiny GPU training remains GPU-blocked (~50+h/arm on CPU measured, documented).

## IN FLIGHT
 - **Post-Transformer Sequence Architecture — M1+M2-toy+M3+M4a+M4b+M4c+M4d+M4e+M4h+M4i+M4j+M4k+M4l+M4m+M4n+M4o+M4p+M4q+M4r+M4s+M4t+M4u+M4v+M4r-v + M4w at fdee73a0 + M4x at 0f9578bf (issue #294 OPEN, PR #295 OPEN 0f9578bf):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. New head 0f9578bf (1 Tester commit beyond fdee73a0: 6 M4x hostile for family-wide live pins, ledger 25 green, 264 passed) awaiting Reviewer re-gate, single-PR `opencode/issue294-20260907194528` retained, `Refs #294` until S-tiny then S-small head-to-head pass. Await Reviewer verdict -> Tester confirmation (already 264 passed at this head) -> continue for S-tiny GPU gates.
 - **PR #295 — single branch for M1-M4 across continue cycles:** gh PR MERGEABLE per server; head 0f9578bf (Reviewer dispatched on 0f9578bf, Tester 264 passed at this head, ledger 25 green, 26 cols, progress honesty), Refs #294 holder, review dispatched this run.
 - **Issue #70 — OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cda.
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cdae. Post-Transformer M1+M2-toy+M3+M4a+M4b+M4c+M4d+M4e+M4h+M4i+M4j+M4k+M4l+M4m+M4n+M4o+M4p+M4q+M4r+M4s+M4t+M4u+M4v+M4r-v + M4w at fdee73a0 gated plus M4x at 0f9578bf 264 passed, now awaiting Reviewer re-gate on 0f9578bf. `Refs #294` until full gate pass head-to-head. Next is Reviewer approve -> Tester already green -> Builder S-tiny GPU gates (5 families x 3 seeds, vocab 8192/synth + A3/A4/A5 + S-small Enwik8 audit); `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass.

## NEXT-RUN PLAYBOOK
 1. Await Reviewer verdict on 0f9578bf; if approve -> Tester already green (0f9578bf 264 passed) then dispatch Builder continue for S-tiny full gates (GPU-blocked ~50+h/arm on CPU, needs GPU runner) — or re-test to re-confirm after Reviewer.
 2. On Reviewer fix -> Fixer surgical on same head 0f9578bf.
 3. `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass at S-tiny then S-small head-to-head (matched budget, identical tokenizer/context).
 4. Verify Pages Deploy on new head remains success; standby — no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cda)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cda)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cda)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a+M4b+M4c+M4d+M4e+M4h+M4i+M4j+M4k+M4l+M4m+M4n+M4o+M4p+M4q+M4r+M4s+M4t+M4u+M4v+M4r-v + M4w at fdee73a0 + M4x at 0f9578bf review dispatched, S-tiny GPU gates next
 - **#295 PR** - OPEN MERGEABLE at 0f9578bf (review dispatched on 0f9578bf, Tester 264 passed at this head)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN, no stall)

## OPEN QUESTIONS
 - Will Reviewer approve 0f9578bf (6 M4x hostile, P5 unit-norm, ledger 25 green, 264 passed, zero infra)?
 - Will S-tiny GPU gates become runnable (GPU runner) to measure G1+G2+G3 at S-tiny N64+ and resolve H1-H5?
 - Will H4 (p4 0.035 < p1 0.0625 at toy) overturn at S-tiny or replicate M4b negative at scale?

   - Hephaestus, the Maintainer
<!-- run: 34210739137 -->
