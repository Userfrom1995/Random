# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~17:55Z, maintainer run 32284310731, owner `/oc maintainer` on PR #90 after the Reviewer approved and the Tester started). **DECISIONS:** `continue` on PR #83 to implement the R11 cross-band/MA in-loop predictor (blueprint `df7942c`); PR #90 left to the pipeline (Reviewer-approved, Tester running) for a rebase-merge on `/oc approve-test`. Orphan-main break persists (non-blocking: gate unmet). PR #90's Finding #1 is now RESOLVED on the branch.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83. A fresh `/oc build this` does NOT override this - route to `continue` on the existing PR.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break - recurrence still live, Factory-caused)

- **Mergeability (BROKEN):** `main` = `8f4c15b` (single orphan commit, no parent). Branch root = orphan + commits -> head `df7942c` (R11 blueprint). `git merge-base origin/main <branch>` is EMPTY (confirmed exit 1). GitHub reports `CONFLICTING`/`dirty`; `gh pr merge --rebase` would fail. `--rebase` is impossible until the Factory re-links.
- **Root cause of the recurrence:** the merge-to-`main` step (and the Builder's "rebuild onto main" step) force-writes an orphan root instead of preserving history, and the opencode App historically could not push `main` to fix it.
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is measurable reproducibly.

## SYSTEMIC INFRASTRUCTURE BLOCKER (status: LIKELY RESOLVED as of ~17:54Z)

- **The opencode GitHub App appears to now HAVE `workflows` permission.** The Factory's second commit on PR #90 (`fbcaaf0`, a `.github/workflows/opencode.yml` edit) LANDED at 17:53:59Z, and PR #90 is MERGEABLE. The earlier rejections ("refusing to allow a GitHub App to create or update workflow ... without workflows permission", runs 32253718673 / 32284201449) did NOT reproduce on this push. Consequence: the Reviewer's Finding #1 on PR #90 WAS applied by the Factory, and future infra changes can likely self-heal. Owner should confirm the App's `workflows: write` grant stuck; if so, the prior "bot can NEVER modify workflow files" blocker is lifted.
- If the permission was only transient, PR #90's merge is still fine (the fix is already on the branch); only FUTURE workflow edits would re-block.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `df7942c`):
  - **DEFAULT shipped codec = 9.5208 bpp mean** (R10-B CFL committed; real Kodak effort-4, reproducible, `2026-08-19-r10.csv`). Beats optipng PNG (13.05) and WebP (9.61) - **both gates MET**. **JPEG XL 8.71 MISSED by ~0.81 bpp** (17/24 images above 8.71). Bit-exact.
  - **R10 build (2026-08-19):** R10-A Squeeze IMPLEMENTED but proven INERT on photographic Kodak (adds ~91 KB on kodim01; never-expand net discards it). R10-B CFL is the ONLY R10 component that helps (~0.5 bpp gain) and is kept. Combined R10 moved the codec 9.6678 -> 9.5208 bpp (WebP gate cleared).
  - **Empirical dead-ends (shared root cause = saturation of the per-pixel CMARC pipeline once coder is at `H(p)+epsilon` and predictor bank is at the JPEG-LS floor):** R3-A, R6-B, R7-A, R8-A, R9-A, R9-C, R10-A all INERT/DORMANT; R9-B +0.04; R10-B helps.
  - **KEY DIAGNOSIS:** the codec is pinned at the ~9.52 bpp ceiling for PNG + WebP. The ~0.81 bpp to JPEG XL is the per-pixel CMARC pipeline's ceiling WITHOUT a cross-band/property-tree (MA) in-loop context model. The fix is a cross-band predictor that references the LL sub-band sample at the same (i,j) - the documented JPEG XL lever and the only remaining blueprinted path to < 8.71.
  - **R11 blueprint DELIVERED (17:40Z, Architect, commit `df7942c`, `obsidian/docs/architect-r11-crossband-predictor-blueprint.md`):** threads the co-located LL sample into `Neighbors` (`ll` field), adds `PredictorId::CrossBand = 19`, extends the R9-B `WeightedTree` to a 6x6 basis `(L, T, TL, TR, ll, 1)`, decodes with zero signaled bytes. Build order R11-A (levels=1) -> R11-B (deep) -> R11-C (analyzer selects CrossBand / exploits `wLL`) -> R11-D (MA-tree context). Worst case ships unchanged 9.5208 (no regression).

## In flight

- **PR #90 (Factory infra PR, branch `opencode/factory-68-build-loop-duplicate-guard`, commits `aaae7cf` + `fbcaaf0`):** duplicate-Builder `concurrency` guard + orphan guard hardening. **Reviewer APPROVED (17:55:24Z)** - both findings resolved (Finding #1 orphan guard now resolves `build_branch` from PR head ref; Finding #2 no `Closes #68`). **Tester RUNNING** (`opencode-test` run 32284409052, in_progress from owner `/oc test` 17:55:26Z). PENDING `/oc approve-test` -> Maintainer rebase-merges with `--no-delete-branch` (no `Closes` keywords, so nothing auto-closes). This is infra, outside the 2-projects/day limit.
- **PR #83 (Obsidian, branch `opencode/issue68-20260818070512`, head `df7942c`):** R11 blueprint delivered. This run fires `continue` on PR #83 to implement R11-A/B/C/D and re-measure REAL Kodak effort-4 against the JPEG XL 8.71 gate. One-PR rule intact. Orphan-main break + unmet JXL gate still apply. `mergeable: CONFLICTING/dirty`.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above; the hard long pole. Needs R11 (cross-band / property-tree MA in-loop predictor) built by the Builder, re-measured on REAL durable Kodak.
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near - now that WebP is cleared, this should be scheduled soon).
- **Orphan-main re-link:** blocked on the App's ability to push `main`; the recurrence root cause in `opencode.yml` must be fixed before #83 can merge. The new orphan guard in PR #90 will ROUTE such cases to the Maintainer instead of merging, but `main` itself still needs re-linking.
- **Confirm `workflows` permission:** verify the App's `workflows: write` grant persisted (Factory pushed `fbcaaf0` successfully). If so, the prior systemic blocker is lifted and future infra changes self-heal.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#90 (Factory infra PR for #68 build loop)** - OPEN; Reviewer-approved; Tester running; pending merge on `/oc approve-test`. No `Closes #68`.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `df7942c`, **rebase-unmergeable** (orphan-main break, recurrence, Factory-caused; API CONFLICTING/dirty). Default 9.5208 (PNG + WebP MET; JXL unmet by +0.81). R10-A Squeeze inert; R10-B CFL helps. R11 blueprint delivered; Builder to implement R11-A..D via this run's `continue`.
- **PR #90:** OPEN, **REVIEWER-APPROVED**; Tester `in_progress`; orphan guard fixed (`fbcaaf0`), no `Closes #68`. Awaiting `/oc approve-test` -> rebase-merge `--no-delete-branch`.

