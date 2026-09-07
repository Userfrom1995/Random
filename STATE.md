# STATE - Random factory checkpoint
 - **Updated:** 2026-09-07T22:39Z, maintainer run 34167402049 (schedule, Reviewer dispatch on M2 toy falsification head 974684c)
 - **Action this run:** DISPATCH `[{"action":"review","pr":295,"head":"974684cb24327b9a9ebd4a8b64d6ad12766146f5"}]` — M2 toy falsification complete (3 commits 4b9132f9..974684cb via Builder 34161112912), ledger 15 rows + 99 curves, G4 flatness proven with RoPE O(T) fix, H1/H5 unresolved honestly ledgered. Prior Reviewer block at 4b9132f9 superseded by new head; Re-reviewer needed to gate 10 findings carry-over + new T6/recursive plots.
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (successor to e9656dd8 via docs sync, `git ls-remote origin/main` = cdf3cdae, `git log --oneline -1` = cdf3cdae lab: mark Folio M4, Tabula, Sextant shipped on landing page (Refs #70), NOT orphan `merge-base e9656dd8 == e9656dd8`, `folio/` + `tabula/` + `sextant/` + `folio/packs/ocr+office` on main, Pages Deploy success on cdf3cdae 34157377631 and PR heads 34167218079 + 34161040802 + 34161725798)
 - **Branch retention:** `opencode/issue277-20260904164811` at `bf67b253` MERGED at 0944bb63 retained, `opencode/issue282-*` Tabula at 23aeb5ce retained, `opencode/issue286-*` Sextant at 1e06b5b retained, `opencode/issue70-20260907160953` at `5f0c98f0` MERGED at cdf3cdae retained (docs sync, Refs #70), `opencode/issue294-20260907194528` at `974684c` OPEN PR #295 (research a062a264 + architect ccbb2ca6 + Builder M1 ad520bcd/8d7a33cc/4b9132f9 + M2a c125dc19 + M2b 12b9877e + M2c 974684cb, 78+ files, ledger 15 rows + 99 curves).
 - **Build guard:** 1 open PR [295 CLEAN head 974684c], `gh issue list --state open` = [42 brainstorm, 70 lab-health, 294 Post-Transformer] (3 open). Builder M1+M2 DONE (Builder 34161112912 completed success, pushed 974684c), Reviewer 34161267877 prior block at 4b9132f9 (10 findings) now stale on 974684c — new Review dispatched this run. Concurrent maintainer 34167238152 in_progress on main (issue_comment) will dedup via guard, not targeting PR. PR body `Refs #294` (single-PR discipline intact).

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42):** O(T^2)-free sequence architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) O(1) state + O(1) latency per token. Binding merge gate across all four. Research track: Dr. Mob survey -> Architect blueprint -> iterative M1-M4 builds on single PR #295 with head-to-head harness. Issue #294 OPEN; research+architect complete, M1 code complete at 4b9132f9, M2 toy falsification complete at 974684c (15 ledger rows, G4 flatness, RoPE fix), Reviewer re-dispatched on 974684c.
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** Update README.md + index.html to reflect live shipped state — COMPLETE at cdf3cdae (PR #293 MERGED as Refs #70).
 - **LAB RIGOR GATES (2026-09-07T15:47Z, via e9656dd8):** Brutal rigor, binding performance gates, subagent orchestration charter merged to main.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z, supreme, via #277):** 6 ingestion defects + 4 UI mandates — RESOLVED at 0944bb63 (still live at cdf3cdae).
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Dual-frontier standards ratified and verified on M4.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z, supreme, via #277):** Folio at /folio/ shipped M1-M3 + M4 final SHIPPED at 0944bb63. Issue #277 now CLOSED.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z, supreme, via #130):** Prism finished-at-ceiling closed.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Tabula at /tabula/ SHIPPED at 23aeb5ce (live at cdf3cdae).
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Sextant at /sextant/ SHIPPED at 1e06b5b (live at cdf3cdae).

## CRITICAL INFRASTRUCTURE STATE
 - **Main cdf3cdae — Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, NOT orphan, folio/tabula/sextant on main, Pages Deploy success on cdf3cdae 34157377631 and PR heads 34167218079 (974684c) + 34161040802 (4b9132f9) + pr-trigger 34167218125.
 - **PR #295 OPEN CLEAN at 974684c, Reviewer DISPATCHED this run:** Verified `gh pr view 295` OPEN MERGEABLE CLEAN head 974684cb24327b9a9ebd4a8b64d6ad12766146f5 base cdf3cdae, `git ls-remote origin opencode/issue294-20260907194528` = 974684c, `git log --oneline 974684c --not cdf3cdae --reverse` = a062a264 + ccbb2ca6 + ad520bcd + 8d7a33cc + 4b9132f9 + c125dc19 + 12b9877e + 974684cb (8 commits), `gh api pulls/295 --jq body` = `Refs #294` (single-PR discipline intact), `progress/294-post-transformer-sequence-architecture.md` at 974684c marks M1 [x] + M2 [x] toy falsification complete (M2a trainer+toy+W0+T6 11 passed, M2b 11 MQAR trainings, M2c A2+ G4 RoPE fix + 15 rows + 99 curves), RoPE O(T)-per-step fixed via RotaryEmbedding.row(), P1 1.06ms flat <1% growth 1k-32k, S-tiny analytic baseline 25M-805M linear vs P1 flat 3.15M. Reviewer 34161267877 prior 10 findings still need gate on new head (factory docstring, ledger check, proof-g4 numbers, etc). Branch NOT orphan `git merge-base cdf3cdae 974684c` = cdf3cdae, body Refs #294, no stubs, params within 2% per T2 extended to toy.
 - **Builder M2 complete, no in_progress builders:** Verified `gh api actions/runs/34161112912` = completed success (pushed 974684c via 3 commits), `opencode-pr-trigger` 34167218125 success + Deploy 34167218079 success on 974684c. No pending opencode/review/test in_progress except this maintainer 34167402049 and concurrent maintainer 34167238152 in_progress on main (duplicate guard, will skip). Prior fix 34161725768 cancelled superseded by M2 push — next fix will be on 974684c if Reviewer re-blocks.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture — M2 TOY FALSIFICATION COMPLETE, REVIEW DISPATCHED (#294 OPEN, PR #295 OPEN 974684c):** Owner challenge via #42 — 4 binding gates vs Causal Transformer, matched budget. Researcher 34156774420 (a062a264, P1-P5 H1-H5 A1-A7) + Architect 34157097837 (ccbb2ca6, PostFormer Delta-Hybrid + W=128, M1-M4 roadmap) complete. Builder delivered M1 (78 files +7366, 9 tests) + M2a/b/c (c125dc19 trainer+toy+W0+T6 11 passed, 12b9877e trainer curves, 974684cb ledger 15 rows + 99 curves, RoPE fix, G4 flatness). M2b MQAR N8 P5 0.300 / P1 0.287 / T 0.146, 2-hop P5 0.532 / P1 0.460 / T 0.118, A1 no delta advantage at toy, H1/H5 unresolved at N=256 honestly ledgered Refs #294. G2 OOD probe + G3 deferred to M4 (byte-mapped path validated). Reviewer DISPATCHED this run on 974684c via `{"action":"review","pr":295,"head":"974684c"}`; next step Reviewer approval then Tester before any merge, then continue for S-tiny GPU gates + M3 P3/P2.
 - **PR #295 — single branch for M1-M4 across continue cycles:** No rebase needed (`merge-base` cdf3cdae); on Reviewer approval expect Tester, then continue M2 ledgered S-tiny full gates + M3/M4; PR stays `Refs #294` until G1+G2+G3+G4 pass head-to-head.
 - **Issue #70 — OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cdae.
 - **No other active pipeline:** No infra anomaly, Auditor 34078079178 All green still authoritative, deploys green, review dispatched.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cdae. Post-Transformer M2 toy falsification complete at 974684c (15 rows, G4 flatness proven), Reviewer re-dispatched on 974684c, awaiting gate before S-tiny GPU training + M3/M4. Refs #294 discipline active.

## NEXT-RUN PLAYBOOK
 1. Await Reviewer on 974684c: verify 10 prior findings (docstrings, CSV+XSS, ledger dedup/check, factory, proof-g4, parse_int_list, length_sweep, vocab, hygiene) + new M2 code (RoPE fix, recursive plots, T6) — if `/oc fix:` then dispatch Fixer on 974684c, else dispatch Tester.
 2. On Reviewer approval: dispatch `{"action":"test","pr":295}` for harness determinism + G4 flat benchmark (1.06ms flat, 256x less at 32k) before any merge.
 3. Continue via `{"action":"continue","pr":295}` or `{"action":"build","issue":294}` for S-tiny full G1/G2/G3 GPU gates (hours on GPU, train.py supports tiny/small presets) + M3 P3/P2.
 4. Verify Pages Deploy on cdf3cdae and PR #295 preview remain green; concurrent maintainer 34167238152 will dedup.
 5. Otherwise standby — no auto-ideation.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cdae)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cdae)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cdae)
 - **#293** - MERGED docs sync at cdf3cdae (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2 toy complete at 974684c (PR #295 15 rows + 99 curves, Reviewer DISPATCHED this run on 974684c)
 - **#295 PR** - OPEN CLEAN at 974684c, Reviewer dispatched this run (prior block at 4b9132f9 superseded)
 - **#42 - OPEN** brainstorm (78 comments, challenge recorded)
 - **#70 - OPEN** lab-health (docs sync SHIPPED at cdf3cdae via Refs #70)

## OPEN QUESTIONS
 - Will Reviewer on 974684c approve M2 toy falsification (RoPE O(1) fix, recursive plots, T6, honest H1/H5) or re-block on remaining factory/ledger/proof hygiene carry-overs?
 - Will follow-up Tester approve G4 flat benchmark (1.06ms flat, bytes flat 3.15M vs 805M) and harness determinism before merge?
 - Will single-PR `Refs #294` discipline hold through S-tiny GPU gates + M3/M4 until all four gates pass head-to-head?
 - Will S-tiny trained gates (GPU runner) finally deliver G1 N256 and G2 4x/8x deltas + G3 Enwik8 BPB for full pass?

   - Hephaestus, the Maintainer
<!-- run: 34167402049 -->
