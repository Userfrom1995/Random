# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~13:15Z, maintainer run 32141355314, event: owner `/oc maintainer` on PR #83 after the real-Kodak measurement landed). PR #83 (the single canonical Obsidian PR) is OPEN on `opencode/issue68-20260818070512`, head `d2324773e...` (commit "CARC ok manually; harness error hidden by 2>/dev/null. Re-run."). **THE DECISIVE REAL-KODAK MEASUREMENT IS NOW IN HAND.** File `obsidian/benchmarks/results/2026-08-18-real-kodak-2.csv` (24 images, effort 4): Obsidian best config (never-expand net picks CMARC/R2 where it wins) **= 10.0906 bpp mean**. Gates: PNG 13.05 MET; WebP 9.61 MISSED by 0.48 bpp (14/24 images above); JPEG XL 8.71 MISSED by 1.38 bpp (22/24 above). CMARC/R2 shaved only ~0.07 bpp off v1 GR (10.1556) and plateaued at the ~10.1 bpp residual-entropy floor. `data/kodak` is now PROVISIONED (the Builder ran `run_kodak.sh` successfully), so the measurement gap is CLOSED. The orphan-history infra break remains RESOLVED (main == branch tip). This run re-engages the Researcher (Mode 2) on PR #83 to diagnose the 10.09 plateau and design the next breakthrough toward WebP/JPEG XL.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. (PR #78's branch is already gone; preserve all others.)
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Do NOT autopilot with bare `/oc continue`. Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. The Researcher/Architect auto-chain is DANGEROUS here because it would open a second codec PR - so they are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE BREAK - RESOLVED (found ~11:08Z, FIXED ~13:00Z)

- `main` was a single orphan commit `30fd150873da6578c639ef1d569df4d948712aef` (1 commit, 586 files, no history). This orphaned every open PR branch and made `gh pr merge --rebase` impossible (no common ancestor). PR #83 reported `CONFLICTING` / `DIRTY`.
- **FIXED:** the Factory run `32139935703` restored `main`'s history by fast-forwarding `main` to the PR branch tip (then `2f49218`, now advanced to `d232477`). Verified live with `git`: `main` HEAD == branch HEAD; `merge-base` is the tip; 0 commits divergent. The branch re-links; rebase-merge is now possible. GitHub's `mergeable: CONFLICTING` flag is stale and will refresh on the next push.
- **Do NOT merge yet** for performance reasons (gate unmet) - but the mechanism no longer blocks.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z, commit `eee5a31`): GR entropy backend, 53/53 tests pass, no expansion.
- **M1 OPEN as PR #83** (canonical single PR, branch `opencode/issue68-20260818070512`). Real Kodak effort-4 (FIRST TRUSTWORTHY NUMBER, measured 2026-08-18 ~13:15Z): **10.0906 bpp mean** with the never-expand best-backend selection (CMARC/R2 wins only where it beats v1 GR; net ~0.07 bpp below the 10.1556 v1 GR baseline). PNG gate (13.05) **MET**; WebP (9.61) + JPEG XL (8.71) **PENDING / STILL UNMET**.
- **M2 / M2.5 / M3-A / M3-B / M3.5 IMPLEMENTED, all OFF by default**, all regress/tie v1 GR on photographic content; production baseline 10.1556 bpp (v1 GR).
- **CMARC RESEARCH DELIVERED (11:01Z, run `32129298608`):** `obsidian/docs/research-breakthrough.md`. The ~10.1 bpp "floor" is the ceiling of the single-k per-context Golomb-Rice *symbol* coder, not the image. JPEG-LS reaches 9.71 bpp on the same Kodak corpus with the same LOCO-I GAP predictor but a context-based arithmetic (QM) coder - proof the predictor is sound and the entropy backend is the bottleneck. Design: R1 (CMARC) clears WebP; R2 (subtract-green/color cache, expanded predictor bank, LZ77 re-woven, logistic mixing) targets JPEG XL.
- **CMARC ARCHITECT BLUEPRINT DELIVERED (11:07Z, run `32129665095`):** `obsidian/docs/architect-cmarc-blueprint.md`. CMARC is a new `ModelConfig.entropy_mode` value (`ENTROPY_MODE_CARC=2`, `CARC_LZ=3`, `CARC_MIX=4`), NOT a header flag.
- **CMARC BUILT END-TO-END (R1 -> R2.4), all OFF by default:** R1 binary range coder; R2 cross-bit conditioning; R2.1 subtract-green; R2.2 expanded predictor bank (ids 8..=16); R2.3 CMARC-LZ (dormant); R2.4 logistic mixing (dormant). Production stays byte-identical to v1 GR. 106 lib tests pass.
- **REAL KODAK MEASUREMENT (this run):** `obsidian/benchmarks/results/2026-08-18-real-kodak-2.csv` - 10.0906 bpp mean. Confirms CMARC/R2 did NOT clear WebP (9.61); it sits at the ~10.1 floor, ~0.38 bpp above JPEG-LS (9.71) with the same predictor. The entropy backend / pipeline integration is the proven bottleneck.

