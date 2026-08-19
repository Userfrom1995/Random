# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~12:40Z, maintainer run 32253803974 on PR #90). **DECISIONS:** `[]` - PR #90 has a blocking review finding (orphan guard at opencode.yml:421-431) that the bot cannot apply: the opencode GitHub App lacks `workflows` permission, so the Factory push was rejected. No triggers fired; owner pinged. Finding #2 (Closes #68) already resolved in the PR body.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83. A fresh `/oc build this` does NOT override this - route to `continue` on the existing PR.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RE-OPENED - 4th recurrence, Factory-caused)

- **Mergeability (BROKEN):** `main` = `8f4c15b` (single orphan commit "factory: harden build loop against 60-min timeout work loss", no parent) - created by the Factory's own merged PR #88. Branch root = `75e2eaa` ("builder: rebuild Obsidian codec crate…", orphan, no parent) + 19 commits -> head `ebcc6b5`. `git merge-base origin/main <branch>` is EMPTY. GitHub still reports `MERGEABLE` but `gh pr merge --rebase` would fail. `--rebase` is impossible until the Factory re-links.
- **Root cause of the recurrence:** the merge-to-`main` step (and the Builder's "rebuild onto main" step) force-writes an orphan root instead of preserving history. The Factory's last round (`32252628750`) confirmed the watchdog but did NOT re-link, and its own merge re-orphaned `main` again.
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is measurable reproducibly.

## SYSTEMIC INFRASTRUCTURE BLOCKER (new this run - 2026-08-19 ~12:40Z)

- **The opencode GitHub App has NO `workflows` permission.** Every pipeline agent (Factory/Builder/Fixer) pushes using the App token, so any edit to `.github/workflows/*.yml` is rejected ("refusing to allow a GitHub App to create or update workflow `.github/workflows/opencode.yml` without `workflows` permission"). Confirmed on PR #90's Factory fix run 32253718673. Consequence: **the bot can NEVER modify workflow files.** The Reviewer's Finding #1 on PR #90 (orphan-guard hardening) therefore cannot be applied by the Factory. Owner must either grant `workflows: write` to the App, or apply workflow edits manually. This also makes the standing "Maintainer may only edit `.github/workflows/*.yml` for model switching" rule moot - nobody in the pipeline can edit them without the owner granting permission.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `ebcc6b5`). Real Kodak (effort 4) numbers, 24-image PCD0992 set (reproducible, durably committed corpus):
  - **DEFAULT shipped codec = CMARC auto-selected best = 9.7094 bpp mean.** Beats JPEG-LS (9.71); PNG 13.05 MET; **WebP 9.61 MISSED by ~0.10 bpp**; **JPEG XL 8.71 MISSED by ~1.0 bpp**. Bit-exact.
  - **Empirical dead-ends (root cause shared = entropy-context fragmentation from predictor/context diversity outside the coder's context budget):**
    - R3-A residual-context INERT (model starvation under ~365x context blowup).
    - R6-B color cache DEAD END (inert on photographic residuals).
    - R7-A per-context weighted predictor REGRESSED to 9.83 bpp (signaled `17+j` codebook indices -> fragmentation). Env-gated OFF (`OBSIDIAN_R7_PERCONTEXT`), so the shipped default remains 9.7094; no live regression.
  - **KEY DIAGNOSIS (empirical, settled):** the codec is pinned at the **JPEG-LS floor (~9.71)**. The entropy backend (CMARC, R4-corrected LZMA carryless range coder verified at `H(p)+epsilon`) is NOT the bottleneck. Remaining gaps are **predictor/transform + coder-context interaction**: adding predictor/context diversity without folding it into the CMARC coder context scatters statistics and raises bpp.
- **CMARC lineage (R1 -> R5) built; entropy core correct (CACM87 / LZMA range coder):**
  - **R4 coder = canonical LZMA carryless binary arithmetic coder** - proven correct; efficiency gate passes (`cmarc_efficiency_vs_shannon` ratio < 1.10).
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` learns the geometric quotient like JPEG-LS QM; delivered the 9.7094 headline (from 11.11 forced CARC).
  - **Faithful R3-A (residual DIFF context):** wired but a NO-OP (model-starvation).
  - **R3-C (JPEG-LS run mode):** implemented; neutral on real Kodak.
  - All CMARC variants ship behind the never-expand safety net, which now ALSO engages by default.
- **R7 blueprint lineage CLOSED as a regression.** R8 blueprint DELIVERED (`8dc421ce`): **signaling-free adaptive weighted predictor** - folds the chosen predictor class into the CMARC residual/quotient context instead of transmitting `17+j` codebook indices, removing the fragmentation that broke R7-A. **Builder mid-R8 (head `ebcc6b5`):** R8-A edits done; tests pending + dead R7 env removal pending.
- **NEW build direction (owner, ~12:40Z):** a fresh build run 32253828516 "fix PPM scramble, 10.16 bpp on Kodak (beats PNG)" was launched and is REUSING the canonical PR #83 branch (one-PR intact). Direction is owner-directed; noted, not redirected.

## In flight

- **PR #90 (Factory infra PR, head `opencode/factory-68-build-loop-duplicate-guard`):** duplicate-Builder `concurrency` guard + orphan guard hardening for the #68 build loop. Reviewed: Finding #2 (Closes #68) already fixed in body; **Finding #1 (orphan guard at opencode.yml:421-431) BLOCKED** - bot cannot push workflow file (missing `workflows` permission). PR stays OPEN, not mergeable, awaiting owner action.
- **Builder (run 32253828516, on PR #83):** owner-launched fresh build "fix PPM scramble, 10.16 bpp on Kodak (beats PNG)" reusing the canonical branch `opencode/issue68-20260818070512`. One-PR rule intact. Orphan-main break + unmet gates still apply.
- **Factory (orphan-main re-link, run 32252628750):** still the open task to durably re-link `main` + fix recurrence root cause; not re-dispatched this run (permission wall + gate unmet = non-urgent, and the App cannot push main anyway without workflows permission).
- **No Architect / Researcher in flight.**

## PENDING (deferred)

- **Clear WebP 9.61 gate:** default 9.7094 is ~0.10 above. R8 (signaling-free adaptive weighted predictor) + newer owner PPM-scramble direction are the attempts.
- **Clear JPEG XL 8.71 gate:** ~1.0 bpp above; the hard long pole - likely needs R8 + tighter color transforms (YCoCg-R + fuller decorrelation) or R7-E/R8 (adaptive per-pixel weighted / MA-tree context).
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near).
- **Document the R7-A regression** in `progress/68-...md` (Builder/Architect task) so the blueprint failure is recorded.
- **PR #90 workflow fix dependency:** Finding #1 cannot land until the owner grants `workflows` permission to the App OR applies the patch manually.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#90 (Factory infra PR for #68 build loop)** - OPEN; blocked on `workflows` permission for the orphan-guard fix (Finding #1). Finding #2 already resolved.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `ebcc6b5`, **rebase-unmergeable** (orphan-main break re-opened, 4th recurrence, Factory-caused). Default 9.7094 (PNG + JPEG-LS met; WebP/JXL unmet). R7-A regressed to 9.83 (OFF by default). R8 blueprint delivered; Builder mid-R8 (run 32252627998) + newer 32253828516 on canonical branch.
- **PR #90:** OPEN, review blocking finding #1 unapplied (bot permission wall), Finding #2 resolved (no `Closes #68`).

## Next steps

1. **PR #90 (owner action):** grant `workflows: write` to the opencode App OR apply the orphan-guard patch manually + merge (after which the duplicate-guard + orphan-guard hardening ships). Do not merge until Finding #1 resolved.
2. **PR #83 Builder finishes** on the canonical branch (R8 / owner's PPM-scramble direction); re-measure REAL Kodak effort-4 reproducibly. Keep R7-A OFF by default until a variant provably beats 9.7094 AND clears 9.61.
3. **Factory re-links `main` to the branch + stops the recurrence** (once `workflows` permission allows the App to push; today it cannot). Rebase branch onto `origin/main`; fix the merge-to-`main`/Builder-rebuild orphan-root root cause.
4. **If still cannot clear WebP:** escalate to the Researcher for R7-E/R8 variants (adaptive per-pixel weighted / MA-tree) or a transform pipeline (YCoCg-R + fuller decorrelation); do NOT loop on band-aids. Do NOT merge until all three gates clear.
5. **Re-fire strict `/oc review`** on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
6. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
7. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current once gates near.

## Open questions

- **SYSTEMIC `workflows` permission gap:** no pipeline agent can edit workflow files; blocks PR #90's Finding #1 and all future infra changes. Owner must grant permission or do manual merges. (This also neutralizes the "Maintainer edits workflows only for model switching" rule - nobody can edit them via the bot.)
- **Can the signaling-free R8 adaptive weighted predictor clear the +0.10 WebP gap without the R7-A fragmentation?** Expected ~9.5-9.6 bpp. If it still fragments, the remaining levers are R7-E (MA-tree / adaptive per-pixel weighted) and transforms (YCoCg-R + fuller decorrelation).
- **Can Obsidian clear JPEG XL 8.71 (~1.0 bpp above)?** Likely needs R8 + tighter color transforms; treat as the hard long pole.
- **Merge gate (owner override #2):** NOT met - default 9.7094 bpp > WebP 9.61 > JXL 8.71. Even best CMARC+R5 beats JPEG-LS but misses WebP by ~0.10 and JXL by ~1.0. R7-A must not ship (regresses to 9.83).
- **Orphan-main break (4th recurrence, Factory-caused):** `main` = `8f4c15b` orphan (from the Factory's own merged PR #88); branch = `75e2eaa` orphan -> `ebcc6b5`. `git merge-base` empty. Factory must re-link AND fix the recurrence root cause; today the App cannot push main without `workflows` permission. Non-blocking now (gate unmet) but must be fixed before merge.
- **Duplicate-Builder-launch defect:** `opencode.yml` spawned two Builder runs from one comment window earlier; the `concurrency` guard (lines 289-291, PR #90) is the intended fix but is itself a workflow edit blocked by the permission gap.
- **Review staleness:** last approve at head ~96a6075; current head `ebcc6b5` un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84, #87 CLOSED. Issue #68 stays OPEN until codecs beaten.

- Mae, the Maintainer
