# STATE - Random factory checkpoint
 - **Updated:** 2026-09-11T14:42Z (maintainer run 34611760458 `created` on PR #303 main 540a68c9 head 5a1cd4fa)
 - **Action this run:** `lab` on PR #303 to re-promote poolduel M1 sweep workflow via PAT (tester approve-test at 5a1cd4fa)
 - **Main:** `540a68c9c015c5b118240674a6070d1c4e4f3953` LIVE (`gh api repos/Userfrom1995/RandomLabs/git/refs/heads/main --jq .object.sha` = 540a68c9, 120/90 + guard verified, Pages deploy success)
 - **Branch retention:** `opencode/issue294-20260907194528` at `053fac6cb27957df225d61b2a3665ed6b63156a3` CLOSED PR #295 (orphan vs 540a68c9, 225 commits, postformer 335 files not on main, retained per #148 - halted per Owner close of #294) + `opencode/issue294-20260909181258` at `92a2115572974a63d7e0e696860834821b82de02` retained (chunked CPU MERGED at 1ba831da) + `opencode/issue297-20260909222720` at `4c974926d260c5af1b4c26089fb639e527d92c59` MERGED PR #298 at 1d32e713 + `opencode/lab-299-recover-orphan-relink` at `f41145d88ba2a54906bf57dd5d31b212ffe28120` MERGED PR #300 at db4c8237 + `opencode/issue294-20260910085935` at `048464d5485f0ee908f3630cc9f857617100d61e` MERGED PR #301 at 540a68c9 + `opencode/issue302-20260911141051` at `5a1cd4fa7cb1871e8c26aa7a69bb1ba474a32cf3` OPEN PR #303 (Poolduel M1 harness, Refs #302, reviewer approved at 079b6a01, tester approved at 5a1cd4fa, lab promotion pending)
---

## STANDING OWNER DIRECTIVES (active)
 - **POOLDUEL (2026-09-11T12:22:20Z, supreme, via #42 -> #302) - ACTIVE:** Exhaustive, honest, publishable shootout of PostgreSQL poolers at /poolduel/ - pgagroal (master tip SHA pinned) vs PgBouncer vs pgpool-II vs Odyssey vs pgcat + direct-to-PG control; Supavisor deferred with written reason. Binding non-discrimination via single harness (identical adapter contracts, same timeouts/warmup/JSON/failure semantics, same machine/PG build/config/dataset, interleaved medians, every non-default cites tuning docs or fails review, every cell published). Methodology: pgbench TPC-B primary + SELECT-only + churn + prepared, clients >> pool_size mandatory, real scale factor, minutes+sustained+warmup, medians, throughput + p99/p999 + errors, reproducibility-by-adversary disclosure. Exhaustiveness: Researcher surveys docs/source per pooler, enumerates every pooling mode (transaction/session/statement/pipeline) + every I/O backend + every tunable into poolduel/docs/test-matrix before runs, bounded grids published, same cell budget, best-vs-best + iso-region matching, N/A never zero. CI round-robin + local repro script, chunked. Phased M1 (transaction pooling all five + control + harness live) -> M2 (remaining modes/I/O variants) -> M3 (charts, MDs, Pages report, fairness audit). Next: lab re-promote workflow on PR #303 5a1cd4fa -> merge Refs #302 -> M2 -> M3.
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294 - CLOSED 2026-09-10T09:10:36Z by Userfrom1995 (Owner):** Owner closed #294, pipeline halts on that track per Owner-Only Stop Authority. Branch retained, postformer stranded not on main, no further Builder/Tester chaining unless Owner reopens.
 - **HARDWARE DIRECTIVE (2026-09-08T20:40:31Z, supreme, via #294) - CLARIFIED 2026-09-09T06:30:17Z via #294 (supreme):** CPU-only chunked/resumed/parallel - now MOOT due to #294 closure (Poolduel will re-apply same CI-sizing).
 - **PARALLELIZATION ORDER (2026-09-09T18:10:01Z, supreme, via #294):** Lab chunked CPU workflow shipped at 1ba831da, hardening at 540a68c9 via PR #301 - COMPLETE (pattern reused for Poolduel).
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** COMPLETE at cdf3cdae and re-verified at 1d32e713/db4c8237/540a68c9.
 - **LAB RIGOR GATES (2026-09-07T15:47Z):** Brutal rigor charter live.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z):** RESOLVED at 0944bb63 live at 540a68c9.
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Ratified.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z):** Folio SHIPPED at 0944bb63.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z):** Prism finished-at-ceiling.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Live at 540a68c9.
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Live at 540a68c9.

## CRITICAL INFRASTRUCTURE STATE
 - **Main 540a68c9 LIVE - verified this run:** `gh api contents/.github/workflows/opencode-test.yml?ref=main` job 120 step 90 + fail-closed guard, `opencode-review.yml` 120/90 parity, `postformer-cpu-train.yml` present, `opencode.json` both knobs free (`muse-spark-1.3-contributor-free`/`muse-spark-1.2-contributor-free`), Pages deploy success (Deploy static site `success` on main + preview `/preview/pr-303/` staging). No held runs blocking.
 - **PR #303 Poolduel OPEN MERGEABLE at 5a1cd4fa:** `gh pr view 303 --json mergeable` = MERGEABLE, head 5a1cd4fa on `opencode/issue302-20260911141051` vs main 540a68c9, 6 commits (5c8d98bb researcher + 46fd8929 architect + 92cb200e harness + 4fa13da5 workflow-staged + 079b6a01 fixer + 5a1cd4fa tester), 41 files (poolduel/docs/*, harness 6 adapters, tests 65 green, repro.sh fixed, `poolduel/ci/poolduel-m1.yml` staged, `ideas/`, `progress/`). Body Refs #302 verified (0 Closes). `gh api contents/.github/workflows/poolduel-m1.yml?ref=5a1cd4fa` 404 (promotion dropped), `gh api contents/poolduel/ci/poolduel-m1.yml?ref=5a1cd4fa` exists 3493 bytes. `poolduel/repro.sh:20` PYTHONPATH=. verified.
 - **Reviewer APPROVED at 079b6a01 + Tester APPROVED at 5a1cd4fa this window:** `opencode-review` 34611234129 success `/oc approve` on 079b6a01 (both blockers cleared, 26/26 green, CLEAN); Fixer cleared repro.sh + Refs trailer; Tester `opencode-test` success at 14:42:23Z `/oc approve-test` on 5a1cd4fa (26/26 existing + 39 new hostile regression = 65/65 green, check ok, repro --dry-run rc=0, hygiene pass, YAML valid). Prod logic unchanged between 079b6a01 and 5a1cd4fa (tester commit only added `poolduel/tests/test_tester_regression.py`), so review remains valid for prod code; lab promotion is last gate before merge.
 - **Lab promotion DROPPED - re-promotion dispatched this run:** Lab Engineer run 34610712673 success at 14:32:16Z promoted 911aaa8e (poolduel/ci -> .github/workflows) but Fixer 079b6a01 reset to 4fa13da5 ancestry discarding 911aaa8e; Tester 5a1cd4fa inherits same ancestry, so workflow again staged at `poolduel/ci/poolduel-m1.yml`. This run dispatches `lab` on PR #303 to `git mv` via PAT (single mv, no edits) before merge so main gets workflow atomically.
 - **PR #295 CLOSED orphan at 053fac6c - HALTED per Owner close of #294:** Branch retained, postformer 335 files not on main, no recover dispatch while #294 closed per Owner-Only Stop Authority.
 - **Poolduel branch history verified descendant (but promotion lost):** `git ls-remote origin opencode/issue302-20260911141051` = 5a1cd4fa, `git ls-remote origin/main` = 540a68c9, common ancestor 540a68c9 non-empty, no orphan. Merge via rebase after lab.
 - **Model health:** `opencode.json` both knobs free, no workflows permission beyond PAT-handled, no green-but-empty stall.

## IN FLIGHT
 - **Poolduel #302 — M1 harness reviewer+tester approved, lab re-promotion dispatched:** Issue OPEN at 2026-09-11T12:24:56Z. Researcher 5c8d98bb + Architect 46fd8929 both landed. Builder M1 landed 92cb200e + 4fa13da5 + lab 911aaa8e (dropped) + fixer 079b6a01 + tester 5a1cd4fa (65/65 green, approve-test). Next: Lab re-promote workflow (this run) -> verify `.github/workflows/poolduel-m1.yml` exists on new head -> merge Refs #302 -> M2.
 - **PR #303 — lab dispatched at 5a1cd4fa:** OPEN at 14:18:26Z, head 5a1cd4fa MERGEABLE, author github-actions[bot], branch opencode/issue302-20260911141051. Comments: /oc architect 14:18:28Z -> architect success -> /oc build -> build success 14:29:48Z -> review+lab dispatched 14:32 -> lab success 911aaa8e -> review fix findings 14:36 -> fix success 079b6a01 -> review approve 14:39:36Z at 079b6a01 -> test 14:39:37Z -> tester approve-test 14:42:23Z at 5a1cd4fa (65/65 green) -> /oc maintainer 14:42:45Z this run. Lab re-dispatch now.
 - **Lab health #70 nominal, brainstorm #42 OPEN (frozen for new picks per Poolduel priority):** No ideate until Poolduel M1 merged.

## PIPELINE POSITION
 Folio/Tabula/Sextant SHIPPED live at 540a68c9, lab rigor gates shipped, docs sync MERGED, chunked CPU infra MERGED, timeout fix MERGED, recover.sh handler MERGED, postformer track halted by Owner closure of #294. Poolduel #302 is single lab priority; research -> architect -> builder M1 + fixer + reviewer approve + tester approve complete at 5a1cd4fa; lab re-promotion in flight this run, then merge Refs #302, then chain M2 (session/statement/I-O arms) via build per progress/302-poolduel.md.

## NEXT-RUN PLAYBOOK
 1. Verify Lab Engineer run on PR #303 succeeded (workflow now at `.github/workflows/poolduel-m1.yml` on new head, `poolduel/ci/` gone, branch MERGEABLE, head descendant of 540a68c9).
 2. Re-verify reviewer approval still covers prod logic (tester commit was test-only) — if lab head is test-only+mv, no extra review loop needed; otherwise dispatch `review` once on new head before merge.
 3. Merge PR #303 via `gh pr merge 303 --rebase` (Refs #302, never Closes until M3 gates). Verify `git merge-base origin/main <pr-head>` non-empty before merge.
 4. On intermediate M1 merge (Refs #302), immediately chain M2 build per progress/302-poolduel.md (no idle) - session/statement/I-O arms.
 5. No auto-ideation - Ideator only on explicit Owner request per Poolduel freeze.
 6. Verify `opencode-test.yml`/`opencode-review.yml` 120/90 + guard remain live.

## ISSUES
 - **#302 Poolduel** - OPEN (created 2026-09-11T12:24:56Z via run 34598572098, research 5c8d98bb + architect 46fd8929 + builder M1 92cb200e+4fa13da5 + lab 911aaa8e (dropped) + fixer 079b6a01 approved 14:39:36Z + tester 5a1cd4fa approved 14:42:23Z 65/65 green) - active, Refs until M3
 - **#303 PR** - OPEN at `5a1cd4fa7cb1871e8c26aa7a69bb1ba474a32cf3` on `opencode/issue302-20260911141051` vs main 540a68c9 MERGEABLE (Poolduel M1 harness, Refs #302, reviewer+tester approved, lab promotion dispatched this run)
 - **#130** - CLOSED (ceiling)
 - **#226** - CLOSED (HALTED)
 - **#277** - CLOSED SHIPPED at 0944bb63 (live at 540a68c9)
 - **#282 Tabula** - CLOSED SHIPPED at 23aeb5ce (live at 540a68c9)
 - **#286 Sextant** - CLOSED SHIPPED at 1e06b5b (live at 540a68c9)
 - **#293** - MERGED docs sync at cdf3cdae (Refs #70)
 - **#294 Post-Transformer** - CLOSED at 2026-09-10T09:10:36Z by Userfrom1995 (Owner) - HALTED, branch 053fac6c retained CLOSED orphan 225 commits
 - **#295 PR** - CLOSED at `053fac6cb27957df225d61b2a3665ed6b63156a3` (CLOSED 2026-09-09T22:32:41Z merged:false, ORPHAN vs 540a68c9, 335 files not on main, Refs #294) - retained, no recover while #294 closed
 - **#296 PR** - MERGED at `1ba831da4bb439b4f1c14e5294cc919dfef1734b` (chunked CPU)
 - **#297 Lab timeout** - CLOSED at 2026-09-10T12:10:01Z by Userfrom1995 (fix MERGED at 1d32e713 via PR #298 - verified)
 - **#298 PR** - MERGED at `1d32e713abcec659c11e36dfa9966ce56da79f9f` (workflow-only, Refs #297)
 - **#299 Lab recover.sh** - CLOSED via PR #300 at db4c8237 (Closes #299 + Refs #294)
 - **#300 PR** - MERGED at `db4c823711fa17618cf885c9dda43673d8dfaee4` (recover.sh handler)
 - **#301 PR** - MERGED at `540a68c9c015c5b118240674a6070d1c4e4f3953` (harden chunked CPU)
 - **#42** - OPEN brainstorm (frozen for new picks per Poolduel)
 - **#70** - OPEN lab-health (nominal)

## OPEN QUESTIONS
 - Will Lab Engineer `git mv poolduel/ci/poolduel-m1.yml .github/workflows/poolduel-m1.yml` land cleanly on head 5a1cd4fa without orphaning?
 - After Refs merge of M1, will M2 correctly build session/statement/I-O arms without breaking M1 harness invariants?
 - Will Owner ever reopen #294 or is Post-Transformer track intentionally halted? (no dispatch until explicit reopen)

  - Hephaestus, the Maintainer
