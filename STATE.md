# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~11:00Z, maintainer run 32361705333, scheduled/dispatch, run 721, empty payload). R15 (learned neural residual predictor) blueprint is on the branch head `ea914a8`, but the R15 Builder build never launched: the 09:53:21 `build` dispatch was swallowed by the 09:48-09:53 owner comment burst (opencode #763 cancelled / #764 skipped on `main`, no build on the Obsidian branch). This run re-triggers `build` on PR #93. JXL 8.71 still MISSED (+0.81). One-PR rule intact.

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
- **Branch `opencode/issue68-20260818070512` OPEN, head `ea914a8b609bbac15c046bb9c4f1e6e5ddec07d2`** (Architect R15 NRP blueprint; Researcher R15 spec `4db4f97`; R14 Builder remain gated off). Merge-base `d6b2894` non-empty. PR #93 is the single canonical Obsidian PR (`Refs #68`). One-PR rule intact.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub auto-closes #68 if literal `Closes #68` appears ANYWHERE. Future commits MUST use `Refs #68` / `Refs to #68`. PR #93 body is correctly `Refs #68`.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian):** OPEN, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL, CMARC backend; R13-A muted, R13-B gated off, R14 gated off). Beats PNG (13.05) + WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
- **R0-R14 codec shipped on PR #93:** R13-A committed but MUTED (auto-net 9.9065 regression). R13-B (CDF 5/3 lifting) committed (`793d692d`), measured as REGRESSION (10.17 alone / 10.58 with R13-A), gated off. R14 (RCCT + MA residual model) committed (`e9608b42`), measured as REGRESSION (9.66 vs 9.52), gated off. R15 (learned neural residual predictor) blueprint on branch (`ea914a8`), NOT yet built. Production unchanged. 142 lib tests pass.

## THE 9-AXIS CEILING (data-backed, exhaustively measured at ~9.52 bpp)

| Axis | Result |
|---|---|
| R11-D MA context | wash |
| R11-A cross-band `wLL` | wash + 45x slowdown (reverted) |
| 64-leaf weight context | regression x2 (per-leaf starvation) |
| R12-A per-band decorrelation | moot (Squeeze rejected on Kodak) |
| R13-A adaptive recursive | regression 9.9065, muted |
| R13-B CDF 5/3 lifting | regression 10.17/10.58, gated off |
| R14-A RCCT + MA residual | regression 9.66, gated off |
| CMARC backend | near-optimal `H(p)+epsilon` |

The +0.81 bpp JXL gap is a STRUCTURAL ARCHITECTURAL CEILING of the single-pixel predict-and-code / decorrelation / context-tree family. No further tuning of that family can move JXL (it already clears WebP). R15 (learned/neural predictor) is the 10th and final documented lever.

## CURRENT LEVER - R15 LEARNED NEURAL RESIDUAL PREDICTOR (fresh paradigm, escape hatch)

- **R15 spec** (`4db4f97`, Dr. Mob): per-image learned MLP `f_theta` fit on the analysis pass (SSR == entropy under CMARC), weights signaled as `O(1)` `i16`; overlay on `P0` reusing R14's `e0buf`/`rcct_properties` front-end; depth-0 zero net = byte-identical base, so never-regress is structural. Honest target ~9.1-9.4 bpp; `< 8.71` optimistic. **Halt trigger:** if R15 is also net-negative, the predictor family is exhausted (10 axes) and the honest close is a Maintainer recalibrate/repivot recommendation to the owner, NOT another tweak.
- **R15 blueprint** (`ea914a8`, the Architect): build order R15 base (single hidden layer) on REAL Kodak first (target < 9.3, gate 8.71); if 9.0-9.3 add R15-B (stack R14 RCCT on the net's smaller residual).
- **This run:** re-triggers `build` on PR #93 (head `ea914a8`) because the 09:53:21 `build` dispatch never launched a Builder run (comment-burst cancellation). The new build will be approved by this run's repo-wide held-run sweep.

## In flight

- **Builder (R15):** re-dispatched this run (`build` on PR #93, head `ea914a8`). No Builder was in flight before this run (verified: no in_progress/queued/held opencode run). No branch collision.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above (default 9.5209); current lever = R15 learned/neural predictor (fresh paradigm). R7-class single-pixel tuning EXCLUDED (exhausted, already clears WebP).
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once JXL nears).
- **Review staleness on #93:** head `ea914a8` clean; fresh Reviewer + Tester gate required before any merge (premature until the new paradigm lands and gates near-clear).
- **Commit-message hygiene:** never write literal `Closes #68` token.

## Issues

- **#68 (Obsidian umbrella)** - OPEN, active fundamental goal, stays open until codecs beaten.
- **#52 / #89 / #90 / #91 / #92 infra** - #90 MERGED; #89 CLOSED; #52 related; #91 MERGED (guard); #92 MERGED (guard). All branches kept.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError`.
- **pages.yml:** green.
- **PR #93 checks:** opencode-pr-trigger on R15 blueprint push SUCCESS; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS.

## Next steps

1. **Await the R15 Builder result** on PR #93 (this run's re-dispatched `build`; a maintainer run auto-triggers on the push). Survey: if it is a viable implementation, measure REAL Kodak effort-4 and post the number. If it also cannot approach 8.71, escalate a definitive halt/repivot recommendation to the owner (NOT loop silently), per the R15 blueprint halt trigger.
2. **After gates clear:** fresh Reviewer + Tester gate, then rebase-merge (`--no-delete-branch`) and close #68. NOT before.

## Open questions

- **Can R15 (learned/neural predictor) break the 8.71 JXL wall?** UNKNOWN - the 10th lever, a genuinely different parametric family. Honest caveat: JXL hits 8.71 only with VarDCT + modular MA tree + splines (JXL-scale engineering); a learned single-pixel predictor may still fall short. If it misses, escalate halt/repivot to owner.
- **Merge gate (owner override #2):** NOT met - default 9.5209 beats PNG + WebP but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, shares history with main).
- **Orphan-main break:** RESOLVED (merge-base `d6b2894` non-empty; PR #93 healthy).
- **Build collision:** CLEARED - no Builder in flight before this run; re-dispatch collision-safe.
- **R13-B no-op watch / R14 no-op watch:** CLOSED - both builds did NOT no-op (real pushes + measurements).
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **pages.yml:** green.
- **Billing:** resolved (no `CreditsError`; `small_model` correctly pinned free).
- **Commit-message hygiene:** PR #93 body correctly `Refs #68`; future commits must avoid literal `Closes #68`.

- Mae, the Maintainer
