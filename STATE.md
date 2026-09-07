# STATE - Random factory checkpoint
 - **Updated:** 2026-09-07T21:28Z, maintainer run 34163229604 (event `created` on PR #295, Reviewer /oc fix: blocked M1 at 4b9132f9, re-dispatching Fixer)
 - **Action this run:** DISPATCH `[{"action":"fix","pr":295}]` — Reviewer 34161267877 blocked M1 with 10 findings, prior Fixer 34161725768 cancelled (no push, remote still 4b9132f9), Builder M2 34161112912 still in_progress (M2a c125dc19 dangling not on branch) — duplicate guard lifted, Fixer re-queued via owner PAT.
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (successor to e9656dd8 via docs sync, `git ls-remote origin/main` = cdf3cdae, `git log --oneline -1` = cdf3cdae lab: mark Folio M4, Tabula, Sextant shipped on landing page (Refs #70), NOT orphan `merge-base e9656dd8 == e9656dd8`, `folio/` + `tabula/` + `sextant/` + `folio/packs/ocr+office` on main, Pages Deploy success on cdf3cdae 34157377631 and PR heads 34157357050 + 34161040802 + 34161725798)
 - **Branch retention:** `opencode/issue277-20260904164811` at `bf67b253` MERGED at 0944bb63 retained, `opencode/issue282-*` Tabula at 23aeb5ce retained, `opencode/issue286-*` Sextant at 1e06b5b retained, `opencode/issue70-20260907160953` at `5f0c98f0` MERGED at cdf3cdae retained (docs sync, Refs #70), `opencode/issue294-20260907194528` at `4b9132f9` OPEN PR #295 (research a062a264 + architect ccbb2ca6 + Builder M1 ad520bcd/8d7a33cc/4b9132f9, 78 files +7366) + dangling c125dc19 (M2a trainer+toy+T6, parent 4b9132f9, not on branch tip).
 - **Build guard:** 1 open PR [295 CLEAN head 4b9132f9], `gh issue list --state open` = [42 brainstorm, 70 lab-health, 294 Post-Transformer] (3 open). Builder M1 DONE (3 pushes to 4b9132f9), Reviewer 34161267877 success posted 10 blocking findings, Fixer RE-DISPATCHED this run (prior 34161725768 cancelled, new fix queued); Builder M2 in_progress 34161112912 via /oc continue (still running since 20:53:42Z, job build in_progress). Pending duplicates 34163236908 opencode pending + 34163236916 maintainer pending on main (both Research #294 done title, will be cancelled/skipped — not targeting PR).

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42):** O(T^2)-free sequence architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) O(1) state + O(1) latency per token. Binding merge gate across all four. Research track: Dr. Mob survey -> Architect blueprint -> iterative M1-M4 builds on single PR #295 with head-to-head harness. Issue #294 OPEN; research+architect complete, M1 code complete at 4b9132f9 (postformer/ scaffold + baseline within 2% + harness 5 scripts + P1/P5 + T1-T5 + smoke ledger/G4 plots), Reviewer found 10 blocking fixes, Fixer re-dispatched, M2 building.
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** Update README.md + index.html to reflect live shipped state — COMPLETE at cdf3cdae (PR #293 MERGED as Refs #70).
 - **LAB RIGOR GATES (2026-09-07T15:47Z, via e9656dd8):** Brutal rigor, binding performance gates, subagent orchestration charter merged to main.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z, supreme, via #277):** 6 ingestion defects + 4 UI mandates — RESOLVED at 0944bb63 (still live at cdf3cdae).
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Dual-frontier standards ratified and verified on M4.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z, supreme, via #277):** Folio at /folio/ shipped M1-M3 + M4 final SHIPPED at 0944bb63. Issue #277 now CLOSED.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z, supreme, via #130):** Prism finished-at-ceiling closed.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Tabula at /tabula/ SHIPPED at 23aeb5ce (live at cdf3cdae).
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Sextant at /sextant/ SHIPPED at 1e06b5b (live at cdf3cdae).

## CRITICAL INFRASTRUCTURE STATE
 - **Main cdf3cdae — Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, NOT orphan, folio/tabula/sextant on main, Pages Deploy success + PR #295 previews success (PR still at 4b9132f9 per `git ls-remote origin opencode/issue294-20260907194528` = 4b9132f9, Deploy 34161725798 success on 4b9132f9, PR trigger 34161725831 success).
 - **PR #295 OPEN CLEAN at 4b9132f9, Reviewer BLOCKED with 10 findings, Fixer RE-DISPATCHED:** Verified `gh pr view 295` OPEN MERGEABLE CLEAN head 4b9132f92bb222909d2313ba4ebe970399d7ce9b base cdf3cdae, 78 files +7366 (docs/research + ideas + postformer/ + harness + ledger + viewer + progress), branch NOT orphan `git merge-base cdf3cdae 4b9132f` = cdf3cdae, body `Refs #294` (single-PR discipline intact until G1+G2+G3+G4 pass), smoke `progress/294-post-transformer-sequence-architecture.md` at 4b9132f9 marks M1 [x] complete. Reviewer 34161267877 (success) verified T1-T5 9 passed + parity +0.024%/+0.002% but raised 10 blocking fixes: (1) forward_chunk docstring loop no-op, (2) viewer CSV quote-unaware + XSS, (3) ledger dedup missing, (4) ledger check only first row + dead except, (5) factory stale pins + dead ternary + tie_embeddings guard, (6) proof-g4 arithmetic 3145824 vs 3146256 + fusion term, (7) parse_int_list k/K suffix, (8) length_sweep ckpt flag, (9) vocab column conflate 258 vs 8192, (10) hygiene imports/tmp_path/exact==0.0. Origin head still 4b9132f9 (`git ls-remote` confirms, c125dc19 M2a is dangling 246+/10- commit not on branch tip, parent 4b9132f9 via `gh api commits/c125dc19`). Fixer must apply on 4b9132f9 head now, then rebase/merge M2a without clobbering.
 - **Builder continuation M2 in_progress + Fixer re-queued:** Verified `gh api actions/runs/34161112912 --jq status` = in_progress (issue_comment 20:53:42Z /oc continue, job build in_progress, steps Run opencode build agent in_progress), `gh api actions/runs/34161725768` = cancelled (fix never ran), new pending `34163236908` opencode pending + `34163236916` maintainer pending on main (both cancelled/skipped expected), `gh api actions/runs/34163229604` = this maintainer in_progress. Duplicate guard: no extra build dispatch; let fix apply 10 findings, then re-review, then M2 G1-G4.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture — M1 REVIEWED (BLOCKED), FIX RE-DISPATCHED, M2 STILL BUILDING (#294 OPEN, PR #295 OPEN 4b9132f9):** Owner challenge via #42 — 4 binding gates vs Causal Transformer, matched budget. Researcher 34156774420 (a062a264, P1-P5 H1-H5 A1-A7) + Architect 34157097837 (ccbb2ca6, PostFormer Delta-Hybrid + W=128, M1-M4 roadmap) complete. Builder M1 delivered 3 commits (ad520bcd models baseline/P1/P5 + 8d7a33cc harness/ledger/T1-T5/viewer + 4b9132f9 smoke rows/G4 plots/ideas entry, 78 files +7366, 9 tests passed, smoke random-init NOT gate results, G4 flat signature shown 3145824B flat vs baseline linear). Reviewer 34161267877 verified parity/T1-T5 but filed 10 blocking fixes. Fixer RE-DISPATCHED this run via `{"action":"fix","pr":295}` (prior 34161725768 cancelled, remote still 4b9132f9); next step Reviewer re-approval then Tester before any merge. PR stays `Refs #294` until G1+G2+G3+G4 pass head-to-head.
 - **PR #295 — single branch for M1-M4 across continue cycles:** No rebase needed (`merge-base` cdf3cdae); on Fixer push expect Reviewer (`/oc review head <new_sha>`), then continue M2 ledgered G1-G4 flat within 5% + A1/A2/H1/H5 real Enwik8. Dangling c125dc19 (M2a trainer + toy scale + W=0 switch + T6 11 passed) will be integrated by Fixer or next M2 push — verify no clobber.
 - **Issue #70 — OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cdae.
 - **No other active pipeline:** No infra anomaly, Auditor 34078079178 All green still authoritative, deploys green, fix re-queued.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cdae. Post-Transformer M1 is reviewed BLOCKED (10 findings) with Fixer re-dispatched on same single PR #295, M2 full S-tiny gates still building via continue 34161112912 (with dangling M2a), Refs #294 discipline active.

## NEXT-RUN PLAYBOOK
 1. Await Fixer push beyond 4b9132f9 (new head): verify 10 fixes applied (docstrings, CSV splitter+XSS, ledger dedup/check, factory, proof-g4 numbers, parse_int_list k/K, length_sweep ckpt docs, vocab column, hygiene) without clobbering M2a trainer work (c125dc19).
 2. On new head >4b9132f9: dispatch `{"action":"review","pr":295,"head":"<sha>"}` if not auto-triggered, verify Refs #294 + no stubs + params within 2% + T1-T5/T6 green.
 3. Monitor Builder M2 34161112912 — do NOT duplicate; pending 34163236908/34163236916 are duplicates on main and will be skipped. After review passes, dispatch `{"action":"test","pr":295}` for harness determinism + G4 flat benchmark before merge.
 4. Verify Pages Deploy on cdf3cdae and PR #295 preview remain green.
 5. Otherwise standby — no auto-ideation.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cdae)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cdae)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cdae)
 - **#293** - MERGED docs sync at cdf3cdae (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1 code complete at 4b9132f9 (PR #295 78 files +7366, Reviewer BLOCKED 10 findings, Fixer RE-DISPATCHED this run, M2 building 34161112912, dangling c125dc19)
 - **#295 PR** - OPEN CLEAN at 4b9132f9, Reviewer blocked, Fixer re-dispatched this run, Builder M2 in_progress 34161112912
 - **#42 - OPEN** brainstorm (78 comments, challenge recorded)
 - **#70 - OPEN** lab-health (docs sync SHIPPED at cdf3cdae via Refs #70)

## OPEN QUESTIONS
 - Will Fixer correctly apply all 10 blocking fixes on current head 4b9132f9 without clobbering M2a trainer/T6 work (c125dc19 dangling) and preserve toy scale?
 - Will follow-up Reviewer re-approve after fixes (no vacuous T1, correct docstrings, CSV RFC4180, ledger dedup, factory parity guard) and allow Tester gate for G1-G4 head-to-head S-tiny?
 - Will single-PR `Refs #294` discipline hold through M1 fix + M2 full gates until all four gates pass head-to-head at S-tiny then S-small?
 - Will Builder M2 34161112912 (90+ min in_progress since 20:53:42Z) finally push c125dc19+ beyond 4b9132f9 or does it need timeout/retry?

   - Hephaestus, the Maintainer
<!-- run: 34163229604 -->