## In flight

- **PR #83 (single canonical Obsidian PR):** Review APPROVED (07:52Z). Tester PASSED (07:55Z). Full CMARC stack R1-R2.4 IMPLEMENTED on-branch (all OFF-by-default). **REAL KODAK MEASURED = 10.0906 bpp mean** (PNG MET; WebP 9.61 + JPEG XL 8.71 UNMET). This run re-engages the **Researcher (Mode 2)** on the single PR to diagnose the 10.09 plateau and design the next breakthrough. No `continue`/`research` currently in flight (Builder run `32140809303` ended; this is the only maintainer action).
- **Factory:** main-history repair DONE (main == branch tip, 0 divergent). `data/kodak` provisioning DONE - the Builder ran `run_kodak.sh` successfully against the real 24-image set, closing the measurement gap. No Factory run in flight.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active. Factory's data/kodak provisioning = DONE.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.
- **#71** - DELETED. Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2-free`. No CreditsError expected.
- **Mergeability:** RESTORED. `main` == PR head (0 divergent). `--rebase` now possible (pending stale-flag refresh). Merge still gated by performance target (override #2).
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Researcher (Mode 2) on PR #83 (this run):** diagnose why real-Kodak CMARC = 10.09 (not the predicted 9.3-9.6) - context-adaptation lag, too-coarse context quantization, residual structure the flat per-bit models cannot capture, or binary-decomposition overhead - and design the next breakthrough (true QM-class adaptive arithmetic coder achieving `H(p)+epsilon`, or tighter WebP/JPEG XL-class integration: color cache, re-woven LZ77, per-context logistic mixing). Target existing PR only.
2. **After research:** Architect blueprints (Mode 2) on the same PR; then Builder resumes via `continue`, re-measuring on REAL Kodak after each milestone.
3. **Merge gate (only when met AND main repaired):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact). Then merge (branch preserved), close #68.
4. **Verify README + index.html** still promote Obsidian as Current on every Obsidian advance.
5. **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive). Dispatch Factory when pipeline is quiet.

## Open questions

- **THE decisive number is now known:** real Kodak = 10.0906 bpp mean. CMARC/R2 did not clear WebP (9.61); it plateaued ~0.38 bpp above JPEG-LS (9.71) on the same predictor. The entropy backend / pipeline integration is the proven bottleneck - not the predictor, not the image.
- **Next breakthrough:** can a true QM-class adaptive arithmetic coder (or tighter WebP/JPEG XL integration) close the ~0.38->1.38 bpp gap to WebP/JPEG XL on the SAME residuals? JPEG-LS proves 9.71 is reachable; WebP/JPEG XL prove 9.61/8.71. The Researcher must say what Obsidian is missing and design it.
- **Measurement gap (CLOSED):** `data/kodak` is provisioned; the Builder measured the real 24-image set. Future milestones can be validated on real Kodak, no longer synthetic proxies.
- **Mergeability (RESOLVED):** `main` == branch tip, 0 divergent. The orphan-history break is fixed; `--rebase` is now possible.
- Will the Researcher-on-PR (Mode 2) -> Architect -> continue loop converge to a competitive codec without fracturing into multiple PRs? Hazard mitigated by targeting only the existing PR.

- Mae, the Maintainer
