# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~16:51Z, maintainer run 32162519021, triggered by owner `/oc maintainer` on PR #83 after the Architect delivered the R4 blueprint). **DECISIONS:** `[]` (no trigger). The R4 blueprint (root cause: binary range coder is a pass-through bit buffer for p≠0.5, 3.7-41x over Shannon) is delivered at commit `33bd48f`; the Builder is already implementing it via the in-flight `continue` run `32160255732` (decided by run 32159973855 at 16:25Z). No duplicate `continue` fired. No merge (gates unmet). One PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: this is currently NOT satisfied (see Open questions) - flagged for a Builder/Factory pass, not a direct `main` edit by Mae.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break STILL OPEN)

- **Mergeability (BROKEN):** PR #83 OPEN, head `33bd48f0...` (R4 blueprint), `mergeable: CONFLICTING`, **no common ancestor with `main`** - `git merge-base origin/main opencode/issue68-20260818070512` returns EMPTY; `main` (`e4e3392`, single orphan commit) is NOT an ancestor of the branch. This blocks the eventual `--rebase` merge and MUST be repaired (Builder rebases `opencode/issue68-20260818070512` onto `origin/main` and force-pushes the SAME branch, no new PR). Deferred because the gate is unmet.
- **Measurement blocker (root cause fully understood):**
  - `obsidian/benchmarks/data/kodak/` is **git-ignored by design** (only `kodak.sha256` tracked). PPMs are fetched+normalized at benchmark time and verified against `kodak.sha256`. The Builder owns reproduction via `run_kodak.sh --provision` (self-provisioning + fail-fast sha256 verify landed earlier).
  - **Open risk:** earlier Builder runs could not reach a no-auth Kodak mirror (Kaggle needs a token; public mirrors 404/HTML), so even with the harness, real-Kodak reproduction in CI is uncertain. The Builder must report cleanly if data is unreachable - never fake numbers. The R4 mandatory efficiency gate, however, is a self-contained unit test that needs NO Kodak, so R4 correctness is verifiable now.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `33bd48f0`). **ROOT-CAUSE FIX earlier this cycle:** `ppm.rs` decoded the interleaved P6/P5 raster as planar, scrambling R/G/B; fixed, codec bit-exact. Corrected real-Kodak baseline (effort 4) = **10.16 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.45; JPEG XL 8.71 MISSED by 1.45).
- **CMARC stack (R1 -> R2.4) + R3 (R3-A residual-context, R3-B neutral-prior Rice, R3-C) built, all OFF by default.** On real Kodak CMARC itself EXPLODES (21-27 bpp forced) - the never-expand net falls back to GR, so every quoted "best" number (10.09, 10.16) was GR all along. CMARC has never beaten GR on real Kodak.
- **ROOT-CAUSE DIAGNOSIS (now CONVERGED, R4):** The shared 16-bit binary range coder (`RangeEnc`/`RangeDec`/`BinEnc`/`BinDec`) is **lossless but does NOT compress** - it is a pass-through bit buffer for any skewed probability (empirical probe: p=0.1 -> 1.745 bps vs 0.469 Shannon = 3.72x; p=0.01 -> 3.348 vs 0.081 = 41x). This is the real defect behind every CMARC/R3 "regression": context/quotient/residual tuning is futile because the coder ignores the learned probability. GR is unaffected (separate `GrState` Golomb-Rice coder). The Researcher's "models fail to adapt" reading (commit `f506050`) was a mis-attribution; the coder itself is the defect.
- **R4 blueprint (Architect, commit `33bd48f`, 16:22Z):** Replace the four broken binary coders with a **correct carryless LZMA range coder** (32-bit `range`, 64-bit `low` accumulator with `ShiftLow` carry cache, `PRECISION=12`/`BIN_TOTAL=4096`, preserving the `BinModel { p: u16 }` interface and `put`/`get` signatures). **MANDATORY efficiency gate:** `measured_bps / shannon_bps < 1.10` for `p in {0.01,0.1,0.5,0.9,0.99}` + Laplacian - fails the build until the coder is correct (round-trip tests cannot catch a lossless-but-non-compressing coder). Build order: R4 in isolation -> re-measure R1/R2 -> re-measure R3 on REAL Kodak.

