# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~12:58Z, maintainer run 32371624746, scheduled/dispatched run; no event payload). **Re-confirmation + RE-DELIVERY of the R15 halt/repivot escalation.** No new owner input has arrived since the R15 verdict (2026-08-20T11:45:49Z). Critically: the prior two escalation runs (32365426983, 32365436689) wrote `comment.md` but the escalation **did not appear on PR #93** (newest PR comment is still 2026-08-20T04:28:01Z from the R15 `continue` run). This run re-delivers the escalation as `comment.md` so the owner can actually see and decide. One-PR rule intact. R15 landed net-negative (10th + final documented lever) and the R15 blueprint's halt trigger has FIRED. JXL 8.71 still MISSED (+0.81).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. Deferred; schedule once the owner's gate decision lands.
- **ONE Obsidian PR only.** PR #93 is the single canonical, open Obsidian PR (supersedes closed #83), branch `opencode/issue68-20260818070512`.
- **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). For the repivot/recalibrate path, the owner must formally revise this via #68.
- **Orchestrate Researcher + Architect + Builder together** on the existing single PR #93 (or issue #68 for factory/lab) - not on a new PR. (If the owner chooses the VarDCT new-family option, that becomes a fresh issue + fresh R/A/B track.)

## CRITICAL INFRASTRUCTURE STATE

- **PR #91 MERGED:** orphan-main guard. **PR #92 MERGED:** `main` = `d6b2894`, determinism guard + umbrella rule + force-with-lease pin.
- **`main` = `d6b2894`** (healthy, clean descendant of prior main).
- **Branch `opencode/issue68-20260818070512` OPEN, head `f1dcb4b7e19f50ff12e5d4f0128b905484c7561c`** (Builder R15 implementation; Researcher R15 spec `4db4f97`; Architect R15 blueprint `ea914a8`; R14/R13-* remain gated off/muted). Merge-base `d6b2894` non-empty. PR #93 is the single canonical Obsidian PR (`Refs #68`). One-PR rule intact.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub auto-closes #68 if literal `Closes #68` appears ANYWHERE. Future commits MUST use `Refs #68` / `Refs to #68`. PR #93 body is correctly `Refs #68`.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian):** OPEN, stays open until codecs beaten (or the owner formally recalibrates via option 1 below). Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **Default shipped codec = 9.5209 bpp mean** (R10-B CFL, CMARC backend; R13-A muted, R13-B/R14/R15 gated off). Beats PNG (13.05) + WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
- **R0-R15 codec shipped on PR #93:** R13-A committed but MUTED (9.9065 regression). R13-B (CDF 5/3 lifting) committed (`793d692d`), REGRESSION (10.17/10.58), gated off. R14 (RCCT + MA residual) committed (`e9608b42`), REGRESSION (9.66), gated off. R15 (learned neural residual predictor) committed (`f1dcb4b7`), NET-NEGATIVE (byte-identical 9.5209, every per-plane net fails the SSR gate), gated off. 152 lib tests pass.

## THE 10-AXIS CEILING (data-backed, exhaustively measured at ~9.52 bpp)

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

The +0.81 bpp JXL gap is a STRUCTURAL ARCHITECTURAL CEILING of the single-pixel predict-and-code / decorrelation / context-tree / learned-overlay family. No further tuning of that family can move JXL (it already clears WebP). **The R15 blueprint's halt trigger has fired:** the honest close is a Maintainer recalibrate/repivot recommendation to the owner, NOT another tweak.

## CURRENT STATE - HALT/REPIVOT ESCALATION (awaiting OWNER DECISION)

- R15 is the 10th and final documented lever. It is net-negative. There is no further predict-and-code tuning to dispatch.
- **SILENT-STALL SELF-DIAGNOSIS:** runs 32365426983 and 32365436689 wrote the escalation to `comment.md`, but the escalation never appeared on PR #93 (newest comment 2026-08-20T04:28:01Z). This run RE-DELIVERS it via `comment.md` so the owner actually sees the required decision. Flagged for follow-up: if the hardcoded comment-post step keeps dropping `comment.md`, the escalation path is broken and needs `lab` attention.
- **Owner decision required (two honest options):**
  1. **Recalibrate the #68 gate** to a realistic LOCO-I-class modular bar (Obsidian already beats PNG 13.05 + WebP 9.61 on Kodak lossless; only JXL 8.71 missed, which JXL reaches via VarDCT + modular MA tree + splines — a fundamentally different, far larger codec family). Then: run Reviewer + Tester, rebase-merge (`--no-delete-branch`) PR #93, close #68 with a clear "what was built / what remains unsolved" writeup.
  2. **Commission a new codec family** (VarDCT / transform-coding) as a separate multi-phase project: fresh issue + fresh research -> architect -> build track. The only paradigm that has actually achieved JXL-class rates.
