# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~09:06Z, maintainer run 32235660749 on PR #83). **DECISIONS:** `[{"action":"continue","pr":83}]` - resume the Builder on the single Obsidian PR to implement the corrected R6 blueprint (Component B quotient-context fix -> A color cache -> C tuned matches), re-measuring REAL Kodak reproducibly. No merge (default ~9.76 bpp still above WebP 9.61 / JPEG XL 8.71); one PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RESOLVED; rebase satisfied)

- **Mergeability (FIXED):** PR #83 OPEN, head `f137881eb9339a4d152c757c615306c4be13df04`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. `git merge-base origin/main opencode/issue68-20260818070512` == `8f4c15b` (== origin/main), verified live this run. Branch is 11 commits ahead of `main`. `--rebase` is possible whenever the gate is met. No new PR needed.
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is now measurable reproducibly.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `f137881`). Real Kodak (effort 4) numbers, 24-image PCD0992 set:
  - **DEFAULT shipped codec = CMARC (auto-selected best of {GR, CMARC, CARC_LZ, CARC_MIX}, never-expand safety net): ~9.76 bpp mean** - at the JPEG-LS floor (JPEG-LS = 9.71 on the same corpus). PNG 13.05 MET; WebP 9.61 MISSED by ~0.15 bpp; JPEG XL 8.71 MISSED by ~0.85 bpp. Bit-exact (8000 fuzz, CRC).
- **CMARC lineage (R1 -> R5) built; entropy core now correct (CACM87):**
  - **R4 coder = CACM87 (Witten-Neal-Cleary binary arithmetic coder)** - proven correct; efficiency gates pass (ratio < 1.10/1.20).
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` learns the geometric quotient like JPEG-LS QM; dropped forced CARC 11.11 -> 9.71 bpp.
  - **R3-C (JPEG-LS run mode):** implemented; neutral on real Kodak.
  - All CMARC variants ship behind the never-expand safety net, which now ALSO engages by default.
- **R6 blueprint DELIVERED, then CORRECTED (this run):**
  - First R6 blueprint (commit `2152825`): R6-A pixel-domain spatial LZ77 + R6-B color cache. The Builder proved R6-A is a **functionally byte-for-byte duplicate** of existing `CARC_LZ` (decoder copies `plane[i-off+l]` from its own reconstructed prefix), which ties on photos because exact pixel repeats of length >= `MIN_MATCH=3` are rare (commit `7170586`, `.github/agents/decisions/builder/2026-08-19-r6a-carc-lz-already-pixel-domain.md`).
  - **Corrected R6 blueprint (commit `f137881`, `obsidian/docs/architect-r6-corrected-blueprint.md`):** keeps `CARC_LZ`, prescribes:
    - **Component B (R3-A fix, build FIRST):** condition the Rice *quotient* bins (not the remainder) on the JPEG-LS residual DIFF context (`residual_context(dL,dU,dUl)`); mandatory test that `cmarc-force+resctx` is no longer byte-identical to `cmarc-force`. Target ≤ 9.71 (JPEG-LS), ideally < 9.61 (WebP).
    - **Component A (R6-B color cache, primary sub-9.61 lever):** per-plane LRU (default 512), `cache_flag` + recency-ranked index via CMARC bins, new `ENTROPY_MODE_CARC_CACHE = 6`, mirrored decoder, `use_color_cache` seam + safety net.
    - **Component C (tuned matches):** `MIN_MATCH = 2` + 2D distance model + cache competition (marginal on photos).
    - **Component D (R6-C multi-channel copy, deferred):** only if A+B+C still > 8.71.
    - **Honest risk:** B should reach JPEG-LS; B+A plausibly clears WebP; JPEG XL 8.71 UNCERTAIN (may need a separate R7 adaptive weighted predictor / MA-tree). The Architect does NOT promise JPEG XL from R6 alone.

## In flight

- **Builder (this run, resume via `continue`):** implement corrected R6 in build order B -> A -> C, re-measuring REAL Kodak effort-4 reproducibly (PCD0992 durable in git). Keep every prior seam OFF by default behind the never-expand net. Must add the mandatory `cmarc-force+resctx != cmarc-force` test for Component B.
- **Architect (done this run):** corrected R6 blueprint delivered (commit `f137881`). Returns `continue` for the Builder on the same branch.
- **Review is STALE:** last `/oc approve` was at 2026-08-18 07:52Z (head ~`96a6075`); since then CMARC default switch (R4/R5/R3-C), R2.1-R2.4, the R6 finding + corrected R6. A fresh strict review is required before any merge, but deferred until the codec stabilizes near the gate.
- No Researcher / Factory in flight.

## PENDING (deferred)

- **Clear WebP 9.61 gate:** default ~9.76 is ~0.15 above; corrected R6 Component B (quotient-context) + A (color cache) are the most plausible single/combined win.
- **Clear JPEG XL 8.71 gate:** ~0.85 bpp above; the hard long pole - needs B+A+C and possibly R6-C, and even then UNCERTAIN (may need R7).
- **Verify/fix R3-A residual-context no-op** (Component B) - free additive win once wired.
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near).
- **Factory infra hardening:** `continue-on-error` still pending but non-blocking.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `f137881`, `mergeable: MERGEABLE` (orphan break resolved). Corrected R6 blueprint delivered; Builder resumes via `continue` this run. No held runs.
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Builder resumes via `continue` (this run's trigger)** to implement corrected R6 Component B (quotient-context fix + mandatory test), then A (color cache), then C (tuned matches), re-measuring REAL Kodak effort-4 reproducibly.
2. **After B+A land:** re-measure real Kodak; if WebP 9.61 cleared, continue with C then D (if JPEG XL needs it).
3. **After gates re-measured:** assess whether the *default* Obsidian mean bpp is now < 9.61 (WebP) AND < 8.71 (JXL) AND < 13.05 (PNG), reproducible + bit-exact. If WebP cleared but JXL not, re-fire `continue` for more; if JXL cleared, proceed to merge prep.
4. **Re-fire strict `/oc review`** on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
5. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
6. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
7. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Will corrected R6 (B->A->C) clear the ~0.15 bpp WebP gap on REAL Kodak?** B (quotient-context, faithful QM) should reach JPEG-LS ~9.71; A (color cache) is the most plausible single win toward < 9.61. JPEG XL 8.71 needs ~0.85 bpp more - UNCERTAIN, may require R7 (Architect explicitly does not promise JPEG XL from R6 alone).
- **Is R3-A residual-context truly a no-op, and can B unstick it?** Blueprint admits `cmarc-force+resctx` == `cmarc-force` byte-for-byte today; Component B must wire the quotient bins to the residual DIFF context so it actually conditions (mandatory test gates this).
- **Merge gate (owner override #2):** NOT met - default ~9.76 bpp > WebP 9.61 > JXL 8.71. Even best auto-selected (~9.76) misses WebP by ~0.15 and JXL by ~0.85.
- **Review staleness:** last approve at head ~96a6075; current head `f137881` (CMARC default + corrected R6) un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.
- **Orphan-main break:** RESOLVED (PR MERGEABLE). Branch re-linked to main; no new PR needed.
- **Trigger storm:** sibling maintainer runs (574/575 in this batch) may also emit `continue`; the Builder re-implements the corrected R6 idempotently (no harm).

- Mae, the Maintainer
