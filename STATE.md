# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~07:50Z, maintainer run 32345784962, owner `/oc maintainer` nudge). PIVOT FIRED: R13-B (the last designed lever) is built, measured, and REGRESSED; the documented fresh-Researcher escape hatch now triggers `research` on PR #93 for a fundamentally new paradigm. Gates unchanged (JXL 8.71 still +0.81 unmet).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. Deferred; schedule once JXL nears.
- **ONE Obsidian PR only.** PR #93 is the single canonical, open Obsidian PR (supersedes closed #83), branch `opencode/issue68-20260818070512`.
- **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec).
- **Orchestrate Researcher + Architect + Builder together** on the existing single PR #93 (or issue #68 for factory/lab) - not on a new PR.

## CRITICAL INFRASTRUCTURE STATE (orphan-main guard MERGED; branch RE-LINKED & PR #93 OPEN)

- **PR #91 MERGED:** orphan-main guard. **PR #92 MERGED:** `main` = `d6b2894`, determinism guard + umbrella rule + force-with-lease pin.
- **`main` = `d6b2894`** (healthy, clean descendant of prior main).
- **Branch `opencode/issue68-20260818070512` OPEN, head `793d692d59dd4c618c7ab4e358c705a62c433b7f`** (R13-B push). Merge-base `d6b2894` non-empty. PR #93 is the single canonical Obsidian PR (`Refs #68`). One-PR rule intact.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub auto-closes #68 if literal `Closes #68` appears ANYWHERE. Future commits MUST use `Refs #68` / `Refs to #68`. PR #93 body is correctly `Refs #68`.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian):** OPEN, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL, CMARC backend; R13-A muted, R13-B gated off). Beats PNG (13.05) + WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
- **R0-R13 codec shipped on PR #93:** R13-A (`PredictorId::AdaptiveRecursive = 19`, 9-property LMS) committed but MUTED (auto-net 9.9065 regression, kept at 9.5209). R13-B (CDF 5/3 lifting) committed (`793d692d`), measured as REGRESSION (10.17 alone / 10.58 with R13-A), gated off by never-expand net. Production unchanged. 141 lib tests pass.

## R13 BLUEPRINT - FULLY BUILT, MEASURED, EXHAUSTED (data-backed ceiling)

- **R13-A (adaptive recursive multi-tap):** forced ~11.18 bpp; auto-net 9.9065 bpp (training-RSS proxy over-selects); MUTED. 139 tests.
- **R13-B (CDF 5/3 lifting):** forced lift alone 10.1708 bpp (+0.65); lift+R13-A 10.5814 bpp (+1.06); net-negative, GATED OFF. 141 tests.
- **Verdict (8 axes total, robust):** the +0.81 bpp JXL gap is a STRUCTURAL ARCHITECTURAL CEILING of the single-pixel predict-and-code / decorrelation pipeline. Failed axes: R11-D MA context (wash), R11-A cross-band `wLL` (wash+slowdown), 64-leaf weight context x2 (regress), R12-A per-band decorrelation (moot; Squeeze rejected), R13-A adaptive multi-tap (regress), R13-B lifting (regress), CMARC backend (near-optimal). All refine context granularity / decorrelation family of a near-optimal predictor. None move JXL.

## CURRENT BUILD STATE (pivot to fresh paradigm)

- **This run (32345784962) fires `research` on PR #93 (head `793d692d`):** the R13 blueprint is fully exhausted with real data (R13-B no longer hypothetical - it regressed). The documented escape hatch now triggers: dispatch the Researcher for a fundamentally new paradigm - a learned predictor, or context-tree weighted prediction at the transform level - NOT another R7/R8/R9/R11/R12/R13-class single-pixel or decorrelation widening (that family is exhausted and already clears WebP).
- **R13-A / R13-B remain in the code, muted/gated off**: production identical to 9.5209 bpp; legacy decode byte-identical; no regression ships. They are documented evidence of the ceiling, not dead weight.
- **No build in flight:** only this maintainer run is active; the R13-B Builder run (32345674366) is `completed`.

## In flight

- **Researcher dispatched by this run (`research` on PR #93):** design a fundamentally different base predictor/transform paradigm (learned predictor OR context-tree weighted prediction at the transform level). Start fresh - the on-branch R7/R8/R9 blueprints (single-pixel weighted predictors) are already implemented and are NOT the answer. Findings feed an Architect blueprint, then the Builder. No merge until all three gates clear.
- **No other builds in flight.**

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above (default 9.5209); current lever = fresh-paradigm `research` (this run). R7-class single-pixel tuning explicitly EXCLUDED.
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once JXL nears).
- **Review staleness on #93:** head `793d692d` clean (141 tests pass); fresh Reviewer + Tester gate required before any merge (premature until new paradigm lands and gates near-clear).
- **Commit-message hygiene:** never write literal `Closes #68` token.

## Issues

- **#68 (Obsidian umbrella)** - OPEN, active fundamental goal, stays open until codecs beaten.
- **#52 / #89 / #90 / #91 / #92 infra** - #90 MERGED; #89 CLOSED; #52 related; #91 MERGED (guard); #92 MERGED (guard). All branches kept.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError`.
- **pages.yml:** green.
- **PR #93 checks:** opencode-pr-trigger SUCCESS on R13-B push; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS.

## Next steps

1. **Await the Researcher's fresh-paradigm spec** on PR #93 (this run's `research` dispatch; a maintainer run auto-triggers on the push). When a Researcher doc lands, dispatch `architect` to blueprint it, then `build` for the Builder.
2. **After gates clear:** fresh Reviewer + Tester gate, then rebase-merge (`--no-delete-branch`) and close #68. NOT before.

## Open questions

- **Can a fundamentally new (learned / context-tree-transform-level) paradigm break the 8.71 JXL wall?** UNKNOWN - the single-pixel/decorrelation family is exhausted (8 real axes, data-backed). This is the only honest lever left.
- **Merge gate (owner override #2):** NOT met - default 9.5209 beats PNG + WebP but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, shares history with main).
- **Orphan-main break:** RESOLVED (merge-base `d6b2894` non-empty; PR #93 healthy).
- **Build collision:** CLEARED - R13-B Builder run completed; `research` is a doc push to the same branch but the Builder is not in flight, so no collision with an active build. (Note: `research`/`architect` push docs; avoid firing `build`/`continue` concurrently on the same branch.)
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **pages.yml:** green.
- **Billing:** resolved (no `CreditsError`; `small_model` correctly pinned free).
- **Commit-message hygiene:** PR #93 body correctly `Refs #68`; future commits must avoid literal `Closes #68`.

- Mae, the Maintainer
