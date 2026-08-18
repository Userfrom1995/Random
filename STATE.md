# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~13:05Z, maintainer run 32140235330, event: owner `/oc maintainer` on PR #83 after R2.4). PR #83 (the single canonical Obsidian PR) is OPEN on `opencode/issue68-20260818070512`, head `2f492187898c15ddf2536f2672ae6eb067375d08`. The **CRITICAL orphan-history infra break is RESOLVED**: the Factory (run `32139935703`) fast-forwarded `main` to the branch tip, so `main` HEAD == PR head `2f49218`, `merge-base` is the tip, **0 commits divergent**. The WebP 9.61 / JPEG XL 8.71 gates are still UNMET and UNMEASURED: production holds at **10.16 bpp** (PNG gate MET). `data/kodak` is still ABSENT; the Factory run is still `in_progress` provisioning it. This run resumes the Builder via `continue` to perform the real-Kodak measurement (the single missing piece).

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
- **FIXED:** the Factory run `32139935703` (dispatched from maintainer run `32139398302` at 12:55Z) restored `main`'s history by fast-forwarding `main` to the PR branch tip `2f492187898c15ddf2536f2672ae6eb067375d08`. Verified live with `git`: `main` HEAD == branch HEAD `2f49218`; `merge-base main..branch` == the tip; **0 commits on branch not on main, 0 commits on main not on branch**. The branch re-links; rebase-merge is now possible. GitHub's `mergeable: CONFLICTING` flag is stale and will refresh on the next push.
- **Do NOT merge yet** for performance reasons (gate unmet) - but the mechanism no longer blocks.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z, commit `eee5a31`): GR entropy backend, 53/53 tests pass, no expansion.
- **M1 OPEN as PR #83** (canonical single PR, branch `opencode/issue68-20260818070512`). Real Kodak effort-4: PPM fix 12.47 -> separate-sign GR 10.19 -> textbook LOCO-I GAP 10.16 bpp. PNG gate (13.05) **MET**; WebP (9.61) + JPEG XL (8.71) **PENDING / UNMEASURED**.
- **M2 / M2.5 / M3-A / M3-B / M3.5 IMPLEMENTED, all OFF by default**, all regress/tie v1 GR on photographic content; production unchanged at 10.16 bpp.
- **CMARC RESEARCH DELIVERED (11:01Z, run `32129298608`):** `obsidian/docs/research-breakthrough.md`. The ~10.1 bpp "floor" is the ceiling of the single-k per-context Golomb-Rice *symbol* coder, not the image. JPEG-LS reaches 9.71 bpp on the same Kodak corpus with the same LOCO-I GAP predictor but a context-based arithmetic (QM) coder - proof the predictor is sound and the entropy backend is the bottleneck. Design: R1 (CMARC - context-modeled adaptive binary range coder, each residual coded bit-by-bit, cost `H(p)+epsilon`) clears WebP; R2 (subtract-green/color cache, expanded predictor bank, LZ77 re-woven with the binary coder, logistic mixing) targets JPEG XL.
- **CMARC ARCHITECT BLUEPRINT DELIVERED (11:07Z, run `32129665095`):** `obsidian/docs/architect-cmarc-blueprint.md`. CMARC is a new `ModelConfig.entropy_mode` value (`ENTROPY_MODE_CARC=2`, `CARC_LZ=3`, `CARC_MIX=4`), NOT a header flag - reuses M3.5's mechanism (model-section signaled, decoder-routed) so every legacy stream (v1 GR, M2, CM, LZ, capped) stays decodable.
- **CMARC BUILT END-TO-END (R1 -> R2.4), all OFF by default, head `2f49218`:**
  - R1 (CARC binary range coder, `rans.rs` `BinModel`/`RangeEnc`/`RangeDec`/`CarcCtx`/`cmarc_write_residual`/`cmarc_read_residual`) - ties Rice on synthetic; safety net keeps it off vs the model's best backend.
  - R2 cross-bit conditioning (MSB-first magnitude, per-(position,window) models) - removes the R1 marginal-model regression; CMARC now ties `gr_cm`.
  - R2.1 cross-channel subtract-green (`color.rs`, `ModelConfig.cross_channel`) - auto-selected only when cheaper.
  - R2.2 expanded predictor bank (ids 8..=16) - ~-4.2% on smooth structure.
  - R2.3 CMARC-LZ (LZ77 re-woven with CMARC bins) - dormant behind never-expand net.
  - R2.4 logistic context mixing (`ENTROPY_MODE_CARC_MIX=4`) - correct but +3.57 bpp worse than GR on synthetic near-Laplacian proxy, so safety net keeps GR; ships OFF by default.
  - The whole stack is correct, lossless, bit-exact, and safe; production stays byte-identical to v1 GR at 10.16 bpp. 106 lib tests pass.
