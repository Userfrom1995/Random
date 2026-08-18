# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~20:43Z, maintainer run 32183829799, owner `/oc maintainer` on PR #83). **DECISIONS:** `[]` - hold. The Architect (re-engaged at 20:39:34Z, in flight) reproduced the R4 coder defect at 20:43:05Z (`low < 0xFF000000` should be `low < 0x01000000`) and is still verifying; no corrected reference has landed, so no `continue` fired and no duplicate `architect` fired.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: this is currently NOT satisfied (see Open questions) - flagged for a Builder/Factory pass, not a direct `main` edit by Mae.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch. Redundant codec-rebase PR #84 was opened by the Factory earlier and REJECTED by the owner; it is CLOSED (confirmed CLOSED).
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break STILL OPEN; rebase deferred)

- **Mergeability (BROKEN):** PR #83 OPEN, head `36ec55330daf91a604cb88d9fd549a942b9d279e` ("Bug: 10 emits vs 43 reads; byte accounting desync."), `mergeable: false` (CONFLICTING), **no common ancestor with `main`** - `git merge-base origin/main opencode/issue68-20260818070512` returns EMPTY (verified live this run); `main` (`e4e3392`, single orphan commit) is NOT an ancestor of the branch. This blocks the eventual `--rebase` merge.
- **Owner-mandated repair (16:51Z, MANY runs overdue):** the Builder must rebase `opencode/issue68-20260818070512` onto `origin/main` (replay all codec commits on top of `e4e3392`, preserving every commit's work) and force-push the SAME branch - NO new PR. The Factory is deliberately NOT used for the rebase (its prior squash-rebase opened redundant PR #84 and re-orphaned `main`, violating the one-PR rule). Deferred until after the coder is fixed; non-blocking now because the performance gate is unmet.
- **Measurement blocker (RESOLVED):** `obsidian/benchmarks/data/kodak/` PPMs ARE PRESENT and tracked in git (kodim01..24.ppm). `run_kodak.sh` self-provisions + verifies against `kodak.sha256`. R4 re-measurement on REAL Kodak is possible. Earlier "10.0906 bpp" was GR-fallback only (CMARC explodes until the coder is fixed).

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `36ec553`). Root-cause PPM-scramble fix landed; codec bit-exact. Corrected real-Kodak baseline (effort 4) = **10.16 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.45; JPEG XL 8.71 MISSED by 1.45).
- **CMARC stack (R1 -> R2.4) + R3 built, all OFF by default.** On real Kodak CMARC itself EXPLODES (21-27 bpp forced) - the never-expand net falls back to GR, so every quoted "best" number (10.09, 10.16) was GR all along. CMARC has never beaten GR because the shared binary coder is **lossless but does NOT compress** (p=0.1 -> 1.745 bps vs 0.469 Shannon = 3.72x; p=0.01 -> 3.348 vs 0.081 = 41x).
- **R4 (correct arithmetic coder + mandatory <1.10x efficiency gate): FOURTH FAILURE, root-caused to the blueprint reference itself.** The "concrete copy-paste" reference delivered by the Architect (commit `53d63e4`, `architect-r4-binary-coder-blueprint.md`) is defective: its `RangeEnc::shift_low` does `self.low = (self.low << 8) & 0xFFFF_FFFF`, masking `low` to 32 bits every call and discarding the LZMA carry accumulator; `(self.low >> 32) as u8` is then dead code, so the encoder emits a byte count that does not match the decoder's expectation ("10 emits vs 43 reads"). The Builder's `continue` (from run 32179754782) copied it and pushed `36ec553` (a WIP bug state).
- **Architect (this run / prior run 32183165907 -> IN FLIGHT now):** re-engaged (Mode 2, PR #83) at 20:39:34Z to deliver a CORRECTED, actually-tested range coder reference. At 20:43:05Z it reproduced the desync and localized the emit guard (`low < 0xFF000000` should be `low < 0x01000000`); it is verifying with a parametrized test and has NOT yet pushed the corrected reference. Once it lands, the Builder resumes via `continue`.

## In flight

- **Architect (triggered 20:39:37Z on PR #83, IN FLIGHT):** deliver the corrected, tested range coder reference - true 64-bit `low` carry accumulator, `low < 0x01000000` emit guard (canonical), encoder/decoder byte counts provably equal, passing the mandatory `measured_bps / shannon_bps < 1.10` efficiency gate AND a real round-trip test BEFORE pushing. Returns `continue` for the Builder after the reference lands.
- **No Builder `continue` in flight** (the last one produced `36ec553` and stopped; this run did not re-fire it).

## PENDING (deferred to a quiet run)

- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Needs a Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Branch rebase onto `main` (owner 16:51Z):** deferred until after R4 coder fixed; then Builder force-pushes the SAME branch, verify MERGEABLE.
- **Factory infra hardening:** raise build `timeout-minutes` (opencode.yml) only if a future `continue` again truncates at 60m; harden `continue-on-error` so a masked failure fails the run. NOT triggered this run (the failure was a design defect in the Architect reference, not a timeout).
- **Re-armed escalation clarified:** the prior "factory on timeout" trigger is specific to 60-min truncation. This run's failure was a defective reference, so the Architect (not Factory) is the correct escalation.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** main workflow agent steps (factory/review/test) pin `opencode/hy3-free`. `opencode.json` `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). main currently = `e4e3392 factory: upgrade reviewer/tester/factory models from mimo-v2.5-free to hy3-free` - the earlier `CreditsError` billing outage is RESOLVED.
- **Mergeability:** PR #83 OPEN, head `36ec553`, `mergeable: false` (CONFLICTING - NO common ancestor with main - orphan break still open; rebase deferred to after R4 coder fix).
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Architect (IN FLIGHT):** deliver the corrected, tested range coder reference (true 64-bit carry accumulator; `low < 0x01000000` emit guard; verified <1.10x efficiency + round-trip before push) to `opencode/issue68-20260818070512`.
2. **Builder `continue` (after Architect lands):** integrate the corrected coder (replace `RcEnc`/`RcDec` + `BinEnc`/`BinDec` with the fixed `RangeEnc`/`RangeDec`; drop `BitWriter`/`BitReader` from carc call sites; adopt `[carc_len][carc_bytes]` framing already in place), land the mandatory efficiency-gate test (remove `#[ignore]`), get `cargo test -p obsidian_core` green, commit a clean R4.
3. **Re-measure R1/R2/R3 on REAL Kodak effort-4** (data durably in git): target < 9.71 JPEG-LS, ideally < 9.61 WebP, then < 8.71 JPEG XL. Record `benchmarks/results/2026-08-18-real-kodak-r4.csv`. Never fake a number.
4. **Builder rebases branch onto `origin/main`** + force-pushes the SAME branch (clear CONFLICTING, preserve all codec work, no new PR).
5. **After a reproducible real-Kodak number below all three gates:** branch already rebase-mergeable, then rebase-merge (`--no-delete-branch` per owner directive), close #68.
6. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
7. **If the corrected reference ALSO fails to let the Builder land R4:** next Mae run should escalate harder (consider Researcher for an independent correct coder design, and/or Factory for a faster free model / longer timeout) before re-resuming.

## Open questions

- **Will the in-flight Architect deliver a corrected, tested range coder (true 64-bit carry accumulator; `low < 0x01000000` emit guard; verified <1.10x efficiency + round-trip before push) so the Builder can land R4?** The prior reference was the proven bottleneck; a corrected, tested one is the right escalation. Watch the Architect run for its push to `opencode/issue68-20260818070512`.
- **Will a correctly-compressing CMARC reach JPEG-LS-class (9.71) or better on REAL Kodak?** Predictor is sound (same LOCO-I GAP); broken coder was the proven 3.7-41x-over-Shannon bottleneck. Awaits R4 completion + re-measurement.
- **Will the branch rebase onto `main` succeed (preserving all codec work) and make PR #83 MERGEABLE without a new PR?** Owner-requested 16:51Z, many runs overdue. Verify next survey (`merge-base` non-empty, `gh pr view 83` MERGEABLE, no new issue68 codec PR).
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84 confirmed CLOSED; no new issue68 codec PR.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** timeout-raise / continue-on-error hardening still pending (deferred); reassess only if a future `continue` truncates at 60m.

- Mae, the Maintainer
