# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~17:40Z, maintainer run 32282982614, owner `/oc maintainer` on PR #83 after the R11 blueprint delivered). **DECISIONS:** `continue` on PR #83 - resume the Builder to implement the cross-band / property-tree (MA) in-loop predictor (R11) that the Architect blueprinted to clear the JPEG XL 8.71 gate. Default codec = 9.5208 bpp (PNG + WebP MET; JPEG XL MISSED by +0.81). Orphan-main break persists (non-blocking: gate unmet).

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
- **Root cause of the recurrence:** the merge-to-`main` step (and the Builder's "rebuild onto main" step) force-writes an orphan root instead of preserving history, and the opencode App cannot push `main` to fix it (no `workflows` permission + branch protection rejected the earlier direct push).
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is measurable reproducibly.

## SYSTEMIC INFRASTRUCTURE BLOCKER (since 2026-08-19 ~12:40Z)

- **The opencode GitHub App has NO `workflows` permission.** Every pipeline agent (Factory/Builder/Fixer) pushes using the App token, so any edit to `.github/workflows/*.yml` is rejected. Confirmed on PR #90's Factory fix run 32253718673. Consequence: **the bot can NEVER modify workflow files.** The Reviewer's Finding #1 on PR #90 (orphan-guard hardening) therefore cannot be applied by the Factory. Owner must either grant `workflows: write` to the App, or apply workflow edits manually. This also makes the standing "Maintainer may only edit `.github/workflows/*.yml` for model switching" rule moot.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `df7942c`):
  - **DEFAULT shipped codec = 9.5208 bpp mean** (R10-B CFL committed; real Kodak effort-4, reproducible, `2026-08-19-r10.csv`). Beats optipng PNG (13.05) and WebP (9.61) - **both gates MET**. **JPEG XL 8.71 MISSED by ~0.81 bpp** (17/24 images above 8.71). Bit-exact.
  - **R10 build (2026-08-19):** R10-A Squeeze IMPLEMENTED but proven INERT on photographic Kodak (adds ~91 KB on kodim01; never-expand net discards it). R10-B CFL is the ONLY R10 component that helps (~0.5 bpp gain) and is kept. Combined R10 moved the codec 9.6678 -> 9.5208 bpp (WebP gate cleared).
  - **Empirical dead-ends (shared root cause = saturation of the per-pixel CMARC pipeline once coder is at `H(p)+epsilon` and predictor bank is at the JPEG-LS floor):**
    - R3-A residual-context INERT (model starvation under ~365x context blowup).
    - R6-B color cache DEAD END (inert on photographic residuals).
    - R7-A per-context weighted predictor REGRESSED (reverted).
    - R8-A signaling-free adaptive weighted predictor INERT.
    - R9-A spatial LZ77 DORMANT on photographic Kodak (0/24 images).
    - R9-B context-tree weighted predictor DONE (+0.04 help, moved to 9.6678).
    - R9-C copy-prev-val run mode INERT (reverted).
    - R10-A Squeeze INERT (escalated; needs cross-band predictor).
    - R10-B CFL HELPS (~0.5 bpp), kept.
  - **KEY DIAGNOSIS (settled across R9-R10):** the codec is pinned at the **~9.52 bpp ceiling** for PNG + WebP. The ~0.81 bpp to JPEG XL is the per-pixel CMARC pipeline's ceiling WITHOUT a cross-band/property-tree (MA) in-loop context model. Squeeze cannot help because its HF sub-bands are decimated grids whose in-band neighbours are 2 px away, so the in-loop predictor cannot decorrelate them. The fix is a cross-band predictor that references the LL sub-band sample at the same (i,j) - the documented JPEG XL lever and the only remaining blueprinted path to < 8.71.
  - **R11 blueprint DELIVERED (17:40Z, Architect, commit `df7942c`, `obsidian/docs/architect-r11-crossband-predictor-blueprint.md`):** threads the co-located LL sample into `Neighbors` (`ll` field, default 0 for plain/LL bands), adds `PredictorId::CrossBand = 19` (identity on `ll`), extends the R9-B `WeightedTree` to a 6x6 basis `(L, T, TL, TR, ll, 1)` so the learned weights exploit `ll` as a 5th input (strict superset -> zero regression on existing streams), and decodes with zero signaled bytes. Build order R11-A (levels=1) -> R11-B (deep) -> R11-C (analyzer selects CrossBand / exploits `wLL`) -> R11-D (MA-tree context). Target <= 8.71 (JPEG XL); worst case Squeeze stays inert and shipped number is unchanged at 9.5208 (no regression ships).

## In flight

- **PR #83 (Obsidian, branch `opencode/issue68-20260818070512`, head `df7942c`):** R11 blueprint delivered. This run fires `continue` on PR #83 to implement R11-A/B/C/D and re-measure REAL Kodak effort-4 against the JPEG XL 8.71 gate. One-PR rule intact. Orphan-main break + unmet JXL gate still apply. `mergeable: CONFLICTING/dirty`.
- **PR #90 (Factory infra PR, head `opencode/factory-68-build-loop-duplicate-guard`):** duplicate-Builder `concurrency` guard + orphan guard hardening. Reviewed: Finding #2 (Closes #68) already fixed; **Finding #1 (orphan guard at opencode.yml:421-431) BLOCKED** - bot cannot push workflow file (missing `workflows` permission). PR stays OPEN, awaiting owner action.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above; the hard long pole. Needs R11 (cross-band / property-tree MA in-loop predictor) built by the Builder, re-measured on REAL durable Kodak.
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near - now that WebP is cleared, this should be scheduled soon).
- **PR #90 workflow fix dependency:** Finding #1 cannot land until the owner grants `workflows` permission to the App OR applies the patch manually.
- **Orphan-main re-link:** blocked on the App's inability to push `main`; unfixed recurrence root cause. Owner-action item.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#90 (Factory infra PR for #68 build loop)** - OPEN; blocked on `workflows` permission for the orphan-guard fix (Finding #1). Finding #2 already resolved.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `df7942c`, **rebase-unmergeable** (orphan-main break, recurrence, Factory-caused; API CONFLICTING/dirty). Default 9.5208 (PNG + WebP MET; JXL unmet by +0.81). R10-A Squeeze inert; R10-B CFL helps. R11 blueprint delivered; Builder to implement R11-A..D via `continue`.
- **PR #90:** OPEN, review blocking finding #1 unapplied (bot permission wall), Finding #2 resolved (no `Closes #68`).

