# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~14:30Z, maintainer run 32148674683, owner `/oc maintainer` on PR #83 at 14:29:52Z). **NEW DECISION:** Architect delivered the CORRECTED R3 blueprint (head `7d096a8`, run `32148118020`, 14:29:43Z), fixing the sparse-context regression and geometric-quotient bug from the failed first R3. The Factory (`/oc factory` on #68, run `32148456266`, in_progress since 14:27:41Z) is durably committing the Kodak PPMs to the existing branch (`opencode/issue68-20260818070512`) and hardening `run_kodak.sh`. I resumed the Builder via `continue` (decision `[{"action":"continue","pr":83}]`) to implement the corrected R3 and re-measure on REAL Kodak once the Factory lands the data. The Builder run overlaps the Factory run, so the real-Kodak measurement should be possible by measure time. **REAL KODAK = 10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.48; JPEG XL 8.71 MISSED by 1.38) - still NON-reproducible until `data/kodak/*.ppm` is committed (Factory in flight).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`.
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (measurement BLOCKER being closed by in-flight Factory)

- **Mergeability RESOLVED.** PR #83 head `7d096a87fc57bbc716ebd3f604889a43f5e03a57` = `main` (`30fd150`) + 1 commit, valid merge base `30fd150`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. `--rebase` of #83 is possible once the target is met.
- **Measurement blocker being closed (Factory in flight):** `obsidian/benchmarks/data/kodak/*.ppm` is NOT yet committed to the repo (only `kodak.sha256` + `run_kodak.sh`). The earlier real-Kodak measurement (run ~13:15Z, 10.0906 bpp) used transient PPMs that were never committed, so it is not reproducible. The Factory run `32148456266` (since 14:27:41Z, `/oc factory` on #68) is durably committing the 24 PCD0992 Kodak PPMs to the existing branch and hardening `run_kodak.sh`. Once it lands, the gate becomes re-measurable.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`). Last trustworthy real-Kodak effort-4 = **10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED; JPEG XL 8.71 MISSED). That number is currently NON-reproducible (data/kodak absent, Factory in flight).
- **CMARC RESEARCH DELIVERED** (`obsidian/docs/research-breakthrough.md`): the ~10.1 bpp ceiling is the single-k/per-(cid,bin) GR-style coder, not the image; JPEG-LS reaches 9.71 bpp on the SAME Kodak corpus with the SAME LOCO-I GAP predictor but a context-based arithmetic (QM) coder.
- **CMARC ARCHITECT BLUEPRINT DELIVERED** (`obsidian/docs/architect-cmarc-blueprint.md`): CMARC as `entropy_mode` values (CARC=2, CARC_LZ=3, CARC_MIX=4).
- **CMARC BUILT END-TO-END (R1 -> R2.4), all OFF by default.** Production stays byte-identical to v1 GR. 106 lib tests pass.
- **R3 ATTEMPTED THEN REVERTED (14:18Z):** R3-A (165-context DIFF) regressed synthetic CARC ~14 -> ~28 bpp; R3-B mis-wired as unary; header/payload desync bug. Builder reverted ALL R3 to clean R2.4 baseline.
- **R3 CORRECTED BLUEPRINT DELIVERED (14:29:43Z, run `32148118020`, head `7d096a8`):** `architect-r3-residual-context-blueprint.md` rewritten. Root cause of first R3: `cmarc_write_residual` fixed-width MSB-first magnitude with `(position,window)` per-bin models -> ~66 bins/ctx; times DIFF context blows per-plane budget; rare-context `BinModel`s pinned at strong wrong prior `CMARC_PRIOR=64/4096` (step 48) cost ~6 bits/bin. Fix: R3-B Golomb-Rice-through-binary using already-computed `CarcCtx.k` -> constant `cmarc_bins_per_ctx()=35`; **neutral `CMARC_PRIOR=2048`** (starved context <=1 bit/bin); R3-A residual DIFF context capped <=365 ids via sign-symmetry LUT, no activity-class multiplication, per-image winner-selection flag so a regression can never ship. Build order R3-B->R3-A->R3-C->R2.4. Gates WebP 9.61 / JPEG XL 8.71.

## In flight

- **PR #83 (single canonical Obsidian PR, OPEN, MERGEABLE, head `7d096a8`):** Review APPROVED (07:52Z). Tester PASSED (07:55Z). Full CMARC R1-R2.4 stack BUILT (all OFF-by-default). R3 reverted then corrected-blueprint delivered. **Builder RESUMED via `continue` this run (decision `[{"action":"continue","pr":83}]`)** to implement corrected R3 and re-measure on REAL Kodak.
- **Factory (`/oc factory` on #68, run `32148456266`, in_progress since 14:27:41Z):** durably provision `obsidian/benchmarks/data/kodak/*.ppm` (commit to `opencode/issue68-20260818070512`, no new PR) + harden `run_kodak.sh`. NOT a duplicate (only one factory run in flight).
- **Architect (`/oc architect` on PR #83):** COMPLETED this run (corrected R3 blueprint delivered, head `7d096a8`). No re-fire.

## PENDING (deferred to a quiet run)

- **Factory hardening (one-PR rule):** dispatch the Factory Engineer to harden the workflow/agent so it NEVER opens a new PR for an issue that already has an open Obsidian/codec PR; it must reuse/push to the existing branch. Deferred to honor the owner's explicit "stop opening new PRs" instruction (a factory fix PR would itself be a new PR).
- **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive).

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.
- **#79 / #81 / #82 / #84** - factory/infra and M0 PRs; #84 is the closed erroneous duplicate.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2-free`. No CreditsError expected.
- **Mergeability:** PR #83 OPEN, head `7d096a8` = main (`30fd150`) + 1 commit, valid merge base `30fd150`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. `--rebase` possible once target met.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Factory (in flight, run `32148456266`):** durably commit `obsidian/benchmarks/data/kodak/*.ppm` to `opencode/issue68-20260818070512` (no new PR); harden `run_kodak.sh` (fail fast + sha256 verify). Confirm it reproduces JXL 8.7062 / WebP 9.6130 / JLS 9.7113 / PNG 13.0518.
2. **Builder (resumed via `continue` this run, PR #83):** implement corrected R3 (R3-B Rice-through-binary + neutral `CMARC_PRIOR` first, then R3-A bounded residual context, then R3-C run mode); re-measure on REAL (now-durable) Kodak effort-4 once Factory data lands. Keep all seams OFF by default; keep never-expand safety net; per-image winner-selection flag must prevent any regression from shipping.
3. **After R3 build:** if gates still unmet on real Kodak, re-engage Researcher/Architect (existing PR only) for a true QM-class adaptive arithmetic coder - do NOT autopilot with bare `continue`.
4. **Merge gate (only when met AND reproducible AND main repaired):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact, reproducible). Then merge (branch preserved per owner directive), close #68.
5. **Verify README + index.html** still promote Obsidian as Current on every Obsidian advance.

## Open questions

- **The decisive blocker is being closed:** `data/kodak/*.ppm` is not yet in git, so the 10.0906 bpp "real Kodak" number is not reproducible and no further gate measurement is possible. The Factory (run `32148456266`) is durably committing the PPMs to the existing branch. Once landed, R3 becomes verifiable against the actual gate.
- **Will corrected R3 clear the WebP (9.61) / JPEG XL (8.71) gates on real Kodak?** The neutral `CMARC_PRIOR` + Rice-through-binary + bounded DIFF context is designed to avoid the sparse-context regression; the Builder will measure it this run. If it still stalls above 9.71 (JPEG-LS), a true QM-class adaptive arithmetic backend is the remaining path.
- **Mergeability (RESOLVED):** branch `7d096a8` = main + 1 commit, valid merge base, MERGEABLE.
- **One-PR integrity (RESOLVED):** #83 is the sole canonical Obsidian PR; the Factory pushes data to it, never opens a codec PR.
- Will the Architect-on-PR (Mode 2) -> continue loop converge to a competitive codec without fracturing into multiple PRs? Hazard mitigated by targeting only the existing PR.

- Mae, the Maintainer
