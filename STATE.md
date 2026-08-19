# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~07:58Z, maintainer run 32230364132 on PR #83). **DECISIONS:** `[{"action":"continue","pr":83}]` - resume the Builder to implement R2.4 (logistic context mixing) on the correct CACM87 core toward the WebP 9.61 / JPEG XL 8.71 gates. Default codec is now CMARC (~9.71 bpp best). No Builder build in flight, so no duplicate. Orphan-main break RESOLVED (PR MERGEABLE, merge-base == origin/main). One PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RESOLVED; rebase satisfied)

- **Mergeability (FIXED):** PR #83 OPEN, head `e3add6a9e9d6548b32bf976ca39f46ec6167d871`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. `git merge-base origin/main opencode/issue68-20260818070512` == `8f4c15b` (== origin/main) - verified live this run. The Builder's re-anchor commits (`833597f`, `058e045`, `75e2eaa`) plus the durable Kodak corpus keep the branch re-linked to `main`, so `--rebase` is possible whenever the gate is met. No new PR needed.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `e3add6a`). Real Kodak (effort 4) numbers, 24-image PCD0992 set:
  - **DEFAULT shipped codec = CMARC + subtract-green (never-expand net per-image auto-selects best of {GR, CMARC, CARC_LZ, CARC_MIX}): ~9.71 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by ~0.10 bpp; JPEG XL 8.71 MISSED by ~1.0 bpp). Bit-exact (8000 fuzz, CRC).
  - Forced CARC mean = 9.7579; gr = 10.0906. The safety-net default number that actually ships is ~9.71.
  - Default `encode()` now engages CMARC unless `OBSIDIAN_CARC=0`; cross-channel subtract-green defaults ON when CMARC is on.
- **CMARC lineage (R1 -> R5) built; entropy core now correct (CACM87):**
  - **R4 coder = CACM87 (Witten-Neal-Cleary binary arithmetic coder)** - proven correct; efficiency gates `range_coder_skew_efficiency` + `cmarc_efficiency_vs_shannon` PASS (ratio < 1.10/1.20).
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` learns the geometric quotient like JPEG-LS QM; dropped forced CARC 11.11 -> 9.71 bpp.
  - **R3-C (JPEG-LS run mode):** implemented; neutral on real Kodak.
  - All CMARC variants ship behind the never-expand safety net, which now ALSO engages by default.

## In flight

- **Builder (resume via `continue`, fired this run):** implement **R2.4 (logistic context mixing / per-context prediction refinement)** on the correct CACM87 core to close the ~0.10 bpp gap to WebP 9.61, re-measuring real Kodak effort-4 reproducibly. R2.4 previously regressed on synthetic; it must be validated on REAL Kodak and only shipped if the safety net confirms a win (no regression). If WebP clears, continue toward JPEG XL 8.71 (~1.0 bpp further - the hard long pole). No Builder run was in flight before this `continue`, so it is not a duplicate.
- **Review is STALE:** last `/oc approve` was at 2026-08-18 07:52Z (head ~`96a6075`); since then the CMARC default switch (R4/R5/R3-C + Kodak corpus) was added. A fresh strict review is required before any merge, but deferred until the codec stabilizes near the gate.
- No Architect / Researcher in flight.

## PENDING (deferred)

- **Clear WebP 9.61 gate:** default ~9.71 is ~0.10 above; R2.4 must close it.
- **Clear JPEG XL 8.71 gate:** ~1.0 bpp above; the hard long pole - needs R2.4 + re-tuned mixing, possibly beyond the current blueprint.
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near).
- **Factory infra hardening:** `continue-on-error` still pending but non-blocking.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `e3add6a`, `mergeable: MERGEABLE` (orphan break resolved). Builder `continue` fired this run (single). No held runs.
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Let the `continue` Builder resume** (this run) - implement R2.4, then re-measure real Kodak effort-4 reproducibly and confirm a win via the safety net.
2. **After it lands + re-measures:** assess whether the *default* Obsidian mean bpp is now < 9.61 (WebP) AND < 8.71 (JXL) AND < 13.05 (PNG), reproducible + bit-exact. If WebP cleared but JXL not, re-fire `continue` for more context mixing/LZ77; if JXL cleared, proceed to merge prep.
3. **Re-fire strict `/oc review`** on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
4. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
5. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
6. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Will R2.4 close the ~0.10 bpp WebP gap on REAL Kodak?** Plausible on CACM87 (H(p)+epsilon); the safety net must confirm a win (no regression). JPEG XL 8.71 needs ~1.0 bpp more - the hard long pole.
- **Merge gate (owner override #2):** NOT met - default ~9.71 bpp > WebP 9.61 > JXL 8.71. Even forced CARC (9.7579) and best auto-selected (~9.71) miss WebP by ~0.10 and JXL by ~1.0.
- **Review staleness:** last approve at head ~96a6075; current head `e3add6a` has the CMARC default switch un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.
- **Orphan-main break:** RESOLVED (PR MERGEABLE). Branch re-anchored onto main; no new PR needed.

- Mae, the Maintainer
