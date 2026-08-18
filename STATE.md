# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~19:30Z, maintainer run 32176992600, owner `/oc maintainer` nudge on PR #83). **DECISIONS:** `[{"action":"continue","pr":83}]` - resumed the Builder on the single branch to (1) FINISH R4 (the WNC arithmetic coder still measures ~2x over Shannon; drive it under 1.10x, land the mandatory efficiency-gate test, green `cargo test -p obsidian_core`, commit clean R4, re-measure R1/R2/R3 on REAL Kodak effort-4) and (2) resolve the CONFLICTING merge state by rebasing `opencode/issue68-20260818070512` onto `origin/main` and force-pushing the SAME branch (no new PR). No merge (gates unmet). One PR preserved. Owner's 16:51Z directive (resolve merge conflicts, preserve all work) explicitly honored.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: this is currently NOT satisfied (see Open questions) - flagged for a Builder/Factory pass, not a direct `main` edit by Mae.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break STILL OPEN, owner-mandated rebase deferred)

- **Mergeability (BROKEN):** PR #83 OPEN, head `5dac45f9...` (R4 WIP: WNC coder swap), `mergeable: CONFLICTING`, **no common ancestor with `main`** - `git merge-base origin/main opencode/issue68-20260818070512` returns EMPTY; `main` (`e4e3392`, single orphan commit) is NOT an ancestor of the branch. This blocks the eventual `--rebase` merge.
- **OWNER-MANDATED REPAIR (16:51Z, now overdue):** in the next `continue` run the Builder must resolve the merge conflicts and preserve all achievements. Approved approach (owner: "or use a better approach if you have one"): rebase `opencode/issue68-20260818070512` onto `origin/main` (replay all codec commits on top of `e4e3392`, preserving every commit's work) and force-push the SAME branch - NO new PR. Verify `git merge-base` non-empty + `gh pr view 83` MERGEABLE. The Factory is deliberately NOT used here (its prior squash-rebase opened redundant PR #84 and re-orphaned `main`, violating the one-PR rule).
- **Measurement blocker (root cause fully understood):**
  - `obsidian/benchmarks/data/kodak/` PPMs are NOW PRESENT in the repo (Builder reported 18:53Z); `run_kodak.sh` self-provisions + verifies against `kodak.sha256`. R4 re-measurement on REAL Kodak is possible this run.
  - Earlier "10.0906 bpp" was GR-fallback only (CMARC explodes until the coder is fixed), so it is not the CMARC ceiling - it is the GR number.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `5dac45f`). **ROOT-CAUSE FIX earlier this cycle:** `ppm.rs` decoded the interleaved P6/P5 raster as planar, scrambling R/G/B; fixed, codec bit-exact. Corrected real-Kodak baseline (effort 4) = **10.16 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.45; JPEG XL 8.71 MISSED by 1.45).
- **CMARC stack (R1 -> R2.4) + R3 (R3-A residual-context, R3-B neutral-prior Rice, R3-C) built, all OFF by default.** On real Kodak CMARC itself EXPLODES (21-27 bpp forced) - the never-expand net falls back to GR, so every quoted "best" number (10.09, 10.16) was GR all along. CMARC has never beaten GR on real Kodak.
- **ROOT-CAUSE DIAGNOSIS (CONVERGED, R4):** The shared 16-bit binary range coder (`RangeEnc`/`RangeDec`/`BinEnc`/`BinDec`) is **lossless but does NOT compress** - a pass-through bit buffer for any skewed probability (empirical probe: p=0.1 -> 1.745 bps vs 0.469 Shannon = 3.72x; p=0.01 -> 3.348 vs 0.081 = 41x). This is the real defect behind every CMARC/R3 "regression": context/quotient/residual tuning is futile because the coder ignores the learned probability. GR is unaffected (separate `GrState` Golomb-Rice coder).
- **R4 blueprint (Architect, commit `33bd48f`):** Replace the four broken binary coders with a **correct arithmetic coder** + **MANDATORY efficiency gate** `measured_bps / shannon_bps < 1.10` for `p in {0.01,0.1,0.5,0.9,0.99}` + Laplacian - fails the build until the coder is correct.
- **R4 IMPLEMENTATION STATUS: INCOMPLETE (coder swapped to WNC).** Builder `continue` run `32174115502` (18:59Z -> completed 19:30Z, pushed `5dac45f`) abandoned the carryless LZMA `ShiftLow`/carry byte-count fix and **swapped in a WNC (Witten-Neal-Cleary) arithmetic coder** with bit I/O, fixing the split mapping so `pm=P(bit==1)` assigns the lower subrange to `bit==1`. `range_coder_bit_roundtrip` now passes (lossless), but **efficiency is still ~2x over Shannon** - the mandatory <1.10x gate is NOT met. R4 is NOT done. The ~2x residual almost certainly means a mapping/normalization detail (cumulative-frequency split, `TOTAL` renormalization, or `pm`->subrange mapping) is still off - a small fixable bug, not a wrong architecture.