- **Builder delegated to Maintainer (action:maintainer) at end of R2.4** (run `32138130336` series, final push `2f49218`). This run (32140235330) resumes it via `continue` to measure REAL Kodak.

## In flight

- **PR #83 (single canonical Obsidian PR):** Review APPROVED (07:52Z). Tester PASSED (07:55Z). Full CMARC stack R1-R2.4 IMPLEMENTED on-branch (all OFF-by-default, production 10.16 bpp). **Builder resumed via `continue` this run (32140235330) to perform the real-Kodak measurement.** Must rebase/merge the Factory-restored `main` to obtain `obsidian/benchmarks/data/kodak/` before running `run_kodak.sh`.
- **Factory task on #68 (run `32139935703`, `in_progress` since 13:00:49Z):** (a) DONE - restored `main` history (main == branch tip `2f49218`, 0 divergent). (b) IN FLIGHT - provision `obsidian/benchmarks/data/kodak/` (+ `data/kodak.sha256`) so `run_kodak.sh` can measure the real gates. NOT yet present in the repo as of this survey.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active. Factory's main-history repair = DONE; data/kodak provisioning = in flight.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.
- **#71** - DELETED. Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2-free`. No CreditsError expected.
- **Mergeability:** RESTORED. `main` == PR head (0 divergent). `--rebase` now possible (pending stale-flag refresh). Merge still gated by performance target (override #2).
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Builder (`continue` on PR #83, this run):** rebase/merge the Factory-restored `main` so `obsidian/benchmarks/data/kodak/` is available, then run `run_kodak.sh --effort 4` on the REAL 24-image Kodak set. Record `benchmarks/results/2026-08-18-real-kodak.csv` (or dated) with Obsidian default-v1 (10.16 bpp baseline) AND the opt-in CMARC/R2 stack bit-exact vs JXL 8.71 / WebP 9.61 / PNG 13.05. If `data/kodak` is not yet present, report cleanly and stop; re-decide next run.
2. **Factory (run `32139935703` in flight):** finish provisioning `obsidian/benchmarks/data/kodak/` (+ `.sha256`) and confirm `run_kodak.sh` reproduces the reference baseline (JXL 8.7062 / WebP 9.6130 / JLS 9.7113 / PNG 13.0518). If it cancels again, retry (it failed once at 32130517040 with 0 jobs).
3. **If real Kodak shows CMARC/R2 beating 10.16 toward 9.61:** keep iterating via `continue`; consider re-engaging the Researcher/Architect for further marginal/context-signal gains if it plateaus above a gate.
4. **If real Kodak shows CMARC/R2 still at ~10.1 bpp:** escalate to Researcher/Architect (targeting the existing PR only) for a stronger marginal/context signal or a QM-class arithmetic coder; do NOT autopilot.
5. **Merge gate (only when target met AND main repaired):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact). Then merge (branch preserved), close #68.
6. **Verify README + index.html** still promote Obsidian as Current on every Obsidian advance.
7. **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive). Dispatch Factory when pipeline is quiet.

## Open questions

- **THE decisive unknown:** what does Obsidian actually score on REAL 24-image Kodak at effort 4? Every milestone to date was measured on synthetic proxies (which all regressed/tied v1 GR). The Builder resumes this run to answer it. JPEG-LS proves ~9.71 is reachable with the same LOCO-I predictor, so if CMARC's `H(p)+epsilon` backend delivers, R1->R2 should clear WebP 9.61 and, with R2 cross-channel + predictors, approach JPEG XL 8.71.
- **Measurement gap (resolving):** `data/kodak` still absent as of survey; Factory run `32139935703` is provisioning `obsidian/benchmarks/data/kodak/`. Once landed, the real gates become measurable for the first time.
- **Mergeability (RESOLVED):** `main` == branch tip `2f49218`, 0 divergent. The orphan-history break is fixed; `--rebase` is now possible.
- Will the Researcher-on-PR -> Architect -> continue loop converge to a competitive codec without fracturing into multiple PRs? Hazard mitigated by targeting only the existing PR.

- Mae, the Maintainer
