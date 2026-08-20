# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~14:55Z, maintainer run 32381296165, triggered by owner `/oc maintainer` + directive comment on PR #93). **OWNER OVERRIDE OF THE HALT/REPIVOT STALEMATE.** The owner rejected recalibration and ordered a two-step plan: (1) complete documentation first, (2) build a NEW lossless codec using the most stable architecture available, goal beat JPEG XL. No merge until fully working/tested/release-ready/documented.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. Deferred; schedule once Step 2 clears gates / owner approves.
- **ONE Obsidian PR only.** PR #93 is the single canonical, open Obsidian PR (supersedes closed #83), branch `opencode/issue68-20260818070512`.
- **DO NOT merge the Obsidian PR until the final target is achieved AND quality bar met** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec) AND fully documented/tested/release-ready per the owner's 2026-08-20T14:37:52Z directive.
- **Orchestrate Researcher + Architect + Builder together** on the existing single PR #93 (or issue #68 for factory/lab) - not on a new PR. A genuinely new codec (Step 2) is developed as the next phase of the Obsidian project on PR #93, honoring the one-PR rule.

## CRITICAL INFRASTRUCTURE STATE

- **PR #91 MERGED:** orphan-main guard. **PR #92 MERGED:** `main` = `d6b2894`, determinism guard + umbrella rule + force-with-lease pin.
- **`main` = `d6b2894`** (healthy, clean descendant of prior main).
- **Branch `opencode/issue68-20260818070512` OPEN, head `f1dcb4b7e19f50ff12e5d4f0128b905484c7561c`** (Builder R15 implementation; Researcher R15 spec `4db4f97`; Architect R15 blueprint `ea914a8`; R14/R13-* remain gated off/muted). Merge-base `d6b2894` non-empty. PR #93 is the single canonical Obsidian PR (`Refs #68`). One-PR rule intact.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub auto-closes #68 if literal `Closes #68` appears ANYWHERE. Future commits MUST use `Refs #68` / `Refs to #68`. PR #93 body is correctly `Refs #68`.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian):** OPEN, stays open until codecs beaten (per owner reaffirmation). Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL, CMARC backend; R13-A muted, R13-B/R14/R15 gated off). Beats PNG (13.05) + WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
- **R0-R15 codec shipped on PR #93:** R13-A committed but MUTED (9.9065 regression). R13-B committed, REGRESSION (10.17/10.58), gated off. R14 committed, REGRESSION (9.66), gated off. R15 committed, NET-NEGATIVE (byte-identical 9.5209), gated off. 152 lib tests pass.

## THE 10-AXIS CEILING (data-backed; exhausted at ~9.52 bpp) - PROVEN, DO NOT REVISIT

| Axis | Result |
|---|---|
| R11-D MA context | wash |
| R11-A cross-band `wLL` | wash + 45x slowdown (reverted) |
| 64-leaf weight context | regression x2 (per-leaf starvation) |
| R12-A per-band decorrelation | moot (Squeeze rejected on Kodak) |
| R13-A adaptive recursive | regression 9.9065, muted |
| R13-B CDF 5/3 lifting | regression 10.17/10.58, gated off |
| R14-A RCCT + MA residual | regression 9.66, gated off |
| R15-A learned neural predictor | net-negative, gated off (10th axis) |
| CMARC backend | near-optimal `H(p)+epsilon` |

The +0.81 bpp JXL gap is a STRUCTURAL ARCHITECTURAL CEILING of the single-pixel predict-and-code / decorrelation / context-tree-overlay / learned-overlay family. **No further tuning of that family will be dispatched (owner reaffirmed beat-JXL target).**

## CURRENT STATE - OWNER DIRECTIVE: DOC FIRST, THEN NEW CODEC (Step 1 in progress)

