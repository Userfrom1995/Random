# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~11:09Z, maintainer run 32246188052 on PR #83). **DECISIONS:** `[]` - no trigger. A Builder run is already in flight (opencode `32246187978`, owner `/oc continue` at 11:09:17Z) implementing **R7-A** on the single branch; re-firing `continue` would duplicate an active run. No merge; one PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RESOLVED; rebase satisfied)

- **Mergeability (FIXED):** PR #83 OPEN, head `124bded` (R7 blueprint commit), `mergeable: MERGEABLE`, base `8f4c15b` (== origin/main), valid merge base. `--rebase` is possible whenever the gate is met. No new PR needed.
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is now measurable reproducibly.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `124bded`). Real Kodak (effort 4) numbers, 24-image PCD0992 set (reproducible, durably committed corpus):
  - **DEFAULT shipped codec = CMARC auto-selected best = 9.7093 bpp mean.** Beats JPEG-LS (9.71); PNG 13.05 MET; **WebP 9.61 MISSED by ~0.10 bpp** (14+ of 24 above); **JPEG XL 8.71 MISSED by ~1.0 bpp** (22 of 24 above). Bit-exact.
  - **KEY DIAGNOSIS (empirical, now settled):** the codec has hit the **JPEG-LS floor (~9.71)**. The entropy backend (CMARC, R4-corrected range coder verified at `H(p)+epsilon` via `cmarc_efficiency_vs_shannon`, plus R5 Rice-quotient fix) is NOT the bottleneck. Two attempts to exploit a neighbor-residual context both failed:
    - **R3-A residual-context is INERT** (`cmarc-force+resctx` == `cmarc-force` byte-for-byte): per-`(cid,bin)` binary-model table balloons ~365x under the JPEG-LS DIFF context; starved bins pin at their prior and emit identical bits.
    - **R6-B color cache is a DEAD END** (forced size-32 = 12.88 bpp, size-512 = 14.58 bpp; never-expand net never selects it).
  - The Builder's ceiling analysis (`docs/decisions/builder/2026-08-19-r6b-colorcache-empirical-ceiling.md`) proves the remaining residual is **prediction error**, not coder inefficiency. So the structural fix is a **better (adaptive weighted) predictor** - exactly the WebP/JXL-class lever.
- **CMARC lineage (R1 -> R5) built; entropy core correct (CACM87 / LZMA range coder):**
  - **R4 coder = canonical LZMA carryless binary arithmetic coder** - proven correct; efficiency gate passes (`cmarc_efficiency_vs_shannon` ratio < 1.10).
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` learns the geometric quotient like JPEG-LS QM; delivered the 9.7093 headline (from 11.11 forced CARC).
  - **Faithful R3-A (residual DIFF context):** wired but a NO-OP (model-starvation).
  - **R3-C (JPEG-LS run mode):** implemented; neutral on real Kodak.
  - All CMARC variants ship behind the never-expand safety net, which now ALSO engages by default.
- **R6 blueprint DELIVERED + CORRECTED, empirically disproven (R6-B dead, R3-A inert):** only Component B (R3-A quotient-context) was absorbed into R5.
- **R7 blueprint DELIVERED (`124bded`):** per-context least-squares weighted predictor (offline in `analyze`, signaled `17+j` in `map`). Zero online state -> exact lockstep. Strict superset of current per-plane weight (regression impossible). Expected 9.71 -> ~9.2-9.5 bpp (clears WebP). R7-B folds predictor class into residual context; R7-C/D re-enable tuned LZ77; R7-E (JXL stretch) flagged as possible R8.

## In flight

- **Builder (resumed via `continue` this run, PR #83):** opencode run `32246187978` IN PROGRESS (owner `/oc continue` at 11:09:17Z) implementing **R7-A** (per-context least-squares weighted predictor) in isolation, then re-measure REAL Kodak effort-4 reproducibly. Keep all prior seams OFF by default behind the never-expand net.
- **No Researcher / Architect / Factory in flight.** R7 blueprint delivered; R7-A is the active Builder step.
- **Review is STALE:** last `/oc approve` was at 2026-08-18 07:52Z (head ~`96a6075`); current head `124bded` un-reviewed. Fresh strict review required before any merge, deferred until the codec stabilizes near the gate.

## PENDING (deferred)

- **Clear WebP 9.61 gate:** default 9.7093 is ~0.10 above; R7-A (per-context weighted predictor) is the most plausible single structural fix; expected ~9.2-9.5 bpp.
- **Clear JPEG XL 8.71 gate:** ~1.0 bpp above; the hard long pole - likely needs R7-A/B/C plus possibly R7-E/R8 (adaptive per-pixel weighted prediction / MA-tree context model).
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near).
- **Factory infra hardening:** `continue-on-error` still pending but non-blocking.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `124bded`, `mergeable: MERGEABLE` (orphan break resolved). R6-B proven dead end; R3-A inert; default 9.7093 (PNG + JPEG-LS met; WebP/JXL unmet). R7 blueprint delivered; Builder resuming R7-A (run `32246187978` in_progress).
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Builder implements R7-A (per-context least-squares weighted predictor) on PR #83 (run `32246187978` in_progress):** expand `default_weight_codebook()`, extend `analyze` per-context cost loop to pick best codebook weight per context, encode `17+j` in `map[cid]`, decoder applies `codebook[j]` for `Weighted` entries. Re-measure REAL Kodak effort-4 reproducibly.
2. **After R7-A lands:** measure against WebP 9.61. If it clears it, stack R7-B (fold predictor class into residual context) and R7-C/D (tuned LZ77). If still short, escalate to Researcher for R7-E/R8 (adaptive per-pixel weighted / MA-tree).
3. **If R7 design cannot plausibly clear WebP:** escalate to the Researcher for a deeper algorithmic redesign (do not loop on band-aids). Do NOT merge until all three gates clear.
4. **Re-fire strict `/oc review`** on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
5. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
6. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current once gates near.
7. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Can a per-context least-squares weighted predictor (offline, signaled) clear the ~0.10 bpp WebP gap?** This is the CALIC/JPEG-XL weighted-predictor win; R7-A is the proven route and is structurally regression-proof. Most plausible single win.
- **Will R7 clear JPEG XL 8.71 (~1.0 bpp above)?** Likely needs R7-A/B/C plus R7-E/R8 (adaptive per-pixel weighted prediction + MA-tree context). R7 alone targets WebP reliably and makes a credible run at JXL.
- **Merge gate (owner override #2):** NOT met - default 9.7093 bpp > WebP 9.61 > JXL 8.71. Even best CMARC+R5 beats JPEG-LS but misses WebP by ~0.10 and JXL by ~1.0.
- **Review staleness:** last approve at head ~96a6075; current head `124bded` un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.
- **Orphan-main break:** RESOLVED (PR MERGEABLE). Branch re-linked to main; no new PR needed.

- Mae, the Maintainer