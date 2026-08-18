# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~13:55Z, maintainer run 32145145967, event: owner `/oc maintainer` on PR #83). PR #83 (the single canonical Obsidian PR) is OPEN on `opencode/issue68-20260818070512`, head `89891e84f9934f5887c0a97fe8495704f62e6c4b`. **REAL KODAK = 10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.48 bpp; JPEG XL 8.71 MISSED by 1.38 bpp). CMARC/R2 (R1->R2.4) built, all OFF by default, production byte-identical to v1 GR (10.1556). R3 blueprint (residual-context conditioning) delivered by the Architect. **The orphan-`main` break is RESOLVED durably**: the Factory's squash-rebase (run `160`, PR #84) put the full codec (M0-R3) onto `main`'s history, so `main` is now an ancestor of the branch and PR #83 is MERGEABLE (1 commit ahead, no conflict). The Builder is implementing R3 (runs 509 in_progress + 510 queued); the Factory run `160` is still provisioning `data/kodak`.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. (PR #78's branch is already gone; preserve all others.)
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Do NOT autopilot with bare `/oc continue`. Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. The Researcher/Architect auto-chain is DANGEROUS here because it would open a second codec PR - so they are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE BREAK - RESOLVED (durably)

- The Factory run `160` (PR #84 `opencode/factory-68-rebase-obsidian`, "[Infra] Factory update for #68") squash-rebased the entire Obsidian codec history (M0-R3) onto `main` (`30fd150`). Verified: `git merge-base origin/main opencode/issue68-20260818070512` == `30fd150` (NOT empty); `main` IS an ancestor of the branch; branch is exactly **1 commit ahead** of main (`89891e84` = "factory: rebase Obsidian codec (M0-R3) onto main - squash of PR #83 orphan branch"); `gh pr view 83` -> `mergeable: MERGEABLE` (mergeStateStatus UNSTABLE = behind base, no conflict). The earlier orphan break (caused when a direct `git push` to `main` was rejected by branch protection, re-orphaning it) is FIXED via a PR-based path. A valid merge base now exists, so `gh pr merge --rebase` is possible again.
- PR #84 itself remains OPEN + MERGEABLE; it will be handled by the normal review/merge pipeline (it is a bot infra PR - merges only after Reviewer approval, like all PRs). Its `data/kodak` provisioning subtask is still in flight.
- `main` is still the orphan `30fd150` until PR #84 merges, but that no longer blocks `--rebase` of PR #83.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z, commit `eee5a31`): GR entropy backend, 53/53 tests pass, no expansion.
- **M1 OPEN as PR #83** (canonical single PR, branch `opencode/issue68-20260818070512`). Real Kodak effort-4 (trustworthy): **10.0906 bpp mean** with the never-expand best-backend selection (CMARC/R2 wins only where it beats v1 GR; net ~0.07 bpp below the 10.1556 v1 GR baseline). PNG gate (13.05) **MET**; WebP (9.61) + JPEG XL (8.71) **PENDING / STILL UNMET**.
- **M2 / M2.5 / M3-A / M3-B / M3.5 IMPLEMENTED, all OFF by default**, all regress/tie v1 GR on photographic content; production baseline 10.1556 bpp (v1 GR).
- **CMARC RESEARCH DELIVERED (11:01Z, run 32129298608):** `obsidian/docs/research-breakthrough.md`. The ~10.1 bpp "floor" is the ceiling of the single-k per-context Golomb-Rice *symbol* coder, not the image. JPEG-LS reaches 9.71 bpp on the same Kodak corpus with the same LOCO-I GAP predictor but a context-based arithmetic (QM) coder - proof the predictor is sound and the entropy backend is the bottleneck.
- **CMARC ARCHITECT BLUEPRINT DELIVERED (11:07Z, run 32129665095):** `obsidian/docs/architect-cmarc-blueprint.md`. CMARC is a new `ModelConfig.entropy_mode` value (`ENTROPY_MODE_CARC=2`, `CARC_LZ=3`, `CARC_MIX=4`), NOT a header flag.
- **CMARC BUILT END-TO-END (R1 -> R2.4), all OFF by default:** R1 binary range coder; R2 cross-bit conditioning; R2.1 subtract-green; R2.2 expanded predictor bank (ids 8..=16); R2.3 CMARC-LZ (dormant); R2.4 logistic mixing (dormant). Production stays byte-identical to v1 GR. 106 lib tests pass.
- **REAL KODAK MEASUREMENT (2026-08-18 ~13:15Z):** `obsidian/benchmarks/results/2026-08-18-real-kodak-2.csv` - 10.0906 bpp mean. Confirms CMARC/R2 did NOT clear WebP (9.61); it sits at the ~10.1 floor, ~0.38 bpp above JPEG-LS (9.71) on the SAME predictor. The entropy backend / pipeline integration is the proven bottleneck.
- **R3 ARCHITECT BLUEPRINT DELIVERED (13:32Z, run 32142354868):** `obsidian/docs/architect-r3-residual-context-blueprint.md`, committed on the branch (squashed into `89891e84`). Diagnosis: (1) PRIMARY (~0.38 bpp) - CMARC conditions on the spatial-gradient context (predictor selection), not on quantized neighboring *residuals* (JPEG-LS DIFF context), so per-(cid,bin) models average over heterogeneous residual scales; (2) SECONDARY - R2 replaced Rice/Exp-Golomb quotient with fixed-width MSB-first binary magnitude. Design: R3-A residual-context `residual_context(dL,dU,dUl)` as coding context (expected ~9.4-9.7 bpp, clears WebP); R3-B restore per-context Rice-through-binary-coder (`q=m>>k` geometric quotient + `k` remainder bits); R3-C JPEG-LS run mode; R2.4 re-tuned on the corrected context to reach JPEG XL.

## In flight

- **PR #83 (single canonical Obsidian PR):** Review APPROVED (07:52Z). Tester PASSED (07:55Z). Full CMARC stack R1-R2.4 IMPLEMENTED on-branch (all OFF-by-default). R3 blueprint DELIVERED (13:32Z, Architect run `32142354868`). **REAL KODAK MEASURED = 10.0906 bpp mean** (PNG MET; WebP 9.61 + JPEG XL 8.71 UNMET). **Builder R3 implementation IN FLIGHT**: opencode run `509` (in_progress, owner `/oc continue` 13:35:06Z) + opencode run `510` (queued, from prior maintainer run 32142951058 `continue`). So R3-A/B/C is being built on the single branch now; no new `continue` needed this run.
- **Factory:** run `160` (PR #84 `opencode/factory-68-rebase-obsidian`) STILL in_progress. Main-history repair DONE (branch now MERGEABLE onto main). Remaining subtask: provision `obsidian/benchmarks/data/kodak/` (+ `.sha256`) so R3 can be measured on REAL Kodak. Branch has 3 kodak references but only `kodak.sha256` is present locally (actual PPMs large/uncached), so the Builder's R3 measurement step may need to re-provision. Not re-dispatched this run (run `160` already in flight).

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.
- **#71** - DELETED. Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2-free`. No CreditsError expected.
- **Mergeability:** RESOLVED durably. `main` == `30fd150` (orphan); branch == `89891e84` = main + 1 squash commit; `main` IS an ancestor of branch; `gh pr view 83` -> `mergeable: MERGEABLE`. `--rebase` now possible. PR #84 open + mergeable (its own review/merge pipeline).
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Builder (via in-flight runs 509/510, NO new trigger this run):** implement R3-A (residual-context `residual_context(dL,dU,dUl)` as the CMARC coding context), re-benchmark REAL Kodak effort-4; then R3-B (Rice-through-binary: `q=m>>k` geometric quotient model + `k` remainder bits) and R3-C (run mode). Measure each against WebP 9.61 / JPEG XL 8.71 on real data (no longer synthetic proxies). Keep all prior seams OFF by default; keep never-expand safety net. Needs `data/kodak` (Factory run `160` provisioning).
2. **After R3 build:** if gates still unmet on real Kodak, re-engage Researcher/Architect (existing PR only) for a stronger marginal/context signal (true QM-class adaptive arithmetic coder) - do NOT autopilot with bare `continue`.
3. **Factory run `160`:** finish provisioning `data/kodak`; then PR #84 can be reviewed/merged to finalize `main` history. Do NOT re-dispatch (run already in flight).
4. **Merge gate (only when met AND main repaired):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact). Then merge (branch preserved per owner directive), close #68.
5. **Verify README + index.html** still promote Obsidian as Current on every Obsidian advance.
6. **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive). Dispatch Factory when pipeline is quiet.

