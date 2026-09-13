# STATE - Random factory checkpoint
 - **Updated:** 2026-09-13T07:13Z (maintainer run 34744690435 `created` on #302, owner review, main 493166ab LIVE, build dispatched)
 - **Action this run:** decision [{"action":"build","issue":302}] — owner review 2026-09-13T07:13:22Z (5 blocking groups, Refs #302) dispatched to Builder to fix harness p99 parser + session/churn adapters + charts + per-pooler pages + fairness; sweep of selected cells follows fix merge
 - **Main:** `493166ab6d6a29c5c2b0b8af4bd5080c7561db5b` LIVE (poolduel M4 deep-dives + ECharts 5.5.1 vendored SVG with VERSION sha256 e84270bd, harness/charts.py + loader + repro --charts, five per-pooler 7-section pages, main 8 comparison figures + published banner, 493166ab is Tester 19 tests commit, parent 93760177 -> ... -> cab2375c, grandparent cab2375c lab Pages trigger, 77ee77d M2 medians 111/79 valid, 8a8e098 M1 42/28 valid, Pages Deploy SUCCESS 34721239893 at 21:53:54Z on 493166ab verified 200, `opencode.json` two-knob `muse-spark-1.3-contributor-free`/`muse-spark-1.2-contributor-free` both free, trigger-list PASS)
 - **Branch retention:** `opencode/issue302-20260911141051` at `8eca8f16` MERGED PR #303 + `opencode/issue302-poolduel-m2` at `e9c2ea70` MERGED PR #306 + `opencode/issue302-poolduel-m3` at `e3bdf6a3` MERGED PR #307 + `opencode/lab-302-poolduel-sweep-commit` at `ba7ec6e` MERGED PR #308 + `opencode/lab-302-poolduel-pgdg-fix` at `aa08c52` MERGED PR #309 + `opencode/lab-302-poolduel-pooler-builds` at `2cad43fe` MERGED PR #310 + `opencode/lab-302-poolduel-pandoc-fix` at `f4a37f48` MERGED PR #311 + `opencode/lab-302-poolduel-pgagroal-deps` at `fdedaac9` MERGED PR #312 + `opencode/lab-302-poolduel-ci-env-fix` at `07235c83` MERGED PR #316 + `opencode/314-fix-maintainer-workflow-run-trigger` at `bc399524` MERGED PR #315 + `opencode/302-poolduel-adapter-fixes` at `eb07f10f` MERGED PR #317 + `opencode/302-poolduel-tx-pipeline-fixes` at `55c19cf0` MERGED PR #318 + `opencode/lab-302-poolduel-pages-trigger` at `2b91c0a` MERGED PR #319 at `cab2375c` + `opencode/issue302-20260912213237` at `838c079bc0a8b334c85173abc15611f3d90dcd10` MERGED PR #320 at `493166ab` (8 commits 49d50a11..493166ab, retained) + `f113eda` Fix researcher handoff + `8a8e09` M1 aggregate + `77ee77d` M2 aggregate + `cab2375c` Pages trigger + `493166ab` M4 deep-dives (all retained).

---

## STANDING OWNER DIRECTIVES (active)
 - **POOLDUEL (2026-09-11T12:22:20Z, supreme, via #42 -> #302) - ACTIVE, M1+M2 GREEN + Pages LIVE + M4 MERGED at 493166ab + Pages SUCCESS 34721239893 + Owner review 2026-09-13T07:13:22Z with 5 blocking groups (Refs #302, best-mode on shared load per SPEC.md:37-38/methodology.md:48-56) - build dispatched:** Exhaustive shootout at /poolduel/ - pgagroal master tip SHA pinned vs PgBouncer vs pgpool-II vs Odyssey vs pgcat + direct control; Supavisor deferred. Binding non-discrimination, pgbench TPC-B + SELECT/churn/prepared, clients >> pool_size, minutes+warmup+medians, p99/p999+errors, exhaustiveness via matrix/grid, CI round-robin + repro.sh, chunked. Phased M1 (transaction all five+control) -> M2 (remaining modes/I-O) -> M3 (charts/MDs/Pages) -> M4 (per-pooler deep-dives at /poolduel/pgagroal/, /pgbouncer/, /pgpool/, /odyssey/, /pgcat/ + main comparison, identical template neutrality, two-way nav, ECharts vendored SVG no CDN, per-point markers + hover config+cellID + zoom/toggles + bands + PNG export, every figure from report bundles, design bar one-message-per-chart labeled axes shared color N/A marked no truncated axes, two-tier verification deterministic SVG coordinates + vision screenshot PNG feed, precondition fixture vision test pin vision free model if needed, build M1-derived now M2 honestly-pending). Owner review 2026-09-13T07:13:22Z requires: (1) no pending cells/blank sections when data exists, (2) readable graphs with log toggle/x-sort/band/legend/iso/flatness/tooltip/palette fixes, (3) per-pooler pages list all configs with results, (4) fix p99 parser + session (S1-S4 pgagroal, S9/10/13/14 pgcat) + churn (-C) then re-run selected cells only with medians rebuild, (5) fairness hardening churn auth/SHOW/dataset-init/backend-count. Refs binding until gates + explicit @Userfrom1995 approval. Close rule overrides everything 2026-09-12T19:02Z.
 - **POST-TRANSFORMER CHALLENGE (2026-09-07T16:35:36Z, supreme, via #42) - AMENDED 2026-09-07T21:23:19Z via #294 - CLOSED 2026-09-10T09:10:36Z by Owner:** Halted per Owner-Only Stop Authority.
 - **HARDWARE DIRECTIVE (2026-09-08T20:40:31Z, supreme) - CLARIFIED 2026-09-09T06:30:17Z:** CPU-only chunked - now MOOT due to #294 closure.
 - **PARALLELIZATION ORDER (2026-09-09T18:10:01Z, supreme):** Lab chunked CPU workflow shipped at 1ba831da - COMPLETE.
 - **DOCS SYNC DIRECTIVE (2026-09-07T16:06:36Z, supreme, via #70):** COMPLETE and re-verified through 493166ab.
 - **LAB RIGOR GATES (2026-09-07T15:47Z):** Brutal rigor charter live.
 - **FOLIO M4 AUDIT DIRECTIVE (2026-09-04T16:44Z):** RESOLVED at 0944bb63.
 - **EXCELLENCE IN CRAFTSMANSHIP CHARTER (2026-09-04T16:28Z):** Ratified.
 - **FOLIO MILESTONE EPIC (2026-09-04T12:04Z):** Folio SHIPPED at 0944bb63.
 - **CEILING ACCEPTANCE (2026-09-03T19:06Z):** Prism finished-at-ceiling.
 - **TABULA SHIPPED (2026-09-04T03:57Z):** Live at 493166ab.
 - **SEXTANT SHIPPED (2026-09-04T09:52Z):** Live at 493166ab.

## CRITICAL INFRASTRUCTURE STATE
 - **Main 493166ab LIVE - Poolduel M1+M2 both GREEN + Pages SUCCESS + M4 deep-dives SHIPPED but Owner review 2026-09-13T07:13:22Z blocks Closes (5 groups):** `origin/main` = 493166ab verified via API and `git ls-remote`, parent cab2375c linear no orphan (merge-base cab2375c), harness adapters live but p99 parser broken (`pgbench.py:114-141` gives 3.9ms avg vs 249895ms p50, S1-S4/S9/10/13/14 session exits, churn -C null tps) causing 46/54 inconclusive, `poolduel/index.html` has pending cells 200-204/247/255, per-pooler pages placeholder Live data, charts.py needs log view/legend/sort/N/A/flatness/iso/palette fixes. `opencode-test.yml`/`opencode-review.yml` 120/90 + guard live, `opencode.json` two-knob free (`muse-spark-1.3-contributor-free`/`muse-spark-1.2-contributor-free`), Pages `Deploy static site` SUCCESS 34721239893 at 21:53:54Z on 493166ab, `maintainer.yml` workflows allowlist 12 verified PASS, `pages.yml` workflow_run declarative verified.
 - **Sweeps 34702737525 SUCCESS on ee8caaa -> 8a8e098 and 34710318693 SUCCESS on 8a8e098 -> 77ee77d (40-89m wall-clock):** `poolduel-m1` 9 chunks avg 39.2m max 88.9m success + aggregate 22s to 8a8e098; `poolduel-m2` 16 chunks avg 32.1m max 40.5m success + aggregate 19s to 77ee77d. Re-run of selected session/churn cells required after parser/adapter fixes (not full matrix).
 - **Trigger-list self-audit PASS:** `maintainer.yml` workflows list covers all 12 live workflow names + maintainer self excluded; dynamic `pages-build-deployment`/`Dependency Graph` are GitHub-managed not repo workflows, correctly excluded.
 - **Model ecosystem two-knob both free PASS:** `opencode.json` `muse-spark-1.3-contributor-free` + `muse-spark-1.2-contributor-free`, workflow `model:` inputs `muse-spark-1.3-contributor-free` + `muse-spark-1.2-contributor-free`, no CreditsError.
 - **No held runs:** `gh run list` shows Deploy success on 493166ab, no blocking `action_required`, 73 comments on #302 with latest owner review 2026-09-13T07:13:22Z.

## IN FLIGHT
 - **Poolduel #302 - M1 GREEN at 8a8e098 + M2 GREEN at 77ee77d (107 measured 46 na, 6 arms, raw 469), report live in git, Pages workflow_run LIVE + M4 MERGED at 493166ab but Owner review 2026-09-13T07:13:22Z requires 5-group fix (pending tables, graphs, per-pooler configs, p99 parser + session/churn re-run, fairness) -> Build dispatched:** Issue OPEN. PR #320 MERGED at 493166ab via Refs #302 (8 commits 49d50a11..493166ab rebased, branch retained). Keep `Refs #302` until parser fix + selected cell re-run + fairness-audit s4 re-check on main + Tier-1/Tier-2 + explicit @Userfrom1995 approval. Next Builder PR will carry Refs #302, then review/test/pages chain, then priced sweep of selected cells only.
 - **Sweep runs:** `poolduel-m1` = 34702737525 SUCCESS 15:36:23Z on ee8caaa -> 8a8e098 (9/9), `poolduel-m2` = 34710318693 SUCCESS 18:09:04Z on 8a8e098 -> 77ee77d (16/16), Pages = 34721239893 success 21:53:54Z on 493166ab
 - **Other open PRs:** `gh pr list --state open` = [] (0 open PRs) — next PR will be Builder fix for owner review

## PIPELINE POSITION
 Folio/Tabula/Sextant SHIPPED, lab rigor gates shipped, docs sync MERGED, chunked CPU MERGED, timeout fix MERGED, recover.sh MERGED, postformer halted, researcher handoff fix SHIPPED at f113eda, M1 sweep GREEN at 8a8e098, M2 sweep GREEN at 77ee77d, Pages workflow_run trigger SHIPPED at cab2375c with deploys SUCCESS, Poolduel #302 M4 MERGED at 493166ab but Owner review 2026-09-13T07:13:22Z (Refs #302, 5 groups) requires Builder fix + selected cell re-run + Tier-1/Tier-2 + fairness-audit before Closes — build dispatched this run.

## NEXT-RUN PLAYBOOK
 1. Verify Builder PR opens on opencode/issue302-* with fixes for 5 groups (pgbench p99 parser, adapters pgagroal/pgcat, runner -C, charts palette/sort/log/legend/N/A/iso/flatness, per-pooler full config tables, pending removal) and stays Refs #302.
 2. Review -> Test gates on that PR (Tier-1 17/17+ new sort/log, repro --charts, 198/198).
 3. After that PR merges, dispatch selected-cell sweep (session S1-S4/S9/10/13/14 + churn M1-6/W6-W10) only, rebuild medians/report.json, re-eval gates, then Pages deploy and re-verify.
 4. Enforce Refs #302 until fairness-audit s4 + Tester repro + @Userfrom1995 approval; monitor Get opencode version transient.

## ISSUES
 - **#302 Poolduel** - OPEN (M1 GREEN 8a8e098 28 measured, M2 GREEN 77ee77d 79 measured, M4 MERGED 493166ab but Owner review 2026-09-13T07:13:22Z blocks Closes — build dispatched for 5-group fix + selected re-run, Refs binding)
 - **#42** - OPEN brainstorm (FROZEN for new picks per Poolduel)
 - **#70** - OPEN lab-health (nominal, Auditor GREEN 34735074969 on 2026-09-13, no anomalies)

## OPEN QUESTIONS
 - Will Builder fix p99 parser so direct M1-1 lat_avg vs p50 aligns and 46/54 inconclusive drops to genuine timeouts only?
 - Will session (pgagroal S1-S4, pgcat S9/10/13/14) and churn (-C) selected re-run succeed after adapter fixes and produce measured medians vs staying inconclusive?
 - Will charts become readable at desktop/mobile with log toggle/legend/N/A/iso/flatness fixes and Tier-2 vision pass?

   - Hephaestus, the Maintainer
