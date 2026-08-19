# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~01:35Z, maintainer run 32205501609, scheduled dispatch). **DECISIONS:** `[{"action":"research","issue":68}]` - escalate to The Researcher for an independent, provably-correct binary arithmetic/range coder, because the Architect's R4 references kept failing to produce a working compressing coder (head still `36ec553`, "10 emits vs 43 reads"). No other triggers fired.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: this is currently NOT satisfied (see Open questions) - flagged for a Builder/Factory pass, not a direct `main` edit by Mae.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch. Redundant codec-rebase PR #84 was opened by the Factory earlier and REJECTED by the owner; it is CLOSED (confirmed CLOSED).
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break STILL OPEN; rebase deferred)

- **Mergeability (BROKEN):** PR #83 OPEN, head `36ec55330daf91a604cb88d9fd549a942b9d279e` ("Bug: 10 emits vs 43 reads; byte accounting desync."), `mergeable: false` (CONFLICTING), **no common ancestor with `main`** - `git merge-base origin/main opencode/issue68-20260818070512` returns EMPTY (verified live in prior runs); `main` (`e4e3392`, single orphan commit) is NOT an ancestor of the branch. This blocks the eventual `--rebase` merge.
- **Owner-mandated repair (16:51Z, MANY runs overdue):** the Builder must rebase `opencode/issue68-20260818070512` onto `origin/main` (replay all codec commits on top of `e4e3392`, preserving every commit's work) and force-push the SAME branch - NO new PR. The Factory is deliberately NOT used for the rebase (its prior squash-rebase opened redundant PR #84 and re-orphaned `main`, violating the one-PR rule). Deferred until after the coder is fixed; non-blocking now because the performance gate is unmet.
- **Measurement blocker (RESOLVED):** `obsidian/benchmarks/data/kodak/` PPMs ARE PRESENT and tracked in git (kodim01..24.ppm). `run_kodak.sh` self-provisions + verifies against `kodak.sha256`. R4 re-measurement on REAL Kodak is possible. Earlier "10.0906 bpp" was GR-fallback only (CMARC explodes until the coder is fixed).

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `36ec553`). Root-cause PPM-scramble fix landed; codec bit-exact. Corrected real-Kodak baseline (effort 4) = **10.16 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.45; JPEG XL 8.71 MISSED by 1.45).
- **CMARC stack (R1 -> R2.4) + R3 built, all OFF by default.** On real Kodak CMARC itself EXPLODES (21-27 bpp forced) - the never-expand net falls back to GR, so every quoted "best" number (10.09, 10.16) was GR all along. CMARC has never beaten GR because the shared binary coder is **lossless but does NOT compress** (p=0.1 -> 1.745 bps vs 0.469 Shannon = 3.72x; p=0.01 -> 3.348 vs 0.081 = 41x).
- **R4 (correct arithmetic coder + mandatory <1.10x efficiency gate): FIFTH FAILURE, now escalated to the Researcher.** The Architect produced two defective references: `53d63e4` ("architect: R4 revised - byte-oriented LZMA range coder, exact buildable spec + efficiency gate") had a `shift_low` that masks `low` to 32 bits (discarding the LZMA carry accumulator) and an emit constant `0xFF000000` that should be `0x01000000`. The Builder's `continue` (run producing `36ec553`, 20:36:07Z) copied it and pushed a WIP bug state ("10 emits vs 43 reads; byte accounting desync"). The Architect was re-engaged at 20:39:37Z (run 569) to deliver a corrected, tested reference but COMPLETED at 20:39:40Z WITHOUT pushing a fix - branch head unchanged at `36ec553` five hours later. Per STATE §7, the next Mae run escalates to the Researcher for an independent, provably-correct coder design.

## In flight

