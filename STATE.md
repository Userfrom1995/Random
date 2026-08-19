# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~08:53Z, maintainer run 32234772744 on PR #83). **DECISIONS:** `[{"action":"architect","pr":83}]` - re-engage the Architect on the single Obsidian PR to deliver a *corrected* R6 blueprint, because the current R6-A stage is a byte-for-byte duplicate of existing `CARC_LZ` (Builder proved it ties at ~13.6 bpp). No merge (default ~9.76 bpp still above WebP 9.61 / JPEG XL 8.71); one PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RESOLVED; rebase satisfied)

- **Mergeability (FIXED):** PR #83 OPEN, head `7170586765953f38ddd7d93545a54a293e1427be`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. `git merge-base origin/main opencode/issue68-20260818070512` == `8f4c15b` (== origin/main), verified live this run. Branch is 10 commits ahead of `main`. `--rebase` is possible whenever the gate is met. No new PR needed.
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is now measurable reproducibly.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `7170586`). Real Kodak (effort 4) numbers, 24-image PCD0992 set:
  - **DEFAULT shipped codec = CMARC (auto-selected best of {GR, CMARC, CARC_LZ, CARC_MIX}, never-expand safety net): ~9.76 bpp mean** - at the JPEG-LS floor (JPEG-LS = 9.71 on the same corpus). PNG 13.05 MET; WebP 9.61 MISSED by ~0.15 bpp; JPEG XL 8.71 MISSED by ~0.85 bpp. Bit-exact (8000 fuzz, CRC).
- **CMARC lineage (R1 -> R5) built; entropy core now correct (CACM87):**
  - **R4 coder = CACM87 (Witten-Neal-Cleary binary arithmetic coder)** - proven correct; efficiency gates pass (ratio < 1.10/1.20).
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` learns the geometric quotient like JPEG-LS QM; dropped forced CARC 11.11 -> 9.71 bpp.
  - **R3-C (JPEG-LS run mode):** implemented; neutral on real Kodak.
  - All CMARC variants ship behind the never-expand safety net, which now ALSO engages by default.
- **R6 blueprint DELIVERED then FOUND WRONG (this run):**
  - Architect delivered R6 blueprint (head `2152825`): R6-A pixel-domain spatial LZ77 (`ENTROPY_MODE_CARC_SPATIAL = 5`) + R6-B color cache; premise that existing `CARC_LZ` is "residual-domain" and therefore ties.
  - Builder resumed R6-A (run `32234283576`) and PROVED the premise wrong: `CARC_LZ` (`ENTROPY_MODE_CARC_LZ = 3`) is ALREADY pixel-domain spatial LZ77 (decoder copies `plane[i-off+l]`, encoder match finder on pixel-valued buffer). It ties (forced 13.62 bpp on kodim01) only because photographic content has too few exact repeats of length >= `MIN_MATCH=3` to amortize match overhead. Implementing R6-A as specified would be a byte-for-byte duplicate of `CARC_LZ` -> dead code. Builder did NOT implement it and recorded the finding (head `7170586`, `.github/agents/decisions/builder/2026-08-19-r6a-carc-lz-already-pixel-domain.md`).
  - **Builder is BLOCKED** awaiting a corrected R6 blueprint. This run re-engages the Architect (Mode 2) on PR #83 to correct it: drop the pixel-LZ duplicate, prescribe **R6-B (LRU color cache)** as the primary new stage, specify a **genuinely more aggressive match finder** (2D block copy / lower match cost / richer match-flag+offset+length context), and **unstick R3-A residual-context** (currently a no-op).

## In flight

- **Architect (this run, re-engage):** deliver the *corrected* R6 blueprint on PR #83 - R6-B color cache (primary new win) + a real aggressive match finder (2D block copy) + unstick R3-A residual-context. Returns `continue` for the Builder on the same branch.
- **Builder (blocked, not in flight):** awaiting the corrected R6 blueprint; will implement R6-B + match-finder + R3-A fix and re-measure REAL Kodak effort-4. Must NOT implement a `CARC_SPATIAL` duplicate of `CARC_LZ`.
- **Review is STALE:** last `/oc approve` was at 2026-08-18 07:52Z (head ~`96a6075`); since then CMARC default switch (R4/R5/R3-C), R2.1-R2.4, LZ77-tie, the R6 finding. A fresh strict review is required before any merge, but deferred until the codec stabilizes near the gate.
- No Researcher / Factory in flight.

## PENDING (deferred)

- **Corrected R6 blueprint (Architect, this run):** R6-B color cache + aggressive 2D match finder + unstick R3-A.
- **Clear WebP 9.61 gate:** default ~9.76 is ~0.15 above; R6-B color cache is the most plausible single win.
- **Clear JPEG XL 8.71 gate:** ~0.85 bpp above; the hard long pole - needs R6-B + aggressive match finder (and possibly R6-C).
- **Verify/fix R3-A residual-context no-op** (blueprint flag) - free additive win once wired.
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near).
- **Factory infra hardening:** `continue-on-error` still pending but non-blocking.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `7170586`, `mergeable: MERGEABLE` (orphan break resolved). Architect re-engaged this run; Builder blocked on corrected R6 blueprint. No held runs.
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Architect delivers corrected R6 blueprint** (this run's `architect` trigger) on PR #83.
2. **Builder resumes via `continue`** to implement R6-B (color cache) + genuinely aggressive 2D match finder + R3-A unstick, re-measuring REAL Kodak effort-4 reproducibly (Kodak PPMs durable in git).
3. **After R6-B lands:** re-measure real Kodak; if WebP not cleared, continue with the aggressive match finder, then R6-C if JPEG XL needs it.
4. **After gates re-measured:** assess whether the *default* Obsidian mean bpp is now < 9.61 (WebP) AND < 8.71 (JXL) AND < 13.05 (PNG), reproducible + bit-exact. If WebP cleared but JXL not, re-fire `continue` for more; if JXL cleared, proceed to merge prep.
5. **Re-fire strict `/oc review`** on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
6. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
7. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
8. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Will the corrected R6 (color cache + aggressive match finder + unstick R3-A) clear the ~0.15 bpp WebP gap on REAL Kodak?** Color cache most plausible; aggressive match finder is the real structural lever for WebP and beyond; JPEG XL 8.71 needs ~0.85 bpp more (hard long pole).
- **Is R3-A residual-context truly a no-op, and can it be unstuck?** Blueprint admits `cmarc-force+resctx` == `cmarc-force` byte-for-byte; the corrected R6 must wire it to actually condition (JPEG-LS DIFF context).
- **Merge gate (owner override #2):** NOT met - default ~9.76 bpp > WebP 9.61 > JXL 8.71. Even forced CARC (9.71) and best auto-selected (~9.76) miss WebP by ~0.15 and JXL by ~0.85.
- **Review staleness:** last approve at head ~96a6075; current head `7170586` has the CMARC default + R6 finding un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.
- **Orphan-main break:** RESOLVED (PR MERGEABLE). Branch re-linked to main; no new PR needed.
- **Trigger storm:** sibling maintainer runs may also emit `architect`; Architect re-blueprints idempotently (no harm).

- Mae, the Maintainer
