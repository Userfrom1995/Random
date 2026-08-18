# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~14:49Z, maintainer run 32150606698, owner `/oc factory` flurry on #68 at 14:43-14:48Z). **DECISIONS:** (1) Routed `review` on PR #85 (model-upgrade infra, head `50c6461`) so it can be approved and merged via owner-PAT (App token cannot push workflow files). (2) Confirmed duplicate PR #86 ("Models upgraded, need manual push to main") is CLOSED - it carried the identical 3-file workflow change as #85 and wrongly said "Closes #68". (3) Deferred the durable Kodak-data re-provisioning: the Builder (run `32149962340`) is in flight on the SAME canonical branch `opencode/issue68-20260818070512`, so pushing data commits now risks a non-fast-forward collision with its pending push. Re-dispatch the Factory for the data NEXT run, after the Builder frees the branch.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`.
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (measurement BLOCKER re-open)

- **Mergeability RESOLVED.** PR #83 head `7d096a87fc57bbc716ebd3f604889a43f5e03a57` = `main` (`30fd150`) + 1 commit, valid merge base `30fd150`, `mergeable: MERGEABLE`, `mergeStateStatus: UNSTABLE` (behind base, no conflict). `--rebase` of #83 is possible once the target is met.
- **MEASUREMENT BLOCKER RE-OPEN:** `obsidian/benchmarks/data/kodak/*.ppm` is NOT committed on the canonical branch (only `obsidian/benchmarks/data/kodak.sha256` was once present and is ALSO now absent at head `7d096a87`). The 10.0906 bpp real-Kodak number from run ~13:15Z used transient PPMs that were wiped by a later history reset; it is not reproducible today. No gate is measurable right now. The Factory's repeated `factory` dispatches (this run's 14:43-14:48Z owner comments) kept producing workflow-model PRs (#85/#86) and never durably landed the PPMs to this branch.
- **Deferred data task:** the Factory will durably commit the 24 PCD0992 Kodak PPMs to `opencode/issue68-20260818070512` (NO new PR) and harden `run_kodak.sh` to be self-sufficient (download + sha256-verify if absent) - NEXT run, after the in-flight Builder frees the branch.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `7d096a87`). Last trustworthy real-Kodak effort-4 = **10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.48; JPEG XL 8.71 MISSED by 1.38). That number is currently NON-reproducible (data/kodak absent).
- **CMARC RESEARCH DELIVERED** (`obsidian/docs/research-breakthrough.md`): the ~10.1 bpp ceiling is the single-k/per-(cid,bin) coder, not the image; JPEG-LS reaches 9.71 bpp on the SAME Kodak corpus with the SAME LOCO-I GAP predictor but a context-based arithmetic (QM) coder.
- **CMARC ARCHITECT BLUEPRINT DELIVERED** (`obsidian/docs/architect-cmarc-blueprint.md`): CMARC as `entropy_mode` values (CARC=2, CARC_LZ=3, CARC_MIX=4).
- **CMARC BUILT END-TO-END (R1 -> R2.4), all OFF by default.** Production stays byte-identical to v1 GR. 106 lib tests pass.
- **R3 CORRECTED BLUEPRINT DELIVERED** (`architect-r3-residual-context-blueprint.md`): R3-A residual DIFF context capped <=365 ids; R3-B Golomb-Rice-through-binary using already-computed `CarcCtx.k`; neutral `CMARC_PRIOR` safety net; per-image winner-selection flag so a regression can never ship.

## In flight

