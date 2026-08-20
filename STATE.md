# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~04:39Z, maintainer event run 32332630329, triggered by owner `/oc maintainer` x2 on PR #93 after the Builder resolved the M3-B break, reverted to 9.5208 bpp / 138 tests pass, and escalated the JXL gap to a **structural architectural ceiling**). Decision: break the `continue` loop and dispatch `research` on PR #93 to design a fundamentally new base predictor/transform architecture (true wavelet/lifting OR learned/context-adaptive predictor). One-PR rule intact; orphan re-link remains fixed.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`. (#91 + #92 branches `opencode/lab-68-orphan-main-guard` intentionally left intact.)
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. Still deferred; schedule once JXL nears.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** PR #93 is the single canonical, open Obsidian PR (supersedes closed #83), branch `opencode/issue68-20260818070512`.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec).
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #93 (or issue #68 for factory/lab) - not on a new PR.

## CRITICAL INFRASTRUCTURE STATE (orphan-main guard MERGED; branch RE-LINKED & PR #93 OPEN)

- **PR #91 MERGED:** orphan-main guard (`c043b7e`, carries literal `Closes #68` commit token; #68 reopened same run).
- **PR #92 MERGED:** `main` = `d6b2894`. Determinism guard + "do not auto-close umbrella" rule + force-with-lease pin. Body `Refs #68`.
- **`main` = `d6b2894`** (healthy, 370 commits, clean descendant of prior main).
- **Branch `opencode/issue68-20260818070512` RE-LINKED** (current head `0c5336ea2663d2839ea57eb857c9dec88e9f6a24`, merge-base `d6b2894` non-empty). PR #93 is the single canonical Obsidian PR (`Refs #68`). ORPHAN PROBLEM RESOLVED.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub auto-closes #68 if the literal `Closes #68` token appears ANYWHERE. Future Builder/Architect/Lab commits MUST use `Refs #68` / `Refs to #68`. PR #93 body is correctly `Refs #68`.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian):** OPEN, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **Default shipped codec = 9.5208 bpp mean** (R10-B CFL). Beats PNG (13.05) + WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
- **R0-R11 codec shipped on PR #93:** Golomb-Rice, CMARC binary range coder (R4), context-tree weighted predictor (R9-B), R10 Squeeze + chroma-from-luma, R11 cross-band in-loop predictor, R11-D MA-tree-lite combined gradient+residual context (opt-in), R11-A cross-band `wLL` (reverted). R12-A (per-band weighted predictor) committed, proven moot (Squeeze never selected on photographic Kodak). 64-leaf weight-context deepening tried twice, both regressed, reverted - branch clean at 15 leaves / 9.5208 bpp / 138 tests pass.

## CURRENT BUILD STATE (structural architectural ceiling - research next)

- **Verdict (robust, 6 axes):** the +0.81 bpp JXL gap is a **STRUCTURAL ARCHITECTURAL CEILING** of the single-pixel CMARC pipeline with the near-optimal R9-B weighted predictor. Every tuning axis failed:
  1. R11-D combined gradient+residual MA context - wash.
  2. R11-A cross-band `wLL` in-loop predictor - wash + 45x slowdown (reverted).
  3. 64-leaf weight context (27->15 modulo collision) - regression (reverted).
  4. R12-A per-band weighted predictor - correct/non-regressive BUT moot (Squeeze rejected on photographic Kodak; `transforms::squeeze` is quincunx *subsampling*, not a wavelet, so HF bands carry ~as much entropy; Squeeze net-negative).
  5. 64-leaf weight context again (15->64, fully populated) - identical +0.0054 regression (per-leaf sample starvation, not empty bins) (reverted).
  6. CMARC backend itself - already `H(p)+epsilon` near-optimal.
- **Conclusion:** the residual-entropy floor is set by the **predictor's functional form**, not context fineness. Closing JXL needs a genuinely new base predictor/transform: a true wavelet/lifting transform with real energy compaction, OR a learned/context-adaptive per-pixel predictor whose functional form differs from single-pixel weighted least-squares R9-B. The on-branch R7/R8/R9 blueprints are all single-pixel weighted predictors already implemented - they are NOT the answer.
- **Last Builder session (run 565, completed 2026-08-20T04:38:26):** resolved M3-B break (root cause: `WC_LEAVES=64` widened `WeightedTree` selection into the `OBSIDIAN_M3_WP` seam which only corrects when `p == Weighted`), reverted to 15 leaves, restored exactly 9.5208 bpp, **138 tests pass**. Head `0c5336ea` is clean. Escalated with decision `maintainer`.

## In flight

- **`research` on PR #93 (DISPATCHED THIS run, 32332630329, head `0c5336ea`):** the Researcher designs a fundamentally new base predictor/transform architecture to break the JXL 8.71 ceiling. Expected pipeline: Researcher -> Architect (blueprint) -> Builder (implement + re-measure REAL Kodak effort-4). No `continue` loop until a real architectural change lands.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above (default 9.5208); lever now = a new architecture (research in flight).
- **Resume Builder via `continue`** - only AFTER the Researcher/Architect deliver a real architectural change to measure.
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once JXL nears).
- **Review staleness on #93:** head `0c5336ea` is clean (138 tests pass); fresh Reviewer + Tester gate required before any merge.
- **Commit-message hygiene:** never write literal `Closes #68` token in ANY commit message or PR body.

## Issues

- **#68 (Obsidian umbrella)** - OPEN, active fundamental goal, stays open until codecs beaten.
- **#52 / #89 / #90 / #91 / #92 infra** - #90 MERGED; #89 CLOSED; #52 related; #91 MERGED (guard); #92 MERGED (guard + umbrella rule + force-with-lease pin). Both branches kept.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule; board live.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError` in recent runs.
- **pages.yml:** green (deployed run 32332626801 at 04:38:39Z).
- **PR #93 checks:** opencode-pr-trigger SUCCESS on recent pushes; pages deploy SKIPPED (expected for PR preview), GitGuardian SUCCESS. No Reviewer/Tester run yet.

## Next steps

1. **Researcher `research` (in flight):** design a fundamentally new base predictor/transform architecture to beat JXL 8.71 (true wavelet/lifting OR learned/context-adaptive predictor). After findings, dispatch `architect` to blueprint it, then `continue`/`build` to implement + re-measure REAL Kodak effort-4. Loop only on real architectural change, not context tuning.
2. **After gates clear:** fresh Reviewer + Tester gate, then rebase-merge (`--no-delete-branch`) and close #68. NOT before.
3. **README / index.html promotion:** schedule once JXL nears / PR clears.

## Open questions

- **What new functional form clears the JXL 8.71 gap?** Now a Researcher question (run to follow). Six independent axes all point to the single-pixel weighted predictor being near-optimal within its class; the lever is a structurally different predictor/transform, not finer contexts.
- **Merge gate (owner override #2):** NOT met - default 9.5208 beats PNG + WebP but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, shares history with main).
- **Orphan-main break:** RESOLVED (merge-base `d6b2894` non-empty; PR #93 healthy).
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **pages.yml:** green.
- **Billing:** resolved (no `CreditsError`; `small_model` correctly pinned free).
- **Commit-message hygiene:** PR #93 body is correctly `Refs #68`; future commits/blueprints must avoid literal `Closes #68`.

- Mae, the Maintainer
