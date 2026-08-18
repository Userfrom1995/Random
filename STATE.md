# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~14:50Z, maintainer run 32150664360). **DECISIONS THIS RUN:** merged PR #85 (infra model swap, approved by Reviewer+Tester, closes no issues, branch preserved); closed PR #86 (redundant duplicate of #85 + wrong `Closes #68` + opened in error by a FAILED Factory run); re-dispatched Factory on #68 to durably land the Kodak PPMs on the existing branch (no new PR). Builder on #83 left in flight (no re-trigger).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`.
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (measurement BLOCKER still open)

- **PR #85 MERGED (run 32150664360):** review/test/factory workflow models `mimo-v2.5-free` -> `hy3-free`. All 11 workflow agent slots now pin `hy3-free`; opencode.json `small_model` stays `mimo-v2.5-free` (free, no CreditsError). Branch preserved.
- **PR #86 CLOSED (run 32150664360):** redundant duplicate of #85, wrongly claimed `Closes #68`, opened in error by Factory run 32150104809 (which FAILED its actual task: durably committing Kodak PPMs).
- **Measurement blocker STILL OPEN:** `obsidian/benchmarks/data/kodak/*.ppm` is NOT yet committed on the PR #83 branch (only `obsidian/benchmarks/data/kodak.sha256` exists on `opencode/issue68-20260818070512`). The Factory was re-dispatched this run (decision `factory` on #68) to durably land the 24 PCD0992 Kodak PPMs and harden `run_kodak.sh`. Until that lands, the 10.0906 bpp real-Kodak number is not reproducible and no further gate measurement is possible.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`). Last trustworthy real-Kodak effort-4 = **10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.48; JPEG XL 8.71 MISSED by 1.38). NON-reproducible until PPMs durably committed.
- **CMARC RESEARCH + ARCHITECT BLUEPRINT DELIVERED** (off by default; production byte-identical to v1 GR; 106 lib tests pass).
- **R3 CORRECTED BLUEPRINT DELIVERED (14:29:43Z):** R3-B Golomb-Rice-through-binary using `CarcCtx.k` -> constant `cmarc_bins_per_ctx()=35`; **neutral `CMARC_PRIOR=2048`**; R3-A residual DIFF context capped <=365 ids; per-image winner-selection flag so a regression can never ship. Build order R3-B->R3-A->R3-C->R2.4. Gates WebP 9.61 / JPEG XL 8.71.
- **R3 BUILDER REVERTED (14:18:41Z)** to clean R2.4 baseline after first R3 sparse-context regression; resumed via `continue` (owner 14:31:56Z) to implement corrected R3.

## In flight

- **Builder (continue, PR #83, run 32149962340, PENDING/queued):** implementing corrected R3 (R3-B -> R3-A -> R3-C -> R2.4), will re-measure on REAL Kodak effort-4 at full effort / highest-quality vs WebP, PNG, JPEG XL (+ other relevant codecs) per owner 14:42 directive. Keep all seams OFF by default; never-expand safety net; per-image winner-selection flag must prevent any regression shipping. NOT re-triggered this run (avoid duplicate). If it measured before Factory lands the PPMs, re-`continue` next run.
- **Factory (re-dispatched THIS run, decision `factory` on #68):** durably commit `obsidian/benchmarks/data/kodak/*.ppm` (24 PCD0992 Kodak PPMs) to `opencode/issue68-20260818070512` (NO new PR; push to existing branch) matching `kodak.sha256`, and harden `run_kodak.sh` (fail fast + sha256 verify). Must reproduce JXL 8.7062 / WebP 9.6130 / JLS 9.7113 / PNG 13.0518.

## PENDING (deferred to a quiet run)

- **Factory hardening (one-PR rule):** dispatch the Factory Engineer to harden the workflow/agent so it NEVER opens a new PR for an issue that already has an open Obsidian/codec PR; it must reuse/push to the existing branch. Deferred to honor the owner's explicit "stop opening new PRs" instruction (a factory fix PR would itself be a new PR). The PR #86 incident re-confirms this is still needed.
- **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive).

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). After PR #85 merge, ALL workflow `.yml` agent steps pin `hy3-free` (auditor, factory, ideate, maintainer, review, test, opencode x5); `small_model` stays `mimo-v2.5-free`.
- **Mergeability:** PR #83 OPEN, head `7d096a8` = main (`30fd150`) + 1 commit, valid merge base, `mergeable: MERGEABLE` (UNSTABLE). PR #85 MERGED. PR #86 CLOSED.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Factory (in flight, on #68):** durably commit `obsidian/benchmarks/data/kodak/*.ppm` (matching `kodak.sha256`) to `opencode/issue68-20260818070512` (no new PR); harden `run_kodak.sh`. Confirm it reproduces JXL 8.7062 / WebP 9.6130 / JLS 9.7113 / PNG 13.0518.
2. **Builder (in flight, PR #83, run 32149962340):** implement corrected R3 (R3-B -> R3-A -> R3-C -> R2.4), re-measure on REAL (now-durable) Kodak effort-4 at full effort / highest-quality vs WebP, PNG, JPEG XL (+ other relevant codecs) per owner 14:42 directive. Keep all seams OFF by default; never-expand safety net; per-image winner-selection flag must prevent any regression shipping. If it ran before data landed, re-`continue`.
3. **After data lands + R3 builds:** re-measure on real Kodak. If gates still unmet, re-engage Researcher/Architect (existing PR only) for a true QM-class adaptive arithmetic coder - do NOT autopilot with bare `continue`.
4. **Merge gate (only when met AND reproducible AND main repaired):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact, reproducible). Then merge (branch preserved per owner directive), close #68.
5. **Verify README + index.html** still promote Obsidian as Current on every Obsidian advance.

## Open questions

- **Decisive blocker being closed (again):** `data/kodak/*.ppm` not yet in git on the PR #83 branch; the 10.0906 bpp number is not reproducible. The Factory (re-dispatched this run) must durably commit the PPMs to the existing branch. Prior Factory attempts (run `160`/PR #84, run 32148116537/PR #85, run 32150104809/PR #86) did not durably land the data.
- **Will corrected R3 clear the WebP (9.61) / JPEG XL (8.71) gates on real Kodak?** The neutral `CMARC_PRIOR` + Rice-through-binary + bounded DIFF context is designed to avoid the sparse-context regression; the Builder will measure it against the owner's full-effort / highest-quality benchmark set. If it still stalls above 9.71 (JPEG-LS), a true QM-class adaptive arithmetic backend is the remaining path.
- **One-PR integrity:** #83 is the sole canonical Obsidian PR; the Factory pushes data to it, never opens a codec PR. PR #86 (a stray duplicate opened by a failed Factory run) is now CLOSED. The Factory-hardening deferred item remains to prevent recurrence.
- **Mergeability:** PR #83 head `7d096a8` = main + 1 commit, valid merge base, MERGEABLE. PR #85 MERGED (branch preserved). PR #86 CLOSED.

- Mae, the Maintainer