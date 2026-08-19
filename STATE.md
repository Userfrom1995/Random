# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~02:0XZ, maintainer run 32206575092, triggered by owner `/oc maintainer` 01:53:41Z on PR #83 after the corrected R4 blueprint landed). **DECISIONS:** `[{"action":"continue","pr":83},{"action":"factory","issue":68}]` - resume the Builder on PR #83 to implement the corrected canonical LZMA range coder (pass the <1.10x efficiency gate) and dispatch the Factory to port the Researcher's roadmap docs from the just-closed redundant PR #87 onto #83 and harden the pipeline against second-PR spawning.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: this is currently NOT satisfied (see Open questions) - flagged for a Builder/Factory pass, not a direct `main` edit by Mae.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch. Redundant codec-rebase PR #84 was opened by the Factory earlier and REJECTED by the owner (CLOSED). **Redundant research PR #87 (branch `opencode/issue68-20260819014150`) was opened by the build workflow during a `research` run and CLOSED this run (32206575092); its docs are being ported to #83 by the Factory.**
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build. **LESSON THIS RUN:** research/architect/factory MUST be triggered ON PR #83 (not on issue #68) so the build workflow reuses the existing branch/PR instead of opening a new one.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break STILL OPEN; rebase deferred)

- **Mergeability (BROKEN):** PR #83 OPEN, head `bab0d383f250f33ebb484fd6edff167348b9ffcd`, `mergeable: false` (CONFLICTING), **no common ancestor with `main`** - `git merge-base origin/main opencode/issue68-20260818070512` returns EMPTY (verified live this run); `main` (`e4e3392`, single orphan commit) is NOT an ancestor of the branch. This blocks the eventual `--rebase` merge.
- **Owner-mandated repair (16:51Z, many runs overdue):** the Builder must rebase `opencode/issue68-20260818070512` onto `origin/main` (replay all codec commits on top of `e4e3392`, preserving every commit's work) and force-push the SAME branch - NO new PR. The Factory is deliberately NOT used for the rebase (its prior squash-rebase opened redundant PR #84 and re-orphaned `main`, violating the one-PR rule). Deferred until after the coder is fixed; non-blocking now because the performance gate is unmet.
- **Measurement blocker (RESOLVED):** `obsidian/benchmarks/data/kodak/` PPMs ARE PRESENT and tracked in git (kodim01..24.ppm). `run_kodak.sh` self-provisions + verifies against `kodak.sha256`. R4 re-measurement on REAL Kodak is possible. Earlier "10.0906 bpp" was GR-fallback only (CMARC explodes until the coder is fixed).

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `bab0d383`). Root-cause PPM-scramble fix landed; codec bit-exact. Corrected real-Kodak baseline (effort 4) = **10.16 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.45; JPEG XL 8.71 MISSED by 1.45).
- **CMARC stack (R1 -> R2.4) + R3 built, all OFF by default.** On real Kodak CMARC itself EXPLODES (21-27 bpp forced) - the never-expand net falls back to GR, so every quoted "best" number (10.09, 10.16) was GR all along. CMARC has never beaten GR because the shared binary coder is **lossless but does NOT compress** (p=0.1 -> 1.745 bps vs 0.469 Shannon = 3.72x; p=0.01 -> 3.348 vs 0.081 = 41x).
- **R4 (correct arithmetic coder + mandatory <1.10x efficiency gate): root cause fully diagnosed, blueprint delivered.** The Architect's latest blueprint (`obsidian/docs/architect-r4-binary-coder-blueprint.md`, delivered 01:53:39Z) pinpoints the three concrete defects behind all prior R4 failures: (1) subrange inversion in the doc's reference `put`; (2) mutated `shift_low` using `(low >> 24) != cache` instead of canonical LZMA carry `(low >> 32) != 0 || low < 0xFF000000` (the "10 emits vs 43 reads" desync); (3) leftover `eprintln!` debug + tunneling through `BitWriter`/`BitReader`. The blueprint ships the verbatim canonical LZMA carryless range coder, a `## 1.4 FIELD BUG LOG`, and a mandatory self-check (`range_coder_skew_efficiency` ratio < 1.10, all round-trips pass). The Builder resumes via `continue` this run to implement it.

## In flight