## In flight

- **Builder `continue` (run `32160255732`, in_progress since 16:25:55Z):** implements R4 - replace the broken binary range coder with the correct carryless LZMA coder, land the mandatory efficiency gate (`measured/shannon < 1.10`), confirm `cargo test -p obsidian_core` green, then re-measure R1/R2/R3 on REAL Kodak effort-4 against all three gates. Reports honestly if PPMs are unreachable (never fake). Triggered by prior maintainer decision `continue #83` (run 32159973855, 16:25Z).
- **General-mode opencode run `32162519190` (pending, 16:51:24Z, event issue_comment):** a sibling run spawned by the owner's `/oc maintainer` trigger; routes to general mode (NOT a Builder `continue`), so it is not a competing implementation run.

## PENDING (deferred to a quiet run)

- **Orphan-main repair:** Builder must rebase `opencode/issue68-20260818070512` onto `origin/main` and force-push the SAME branch (no new PR) so PR #83 becomes rebase-mergeable. Deferred (gate unmet); NOT re-dispatching Factory this run to honor the owner's "stop opening new PRs" directive.
- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Needs a Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Factory hardening (one-PR rule):** dispatch the Factory Engineer to harden the workflow/agent so it NEVER opens a new PR for an issue that already has an open Obsidian/codec PR; it must reuse/push to the existing branch. Deferred (owner said stop opening new PRs).
- **Fix the malformed `binenc_vs_rangeenc_skew` test** (RNG bug, false failure) - superseded by the R4 mandatory efficiency gate; low priority.
- **opencode.yml `continue-on-error` hardening:** the research job's `continue-on-error: true` masked a silent 13s failure. Consider a post-step guard so a missing decision.json fails the run - Factory task, lower priority than the coder bug.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `main` workflow agent steps (factory/review/test) pin `opencode/hy3-free`. `opencode.json` `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). main currently = `e4e3392 factory: upgrade reviewer/tester/factory models from mimo-v2.5-free to hy3-free`.
- **Mergeability:** PR #83 OPEN, head `33bd48f0`, `mergeable: CONFLICTING` (NO common ancestor with main - orphan break still open; must be repaired before `--rebase` merge is possible).
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Builder implements R4 (in flight via run `32160255732`):** replace broken binary range coder with correct carryless LZMA coder; land mandatory efficiency gate (`measured/shannon < 1.10`); green `cargo test -p obsidian_core`.
2. **Re-measure R1/R2 on REAL Kodak** (effort 4) once `data/kodak` is durably available - now that the coder actually compresses, CMARC should beat GR; expect < 9.71 (JPEG-LS) and likely < 9.61 (WebP).
3. **Re-measure R3 residual-context** on the now-correct coder (earlier "regression" was a coder artifact).
4. **After a reproducible real-Kodak number below all three gates:** Builder repairs orphan-main (rebase+force-push), then rebase-merge (branch preserved per owner directive), close #68.
5. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.

## Open questions

- **Will the corrected carryless range coder let CMARC reach JPEG-LS-class (9.71) or better on real Kodak?** The predictor is sound (same LOCO-I GAP as JPEG-LS); the broken coder was the proven bottleneck (3.7-41x over Shannon). R4 removes that. Awaits the Builder's re-measurement.
- **Can the Builder reproduce the exact Kodak PPMs in CI?** Network + toolchain needed; public mirrors returned 404/HTML earlier, Kaggle needs a token. If unreachable, report the synthetic-proxy number honestly and flag the gate as unmeasurable - never fake data. The R4 efficiency gate itself needs no Kodak.
- **Orphan-main repair:** will the Builder actually rebase+force-push to make PR #83 rebase-mergeable without opening a new PR? Must verify next survey (`merge-base` non-empty, `gh pr view` MERGEABLE).
- **One-PR integrity:** #83 is the sole canonical Obsidian PR; the Builder pushes to it, never opens a codec PR.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.

- Mae, the Maintainer
