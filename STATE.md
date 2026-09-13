# STATE - Random factory checkpoint
 - **Updated:** 2026-09-13T09:48Z (maintainer run 34750283106 `created` on PR #323, review SUCCESS awaiting test, main 3d0675 LIVE with sweeps COMMITTED)
 - **Action this run:** `[]` standby - PR #323 Curator README/landing sync 1ba19f84 APPROVED by Reviewer at 09:47:59Z (opencode-review 34750277425 SUCCESS) and forwarded to Tester via /oc test (opencode-test 34750314931 QUEUED), no duplicate dispatch, main 3d0675 LIVE (poolduel M1+M2 sweep results committed beyond 7bc6eb0f), Pages Deploy SUCCESS 34750284436 on 3d0675, trigger-list 13/13 PASS, two-knob free
 - **Main:** `3d067532c600384f9d9a92ac417aada2a2b92b51` LIVE (M2 sweep 1221f8bf + M1 sweep 3d0675 both Refs #302 committed on top of 7bc6eb0f; 7bc6eb0f was PR #321 MERGED Refs #302 at 08:04:09Z 10 commits 5+4+1 on top of c636ea90 curator feat + 493166ab M4 deep-dives; verified `git ls-remote origin/main` = 3d0675 and `git log --oneline origin/main -4` = 3d0675 M1 sweep + 1221f8bf M2 sweep + 7bc6eb0f tester suite + 148f469c/76d324d2/06e08ecb chain NOT orphan (merge-base 493166ab), `opencode.json` two-knob `muse-spark-1.3-contributor-free`/`muse-spark-1.2-contributor-free` both free, trigger-list PASS 13/13 `curator` includes, Pages Deploy SUCCESS 34750284436 on 3d0675)
 - **Branch retention:** `opencode/issue302-20260911141051` at `8eca8f16` MERGED PR #303 + `opencode/issue302-poolduel-m2` at `e9c2ea70` MERGED PR #306 + `opencode/issue302-poolduel-m3` at `e3bdf6a3` MERGED PR #307 + `opencode/lab-302-poolduel-sweep-commit` at `ba7ec6e` MERGED PR #308 + `opencode/lab-302-poolduel-pgdg-fix` at `aa08c52` MERGED PR #309 + `opencode/lab-302-poolduel-pooler-builds` at `2cad43fe` MERGED PR #310 + `opencode/lab-302-poolduel-pandoc-fix` at `f4a37f48` MERGED PR #311 + `opencode/lab-302-poolduel-pgagroal-deps` at `fdedaac9` MERGED PR #312 + `opencode/lab-302-poolduel-ci-env-fix` at `07235c83` MERGED PR #316 + `opencode/314-fix-maintainer-workflow-run-trigger` at `bc399524` MERGED PR #315 + `opencode/302-poolduel-adapter-fixes` at `eb07f10f` MERGED PR #317 + `opencode/302-poolduel-tx-pipeline-fixes` at `55c19cf0` MERGED PR #318 + `opencode/lab-302-poolduel-pages-trigger` at `2b91c0a` MERGED PR #319 at `cab2375c` + `opencode/issue302-20260912213237` at `838c079b` MERGED PR #320 at `493166ab` (8 commits 49d50a11..493166ab) + `c636ea90` curator feat + `opencode/issue302-20260913071636` at `7bc6eb0f` MERGED PR #321 (10 commits, Refs #302) + `1221f8bf` M2 sweep + `3d067532` M1 sweep (both Refs #302) + `opencode/issue322-curate-poolduel-readme-sync` at `1ba19f84` OPEN PR #323 (1 commit, Fixes #322, parent 3d0675, MERGEABLE CLEAN)

---

## STANDING OWNER DIRECTIVES (active)
 - **POOLDUEL (2026-09-11T12:22:20Z, supreme, via #42 -> #302) - ACTIVE, M1+M2 both GREEN at 8a8e098+77ee77d + M4 MERGED at 493166ab + owner-review fix MERGED at 7bc6eb0f Refs #302 + sweeps COMMITTED at 1221f8bf+3d0675 Refs #302 + Curator README sync at 1ba19f84 under review (Refs #302 for Poolduel, Fixes #322 for doc sync):** Exhaustive shootout at /poolduel/ - pgagroal master tip SHA pinned vs PgBouncer vs pgpool-II vs Odyssey vs pgcat + direct control; Supavisor deferred. Binding non-discrimination, pgbench TPC-B + SELECT/churn/prepared, clients >> pool_size, minutes+warmup+medians, p99/p999+errors, exhaustiveness via matrix/grid, CI round-robin + repro.sh, chunked. Phased M1 (transaction all five+control) -> M2 (remaining modes/I-O) -> M3 (charts/MDs/Pages) -> M4 (per-pooler deep-dives at /poolduel/pgagroal/ etc, identical template neutrality, two-way nav, ECharts vendored SVG no CDN, per-point markers + hover config+cellID + zoom/toggles + bands + PNG export, every figure from report bundles). Owner review 2026-09-13T07:13:22Z required 5 groups (parser session charts pages fairness) now fixed at 7bc6eb0f; selected-cell re-run (pgagroal S1-S4, pgcat S9/10/13/14, churn M1-6/W6-W10) now COMMITTED at 3d0675 as sweep results. Refs binding until gates + explicit @Userfrom1995 approval per 2026-09-12T19:02Z. PR #323 is isolated 2-line Curator doc sync (README+index) claiming medians published on main, not a Poolduel build gate.
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294 - CLOSED 2026-09-10T09:10:36Z by Owner:** Halted per Owner-Only Stop Authority.
 - **HARDWARE DIRECTIVE (2026-09-08T20:40:31Z, supreme) - CLARIFIED 2026-09-09T06:30:17Z:** CPU-only chunked - now MOOT due to #294 closure.
 - **PARALLELIZATION ORDER (2026-09-09T18:10:01Z, supreme):** Lab chunked CPU workflow shipped at 1ba831da - COMPLETE.
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** COMPLETE and re-verified through 3d0675 via Lab 34746843208 success (README.md:48-54 / index.html:121-158 Shipped at cdf3cdae, folio/tabula/sextant live).
 - **LAB RIGOR GATES (2026-09-07T15:47Z):** Brutal rigor charter live.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z):** RESOLVED at 0944bb63.
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Ratified.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z):** Folio SHIPPED at 0944bb63.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z):** Prism finished-at-ceiling.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Live at 493166ab.
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Live at 493166ab.

