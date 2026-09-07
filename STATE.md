# STATE - Random factory checkpoint
 - **Updated:** 2026-09-07T22:36Z, maintainer run 34167238152 (event `created` on PR #295, M2 toy falsification at 974684cb — dispatching Reviewer)
 - **Action this run:** DISPATCH `[{"action":"review","pr":295,"head":"974684cb24327b9a9ebd4a8b64d6ad12766146f5"}]` — M2 toy falsification complete at 974684cb (3 commits beyond 4b9132f9), prior Reviewer 34161267877 blocked M1 with 10 findings (Fixer cancelled/re-dispatched never pushed), Builder M2 34161112912 now completed success; re-gating full head including unresolved M1 findings before Tester.
 - **Main:** `cdf3cdae489c7efd1b655e46af83623e722ace19` LIVE (successor to e9656dd8 via docs sync, `git ls-remote origin/main` = cdf3cdae, `git log --oneline -1` = cdf3cdae lab: mark Folio M4, Tabula, Sextant shipped on landing page (Refs #70), NOT orphan `merge-base e9656dd8 == e9656dd8`, `folio/` + `tabula/` + `sextant/` + `folio/packs/ocr+office` on main, Pages Deploy success on cdf3cdae 34157377631)
 - **Branch retention:** `opencode/issue277-20260904164811` at `bf67b253` MERGED at 0944bb63 retained, `opencode/issue282-*` Tabula at 23aeb5ce retained, `opencode/issue286-*` Sextant at 1e06b5b retained, `opencode/issue70-20260907160953` at `5f0c98f0` MERGED at cdf3cdae retained (docs sync, Refs #70), `opencode/issue294-20260907194528` at `974684cb` OPEN PR #295 (research a062a264 + architect ccbb2ca6 + Builder M1 ad520bcd/8d7a33cc/4b9132f9 + Builder M2 c125dc19/12b9877e/974684cb, ~100 files, 99 curves, `Refs #294`).
 - **Build guard:** 1 open PR [295 CLEAN head 974684cb base cdf3cdae MERGEABLE], `gh issue list --state open` = [42 brainstorm, 70 lab-health, 294 Post-Transformer] (3 open). Builder M1+M2 DONE (6 commits to 974684cb), Reviewer 34161267877 success posted 10 blocking findings on 4b9132f9 (still live at 974684cb per git show), Fixer prior 34161725768 cancelled + 34163229604 re-dispatch never pushed before M2 landed, Builder M2 34161112912 completed success at cdf3cdae head; new Review dispatched this run on 974684cb.

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42):** O(T^2)-free sequence architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) O(1) state + O(1) latency per token. Binding merge gate across all four. Research track: Dr. Mob survey -> Architect blueprint -> iterative M1-M4 builds on single PR #295 with head-to-head harness. Issue #294 OPEN; research+architect complete, M1+M2 toy falsification complete at 974684cb (postformer/ scaffold + baseline within 2% + harness 5 scripts + P1/P5/P1-W0/toy + T1-T6 + toy G1/G4 curves, Refs discipline intact), Reviewer re-dispatched, full S-tiny gates deferred (GPU runner).
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** Update README.md + index.html to reflect live shipped state — COMPLETE at cdf3cdae (PR #293 MERGED as Refs #70).
 - **LAB RIGOR GATES (2026-09-07T15:47Z, via e9656dd8):** Brutal rigor, binding performance gates, subagent orchestration charter merged to main.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z, supreme, via #277):** 6 ingestion defects + 4 UI mandates — RESOLVED at 0944bb63 (still live at cdf3cdae).
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Dual-frontier standards ratified and verified on M4.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z, supreme, via #277):** Folio at /folio/ shipped M1-M3 + M4 final SHIPPED at 0944bb63. Issue #277 now CLOSED.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z, supreme, via #130):** Prism finished-at-ceiling closed.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Tabula at /tabula/ SHIPPED at 23aeb5ce (live at cdf3cdae).
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Sextant at /sextant/ SHIPPED at 1e06b5b (live at cdf3cdae).

## CRITICAL INFRASTRUCTURE STATE
 - **Main cdf3cdae — Docs sync SHIPPED:** Verified via `git ls-remote origin/main` = cdf3cdae, NOT orphan, folio/tabula/sextant on main, Pages Deploy success on cdf3cdae.
 - **PR #295 OPEN CLEAN at 974684cb, Reviewer RE-DISPATCHED on new head:** Verified `gh pr view 295` OPEN MERGEABLE CLEAN head 974684cb24327b9a9ebd4a8b64d6ad12766146f5 base cdf3cdae, `git merge-base origin/main 974684cb` = cdf3cdae NOT orphan, `git log --oneline origin/opencode/issue294-20260907194528 --not origin/main` = a062a264 + ccbb2ca6 + ad520bcd + 8d7a33cc + 4b9132f9 + c125dc19 + 12b9877e + 974684cb (8 commits), branch `Refs #294` (single-PR discipline intact until G1+G2+G3+G4 pass), `progress/294-post-transformer-sequence-architecture.md` at 974684cb marks M1 [x] + M2 toy [x] (M2a T6 11 passed, M2b/c toy matched-budget 11 trainings + G4 flatness), smoke/toy rows honestly labeled NOT gate results. Reviewer 34161267877 (success) verified T1-T5 9 passed + parity +0.024%/+0.002% but raised 10 blocking fixes: (1) forward_chunk docstring loop no-op in p1_delta_hybrid.py:77-87 + p5_map.py:65-74, (2) viewer/index.html:32-40 quote-unaware CSV + XSS, (3) ledger.py:36-47 dedup missing, (4) ledger.py:50-103 check only first row + dead except, (5) factory.py stale pins + dead ternary + tie_embeddings guard, (6) proof-g4 arithmetic 3145824 vs 3146256 + fusion term, (7) parse_int_list k/K suffix, (8) length_sweep ckpt flag, (9) vocab column conflate 258 vs 8192, (10) hygiene imports/tmp_path/exact==0.0 — all still live at 974684cb per `git show` (forward_chunk still "Reference chunked forward: same math as step(), grouped in chunks of C", viewer still `l.split(",")`, factory still `~25.17M/~113.26M` + `parts[0] if len==1 else parts[0]`). New M2 adds RoPE O(1) fix via `RotaryEmbedding.row()` (parity 11/11 green post-fix) + toy G1 (MQAR N8 P5 0.300/P1 0.287/T 0.146, N16 collapse, 2-hop P5 0.532/P1 0.460/T 0.118) + G4 1k-32k flat (p1-toy 1.06ms flat <1%, bytes flat 24592 vs control linear).
 - **Builder continuation M2 COMPLETED + Reviewer re-queued:** Verified `gh api actions/runs/34161112912 --jq` = completed/success (was in_progress 94m at 21:28Z, now success at survey), `gh api actions/runs/34161725768` = completed/cancelled (fix never ran), `gh ls-remote origin opencode/issue294-20260907194528` = 974684cb (was 4b9132f9 at last maintainer, now superseded by 3-commit M2 push), `git ls-remote origin/main` = cdf3cdae stable, branch NOT orphan, `opencode.json` both knobs muse-spark-1.3/muse-spark-1.2-contributor-free free, no workflows permission rejection, Pages preview on 974684cb pending Deploy.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture — M2 TOY FALSIFICATION COMPLETE, RE-REVIEW DISPATCHED (#294 OPEN, PR #295 OPEN 974684cb):** Owner challenge via #42 — 4 binding gates vs Causal Transformer, matched budget. Researcher 34156774420 (a062a264, P1-P5 H1-H5 A1-A7) + Architect 34157097837 (ccbb2ca6, PostFormer Delta-Hybrid + W=128, M1-M4 roadmap) complete. Builder M1 delivered 3 commits (ad520bcd models baseline/P1/P5 + 8d7a33cc harness/ledger/T1-T5/viewer + 4b9132f9 smoke rows/G4 plots) + Builder M2 delivered 3 commits (c125dc19 trainer+toy+W0+T6 246+/10- + 12b9877e RoPE fix+toy scale T6 + 974684cb ledger+docs 15 rows/99 curves/G4 flatness, 11 tests passed, toy G1/G4 honestly ledgered, Refs #294 kept). Prior Reviewer blocked M1 but fixes still outstanding at new head; new Reviewer dispatched this run to re-gate inclusive of M2; next step Fixer on findings then Tester before any merge. PR stays `Refs #294` until G1+G2+G3+G4 pass head-to-head at S-tiny then S-small.
 - **PR #295 — single branch for M1-M4 across continue cycles:** No rebase needed (`merge-base` cdf3cdae); on Reviewer verdict expect `fix` on same head (apply 10 findings without clobbering trainer/toy work), then re-review, then `continue` for S-tiny trained gates (GPU runner, train.py supports tiny/small presets, ~25M x 3 arms x 3 seeds).
 - **Issue #70 — OPEN pinned lab-health board:** Must stay OPEN; merged as Refs #70 at cdf3cdae.
 - **No other active pipeline:** No infra anomaly, Auditor 34078079178 All green still authoritative, deploy on new head pending verification.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at cdf3cdae, lab rigor gates shipped, docs sync MERGED at cdf3cdae. Post-Transformer M2 toy falsification is complete and ledgered at 974684cb (15 rows check-green, 99 curves, G4 flat 1.06ms, H1/H5 unresolved honestly `Refs #294`), now awaiting Reviewer re-gate on same single PR #295 before Fixer and Tester; S-tiny GPU gates + M3/M4 deferred.

## NEXT-RUN PLAYBOOK
 1. Await Reviewer verdict on 974684cb (run dispatched this run): verify 10 M1 findings + new M2 trainer/toy determinism + RoPE flatness without vacuous T1.
 2. On `/oc fix:`: dispatch `{"action":"fix","pr":295}` to apply all findings on current head without clobbering M2a/b trainer work, preserving toy scale.
 3. On `/oc approve` (Reviewer): dispatch `{"action":"test","pr":295}` for harness determinism + G4 flat benchmark before any merge; verify `Refs #294` + no stubs + params within 2% + T1-T6 green.
 4. Then chain `{"action":"continue","pr":295}` for full S-tiny trained G1/G2/G3 (GPU runner) + M3 P3/P2 via `progress/294-post-transformer-sequence-architecture.md` M2->M3 roadmap; keep `Refs #294` until G1+G2+G3+G4 all pass head-to-head.
 5. Verify Pages Deploy on cdf3cdae and PR #295 preview remain green; otherwise standby — no auto-ideation.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at cdf3cdae)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at cdf3cdae)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at cdf3cdae)
 - **#293** - MERGED docs sync at cdf3cdae (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2 toy complete at 974684cb (PR #295 8 commits, Reviewer re-dispatched this run, 15 rows/99 curves, Refs #294, full S-tiny gates deferred to GPU)
 - **#295 PR** - OPEN CLEAN at 974684cb, Reviewer re-dispatched this run (prior blocked at 4b9132f9, fixes still live), Builder M2 completed success at cdf3cdae
 - **#42 - OPEN** brainstorm (78 comments, challenge recorded)
 - **#70 - OPEN** lab-health (docs sync SHIPPED at cdf3cdae via Refs #70)

## OPEN QUESTIONS
 - Will Reviewer on 974684cb re-confirm the 10 M1 blocking findings still live (forward_chunk docstring, viewer CSV/XSS, ledger dedup/check, factory pins/ternary/tie, proof-g4, parse_int_list, length_sweep, vocab, hygiene) plus any new M2 trainer/toy gaps, and block again for Fixer?
 - Will Fixer correctly apply all findings on 974684cb without clobbering M2 trainer/toy work (c125dc19/12b9877e) and preserve `-0.13%` toy parity + W=0 switch?
 - Will follow-up Reviewer approve after fixes and allow Tester gate for G1-G4 head-to-head S-tiny (GPU runner, train.py tiny/small presets) before any `Closes #294`?
 - Will single-PR `Refs #294` discipline hold through M2 fix + S-tiny/M3/M4 until all four gates pass head-to-head?

   - Hephaestus, the Maintainer
<!-- run: 34167238152 -->
