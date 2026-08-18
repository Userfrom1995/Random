# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~14:52Z, maintainer run 32150621428, triggered by PR #86 "Models upgraded, need manual push to main" open). **DECISIONS:** (1) Merged PR #85 (Factory infra, model `mimo-v2.5-free` -> `hy3-free`; Reviewer + Tester approved; body `Closes #68` already removed) via rebase, branch preserved - this is the clean path that pushed the model upgrades to `main`. (2) Closed PR #86 as a duplicate of #85; its mislabeled `Closes #68` never fired (closed, not merged) so #68 stays OPEN. (3) Re-dispatched the Factory Engineer on #68 to durably commit the Kodak PPMs to the EXISTING Obsidian branch `opencode/issue68-20260818070512` (no new PR) - the prior Factory attempt (32150104809) FAILED and wrongly opened #86 instead of landing the data. Builder R3 on #83 left in flight (not re-dispatched).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (measurement BLOCKER still open)

- **Mergeability RESOLVED.** PR #83 head `7d096a87fc57bbc716ebd3f604889a43f5e03a57` = `main` (`30fd150`) + 1 commit, valid merge base `30fd150`, `mergeable: MERGEABLE`, `mergeStateStatus: UNSTABLE` (behind base, no conflict). `--rebase` of #83 is possible once the target is met. PR #85 is MERGED.
- **Measurement blocker STILL OPEN:** `obsidian/benchmarks/data/kodak/*.ppm` is NOT yet committed on the Obsidian branch (only `obsidian/benchmarks/data/kodak.sha256` exists). The trustworthy real-Kodak measurement (run ~13:15Z, 10.0906 bpp) used transient PPMs that were never committed, so the number is not reproducible and further gate measurement is blocked. The Factory has been re-dispatched (this run) to durably commit the 24 PCD0992 Kodak PPMs to `opencode/issue68-20260818070512` (NO new PR) and harden `run_kodak.sh`.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `7d096a8`). Last trustworthy real-Kodak effort-4 = **10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.48; JPEG XL 8.71 MISSED by 1.38). That number is currently NON-reproducible (data/kodak absent; Factory in flight again).
- **CMARC RESEARCH DELIVERED** (`obsidian/docs/research-breakthrough.md`): the ~10.1 bpp ceiling is the single-k/per-(cid,bin) GR-style coder, not the image; JPEG-LS reaches 9.71 bpp on the SAME Kodak corpus with the SAME LOCO-I GAP predictor but a context-based arithmetic (QM) coder.
- **CMARC ARCHITECT BLUEPRINT DELIVERED** (`obsidian/docs/architect-cmarc-blueprint.md`): CMARC as `entropy_mode` values (CARC=2, CARC_LZ=3, CARC_MIX=4).
- **CMARC BUILT END-TO-END (R1 -> R2.4), all OFF by default.** Production stays byte-identical to v1 GR. 106 lib tests pass.
- **R3 CORRECTED BLUEPRINT DELIVERED (14:29:43Z, run `32148118020`, head `7d096a8`):** `architect-r3-residual-context-blueprint.md` rewritten. Root cause of first R3: sparse-context regression + R3-B mis-wired as unary. Fix: R3-B Golomb-Rice-through-binary using already-computed `CarcCtx.k` -> constant `cmarc_bins_per_ctx()=35`; **neutral `CMARC_PRIOR=2048`**; R3-A residual DIFF context capped <=365 ids; per-image winner-selection flag so a regression can never ship.

## In flight

