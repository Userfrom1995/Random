# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~07:52Z, maintainer run 32346009111). CORRECTION: the `research` dispatched by run 32345784962 NEVER RAN - the opencode researcher agent crashed (exit 1, no doc, no decision file) on run 32345990841, whose forward step fell through to `/oc maintainer` and triggered this run. Re-dispatching `research` on PR #93 cleanly with a self-contained mandate. Gates unchanged (JXL 8.71 still +0.81 unmet).

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

## RESEARCH DISPATCH STATUS (CORRECTION THIS RUN)

- **The `research` from run 32345784962 did NOT execute.** Run 32345990841 (owner `/oc research`, 07:51:51Z) shows the `research` job `Run opencode researcher agent` exiting code 1 with NO spec doc and NO `/tmp/random-lab-decision.json`; the forward step posted `/oc maintainer` (comment 5353012675), which triggered this run. So the fresh-paradigm brief was never authored.
- **This run (32346009111) RE-DISPATCHES `research` on PR #93 (head `793d692d`)** with a self-contained mandate: design a fundamentally NEW paradigm (learned/neural predictor, OR context-tree weighted prediction at the transform level) for the +0.81 bpp JXL gap; explicitly EXCLUDE all R7/R8/R9/R11/R12/R13-class single-pixel/decorrelation widening (exhausted, already clears WebP). Findings feed an Architect blueprint, then the Builder.
- **Watch item:** if the re-dispatched research ALSO exits 1, dispatch `lab` to inspect the researcher agent wiring / model (agent runtime fault), rather than re-looping.

## CURRENT BUILD STATE (fresh paradigm, pending Researcher)

- **No build in flight** except this maintainer run (32346009111, in_progress). R13-B Builder run 32345674366 is `completed`. The research re-dispatch will push a doc to the branch (no collision with an active Builder).
- R13-A / R13-B remain in the code, muted/gated off: production identical to 9.5209 bpp; legacy decode byte-identical; no regression ships. They are documented evidence of the ceiling, not dead weight.

## In flight

- **Researcher (RE-DISPATCHED this run, `research` on PR #93):** author a fundamentally new base predictor/transform paradigm. Start fresh - on-branch R7/R8/R9 blueprints (single-pixel weighted predictors) are already implemented and are NOT the answer. Findings feed an Architect blueprint, then the Builder. No merge until all three gates clear.
- **No other builds in flight.**

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above (default 9.5209); current lever = fresh-paradigm `research` (re-dispatched this run). R7-class single-pixel tuning explicitly EXCLUDED.
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
- **PR #93 checks:** opencode-pr-trigger SUCCESS on R13-B push; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS. Research run 32345990841 FAILED (agent exit 1) - being re-dispatched.

## Next steps

1. **Await the Researcher's fresh-paradigm spec** on PR #93 (this run's re-dispatched `research`; a maintainer run auto-triggers on the push). When a Researcher doc lands, dispatch `architect` to blueprint it, then `build` for the Builder.
2. **If the re-dispatched research ALSO exits 1:** dispatch `lab` to inspect the researcher agent / opencode.yml research-mode wiring and model config.
3. **After gates clear:** fresh Reviewer + Tester gate, then rebase-merge (`--no-delete-branch`) and close #68. NOT before.

## Open questions

- **Can a fundamentally new (learned / context-tree-transform-level) paradigm break the 8.71 JXL wall?** UNKNOWN - the single-pixel/decorrelation family is exhausted (8 real axes, data-backed). This is the only honest lever left; the Researcher must produce a real spec this time.
- **Research-agent reliability:** run 32345990841 crashed (exit 1) with no output. Is this a recurring agent runtime fault? Monitor the re-dispatch; escalate to `lab` if it repeats.
- **Merge gate (owner override #2):** NOT met - default 9.5209 beats PNG + WebP but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, shares history with main).
- **Orphan-main break:** RESOLVED (merge-base `d6b2894` non-empty; PR #93 healthy).
- **Build collision:** CLEARED - no Builder in flight; the research re-dispatch pushes only a doc, safe.
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **pages.yml:** green.
- **Billing:** resolved (no `CreditsError`; `small_model` correctly pinned free).
- **Commit-message hygiene:** PR #93 body correctly `Refs #68`; future commits must avoid literal `Closes #68`.

- Mae, the Maintainer
