# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~09:42Z, maintainer run 32355207087, triggered by owner `/oc maintainer` x3 on PR #93). R14 (the 9th lever) is BUILT, MEASURED, and FAILED the JXL gate (9.66 bpp net-negative). Per the R14 Architect blueprint the R14-B gate (~8.8-9.0) is NOT met, so R14 tuning stops. This run dispatches `research` for the final documented escape-hatch lever: a learned/neural predictor.

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
- **Branch `opencode/issue68-20260818070512` OPEN, head `e9608b429984`** (R14 Builder implementation push, 142 tests pass). Merge-base `d6b2894` non-empty. PR #93 is the single canonical Obsidian PR (`Refs #68`). One-PR rule intact.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub auto-closes #68 if literal `Closes #68` appears ANYWHERE. Future commits MUST use `Refs #68` / `Refs to #68`. PR #93 body is correctly `Refs #68`.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian):** OPEN, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL, CMARC backend; R13-A muted, R13-B gated off, R14 gated off). Beats PNG (13.05) + WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
- **R0-R14 codec shipped on PR #93:** R13-A committed but MUTED (auto-net 9.9065 regression). R13-B (CDF 5/3 lifting) committed (`793d692d`), measured as REGRESSION (10.17 alone / 10.58 with R13-A), gated off. R14 (RCCT + MA residual model) committed (`e9608b42`), measured as REGRESSION (9.66 vs 9.52), gated off. Production unchanged. 142 lib tests pass.

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

The +0.81 bpp JXL gap is a STRUCTURAL ARCHITECTURAL CEILING of the single-pixel predict-and-code / decorrelation / context-tree family. No further tuning of that family can move JXL (it already clears WebP).

## CURRENT LEVER - LEARNED / NEURAL PREDICTOR (fresh paradigm, escape hatch)

- **This run (32355207087):** dispatched `research` on PR #93 (head `e9608b42`) to design a genuinely new predictor paradigm - a learned/neural predictor whose functional form differs from the 4-tap / 9-property linear map. This is the final documented escape-hatch lever (first referenced run 32332621107, re-affirmed 32345784962 / 32347142216). R14 base missed the blueprint's ~8.8-9.0 R14-B gate (landed 9.66), so R14 tuning stops and R14-B is out.
- **R14 finalization (directive):** the R14 implementation on the branch should be landed as a gated, never-shipping ceiling-evidence feature (Builder option (a): `RCCT_EFFORT=255`, `OBSIDIAN_R14_FORCE`/`OBSIDIAN_R14_SHIP` seams) so the learned-predictor work builds on a stable base. Do NOT leave R14 half-pushed.
- **Expected flow:** Researcher spec -> Architect blueprint -> Builder implements learned predictor -> measure REAL Kodak effort-4, target `< 8.71`.

## In flight

- **Researcher (learned predictor):** the only worker dispatched this run. No Builder in flight (R14 finished + pushed `e9608b42` before this run). No branch collision.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above (default 9.5209); current lever = learned/neural predictor (fresh paradigm). R7-class single-pixel tuning EXCLUDED (exhausted, already clears WebP).
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once JXL nears).
- **Review staleness on #93:** head `e9608b42` clean (142 tests pass); fresh Reviewer + Tester gate required before any merge (premature until the new paradigm lands and gates near-clear).
- **Commit-message hygiene:** never write literal `Closes #68` token.

## Issues

- **#68 (Obsidian umbrella)** - OPEN, active fundamental goal, stays open until codecs beaten.
- **#52 / #89 / #90 / #91 / #92 infra** - #90 MERGED; #89 CLOSED; #52 related; #91 MERGED (guard); #92 MERGED (guard). All branches kept.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError`.
- **pages.yml:** green.
- **PR #93 checks:** opencode-pr-trigger on R14 push SUCCESS; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS. R14 no-op watch CLOSED (R14 pushed real measurement, unlike R13-B run 32336195985).

## Next steps

1. **Await the Researcher's learned-predictor spec** on PR #93 (this run's `research`; a maintainer run auto-triggers on the push). Survey: if it is a viable blueprint, hand off to Architect, then Builder; measure REAL Kodak and post the number. If it also cannot approach 8.71, I will escalate a definitive halt/repivot recommendation to the owner (NOT loop silently).
2. **After gates clear:** fresh Reviewer + Tester gate, then rebase-merge (`--no-delete-branch`) and close #68. NOT before.

## Open questions

- **Can a learned/neural predictor break the 8.71 JXL wall?** UNKNOWN - the 10th lever, a genuinely different parametric family. Honest caveat: JXL hits 8.71 only with VarDCT + modular MA tree + splines (JXL-scale engineering); a learned single-pixel predictor may still fall short. If it misses, escalate halt/repivot to owner.
- **Merge gate (owner override #2):** NOT met - default 9.5209 beats PNG + WebP but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, shares history with main).
- **Orphan-main break:** RESOLVED (merge-base `d6b2894` non-empty; PR #93 healthy).
- **Build collision:** CLEARED - R14 Builder finished + pushed `e9608b42` before this run; `research` dispatch is collision-safe.
- **R13-B no-op watch:** CLOSED - R14 build did NOT no-op (real push + measurement).
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **pages.yml:** green.
- **Billing:** resolved (no `CreditsError`; `small_model` correctly pinned free).
- **Commit-message hygiene:** PR #93 body correctly `Refs #68`; future commits must avoid literal `Closes #68`.

- Mae, the Maintainer
