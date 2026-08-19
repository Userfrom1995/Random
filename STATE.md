# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~08:35Z, maintainer run 32232990068 on PR #83). **DECISIONS:** `[{"action":"continue","pr":83}]` - resume the Builder on the single Obsidian PR to implement the R6 spatial pixel-domain LZ77 blueprint (Architect delivered at head `2152825`). No merge (default 9.7579 bpp still above WebP 9.61 / JPEG XL 8.71); one PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RESOLVED; rebase satisfied)

- **Mergeability (FIXED):** PR #83 OPEN, head `2152825c66fed85590b859a6d1b63ed5f84e1792`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. `git merge-base origin/main opencode/issue68-20260818070512` == `8f4c15b` (== origin/main) - verified live this run. `--rebase` is possible whenever the gate is met. No new PR needed.
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is now measurable reproducibly.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `2152825`). Real Kodak (effort 4) numbers, 24-image PCD0992 set:
  - **DEFAULT shipped codec = CMARC + R5 Rice-quotient + subtract-green (never-expand net per-image auto-selects best of {GR, CMARC, CARC_LZ, CARC_MIX}): ~9.7579 bpp mean** - at the JPEG-LS floor (JPEG-LS = 9.71 on the same corpus). PNG 13.05 MET; WebP 9.61 MISSED by ~0.15 bpp; JPEG XL 8.71 MISSED by ~0.85 bpp. Bit-exact (8000 fuzz, CRC).
  - Forced CARC mean = 9.7579; gr = 10.0906. The safety-net default number that actually ships is ~9.7579.
  - Default `encode()` now engages CMARC unless `OBSIDIAN_CARC=0`; cross-channel subtract-green defaults ON when CMARC is on.
- **CMARC lineage (R1 -> R5) built; entropy core now correct (CACM87):**
  - **R4 coder = CACM87 (Witten-Neal-Cleary binary arithmetic coder)** - proven correct; efficiency gates pass (ratio < 1.10/1.20).
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` learns the geometric quotient like JPEG-LS QM; dropped forced CARC 11.11 -> 9.71 bpp.
  - **R3-C (JPEG-LS run mode):** implemented; neutral on real Kodak.
  - All CMARC variants ship behind the never-expand safety net, which now ALSO engages by default.
- **Builder's latest finding (`39f7255`):** residual-domain LZ77 (R2.3 / CARC_LZ / R3-style) **ties** - the strong R2 predictor bank removes the exact repeats LZ would copy, so LZ adds no gain. The Builder concludes the WebP gap "needs pixel-domain LZ77" (over the reconstructed raster + color cache).
- **R6 blueprint DELIVERED (head `2152825`, Architect run `32232599584`, 08:30Z):** `obsidian/docs/architect-r6-spatial-lz77-blueprint.md`. Design: R6-A per-plane spatial back-reference over `recon[c]` (literal = CMARC residual; match = copy from reconstructed buffer, decoder copies from its own buffer -> bit-exact by induction), new `ENTROPY_MODE_CARC_SPATIAL = 5` signaled in `model.entropy_mode` (no header flag bit); R6-B per-plane LRU color cache; R6-C multi-channel copy deferred. Also flags R3-A residual-context is a NO-OP (`cmarc-force+resctx` == `cmarc-force` byte-for-byte) and must be wired before stacking. Targets: R6-A -> WebP (< 9.61), R6-B -> JPEG XL (< 8.71).

## In flight

- **Builder (resume via `continue`, this run):** implement R6-A (spatial pixel-domain LZ77) on the single branch, re-measure REAL Kodak effort-4 reproducibly, and confirm a win via the never-expand safety net (no regression). Must also verify/fix R3-A residual-context (currently no-op) per the blueprint. After R6-A lands, R6-B (color cache) follows if WebP is not yet cleared; R6-C only if needed for JPEG XL. NOT yet triggered this run (the decision fires it).
- **Architect (delivered, not in flight):** R6 blueprint is on the branch; no further Architect needed unless R6-A/B fails on real Kodak.
- **Review is STALE:** last `/oc approve` was at 2026-08-18 07:52Z (head ~`96a6075`); since then CMARC default switch (R4/R5/R3-C), R2.1-R2.3, LZ77-tie, and the R6 blueprint were added. A fresh strict review is required before any merge, but deferred until the codec stabilizes near the gate.
- No Researcher / Factory in flight.

## PENDING (deferred)

- **Clear WebP 9.61 gate:** default ~9.7579 is ~0.15 above; R6-A spatial LZ77 is the path.
- **Clear JPEG XL 8.71 gate:** ~0.85 bpp above; the hard long pole - R6-B color cache (and possibly R6-C) likely needed.
- **Verify/fix R3-A residual-context no-op** (blueprint flag) - likely a free win before stacking context.
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near).
- **Factory infra hardening:** `continue-on-error` still pending but non-blocking.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `2152825`, `mergeable: MERGEABLE` (orphan break resolved). Architect R6 delivered; Builder `continue` fired this run. No held runs.
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Let the Builder implement R6-A** (this run's `continue`) on PR #83.
2. **After R6-A lands:** re-measure real Kodak effort-4 reproducibly; if WebP not cleared, continue to R6-B (color cache), then R6-C if JPEG XL needs it. Verify/fix R3-A no-op along the way.
3. **After gates re-measured:** assess whether the *default* Obsidian mean bpp is now < 9.61 (WebP) AND < 8.71 (JXL) AND < 13.05 (PNG), reproducible + bit-exact. If WebP cleared but JXL not, re-fire `continue` for more; if JXL cleared, proceed to merge prep.
4. **Re-fire strict `/oc review`** on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
5. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
6. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
7. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Will R6-A spatial LZ77 clear the ~0.15 bpp WebP gap on REAL Kodak?** Plausible (WebP/JPEG XL LZ77 the pixel buffer); JPEG XL 8.71 needs ~0.85 bpp more (R6-B + possibly R6-C).
- **Is R3-A residual-context truly a no-op?** Blueprint flags `cmarc-force+resctx` == `cmarc-force` byte-for-byte; Builder must diagnose and fix.
- **Merge gate (owner override #2):** NOT met - default ~9.7579 bpp > WebP 9.61 > JXL 8.71. Even forced CARC (9.7579) and best auto-selected (~9.7579) miss WebP by ~0.15 and JXL by ~0.85.
- **Review staleness:** last approve at head ~96a6075; current head `2152825` has the CMARC default + R6 blueprint un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.
- **Orphan-main break:** RESOLVED (PR MERGEABLE). Branch re-linked to main; no new PR needed.
- **Trigger storm:** a sibling maintainer run (`32233004251`, 08:31:11Z) may also emit `continue`; Builder resumes idempotently from the progress file (no harm).

- Mae, the Maintainer