## Next steps

1. **PR #83 `continue` (this run):** Builder implements R11-A (levels=1 cross-band predictor) first, re-measures REAL Kodak effort-4, then stacks R11-B (deep levels) -> R11-C (analyzer selects CrossBand / exploits `wLL`) -> R11-D (MA-tree context). Record `benchmarks/results/2026-08-19-r11-*.csv`. Each stage measured against the JPEG XL 8.71 gate.
2. **PR #90 merge (pending Tester):** on `/oc approve-test`, rebase-merge `--no-delete-branch`; close no issue (no `Closes` keyword). Confirm `pages.yml` ran.
3. **After R11 measured:** if JPEG XL gate clears (default < 8.71 bpp, alongside PNG 13.05 + WebP 9.61), rebase-merge (`--no-delete-branch`), close #68.
4. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current now that WebP is cleared.
5. **Orphan-main re-link + fix recurrence root cause** in `opencode.yml` (the new guard in #90 routes future orphans to the Maintainer, but `main` itself must be re-linked; do it once permission is confirmed).
6. **Confirm App `workflows: write`** persisted (Factory pushed the workflow edit).

## Open questions

- **Can R11 (cross-band / MA in-loop predictor) clear the +0.81 JPEG XL gap on REAL Kodak?** Transform + cross-band context is the only remaining blueprinted lever after every per-pixel enhancement (R1-R10) proved inert. WebP is cleared; JPEG XL is the hard long pole. Empirical verdict pending the Builder's R11 build (this run's `continue`) + real-Kodak re-measure.
- **Merge gate (owner override #2):** NOT met - default 9.5208 bpp > 8.71 JXL (PNG 13.05 + WebP 9.61 already MET). No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **Orphan-main break (recurrence):** `main` = `8f4c15b` orphan; branch = orphan root -> `df7942c`. `git merge-base` empty (confirmed exit 1). Factory must re-link AND fix the recurrence root cause; now that the App may have `workflows` permission, this becomes actionable. Non-blocking now (gate unmet) but must be fixed before #83 merges.
- **`workflows` permission blocker:** LIKELY RESOLVED - Factory pushed the `opencode.yml` edit `fbcaaf0` successfully at 17:53:59Z. Confirm persisted; if so, future infra edits self-heal.
- **Review staleness on #83:** last approve ~96a6075; current head `df7942c` un-reviewed (pre-implementation). Fresh review required after R11 build.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive (now WebP gate is cleared, so promotion should be scheduled).
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84, #87 CLOSED. Issue #68 stays OPEN until codecs beaten.

- Mae, the Maintainer
