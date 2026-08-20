# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~04:13Z, maintainer event run 32331099954, triggered by owner `/oc continue` on PR #93 after the Builder completed R12-A). Decision: dispatch `continue` on PR #93 so the Builder pivots to a deeper BASE predictor/transform (the R12 Squeeze-gated premise is now proven moot). One-PR rule intact; orphan re-link remains fixed.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`. (#91 + #92 branches `opencode/lab-68-orphan-main-guard` intentionally left intact.)
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. Still deferred; schedule once JXL nears.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** PR #93 is the single canonical, open Obsidian PR (supersedes closed #83), branch `opencode/issue68-20260818070512`.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec).
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #93 (or issue #68 for factory/lab) - not on a new PR.

## CRITICAL INFRASTRUCTURE STATE (orphan-main guard MERGED; branch RE-LINKED & PR #93 OPEN)

- **PR #91 MERGED:** orphan-main guard (`c043b7e`, carries literal `Closes #68` commit token; #68 reopened same run).
- **PR #92 MERGED:** `main` = `d6b2894`. Determinism guard + "do not auto-close umbrella" rule + force-with-lease pin. Body `Refs #68`.
- **`main` = `d6b2894`** (healthy, 370 commits, clean descendant of prior main).
- **Branch `opencode/issue68-20260818070512` RE-LINKED** (current head `1471a3f8`), shares history with `main` (merge-base `d6b2894`). PR #93 is the single canonical Obsidian PR (`Refs #68`). ORPHAN PROBLEM RESOLVED.
- Root cause of the prior stall (Lab Engineer refused the re-link; Mae hard-barred from pushing) resolved by the Builder's `/oc continue` rebuild + reopen as PR #93.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub auto-closes #68 if the literal `Closes #68` token appears ANYWHERE. Future Builder/Architect/Lab commits MUST use `Refs #68` / `Refs to #68`. PR #93 body is correctly `Refs #68`.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian):** OPEN, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **Default shipped codec = 9.5208 bpp mean** (R10-B CFL). Beats PNG (13.05) + WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
- **R0-R11 codec shipped on PR #93:** Golomb-Rice, CMARC binary range coder (R4), context-tree weighted predictor (R9-B), R10 Squeeze + chroma-from-luma, R11 cross-band in-loop predictor, R11-D MA-tree-lite combined gradient+residual context (opt-in `OBSIDIAN_CARC_MA_CTX=1`), R11-A cross-band `wLL` (reverted - wash + 45x slowdown).
- **R12-A (per-band weighted predictor) NOW COMMITTED (non-regressive 9.5209 vs 9.5208).** BUT the key finding: the never-expand net REJECTS Squeeze on photographic Kodak because `transforms::squeeze` is a quincunx **subsampling**, not a wavelet - HF bands carry ~as much entropy as the original, so Squeeze is net-negative and correctly rejected. Therefore the R12 escalation premise (per-band decorrelation = missing JXL edge) is **WRONG**.
- **CONCLUSION (robust, 4 independent axes):** the +0.81 bpp gap to JXL 8.71 is the **BASE PREDICTOR** (LOCO-I GAP's residual entropy already near-optimal), NOT context refinement (R3-A/R11-D/64-leaf), NOT Squeeze-gated decorrelation (R12-A/R12-B). Closing JXL needs a genuinely better base predictor/transform (R7 weighted / R8 adaptive-weighted / R9 spatial-weighted blueprints on-branch; or a true wavelet/lifting transform with real energy compaction).

## R12 ARCHITECT BLUEPRINT (DELIVERED, on PR #93 branch)

- File `obsidian/docs/architect-r12-per-band-weighted-ma-tree-blueprint.md` committed + pushed.
- **R12-A (IMPLEMENTED, committed `1055955`):** per-band `analyze_bands` - one `WeightedTree` table + predictor map per Squeeze band. Non-regressive (9.5209). Moot on this corpus because Squeeze is never selected.
- **R12-B (NOT implemented, deprioritized):** replace the uniform `combined_ma_context` fold with a per-band-kind `ma_tree_context`. Also Squeeze-gated -> equally insufficient on its own. Deprioritize; do not sink effort here until a base predictor makes Squeeze beneficial.

## In flight

- **`continue` on PR #93 (DISPATCHED THIS run, 32331099954):** the Builder pivots from Squeeze-gated R12 work to a deeper BASE predictor/transform toward the JXL 8.71 gate, using R7/R8/R9 blueprints (adaptive/learned per-context weighted predictor, or a true wavelet/lifting transform). Loop via `continue` until all three gates clear. The owner's manual `/oc continue` at 04:13:30 hit the skipped opencode path, so this run re-drives it cleanly.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above (default 9.5208); next lever = a genuinely better BASE predictor/transform (in flight via `continue`).
- **Resume Builder (base predictor) via `continue`** - dispatched THIS run.
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once JXL nears).
- **Review staleness on #93:** head `1471a3f8` is builder self-pushed; fresh Reviewer + Tester gate required before any merge.
- **Commit-message hygiene:** never write literal `Closes #68` token in ANY commit message or PR body.

## Issues

- **#68 (Obsidian umbrella)** - OPEN, active fundamental goal, stays open until codecs beaten.
- **#52 / #89 / #90 / #91 / #92 infra** - #90 MERGED; #89 CLOSED; #52 related; #91 MERGED (guard); #92 MERGED (guard + umbrella rule + force-with-lease pin). Both branches kept.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule; board live.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError` in recent runs.
- **pages.yml:** green.
- **PR #93 checks:** opencode-pr-trigger SUCCESS, pages deploy SKIPPED (expected for PR preview), GitGuardian SUCCESS. No Reviewer/Tester run yet.

## Next steps

1. **Builder `continue` (in flight):** implement a genuinely better BASE predictor/transform (R7/R8/R9 basis; adaptive/learned per-context weighted predictor OR a true wavelet/lifting transform), re-measure REAL Kodak effort-4 against the JXL 8.71 gate. Deprioritize R12-B. Loop until all three gates clear.
2. **After gates clear:** fresh Reviewer + Tester gate, then rebase-merge (`--no-delete-branch`) and close #68. NOT before.
3. **README / index.html promotion:** schedule once JXL nears / PR clears.

## Open questions

- **Will a better BASE predictor/transform clear the +0.81 JPEG XL gap on REAL Kodak?** Verdict pending the Builder's next `continue` + real-Kodak re-measure. Four independent axes now prove context refinement AND Squeeze-gated decorrelation are exhausted; the base predictor's functional form is the only seen lever.
- **Merge gate (owner override #2):** NOT met - default 9.5208 beats PNG + WebP but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, shares history with main).
- **Orphan-main break:** RESOLVED (merge-base `d6b2894` non-empty; PR #93 healthy).
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **pages.yml:** green.
- **Billing:** resolved (no `CreditsError`; `small_model` correctly pinned free).
- **Commit-message hygiene:** PR #93 body is correctly `Refs #68`; future commits/blueprints must avoid literal `Closes #68`.

- Mae, the Maintainer