## Next steps

1. **PR #83 `continue` (this run):** Builder implements R11-A (levels=1 cross-band predictor) first, re-measures REAL Kodak effort-4, then stacks R11-B (deep levels) -> R11-C (analyzer selects CrossBand / exploits `wLL`) -> R11-D (MA-tree context stretch). Record `benchmarks/results/2026-08-19-r11-*.csv`. Each stage measured against the JPEG XL 8.71 gate.
2. **After R11 measured:** if JPEG XL gate clears (default < 8.71 bpp, alongside PNG 13.05 + WebP 9.61), rebase-merge (`--no-delete-branch`), close #68.
3. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current now that WebP is cleared.
4. **PR #90 (owner action):** grant `workflows: write` to the opencode App OR apply the orphan-guard patch manually + merge. Do not merge until Finding #1 resolved.
5. **Factory re-links `main` + fixes the orphan-root recurrence** (once the permission/root-cause allows). Non-blocking now (gate unmet) but must be fixed before merge.

## Open questions

- **SYSTEMIC `workflows` permission gap:** no pipeline agent can edit workflow files; blocks PR #90's Finding #1 and all future infra changes. Owner must grant permission or do manual merges.
- **Can R11 (cross-band / MA in-loop predictor) clear the +0.81 JPEG XL gap on REAL Kodak?** Transform + cross-band context is the only remaining blueprinted lever after every per-pixel enhancement (R1-R10) proved inert. WebP is cleared; JPEG XL is the hard long pole. Empirical verdict pending the Architect's R11 blueprint + the Builder's R11 build + real-Kodak re-measure.
- **Merge gate (owner override #2):** NOT met - default 9.5208 bpp > 8.71 JXL (PNG 13.05 + WebP 9.61 already MET). No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **Orphan-main break (recurrence):** `main` = `8f4c15b` orphan; branch = orphan root -> `df7942c`. `git merge-base` empty (confirmed exit 1). Factory must re-link AND fix the recurrence root cause; today the App cannot push main. Non-blocking now (gate unmet) but must be fixed before merge.
- **Review staleness:** last approve at head ~96a6075; current head `df7942c` un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive (now WebP gate is cleared, so promotion should be scheduled).
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84, #87 CLOSED. Issue #68 stays OPEN until codecs beaten.

- Mae, the Maintainer
