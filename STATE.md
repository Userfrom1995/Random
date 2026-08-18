# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~14:04Z, maintainer run 32146078029, event: owner `/oc maintainer` on PR #83 asking why #83 and #84 were both closed and to stop opening new PRs). **CRITICAL STATE BREAK FOUND AND FIXED THIS RUN:** both PR #83 and PR #84 were CLOSED (no open Obsidian PR), which violated the owner's ONE-PR directive. Root cause: PR #84 was an erroneous Factory infra PR (run `160`) that opened a SECOND PR for #68; then a race between two co-running steps closed both. I **reopened PR #83** as the single canonical Obsidian PR (branch `opencode/issue68-20260818070512`, head `89891e8`, 1 commit ahead of `main` `30fd150`, valid merge base, rebase-mergeable). The Builder's R3 implementation run (`509`) is still in flight on that branch, so work continues. **REAL KODAK = 10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.48 bpp; JPEG XL 8.71 MISSED by 1.38 bpp).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. (PR #78's branch is already gone; preserve all others.)
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. **REINFORCED this run:** a Factory infra PR (#84) for #68 was an error; the Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must reuse the existing one.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Do NOT autopilot with bare `/oc continue`. Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. The Researcher/Architect auto-chain is DANGEROUS here because it would open a second codec PR - so they are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE BREAK - RESOLVED (this run, durably enough for iteration)

- PR #83 was CLOSED at 13:58:10Z and PR #84 was CLOSED at 13:59:10Z, leaving **zero open Obsidian PRs** (a violation of override #1). Cause: Factory run `160` opened PR #84 (a second PR for #68) to repair the orphan-`main` history break; then a race between two maintainer/factory steps each closed the "other" PR as redundant, closing both.
- **Fixed this run:** `gh pr reopen 83` restored PR #83 as the single canonical Open PR. Verified: head `opencode/issue68-20260818070512` = `89891e8` (main `30fd150` + 1 commit), merge base `30fd150` valid, rebase-mergeable. PR #84 remains CLOSED (correct - it was the erroneous duplicate).
- `main` is still the orphan `30fd150` until PR #84 merges, but a valid merge base now exists so `--rebase` of PR #83 is possible whenever the target is met. PR #84 should stay closed and be deleted once its `main`-history content is subsumed by #83's branch (its squash is already mirrored in #83's single head commit `89891e8`).

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z).
- **M1 OPEN as PR #83** (single canonical PR, reopened this run, branch `opencode/issue68-20260818070512`). Real Kodak effort-4 (trustworthy): **10.0906 bpp mean** with the never-expand best-backend selection. PNG gate (13.05) **MET**; WebP (9.61) + JPEG XL (8.71) **PENDING / STILL UNMET**.
- **M2 / M2.5 / M3-A / M3-B / M3.5 IMPLEMENTED, all OFF by default**, all regress/tie v1 GR on photographic content; production baseline 10.1556 bpp (v1 GR).
- **CMARC RESEARCH DELIVERED** (`obsidian/docs/research-breakthrough.md`): the ~10.1 bpp "floor" is the ceiling of the single-k per-context GR symbol coder, not the image; JPEG-LS reaches 9.71 bpp on the same Kodak corpus with the same LOCO-I GAP predictor but a context-based arithmetic coder.
- **CMARC ARCHITECT BLUEPRINT DELIVERED** (`obsidian/docs/architect-cmarc-blueprint.md`): CMARC as `entropy_mode` values (CARC=2, CARC_LZ=3, CARC_MIX=4), not a header flag.
- **CMARC BUILT END-TO-END (R1 -> R2.4), all OFF by default.** Production stays byte-identical to v1 GR. 106 lib tests pass.
- **REAL KODAK MEASUREMENT:** `obsidian/benchmarks/results/2026-08-18-real-kodak-2.csv` - 10.0906 bpp mean. Confirms CMARC/R2 plateaued ~0.38 bpp above JPEG-LS (9.71) on the SAME predictor. Entropy backend / pipeline integration is the proven bottleneck.
- **R3 ARCHITECT BLUEPRINT DELIVERED** (`obsidian/docs/architect-r3-residual-context-blueprint.md`): diagnosis = CMARC conditions on spatial-gradient context (predictor selection) instead of quantized neighboring residuals (JPEG-LS DIFF context), plus R2 dropped the geometric quotient for fixed-width binary. Design R3-A (residual-context conditioning, ~9.4-9.7 bpp, clears WebP), R3-B (Rice-through-binary), R3-C (run mode), R2.4 re-tuned.
- **R3 BUILDER IMPLEMENTATION IN FLIGHT** (run `509`, in_progress as of 14:04Z) on the reopened PR #83 branch. Not yet measured on real Kodak.

