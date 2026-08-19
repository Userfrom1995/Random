# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~13:50Z, maintainer run 32260382145, owner `/oc maintainer` after the R9 Architect blueprint). **DECISIONS:** `continue` on PR #83 - resume the Builder to implement the R9 blueprint (spatial LZ77 2D-distance + color cache, then context-tree weighted predictor). No duplicate trigger (no Builder/Architect/Researcher in flight). R8-A confirmed inert at 9.7080 bpp (real Kodak effort-4). WebP/JPEG XL gates still unmet.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83. A fresh `/oc build this` does NOT override this - route to `continue` on the existing PR.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RE-OPENED - 4th recurrence, Factory-caused)

- **Mergeability (BROKEN):** `main` = `8f4c15b` (single orphan commit "factory: harden build loop against 60-min timeout work loss", no parent) - created by the Factory's own merged PR #88. Branch root = `75e2eaa` ("builder: rebuild Obsidian codec crate…", orphan, no parent) + commits -> head `eee867d` (R9 Architect blueprint). `git merge-base origin/main <branch>` is EMPTY. GitHub reports `CONFLICTING`; `gh pr merge --rebase` would fail. `--rebase` is impossible until the Factory re-links.
- **Root cause of the recurrence:** the merge-to-`main` step (and the Builder's "rebuild onto main" step) force-writes an orphan root instead of preserving history, and the opencode App cannot push `main` to fix it (no `workflows` permission + branch protection rejected the earlier direct push).
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is measurable reproducibly.

## SYSTEMIC INFRASTRUCTURE BLOCKER (since 2026-08-19 ~12:40Z)

- **The opencode GitHub App has NO `workflows` permission.** Every pipeline agent (Factory/Builder/Fixer) pushes using the App token, so any edit to `.github/workflows/*.yml` is rejected ("refusing to allow a GitHub App to create or update workflow ... without `workflows` permission"). Confirmed on PR #90's Factory fix run 32253718673. Consequence: **the bot can NEVER modify workflow files.** The Reviewer's Finding #1 on PR #90 (orphan-guard hardening) therefore cannot be applied by the Factory. Owner must either grant `workflows: write` to the App, or apply workflow edits manually. This also makes the standing "Maintainer may only edit `.github/workflows/*.yml` for model switching" rule moot.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `eee867d`):
  - **DEFAULT shipped codec = CMARC auto-selected best = 9.7080 bpp mean** (R8-A committed; real Kodak effort-4, reproducible). Beats JPEG-LS (9.71); PNG 13.05 MET; **WebP 9.61 MISSED by ~0.098 bpp**; **JPEG XL 8.71 MISSED by ~0.998 bpp**. Bit-exact.
  - **Empirical dead-ends (root cause shared = entropy-context fragmentation / saturation of the single-pixel predictor bank under the CMARC context budget):**
    - R3-A residual-context INERT (model starvation under ~365x context blowup).
    - R6-B color cache DEAD END (inert on photographic residuals).
    - R7-A per-context weighted predictor REGRESSED to 9.8323 bpp (signaled `17+j` codebook indices + codebook expansion -> fragmentation). Reverted to 9.7094 baseline.
    - R8-A signaling-free adaptive weighted predictor INERT (+0.0014 bpp; the Architect's prescribed WebP lever did not move the photographic needle).
  - **KEY DIAGNOSIS (empirical, settled):** the codec is pinned at the **JPEG-LS floor (~9.71)**. The entropy backend (CMARC, R4-corrected LZMA carryless range coder verified at `H(p)+epsilon`; R5 Rice quotient) is NOT the bottleneck. Remaining gaps are **long-range + context-tree redundancy + predictor/transform**, per the R9 Researcher diagnosis: stop tuning the causal predictor; add spatial LZ77 (WebP lever) and a context-tree weighted predictor (JPEG XL lever).
- **CMARC lineage (R1 -> R5) built; entropy core correct (CACM87 / LZMA range coder):**
  - **R4 coder = canonical LZMA carryless binary arithmetic coder** - proven correct; efficiency gate passes (`cmarc_efficiency_vs_epsilon` ratio < 1.10).
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` learns the geometric quotient like JPEG-LS QM; delivered the 9.7080 headline (R8-A re-implemented cleanly on top).
  - All CMARC variants ship behind the never-expand safety net, which now ALSO engages by default.

## In flight

- **PR #83 (Obsidian, branch `opencode/issue68-20260818070512`, head `eee867d`):** R9 research + Architect blueprint DELIVERED. **This run fires `continue`** to implement R9-A (spatial LZ77: `MIN_MATCH=2`, 2D distance model, color-cache competition in the mode-3 match layer) then R9-B (context-tree `WeightedTree` predictor, <=15 leaves, O(1) per-plane model bytes). One-PR rule intact. Orphan-main break + unmet gates still apply. `mergeable: CONFLICTING`.
- **PR #90 (Factory infra PR, head `opencode/factory-68-build-loop-duplicate-guard`):** duplicate-Builder `concurrency` guard + orphan guard hardening for the #68 build loop. Reviewed: Finding #2 (Closes #68) already fixed in body; **Finding #1 (orphan guard at opencode.yml:421-431) BLOCKED** - bot cannot push workflow file (missing `workflows` permission). PR stays OPEN, not mergeable in good standing, awaiting owner action.

## PENDING (deferred)

- **Clear WebP 9.61 gate:** default 9.7080 is ~0.098 above. R9-A (spatial LZ77 2D distance + color cache) is the active attempt; high confidence per WebP's published LZ77 margin.
- **Clear JPEG XL 8.71 gate:** ~1.0 bpp above; the hard long pole - needs R9-B (context-tree weighted predictor) and possibly R9-C (palette + Squeeze transform).
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near).
- **PR #90 workflow fix dependency:** Finding #1 cannot land until the owner grants `workflows` permission to the App OR applies the patch manually.
- **Orphan-main re-link:** blocked on the App's inability to push `main`; unfixed recurrence root cause.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#90 (Factory infra PR for #68 build loop)** - OPEN; blocked on `workflows` permission for the orphan-guard fix (Finding #1). Finding #2 already resolved.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `eee867d`, **rebase-unmergeable** (orphan-main break re-opened, 4th recurrence, Factory-caused; API CONFLICTING). Default 9.7080 (PNG + JPEG-LS met; WebP/JXL unmet). R7-A reverted (regressed to 9.8323); R8-A inert (+0.0014). R9 blueprint delivered; Builder resumes via `continue`.
- **PR #90:** OPEN, review blocking finding #1 unapplied (bot permission wall), Finding #2 resolved (no `Closes #68`).

## Next steps

1. **PR #83 `continue` (this run):** Builder implements R9-A (spatial LZ77: `MIN_MATCH=2`, 2D distance bins, color-cache competition in mode-3) -> re-measure REAL Kodak effort-4; assert never-expand net keeps it non-regressive; target <= 9.61 (WebP). Then R9-B (context-tree `WeightedTree`, <=15 leaves, O(1) model bytes) -> re-measure; target <= 8.71 (JPEG XL). Then R9-C only if needed.
2. **After R9 build:** fresh `/oc review` + `/oc test` on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
3. **PR #90 (owner action):** grant `workflows: write` to the opencode App OR apply the orphan-guard patch manually + merge. Do not merge until Finding #1 resolved.
4. **Factory re-links `main` + fixes the orphan-root recurrence** (once the permission/root-cause allows). Rebase branch onto `origin/main`. Non-blocking now (gate unmet) but must be fixed before merge.
5. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
6. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current once gates near.

## Open questions

- **SYSTEMIC `workflows` permission gap:** no pipeline agent can edit workflow files; blocks PR #90's Finding #1 and all future infra changes. Owner must grant permission or do manual merges.
- **Can R9-A spatial LZ77 clear the +0.098 WebP gap?** Research/Architect: high confidence (WebP's published Kodak LZ77 margin ~0.2-0.5 bpp comfortably covers it; MIN_MATCH=2 + 2D distance + cache address the prior dormant-match failure modes). The never-expand net guarantees no regression.
- **Can R9-B context-tree weighted predictor clear the +0.998 JPEG XL gap?** Per the Researcher, likely needs R9-A + R9-B (and possibly R9-C palette/Squeeze). True JPEG XL WP/TM-WP at fine granularity, O(1) model bytes, no R7-A blowup.
- **Merge gate (owner override #2):** NOT met - default 9.7080 bpp > WebP 9.61 > JXL 8.71. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **Orphan-main break (4th recurrence, Factory-caused):** `main` = `8f4c15b` orphan; branch = `75e2eaa` orphan -> `eee867d`. `git merge-base` empty. Factory must re-link AND fix the recurrence root cause; today the App cannot push main. Non-blocking now (gate unmet) but must be fixed before merge.
- **Review staleness:** last approve at head ~96a6075; current head `eee867d` un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84, #87 CLOSED. Issue #68 stays OPEN until codecs beaten.

- Mae, the Maintainer