- **Builder (continue, PR #83, run 32149962340, pending/started 14:42:17Z):** implementing corrected R3 (R3-B Rice-through-binary + neutral prior first, then R3-A bounded residual context, then R3-C run mode) on the canonical branch. It will attempt the real-Kodak measurement, but `data/kodak` is absent on the branch so its measurement will be on transient data (non-reproducible). DO NOT push data to this branch while it is in flight (non-fast-forward collision risk).
- **PR #85 (Factory infra, head `50c6461`, OPEN, MERGEABLE):** review/test/factory workflow agent models `mimo-v2.5-free` -> `hy3-free` (both free; `small_model` in opencode.json stays `mimo-v2.5-free`). Body correctly does NOT close #68 (I fixed it two runs ago). Queued for `review` THIS run; I merge next run once approved (lab-infra PR, shipping limit N/A; lands via owner-PAT since App token cannot push workflow files).
- **PR #86 (duplicate of #85): CLOSED.** Harmful "Closes #68" body + identical workflow change; superseded by #85.

## PENDING (deferred to a quiet run)

- **Factory hardening (one-PR rule):** dispatch the Factory Engineer to harden the workflow/agent so it NEVER opens a new PR for an issue that already has an open Obsidian/codec PR; it must reuse/push to the existing branch. Deferred to honor the owner's explicit "stop opening new PRs" instruction (a factory fix PR would itself be a new PR).
- **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive).
- **Durable Kodak-data re-provisioning** (this run's deferred task): Factory commits 24 PCD0992 PPMs to `opencode/issue68-20260818070512` (no new PR) + self-sufficient `run_kodak.sh`; NEXT run, after Builder frees the branch.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). PR #85 switches workflow `.yml` agent steps (factory/review/test) from `mimo-v2.5-free` to `hy3-free` - both free, no CreditsError. After merge, those agent steps run on `hy3-free` while `small_model` stays `mimo-v2.5-free`.
- **Mergeability:** PR #83 OPEN, head `7d096a87` = main (`30fd150`) + 1 commit, valid merge base, `mergeable: MERGEABLE` (UNSTABLE). PR #85 OPEN, head `50c6461`, MERGEABLE.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Wait for Builder run `32149962340` to finish** (do not disrupt). Re-survey its push + measurement next run.
2. **NEXT run (after Builder frees branch): re-dispatch `factory` on #68** to durably commit `obsidian/benchmarks/data/kodak/*.ppm` (24 PCD0992 Kodak PPMs, matching `kodak.sha256`) to `opencode/issue68-20260818070512` (NO new PR) and harden `run_kodak.sh` (self-sufficient: download + sha256-verify if absent; fail fast). Confirm it reproduces JXL 8.7062 / WebP 9.6130 / JLS 9.7113 / PNG 13.0518.
3. **Merge PR #85** once the Reviewer approves (lab-infra PR; lands workflow model upgrade via owner-PAT; closes no issues).
4. **After R3 build + reproducible data:** re-measure Obsidian on REAL (now-durable) Kodak at full effort / highest-quality vs WebP, PNG, JPEG XL (+ other relevant codecs) per the owner's 14:42 directive. If gates still unmet, re-engage Researcher/Architect (existing PR only) for a true QM-class adaptive arithmetic coder - do NOT autopilot with bare `continue`.
5. **Merge gate (only when met AND reproducible AND main repaired):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact, reproducible). Then merge (branch preserved per owner directive), close #68.
6. **Verify README + index.html** still promote Obsidian as Current on every Obsidian advance.

## Open questions

- **The decisive blocker is re-open:** `data/kodak/*.ppm` is not in git on the canonical branch, so the 10.0906 bpp "real Kodak" number is not reproducible and no further gate measurement is possible. The Factory must durably commit the PPMs to the existing branch (deferred to next run to avoid colliding with the in-flight Builder).
- **Will corrected R3 clear the WebP (9.61) / JPEG XL (8.71) gates on real Kodak?** The neutral `CMARC_PRIOR` + Rice-through-binary + bounded DIFF context is designed to avoid the sparse-context regression; the in-flight Builder (run `32149962340`) will measure it - but on transient data, so the result must be re-confirmed after the durable data lands.
- **Mergeability (RESOLVED):** PR #83 head `7d096a87` = main + 1 commit, valid merge base, MERGEABLE. PR #85 MERGEABLE.
- **One-PR integrity (RESOLVED):** #83 is the sole canonical Obsidian PR. PR #86 (duplicate) is CLOSED. PR #85 is a separate, legitimate infra PR (workflow models) that does not close #68.
- Will the Architect-on-PR (Mode 2) -> continue loop converge to a competitive codec without fracturing into multiple PRs? Hazard mitigated by targeting only the existing PR.

- Mae, the Maintainer
