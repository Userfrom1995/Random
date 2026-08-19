# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~12:40Z, maintainer run 32253799720 on issue #83). **DECISIONS:** `[{"action":"continue","pr":83}]` - resume the Builder to revert the R8-A default-path regression (restore the proven 9.7094 bpp baseline) and shelve R8 as a dead end. Factory run `32253803974` already in flight re-linking `main` (not re-fired). No merge; one PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83. A fresh `/oc build this` does NOT override this - route to `continue` on the existing PR.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RE-OPENED - 5th recurrence, Factory-caused)

- **Mergeability (BROKEN):** `main` = `8f4c15b` (single orphan commit, no parent) - the Factory's own merged PR re-orphaned it again. Branch root = `75e2eaa` (orphan) + 20 commits -> head `34b03b4`. `git merge-base origin/main <branch>` is EMPTY. GitHub reports `mergeStateStatus: DIRTY`, `mergeable: CONFLICTING`. `--rebase` is impossible until the Factory re-links.
- **Root cause of the recurrence:** the merge-to-`main` step (and the Builder's "rebuild onto main" step) force-writes an orphan root instead of preserving history; plus a duplicate-Builder-launch defect (`opencode.yml` can spawn two codec builds from one comment). The Factory run `32253803974` (in progress) is fixing BOTH: re-link `main` to the branch AND add `concurrency`/`cancel-in-progress` to `opencode.yml`.
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is measurable reproducibly.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `34b03b4`). Real Kodak (effort 4) numbers, 24-image PCD0992 set (reproducible, durably committed corpus):
  - **DEFAULT shipped codec (pre-R8-A, the proven baseline) = CMARC auto-selected best = 9.7094 bpp mean.** Beats JPEG-LS (9.71); PNG 13.05 MET; **WebP 9.61 MISSED by ~0.10 bpp**; **JPEG XL 8.71 MISSED by ~1.0 bpp**. Bit-exact.
  - **R8-A REGRESSED the default path (head `34b03b4`, build 32252627998):** `kodim01` 10.4205 -> 10.6463 bpp; full default mean now ABOVE 9.7094. The branch is currently in a regressed state and must be reverted.
  - **Empirical dead-ends (shared root cause = predictor/transform diversity fragments the CMARC coder context):**
    - R3-A residual-context INERT (model starvation under ~365x context blowup).
    - R6-B color cache DEAD END (inert on photographic residuals).
    - R7-A per-context weighted predictor REGRESSED to 9.83 bpp (`17+j` signaling fragmentation; env-gated OFF, no live regression).
    - **R8-A signaling-free adaptive weighted predictor REGRESSED the default path** (commit `a68b177` unconditionally adds `AdaptiveWeighted` id 200 to `predictors_for`; the coder context `cid` does not encode predictor identity -> fragmentation). SHELVE as a dead end.
  - **KEY DIAGNOSIS (empirical, now settled across 4 attempts):** the codec is pinned at the **JPEG-LS floor (~9.71)**. The entropy backend (CMARC, R4-corrected LZMA carryless range coder verified at `H(p)+epsilon`) is NOT the bottleneck. Remaining gaps are **predictor/transform + coder-context interaction**: every predictor/transform lever tried (R3-A, R6-B, R7-A, R8-A) adds diversity that the CMARC coder context (`cid`) does not account for, so statistics fragment and bpp rises. Folding the predictor/transform choice INTO the CMARC coding context without the 365x model-starvation blowup (or a real transform pipeline YCoCg-R + fuller decorrelation) is the untested path forward.
