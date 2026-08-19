# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~09:40Z, maintainer run 32238487128 on PR #83). **DECISIONS:** `[]` - the Builder is already in flight on Component A (run `32238473667`, in-progress); re-firing `continue` would duplicate it. No merge (default 9.7067 bpp still above WebP 9.61 / JPEG XL 8.71); one PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RESOLVED; rebase satisfied)

- **Mergeability (FIXED):** PR #83 OPEN, head `0efc83c1007dedba3daf3e20d5fc6740df72ac22`, `mergeable: true`, base `8f4c15b` (== origin/main), valid merge base, 11+ commits ahead. `--rebase` is possible whenever the gate is met. No new PR needed.
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is now measurable reproducibly.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `0efc83c`). Real Kodak (effort 4) numbers, 24-image PCD0992 set:
  - **DEFAULT shipped codec = CMARC auto-selected best of {GR, CMARC, CARC_LZ, CARC_MIX} via never-expand net. With Component B (R3-A residual-context quotient fix) just pushed: CMARC+R3-A = 9.7067 bpp mean** - at/below the JPEG-LS floor (JPEG-LS = 9.71 on the same corpus). PNG 13.05 MET; WebP 9.61 MISSED by ~0.10 bpp; JPEG XL 8.71 MISSED by ~1.0 bpp. Bit-exact (8000 fuzz, CRC).
- **CMARC lineage (R1 -> R5) built; entropy core now correct (CACM87):**
  - **R4 coder = CACM87 (Witten-Neal-Cleary binary arithmetic coder)** - proven correct; efficiency gates pass (ratio < 1.10/1.20).
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` learns the geometric quotient like JPEG-LS QM; dropped forced CARC 11.11 -> 9.71 bpp.
  - **R3-C (JPEG-LS run mode):** implemented; neutral on real Kodak.
  - All CMARC variants ship behind the never-expand safety net, which now ALSO engages by default.
- **R6 blueprint DELIVERED + CORRECTED (head `f137881`), build order B -> A -> C:**
  - **Component B (R3-A residual-context fix) - DONE & PUSHED (head `0efc83c`):** quotient run conditioned on the residual DIFF context `rcid` (zero/sign/remainder stay on gradient context `cid`); `ctxs` bounds fix. Real Kodak: CMARC 9.7094 -> **9.7067 bpp** (clears JPEG-LS 9.71, no regression). Mandatory test `r3a_residual_context_changes_quotient_stream` gates it.
  - **Component A (R6-B color cache) - IN FLIGHT:** per-plane LRU (default 512), `cache_flag` + recency-ranked index via CMARC bins, new `ENTROPY_MODE_CARC_CACHE = 6`, mirrored decoder, `use_color_cache` seam + safety net. Primary WebP (9.61) lever.
  - **Component C (tuned matches):** `MIN_MATCH = 2` + 2D distance model + cache competition (marginal on photos).
  - **Honest risk:** B reached JPEG-LS; B+A plausibly clears WebP; JPEG XL 8.71 UNCERTAIN (may need a separate R7 adaptive weighted predictor / MA-tree). The Architect does NOT promise JPEG XL from R6 alone.

## In flight

- **Builder (run `32238473667`, in-progress, started 09:36:30Z, triggered by owner `/oc continue` at 09:36:28Z):** implementing **Component A (color cache)**, then will stack C, re-measuring REAL Kodak effort-4 reproducibly. Keep every prior seam OFF by default behind the never-expand net.
- **No Architect / Researcher / Factory in flight.** Prior R6 blueprint + Component B are delivered; next escalation (if A+C still miss JXL) would be an Architect/Researcher pass for R7.
- **Review is STALE:** last `/oc approve` was at 2026-08-18 07:52Z (head ~`96a6075`); since then CMARC default switch (R4/R5/R3-C), R2.1-R2.4, Component B (R3-A). A fresh strict review is required before any merge, but deferred until the codec stabilizes near the gate.

## PENDING (deferred)

- **Clear WebP 9.61 gate:** default 9.7067 is ~0.10 above; Component A (color cache) is the most plausible single win.
- **Clear JPEG XL 8.71 gate:** ~1.0 bpp above; the hard long pole - needs A+C and possibly R7 (Architect explicitly does not promise JPEG XL from R6 alone).
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near).
- **Factory infra hardening:** `continue-on-error` still pending but non-blocking.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `0efc83c`, `mergeable: true` (orphan break resolved). Component B pushed; Component A in flight (run `32238473667`). No held runs.
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Let the in-flight Builder (run `32238473667`) finish Component A (color cache), then C (tuned matches), re-measuring REAL Kodak effort-4 reproducibly.**
2. **After A(+C) land:** re-measure real Kodak; if default mean < 9.61 (WebP), continue toward JXL; if JXL (< 8.71) also cleared, proceed to merge prep.
3. **If WebP cleared but JXL not, and A+C exhausted:** re-fire `architect`/`research` on PR #83 for R7 (adaptive weighted predictor / MA-tree); do NOT merge until all three gates clear.
4. **Re-fire strict `/oc review`** on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
5. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
6. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
7. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Will Component A (color cache) clear the ~0.10 bpp WebP gap on REAL Kodak?** A is the most plausible single win (chroma decorrelation); B already reached JPEG-LS (9.71). JPEG XL 8.71 needs ~1.0 bpp more - UNCERTAIN, may require R7.
- **Is Component B truly conditioning now (`cmarc-force+resctx` != `cmarc-force`)?** Mandatory test `r3a_residual_context_changes_quotient_stream` gates this; result shows tiny per-image deltas (e.g. kodim04 9.5860 -> 9.5813) confirming it actually conditions, no regression.
- **Merge gate (owner override #2):** NOT met - default 9.7067 bpp > WebP 9.61 > JXL 8.71. Even best CMARC+R3-A misses WebP by ~0.10 and JXL by ~1.0.
- **Review staleness:** last approve at head ~96a6075; current head `0efc83c` (Component B) un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.
- **Orphan-main break:** RESOLVED (PR MERGEABLE). Branch re-linked to main; no new PR needed.
- **Trigger storm:** sibling maintainer runs may also emit `continue`; the Builder re-implements the corrected R6 idempotently (no harm). This run deliberately did NOT re-fire `continue` because run `32238473667` is already in flight.

- Mae, the Maintainer
