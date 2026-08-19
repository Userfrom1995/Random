# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~12:02Z, maintainer run 32250583359 on PR #83). **DECISIONS:** `[{"action":"architect","pr":83}]` - re-engage the Architect (Mode 2) on the single PR to reconcile the R7-A regression and redesign R7 (fold predictor class into residual context / constrain codebook) before another Builder pass. No merge; one PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RESOLVED; rebase satisfied)

- **Mergeability (FIXED):** PR #83 OPEN, head `41c2d1a` (R7-A build), `mergeable: MERGEABLE`, base == origin/main, valid merge base. `--rebase` is possible whenever the gate is met. No new PR needed.
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is now measurable reproducibly.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `41c2d1a`). Real Kodak (effort 4) numbers, 24-image PCD0992 set (reproducible, durably committed corpus):
  - **DEFAULT shipped codec = CMARC auto-selected best = 9.7093 bpp mean.** Beats JPEG-LS (9.71); PNG 13.05 MET; **WebP 9.61 MISSED by ~0.10 bpp** (14+ of 24 above); **JPEG XL 8.71 MISSED by ~1.0 bpp** (22 of 24 above). Bit-exact.
  - **R7-A (per-context least-squares weighted predictor) REGRESSED to 9.83 bpp** on real Kodak (head `41c2d1a`). It is **env-gated OFF** (`OBSIDIAN_R7_PERCONTEXT`), so the shipped default remains 9.7093; no live regression. The regression is a structural entropy-context fragmentation effect (per-context predictor diversity scatters CMARC model statistics), NOT a raw-energy increase (R7-A is a strict superset of the per-plane weight, so residual energy cannot rise). This refutes the Architect's R7 blueprint central prediction and must be reconciled.
  - **KEY DIAGNOSIS (empirical, settled):** the codec is pinned at the **JPEG-LS floor (~9.71)**. The entropy backend (CMARC, R4-corrected range coder verified at `H(p)+epsilon`) is NOT the bottleneck. Remaining gaps are **predictor/transform + coder-context interaction**:
    - R3-A residual-context INERT (model starvation under ~365x context blowup).
    - R6-B color cache DEAD END (inert on photographic residuals).
    - R7-A per-context weighted predictor REGRESSED via context fragmentation.
    - All three failures share one root: adding predictor/context diversity without folding that diversity into the entropy coder's context scatters statistics and raises bpp.
- **CMARC lineage (R1 -> R5) built; entropy core correct (CACM87 / LZMA range coder):**
  - **R4 coder = canonical LZMA carryless binary arithmetic coder** - proven correct; efficiency gate passes (`cmarc_efficiency_vs_shannon` ratio < 1.10).
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` learns the geometric quotient like JPEG-LS QM; delivered the 9.7093 headline (from 11.11 forced CARC).
  - **Faithful R3-A (residual DIFF context):** wired but a NO-OP (model-starvation).
  - **R3-C (JPEG-LS run mode):** implemented; neutral on real Kodak.
  - All CMARC variants ship behind the never-expand safety net, which now ALSO engages by default.
- **R7 blueprint DELIVERED (`124bded`) but its central prediction FAILED:** per-context LS weighted predictor expected ~9.2-9.5 bpp (clears WebP); actually 9.83 (regresses). R7-B (fold predictor class into residual context) is the natural fix and must be designed together with R7-A, not stacked after it.

## In flight

- **Architect (re-engaged via this run, PR #83):** produce a corrected R7 design that (a) folds the chosen predictor class into the CMARC residual/quotient context to stop fragmentation, and/or (b) constrains the per-context codebook to a small shared set; must honestly state whether per-context weighted prediction can clear the +0.10 WebP gap or whether R7-E (adaptive MA-tree / per-pixel weighted) or a transform (YCoCg-R + fuller color decorrelation) is required. No Builder pass until the corrected blueprint lands.
- **No Builder / Researcher / Factory in flight.**
- **Review is STALE:** last `/oc approve` was at 2026-08-18 07:52Z (head ~`96a6075`); current head `41c2d1a` un-reviewed. Fresh strict review required before any merge, deferred until the codec stabilizes near the gate.

## PENDING (deferred)

- **Clear WebP 9.61 gate:** default 9.7093 is ~0.10 above. R7-A regressed; corrected R7 (predictor-class-in-context) is the next attempt.
- **Clear JPEG XL 8.71 gate:** ~1.0 bpp above; the hard long pole - likely needs corrected R7 + possibly R7-E/R8 (adaptive per-pixel weighted / MA-tree context) and/or better color transforms.
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near).
- **Factory infra hardening:** `continue-on-error` still pending but non-blocking.
- **Document the R7-A regression** in `progress/68-...md` so the blueprint failure is recorded (Builder/Architect task).

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `41c2d1a`, `mergeable: MERGEABLE` (orphan break resolved). Default 9.7093 (PNG + JPEG-LS met; WebP/JXL unmet). R7-A regressed to 9.83 (OFF by default). R7 blueprint refuted; Architect re-engaged for corrected design.
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Architect delivers corrected R7 blueprint on PR #83** (this run's trigger): reconcile R7-A regression; fold predictor class into CMARC residual/quotient context (R7-B) and/or constrain codebook; state honestly whether per-context weighted prediction clears WebP, else propose R7-E or a transform.
2. **Builder resumes R7 (via `continue`) on the corrected blueprint;** re-measure REAL Kodak effort-4 reproducibly. Keep R7-A OFF by default until it provably beats 9.7093 AND clears 9.61.
3. **If corrected R7 still cannot clear WebP:** escalate to the Researcher for R7-E/R8 (adaptive per-pixel weighted / MA-tree context) or a transform pipeline; do NOT loop on band-aids. Do NOT merge until all three gates clear.
4. **Re-fire strict `/oc review`** on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
5. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
6. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current once gates near.
7. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Why did R7-A regress despite being a residual-energy strict superset?** Answer: entropy-context fragmentation - per-context `17+j` predictor diversity scatters CMARC model statistics, raising `H(p)` more than the lower residual energy saves. This is the SAME root cause as R3-A inertness and R6-B dead-end. Corrected R7 must fold predictor class into the coder context.
- **Can per-context weighted prediction clear the +0.10 WebP gap at all?** Open until the Architect reconciles. If not, the remaining levers are R7-E (MA-tree / adaptive per-pixel weighted) and transforms (YCoCg-R + fuller decorrelation) that WebP/JXL actually use.
- **Merge gate (owner override #2):** NOT met - default 9.7093 bpp > WebP 9.61 > JXL 8.71. Even best CMARC+R5 beats JPEG-LS but misses WebP by ~0.10 and JXL by ~1.0. R7-A must not ship (regresses to 9.83).
- **Review staleness:** last approve at head ~96a6075; current head `41c2d1a` un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.
- **Orphan-main break:** RESOLVED (PR MERGEABLE). Branch re-linked to main; no new PR needed.

- Mae, the Maintainer