## In flight

- **PR #83 (single canonical Obsidian PR, REOPENED this run):** Review APPROVED (07:52Z). Tester PASSED (07:55Z). Full CMARC stack R1-R2.4 IMPLEMENTED on-branch (all OFF-by-default). R3 blueprint DELIVERED. **REAL KODAK MEASURED = 10.0906 bpp mean** (PNG MET; WebP 9.61 + JPEG XL 8.71 UNMET). **Builder R3 implementation IN FLIGHT**: opencode run `509` (in_progress) + run `512` (in_progress) building R3-A/B/C on `opencode/issue68-20260818070512`. Reopening #83 re-attaches the review/test loop; no new `continue` needed (would duplicate).
- **Factory run `160` (PR #84):** main-history repair DONE (branch now mergeable onto main); remaining subtask `data/kodak` provisioning (+ `.sha256`). PR #84 is now CLOSED (erroneous duplicate) - its content is already mirrored in #83's head `89891e8`, so no further action on #84 is needed beyond leaving it closed.

## PENDING (deferred to a quiet run)

- **Factory hardening (one-PR rule):** dispatch the Factory Engineer to harden the workflow/agent so it NEVER opens a new PR for an issue that already has an open Obsidian/codec PR; it must reuse the existing PR. Deferred this run to honor the owner's explicit "stop opening new PRs" instruction (a factory fix PR would itself be a new PR).

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.
- **#71** - DELETED. Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.
- **#79 / #81 / #82 / #84** - factory/infra and M0 PRs; #84 is the closed erroneous duplicate.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2-free`. No CreditsError expected.
- **Mergeability:** PR #83 REOPENED, head `89891e8` = main (`30fd150`) + 1 commit, valid merge base `30fd150`, rebase-mergeable. PR #84 CLOSED (duplicate). `--rebase` of #83 possible once target met.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Builder (via in-flight run `509`/`512`, NO new trigger this run):** implement R3-A (residual-context `residual_context(dL,dU,dUl)` as the CMARC coding context), re-benchmark REAL Kodak effort-4; then R3-B (Rice-through-binary) and R3-C (run mode). Measure each against WebP 9.61 / JPEG XL 8.71 on real data. Keep all prior seams OFF by default; keep never-expand safety net.
2. **After R3 build:** if gates still unmet on real Kodak, re-engage Researcher/Architect (existing PR #83 only) for a stronger marginal/context signal (true QM-class adaptive arithmetic coder) - do NOT autopilot with bare `continue`.
3. **Factory hardening (PENDING, quiet run):** harden the one-PR rule so the Factory never opens a redundant codec PR; reuse the existing open PR.
4. **Merge gate (only when met AND main repaired):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact). Then merge (branch preserved per owner directive), close #68.
5. **Verify README + index.html** still promote Obsidian as Current on every Obsidian advance.
6. **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive). Dispatch Factory when pipeline is quiet.

## Open questions

- **THE decisive number is known:** real Kodak = 10.0906 bpp mean. CMARC/R2 plateaued ~0.38 bpp above JPEG-LS (9.71) on the SAME predictor. The Architect's R3 diagnosis: CMARC conditions on the wrong context (spatial gradient, not quantized neighbor residuals), and R2 dropped the geometric quotient for fixed-width binary - both fixed by R3-A/B/C.
- **Next breakthrough:** can R3 (residual-context conditioning + Rice-through-binary + run mode) close the ~0.38->1.38 bpp gap to WebP/JPEG XL on the SAME residuals? JPEG-LS (9.71) / WebP (9.61) / JPEG XL (8.71) prove ~9.4-9.7 is reachable; R3-A alone is projected to reach ~9.4-9.7 bpp and clear WebP, with R3-B/C + re-tuned R2.4 aiming at JPEG XL. R3 is being built and will be measured on real Kodak by in-flight run `509`.
- **One-PR integrity (RESOLVED this run):** #83 reopened as the sole canonical Obsidian PR; #84 closed. Root cause (Factory spawning a 2nd PR) logged as a PENDING factory fix, deferred to avoid opening more PRs.
- **Mergeability (RESOLVED):** branch `opencode/issue68-20260818070512` = main + 1 commit, valid merge base `30fd150`; rebase-merge possible once target met.
- **Measurement gap (CLOSED earlier):** `data/kodak` provisioned; real Kodak now measurable.
- Will the Architect-on-PR -> continue loop converge to a competitive codec without fracturing into multiple PRs? Hazard mitigated by reopening only #83 and hardening the Factory to never duplicate.

- Mae, the Maintainer
