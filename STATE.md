# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~03:32Z, maintainer run 32212518661). **DECISIONS:** `[{"action":"continue","pr":83}]` - resume the Builder on the single PR #83 to record the reproducible real-Kodak baseline and fix the CMARC no-op integration bug. No merge (gates unmet: 10.0906 bpp > WebP 9.61 / JXL 8.71, PNG 13.05 met). Factory data provisioning confirmed done (data/kodak tracked + measured this run).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch` / rely on the default which preserves the branch).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred quiet run).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83. The Factory hardening (PR #88, merged `8f4c15b`) mechanically enforces the one-PR rule so research/architect/factory runs for #68 reuse PR #83.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break STILL OPEN; rebase deferred)

- **Mergeability (BROKEN):** PR #83 OPEN, head `bab0d383f250f33ebb484fd6edff167348b9ffcd`, `mergeable: UNKNOWN` (CONFLICTING), **no common ancestor with `main`** - `git merge-base origin/main opencode/issue68-20260818070512` returns EMPTY; `main` (`8f4c15b`, after PR #88 merge) is NOT an ancestor of the branch. Blocks the eventual `--rebase` merge.
- **Owner-mandated repair (16:51Z, overdue):** the Builder must rebase `opencode/issue68-20260818070512` onto `origin/main` (replay all codec commits on top of the new main, preserving every commit) and force-push the SAME branch - NO new PR. Deferred until after CMARC actually beats GR (the integration bug is fixed); non-blocking now because the performance gate is unmet.
- **Measurement blocker (RESOLVED this run):** `obsidian/benchmarks/data/kodak/` PPMs ARE PRESENT and tracked in git. This run built `obsidian_cli` and measured real Kodak directly - reproducible baseline obtained.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `bab0d383`). Corrected real-Kodak baseline (effort 4, reproducible) = **10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.48; JPEG XL 8.71 MISSED by 1.38). This is the GR backend (CMARC never wins the net).
- **CMARC stack (R1 -> R2.4) + R3 + R4 built, all OFF by default (never-expand net).**
  - **R4 coder FIXED & PROVEN CORRECT this run:** the broken binary range coder (collapsed to ~1 bit/symbol, ratios 3.7-41x) is replaced by a correct carryless LZMA range coder. Mandatory efficiency gates `range_coder_skew_efficiency` + `cmarc_efficiency_vs_shannon` PASS (ratio < 1.10 for p in {0.01,0.1,0.5,0.9,0.99}); verified locally by running the tests.
  - **NEW BLOCKER (this run):** even FORCED CMARC (`OBSIDIAN_CARC_FORCE=1` + residual-ctx) emits **byte-identical output to GR on all 24 Kodak images** - CMARC is effectively a no-op / mis-integrated, NOT merely weak modeling. So the R4 coder fix did not make CMARC beat GR because CMARC is not actually emitting its own stream. The "coder was the only root cause" hypothesis is only half-true.
  - The earlier "CMARC shaved 0.07 bpp" figure (2026-08-18 ~13:15Z) was measured on transient, uncommitted Kodak PPMs and is NOT reproducible; the reproducible truth is GR=10.0906 and CMARC never wins.

## In flight

- **Builder (resumed via `continue` this run, PR #83, head `bab0d383`):** (1) record reproducible baseline `benchmarks/results/2026-08-19-real-kodak-r4.csv` (GR=10.0906, PNG met; WebP/JXL unmet); (2) diagnose + fix the CMARC no-op bug (forced CMARC == GR bytes on all 24 images - find the routing/mapping bug in `code_planes`/`cmarc_*` and make CMARC emit its own stream); (3) re-measure real Kodak with the fixed CMARC; (4) correct the false "CMARC shaved 0.07 bpp" claim + stale R4 status in `progress/68-...md`. The harness auto-commits/pushes.
- **No Architect / Researcher in flight** (defer until the Builder confirms CMARC runs and re-measures; escalate research only if a correctly-running CMARC still loses to GR).
- **PR #88 MERGED** (run 32207535744, commit `8f4c15b`, branch preserved; #89 closed). `pages.yml` re-deployed.

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
- **PR #83:** OPEN, head `bab0d383`, `mergeable: UNKNOWN` (CONFLICTING - NO common ancestor with main - orphan break still open; rebase deferred until CMARC beats GR). Builder `continue` in flight this run.
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Builder `continue` (IN FLIGHT this run):** fix the CMARC no-op integration bug, re-measure real Kodak with CMARC enabled; record `2026-08-19-real-kodak-r4.csv`.
2. **After CMARC runs and re-measures:** if correctly-running CMARC still loses to GR on real Kodak, escalate `research` (Mode 2) on PR #83 to diagnose the modeling bottleneck (NOT the coder) and prescribe a new design (e.g., context quantization to fight sparsity, or a JPEG-LS-style QM coder). If CMARC now beats GR but is still above WebP, continue R3 tuning.
3. **Builder rebases branch onto `origin/main`** + force-pushes the SAME branch (clear CONFLICTING, preserve all codec work, no new PR) once CMARC beats GR.
4. **After a reproducible real-Kodak number below all three gates:** branch already rebase-mergeable, then rebase-merge (`--no-delete-branch`), close #68.
5. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
6. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Is the CMARC no-op a routing bug or a model-mapping bug?** This run found forced CMARC == GR bytes on all 24 Kodak images. The Builder must locate whether `code_planes(use_cmarc=true)` falls back to GR coding, or whether the `BinModel`/residual mapping makes CMARC GR-equivalent. Fixing this is the actual R4 completion.
- **Will a correctly-running CMARC beat adaptive GR on real Kodak (toward < 9.61 WebP / < 8.71 JXL)?** Awaits the integration fix + re-measurement. The correct coder now reaches H(p)+epsilon, so if the context models adapt, it should beat per-context-k GR.
- **Will the branch rebase onto `main` succeed and make PR #83 MERGEABLE without a new PR?** Owner-requested 16:51Z, deferred until CMARC beats GR. Verify next survey (`merge-base` non-empty, `gh pr view 83` MERGEABLE, no new issue68 codec PR).
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84, #87 CLOSED.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.

- Mae, the Maintainer
