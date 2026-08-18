# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~07:23Z, maintainer run 32111132870). **OWNER OVERRIDE on #68**: one PR only, iterate via resume, do NOT merge until Obsidian beats WebP/PNG/JPEG XL on Kodak. M1 build in flight (run 32109757749); redundant duplicate run cancelled.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. (PR #78's branch is already gone; preserve all others.)
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDE (2026-08-18T07:22:38Z, issue #68)

- **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached.
- **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact). This overrides the prior incremental-per-milestone merge plan.
- This replaces STATE "Next steps" item 1 (was: merge M1 incremental). M0 (PR #82) is already merged and is history; the rule applies to all future Obsidian work.
- Consequence: the in-flight M1 build (run 32109757749) will open the single canonical Obsidian PR; thereafter all M2/M3 milestones accumulate on that branch via `continue`. No further Obsidian PRs.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z, commit `eee5a31`): GR entropy backend, 53/53 tests pass, no expansion (768x512 @ effort 4 = 21.3 bpp). NOT competitive vs WebP 9.61 / PNG 13.05 / JPEG XL 8.71.
- **Research + Architecture delivered** (PR #82): defect is purely entropy-coding; fix = per-context adaptive Golomb-Rice (Design A), provably non-expanding.
- **M1 IN FLIGHT** (opencode build run `32109757749`, started 2026-08-18T07:04:55Z, ~18 min in, model `hy3-free`): Builder implements per-context predictor selection + GR tuning to beat WebP 9.61. Will open the single canonical Obsidian PR. Per the override, that PR is NOT merged and no further Obsidian PRs are opened; later milestones resume the same branch.

## In flight

- **Builder (M1, #68):** opencode build run `32109757749` (in_progress). Will push the single canonical Obsidian PR. Mae stands by; on PR open, do NOT review-to-merge (override) - keep iterating via `continue` until Kodak target met. Redundant duplicate `opencode` run `32111132965` cancelled this run.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target override active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule (last update 2026-08-17).
- **#42 (Brainstorm Board)** - frozen until Obsidian resolves (owner directive).
- **#71** - DELETED. Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2.5-free`. No CreditsError expected.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **M1 (Builder, #68):** let opencode build run `32109757749` finish and open the single canonical Obsidian PR. Do NOT merge (override). Report real Kodak mean bpp row in that PR.
2. **Loop M2/M3 on the SAME PR:** use `/oc continue` to resume the same branch for per-context predictor selection, capped escaped rANS, squeeze toward JPEG XL 8.71. Accumulate all milestones in the one PR.
3. **Merge gate (only when target met):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless). Then merge, preserve branch, close #68.
4. **Fold `gr_unmap` doc correction** (`obsidian/docs/entropy-architecture.md` line 62) into the single PR so spec matches implementation (`-(u>>1)`, not `-(u+1)>>1`).
5. **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive). Dispatch Factory when pipeline is quiet.

## Open questions

- M1: will per-context predictor selection + GR get under WebP 9.61 on real Kodak? M0 already removed expansion (21.3 bpp @ effort 4); M1 must add the efficiency gain. This lands in the single canonical PR (not merged until target).
- Real Kodak mean bpp row: pending env data/toolchain; must be reported in the single Obsidian PR.
- Will the durable branch-preservation + single-PR rule (maintainer.md update via Factory PR) land cleanly and stop future multi-PR merges?
- M2/M3: capped escaped rANS / squeeze to approach JPEG XL 8.71 - will the staged plan hold on the single branch?
