# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~05:09Z, maintainer run 32218320979). **DECISIONS:** `[{"action":"continue","pr":83,"head":"7f636a45107675d77877e51e02f4b6248861360c"}]` - re-fire the Builder to fix the GR_LZ WNC panic + CMARC no-op/explosion integration bugs and re-measure real Kodak (the 05:03Z `continue` session completed without advancing the branch). No merge (gates unmet: 10.0906 bpp > WebP 9.61 / JXL 8.71, PNG 13.05 met). One PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred quiet run).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83. PR #88 hardening mechanically enforces the one-PR rule so research/architect/factory runs for #68 reuse PR #83.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break STILL OPEN; rebase deferred)

- **Mergeability (BROKEN):** PR #83 OPEN, head `7f636a45107675d77877e51e02f4b6248861360c`, `mergeable: CONFLICTING`, **no common ancestor with `main`** - `git merge-base origin/main opencode/issue68-20260818070512` returns EMPTY; `main` (`8f4c15b`, after PR #88 merge) is NOT an ancestor of the branch. Blocks the eventual `--rebase` merge.
- **Owner-mandated repair (2026-08-18 16:51Z, overdue):** the Builder must rebase `opencode/issue68-20260818070512` onto `origin/main` (replay all codec commits on top of the new main, preserving every commit) and force-push the SAME branch - NO new PR. Deferred until after CMARC actually beats GR (the integration bug is fixed); non-blocking now because the performance gate is unmet.
- **Measurement blocker (RESOLVED):** `obsidian/benchmarks/data/kodak/` PPMs ARE PRESENT and tracked in git. Reproducible baseline obtained (GR = 10.0906 bpp).

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `7f636a4`). Corrected real-Kodak baseline (effort 4, reproducible) = **10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.48; JPEG XL 8.71 MISSED by 1.38). This is the GR backend (CMARC never wins the net).
- **CMARC stack (R1 -> R2.4) + R3 + R4 built, all OFF by default (never-expand net).**
  - **R4 coder FIXED as CACM87 (this lineage):** the lossy LZMA/WNC range-coder ports were replaced with a correct **CACM87 (Witten-Neal-Cleary) binary arithmetic coder** (commits `aca6650`, `7f636a4`). The mandatory efficiency gates `range_coder_skew_efficiency` + `cmarc_efficiency_vs_shannon` PASS (measured_bps/shannon < 1.10/1.20). The arithmetic core is sound.
  - **OPEN DEFECT 1 (CMARC still a no-op / explodes):** with `OBSIDIAN_CARC_FORCE=1` the encoder output is byte-identical to GR on all 24 Kodak images, and/or the never-expand net falls back to `GR_LZ`. So CMARC is not actually winning. Root cause is integration-level: `code_planes`/`cmarc_*` routing, per-bin `BinModel` adaptation (prior/step/sparsity), or residual mapping/overflow - NOT the coder. CMARC still cannot beat GR on real Kodak.
  - **OPEN DEFECT 2 (GR_LZ WNC flag coder PANICS):** the `GR_LZ` fallback uses a still-broken WNC LZ flag coder that corrupts and panics, so a default encode can crash whenever that fallback is selected. 23 end-to-end tests fail (full-image CMARC tests + explicitly-broken `BinEnc`/`BinDec`). This is the visible crash chain.
  - **Stale progress file:** `progress/68-obsidian-lossless-image-codec.md` still claims `data/kodak` absent / gates unmeasurable - contradicts the reproducible 10.0906 measurement. Must be corrected by the Builder this run.

## In flight

- **Builder (resumed via `continue` this run, PR #83, head `7f636a4`):** (1) fix the GR_LZ WNC LZ flag coder panic (restore a non-crashing default - hard stability gate); (2) diagnose + fix why CMARC is a no-op / explodes (routing or per-bin `BinModel` adaptation in `code_planes`/`cmarc_*`); (3) re-measure real Kodak with the fixed CMARC; (4) correct the stale `progress/68-...md` (data/kodak present; real Kodak = 10.0906). The harness auto-commits/pushes.
  - NOTE: the prior `continue` (owner 05:03Z -> run 32218005352) COMPLETED at ~05:08Z WITHOUT advancing the branch (head still `7f636a4`). This run's `continue` re-fires the integration work.
- **No Architect / Researcher in flight** (defer until the Builder confirms CMARC runs and re-measures; escalate research only if a correctly-wired CMARC still loses to GR on real Kodak).

## PENDING (deferred to a quiet run)

- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Branch rebase onto `main` (owner 16:51Z):** after CMARC actually beats GR; then Builder force-pushes the SAME branch, verify MERGEABLE.
- **Factory infra hardening:** PR #88 delivered "Preserve local commits" + 120/105-min timeouts; `continue-on-error` hardening still pending but non-blocking.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #88:** MERGED (commit 8f4c15b), branch preserved, #89 closed.
- **PR #83:** OPEN, head `7f636a4`, `mergeable: CONFLICTING` (NO common ancestor with main - orphan break still open; rebase deferred until CMARC beats GR). Builder `continue` re-fired this run.
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Builder `continue` (re-fired this run):** fix GR_LZ panic, fix CMARC no-op/explosion, re-measure real Kodak with CMARC, correct stale progress file.
2. **After CMARC runs and re-measures:** if correctly-running CMARC still loses to GR on real Kodak, escalate `research` (Mode 2) on PR #83 to diagnose the modeling bottleneck. If CMARC now beats GR but is still above WebP, continue R3/R4 tuning.
3. **Builder rebases branch onto `origin/main`** + force-pushes the SAME branch (clear CONFLICTING, preserve all codec work, no new PR) once CMARC beats GR.
4. **After a reproducible real-Kodak number below all three gates:** branch already rebase-mergeable, then rebase-merge (`--no-delete-branch`), close #68.
5. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
6. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Will the re-fired Builder actually advance the branch this time?** The prior `continue` (05:03Z -> 32218005352) completed without pushing. Watch for a new opencode build run on `opencode/issue68-20260818070512` that lands the GR_LZ panic fix + CMARC integration fix and a real-Kodak CSV.
- **Is the CMARC no-op a routing bug or a model-mapping bug?** Forced CMARC == GR bytes on all 24 Kodak images. Locate whether `code_planes(use_cmarc=true)` falls back to GR, or whether the `BinModel`/residual mapping makes CMARC GR-equivalent. Fixing this is the actual R4 completion.
- **Will a correctly-wired CMARC beat adaptive GR on real Kodak (toward < 9.61 WebP / < 8.71 JXL)?** Awaits the integration fix + re-measurement. The correct coder now reaches H(p)+epsilon, so if the context models adapt, it should beat per-context-k GR.
- **Will the branch rebase onto `main` succeed and make PR #83 MERGEABLE without a new PR?** Owner-requested 16:51Z, deferred until CMARC beats GR.
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84, #87 CLOSED.
- **Stale progress file:** `progress/68-obsidian-lossless-image-codec.md` contradicts the reproducible 10.0906; Builder must correct it.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.

- Mae, the Maintainer
