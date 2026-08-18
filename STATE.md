# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~14:40Z, maintainer run 32149533030, owner `/oc maintainer` on PR #83 at 14:38:03Z). **NEW ROOT CAUSE FOUND:** the real-Kodak measurement gap is caused by `obsidian/.gitignore` containing `benchmarks/data/kodak/`, which excludes the Kodak PPMs from git - so every prior Factory data-provisioning attempt only ever committed `kodak.sha256` + `run_kodak.sh` and the PPMs never landed (confirmed on both the #83 and the closed #84 branches). The "10.0906 bpp" number was produced from transient, uncommitted PPMs and is NOT reproducible. Dispatched the Factory (this run) to remove that `.gitignore` exclusion and force-add the 24 Kodak PPMs durably to the existing #83 branch (no new PR), then harden `run_kodak.sh`. A Builder run (32148908053) is in_progress on #83 implementing the corrected R3 blueprint (head `7d096a8`); once the data lands I resume via `continue` to measure R3 for real.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`.
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE

- **Mergeability RESOLVED (durable).** PR #83 head `7d096a87fc57bbc716ebd3f604889a43f5e03a57` = `main` (`30fd150`) + 1 commit (the corrected-R3 Architect commit), valid merge base `30fd150`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. `--rebase` of #83 is possible once the target is met. (The Factory's earlier squash-rebase via PR #84 established the shared history; #84 is now CLOSED as the redundant duplicate.)
- **Measurement blocker - ROOT CAUSE NOW KNOWN:** `obsidian/.gitignore` contains `benchmarks/data/kodak/`, so the Kodak PPMs are git-excluded and were NEVER durably committed by any Factory run (only `kodak.sha256` + `run_kodak.sh` + a results CSV landed). The real-Kodak gate is therefore non-reproducible. The Factory dispatched this run must remove that gitignore line and force-add the 24 PCD0992 PPMs to the existing #83 branch.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z).
- **M1/M2/M2.5/M3/R1-R2.4 BUILT OFF-by-default** on #83; production unchanged at ~10.16 bpp (PNG 13.05 MET).
- **Last trustworthy real-Kodak effort-4 = 10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.48; JPEG XL 8.71 MISSED by 1.38) - but NON-reproducible until `data/kodak/*.ppm` is durably committed (Factory in flight this run).
- **CMARC RESEARCH DELIVERED** + **CMARC ARCHITECT BLUEPRINT** + **R3 CORRECTED ARCHITECT BLUEPRINT** (head `7d096a8`, 14:29:23Z): R3-A bounded residual DIFF context (sign-symmetric LUT, capped ids) + R3-B Rice-through-binary using `CarcCtx.k` (constant `cmarc_bins_per_ctx()=35`) + neutral `CMARC_PRIOR=2048` + R3-C JPEG-LS run mode; per-image winner-selection flag so a regression never ships. Build order R3-B->R3-A->R3-C->R2.4. Gates WebP 9.61 / JPEG XL 8.71.

## In flight

- **Builder (opencode run `32148908053`, in_progress since 14:31:59Z, owner `/oc continue` at 14:31:56Z):** implementing the corrected R3 blueprint on PR #83 branch `opencode/issue68-20260818070512`. Head still `7d096a8` (no push yet). Without `data/kodak` it will fall back to synthetic proxies and likely revert (as before); once the Factory lands the PPMs, the next `continue` can measure for real.
- **Factory (dispatched THIS run, `factory` on #68):** remove `benchmarks/data/kodak/` from `obsidian/.gitignore`, force-add + durably commit the 24 Kodak PPMs to the existing #83 branch (no new PR), harden `run_kodak.sh`, confirm reference baseline reproduction. NOT a duplicate (no factory currently in flight).

## PENDING (deferred to a quiet run)

- **Factory hardening (one-PR rule):** dispatch the Factory Engineer to harden the workflow/agent so it NEVER opens a new PR for an issue that already has an open Obsidian/codec PR; it must reuse/push to the existing branch. Deferred to honor the owner's explicit "stop opening new PRs" instruction (a factory fix PR would itself be a new PR).
- **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive).

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.
- **#79 / #81 / #82** - factory/infra and M0 PRs (merged). **#84** - closed erroneous duplicate (Factory rebase rebase-obsidian branch); content mirrored in #83.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2-free`. No CreditsError expected.
- **Mergeability:** PR #83 OPEN, head `7d096a8` = main (`30fd150`) + 1 commit, valid merge base `30fd150`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. `--rebase` possible once target met.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Factory (dispatched this run, #68):** remove `benchmarks/data/kodak/` from `obsidian/.gitignore`; durably force-add + commit the 24 Kodak PPMs into `obsidian/benchmarks/data/kodak/` on the EXISTING branch `opencode/issue68-20260818070512` (no new PR); harden `run_kodak.sh` (fail fast + sha256 verify). Confirm it reproduces JXL 8.7062 / WebP 9.6130 / JLS 9.7113 / PNG 13.0518.
2. **Builder (resume via `continue` after data lands):** implement corrected R3 (R3-B Rice-through-binary + neutral `CMARC_PRIOR` first, then R3-A bounded residual context, then R3-C run mode); re-measure on REAL (now-durable) Kodak effort-4. Keep all seams OFF by default; keep never-expand safety net; per-image winner-selection flag must prevent any regression from shipping.
3. **After R3 build:** if gates still unmet on real Kodak, re-engage Researcher/Architect (existing PR only) for a true QM-class adaptive arithmetic coder - do NOT autopilot with bare `continue`.
4. **Merge gate (only when met AND reproducible AND main repaired):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact, reproducible). Then merge (branch preserved per owner directive), close #68.
5. **Verify README + index.html** still promote Obsidian as Current on every Obsidian advance.

## Open questions

- **The decisive blocker has a known root cause now:** `obsidian/.gitignore` excludes `benchmarks/data/kodak/`, so the PPMs were never committed and the 10.0906 bpp "real Kodak" number is not reproducible. The Factory (this run) removes that exclusion and force-adds the PPMs to #83's branch. Once landed, R3 becomes verifiable against the actual gate.
- **Will corrected R3 clear the WebP (9.61) / JPEG XL (8.71) gates on real Kodak?** The neutral `CMARC_PRIOR` + Rice-through-binary + bounded DIFF context is designed to avoid the sparse-context regression that broke the first R3; the Builder will measure it once real data lands. If it still stalls above 9.71 (JPEG-LS), a true QM-class adaptive arithmetic backend is the remaining path.
- **Mergeability (RESOLVED):** branch `7d096a8` = main + 1 commit, valid merge base, MERGEABLE.
- **One-PR integrity (RESOLVED):** #83 is the sole canonical Obsidian PR; #84 is CLOSED as the redundant duplicate. The Factory pushes data to #83, never opens a codec PR.
- Will the Architect-on-PR (Mode 2) -> continue loop converge to a competitive codec without fracturing into multiple PRs? Hazard mitigated by targeting only the existing PR.

- Mae, the Maintainer
