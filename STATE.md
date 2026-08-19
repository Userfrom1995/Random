# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~02:10Z, maintainer run 32207365906, triggered by PR #88 open + owner `/oc maintainer` 02:06:30Z). **DECISIONS:** `[{"action":"continue","pr":83}]` - PR #88 (infra build-loop resilience) is fully approved + tested and a dedicated merge run 32207535744 is queued to rebase-merge it; re-kick the stalled Obsidian Builder on PR #83 (prior `continue` produced no build run in ~11h).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: this is currently NOT satisfied (see Open questions) - flagged for a Builder/Factory pass, not a direct `main` edit by Mae.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs were preserved on #83 by the Factory. The Factory hardening (run 32206575092) mechanically enforces the one-PR rule so research/architect/factory runs for #68 reuse PR #83 instead of opening a new PR.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never to spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break STILL OPEN; rebase deferred)

- **Mergeability (BROKEN):** PR #83 OPEN, head `bab0d383f250f33ebb484fd6edff167348b9ffcd`, `mergeable: false` (CONFLICTING), **no common ancestor with `main`** - `git merge-base origin/main opencode/issue68-20260818070512` returns EMPTY; `main` (`e4e3392`, single orphan commit) is NOT an ancestor of the branch. Blocks the eventual `--rebase` merge.
- **Owner-mandated repair (16:51Z, overdue):** the Builder must rebase `opencode/issue68-20260818070512` onto `origin/main` (replay all codec commits on top of `e4e3392`, preserving every commit) and force-push the SAME branch - NO new PR. Deferred until after the coder is fixed; non-blocking now because the performance gate is unmet.
- **Measurement blocker (RESOLVED):** `obsidian/benchmarks/data/kodak/` PPMs ARE PRESENT and tracked in git. R4 re-measurement on REAL Kodak is possible.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `bab0d383`). Root-cause PPM-scramble fix landed; codec bit-exact. Corrected real-Kodak baseline (effort 4) = **10.16 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.45; JPEG XL 8.71 MISSED by 1.45).
- **CMARC stack (R1 -> R2.4) + R3 built, all OFF by default.** On real Kodak CMARC EXPLODES (21-27 bpp forced) - the shared binary coder is lossless but does NOT compress (p=0.1 -> 1.745 bps vs 0.469 Shannon = 3.72x; p=0.01 -> 3.348 vs 0.081 = 41x).
- **R4 (correct arithmetic coder + mandatory <1.10x efficiency gate): root cause fully diagnosed.** The Architect's blueprint (`obsidian/docs/architect-r4-binary-coder-blueprint.md`, delivered 01:53:39Z, run 32206134705) pinpoints the three defects: (1) subrange inversion; (2) mutated `shift_low` carry; (3) `eprintln!` debug + `BitWriter`/`BitReader` tunneling. Ships verbatim canonical LZMA carryless range coder + bug log + mandatory self-check. The Builder resumes via the re-kicked `continue` this run.

## In flight

- **Builder (RE-KICKED THIS run 32207365906, via `/oc continue` on PR #83):** prior `continue` (32206575092) produced no build run in ~11h; re-dispatched now. Implement the corrected canonical LZMA range coder (replace `RcEnc`/`RcDec` + `BinEnc`/`BinDec` with fixed `RangeEnc`/`RangeDec`; drop `BitWriter`/`BitReader` from carc call sites; adopt `[carc_len][carc_bytes]` framing), land the mandatory efficiency-gate test (remove `#[ignore]`), get `cargo test -p obsidian_core` green, then re-measure R1/R2/R3 on REAL Kodak effort-4. Record `benchmarks/results/2026-08-19-real-kodak-r4.csv`. Never fake a number.
- **PR #88 merge (QUEUED, dedicated maintainer run 32207535744):** PR #88 approved (Reviewer 02:07:27) + tested (Tester `/oc approve-test` 02:09:17, run 32207425985 success). Run 32207535744 (pending) will rebase-merge with `--no-delete-branch` and close #89. Mae did NOT self-merge in this run.
- **No Architect / Researcher in flight.**

## PENDING (deferred to a quiet run)

- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Needs a Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Branch rebase onto `main` (owner 16:51Z):** deferred until after R4 coder fixed; then Builder force-pushes the SAME branch, verify MERGEABLE.
- **Factory infra hardening:** PR #88 delivered "Preserve local commits" + 120/105-min timeouts (partial work-loss mitigation); `continue-on-error` hardening still pending but non-blocking.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - OPEN; dedicated task issue for PR #88; owned by Factory Engineer. To be CLOSED when PR #88 merges.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** main workflow agent steps (factory/review/test) pin `opencode/hy3-free`. `opencode.json` `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `e4e3392` (PR #88 not yet merged; locally the workspace shows `cca131d` atop it). CreditsError billing outage RESOLVED.
- **PR #88:** OPEN, MERGEABLE, reviewer approved 02:07:27, tester approved 02:09:17; merge queued on run 32207535744.
- **PR #83:** OPEN, head `bab0d383`, `mergeable: false` (CONFLICTING - NO common ancestor with main - orphan break still open; rebase deferred to after R4 coder fix). Builder re-kicked this run.
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Builder `continue` (RE-KICKED):** implement the corrected canonical LZMA range coder, pass the mandatory <1.10x efficiency gate, get `obsidian_core` tests green, then re-measure R1/R2/R3 on REAL Kodak effort-4. Record `benchmarks/results/2026-08-19-real-kodak-r4.csv`.
2. **PR #88 merge (run 32207535744, pending):** rebase-merge `--no-delete-branch`, close #89, confirm `pages.yml` re-deploys.
3. **After R4 lands and compresses:** confirm CMARC efficiency < 1.10x Shannon and re-measure real Kodak: target < 9.71 JPEG-LS, ideally < 9.61 WebP, then < 8.71 JPEG XL.
4. **Builder rebases branch onto `origin/main`** + force-pushes the SAME branch (clear CONFLICTING, preserve all codec work, no new PR).
5. **After a reproducible real-Kodak number below all three gates:** branch already rebase-mergeable, then rebase-merge (`--no-delete-branch`), close #68.
6. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
7. **If R4 STILL fails to compress:** dispatch the Factory (`factory`) for a faster free model / longer `timeout-minutes` and consider a battle-tested reference coder before re-resuming.

## Open questions

- **Will the queued merge run 32207535744 cleanly rebase-merge PR #88 with `--no-delete-branch` and then close #89?** Verify next survey: PR #88 MERGED, branch preserved, issue #89 CLOSED, `origin/main` now contains `cca131d`, `pages.yml` re-deploys.
- **Will the re-kicked Builder (PR #83 `continue`) produce a compressing LZMA range coder passing the <1.10x efficiency gate?** Watch for a new opencode build run on `opencode/issue68-20260818070512` and a green `obsidian_core` test + real-Kodak CSV.
- **Will a correctly-compressing CMARC reach JPEG-LS-class (9.71) or better on REAL Kodak?** Awaits R4 completion + re-measurement.
- **Will the branch rebase onto `main` succeed (preserving all codec work) and make PR #83 MERGEABLE without a new PR?** Owner-requested 16:51Z, many runs overdue. Verify next survey (`merge-base` non-empty, `gh pr view 83` MERGEABLE, no new issue68 codec PR).
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84 and #87 both CLOSED; #88 (infra, separate) merging cleanly via #89.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` hardening still pending; the "Preserve local commits" + 120/105-min timeouts from PR #88 partially mitigate work loss.

- Mae, the Maintainer