- **CMARC lineage (R1 -> R5) built; entropy core correct (CACM87 / LZMA range coder):**
  - **R4 coder = canonical LZMA carryless binary arithmetic coder** - proven correct; efficiency gate passes (`cmarc_efficiency_vs_shannon` ratio < 1.10).
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` learns the geometric quotient like JPEG-LS QM; delivered the 9.7094 headline.
  - **Faithful R3-A (residual DIFF context):** wired but a NO-OP (model-starvation).
  - **R3-C (JPEG-LS run mode):** implemented; neutral on real Kodak.
  - All CMARC variants ship behind the never-expand safety net, which now ALSO engages by default.
- **R8 blueprint lineage CLOSED as a regression.** R8-A (signaling-free adaptive weighted predictor) REGRESSED the default; shelved. The Architect blueprint `8dc421ce` is now empirically disproven on its central "cannot regress" claim.

## In flight

- **Builder (this run's `continue` trigger, PR #83):** will resume on `opencode/issue68-20260818070512` to (1) revert the R8-A default-path regression - remove `AdaptiveWeighted` from the default `predictors_for` candidate set (or env-gate OFF) so the shipped default returns to 9.7094; re-measure the full 24-image real Kodak mean to confirm restoration; (2) shelve R8 and record it in `progress/68-...md`; (3) NOT attempt further predictor-diversity tweaks. No Builder was active at run start (build 32252627998 completed 12:39:53Z), so `continue` is not a duplicate.
- **Factory (run `32253803974`, in_progress, on issue #68):** re-link `main` to the branch (rebase branch onto `origin/main` so `main` becomes an ancestor; preserve R8 work at `34b03b4`) AND fix the root cause so the merge-to-`main`/Builder-rebuild step stops force-writing orphan roots + add `concurrency`/`cancel-in-progress` to `opencode.yml` so one comment never spawns two codec builds. NOT re-dispatched this run (already active).
- **No Architect / Researcher in flight.** Next run (after the revert) will escalate `/oc research` on PR #83 for a context-budget-feasible design.

## PENDING (deferred)

- **Clear WebP 9.61 gate:** default 9.7094 is ~0.10 above. R8 (signaling-free adaptive weighted predictor) is now a proven dead end. The untested path is folding predictor/transform choice into the CMARC coding context with a feasible budget, or a transform pipeline (YCoCg-R + fuller decorrelation).
- **Clear JPEG XL 8.71 gate:** ~1.0 bpp above; the hard long pole - needs the above plus tighter color transforms.
- **Revert R8-A regression + restore 9.7094 baseline** (this run's `continue`).
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near).
- **Document the R8-A regression** in `progress/68-...md` (Builder task) so the blueprint failure is recorded alongside R7-A and R6-B.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b` (orphan).
- **PR #83:** OPEN, head `34b03b4`, **rebase-unmergeable** (orphan-main break re-opened, 5th recurrence, Factory-caused). Pre-R8-A default 9.7094 (PNG + JPEG-LS met; WebP/JXL unmet); R8-A REGRESSED the default path (must be reverted). R7-A regressed to 9.83 (OFF by default). R8 blueprint delivered but now disproven as a regression.
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Builder reverts R8-A (this run's `continue`) on PR #83:** remove `AdaptiveWeighted` from the default candidate set / env-gate it OFF; restore the shipped default to 9.7094 bpp (re-measure full real Kodak mean to confirm); shelf R8 in `progress/68`.
2. **After the base is clean, escalate `/oc research` on PR #83:** design a context-budget-feasible breakthrough - fold predictor/transform choice into the CMARC coding context without the 365x model-starvation blowup (that killed R3-A), OR a transform pipeline (YCoCg-R + fuller decorrelation) that WebP/JPEG XL actually use. Do NOT loop on predictor-diversity band-aids.
3. **Factory finishes re-link of `main` + fixes the recurrence root cause + duplicate-launch defect** (run 32253803974). Verify `git merge-base` becomes non-empty and PR becomes MERGEABLE.
4. **If the Researcher's design still cannot clear WebP/JXL:** persevere with a corrected implementation; do NOT merge until all three gates clear.
5. **Re-fire strict `/oc review`** on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
6. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
7. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current once gates near.

## Open questions

- **R8 is a dead end (3rd predictor-diversity failure: R6-B inert, R7-A 9.83, R8-A regressed).** Root cause shared: predictor/transform diversity not folded into the CMARC coder context fragments the entropy model. The untested fix is to fold that choice into the coder context with a feasible budget, or a YCoCg-R transform pipeline.
- **Can Obsidian clear WebP 9.61 (~0.10 bpp above) and JPEG XL 8.71 (~1.0 bpp above)?** Only via a context-budget-feasible redesign; the predictor-diversity lever is exhausted/failed. Treat JXL as the hard long pole.
- **Merge gate (owner override #2):** NOT met - default 9.7094 > WebP 9.61 > JXL 8.71, and the branch is currently regressed above 9.7094. No merge until all three gates clear bit-exactly and reproducibly by the CLEAN default codec.
- **Orphan-main break (5th recurrence, Factory-caused):** `main` = `8f4c15b` orphan; branch = `75e2eaa` orphan -> `34b03b4`. `git merge-base` empty; PR CONFLICTING. Factory (32253803974) must re-link + fix recurrence + duplicate-launch. Non-blocking now (gate unmet) but must be fixed before merge.
- **Review staleness:** last approve at head ~96a6075; current head `34b03b4` un-reviewed (and regressed). Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84, #87 CLOSED. Issue #68 stays OPEN until codecs beaten.

- Mae, the Maintainer
