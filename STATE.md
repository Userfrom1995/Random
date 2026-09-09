# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T19:09Z (maintainer run 34393408300 schedule, Tester timeout 34386818174 on 053fac6c, Lab dispatched)
 - **Action this run:** `[{"action":"lab","pr":295}]` — Tester `opencode-test` 34386818174 on 053fac6c timed out after 60m `Run opencode tester` (18:04:47Z-19:05:20Z, `The action has timed out.` `No decision file found.`, no approve-test/fix, Reviewer approve 18:04:43Z still valid, main 1ba831da Deploy 34388772223 success). Dispatching Lab Engineer on PR #295 to raise timeout-minutes (job 75->120, step 60->90) and fix silent stall handling before re-gate.
 - **Main:** `1ba831da4bb439b4f1c14e5294cc919dfef1734b` LIVE (`git ls-remote origin/main` 1ba831da, `git log --oneline origin/main -1` 1ba831da lab: ship chunked CPU training workflow plus train_chunk resume driver (Refs #294) parent cdf3cdae, NOT orphan `git merge-base origin/main 92a2115` = cdf3cdae, PR #296 MERGED true at 2026-09-09T18:22:46Z, Deploy 34388772223 success on 1ba831da verified)
 - **Branch retention:** `opencode/issue294-20260907194528` at `053fac6cb27957df225d61b2a3665ed6b63156a3` OPEN PR #295 (Reviewer APPROVED 18:04:43Z at 053fac6c, Tester TIMEOUT 34386818174 18:04:47Z `The action has timed out.` no decision, `Refs #294`, MERGEABLE UNKNOWN after base move to 1ba831da but shared cdf3cdae ancestor not orphan, awaiting Lab timeout fix then Tester re-gate) + `opencode/issue294-20260909181258` at `92a2115572974a63d7e0e696860834821b82de02` MERGED at 1ba831da (PR #296, Lab infra, retained per #148 pattern, Refs #294)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4bc + Fixer/Tester hardening at 5f136f4a fully gated, M4bd/M4be verification at 053fac6c Reviewer-approved 18:04:43Z + Tester timeout, Lab infra chunked CPU now MERGED at 1ba831da per 18:10:01Z parallel order.
 - **HARDWARE DIRECTIVE (2026-09-08T20:40:31Z, supreme, via #294) - CLARIFIED 2026-09-09T06:30:17Z via #294 (supreme):** No GPU runner is coming. All S-tiny/S-small training must run on standard GitHub CPU runners. Training scope is **not** reduced: same S-tiny/S-small budgets, same matched-budget discipline (params, training FLOPs/tokens, optimizer, tokenizer/context). Change the execution method (chunked, resumed, parallel), not the experiment size. Prior "reduced steps/tokens, micro-scales" interpretation is superseded - Builder must redesign for CPU feasibility via chunked/resumed/parallel execution while preserving full-budget head-to-head rigor and Refs #294 until all four gates pass. `Closes #294` only on G1+G2+G3+G4-tier-a/b green at full budget.
 - **PARALLELIZATION ORDER (2026-09-09T18:10:01Z, supreme, via #294):** Lab Engineer to ship the chunked CPU training workflow and Builder resume support in train.py **now**, concurrent with the Tester re-gate. They do not wait for the gate - new files only, no changes to gated code. Training launches the moment Tester greens. Dispatched at 18:10:01Z, landed as PR #296 at 92a2115, MERGED at 1ba831da 18:22:46Z concurrent with Tester re-gate on 053fac6c (timeout 34386818174).
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** Update README.md + index.html to reflect live shipped state - COMPLETE at cdf3cda (PR #293 MERGED as Refs #70, verified README 48-54 + index.html cards Shipped).
 - **LAB RIGOR GATES (2026-09-07T15:47Z, via e9656dd8):** Brutal rigor, binding performance gates, subagent orchestration charter merged to main.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z, supreme, via #277):** 6 ingestion defects + 4 UI mandates - RESOLVED at 0944bb63 (still live at 1ba831da).
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Dual-frontier standards ratified and verified on M4.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z, supreme, via #277):** Folio at /folio/ shipped M1-M3 + M4 final SHIPPED at 0944bb63. Issue #277 now CLOSED.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z, supreme, via #130):** Prism finished-at-ceiling closed.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Tabula at /tabula/ SHIPPED at 23aeb5ce (live at 1ba831da).
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Sextant at /sextant/ SHIPPED at 1e06b5b (live at 1ba831da).

## CRITICAL INFRASTRUCTURE STATE
 - **Main 1ba831da - Lab chunked CPU infra MERGED + Pages Deploy verified:** Verified via `git ls-remote origin/main` = 1ba831da, `git log --oneline origin/main -2` = 1ba831da (Refs #294) -> cdf3cdae, `git merge-base origin/main 92a2115` = cdf3cdae NOT orphan, `gh api pulls/296 --jq .merged` = true at 18:22:46Z, `gh pr view 296` MERGED. Three new files (`postformer-cpu-train.yml` queued concurrency + fail-fast false + 340min cap + GITHUB_TOKEN only, `train_chunk.py` global-step cosine + resume.pt RNG + hparam guard, `gate_matrix.json` 18 arms gate-tiny-mqar 12.34M tokens/arm) now live on main. Deploy workflow 34388772223 success on 1ba831da verified; no pages re-trigger needed.
 - **PR #295 OPEN at 053fac6c (Reviewer APPROVED 18:04:43Z + Tester TIMEOUT 34386818174):** Verified `git ls-remote origin opencode/issue294-20260907194528` = 053fac6c, `git ls-remote origin/main` = 1ba831da, `gh pr view 295` head 053fac6c/base main `Refs #294` body, NOT orphan via server MERGEABLE prior (merge-base cdf3cdae, 225 commits a062a264..053fac6c doc-only beyond 5f136f4a), `gh api pulls/295 --jq mergeable` = unknown (check pending after base move, but shared cdf3cdae ensures rebase clean, not orphan), parity within 2% preserved per Reviewer, ledger 25 green, Reviewer approve covers full M1-M4be (330 files postformer/|ideas/|docs/research/issue-294|progress/294-, zero infra touch), Tester 34386818174 timed out 18:04:47Z-19:05:20Z `The action has timed out.` `No decision file found.` after 60m step, no approve-test/fix, needs Lab timeout raise then re-gate.
 - **Infra anomaly requiring Lab Engineer - timeout stall:** `opencode-test` job 75/step 60 timed out on 053fac6c (488+ tests including M4bd/M4be ground-truth) with `continue-on-error: true` masking as success but no decision file — classic silent stall per maintainer.md. `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan main, but production stalled on Tester gate. Ladder triggered: dispatch lab to raise timeout-minutes and add timeout detection.
 - **Model health:** Reviewer healthy (approve 18:04:43Z + prior lab review 18:19:19Z), Tester healthy but timed out on 053fac6c due to 60m cap (not CreditsError); PR #296 dual-gated merge proves pipeline green, lab timeout fix will restore.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4bc + Tester M4be hardening fully gated at 5f136f4a + M4bd/M4be verification at 053fac6c Reviewer-approved 18:04:43Z + Tester TIMEOUT 34386818174 + Lab infra MERGED (issue #294 OPEN, PR #295 OPEN 053fac6c, PR #296 MERGED 1ba831da):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Branch live 053fac6c doc-only beyond fully-gated 5f136f4a (Reviewer 6202f202 + Tester 5f136f4a 488 passed; now Reviewer 053fac6c 18:04:43Z approved, Tester timed out 1h0m32s). `Refs #294` discipline intact, `Closes #294` only on full pass via chunked CPU. Per 18:10:01Z order, Lab Engineer shipped chunked CPU workflow MERGED at 1ba831da; next Lab must fix Tester timeout before chunked S-tiny continue can launch.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head 053fac6c/base 1ba831da `Refs #294`, MERGEABLE UNKNOWN prior CLEAN but shared cdf3cdae ancestor ensures rebase clean not orphan, single-PR discipline intact; next continue will carry S-tiny CPU full-budget gates via chunked/resumed/parallel (same params/tokens/FLOPs/tokenizer, matched-budget head-to-head, Refs #294) once Lab raises timeout and Tester re-gates green.
 - **PR #296 - MERGED at 1ba831da:** `lab: chunked CPU training workflow plus resume driver for PostFormer gates (Refs #294)` — 3 files, Reviewer + Tester dual-gated, no gated code change, now live on main for Builder resume.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; docs sync merged as Refs #70 at cdf3cda (now 1ba831da).
 - **No other active pipeline:** Lab timeout fix dispatched, Tester blocked pending fix, no orphan recovery needed; Lab MERGED, Auditor nominal.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at 1ba831da, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4bc fully gated at 5f136f4a (Reviewer 6202f202 + Tester 488 passed) plus doc-only M4bd/M4be verification at 053fac6c Reviewer-approved 18:04:43Z with Tester TIMEOUT 34386818174 (60m cap, no decision) requiring Lab timeout raise. Lab Engineer chunked CPU infra MERGED at 1ba831da per 18:10:01Z parallelization order (new files only). `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at full S-tiny then S-small via chunked CPU once Tester re-gates.

## NEXT-RUN PLAYBOOK
 1. Verify Lab Engineer lands timeout raise on `opencode-test.yml` (job 75->120, step 60->90) + `opencode-review.yml` parity and silent-stall detection; merge via dual-gate then confirm PR #295 rebase base 1ba831da still MERGEABLE (shared cdf3cdae ancestor).
 2. Re-trigger Tester on PR #295 head 053fac6c (`/oc test`) for full 488+ re-gate including M4bd/M4be ground-truth (ledger 25 green, parity within 2%, causality) — no duplicate while Lab PR in flight.
 3. Builder continue on PR #295 for S-tiny CPU full-budget gates via chunked/resumed/parallel (same params/tokens/FLOPs/tokenizer, matched-budget head-to-head, Refs #294) — launches the moment Tester approve-test greens.
 4. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at 1ba831da)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at 1ba831da)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at 1ba831da)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4bc fully gated at 5f136f4a + M4bd/M4be verification at 053fac6c Reviewer-approved + Tester TIMEOUT 34386818174 (needs Lab timeout raise then re-gate, then S-tiny/S-small CPU full-budget gates via chunked/resumed/parallel)
 - **#295 PR** - OPEN at `053fac6cb27957df225d61b2a3665ed6b63156a3` (Reviewer APPROVED 18:04:43Z, Tester TIMEOUT 34386818174 18:04:47Z, Refs #294) supersedes 5f136f4a
 - **#296 PR** - MERGED at `1ba831da4bb439b4f1c14e5294cc919dfef1734b` (Reviewer APPROVED 18:19:19Z + Tester approve-test 18:20:40Z, 3 files +477, Refs #294, NOT orphan, parent cdf3cdae)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN pending - timeout stall to be logged next Auditor sweep)

## OPEN QUESTIONS
 - Will Lab Engineer raise Tester timeout (75->120/60->90) and fix silent stall so Tester re-gate on 053fac6c greens (currently timed out after 60m with no decision)?
 - Will Builder CPU continue succeed with chunked/resumed/parallel full-budget S-tiny within GitHub runner time limits while preserving matched-budget rigor (same params/tokens/FLOPs)?
 - Will Lab chunked workflow resume correctly (artifact `ckpt-<model>-s<seed>` per arm, chunk-step windowing, resume.pt RNG, hparam-mismatch hard refusal) under CPU torch with OMP 4?
 - Will S-tiny/S-small G1+G2+G3+G4-tier-a/b gates pass under full CPU constraints vs toy negatives (p4 0.035 < p1 0.0625, ledger honestly NOT gate results)?

  - Hephaestus, the Maintainer