- **Researcher (triggered THIS run 32205501609, via `/oc research` on issue #68, IN FLIGHT after dispatch):** deliver an independent, provably-correct binary arithmetic/range coder design (true 64-bit carry accumulator; correct renorm/emit; encoder/decoder byte counts provably equal), shipped with a self-contained Rust test proving `measured_bps / shannon_bps < 1.10` AND a full round-trip BEFORE the spec is handed to the Architect/Builder. Targets the SAME single PR - no new build.
- **No Architect / Builder in flight.**

## PENDING (deferred to a quiet run)

- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Needs a Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Branch rebase onto `main` (owner 16:51Z):** deferred until after R4 coder fixed; then Builder force-pushes the SAME branch, verify MERGEABLE.
- **Factory infra hardening:** raise build `timeout-minutes` (opencode.yml) only if a future `continue` again truncates at 60m; harden `continue-on-error` so a masked failure fails the run. NOT triggered this run (the failure was a design defect in the coder, not a timeout).

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active. Researcher now engaged for the coder.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** main workflow agent steps (factory/review/test) pin `opencode/hy3-free`. `opencode.json` `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). main currently = `e4e3392 factory: upgrade reviewer/tester/factory models from mimo-v2.5-free to hy3-free` - the earlier `CreditsError` billing outage is RESOLVED.
- **Mergeability:** PR #83 OPEN, head `36ec553`, `mergeable: false` (CONFLICTING - NO common ancestor with main - orphan break still open; rebase deferred to after R4 coder fix).
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Researcher (IN FLIGHT):** deliver the independent, verified coder spec (true 64-bit carry accumulator; correct renorm/emit; provably-equal encoder/decoder byte counts; self-contained Rust test proving <1.10x efficiency + full round-trip) to issue #68 / PR #83.
2. **Architect (after Researcher lands):** implement the Researcher's verified coder into `obsidian` on the existing branch (replace `RcEnc`/`RcDec` + `BinEnc`/`BinDec` with the fixed `RangeEnc`/`RangeDec`; drop `BitWriter`/`BitReader` from carc call sites; adopt `[carc_len][carc_bytes]` framing), land the mandatory efficiency-gate test (remove `#[ignore]`), get `cargo test -p obsidian_core` green.
3. **Builder `continue` (after Architect integrates):** land a clean R4, re-measure R1/R2/R3 on REAL Kodak effort-4 (data durably in git): target < 9.71 JPEG-LS, ideally < 9.61 WebP, then < 8.71 JPEG XL. Record `benchmarks/results/2026-08-19-real-kodak-r4.csv`. Never fake a number.
4. **Builder rebases branch onto `origin/main`** + force-pushes the SAME branch (clear CONFLICTING, preserve all codec work, no new PR).
5. **After a reproducible real-Kodak number below all three gates:** branch already rebase-mergeable, then rebase-merge (`--no-delete-branch` per owner directive), close #68.
6. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
7. **If the Researcher's spec ALSO fails to let the Architect/Builder land R4:** next Mae run should dispatch the Factory (`factory`) for a faster free model / longer `timeout-minutes` and consider a battle-tested reference coder (e.g. a known-good arithmetic coder from a reputable source) before re-resuming.

## Open questions

- **Will the Researcher deliver a verified-correct, efficiency-gated coder spec the Architect can implement into a working, compressing Obsidian backend?** The Architect's two references both failed; an independent correct derivation is the documented escalation (STATE §7). Watch for the Researcher's handoff to the existing PR.
- **Will a correctly-compressing CMARC reach JPEG-LS-class (9.71) or better on REAL Kodak?** Predictor is sound (same LOCO-I GAP); broken coder was the proven 3.7-41x-over-Shannon bottleneck. Awaits R4 completion + re-measurement.
- **Will the branch rebase onto `main` succeed (preserving all codec work) and make PR #83 MERGEABLE without a new PR?** Owner-requested 16:51Z, many runs overdue. Verify next survey (`merge-base` non-empty, `gh pr view 83` MERGEABLE, no new issue68 codec PR).
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84 confirmed CLOSED; no new issue68 codec PR.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** timeout-raise / continue-on-error hardening still pending (deferred); reassess only if a future `continue` truncates at 60m.

- Mae, the Maintainer
