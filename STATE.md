# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~15:47Z, maintainer run 32156541447, triggered by owner `/oc research` + `/oc maintainer` on PR #83). **DECISIONS:** `[{"action":"research","pr":83}]`. Re-engaged the Researcher (Mode 2) on the single canonical PR #83 to diagnose the **binary range coder explosion** on real Kodak (the decisive root-cause bug masking every CMARC "win"). The prior `/oc research` trigger (run `32156521813`) silently failed in 13s (no deliverable, masked by `continue-on-error`), so this run re-fires it. No merge (gates unmet; CMARC itself explodes on real Kodak). One PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: this is currently NOT satisfied (see Open questions) - flagged for a Builder/Factory pass, not a direct `main` edit by Mae.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break STILL OPEN)

- **Mergeability (BROKEN):** PR #83 OPEN, head `206781fc`, `mergeable: CONFLICTING`, **no common ancestor with `main`** - `git merge-base origin/main opencode/issue68-20260818070512` returns EMPTY; `main` is NOT an ancestor of the branch. This blocks the eventual `--rebase` merge and MUST be repaired (Builder rebases `opencode/issue68-20260818070512` onto `origin/main` and force-pushes the SAME branch, no new PR).
- **Measurement blocker (root cause fully understood):**
  - `obsidian/benchmarks/data/kodak/` is **git-ignored by design** (only `kodak.sha256` tracked). PPMs are fetched+normalized at benchmark time and verified against `kodak.sha256`; not meant to live in git. The Builder owns reproduction via `run_kodak.sh --provision` (self-provisioning + fail-fast sha256 verify landed in Builder run 32151973192).
  - **Open risk:** earlier Builder runs could not reach a no-auth Kodak mirror (Kaggle needs a token; public mirrors 404/HTML), so even with the harness, real-Kodak reproduction in CI is uncertain. The Builder must report cleanly if data is unreachable - never fake numbers.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `206781fc`). **ROOT-CAUSE FIX earlier this cycle:** `ppm.rs` decoded the interleaved P6/P5 raster as planar, scrambling R/G/B; fixed, codec bit-exact. Corrected real-Kodak baseline (effort 4) = **10.16 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.45; JPEG XL 8.71 MISSED by 1.45).
- **CMARC stack (R1 -> R2.4) built, all OFF by default.** On real Kodak it shaved only ~0.07 bpp off v1 GR, plateauing at ~10.09 bpp - but that number came ENTIRELY from the never-expand safety net falling back to GR.
- **R3 BLOCKED by a CORE CODER BUG (decisive finding, Builder run 32153177489):** the shared 16-bit binary range coder (`BinModel` WNC probabilities in `rans.rs`, used by both CMARC `RangeEnc`/`RangeDec` and M3-A `BinEnc`/`BinDec`) is lossless but **EXPLODES on real Kodak residuals** - CMARC forced = kodim01 27.3, kodim02 25.5, kodim03 21.6 bpp vs GR; R3-B reverted to blueprint-exact unary and still exploded (25.7 bpp); R3-A scaffolding is safe/off-by-default (`OBSIDIAN_CARC_RESIDUAL_CTX`). The blueprint's "CMARC costs H(p)+epsilon" assumption is false on real residuals - the binary coder's probability adaptation is broken. The progress file states this is a Researcher/Architect task, not a Builder task.

## In flight

- **Researcher `research` run (this decision, RE-FIRED):** my prior run (32156121439, 15:42Z) decided `research`; the hardcoded step posted `/oc research` (owner 15:46:48Z); `opencode.yml` research job `32156521813` concluded `success` in 13s but committed **no diagnostic doc and posted no bot comment** - silently failed (masked by `continue-on-error`). This run re-fires `research` on PR #83. Task: diagnose WHY the binary range coder explodes on real photographic residuals (WNC prior/adaptation, context sparsity, or a lockstep/normalization bug in `RangeEnc`/`RangeDec`/`BinEnc`/`BinDec`), and prescribe a correct context-modeled adaptive arithmetic coder (QM-class or correct adaptive rANS) that reaches `H(p)+epsilon` on real Kodak. Targets the existing single PR. If this re-fire also silently fails, forward directly to the Architect with the existing empirical diagnosis and flag the 13s-crash to the Factory (model/infra fallback).

## PENDING (deferred to a quiet run)

- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Needs a Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Factory hardening (one-PR rule):** dispatch the Factory Engineer to harden the workflow/agent so it NEVER opens a new PR for an issue that already has an open Obsidian/codec PR; it must reuse/push to the existing branch. Deferred (owner said stop opening new PRs; also the Factory is the wrong data tool, so this is lower priority now).
- **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive).
- **Orphan-main repair:** Builder must rebase `opencode/issue68-20260818070512` onto `origin/main` and force-push the SAME branch (no new PR) so PR #83 becomes rebase-mergeable.
- **opencode.yml `continue-on-error` hardening:** the research job's `continue-on-error: true` masked a silent 13s failure (no deliverable, no comment). Consider a post-step guard that fails the run if no `/tmp/random-lab-decision.json` is written - Factory task, but lower priority than the coder bug.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `main` workflow agent steps (factory/review/test) pin `opencode/hy3-free`. `opencode.json` `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free).
- **Mergeability:** PR #83 OPEN, head `206781fc`, `mergeable: CONFLICTING` (NO common ancestor with main - orphan break still open; Builder `continue` did not repair it). Must be repaired before `--rebase` merge is possible.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Wait for the Researcher's diagnosis** of the binary-coder explosion (re-fired this run); then have the Architect re-blueprint the coder fix on PR #83 (Mode 2) and the Builder resume via `continue`.
2. **If the re-fired research silently fails again (13s no-op):** forward directly to the Architect with the existing empirical diagnosis (binary-coder adaptation broken, predictor sound - same LOCO-I GAP as JPEG-LS which hits 9.71 bpp), and flag the opencode.yml `continue-on-error` masking + possible model/API crash to the Factory for fallback.
3. **After a reproducible real-Kodak number below all three gates:** Builder repairs orphan-main (rebase+force-push), then rebase-merge (branch preserved per owner directive), close #68.
4. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.

## Open questions

- **Why does the 16-bit binary range coder explode on real Kodak (21-27 bpp) while staying lossless?** WNC prior too strong? adaptation too slow on sparse contexts? a normalization/lockstep bug in `RangeEnc`/`RangeDec`/`BinEnc`/`BinDec`? Awaits the (re-fired) Researcher.
- **Can the Researcher/Architect deliver a correct adaptive arithmetic coder that reaches JPEG-LS-class (9.71) or better on real Kodak?** The predictor is sound (same LOCO-I GAP as JPEG-LS); the entropy backend is the proven bottleneck.
- **Can the Builder reproduce the exact Kodak PPMs in CI?** Network + toolchain needed; public mirrors returned 404/HTML earlier, Kaggle needs a token. If unreachable, the Builder must report the synthetic-proxy number honestly and flag the gate as unmeasurable - never fake data.
- **Orphan-main repair:** will the Builder actually rebase+force-push to make PR #83 rebase-mergeable without opening a new PR? Must verify next survey (`merge-base` non-empty, `gh pr view` MERGEABLE).
- **One-PR integrity:** #83 is the sole canonical Obsidian PR; the Builder pushes to it, never opens a codec PR.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **opencode.yml silent-failure masking:** the research job's `continue-on-error: true` let a 13s no-deliverable run pass as `success`. Should be guarded so a missing decision.json fails the run.

- Mae, the Maintainer