- **Builder (triggered THIS run 32206575092, via `/oc continue` on PR #83, IN FLIGHT after dispatch):** implement the corrected canonical LZMA range coder (replace `RcEnc`/`RcDec` + `BinEnc`/`BinDec` with fixed `RangeEnc`/`RangeDec`; drop `BitWriter`/`BitReader` from carc call sites; adopt `[carc_len][carc_bytes]` framing), land the mandatory efficiency-gate test (remove `#[ignore]`), get `cargo test -p obsidian_core` green, then re-measure R1/R2/R3 on REAL Kodak effort-4. Record `benchmarks/results/2026-08-19-real-kodak-r4.csv`. Never fake a number.
- **Factory (triggered THIS run, via `/oc factory` on #68, IN FLIGHT after dispatch):** (a) port `obsidian/docs/research-roadmap-m2m3.md` (new) and the augmented `obsidian/docs/research.md` (strict-superset addendum) from branch `opencode/issue68-20260819014150` onto the canonical branch `opencode/issue68-20260818070512` (clean, non-destructive); (b) harden `opencode.yml`/dispatch so research/architect/factory runs for issue #68 reuse PR #83 instead of opening a new PR (mechanically enforce the one-PR rule).
- **No Architect / Researcher in flight.**

## PENDING (deferred to a quiet run)

- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Needs a Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Branch rebase onto `main` (owner 16:51Z):** deferred until after R4 coder fixed; then Builder force-pushes the SAME branch, verify MERGEABLE.
- **Factory infra hardening:** raise build `timeout-minutes` (opencode.yml) only if a future `continue` again truncates at 60m; harden `continue-on-error` so a masked failure fails the run. NOT triggered this run (the failure was a design defect in the coder, not a timeout). The one-PR spawn-prevention hardening IS in this run's Factory dispatch.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active. Researcher roadmap docs being ported to #83 by Factory.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** main workflow agent steps (factory/review/test) pin `opencode/hy3-free`. `opencode.json` `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). main currently = `e4e3392 factory: upgrade reviewer/tester/factory models from mimo-v2.5-free to hy3-free` - the earlier `CreditsError` billing outage is RESOLVED.
- **Mergeability:** PR #83 OPEN, head `bab0d383`, `mergeable: false` (CONFLICTING - NO common ancestor with main - orphan break still open; rebase deferred to after R4 coder fix).
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Builder `continue` (IN FLIGHT):** implement the corrected canonical LZMA range coder, pass the mandatory <1.10x efficiency gate, get `obsidian_core` tests green, then re-measure R1/R2/R3 on REAL Kodak effort-4. Record `benchmarks/results/2026-08-19-real-kodak-r4.csv`.
2. **Factory (IN FLIGHT):** port the two Researcher roadmap docs onto #83's branch; harden the pipeline so research/architect/factory always reuse PR #83 (no second PR).
3. **After R4 lands and compresses:** confirm CMARC efficiency < 1.10x Shannon and re-measure real Kodak: target < 9.71 JPEG-LS, ideally < 9.61 WebP, then < 8.71 JPEG XL.
4. **Builder rebases branch onto `origin/main`** + force-pushes the SAME branch (clear CONFLICTING, preserve all codec work, no new PR).
5. **After a reproducible real-Kodak number below all three gates:** branch already rebase-mergeable, then rebase-merge (`--no-delete-branch` per owner directive), close #68.
6. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
7. **If R4 STILL fails to compress after the corrected blueprint:** next Mae run should dispatch the Factory (`factory`) for a faster free model / longer `timeout-minutes` and consider a battle-tested reference coder (e.g. a known-good arithmetic coder from a reputable source) before re-resuming.

## Open questions

- **Will the corrected LZMA range coder (verbatim from the blueprint) finally compress to `H(p)+epsilon` and pass the <1.10x efficiency gate?** The blueprint is now the canonical reference with a documented bug log; the Builder must not re-introduce the three known defects. Watch the Builder's `continue` run.
- **Will a correctly-compressing CMARC reach JPEG-LS-class (9.71) or better on REAL Kodak?** Predictor is sound (same LOCO-I GAP); broken coder was the proven 3.7-41x-over-Shannon bottleneck. Awaits R4 completion + re-measurement.
- **Will the branch rebase onto `main` succeed (preserving all codec work) and make PR #83 MERGEABLE without a new PR?** Owner-requested 16:51Z, many runs overdue. Verify next survey (`merge-base` non-empty, `gh pr view 83` MERGEABLE, no new issue68 codec PR).
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84 and #87 both CLOSED; no new issue68 codec PR. Factory hardening this run should make the violation mechanically impossible going forward.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** timeout-raise / continue-on-error hardening still pending; one-PR spawn-prevention hardening IS in this run's Factory dispatch.

- Mae, the Maintainer