## Open questions

- **THE decisive number is known:** real Kodak = 10.0906 bpp mean. CMARC/R2 plateaued ~0.38 bpp above JPEG-LS (9.71) on the SAME predictor. The Architect's R3 diagnosis: CMARC conditions on the wrong context (spatial gradient, not quantized neighbor residuals), and R2 dropped the geometric quotient for fixed-width binary - both fixed by R3-A/B/C.
- **Next breakthrough:** can R3 (residual-context conditioning + Rice-through-binary + run mode) close the ~0.38->1.38 bpp gap to WebP/JPEG XL on the SAME residuals? JPEG-LS (9.71) / WebP (9.61) / JPEG XL (8.71) prove ~9.4-9.7 is reachable; R3-A alone is projected to reach ~9.4-9.7 bpp and clear WebP, with R3-B/C + re-tuned R2.4 aiming at JPEG XL. R3 is now being built and will be measured on real Kodak.
- **Mergeability (RESOLVED durably):** Factory squash-rebase (run `160`, PR #84) put the full codec (M0-R3) onto `main`'s history; branch is 1 commit ahead of main and MERGEABLE. A valid merge base exists, so `--rebase` is possible.
- **Measurement gap (re-closing):** `data/kodak` still absent locally (only `.sha256`); Factory run `160` is provisioning it. R3's real-Kodak measurement depends on it landing before the Builder's measurement step.
- Will the Architect-on-PR -> continue loop converge to a competitive codec without fracturing into multiple PRs? Hazard mitigated by targeting only the existing PR.

- Mae, the Maintainer
