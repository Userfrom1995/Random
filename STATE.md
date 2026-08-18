# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~19:56Z, maintainer run 32179393111, owner `/oc factory` on issue #68). **DECISIONS:** `[]` - NO triggers fired. The Architect escalation from the prior run (32179002001: `architect pr 83` + `factory issue 68`) is ALREADY LIVE: Architect run `32179249366` is in_progress delivering the CONCRETE correct byte-oriented arithmetic/range-coder reference (Mode 2, on the single branch, no new PR). Firing any new trigger would collide. The Factory's own `factory issue 68` decision (run 32179002230) was SKIPPED, and the owner's 19:54Z `/oc factory` (run 32179250198) correctly scoped itself to infra-only and returned `maintainer`; the codec-domain work is the Builder's. No merge (gates unmet).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: this is currently NOT satisfied (see Open questions) - flagged for a Builder/Factory pass, not a direct `main` edit by Mae.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch. Redundant codec-rebase PR #84 was opened by the Factory earlier and REJECTED by the owner; it is CLOSED (confirmed live this run: state CLOSED, MERGEABLE).
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break STILL OPEN; rebase deferred)

- **Mergeability (BROKEN):** PR #83 OPEN, head `ad6efa6b7cca57bace9758254ee79958ce962a82` (R4 WIP: WNC ~2x + bit-sync bug, needs byte-oriented coder), `mergeable: CONFLICTING`, **no common ancestor with `main`** - `git merge-base origin/main opencode/issue68-20260818070512` returns EMPTY (verified live this run); `main` (`e4e3392`, single orphan commit) is NOT an ancestor of the branch. This blocks the eventual `--rebase` merge.
- **OWNER-MANDATED REPAIR (16:51Z, MANY runs overdue):** the Builder must rebase `opencode/issue68-20260818070512` onto `origin/main` (replay all codec commits on top of `e4e3392`, preserving every commit's work) and force-push the SAME branch - NO new PR. The Factory is deliberately NOT used for the rebase (its prior squash-rebase opened redundant PR #84 and re-orphaned `main`, violating the one-PR rule). This is deferred until after the coder is fixed; non-blocking now because the performance gate is unmet.
- **Measurement blocker (RESOLVED):** `obsidian/benchmarks/data/kodak/` PPMs ARE PRESENT in the repo (kodim01..24.ppm). `run_kodak.sh` self-provisions + verifies against `kodak.sha256`. R4 re-measurement on REAL Kodak is possible. Earlier "10.0906 bpp" was GR-fallback only (CMARC explodes until the coder is fixed).

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `ad6efa6`). Root-cause PPM-scramble fix landed; codec bit-exact. Corrected real-Kodak baseline (effort 4) = **10.16 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.45; JPEG XL 8.71 MISSED by 1.45).
- **CMARC stack (R1 -> R2.4) + R3 built, all OFF by default.** On real Kodak CMARC itself EXPLODES (21-27 bpp forced) - the never-expand net falls back to GR, so every quoted "best" number (10.09, 10.16) was GR all along. CMARC has never beaten GR because the shared 16-bit binary range coder is **lossless but does NOT compress** (p=0.1 -> 1.745 bps vs 0.469 Shannon = 3.72x; p=0.01 -> 3.348 vs 0.081 = 41x).
- **R4 (correct arithmetic coder + mandatory <1.10x efficiency gate): THIRD failure -> ESCALATED to Architect.** Builder tried (1) carryless LZMA `ShiftLow` (byte-count bug), (2) WNC coder (lossless but ~1.57-2.05x over Shannon, gate NOT met), (3) hit CMARC bit-sync bug + 32x32 CARC integration bug (`ad6efa6`, "need byte-oriented coder"). The abstract blueprint (commit `33bd48f`) is insufficient; a CONCRETE reference is mandated.
- **Architect escalation LIVE (this run's context):** run `32179249366` (ARCHITECT Mode 2 on PR #83) in_progress since 19:54:27Z, delivering the concrete correct byte-oriented coder reference + mandatory <1.10x efficiency-gate test on the same branch. Returns `continue` for the Builder.

## In flight

- **Architect (`/oc architect` on PR #83, run `32179249366`, in_progress):** deliver a CONCRETE, correct, byte-oriented binary arithmetic/range coder reference implementation (working Rust code) with exact subrange split (`pm=P(bit==1)` -> lower subrange), renormalization, carry handling, and the MANDATORY `measured_bps / shannon_bps < 1.10` efficiency-gate test for `p in {0.01,0.1,0.5,0.9,0.99}` + Laplacian. Commits to the single branch; returns `continue`.
- **Builder `continue` (deferred):** resumes ONLY after the Architect's concrete reference lands - then finishes R4 (correct coder <1.10x + 32x32 CARC bug fix + efficiency-gate test + green `cargo test -p obsidian_core` + clean commit), then re-measures R1/R2/R3 on real Kodak, then does the owner-mandated rebase onto `main`.
- **Factory (DEFERRED, not yet executed):** the prior run's `factory issue 68` decision (run 32179002230) was SKIPPED; the 19:54Z `/oc factory` (run 32179250198) assessed infra healthy and refused `/obsidian` domain work. Pending genuine infra hardening: (a) raise `timeout-minutes` on the opencode build step (60 -> higher) so long R4 sessions stop truncating at 60m; (b) harden `continue-on-error` so a masked failure fails the run. Re-engage Factory on next run if Architect/Builder again hit the 60-min wall. (#84 already CLOSED; one-PR rule enforced.)

## PENDING (deferred to a quiet run)

- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Needs a Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Branch rebase onto `main` (owner 16:51Z):** deferred until after R4 coder fixed; then Builder force-pushes the SAME branch, verify MERGEABLE.
- **Fix the malformed `binenc_vs_rangeenc_skew` test** (RNG bug, false failure) - superseded by the R4 mandatory efficiency gate; low priority.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** main workflow agent steps (factory/review/test) pin `opencode/hy3-free`. `opencode.json` `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). main currently = `e4e3392 factory: upgrade reviewer/tester/factory models from mimo-v2.5-free to hy3-free` - the earlier `CreditsError` billing outage is RESOLVED.
- **Mergeability:** PR #83 OPEN, head `ad6efa6`, `mergeable: CONFLICTING` (NO common ancestor with main - orphan break still open; rebase deferred to after R4 coder fix).
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Architect delivers concrete correct coder reference (run `32179249366`, in flight):** working byte-oriented arithmetic coder + mandatory `<1.10x` efficiency gate, committed on the single branch.
2. **Builder `continue` (after reference lands):** finish R4 (coder <1.10x + 32x32 CARC fix + efficiency-gate test + green tests + clean commit); re-measure R1/R2/R3 on REAL Kodak effort-4 (target < 9.71 JPEG-LS, ideally < 9.61 WebP, then < 8.71 JPEG XL); then rebase branch onto `origin/main` + force-push SAME branch (clear CONFLICTING).
3. **Factory (deferred):** raise build timeout, harden `continue-on-error` - re-engage only if the 60-min window again truncates the coder work. (#84 closed; one-PR enforced.)
4. **After a reproducible real-Kodak number below all three gates:** branch already rebase-mergeable, then rebase-merge (`--no-delete-branch` per owner directive), close #68.
5. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.

## Open questions

- **Will the Architect's CONCRETE reference coder let the Builder land R4 (<1.10x efficiency + 32x32 CARC fixed + green tests)?** The architecture is sound; the failures were purely implementing an abstract spec. A verified reference is the right escalation. Architect run `32179249366` in flight - watch for its push.
- **Will a correctly-compressing CMARC reach JPEG-LS-class (9.71) or better on REAL Kodak?** Predictor is sound (same LOCO-I GAP); broken coder was the proven bottleneck (3.7-41x over Shannon). Awaits R4 completion + re-measurement.
- **Will the branch rebase onto `main` finally succeed (preserving all codec work) and make PR #83 MERGEABLE without a new PR?** Owner-requested 16:51Z, MANY runs overdue. Verify next survey (`merge-base` non-empty, `gh pr view 83` MERGEABLE, no new issue68 codec PR, #84 closed).
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84 (redundant codec-rebase) confirmed CLOSED this run; no new issue68 codec PR opened.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** timeout-raise / continue-on-error hardening still pending (deferred, not yet executed); reassess after the Architect/Builder finish R4.

- Mae, the Maintainer
