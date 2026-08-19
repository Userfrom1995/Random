# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~08:20Z, maintainer run 32232110789 on PR #83). **DECISIONS:** `[{"action":"architect","pr":83}]` - engage the Architect (Mode 2) on the single Obsidian PR to design the pixel-domain LZ77 + WebP/JPEG XL-class pipeline, because the Builder's own measurement shows residual-domain LZ77 ties at the JPEG-LS floor (~9.71 bpp) and the WebP gap needs pixel-domain LZ77. No Architect in flight, so no duplicate. Merge gate still unmet; one PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RESOLVED; rebase satisfied)

- **Mergeability (FIXED):** PR #83 OPEN, head `39f7255055867d29575067bc624e5833fe06ddb3`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. `git merge-base origin/main opencode/issue68-20260818070512` == `8f4c15b` (== origin/main) - verified live this run. `--rebase` is possible whenever the gate is met. No new PR needed.
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is now measurable reproducibly.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `39f7255`). Real Kodak (effort 4) numbers, 24-image PCD0992 set:
  - **DEFAULT shipped codec = CMARC + subtract-green (never-expand net per-image auto-selects best of {GR, CMARC, CARC_LZ, CARC_MIX}): ~9.71 bpp mean** - at the JPEG-LS floor (JPEG-LS = 9.71 on the same corpus). PNG 13.05 MET; WebP 9.61 MISSED by ~0.10 bpp; JPEG XL 8.71 MISSED by ~1.0 bpp. Bit-exact (8000 fuzz, CRC).
  - Forced CARC mean = 9.7579; gr = 10.0906. The safety-net default number that actually ships is ~9.71.
  - Default `encode()` now engages CMARC unless `OBSIDIAN_CARC=0`; cross-channel subtract-green defaults ON when CMARC is on.
- **CMARC lineage (R1 -> R5) built; entropy core now correct (CACM87):**
  - **R4 coder = CACM87 (Witten-Neal-Cleary binary arithmetic coder)** - proven correct; efficiency gates pass (ratio < 1.10/1.20).
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` learns the geometric quotient like JPEG-LS QM; dropped forced CARC 11.11 -> 9.71 bpp.
  - **R3-C (JPEG-LS run mode):** implemented; neutral on real Kodak.
  - All CMARC variants ship behind the never-expand safety net, which now ALSO engages by default.
- **Builder's latest finding (`39f7255`):** residual-domain LZ77 (R2.3 / R3-style) **ties** - the strong R2 predictor bank removes the exact repeats LZ would copy, so LZ adds no gain. The Builder concludes the WebP gap "needs pixel-domain LZ77" - a WebP/JPEG XL-class pipeline where LZ77 operates on the reconstructed pixel/transform buffer with a color cache.

## In flight

- **Architect (engaged this run, `architect` on PR #83):** design the pixel-domain LZ77 + WebP/JPEG XL-class transform/color-cache pipeline to push below the JPEG-LS 9.71 floor toward WebP 9.61, then JPEG XL 8.71. No Architect currently running; this is the first trigger for this stage.
- **Builder (resume via `continue` after the Architect blueprint lands):** implement pixel-domain LZ77 + transform integration on the same branch, re-measuring real Kodak effort-4 reproducibly. NOT yet triggered this run (needs the blueprint first).
- **Review is STALE:** last `/oc approve` was at 2026-08-18 07:52Z (head ~`96a6075`); since then CMARC default switch (R4/R5/R3-C), R2.1-R2.3, and the LZ77 work were added. A fresh strict review is required before any merge, but deferred until the codec stabilizes near the gate.
- No Researcher / Factory in flight.

## PENDING (deferred)

- **Clear WebP 9.61 gate:** default ~9.71 is ~0.10 above; pixel-domain LZ77 (per upcoming Architect blueprint) is the path.
- **Clear JPEG XL 8.71 gate:** ~1.0 bpp above; the hard long pole - needs pixel-domain LZ77 + color cache + likely re-tuned mixing, possibly beyond the current blueprint.
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near).
- **Factory infra hardening:** `continue-on-error` still pending but non-blocking.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `39f7255`, `mergeable: MERGEABLE` (orphan break resolved). Architect `architect` fired this run (single). No held runs.
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Let the Architect deliver the pixel-domain LZ77 blueprint** (this run) on PR #83.
2. **After it lands:** resume the Builder via `continue` to implement pixel-domain LZ77 + transform integration, then re-measure real Kodak effort-4 reproducibly and confirm a win via the safety net.
3. **After it lands + re-measures:** assess whether the *default* Obsidian mean bpp is now < 9.61 (WebP) AND < 8.71 (JXL) AND < 13.05 (PNG), reproducible + bit-exact. If WebP cleared but JXL not, re-fire `continue` for more; if JXL cleared, proceed to merge prep.
4. **Re-fire strict `/oc review`** on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
5. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
6. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
7. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Will pixel-domain LZ77 clear the ~0.10 bpp WebP gap on REAL Kodak?** Plausible: WebP/JPEG XL reach 9.61/8.71 precisely because they LZ77 the pixel/transform buffer, which residual-domain LZ77 cannot do. JPEG XL 8.71 needs ~1.0 bpp more - the hard long pole.
- **Merge gate (owner override #2):** NOT met - default ~9.71 bpp > WebP 9.61 > JXL 8.71. Even forced CARC (9.7579) and best auto-selected (~9.71) miss WebP by ~0.10 and JXL by ~1.0.
- **Review staleness:** last approve at head ~96a6075; current head `39f7255` has the CMARC default + LZ77 work un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.
- **Orphan-main break:** RESOLVED (PR MERGEABLE). Branch re-linked to main; no new PR needed.
- **Trigger storm:** several maintainer runs fired in quick succession at 08:20Z; decision `architect` on PR #83 is the single needed step.

- Mae, the Maintainer
