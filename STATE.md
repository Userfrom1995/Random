# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~07:30Z, maintainer run 32111688933). Owner directive at 07:29:31Z: orchestrate Researcher + Architect + Builder together (no autopilot `/oc continue`); keep ONE Obsidian PR, no merge until Kodak target beaten. M1 build still in flight on branch `opencode/issue68-20260818070512`.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. (PR #78's branch is already gone; preserve all others.)
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** (owner directive 2026-08-18T07:29:31Z). Do NOT autopilot with bare `/oc continue`. Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. The Researcher/Architect auto-chain (researcher -> architect -> builder) is DANGEROUS here because it would open a second codec PR - so I trigger them only when they can target the existing single PR, never to spawn a fresh build.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z, commit `eee5a31`): GR entropy backend, 53/53 tests pass, no expansion (768x512 @ effort 4 = 21.3 bpp). NOT competitive vs WebP 9.61 / PNG 13.05 / JPEG XL 8.71.
- **Research + Architecture delivered** (PR #76, #82): defect is purely entropy-coding; fix = per-context adaptive Golomb-Rice (Design A), provably non-expanding.
- **M1 IN FLIGHT** (opencode build run `32109757749`, started 2026-08-18T07:04:55Z, model `hy3-free`). Builder commits to branch `opencode/issue68-20260818070512` (confirmed exists, head `f822c481`); PR NOT yet opened. Implements per-context predictor selection + GR tuning to beat WebP 9.61. This branch/PR will become the single canonical Obsidian PR. Per overrides, NOT merged and NO further Obsidian PRs.

## In flight

- **Builder (M1, #68):** opencode build run `32109757749` (build job in_progress, ~25 min in). Commits landing on `opencode/issue68-20260818070512`. When it opens the PR, that is the single canonical Obsidian PR. Mae stands by; on PR open, route Architect (Mode 2) to design M2, then Builder via `continue` - NOT a bare merge.
- **Stray run 32111688862** (opencode, event issue_comment, no matching `/oc` job) will self-skip; no action needed, no PR spawned.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule (last update 2026-08-17).
- **#42 (Brainstorm Board)** - frozen until Obsidian resolves (owner directive).
- **#71** - DELETED. Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2.5-free`. No CreditsError expected.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **M1 (Builder, #68):** let opencode build run `32109757749` finish and open the single canonical Obsidian PR (branch `opencode/issue68-20260818070512`). Do NOT merge (override). Report real Kodak mean bpp row in that PR.
2. **Orchestration loop (R+A+B on the ONE PR):** once the M1 PR is open, trigger `architect` ON THE PR (Mode 2) to design the next state-of-the-art milestone; Architect hands back `continue`; Builder implements on the same branch. Re-engage `research` (its docs feed the Architect; do not let it spawn a second codec PR). Loop with Reviewer/Tester gating (bit-exact + Kodak bpp).
3. **Merge gate (only when target met):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless). Then merge (branch preserved), close #68.
4. **Fold `gr_unmap` doc correction** (`obsidian/docs/entropy-architecture.md` line 62) into the single PR so spec matches implementation (`-(u>>1)`, not `-(u+1)>>1`).
5. **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive). Dispatch Factory when pipeline is quiet.

## Open questions

- M1: will per-context predictor selection + GR get under WebP 9.61 on real Kodak? M0 already removed expansion (21.3 bpp @ effort 4); M1 must add the efficiency gain. Lands in the single canonical PR (not merged until target).
- Real Kodak mean bpp row: pending env data/toolchain; must be reported in the single Obsidian PR and is the merge gate.
- Will the Architect-on-PR (Mode 2) -> continue loop converge to a competitive codec without fracturing into multiple PRs? The auto-chain hazard is mitigated by only triggering R/A against the existing PR.
- Will the durable one-PR + branch-preservation rule (maintainer.md update via Factory PR) land cleanly and stop future multi-PR merges?