## In flight

- **Builder `continue` (this run, run pending dispatch via decision `[continue #83]`):** re-implements/finishes R4 on the single branch:
  1. Make the WNC coder actually compress - drive `measured_bps / shannon_bps` under **1.10x** for the probe set; **land the mandatory efficiency-gate test** (build breaker); green `cargo test -p obsidian_core`; commit clean R4.
  2. Re-measure R1/R2/R3 on NOW-PRESENT real Kodak effort-4 against all three gates; report honestly (target < 9.71 JPEG-LS, ideally < 9.61 WebP), never fake.
  3. Rebase `opencode/issue68-20260818070512` onto `origin/main` (`e4e3392`), resolve conflicts preserving all Obsidian work, and force-push the SAME branch to make PR #83 MERGEABLE (no new PR).
- **ESCALATION TRIGGER (if this continue also fails/times out):** the opencode build step has a 60-min window and R4 has run long before. If R4 again fails to land in this window, the NEXT Mae run MUST dispatch `factory` to raise `timeout-minutes` on the opencode build step (line 318 of `opencode.yml`, currently 60) and/or switch to a faster free model.

## PENDING (deferred to a quiet run)

- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Needs a Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Factory hardening (one-PR rule):** dispatch the Factory Engineer to harden the workflow/agent so it NEVER opens a new PR for an issue that already has an open Obsidian/codec PR; it must reuse/push to the existing branch. Deferred (owner said stop opening new PRs).
- **Fix the malformed `binenc_vs_rangeenc_skew` test** (RNG bug, false failure) - superseded by the R4 mandatory efficiency gate; low priority.
- **opencode.yml `continue-on-error` hardening:** the research job's `continue-on-error: true` masked a silent 13s failure. Consider a post-step guard so a missing decision.json fails the run - Factory task, lower priority than the coder bug. Could batch with the timeout-raise if Factory is dispatched.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `main` workflow agent steps (factory/review/test) pin `opencode/hy3-free`. `opencode.json` `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). main currently = `e4e3392 factory: upgrade reviewer/tester/factory models from mimo-v2.5-free to hy3-free` - the earlier `CreditsError` billing outage is RESOLVED.
- **Mergeability:** PR #83 OPEN, head `5dac45f9`, `mergeable: CONFLICTING` (NO common ancestor with main - orphan break still open; explicit rebase queued for this run's `continue`, owner 16:51Z directive).
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Builder finishes R4 (this run's `continue`):** correct WNC arithmetic coder (<1.10x efficiency) + mandatory efficiency-gate test + green `cargo test -p obsidian_core` + clean R4 commit.
2. **Builder rebases branch onto `origin/main` + force-pushes SAME branch** to resolve the CONFLICTING merge state (owner 16:51Z directive, overdue), preserving all codec work; verify `gh pr view 83` MERGEABLE.
3. **Re-measure R1/R2/R3 on REAL Kodak (effort 4)** now that PPMs are present - with the corrected coder, CMARC should finally beat GR; expect < 9.71 (JPEG-LS) and likely < 9.61 (WebP).
4. **After a reproducible real-Kodak number below all three gates:** branch already rebase-mergeable, then rebase-merge (`--no-delete-branch` per owner directive), close #68.
5. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.

## Open questions

- **Will the WNC coder reach <1.10x efficiency + land the mandatory gate within the 60-min opencode build window?** The Builder swapped coders (LZMA -> WNC); a ~2x residual suggests a mapping/normalization detail is still off - a small fixable bug, not a wrong architecture. If this `continue` again fails to land R4 (or times out), next Mae run MUST dispatch `factory` to raise `timeout-minutes` and/or pick a faster free model.
- **Will the corrected arithmetic coder let CMARC reach JPEG-LS-class (9.71) or better on real Kodak?** The predictor is sound (same LOCO-I GAP as JPEG-LS); the broken coder was the proven bottleneck (3.7-41x over Shannon). R4 removes that. Awaits the Builder's re-measurement on the now-present real Kodak.
- **Will the Builder's rebase onto `main` succeed without opening a new PR and preserve all codec work?** Must verify next survey (`merge-base` non-empty, `gh pr view 83` MERGEABLE, no new issue68 PR opened). This was owner-requested at 16:51Z and is now two runs overdue.
- **One-PR integrity:** #83 is the sole canonical Obsidian PR; the Builder pushes to it, never opens a codec PR. Confirm next survey no new issue68 PR opened.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.

- Mae, the Maintainer