- **Builder (continue, PR #83, run 32148908053 build job in_progress since 14:32; owner 2nd `/oc continue` run 32149962340 queued behind it):** implementing corrected R3 (R3-B Rice-through-binary + neutral prior first, then R3-A bounded residual context, then R3-C run mode); will re-measure on REAL Kodak effort-4 at full effort / highest-quality vs WebP, PNG, JPEG XL (+ other relevant codecs) per the owner's 14:42 directive. Keep all seams OFF by default; keep never-expand safety net; per-image winner-selection flag must prevent any regression from shipping. NOT re-dispatched this run (already in flight).
- **Factory (re-dispatched this run, `/oc factory` on #68):** durably commit `obsidian/benchmarks/data/kodak/*.ppm` (24 PCD0992 Kodak PPMs) to `opencode/issue68-20260818070512` (NO new PR; push to existing branch) matching `kodak.sha256`, and harden `run_kodak.sh`. The prior attempt (run 32150104809) FAILED and opened duplicate PR #86 instead of landing the data; no Factory run is currently in flight, so this re-dispatch is not a duplicate.
- **PR #85 (Factory infra) - MERGED** (14:52:06Z, rebase, branch preserved). Model pins `mimo-v2.5-free` -> `hy3-free` across factory.yml/opencode-review.yml/opencode-test.yml now on `main`. Closes no issues; `small_model` in opencode.json stays `mimo-v2.5-free` (free, no CreditsError).

## PENDING (deferred to a quiet run)

- **Factory hardening (one-PR rule):** dispatch the Factory Engineer to harden the workflow/agent so it NEVER opens a new PR for an issue that already has an open Obsidian/codec PR; it must reuse/push to the existing branch. Deferred to honor the owner's explicit "stop opening new PRs" instruction (a factory fix PR would itself be a new PR).
- **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive).

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `main` workflow agent steps (factory/review/test) now pin `opencode/hy3-free` (via merged PR #85). `opencode.json` `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free; `mimo-v2.5-free` still listed at opencode.ai/zen/v1/models). After merge, all agent steps run on `hy3-free` while `small_model` stays `mimo-v2.5-free`.
- **Mergeability:** PR #83 OPEN, head `7d096a8` = main (`30fd150`) + 1 commit, valid merge base, `mergeable: MERGEABLE` (UNSTABLE). PR #85 MERGED. `--rebase` possible once target met.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Factory (re-dispatched this run, on #68):** durably commit `obsidian/benchmarks/data/kodak/*.ppm` (matching `kodak.sha256`) to `opencode/issue68-20260818070512` (no new PR); harden `run_kodak.sh` (fail fast + sha256 verify). Confirm it reproduces JXL 8.7062 / WebP 9.6130 / JLS 9.7113 / PNG 13.0518.
2. **Builder (in flight, PR #83, run 32148908053 + queued 32149962340):** implement corrected R3 (R3-B -> R3-A -> R3-C -> R2.4), re-measure on REAL (now-durable) Kodak effort-4 at full effort / highest-quality vs WebP, PNG, JPEG XL (+ other relevant codecs) per the owner's 14:42 directive. Keep all seams OFF by default; keep never-expand safety net; per-image winner-selection flag must prevent any regression from shipping.
3. **After R3 build:** if gates still unmet on real Kodak, re-engage Researcher/Architect (existing PR only) for a true QM-class adaptive arithmetic coder - do NOT autopilot with bare `continue`.
4. **PR #85: DONE** (merged this run; no further action - lab-infra, closed no issues).
5. **Merge gate (only when met AND reproducible AND main repaired):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact, reproducible). Then merge (branch preserved per owner directive), close #68.
6. **Verify README + index.html** still promote Obsidian as Current on every Obsidian advance.

## Open questions

- **The decisive blocker is being closed (again):** `data/kodak/*.ppm` is not yet in git on the Obsidian branch, so the 10.0906 bpp "real Kodak" number is not reproducible and no further gate measurement is possible. The Factory (re-dispatched this run) must durably commit the PPMs to the existing branch. Prior Factory attempts (run `160`/PR #84, run 32148116537/PR #85, run 32150104809/failed) did not durably land the data.
- **Will corrected R3 clear the WebP (9.61) / JPEG XL (8.71) gates on real Kodak?** The neutral `CMARC_PRIOR` + Rice-through-binary + bounded DIFF context is designed to avoid the sparse-context regression; the Builder will measure it this run against the owner's full-effort / highest-quality benchmark set. If it still stalls above 9.71 (JPEG-LS), a true QM-class adaptive arithmetic backend is the remaining path.
- **Mergeability (RESOLVED):** PR #83 head `7d096a8` = main + 1 commit, valid merge base, MERGEABLE. PR #85 MERGED.
- **One-PR integrity (RESOLVED):** #83 is the sole canonical Obsidian PR; the Factory pushes data to it, never opens a codec PR. #85 was the legitimate infra PR (now merged); #86 was a redundant duplicate (closed).
- Will the Architect-on-PR (Mode 2) -> continue loop converge to a competitive codec without fracturing into multiple PRs? Hazard mitigated by targeting only the existing PR.

- Mae, the Maintainer
