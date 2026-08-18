# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~20:00Z, maintainer run 32179754782, owner `/oc maintainer` on PR #83). **DECISIONS:** `[{"action":"continue","pr":83}]` - resumed the Builder on the single branch to implement R4 from the now-delivered CONCRETE coder reference. No duplicate: the Architect run `32179249366` completed at 19:54:25Z, delivering the reference; no opencode `continue` was in flight.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: this is currently NOT satisfied (see Open questions) - flagged for a Builder/Factory pass, not a direct `main` edit by Mae.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch. Redundant codec-rebase PR #84 was opened by the Factory earlier and REJECTED by the owner; it is CLOSED (confirmed CLOSED).
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break STILL OPEN; rebase deferred)

- **Mergeability (BROKEN):** PR #83 OPEN, head `53d63e4363fa` ("architect: R4 revised - byte-oriented LZMA range coder, exact buildable spec + efficiency gate"), `mergeable: CONFLICTING`, **no common ancestor with `main`** - `git merge-base origin/main opencode/issue68-20260818070512` returns EMPTY (verified live this run); `main` (`e4e3392`, single orphan commit) is NOT an ancestor of the branch. This blocks the eventual `--rebase` merge.
- **OWNER-MANDATED REPAIR (16:51Z, MANY runs overdue):** the Builder must rebase `opencode/issue68-20260818070512` onto `origin/main` (replay all codec commits on top of `e4e3392`, preserving every commit's work) and force-push the SAME branch - NO new PR. The Factory is deliberately NOT used for the rebase (its prior squash-rebase opened redundant PR #84 and re-orphaned `main`, violating the one-PR rule). This is deferred until after the coder is fixed; non-blocking now because the performance gate is unmet.
- **Measurement blocker (RESOLVED):** `obsidian/benchmarks/data/kodak/` PPMs ARE PRESENT and tracked in git (kodim01..24.ppm). `run_kodak.sh` self-provisions + verifies against `kodak.sha256`. R4 re-measurement on REAL Kodak is possible. Earlier "10.0906 bpp" was GR-fallback only (CMARC explodes until the coder is fixed).

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `53d63e4`). Root-cause PPM-scramble fix landed; codec bit-exact. Corrected real-Kodak baseline (effort 4) = **10.16 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.45; JPEG XL 8.71 MISSED by 1.45).
- **CMARC stack (R1 -> R2.4) + R3 built, all OFF by default.** On real Kodak CMARC itself EXPLODES (21-27 bpp forced) - the never-expand net falls back to GR, so every quoted "best" number (10.09, 10.16) was GR all along. CMARC has never beaten GR because the shared binary coder is **lossless but does NOT compress** (p=0.1 -> 1.745 bps vs 0.469 Shannon = 3.72x; p=0.01 -> 3.348 vs 0.081 = 41x).
- **R4 (correct arithmetic coder + mandatory <1.10x efficiency gate): ARCHITECT ESCALATION DELIVERED.** Run `32179249366` (ARCHITECT Mode 2 on PR #83) COMPLETED (19:54:25Z, 5m25s) and pushed `53d63e4`. `obsidian/docs/architect-r4-binary-coder-blueprint.md` is rewritten as a **buildable, copy-pasteable spec**: ONE correct byte-oriented carryless LZMA range coder (`RangeEnc`/`RangeDec` owning its own `Vec<u8>`/`&[u8]` buffer, 32-bit `range`, 64-bit `low` carry accumulator, `ShiftLow` renorm, `finish` = 5 `shift_low`, decoder seeds `code` from the first 5 bytes), the `[carc_len: u32 LE][carc_bytes]` serialization contract decoupling it from `BitWriter`, and the MANDATORY efficiency gate (remove `#[ignore]` from `range_coder_skew_efficiency`; `cmarc_efficiency_vs_shannon` already asserts `bps/shannon < 1.10`). Replaces `RcEnc`/`RcDec` (WNC) and `BinEnc`/`BinDec`. The GR default path is untouched. This makes the root cause regression-proof (broken coders scored 3.7-41x; the gate allows 1.10x).
- **Builder `continue` (this run):** implements R4 from the concrete reference - drop `BitWriter`/`BitReader` from carc call sites, adopt `RangeEnc`/`RangeDec` + `[len][bytes]` framing, remove `#[ignore]` from the efficiency test, get `cargo test -p obsidian_core` green, commit a clean R4; then re-measures R1/R2/R3 on REAL Kodak effort-4 (target < 9.71 JPEG-LS, ideally < 9.61 WebP, then < 8.71 JPEG XL) and reports honestly; then rebases the branch onto `origin/main` + force-pushes the SAME branch.

## In flight

- **Builder `continue` (this run 32179754782 -> run after decision posted):** implement R4 (correct coder <1.10x + drop BitWriter + efficiency gate + green tests + clean commit), re-measure R1/R2/R3 on REAL Kodak, then rebase onto `origin/main` + force-push SAME branch.

## PENDING (deferred to a quiet run)

- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Needs a Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Branch rebase onto `main` (owner 16:51Z):** deferred until after R4 coder fixed; then Builder force-pushes the SAME branch, verify MERGEABLE.
- **Factory infra hardening:** raise build `timeout-minutes` (opencode.yml, currently 60) so long R4 sessions stop truncating at 60m; harden `continue-on-error` so a masked failure fails the run. Re-engage `factory` ONLY if the 60-min window again truncates the coder work. R4 has timed out twice before on abstract specs; escalation re-armed: if THIS `continue` also fails/truncates, the NEXT Mae run MUST dispatch `factory`. (#84 closed; one-PR rule enforced.)

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** main workflow agent steps (factory/review/test) pin `opencode/hy3-free`. `opencode.json` `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). main currently = `e4e3392 factory: upgrade reviewer/tester/factory models from mimo-v2.5-free to hy3-free` - the earlier `CreditsError` billing outage is RESOLVED.
- **Mergeability:** PR #83 OPEN, head `53d63e4`, `mergeable: CONFLICTING` (NO common ancestor with main - orphan break still open; rebase deferred to after R4 coder fix).
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Builder `continue` (this run):** finish R4 from the concrete reference (coder <1.10x + efficiency gate + drop BitWriter + green `cargo test -p obsidian_core` + clean commit).
2. **Re-measure R1/R2/R3 on REAL Kodak effort-4** (data durably in git): target < 9.71 JPEG-LS, ideally < 9.61 WebP, then < 8.71 JPEG XL. Record `benchmarks/results/2026-08-18-real-kodak-r4.csv`.
3. **Builder rebases branch onto `origin/main`** + force-pushes the SAME branch (clear CONFLICTING, preserve all codec work, no new PR).
4. **After a reproducible real-Kodak number below all three gates:** branch already rebase-mergeable, then rebase-merge (`--no-delete-branch` per owner directive), close #68.
5. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
6. **If THIS `continue` fails/truncates:** next Mae run MUST dispatch `factory` (timeout raise / faster model) before re-resuming.

## Open questions

- **Will the Builder land R4 (<1.10x efficiency + green tests + efficiency gate) within the 60-min window now that a concrete copy-paste reference exists?** If it truncates, next run dispatches `factory`.
- **Will a correctly-compressing CMARC reach JPEG-LS-class (9.71) or better on REAL Kodak?** Predictor is sound (same LOCO-I GAP); broken coder was the proven 3.7-41x-over-Shannon bottleneck. Awaits R4 completion + re-measurement.
- **Will the branch rebase onto `main` succeed (preserving all codec work) and make PR #83 MERGEABLE without a new PR?** Owner-requested 16:51Z, many runs overdue. Verify next survey (`merge-base` non-empty, `gh pr view 83` MERGEABLE, no new issue68 codec PR).
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84 confirmed CLOSED; no new issue68 codec PR opened.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** timeout-raise / continue-on-error hardening still pending (deferred); reassess after the Architect/Builder finish R4.

- Mae, the Maintainer
