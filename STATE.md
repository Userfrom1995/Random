# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~19:52Z, maintainer run 32179002001, PR #83 trigger). **DECISIONS:** `[{"action":"architect","pr":83},{"action":"factory","issue":68}]` - ESCALATION FIRED after the THIRD consecutive R4 failure: the Builder's `continue` (run 32177832808) pushed `ad6efa6` ("Found CMARC bit-sync bug; need byte-oriented coder") - WNC coder still ~2x over Shannon, 32x32 CARC bug, R4 NOT landed. Architect must deliver a CONCRETE correct arithmetic-coder reference (not abstract); Factory raises the opencode build `timeout-minutes` + hardens `continue-on-error` + enforces the one-PR rule (close redundant codec PR #84). No `continue` fired (Builder must wait for the reference). No merge (gates unmet).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: this is currently NOT satisfied (see Open questions) - flagged for a Builder/Factory pass, not a direct `main` edit by Mae.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch. Redundant codec-rebase PR #84 was opened by the Factory earlier and REJECTED by the owner; it must be CLOSED.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break STILL OPEN; rebase MANY runs overdue)

- **Mergeability (BROKEN):** PR #83 OPEN, head `ad6efa6b7cca57bace9758254ee79958ce962a82` (R4 WIP: WNC ~2x + bit-sync bug, needs byte-oriented coder), `mergeable: CONFLICTING`, **no common ancestor with `main`** - `git merge-base origin/main opencode/issue68-20260818070512` returns EMPTY; `main` (`e4e3392`, single orphan commit) is NOT an ancestor of the branch. This blocks the eventual `--rebase` merge.
- **OWNER-MANDATED REPAIR (16:51Z, NOW MANY RUNS OVERDUE):** the Builder must rebase `opencode/issue68-20260818070512` onto `origin/main` (replay all codec commits on top of `e4e3392`, preserving every commit's work) and force-push the SAME branch - NO new PR. The Factory is deliberately NOT used for the rebase (its prior squash-rebase opened redundant PR #84 and re-orphaned `main`, violating the one-PR rule). This is deferred until after the coder is fixed; non-blocking now because the performance gate is unmet.
- **Measurement blocker (RESOLVED):** `obsidian/benchmarks/data/kodak/` PPMs ARE PRESENT in the repo (kodim01..24.ppm). `run_kak.sh` self-provisions + verifies against `kodak.sha256`. R4 re-measurement on REAL Kodak is possible. Earlier "10.0906 bpp" was GR-fallback only (CMARC explodes until the coder is fixed).

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `ad6efa6`). **ROOT-CAUSE FIX earlier this cycle:** `ppm.rs` decoded the interleaved P6/P5 raster as planar, scrambling R/G/B; fixed, codec bit-exact. Corrected real-Kodak baseline (effort 4) = **10.16 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.45; JPEG XL 8.71 MISSED by 1.45).
- **CMARC stack (R1 -> R2.4) + R3 (R3-A residual-context, R3-B neutral-prior Rice, R3-C) built, all OFF by default.** On real Kodak CMARC itself EXPLODES (21-27 bpp forced) - the never-expand net falls back to GR, so every quoted "best" number (10.09, 10.16) was GR all along. CMARC has never beaten GR on real Kodak.
- **ROOT-CAUSE DIAGNOSIS (CONVERGED, R4):** The shared 16-bit binary range coder (`RangeEnc`/`RangeDec`/`BinEnc`/`BinDec`) is **lossless but does NOT compress** - a pass-through bit buffer for any skewed probability (empirical probe: p=0.1 -> 1.745 bps vs 0.469 Shannon = 3.72x; p=0.01 -> 3.348 vs 0.081 = 41x). This is the real defect behind every CMARC/R3 "regression": context/quotient/residual tuning is futile because the coder ignores the learned probability. GR is unaffected (separate `GrState` Golomb-Rice coder).
- **R4 blueprint (Architect, commit `33bd48f`):** a correct arithmetic coder + MANDATORY efficiency gate `measured_bps / shannon_bps < 1.10` for `p in {0.01,0.1,0.5,0.9,0.99}` + Laplacian - fails the build until the coder is correct.
- **R4 IMPLEMENTATION STATUS: STILL FAILING (THIRD attempt).** The Builder: (1) tried a carryless LZMA `ShiftLow`/`range_coder` (abandoned, byte-count bug); (2) swapped in a WNC (Witten-Neal-Cleary) arithmetic coder with bit I/O (commit `5dac45f`, roundtrip lossless) but efficiency still ~1.57-2.05x over Shannon - gate NOT met; (3) hit a CMARC bit-sync bug + 32x32 CARC integration bug (commit `ad6efa6`, "need byte-oriented coder"). The abstract blueprint is insufficient; a CONCRETE reference is now mandated (see In flight).

