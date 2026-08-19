# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~14:17Z, maintainer run 32263157758, after the R9-A build report). **DECISIONS:** `continue` on PR #83 - resume the Builder to implement R9-B (context-tree `WeightedTree` predictor, the JPEG XL lever; also targets WebP). No duplicate trigger (no Builder/Architect/Researcher in flight). R9-A confirmed dormant on photographic Kodak (0/24 images select LZ); codec plateaus at the ~9.71 bpp architectural ceiling. WebP/JPEG XL gates still unmet.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83. A fresh `/oc build this` does NOT override this - route to `continue` on the existing PR.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break - recurrence still live, Factory-caused)

- **Mergeability (BROKEN):** `main` = `8f4c15b` (single orphan commit, no parent). Branch root = `75e2eaa` ("builder: rebuild Obsidian codec crate...", orphan) + commits -> head `01c286d` (R9-A). `git merge-base origin/main <branch>` is EMPTY. GitHub reports `CONFLICTING`; `gh pr merge --rebase` would fail. `--rebase` is impossible until the Factory re-links.
- **Root cause of the recurrence:** the merge-to-`main` step (and the Builder's "rebuild onto main" step) force-writes an orphan root instead of preserving history, and the opencode App cannot push `main` to fix it (no `workflows` permission + branch protection rejected the earlier direct push).
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is measurable reproducibly.

## SYSTEMIC INFRASTRUCTURE BLOCKER (since 2026-08-19 ~12:40Z)

- **The opencode GitHub App has NO `workflows` permission.** Every pipeline agent (Factory/Builder/Fixer) pushes using the App token, so any edit to `.github/workflows/*.yml` is rejected ("refusing to allow a GitHub App to create or update workflow ... without `workflows` permission"). Confirmed on PR #90's Factory fix run 32253718673. Consequence: **the bot can NEVER modify workflow files.** The Reviewer's Finding #1 on PR #90 (orphan-guard hardening) therefore cannot be applied by the Factory. Owner must either grant `workflows: write` to the App, or apply workflow edits manually. This also makes the standing "Maintainer may only edit `.github/workflows/*.yml` for model switching" rule moot.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `01c286d`):
  - **DEFAULT shipped codec = CMARC auto-selected best = 9.7080 bpp mean** (R8-A committed; real Kodak effort-4, reproducible). Beats JPEG-LS (9.71); PNG 13.05 MET; **WebP 9.61 MISSED by ~0.098 bpp**; **JPEG XL 8.71 MISSED by ~0.998 bpp**. Bit-exact.
  - **Empirical dead-ends (root cause shared = entropy-context fragmentation / saturation of the single-pixel predictor bank under the CMARC context budget):**
    - R3-A residual-context INERT (model starvation under ~365x context blowup).
    - R6-B color cache DEAD END (inert on photographic residuals).
    - R7-A per-context weighted predictor REGRESSED to 9.8323 bpp (signaled `17+j` codebook indices + codebook expansion -> fragmentation). Reverted to 9.7094 baseline.
    - R8-A signaling-free adaptive weighted predictor INERT (+0.0014 bpp; the Architect's prescribed WebP lever did not move the photographic needle).
    - R9-A spatial LZ77 (2D-distance, MIN_MATCH=2) DORMANT on photographic Kodak (never-expand net selects CARC_LZ on 0/24 images; the strong predictor bank removes the repeats LZ would copy). 9.708 bpp ceiling; live regression-proof lever for repetitive content only.
  - **KEY DIAGNOSIS (empirical, settled):** the codec is pinned at the **JPEG-LS floor (~9.71)**. The entropy backend (CMARC, R4-corrected LZMA carryless range coder verified at `H(p)+epsilon`; R5 Rice quotient) is NOT the bottleneck. Remaining gaps are **long-range + context-tree redundancy + predictor/transform**, per the R9 Researcher diagnosis: stop tuning the causal predictor; add spatial LZ77 (WebP lever, R9-A - DORMANT) and a context-tree weighted predictor (JPEG XL lever, R9-B - not yet attempted).
- **CMARC lineage (R1 -> R5) built; entropy core correct (CACM87 / LZMA range coder):**
  - **R4 coder = canonical LZMA carryless binary arithmetic coder** - proven correct; efficiency gate passes (`cmarc_efficiency_vs_epsilon` ratio < 1.10).
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` learns the geometric quotient like JPEG-LS QM; delivered the 9.7080 headline (R8-A re-implemented cleanly on top).
  - All CMARC variants ship behind the never-expand safety net, which now ALSO engages by default.

## In flight

- **PR #83 (Obsidian, branch `opencode/issue68-20260818070512`, head `01c286d`):** R9-A (spatial LZ77 2D-distance) DONE and measured dormant (9.708 bpp, 0/24 LZ). **This run fires `continue`** to implement R9-B (context-tree `WeightedTree` predictor, K<=15 leaves, O(1) per-plane model bytes) then re-measure REAL Kodak. One-PR rule intact. Orphan-main break + unmet gates still apply. `mergeable: CONFLICTING`.
- **PR #90 (Factory infra PR, head `opencode/factory-68-build-loop-duplicate-guard`):** duplicate-Builder `concurrency` guard + orphan guard hardening for the #68 build loop. Reviewed: Finding #2 (Closes #68) already fixed in body; **Finding #1 (orphan guard at opencode.yml:421-431) BLOCKED** - bot cannot push workflow file (missing `workflows` permission). PR stays OPEN, awaiting owner action.

## PENDING (deferred)

- **Clear WebP 9.61 gate:** default 9.7080 is ~0.098 above. R9-A (spatial LZ77 2D distance) is DORMANT on photographic Kodak (predictor bank removed repeats). R9-B (context-tree weighted predictor) is the next attempt and has never been tried; expected to help JPEG XL primarily.
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
- **PR #83:** OPEN, head `01c286d`, **rebase-unmergeable** (orphan-main break, recurrence, Factory-caused; API CONFLICTING). Default 9.7080 (PNG + JPEG-LS met; WebP/JXL unmet). R9-A dormant (0/24 LZ). R9-B is the next blueprinted step (never attempted).
- **PR #90:** OPEN, review blocking finding #1 unapplied (bot permission wall), Finding #2 resolved (no `Closes #68`).

## Next steps

1. **PR #83 `continue` (this run):** Builder implements R9-B (context-tree `WeightedTree` predictor, K<=15 leaves, O(1) per-plane model bytes), re-measures REAL Kodak effort-4, asserts never-expand net keeps it non-regressive; target <= 8.71 (JPEG XL) and <= 9.61 (WebP). Then R9-C (palette + Squeeze) only if still short.
2. **After R9-B/C build:** fresh `/oc review` + `/oc test` on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
3. **PR #90 (owner action):** grant `workflows: write` to the opencode App OR apply the orphan-guard patch manually + merge. Do not merge until Finding #1 resolved.
4. **Factory re-links `main` + fixes the orphan-root recurrence** (once the permission/root-cause allows). Rebase branch onto `origin/main`. Non-blocking now (gate unmet) but must be fixed before merge.
5. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
6. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current once gates near.

## Open questions

- **SYSTEMIC `workflows` permission gap:** no pipeline agent can edit workflow files; blocks PR #90's Finding #1 and all future infra changes. Owner must grant permission or do manual merges.
- **Can R9-B context-tree weighted predictor clear the +0.998 JPEG XL gap (and +0.098 WebP)?** It is a fundamentally different mechanism from R8-A (single formula) and R7-A (per-coarse-context codebook): per-fine-weight-context LS weights (JPEG XL WP/TM-WP) signaled O(1) per-plane. Empirical verdict pending this `continue`. If also inert, R9-C (palette + Squeeze) is the last blueprinted lever, then escalate to Researcher and/or surface the owner's three-gate override for a decision.
- **Merge gate (owner override #2):** NOT met - default 9.7080 bpp > WebP 9.61 > JXL 8.71. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **Orphan-main break (recurrence):** `main` = `8f4c15b` orphan; branch = `75e2eaa` orphan -> `01c286d`. `git merge-base` empty. Factory must re-link AND fix the recurrence root cause; today the App cannot push main. Non-blocking now (gate unmet) but must be fixed before merge.
- **Review staleness:** last approve at head ~96a6075; current head `01c286d` un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84, #87 CLOSED. Issue #68 stays OPEN until codecs beaten.

- Mae, the Maintainer
