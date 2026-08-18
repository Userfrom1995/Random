# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~14:55Z, maintainer run 32151259649, triggered by PR #83 event + owner `/oc factory` flurry). **DECISIONS:** `[]` - no triggers fired. The Builder already pushed the corrected R3 implementation (head `7f76842`); the Factory is already in flight x2 (owner-fired at 14:53/14:54Z) to durably commit the Kodak PPMs, so re-dispatching `factory`/`continue` would be a duplicate and premature. Hold until the Factory lands data, then resume `continue` to re-measure R3 on REAL Kodak. No merge (gates unmet / non-reproducible).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: this is currently NOT satisfied (see Open questions) - flagged for a Builder/Factory pass, not a direct `main` edit by Mae.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (measurement BLOCKER still open)

- **Mergeability RESOLVED.** PR #83 head `7f7684219e77df3fa6941f310d407ed45226a71d` = `main` (`30fd150`) + clean commits (squash-rebase of M0-R3 codec + architect R3 blueprint + builder R3 implementation), valid merge base `30fd150`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. `--rebase` of #83 is possible once the target is met.
- **Measurement blocker STILL OPEN:** `obsidian/benchmarks/data/kodak/*.ppm` is NOT committed on the Obsidian branch (only `obsidian/benchmarks/data/kodak.sha256` exists, plus the stale results CSV `2026-08-18-real-kodak-2.csv` from the non-reproducible run). Real-Kodak gate measurement is impossible until the PPMs land. The owner re-fired `/oc factory` twice (14:53:33Z, 14:54:26Z) to durably commit the 24 Kodak PPMs to the EXISTING branch `opencode/issue68-20260818070512` and harden `run_kodak.sh`; two Factory runs are now in flight (`32151115174` in_progress, `32151205413` pending). No Mae-fired factory dispatch this run (would duplicate).

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `7f76842`). Last NON-reproducible real-Kodak effort-4 = **10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.48; JPEG XL 8.71 MISSED by 1.38). Reproducibility pending durable data/kodak.
- **CMARC RESEARCH DELIVERED** (`obsidian/docs/research-breakthrough.md`): the ~10.1 bpp ceiling is the single-k/per-(cid,bin) GR-style coder, not the image; JPEG-LS reaches 9.71 bpp on the SAME Kodak corpus with the SAME LOCO-I GAP predictor but a context-based arithmetic (QM) coder.
- **CMARC ARCHITECT BLUEPRINT DELIVERED** (`obsidian/docs/architect-cmarc-blueprint.md`): CMARC as `entropy_mode` values (CARC=2, CARC_LZ=3, CARC_MIX=4).
- **CMARC BUILT END-TO-END (R1 -> R2.4), all OFF by default.** Production stays byte-identical to v1 GR. 106 lib tests pass.
- **R3 CORRECTED BLUEPRINT DELIVERED (14:29:43Z, run `32148118020`):** `architect-r3-residual-context-blueprint.md`. Root cause of first R3: sparse-context regression + R3-B mis-wired as unary. Fix: R3-B Golomb-Rice-through-binary using `CarcCtx.k` -> constant `cmarc_bins_per_ctx()=35`; neutral `CMARC_PRIOR=2048`; R3-A residual DIFF context capped <=365 ids; per-image winner-selection flag.
- **R3 IMPLEMENTED & PUSHED (head `7f76842`, builder run in prior cycle):** R3-B (neutral prior + Rice-through-binary magnitude, 35 bins) and R3-A (residual DIFF context as CMARC coding context, capped, winner-selection flag). Cannot be validated yet (no data/kodak).

## In flight

- **Factory (owner-fired, in flight, NOT Mae-dispatched):** two runs (`32151115174` in_progress since 14:53:39Z, `32151205413` pending) to durably commit `obsidian/benchmarks/data/kodak/*.ppm` (24 PCD0992 Kodak PPMs) to `opencode/issue68-20260818070512` (NO new PR) matching `kodak.sha256`, and harden `run_kodak.sh`. Hazards: two near-simultaneous runs may race; both instructed to reuse the existing branch and never open a new PR. Mae will verify on next survey that the PPMs landed and no redundant PR appeared.
- **Builder R3: IMPLEMENTED, awaiting durable data to measure.** No Builder run in flight. Once Factory lands data, Mae resumes via `continue` to re-benchmark R3 on REAL Kodak effort-4 vs WebP/PNG/JPEG XL.

## PENDING (deferred to a quiet run)

- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Needs a Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Factory hardening (one-PR rule):** dispatch the Factory Engineer to harden the workflow/agent so it NEVER opens a new PR for an issue that already has an open Obsidian/codec PR; it must reuse/push to the existing branch. Deferred to honor the owner's explicit "stop opening new PRs" instruction.
- **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive).

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `main` workflow agent steps (factory/review/test) pin `opencode/hy3-free` (via merged PR #85). `opencode.json` `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free; `mimo-v2.5-free` still listed at opencode.ai/zen/v1/models).
- **Mergeability:** PR #83 OPEN, head `7f76842` = main (`30fd150`) + clean commits, valid merge base, `mergeable: MERGEABLE` (CLEAN). `--rebase` possible once target met.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Factory (owner in flight x2, NOT Mae-dispatched):** durably commit `obsidian/benchmarks/data/kodak/*.ppm` (matching `kodak.sha256`) to `opencode/issue68-20260818070512` (no new PR); harden `run_kodak.sh` (fail fast + sha256 verify). Verify on next survey: PPMs present, no redundant PR opened, branch still single.
2. **After data lands:** Mae fires `continue` on PR #83 -> Builder re-implements/measures R3 on REAL Kodak effort-4 vs WebP 9.61 / PNG 13.05 / JPEG XL 8.71 (+ other codecs) per owner directive. Keep all seams OFF by default; never-expand safety net; per-image winner-selection flag must prevent any regression from shipping.
3. **After R3 build:** if gates still unmet on real Kodak, re-engage Researcher/Architect (existing PR only) for a true QM-class adaptive arithmetic coder - do NOT autopilot with bare `continue`.
4. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
5. **Merge gate (only when met AND reproducible AND main repaired):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact, reproducible). Then merge (branch preserved per owner directive), close #68.

## Open questions

- **Measurement blocker (still open):** `data/kodak/*.ppm` is not yet in git on the Obsidian branch, so no real-Kodak gate measurement is possible. Owner re-fired Factory x2 (14:53/14:54Z); runs `32151115174` (in_progress) + `32151205413` (pending) must durably land the PPMs. Prior Factory attempts (run `160`/PR #84, run 32148116537/PR #85, run 32150104809/failed) did not durably land the data - this must finally stick.
- **Will corrected R3 clear the WebP (9.61) / JPEG XL (8.71) gates on real Kodak?** Neutral `CMARC_PRIOR` + Rice-through-binary + bounded DIFF context is designed to avoid the sparse-context regression; the Builder will measure it once data lands. If it still stalls above 9.71 (JPEG-LS), a true QM-class adaptive arithmetic backend is the remaining path.
- **Duplicate Factory race:** two in-flight Factory runs on the same branch could conflict. Both instructed to reuse the existing branch + no new PR; Mae will verify next survey.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **One-PR integrity (RESOLVED):** #83 is the sole canonical Obsidian PR; the Factory pushes data to it, never opens a codec PR. #85 was the legitimate infra PR (merged); #86 was a redundant duplicate (closed).

- Mae, the Maintainer
