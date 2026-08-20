# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~08:06Z, maintainer run 32347142216, triggered by owner `/oc build this` on PR #93). The R13 blueprint is FULLY BUILT, MEASURED, and EXHAUSTED (8 real axes). The fresh-paradigm escape hatch has fired: Researcher authored R14, Architect blueprinted R14, owner confirmed `/oc build this`, and this run dispatches `build` to implement R14 base.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. Deferred; schedule once JXL nears.
- **ONE Obsidian PR only.** PR #93 is the single canonical, open Obsidian PR (supersedes closed #83), branch `opencode/issue68-20260818070512`.
- **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec).
- **Orchestrate Researcher + Architect + Builder together** on the existing single PR #93 (or issue #68 for factory/lab) - not on a new PR.

## CRITICAL INFRASTRUCTURE STATE

- **PR #91 MERGED:** orphan-main guard. **PR #92 MERGED:** `main` = `d6b2894`, determinism guard + umbrella rule + force-with-lease pin.
- **`main` = `d6b2894`** (healthy, clean descendant of prior main).
- **Branch `opencode/issue68-20260818070512` OPEN, head `a544ed0c021064590e55c952b0e9778ea9a1c5a2`** (R14 Architect blueprint push). Merge-base `d6b2894` non-empty. PR #93 is the single canonical Obsidian PR (`Refs #68`). One-PR rule intact.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub auto-closes #68 if literal `Closes #68` appears ANYWHERE. Future commits MUST use `Refs #68` / `Refs to #68`. PR #93 body is correctly `Refs #68`.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian):** OPEN, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL, CMARC backend; R13-A muted, R13-B gated off). Beats PNG (13.05) + WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
- **R0-R13 codec shipped on PR #93:** R13-A committed but MUTED (auto-net 9.9065 regression). R13-B (CDF 5/3 lifting) committed (`793d692d`), measured as REGRESSION (10.17 alone / 10.58 with R13-A), gated off. Production unchanged. 141 lib tests pass.

## R13 BLUEPRINT - FULLY BUILT, MEASURED, EXHAUSTED (data-backed ceiling)

- **8 real, measured axes, all fail to close JXL:** R11-D MA context (wash), R11-A cross-band `wLL` (wash+slowdown), 64-leaf weight context x2 (regress), R12-A per-band decorrelation (moot; Squeeze rejected), R13-A adaptive multi-tap (regress 9.9065, muted), R13-B lifting (regress 10.17/10.58, gated off), plus CMARC backend (near-optimal). None move JXL. The +0.81 bpp gap is a STRUCTURAL ARCHITECTURAL CEILING of the single-pixel predict-and-code / decorrelation family.

## FRESH-PARADIGM ESCAPE HATCH - R14 (current lever)

- **Researcher R14 spec** (`obsidian/docs/research-r14-context-tree-ma-residual-model.md`, commit `b90e7e9`, Dr. Mob): residual-conditioned context tree (RCCT) + multiplier-additive (MA) residual model that consumes decode-available **base errors `e0` of the four causal neighbors** as predictor features. Strict superset (depth-0 = base predictor); bit-exact lockstep proven; targets `< 8.71`. Includes optional R14-B (RCCT on a lifting LL).
- **Architect R14 blueprint** (`obsidian/docs/architect-r14-rcct-ma-blueprint.md`, commit `a544ed0c`): an overlay on the existing per-context pixel predictor `P0` (does NOT replace `P0`, does NOT touch the entropy backend). Coded residual becomes `r = (v - P0) - r_pred`, where `r_pred` is an MA model of the residual conditioned on `e0` of the four causal neighbors (stored in per-plane `e0buf` in raster order). Zero signaled bytes at depth-0 (`r_pred=0` = byte-identical to current codec) so the never-expand net makes regression structurally impossible; selection on ACTUAL encoded bytes (avoids the R13-A training-RSS proxy pitfall). Build order: `predict.rs` (RCCT types, `rcct_properties`, `rcct_predict`, `solve_ma_least_squares`) -> `model.rs` (`rcct` field, `build_rcct` greedy split, signaling) -> `encoder.rs`/`decoder.rs` (thread `e0buf`, overlay in all 8 backends) -> CLI `--rcct` seam -> measure REAL Kodak; then R14-B only if base lands ~8.8-9.0.
- **This run (32347142216):** dispatched `build` on PR #93 (head `a544ed0c`) to implement R14 base. No Builder in flight at dispatch (safe, no collision).

