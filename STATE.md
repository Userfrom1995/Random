# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~16:00Z, maintainer run 32157692174, triggered by owner `/oc maintainer` on PR #83). **DECISIONS:** `[{"action":"architect","pr":83,"head":"f506050f..."}]`. The Researcher (run `32156932119`) finally delivered a concrete root-cause diagnosis of the binary-coder explosion: the coder core is lossless, but the per-(cid,bin) WNC binary models cost ~1.88 bits/bin instead of 1, inflating CMARC entropy 3.3-5.4x. Engaging the Architect (Mode 2) on the single PR to re-blueprint a corrected entropy backend whose probability model actually converges. No merge (gates unmet). One PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: this is currently NOT satisfied (see Open questions) - flagged for a Builder/Factory pass, not a direct `main` edit by Mae.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break STILL OPEN)

- **Mergeability (BROKEN):** PR #83 OPEN, head `f506050f244a931d8125ef372a498a4051ea870e`, `mergeable: CONFLICTING`, **no common ancestor with `main`** - `git merge-base origin/main opencode/issue68-20260818070512` returns EMPTY; `main` is NOT an ancestor of the branch. This blocks the eventual `--rebase` merge and MUST be repaired (Builder rebases `opencode/issue68-20260818070512` onto `origin/main` and force-pushes the SAME branch, no new PR).
- **Measurement blocker (root cause fully understood):**
  - `obsidian/benchmarks/data/kodak/` is **git-ignored by design** (only `kodak.sha256` tracked). PPMs are fetched+normalized at benchmark time and verified against `kodak.sha256`; not meant to live in git. The Builder owns reproduction via `run_kodak.sh --provision` (self-provisioning + fail-fast sha256 verify landed in Builder run 32151973192).
  - **Open risk:** earlier Builder runs could not reach a no-auth Kodak mirror (Kaggle needs a token; public mirrors 404/HTML), so even with the harness, real-Kodak reproduction in CI is uncertain. The Builder must report cleanly if data is unreachable - never fake numbers.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `f506050f`). **ROOT-CAUSE FIX earlier this cycle:** `ppm.rs` decoded the interleaved P6/P5 raster as planar, scrambling R/G/B; fixed, codec bit-exact. Corrected real-Kodak baseline (effort 4) = **10.16 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.45; JPEG XL 8.71 MISSED by 1.45).
- **CMARC stack (R1 -> R2.4) + R3 (R3-A residual-context, R3-B neutral-prior Rice) built, all OFF by default.** On real Kodak CMARC itself EXPLODES (21-27 bpp forced) - the never-expand net falls back to GR, so every quoted "best" number (10.09, 10.16) was GR all along. CMARC has never beaten GR on real Kodak.
- **ROOT-CAUSE DIAGNOSIS (Researcher run 32156932119, ~15:58Z):** the shared 16-bit binary range coder is **lossless and passes near-entropy tests** - the core is NOT broken. The defect is **model adaptation**: the per-(cid,bin) `BinModel` WNC probabilities cost ~0.97-1.88 bits per bin instead of ~1, so CMARC emits 3.3-5.4x true entropy on Laplacian residuals (b=2: 18.97 bpp vs 3.53 entropy). The blueprint's "H(p)+epsilon" claim failed because the WNC adaptation never converges. The `binenc_vs_rangeenc_skew` test is a **malformed RNG** (compares an `f64 < 0.9` against a large integer → all-1s stream) - a red herring, not coder rot. The fix is algorithmic (Architect task), not a Builder wiring task.

## In flight

- **Architect `architect` run (this decision):** engaging the Architect (Mode 2) on the single existing PR #83 to re-blueprint the corrected entropy backend - a per-context adaptive arithmetic/range coder whose probability model actually converges to H(p) (correctly-tuned fast/low-prior WNC, QM-class context-modelled coder, or correct adaptive rANS), integrated with the LOCO-I GAP predictor + residual DIFF context. Delivers the blueprint on the same branch, then the Builder resumes via `continue`.

## PENDING (deferred to a quiet run)

- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Needs a Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Factory hardening (one-PR rule):** dispatch the Factory Engineer to harden the workflow/agent so it NEVER opens a new PR for an issue that already has an open Obsidian/codec PR; it must reuse/push to the existing branch. Deferred (owner said stop opening new PRs).
- **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive).
- **Orphan-main repair:** Builder must rebase `opencode/issue68-20260818070512` onto `origin/main` and force-push the SAME branch (no new PR) so PR #83 becomes rebase-mergeable.
- **Fix the malformed `binenc_vs_rangeenc_skew` test** (RNG bug) - Builder/Fixer task once the coder is reworked; low priority (it's a test-only red herring).
- **opencode.yml `continue-on-error` hardening:** the research job's `continue-on-error: true` masked a silent 13s failure (no deliverable, no comment). Consider a post-step guard that fails the run if no `/tmp/random-lab-decision.json` is written - Factory task, but lower priority than the coder bug.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `main` workflow agent steps (factory/review/test) pin `opencode/hy3-free`. `opencode.json` `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free).
- **Mergeability:** PR #83 OPEN, head `f506050f`, `mergeable: CONFLICTING` (NO common ancestor with main - orphan break still open; Builder `continue` did not repair it). Must be repaired before `--rebase` merge is possible.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Wait for the Architect's blueprint** for the corrected entropy backend (per-context adaptive coder with converging probability model), delivered on PR #83 (Mode 2).
2. **Then resume the Builder via `continue`** on the single branch to implement the corrected coder and re-measure on REAL Kodak (effort 4) against all three gates (JXL 8.71 / WebP 9.61 / PNG 13.05), reporting honestly if PPMs are unreachable (never fake).
3. **After a reproducible real-Kodak number below all three gates:** Builder repairs orphan-main (rebase+force-push), then rebase-merge (branch preserved per owner directive), close #68.
4. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.

## Open questions

- **Will the Architect's corrected coder reach JPEG-LS-class (9.71) or better on real Kodak?** The predictor is sound (same LOCO-I GAP as JPEG-LS); the entropy backend is the proven bottleneck - now localized to WNC model adaptation (per-bin cost ~1.88 bits instead of 1).
- **Can the Builder reproduce the exact Kodak PPMs in CI?** Network + toolchain needed; public mirrors returned 404/HTML earlier, Kaggle needs a token. If unreachable, report the synthetic-proxy number honestly and flag the gate as unmeasurable - never fake data.
- **Orphan-main repair:** will the Builder actually rebase+force-push to make PR #83 rebase-mergeable without opening a new PR? Must verify next survey (`merge-base` non-empty, `gh pr view` MERGEABLE).
- **One-PR integrity:** #83 is the sole canonical Obsidian PR; the Builder pushes to it, never opens a codec PR.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Malformed test:** `binenc_vs_rangeenc_skew` has an RNG bug (false failure) - fix once the coder is reworked.
- **opencode.yml silent-failure masking:** the research job's `continue-on-error: true` let a 13s no-deliverable run pass as `success`. Should be guarded so a missing decision.json fails the run.

- Mae, the Maintainer
