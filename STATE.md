# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~15:10Z, maintainer run 32152812476, triggered by owner `/oc maintainer` on PR #83). **DECISIONS:** `[{"action":"continue","pr":83}]`. Resumed the Builder on the single canonical PR #83 to (1) durably repair the re-opened orphan-`main` break by rebasing the branch onto `main` (force-push, SAME branch, no new PR) and (2) implement the corrected R3 blueprint (R3-B Rice-through-binary + neutral prior, then R3-A residual DIFF context, R3-C, R2.4) and re-measure on real Kodak. No merge (gates unmet / reproducible measurement still being established).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: this is currently NOT satisfied (see Open questions) - flagged for a Builder/Factory pass, not a direct `main` edit by Mae.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RE-OPENED)

- **Mergeability (BROKEN again):** PR #83 OPEN, head `977398e0c1d32d556ffda62426345b00be0b4daf`, `mergeable: CONFLICTING`, **no common ancestor with `main` (`e4e33928`)** - `git merge-base` returns empty. The Factory's squash-rebase (`f1788472`, "factory: rebase Obsidian codec (M0-R3) onto main") created a *parallel* history whose commits duplicate main's messages with new SHAs (e.g. `9d4ed56e` mirrors main's `30fd1508`), so `--rebase` of #83 is impossible. This blocks the eventual merge of the fundamental goal and MUST be repaired (the Builder is instructed to rebase the branch onto `origin/main` and force-push the SAME branch, no new PR).
- **Measurement blocker (root cause understood, path set):**
  - `obsidian/benchmarks/data/kodak/` is **git-ignored by design** (only `kodak.sha256` is tracked). The PPMs are fetched+normalized into the working tree at benchmark time and verified against `kodak.sha256`; they are NOT meant to live in git. The Factory is the WRONG agent (its prompt forbids `/obsidian/`); the Builder owns this.
  - Harness hardening landed during Builder run `32151973192`: `run_kodak.sh` is now self-provisioning (`--provision` download+convert+manifest), fail-fast sha256-verifying the 24 PPMs, `--require-refs` gated, with an explicit competitive-gate summary (Obsidian mean bpp vs JXL 8.71 / WebP 9.61 / PNG 13.05). The gate is now reproducible in any Builder env with network + toolchain.
  - **Open risk:** the earlier Builder runs could not reach a no-auth Kodak mirror (Kaggle needs a token; public mirrors 404/HTML), so even with the harness, real-Kodak reproduction in CI is uncertain. The Builder must report cleanly if data is unreachable - never fake numbers.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `977398e0`). **ROOT-CAUSE FIX earlier this cycle:** `ppm.rs` decoded the interleaved P6/P5 raster as planar, scrambling R/G/B; fixed, codec bit-exact. Corrected real-Kodak baseline (effort 4) = **10.16 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.45; JPEG XL 8.71 MISSED by 1.45).
- **CMARC stack (R1 -> R2.4) built, all OFF by default.** On real Kodak it shaved only ~0.07 bpp off v1 GR, plateauing at ~10.09 bpp - ~0.38 bpp above JPEG-LS (9.71) on the SAME LOCO-I GAP predictor, so the entropy backend / integration is the proven bottleneck.
- **Corrected R3 blueprint delivered** (commit `b6f67d04`, `obsidian/docs/architect-r3-residual-context-blueprint.md`): R3-B Rice-through-binary magnitude (constant 35 bins/ctx) + neutral `CMARC_PRIOR=2048` first; then R3-A residual DIFF context (capped <=365 ids, no activity-class multiplication, per-image selection flag); R3-C run mode; R2.4 re-tune. Targets < 9.61 (WebP) then < 8.71 (JPEG XL).

## In flight

- **Builder `continue` run (this decision):** triggered by this run's `{"action":"continue","pr":83}`. Two ordered tasks: (1) rebase `opencode/issue68-20260818070512` onto `origin/main`, force-push the SAME branch (repair orphan-main, no new PR); (2) implement corrected R3-B -> R3-A -> R3-C -> R2.4 and re-measure on real Kodak (or synthetic if PPMs unreachable). Watched; no duplicate trigger.

## PENDING (deferred to a quiet run)

- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Needs a Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Factory hardening (one-PR rule):** dispatch the Factory Engineer to harden the workflow/agent so it NEVER opens a new PR for an issue that already has an open Obsidian/codec PR; it must reuse/push to the existing branch. Deferred (owner said stop opening new PRs; also the Factory is the wrong data tool, so this is lower priority now).
- **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive).

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `main` workflow agent steps (factory/review/test) pin `opencode/hy3-free` (merged PR #85 at `e4e33928`). `opencode.json` `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free).
- **Mergeability:** PR #83 OPEN, head `977398e0`, `mergeable: CONFLICTING` (NO common ancestor with main `e4e33928` - orphan break re-opened by Factory squash-rebase). Must be repaired before `--rebase` merge is possible.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Watch the Builder `continue` run:** it must (a) rebase the branch onto `main` and force-push the same branch so PR #83 becomes rebase-mergeable, and (b) implement corrected R3 and produce a reproducible real-Kodak (or honest synthetic) number.
2. **If R3 clears WebP 9.61 but not JPEG XL 8.71:** continue to R3-C / R2.4 per blueprint; if still short, re-engage Researcher/Architect for a true QM-class adaptive arithmetic coder (no autopilot `continue`).
3. **After a reproducible real-Kodak number below all three gates:** rebase-merge (branch preserved per owner directive), close #68.
4. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.

## Open questions

- **Can the Builder reproduce the exact Kodak PPMs in CI?** Network + toolchain needed; public mirrors returned 404/HTML earlier, Kaggle needs a token. If unreachable, the Builder must report the synthetic-proxy number honestly and flag the gate as unmeasurable - never fake data.
- **Will corrected R3 (neutral prior + Rice-through-binary + bounded residual context) actually beat 9.61 on real Kodak?** The Architect's analysis says yes (~9.4-9.7); the first R3 regressed due to the prior/budget bug now corrected. Awaits measurement.
- **Orphan-main repair:** will the Builder's rebase+force-push make PR #83 rebase-mergeable without opening a new PR? Must verify next survey (`merge-base` non-empty, `gh pr view` MERGEABLE).
- **One-PR integrity:** #83 is the sole canonical Obsidian PR; the Builder pushes to it, never opens a codec PR.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.

- Mae, the Maintainer