## In flight

- **Architect (`/oc architect` on PR #83, this run's decision):** deliver a CONCRETE, correct, byte-oriented binary arithmetic/range coder reference implementation (working Rust code) with exact subrange split, renormalization, carry handling, and the MANDATORY `<1.10x` efficiency-gate test. Not an abstract blueprint. Returns `continue` for the Builder on the same branch.
- **Factory (`/oc factory` on #68, this run's decision):** (a) raise `timeout-minutes` on the opencode build step (opencode.yml, currently 60); (b) harden `continue-on-error` so a masked failure fails the run; (c) enforce one-PR rule and CLOSE redundant codec-rebase PR #84.
- **Builder `continue` (deferred):** resumes ONLY after the Architect's concrete reference lands - then finishes R4 (correct coder <1.10x + 32x32 CARC bug fix + efficiency-gate test + green `cargo test -p obsidian_core` + clean commit), then re-measures R1/R2/R3 on real Kodak, then does the owner-mandated rebase onto `main`.

## PENDING (deferred to a quiet run)

- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Needs a Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Branch rebase onto `main` (owner 16:51Z, MANY runs overdue):** deferred until after R4 coder fixed; then Builder force-pushes the SAME branch, verify MERGEABLE.
- **Fix the malformed `binenc_vs_rangeenc_skew` test** (RNG bug, false failure) - superseded by the R4 mandatory efficiency gate; low priority.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `main` workflow agent steps (factory/review/test) pin `opencode/hy3-free`. `opencode.json` `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). main currently = `e4e3392 factory: upgrade reviewer/tester/factory models from mimo-v2.5-free to hy3-free` - the earlier `CreditsError` billing outage is RESOLVED.
- **Mergeability:** PR #83 OPEN, head `ad6efa6`, `mergeable: CONFLICTING` (NO common ancestor with main - orphan break still open; rebase deferred to after R4 coder fix).
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Architect delivers concrete correct coder reference (this run's `architect`):** working byte-oriented arithmetic coder + mandatory `<1.10x` efficiency gate, committed on the single branch.
2. **Builder `continue` (after reference lands):** finish R4 (coder <1.10x + 32x32 CARC fix + efficiency-gate test + green tests + clean commit); re-measure R1/R2/R3 on REAL Kodak effort-4 (target < 9.71 JPEG-LS, ideally < 9.61 WebP, then < 8.71 JPEG XL); then rebase branch onto `origin/main` + force-push SAME branch (clear CONFLICTING).
3. **Factory (this run's `factory`):** raise build timeout, harden `continue-on-error`, enforce one-PR rule, close redundant PR #84.
4. **After a reproducible real-Kodak number below all three gates:** branch already rebase-mergeable, then rebase-merge (`--no-delete-branch` per owner directive), close #68.
5. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.

## Open questions

- **Will the Architect's CONCRETE reference coder let the Builder land R4 (<1.10x efficiency + 32x32 CARC fixed + green tests)?** The architecture is sound; the failures were purely implementing an abstract spec. A verified reference is the right escalation.
- **Will a correctly-compressing CMARC reach JPEG-LS-class (9.71) or better on REAL Kodak?** Predictor is sound (same LOCO-I GAP); broken coder was the proven bottleneck (3.7-41x over Shannon). Awaits R4 completion + re-measurement.
- **Will the branch rebase onto `main` finally succeed (preserving all codec work) and make PR #83 MERGEABLE without a new PR?** Owner-requested 16:51Z, MANY runs overdue. Verify next survey (`merge-base` non-empty, `gh pr view 83` MERGEABLE, no new issue68 codec PR, #84 closed).
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84 (redundant codec-rebase) must be closed by the Factory; no new issue68 codec PR opened.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.

- Mae, the Maintainer