- **Owner directive 2026-08-20T14:37:52Z (overrides halt):** (1) complete documentation of Obsidian on PR #93 first (usage, all flags/options/features); (2) then develop a NEW lossless codec using the most stable architecture available, goal beat JPEG XL + WebP + PNG; (3) do NOT merge until fully working, tested, release-ready, documented.
- **Interpretation of "most stable architecture available":** the proven, non-speculative design that reaches JXL-class lossless rates is the **FLIF / JPEG XL modular context-tree weighted predictor used as the PRIMARY predictor** (not the R14 overlay form, which was net-negative because it stacked on an already near-optimal base). Step 2 will steer the Builder toward that architecture.
- **This run's action:** `continue` on PR #93 (head `f1dcb4b7`) - resume the build to (Step 1) finish Obsidian documentation, then (Step 2) build the new modular context-tree codec. No merge (owner override + quality bar).
- **Recalibration rejected** by owner; #68 target (beat JXL) reaffirmed.

## In flight

- **Builder (Step 1):** dispatched via `continue` this run to complete Obsidian documentation on PR #93, then proceed to Step 2. No other Builder/Researcher/Architect in flight at decision time.

## PENDING (awaiting completion)

- **Step 1 - Documentation:** full CLI usage, every flag/option/feature, including the stable shipped R10-B+CMARC path and the gated experimental R13/R14/R15 work with honest measurements. Must be complete before merge.
- **Step 2 - New codec:** architect/blueprint the FLIF/JXL-modular primary context-tree predictor (research only if a genuinely novel algorithmic question arises; otherwise architect -> build directly since the architecture is proven/stable), implement, measure on REAL Kodak effort-4, target < 8.71 JXL AND < 9.61 WebP AND < 13.05 PNG bit-exactly.
- **Before merge (owner override):** fully working, thoroughly tested (full lib + real-Kodak reproducible), release-ready, properly documented. Then Reviewer + Tester gate, then rebase-merge (`--no-delete-branch`).
- **README / index.html Obsidian promotion** (standing directive, deferred until Step 2 clears gates / owner approves).
- **Review staleness on #93:** head `f1dcb4b7` clean; fresh Reviewer + Tester gate required before any merge.
- **Commit-message hygiene:** never write literal `Closes #68` token.

## Issues

- **#68 (Obsidian umbrella)** - OPEN, active fundamental goal, stays open until codecs beaten (owner reaffirmed).
- **#52 / #89 / #90 / #91 / #92 infra** - all merged/closed; branches kept.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError`.
- **pages.yml:** green.
- **PR #93 checks:** opencode-pr-trigger SUCCESS on R15 push; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS.

## Next steps

1. **Step 1 (this run's dispatch):** Builder completes Obsidian documentation on PR #93 (usage, all flags/options/features). 
2. **Step 2 (after docs):** route architect -> build for the new FLIF/JXL-modular primary context-tree codec on PR #93; measure REAL Kodak; target all three gates bit-exactly.
3. **Merge gate (owner override + quality bar):** do NOT merge until default codec beats PNG 13.05 + WebP 9.61 + JPEG XL 8.71 bit-exactly AND is fully tested/documented/release-ready. Then Reviewer + Tester, rebase-merge (`--no-delete-branch`), close #68 with "what was built / what remains unsolved" writeup.

## Open questions

- **Owner's gate decision:** RESOLVED BY DIRECTIVE - recalibration rejected; build a new codec with the most stable architecture, beat JXL. #68 target reaffirmed.
- **Most stable architecture for Step 2:** selected as FLIF/JXL-modular context-tree weighted predictor as PRIMARY (proven JXL-class). Will be confirmed via Architect blueprint before build.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, shares history with main).
- **Orphan-main break:** RESOLVED (merge-base `d6b2894` non-empty; PR #93 healthy).
- **Build collision:** CLEARED - prior R15 Builder finished; this run's `continue` is the next step.
- **Work preservation:** all R0-R15 codec work preserved on PR #93 (never-merged, branch kept per standing directive); issue #68 open; ready to document/publish/pivot on the owner's word.
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **pages.yml:** green.
- **Billing:** resolved (no `CreditsError`; `small_model` correctly pinned free).
- **Silent-stall comment-delivery:** the prior escalation comments (runs 32365426983/32365436689) apparently did not post, but the owner clearly saw the situation and responded with a directive - so the escalation reached the owner. No `lab` dispatch needed now; will revisit only if a future required comment fails to post.
- **Commit-message hygiene:** PR #93 body correctly `Refs #68`; future commits must avoid literal `Closes #68`.

- Mae, the Maintainer
