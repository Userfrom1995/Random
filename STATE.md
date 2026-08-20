# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~04:27Z, maintainer event run 32331889345, triggered by owner `/oc maintainer` x3 on PR #93 after the Builder's R9-B deepening session committed `bd88b145` with 2 broken M3-B tests). Decision: dispatch `continue` on PR #93 so the Builder resolves the test breakage and re-measures REAL Kodak toward the JXL 8.71 gate. One-PR rule intact; orphan re-link remains fixed.

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
- **Branch `opencode/issue68-20260818070512` RE-LINKED** (current head `bd88b145`, merge-base `d6b2894` non-empty). PR #93 is the single canonical Obsidian PR (`Refs #68`). ORPHAN PROBLEM RESOLVED.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub auto-closes #68 if the literal `Closes #68` token appears ANYWHERE. Future Builder/Architect/Lab commits MUST use `Refs #68` / `Refs to #68`. PR #93 body is correctly `Refs #68`.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian):** OPEN, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **Default shipped codec = 9.5208 bpp mean** (R10-B CFL). Beats PNG (13.05) + WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
- **R0-R11 codec shipped on PR #93:** Golomb-Rice, CMARC binary range coder (R4), context-tree weighted predictor (R9-B), R10 Squeeze + chroma-from-luma, R11 cross-band in-loop predictor, R11-D MA-tree-lite combined gradient+residual context (opt-in), R11-A cross-band `wLL` (reverted). R12-A (per-band weighted predictor) committed, proven moot (Squeeze never selected on photographic Kodak).

## CURRENT BUILD STATE (base-predictor pivot)

- **R12-A premise refuted (robust, 4 axes):** the +0.81 bpp JXL gap is the **BASE PREDICTOR** (LOCO-I GAP's residual entropy near-optimal), NOT context refinement (R3-A/R11-D/64-leaf) and NOT Squeeze-gated decorrelation (R12-A/R12-B). `transforms::squeeze` is a quincunx *subsampling*, not a wavelet, so HF bands carry ~as much entropy as the original and Squeeze is net-negative and correctly rejected by the never-expand net.
- **Current experiment (in flight, head `bd88b145`):** deeper base-predictor weight context - `WC_LEAVES` 15→64 in `predict.rs` with a 4-tier-per-gradient `weight_context` so every leaf is populated (the earlier 64-leaf regression left most bins empty). Status: the Builder's session (run 564, 2026-08-20T04:26:35) committed this as `bd88b14 "Deepened predictor; broke 2 M3-B tests, investigating."` - it **broke two M3-B tests** (`m3_wp_improves_over_v1`, `m3_wp_self_correcting_roundtrip`) that pass on the stashed baseline, and is investigating the interaction before compiling a final real-Kodak measurement. The branch currently has 2 failing lib tests; no merge risk yet (JXL gate unmet regardless).

## In flight

- **`continue` on PR #93 (DISPATCHED THIS run, 32331889345):** the Builder resolves the M3-B test breakage from `bd88b145`, then re-measures REAL Kodak effort-4 against the JXL 8.71 gate. If the 64-leaf deepening regresses or is neutral (consistent with the 5-axis context-exhaustion conclusion), the Builder reverts and the verdict strengthens: a fundamentally different base predictor functional form is needed (true wavelet/lifting transform with real energy compaction, or a genuinely adaptive/learned per-context predictor - R7/R8/R9 blueprints are the design basis). Loop via `continue` until all three gates clear.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above (default 9.5208); next lever = a genuinely better BASE predictor/transform (in flight via `continue`).
- **Resume Builder (base predictor) via `continue`** - dispatched THIS run (head `bd88b145`).
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once JXL nears).
- **Review staleness on #93:** head `bd88b145` is builder self-pushed; fresh Reviewer + Tester gate required before any merge.
- **Commit-message hygiene:** never write literal `Closes #68` token in ANY commit message or PR body.

## Issues

- **#68 (Obsidian umbrella)** - OPEN, active fundamental goal, stays open until codecs beaten.
- **#52 / #89 / #90 / #91 / #92 infra** - #90 MERGED; #89 CLOSED; #52 related; #91 MERGED (guard); #92 MERGED (guard + umbrella rule + force-with-lease pin). Both branches kept.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule; board live.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError` in recent runs.
- **pages.yml:** green; deploying (run 566 in progress at 04:26:47Z).
- **PR #93 checks:** opencode-pr-trigger SUCCESS on recent pushes; pages deploy SKIPPED (expected for PR preview), GitGuardian SUCCESS. No Reviewer/Tester run yet.

## Next steps

1. **Builder `continue` (in flight):** resolve M3-B breakage on `bd88b145`, re-measure REAL Kodak effort-4 against JXL 8.71. If 64-leaf deepening is neutral/regressive, revert and pivot to a fundamentally different base predictor (true wavelet/lifting transform OR adaptive/learned per-context weighted predictor per R7/R8/R9). Loop until all three gates clear.
2. **After gates clear:** fresh Reviewer + Tester gate, then rebase-merge (`--no-delete-branch`) and close #68. NOT before.
3. **README / index.html promotion:** schedule once JXL nears / PR clears.

## Open questions

- **Will the deeper base-predictor weight context (64-leaf, fully populated) clear the JXL gap?** Pending the Builder's measurement on `bd88b145`. Five independent axes (R11-D, R11-A, 64-leaf 27->15 modulo, R12-A Squeeze rejection, now the 15->64 WC_LEAVES deepening) all point to context granularity being exhausted; a genuinely different functional form is the only seen lever.
- **Merge gate (owner override #2):** NOT met - default 9.5208 beats PNG + WebP but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, shares history with main).
- **Orphan-main break:** RESOLVED (merge-base `d6b2894` non-empty; PR #93 healthy).
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **pages.yml:** green; re-deploying (run 566 in progress).
- **Billing:** resolved (no `CreditsError`; `small_model` correctly pinned free).
- **Commit-message hygiene:** PR #93 body is correctly `Refs #68`; future commits/blueprints must avoid literal `Closes #68`.

- Mae, the Maintainer