## CRITICAL INFRASTRUCTURE STATE
 - **Main 3d0675 LIVE - Poolduel M1+M2 sweep results COMMITTED at 1221f8bf+3d0675 (Refs #302) on top of 7bc6eb0f owner-review fix + M4 SHIPPED at 493166ab + Curator at c636ea90 + Pages LIVE:** `origin/main` = 3d0675 verified via `git ls-remote origin/main` = 3d0675 and `gh api repos/.../git/refs/heads/main` = 3d0675 and `git log --oneline origin/main -4` = 3d0675 M1 sweep + 1221f8bf M2 sweep + 7bc6eb0f tester suite + 148f469c fixer chain NOT orphan (merge-base 493166ab). `opencode.json` two-knob free (`muse-spark-1.3-contributor-free`/`muse-spark-1.2-contributor-free`), ECharts 5.5.1 vendored 1030855 sha256 e84270bd, harness/charts.py+loader+repro --charts live. Pages Deploy SUCCESS 34750284436 on 3d0675. `maintainer.yml` workflows allowlist 13/13 PASS includes `curator`, `curator.yml` 6h cron.
 - **PR #323 Curator 1ba19f84 OPEN MERGEABLE CLEAN - Reviewer APPROVED at 09:47:59Z (34750277425 SUCCESS) forwarded to Tester via /oc test (34750314931 QUEUED):** Diff 2 lines only (README.md:1 + index.html:1, stale No numbers -> M1 42 + M2 111 + report bundle published on main Refs #302), verified no creep, zero em dashes, security text-only PASS, mergeable MERGEABLE mergeStateStatus CLEAN, bot-authored, parent 3d0675. Tester run QUEUED at 09:48:43Z awaiting verdict; merge blocked until /oc approve-test per review gate, infrastructure guard PASS (no workflows touch).
 - **Sweeps COMMITTED beyond 7bc6eb0f:** poolduel-m1/m2 aggregate commits 1221f8bf (M2) + 3d0675 (M1) with Refs #302 are LIVE on main; prior dispatched runs 34747066313/34747067398 have been superseded by these commits. No duplicate sweep dispatch needed; await Tester gate for PR #323 then verify medians/report.json rebuilt with genuine selected-cell measurements (pgagroal S1-S4, pgcat S9/10/13/14, churn M1-6/W6-W10).
 - **Trigger-list self-audit PASS 13/13 fresh:** `maintainer.yml` workflows list `[auditor, "Deploy static site to GitHub Pages", "Lab Engineer", opencode-review, opencode-pr-trigger, opencode-test, ideate, opencode, opencode-recover, poolduel-m1, poolduel-m2, postformer-cpu-train, curator]` covers all live names; live `gh api actions/workflows --jq .workflows[].name` shows 14 inc dynamic (curator includes). No drift.
 - **Model ecosystem two-knob both free PASS:** `opencode.json` `muse-spark-1.3-contributor-free` + `muse-spark-1.2-contributor-free`, workflow `model:` inputs same, no CreditsError.
 - **No held runs beyond Tester QUEUED:** `gh run list` shows Tester 34750314931 QUEUED on PR #323 head, Reviewer 34750277425 SUCCESS, Pages 34750284436 SUCCESS on 3d0675; no blocking `action_required`.

## IN FLIGHT
 - **Poolduel #302 - M1 GREEN at 8a8e098 + M2 GREEN at 77ee77d (historical) + M4 MERGED at 493166ab + owner-review fix MERGED at 7bc6eb0f Refs #302 + sweeps COMMITTED at 1221f8bf+3d0675 Refs #302 (selected-cell rebuild LIVE):** Issue OPEN. Sweeps now committed beyond 7bc6eb0f; keep `Refs #302` until fairness-audit s4 re-check + Tester repro on new medians + explicit @Userfrom1995 approval.
 - **PR #323 Curator - OPEN at 1ba19f84 Fixes #322 (README+landing sync for published medians):** Reviewer /oc approve at 09:47:59Z SUCCESS, Tester /oc test QUEUED at 09:48:43Z (34750314931). Merge blocked until Tester /oc approve-test, then Fixes #322 will close #322.
 - **Lab health #70:** Lab Engineer 34746843208 success docs-sync satisfied, Auditor GREEN 34735074969, Pages live, sweeps committed.
 - **Sweep commits:** `1221f8bf` M2 sweep + `3d0675` M1 sweep on main (Refs #302); prior runs 34747066313/34747067398 superseded; Pages = 34750284436 success on 3d0675
 - **Other open:** #322 Curator issue OPEN (targeted by Fixes #322), #302 Poolduel OPEN, #42 brainstorm FROZEN, #70 lab-health nominal

## PIPELINE POSITION
 Folio/Tabula/Sextant SHIPPED, lab rigor gates shipped, docs sync MERGED, chunked CPU MERGED, timeout fix MERGED, recover.sh MERGED, postformer halted, researcher handoff fix SHIPPED at f113eda, M1 sweep GREEN at 8a8e098, M2 sweep GREEN at 77ee77d, Pages workflow_run trigger SHIPPED at cab2375c, Poolduel M4 MERGED at 493166ab + owner-review fix MERGED Refs #302 at 7bc6eb0f + selected-cell sweep results COMMITTED at 1221f8bf+3d0675 Refs #302, PR #323 Curator 1ba19f84 OPEN review APPROVED awaiting Tester, then merge Fixes #322.

## NEXT-RUN PLAYBOOK
 1. Await Tester verdict on PR #323 (34750314931): on /oc approve-test merge 1ba19f84 via --rebase to close Fixes #322; on /oc fix dispatch Fixer.
 2. After PR #323 merge, verify medians/report.json on 3d0675 are genuine selected-cell measurements (42 M1 + 111 M2 rows, report verdicts, 18 chart bundles, log twins, page scripts node --check) and Pages 200 on /poolduel/ + per-pooler pages.
 3. Enforce Refs #302 for Poolduel until fairness-audit s4 + Tester repro on new medians + explicit @Userfrom1995 approval grants Closes #302.
 4. No lab dispatch unless trigger-list drift; currently PASS 13/13.

## ISSUES
 - **#302 Poolduel** - OPEN (M1/M2 GREEN + M4 MERGED 493166ab + fix MERGED 7bc6eb0f Refs #302 + sweeps COMMITTED 1221f8bf+3d0675 Refs #302, awaiting fairness-audit s4 + Tester repro + @Userfrom1995 approval for Refs->Closes)
 - **#322 Curator sync** - OPEN ([Curator] Sync README and landing page: Poolduel M1/M2 medians now published, targeted by PR #323 Fixes #322, Reviewer approved 34750277425, Tester queued 34750314931)
 - **#42** - OPEN brainstorm (FROZEN for new picks per Poolduel)
 - **#70** - OPEN lab-health (nominal, Auditor GREEN 34735074969, Lab 34746843208 docs-sync satisfied, Pages 34750284436 success on 3d0675)

## OPEN QUESTIONS
 - Will Tester approve PR #323 (2-line Curator sync, text-only, 43 links verified + chart bundles) with /oc approve-test?
 - Do sweep commits 1221f8bf+3d0675 carry genuine selected-cell medians (pgagroal S1-S4, pgcat S9/10/13/14, churn M1-6/W6-W10) with timeout/inconclusive nulls never zero-filled?
 - Will Pages re-deploy on next commit after PR #323 merge succeed and will @Userfrom1995 grant Refs->Closes for Poolduel only after fairness-audit s4 re-check?

   - Hephaestus, the Maintainer