- This run's decision list is `[]` (empty) — no workflow trigger is appropriate; re-dispatching build/research/architect would loop against the blueprint's own halt contract. The escalation is delivered via `comment.md` on PR #93.
- No merge (owner override #2; JXL gate unmet). I will not dispatch further predict-and-code tuning on my own.

## In flight

- **None.** R15 Builder finished and pushed `f1dcb4b7` before this run. No Builder/Researcher/Architect in flight. No duplicate `continue`/`build`/`research` fired.

## PENDING (awaiting owner word)

- **Owner decision: recalibrate gate (option 1) OR commission VarDCT new family (option 2).** This is the only blocking item.
- **If option 1 (recalibrate):** update #68 target; then Reviewer + Tester gate on PR #93; then rebase-merge (`--no-delete-branch`) + close #68 + write "what remains unsolved" note.
- **If option 2 (new family):** open a fresh issue; route research -> architect -> build for VarDCT/transform-coding; PR #93 is preserved (never-merged) as the predict-and-code line's record.
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once the owner's gate decision lands).
- **Review staleness on #93:** head `f1dcb4b7` clean; fresh Reviewer + Tester gate required before any merge (premature until the owner's gate decision / new paradigm lands and gates near-clear).
- **Commit-message hygiene:** never write literal `Closes #68` token.

## Issues

- **#68 (Obsidian umbrella)** - OPEN, active fundamental goal, stays open until codecs beaten (or owner formally recalibrates via option 1).
- **#52 / #89 / #90 / #91 / #92 infra** - #90 MERGED; #89 CLOSED; #52 related; #91 MERGED (guard); #92 MERGED (guard). All branches kept.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError`.
- **pages.yml:** green.
- **PR #93 checks:** opencode-pr-trigger SUCCESS on R15 push; pages deploy SKIPPED (PR preview); GitGuardian SUCCESS.

## Next steps

1. **AWAIT OWNER DECISION** (recalibrate vs. new VarDCT family). This run's decision list is `[]` and I will not loop. When the owner replies, route accordingly:
   - Option 1 (recalibrate): update #68 target -> dispatch `review` + `test` on PR #93 -> rebase-merge (`--no-delete-branch`) -> close #68.
   - Option 2 (new family): open fresh issue -> `research` for VarDCT/transform-coding -> `architect` -> `build`. Preserve PR #93 as the predict-and-code record.
2. **After any merge:** promote Obsidian in README + index.html, verify pages.yml, close linked issues.

## Open questions

- **Owner's gate decision (option 1 recalibrate vs. option 2 new-family):** UNKNOWN - this is the single blocking item. I escalated it in `comment.md` (re-delivered this run) and will not act until answered (per "never poll for answers; wait for the owner's answer" rule).
- **Merge gate (owner override #2):** NOT met - default 9.5209 beats PNG + WebP but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec (or the owner formally recalibrates the #68 target).
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, shares history with main).
- **Orphan-main break:** RESOLVED (merge-base `d6b2894` non-empty; PR #93 healthy).
- **Build collision:** CLEARED - no Builder in flight; this run held with an empty decision list (no duplicate dispatch).
- **R13-B/R14/R15 no-op watch:** CLOSED - all three builds pushed real measurements.
- **Work preservation:** all R0-R15 codec work preserved on PR #93 (never-merged, branch kept per standing directive); issue #68 open; ready to publish or pivot on the owner's word.
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge (after the owner's gate decision / new paradigm lands and gates near-clear).
- **pages.yml:** green.
- **Billing:** resolved (no `CreditsError`; `small_model` correctly pinned free).
- **Comment-delivery silent-stall:** ESCALATION from runs 32365426983/32365436689 did not post to PR #93; re-delivered this run. If it still fails to appear, dispatch `lab` to fix the comment-post step.
- **Commit-message hygiene:** PR #93 body correctly `Refs #68`; future commits must avoid literal `Closes #68`.

- Mae, the Maintainer
