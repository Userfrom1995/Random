# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~12:11Z, maintainer run 32251348552 on PR #83). **DECISIONS:** `[{"action":"continue","pr":83}]` - resume the Builder on the single PR to implement the delivered R8 blueprint (signaling-free adaptive weighted predictor); route via `continue`, not `/oc build this`, to honor the one-PR override. No merge; one PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83. A fresh `/oc build this` does NOT override this - route to `continue` on the existing PR.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RESOLVED; rebase satisfied)

- **Mergeability (FIXED):** PR #83 OPEN, head `8dc421ce` (R8 blueprint), `mergeable: MERGEABLE`, base == origin/main, valid merge base. `--rebase` is possible whenever the gate is met. No new PR needed.
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is now measurable reproducibly.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `8dc421ce`). Real Kodak (effort 4) numbers, 24-image PCD0992 set (reproducible, durably committed corpus):
  - **DEFAULT shipped codec = CMARC auto-selected best = 9.7093 bpp mean.** Beats JPEG-LS (9.71); PNG 13.05 MET; **WebP 9.61 MISSED by ~0.10 bpp** (14+ of 24 above); **JPEG XL 8.71 MISSED by ~1.0 bpp** (22 of 24 above). Bit-exact.
  - **Empirical dead-ends (root cause shared = entropy-context fragmentation from predictor/context diversity outside the coder's context budget):**
    - R3-A residual-context INERT (model starvation under ~365x context blowup).
    - R6-B color cache DEAD END (inert on photographic residuals).
    - R7-A per-context weighted predictor REGRESSED to 9.83 bpp (signaled `17+j` codebook indices -> fragmentation). Env-gated OFF (`OBSIDIAN_R7_PERCONTEXT`), so the shipped default remains 9.7093; no live regression.
  - **KEY DIAGNOSIS (empirical, settled):** the codec is pinned at the **JPEG-LS floor (~9.71)**. The entropy backend (CMARC, R4-corrected LZMA carryless range coder verified at `H(p)+epsilon`) is NOT the bottleneck. Remaining gaps are **predictor/transform + coder-context interaction**: adding predictor/context diversity without folding it into the CMARC coder context scatters statistics and raises bpp.
- **CMARC lineage (R1 -> R5) built; entropy core correct (CACM87 / LZMA range coder):**
  - **R4 coder = canonical LZMA carryless binary arithmetic coder** - proven correct; efficiency gate passes (`cmarc_efficiency_vs_shannon` ratio < 1.10).
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` learns the geometric quotient like JPEG-LS QM; delivered the 9.7093 headline (from 11.11 forced CARC).
  - **Faithful R3-A (residual DIFF context):** wired but a NO-OP (model-starvation).
  - **R3-C (JPEG-LS run mode):** implemented; neutral on real Kodak.
  - All CMARC variants ship behind the never-expand safety net, which now ALSO engages by default.
- **R7 blueprint lineage CLOSED as a regression.** R8 blueprint DELIVERED (`8dc421ce`): **signaling-free adaptive weighted predictor** - folds the chosen predictor class into the CMARC residual/quotient context instead of transmitting `17+j` codebook indices, removing the fragmentation that broke R7-A. Targets the ~0.10 bpp WebP gap, then JXL via tighter transforms.

## In flight

- **Builder (this run's `continue` trigger, PR #83):** implement R8 from the delivered blueprint (`obsidian/docs/architect-r8-adaptive-weighted-predictor-blueprint.md`); re-measure REAL Kodak effort-4 reproducibly. Keep R7-A OFF by default until R8 provably beats 9.7093 AND clears 9.61.
- **No Architect / Researcher / Factory in flight.**
- **Review is STALE:** last `/oc approve` was at 2026-08-18 07:52Z (head ~`96a6075`); current head `8dc421ce` un-reviewed. Fresh strict review required before any merge, deferred until the codec stabilizes near the gate.

## PENDING (deferred)

- **Clear WebP 9.61 gate:** default 9.7093 is ~0.10 above. R8 (signaling-free adaptive weighted predictor) is the next attempt.
- **Clear JPEG XL 8.71 gate:** ~1.0 bpp above; the hard long pole - likely needs R8 + tighter color transforms (YCoCg-R + fuller decorrelation) or R7-E/R8 (adaptive per-pixel weighted / MA-tree context).
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near).
- **Factory infra hardening:** `continue-on-error` still pending but non-blocking.
- **Document the R7-A regression** in `progress/68-...md` (Builder/Architect task) so the blueprint failure is recorded.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `8dc421ce`, `mergeable: MERGEABLE` (orphan break resolved). Default 9.7093 (PNG + JPEG-LS met; WebP/JXL unmet). R7-A regressed to 9.83 (OFF by default). R8 blueprint delivered; Builder to implement via `continue`.
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Builder resumes R8 (via `continue`, this run's trigger) on PR #83:** implement the signaling-free adaptive weighted predictor; re-measure REAL Kodak effort-4 reproducibly. Keep R7-A OFF by default until R8 provably beats 9.7093 AND clears 9.61.
2. **If R8 still cannot clear WebP:** escalate to the Researcher for R7-E/R8 variants (adaptive per-pixel weighted / MA-tree) or a transform pipeline (YCoCg-R + fuller decorrelation); do NOT loop on band-aids. Do NOT merge until all three gates clear.
3. **Re-fire strict `/oc review`** on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
4. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
5. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current once gates near.
6. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Can the signaling-free R8 adaptive weighted predictor clear the +0.10 WebP gap without the R7-A fragmentation?** The design removes the `17+j` signaling that caused the regression. Expected ~9.5-9.6 bpp. If it still fragments, the remaining levers are R7-E (MA-tree / adaptive per-pixel weighted) and transforms (YCoCg-R + fuller decorrelation) that WebP/JXL actually use.
- **Can Obsidian clear JPEG XL 8.71 (~1.0 bpp above)?** Likely needs R8 + tighter color transforms; treat as the hard long pole.
- **Merge gate (owner override #2):** NOT met - default 9.7093 bpp > WebP 9.61 > JXL 8.71. Even best CMARC+R5 beats JPEG-LS but misses WebP by ~0.10 and JXL by ~1.0. R7-A must not ship (regresses to 9.83).
- **Review staleness:** last approve at head ~96a6075; current head `8dc421ce` un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.
- **Orphan-main break resolved; one-PR integrity:** #83 sole canonical Obsidian PR; #84, #87 CLOSED. Issue #68 stays OPEN until codecs beaten.

- Mae, the Maintainer
