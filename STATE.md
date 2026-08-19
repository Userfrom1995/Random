# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~18:41Z, maintainer run 32288753918, schedule) - re-fired `continue` on PR #83 (head `df7942c`, unchanged) to implement R11; prior `continue` (32284310731) had not produced an implementation commit and no Builder was in flight. PR #90 MERGED (32285144475); #68 reopened.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (gh has no `--no-delete-branch` flag; simply omit `-d` to preserve the branch).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83. A fresh `/oc build this` does NOT override this - route to `continue` on the existing PR.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break - recurrence still live)

- **Mergeability (BROKEN):** `main` = `8f4c15b` (single orphan commit, no parent). Branch root = orphan + commits -> head `df7942c` (R11 blueprint). `git merge-base origin/main <branch>` is EMPTY (confirmed exit 1). GitHub reports `CONFLICTING`/`dirty`; `gh pr merge --rebase` would fail. `--rebase` is impossible until the Factory re-links.
- **Root cause of the recurrence:** the merge-to-`main` step (and the Builder's "rebuild onto main" step) force-writes an orphan root instead of preserving history, and the opencode App historically could not push `main` to fix it.
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is measurable reproducibly.

## SYSTEMIC INFRASTRUCTURE BLOCKER (status: RESOLVED as of ~17:54-18:05Z, CONFIRMED)

- **The opencode GitHub App / Factory CAN now push `.github/workflows/*.yml` edits.** Confirmed on PR #90: the Factory landed two workflow edits (`fbcaaf0` Reviewer Finding #1, `88b55b8` Tester non-fast-forward fix) and the branch merged cleanly to `main` (`b85f30e`). Future Factory infra changes self-heal.
- **NEW CAVEAT (commit-message auto-close):** GitHub's naive auto-close regex matches the literal token `Closes #68` (and Fixes/Resolves) ANYWHERE in a merged commit message, even inside quotes or negations. The merged commit `b85f30e` body said "PR body no longer uses 'Closes #68'", which auto-closed #68 against the standing directive. **Future Factory/Builder commits must NEVER write the literal phrase `Closes #68` (even quoted/negated).** #68 was reopened this run.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED (auto-closed by PR #90's merge, reopened 18:05Z); stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `df7942c`):
  - **DEFAULT shipped codec = 9.5208 bpp mean** (R10-B CFL committed; real Kodak effort-4, reproducible, `2026-08-19-r10.csv`). Beats optipng PNG (13.05) and WebP (9.61) - **both gates MET**. **JPEG XL 8.71 MISSED by ~0.81 bpp** (17/24 images above 8.71). Bit-exact.
  - **R10 build (2026-08-19):** R10-A Squeeze INERT on photographic Kodak (adds ~91 KB on kodim01; never-expand net discards it). R10-B CFL is the ONLY R10 component that helps (~0.5 bpp gain) and is kept. Combined moved the codec 9.6678 -> 9.5208 bpp (WebP gate cleared).
  - **KEY DIAGNOSIS:** the codec is pinned at the ~9.52 bpp ceiling for PNG + WebP. The ~0.81 bpp to JPEG XL is the per-pixel CMARC pipeline's ceiling WITHOUT a cross-band/property-tree (MA) in-loop context model. The fix is a cross-band predictor that references the LL sub-band sample at the same (i,j).
  - **R11 blueprint DELIVERED (17:40Z, Architect, commit `df7942c`):** threads co-located LL sample into `Neighbors` (`ll` field), adds `PredictorId::CrossBand = 19`, extends R9-B `WeightedTree` to a 6x6 basis `(L, T, TL, TR, ll, 1)`, decodes with zero signaled bytes. Build order R11-A (levels=1) -> R11-B (deep) -> R11-C (analyzer selects CrossBand / exploits `wLL`) -> R11-D (MA-tree context). Worst case ships unchanged 9.5208 (no regression). **R11 NOT yet implemented - head is still the blueprint `df7942c`.**

## In flight

- **PR #83 (Obsidian, branch `opencode/issue68-20260818070512`, head `df7942c`):** R11 blueprint delivered. `continue` re-fired on run 32288753918 to implement R11-A/B/C/D and re-measure REAL Kodak effort-4 against the JPEG XL 8.71 gate. One-PR rule intact. Orphan-main break + unmet JXL gate still apply. `mergeable: UNKNOWN`/CONFLICTING. Default 9.5208 (PNG + WebP MET; JXL unmet by +0.81). R10-A Squeeze inert; R10-B CFL helps. No implementation commit yet for R11.
- **PR #90 (Factory infra PR) - MERGED (18:05Z, run 32285144475).** Branch `opencode/factory-68-build-loop-duplicate-guard` preserved (no delete). Merged commit `b85f30e` on `main`. Delivered: duplicate-Builder `concurrency` guard + reliable head-ref orphan guard. PR body non-closing (no `Closes #68`). This is infra, outside the 2-projects/day limit. pages.yml re-triggered. The merged commit body contained a literal `'Closes #68'` that auto-closed #68; #68 reopened.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above; the hard long pole. Needs R11 (cross-band / property-tree MA in-loop predictor) built by the Builder, re-measured on REAL durable Kodak. (Re-engaged via `continue` this run.)
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near - now that WebP is cleared, this should be scheduled soon).
- **Orphan-main re-link:** blocked on the App's ability to push `main`; the recurrence root cause in `opencode.yml` must be fixed before #83 can merge. The new orphan guard in PR #90 will ROUTE such cases to the Maintainer instead of merging, but `main` itself still needs re-linking. Now that `workflows` permission is CONFIRMED, the Factory can fix the recurrence root cause - candidate for a future `factory` trigger (deferred until JXL gate is closer).
- **FUTURE `factory` candidate:** fix the merge step in `opencode.yml` that force-writes the orphan root on `main`, so the orphan-main recurrence cannot recur (and re-link `main` to the obsidian branch). Possible now that workflow edits land.
- **Commit-message hygiene:** never write the literal `Closes #68` token (even quoted/negated) in any commit message - GitHub auto-closes #68 on merge.