## CURRENT BUILD STATE

- **Builder (DISPATCHED this run, `build` on PR #93):** implement R14 RCCT + MA residual model per the Architect blueprint; measure REAL Kodak effort-4; target `< 8.71`; R14-B only if base ~8.8-9.0; never-regress guard + fair (actual-bytes) candidate metric.
- R13-A / R13-B remain in the code, muted/gated off: production identical to 9.5209 bpp; legacy decode byte-identical; no regression ships. They are documented evidence of the ceiling, not dead weight.

## In flight

- **Builder (R14 base):** the only build in flight once dispatched. Researcher/Architect are done (docs pushed). No other builds.
- **No other builds in flight.**

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above (default 9.5209); current lever = R14 (fresh paradigm). R7-class single-pixel tuning explicitly EXCLUDED (exhausted, already clears WebP).
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once JXL nears).
- **Review staleness on #93:** head `a544ed0c` clean (141 tests pass); fresh Reviewer + Tester gate required before any merge (premature until R14 lands and gates near-clear).
- **Commit-message hygiene:** never write literal `Closes #68` token.

## Issues

- **#68 (Obsidian umbrella)** - OPEN, active fundamental goal, stays open until codecs beaten.
- **#52 / #89 / #90 / #91 / #92 infra** - #90 MERGED; #89 CLOSED; #52 related; #91 MERGED (guard); #92 MERGED (guard). All branches kept.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError`.
- **pages.yml:** green.
- **PR #93 checks:** opencode-pr-trigger SUCCESS on R14 Architect push; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS. No in-flight Builder at survey time.

## Next steps

1. **Await the Builder's R14 implementation + real-Kodak measurement** on PR #93 (this run's `build`; a maintainer run auto-triggers on the push). When the Builder posts a number, survey: if R14 base clears `< 8.71`, proceed to R14-B and then the Reviewer/Tester gate; if it lands ~8.8-9.0, authorize R14-B; if it still misses, evaluate whether R14-B is the last realistic lever or whether a deeper paradigm shift (learned predictor) is required.
2. **After gates clear:** fresh Reviewer + Tester gate, then rebase-merge (`--no-delete-branch`) and close #68. NOT before.
3. **Watch item:** the R13-B no-op incident (run 32336195985 completed green but pushed no commit) - if the R14 build ALSO no-ops (no push), dispatch `lab` to inspect opencode.yml `verify pushed` / `forward builder decision`. Re-drive once before escalating.

## Open questions

- **Can R14 (RCCT + MA residual model consuming neighbor base errors) break the 8.71 JXL wall?** UNKNOWN - genuinely new paradigm (the 9th lever), never instantiated in Obsidian before. It targets the exact JXL/FLIF mechanism (neighbor residual conditioning + decision tree) that the 8 exhausted axes never touched. This is the strongest remaining lever.
- **If R14 base still misses 8.71, what then?** R14-B (RCCT on lifting LL) is the additive follow-on. Beyond that, a learned/neural predictor would be a further paradigm step - escalate to the owner before authorizing if R14-B also falls short.
- **Merge gate (owner override #2):** NOT met - default 9.5209 beats PNG + WebP but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, shares history with main).
- **Orphan-main break:** RESOLVED (merge-base `d6b2894` non-empty; PR #93 healthy).
- **Build collision:** CLEARED - no Builder in flight at dispatch; the `build` this run is the first R14 build.
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **pages.yml:** green.
- **Billing:** resolved (no `CreditsError`; `small_model` correctly pinned free).
- **Commit-message hygiene:** PR #93 body correctly `Refs #68`; future commits must avoid literal `Closes #68`.

- Mae, the Maintainer
