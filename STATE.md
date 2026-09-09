# STATE - Random factory checkpoint
 - **Updated:** 2026-09-09T18:22Z (maintainer run 34388421980 issue_comment, PR #296 MERGED 1ba831da, PR #295 still open)
 - **Action this run:** `[]` — MERGED PR #296 `1ba831da` via `gh pr merge --rebase` (dual-gated: Reviewer approve 18:19:19Z + Tester approve-test 18:20:40Z, read-only infra guard, parse/py_compile/curve green, Refs #294 correct, NOT orphan merge-base cdf3cdae). No new triggers; PR #295 still awaiting Tester on 053fac6c before chunked S-tiny continue.
 - **Main:** `1ba831da4bb439b4f1c14e5294cc919dfef1734b` LIVE (`git ls-remote origin/main` 1ba831da4bb439b4f1c14e5294cc919dfef1734b, `git log --oneline origin/main -1` 1ba831da lab: ship chunked CPU training workflow plus train_chunk resume driver (Refs #294) parent cdf3cdae, NOT orphan `git merge-base origin/main 92a2115` = cdf3cdae, PR #296 MERGED true, `gh pr view 296` MERGED at 2026-09-09T18:22:46Z)
 - **Branch retention:** `opencode/issue294-20260907194528` at `053fac6cb27957df225d61b2a3665ed6b63156a3` OPEN PR #295 (Reviewer APPROVED 18:04:43Z at 053fac6c, Tester in_progress `opencode-test` 18:04:47Z, `Refs #294`, MERGEABLE CLEAN per prior gate, awaiting Tester approve-test then chunked S-tiny/S-small continue) + `opencode/issue294-20260909181258` at `92a2115572974a63d7e0e696860834821b82de02` MERGED at 1ba831da (PR #296, Lab infra, retained per #148 pattern, Refs #294)
---

## STANDING OWNER DIRECTIVES (active)
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294:** O(T^2)-free architecture must beat/match Causal Transformer under matched param budget on 4 gates: (1) associative recall & tracking, (2) length generalization 4x-8x, (3) BPB on Enwik8, (4) **Inference Footprint - Pareto dominance**: asymptotic proof (no hidden T) + state-bytes and ms/token vs T 1k..32k. Tiers: (a) full O(1) flat within 5% 1k->32k; (b) conditional sublinear/subquadratic dominating baseline at every T with G1+G2+G3 green counts as `G4-tier-b` keep-worthy. Research track single-PR #295 Refs #294 until all gates pass; issue #294 OPEN; M1+M2-toy+M3+M4a-M4bc + Fixer/Tester hardening at 5f136f4a fully gated, M4bd/M4be verification at 053fac6c Reviewer-approved 18:04:43Z + Tester in_progress, Lab infra chunked CPU now MERGED at 1ba831da per 18:10:01Z parallel order.
 - **HARDWARE DIRECTIVE (2026-09-08T20:40:31Z, supreme, via #294) - CLARIFIED 2026-09-09T06:30:17Z via #294 (supreme):** No GPU runner is coming. All S-tiny/S-small training must run on standard GitHub CPU runners. Training scope is **not** reduced: same S-tiny/S-small budgets, same matched-budget discipline (params, training FLOPs/tokens, optimizer, tokenizer/context). Change the execution method (chunked, resumed, parallel), not the experiment size. Prior "reduced steps/tokens, micro-scales" interpretation is superseded - Builder must redesign for CPU feasibility via chunked/resumed/parallel execution while preserving full-budget head-to-head rigor and Refs #294 until all four gates pass. `Closes #294` only on G1+G2+G3+G4-tier-a/b green at full budget.
 - **PARALLELIZATION ORDER (2026-09-09T18:10:01Z, supreme, via #294):** Lab Engineer to ship the chunked CPU training workflow and Builder resume support in train.py **now**, concurrent with the Tester re-gate. They do not wait for the gate - new files only, no changes to gated code. Training launches the moment Tester greens. Dispatched at 18:10:01Z, landed as PR #296 at 92a2115, MERGED at 1ba831da 18:22:46Z concurrent with Tester re-gate on 053fac6c (still in_progress).
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** Update README.md + index.html to reflect live shipped state - COMPLETE at cdf3cda (PR #293 MERGED as Refs #70, verified README 48-54 + index.html cards Shipped).
 - **LAB RIGOR GATES (2026-09-07T15:47Z, via e9656dd8):** Brutal rigor, binding performance gates, subagent orchestration charter merged to main.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z, supreme, via #277):** 6 ingestion defects + 4 UI mandates - RESOLVED at 0944bb63 (still live at 1ba831da).
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Dual-frontier standards ratified and verified on M4.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z, supreme, via #277):** Folio at /folio/ shipped M1-M3 + M4 final SHIPPED at 0944bb63. Issue #277 now CLOSED.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z, supreme, via #130):** Prism finished-at-ceiling closed.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Tabula at /tabula/ SHIPPED at 23aeb5ce (live at 1ba831da).
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Sextant at /sextant/ SHIPPED at 1e06b5b (live at 1ba831da).

## CRITICAL INFRASTRUCTURE STATE
 - **Main 1ba831da - Lab chunked CPU infra MERGED:** Verified via `git ls-remote origin/main` = 1ba831da, `git log --oneline origin/main -2` = 1ba831da (Refs #294) -> cdf3cdae, `git merge-base origin/main 92a2115` = cdf3cdae NOT orphan, `gh api pulls/296 --jq .merged` = true at 18:22:46Z, `gh pr view 296` MERGED. Three new files (`postformer-cpu-train.yml` queued concurrency + fail-fast false + 340min cap + GITHUB_TOKEN only, `train_chunk.py` global-step cosine + resume.pt RNG + hparam guard, `gate_matrix.json` 18 arms gate-tiny-mqar 12.34M tokens/arm) now live on main. Deploy workflow `opencode-pr-trigger`/`Deploy` action_required on pre-merge 92a2115; post-merge Pages deploy on 1ba831da to be verified next run (will `gh workflow run pages.yml` if missing).
 - **PR #295 OPEN at 053fac6c (Reviewer APPROVED 18:04:43Z + Tester in_progress, Lab infra now on main):** Verified `git ls-remote origin opencode/issue294-20260907194528` = 053fac6c, `git ls-remote origin/main` = 1ba831da, `gh pr view 295` head 053fac6c/base 1ba831da (rebase will be clean, not orphan since both share cdf3cdae ancestor), `Refs #294` body, NOT orphan via server MERGEABLE prior (merge-base cdf3cdae), 225 commits a062a264..053fac6c doc-only beyond 5f136f4a (M4bd/M4be verification, ledger 25 green, py_compile clean, zero forward_chunk in shipped), parity within 2% preserved, Reviewer approve covers full M1-M4be (330 files postformer/|ideas/|docs/research/issue-294|progress/294-, zero infra touch), Tester 18:04:47Z still in_progress for 488+ tests including M4bd/M4be ground-truth, Lab infra now merged so chunked S-tiny continue can launch the moment Tester greens.
 - **No infra anomaly requiring emergency yet:** `opencode.json` both knobs free (muse-spark-1.3-free / muse-spark-1.2-contributor-free), no `workflows permission` rejection, no orphan recovery needed (main 1ba831da, PR #295 still MERGEABLE after base move via shared history, branch retention verified), production not halted; if Tester hits `The action has timed out.` will dispatch lab to raise timeout-minutes. Lab infra merged per parallel order.
 - **Model health:** Reviewer and Tester healthy, no CreditsError; PR #296 dual-gated merge proves pipeline green, PR #295 Tester still in_progress healthy.

## IN FLIGHT
 - **Post-Transformer Sequence Architecture - M1+M2-toy+M3+M4a-M4b-M4bc + Tester M4be hardening fully gated at 5f136f4a + M4bd/M4be verification at 053fac6c Reviewer-approved 18:04:43Z + Tester in_progress + Lab infra MERGED (issue #294 OPEN, PR #295 OPEN 053fac6c, PR #296 MERGED 1ba831da):** Owner challenge via #42 with binding 4 gates (G4 Pareto tiers a/b). Researcher + Architect complete. Branch live 053fac6c doc-only beyond fully-gated 5f136f4a (Reviewer 6202f202 + Tester 5f136f4a 488 passed; now Reviewer 053fac6c 18:04:43Z approved), `Refs #294` discipline intact, `Closes #294` only on full pass via chunked CPU. Per 18:10:01Z order, Lab Engineer shipped chunked CPU workflow + train_chunk resume (3 files +477) MERGED at 1ba831da concurrent with Tester re-gate; training launches the moment Tester greens.
 - **PR #295 - single branch for M1-M4 across continue cycles:** gh PR head 053fac6c/base 1ba831da `Refs #294`, MERGEABLE CLEAN prior, NOT orphan, single-PR discipline intact; next continue will carry S-tiny CPU full-budget gates via chunked/resumed/parallel (same params/tokens/FLOPs/tokenizer, matched-budget head-to-head, Refs #294) once Tester approve-test lands.
 - **PR #296 - MERGED at 1ba831da:** `lab: chunked CPU training workflow plus resume driver for PostFormer gates (Refs #294)` — 3 files, Reviewer + Tester dual-gated, no gated code change, now live on main for Builder resume.
 - **Issue #70 - OPEN pinned lab-health board:** Must stay OPEN; docs sync merged as Refs #70 at cdf3cda (now 1ba831da).
 - **No other active pipeline:** No Auditor bug, no orphan recovery needed; Lab MERGED, Tester in_progress on 053fac6c.

## PIPELINE POSITION
 Prism ceiling accepted, Tabula + Sextant + Folio M4 SHIPPED live at 1ba831da, lab rigor gates shipped, docs sync MERGED at cdf3cda. Post-Transformer M1+M2-toy+M3+M4a-M4b-M4bc fully gated at 5f136f4a (Reviewer 6202f202 + Tester 488 passed) plus doc-only M4bd/M4be verification at 053fac6c Reviewer-approved 18:04:43Z with Tester in_progress, Lab Engineer chunked CPU infra MERGED at 1ba831da per 18:10:01Z parallelization order (new files only). `Closes #294` only on G1+G2+G3+G4-tier-a/b all pass head-to-head at full S-tiny then S-small via chunked CPU once Tester greens.

## NEXT-RUN PLAYBOOK
 1. Verify post-merge Pages Deploy on 1ba831da (trigger `gh workflow run pages.yml` if missing) + confirm PR #295 rebase base 1ba831da still MERGEABLE (shared cdf3cdae ancestor).
 2. Await Tester approve-test on 053fac6c (488+ tests including M4bd/M4be ground-truth, in_progress 18:04:47Z) — no re-dispatch while in_progress.
 3. Builder continue on PR #295 for S-tiny CPU full-budget gates via chunked/resumed/parallel (same params/tokens/FLOPs/tokenizer, matched-budget head-to-head, Refs #294) — launches the moment Tester greens per 18:10:01Z order.
 4. Standby - no auto-ideation while #294 active.

## ISSUES
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at 1ba831da)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at 1ba831da)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at 1ba831da)
 - **#293** - MERGED docs sync at cdf3cda (Refs #70)
 - **#294 Post-Transformer** - OPEN research+architect+M1+M2-toy+M3+M4a-M4b-M4bc fully gated at 5f136f4a + M4bd/M4be verification at 053fac6c Reviewer-approved + Tester in_progress + Lab infra MERGED at 1ba831da (needs S-tiny/S-small CPU full-budget gates via chunked/resumed/parallel)
 - **#295 PR** - OPEN at `053fac6cb27957df225d61b2a3665ed6b63156a3` (Reviewer APPROVED 18:04:43Z, Tester in_progress 18:04:47Z, Refs #294) supersedes 5f136f4a
 - **#296 PR** - MERGED at `1ba831da4bb439b4f1c14e5294cc919dfef1734b` (Reviewer APPROVED 18:19:19Z + Tester approve-test 18:20:40Z, 3 files +477, Refs #294, NOT orphan, parent cdf3cdae)
 - **#42 - OPEN** brainstorm (challenge recorded, amended gate 4 via 294)
 - **#70 - OPEN** lab-health (GREEN pending)

## OPEN QUESTIONS
 - Will Tester re-gate 18:04:47Z green on 053fac6c including M4bd/M4be ground-truth before approve-test (currently in_progress)?
 - Will Builder CPU continue succeed with chunked/resumed/parallel full-budget S-tiny within GitHub runner time limits while preserving matched-budget rigor (same params/tokens/FLOPs)?
 - Will Lab chunked workflow resume correctly (artifact `ckpt-<model>-s<seed>` per arm, chunk-step windowing, resume.pt RNG, hparam-mismatch hard refusal) under CPU torch with OMP 4?
 - Will S-tiny/S-small G1+G2+G3+G4-tier-a/b gates pass under full CPU constraints vs toy negatives (p4 0.035 < p1 0.0625, ledger honestly NOT gate results)?

  - Hephaestus, the Maintainer