## Issues

- **#68 (Obsidian umbrella)** - REOPENED/OPEN (auto-closed by PR #90 merge, reopened 18:05Z); active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#52 / #90 infra** - PR #90 MERGED (infra hardening shipped).
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `b85f30e` (post PR #90 merge).
- **PR #83:** OPEN, head `df7942c`, **rebase-unmergeable** (orphan-main break, recurrence, Factory-caused; API CONFLICTING/UNKNOWN). Default 9.5208 (PNG 13.05 + WebP 9.61 MET; JXL 8.71 unmet by +0.81). R10-A Squeeze inert; R10-B CFL helps. R11 blueprint delivered; Builder to implement R11-A..D via run 32288753918 `continue`.
- **PR #90:** MERGED (18:05Z, run 32285144475). infra hardening on `main`; branch preserved; #68 reopened.

## Next steps

1. **PR #83 `continue` (re-fired run 32288753918):** Builder implements R11-A (levels=1 cross-band predictor) first, re-measures REAL Kodak effort-4, then stacks R11-B/C/D. Record `benchmarks/results/2026-08-19-r11-*.csv`. Each stage measured against the JPEG XL 8.71 gate.
2. **After R11 measured:** if JPEG XL gate clears (default < 8.71 bpp, alongside PNG 13.05 + WebP 9.61), rebase-merge (`--no-delete-branch`) - but only AFTER the Factory re-links `main` (orphan break fixed) - then close #68.
3. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current now that WebP is cleared.
4. **Orphan-main re-link + fix recurrence root cause in `opencode.yml`** (candidate `factory` trigger now that `workflows` permission is confirmed); re-link `main` to the obsidian branch before #83 merges.
5. **Commit-message hygiene:** enforce "never write literal `Closes #68`" in Factory/Builder commits (GitHub auto-close bug that bit #68 this run).

## Open questions

- **Can R11 (cross-band / MA in-loop predictor) clear the +0.81 JPEG XL gap on REAL Kodak?** Transform + cross-band context is the only remaining blueprinted lever after every per-pixel enhancement (R1-R10) proved inert. WebP is cleared; JPEG XL is the hard long pole. Empirical verdict pending the Builder's R11 build (run 32288753918 `continue`) + real-Kodak re-measure.
- **Merge gate (owner override #2):** NOT met - default 9.5208 bpp > 8.71 JXL (PNG 13.05 + WebP 9.61 already MET). No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **Orphan-main break (recurrence):** `main` = `8f4c15b` orphan; branch = orphan root -> `df7942c`. `git merge-base` empty (confirmed exit 1). The new orphan guard (PR #90, now on `main`) will ROUTE such cases to the Maintainer instead of merging, but `main` itself still needs re-linking. The Factory can fix the recurrence root cause now that workflow edits land; non-blocking now (gate unmet) but must be fixed before #83 merges.
- **#68 auto-close incident RESOLVED:** reopened 18:05Z after the PR #90 merge commit `b85f30e` body literally contained `'Closes #68'`. Future commits must avoid that token.
- **`workflows` permission blocker: RESOLVED (confirmed).** Factory pushed `fbcaaf0` + `88b55b8` (both workflow edits) and PR #90 merged to `main`. Future Factory workflow edits self-heal.
- **Review staleness on #83:** last approve ~96a6075; current head `df7942c` un-reviewed (pre-implementation). Fresh review required after R11 build.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive (now WebP gate is cleared, so promotion should be scheduled).
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84, #87 CLOSED. Issue #68 OPEN (reopened) until codecs beaten.

- Mae, the Maintainer
