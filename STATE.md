# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~11:00Z, maintainer run 32245495266 on PR #83). **DECISIONS:** `[]` (no trigger) - the R7 Architect pass is already in flight (run `32245495346`, owner `/oc architect` 11:00:43Z), so no duplicate. The Architect will write `continue` on delivery, resuming the Builder on the same branch to implement R7 (QM-class adaptive coder conditioned on neighbor-residual DIFF context WITHOUT per-(cid,bin) model starvation) and re-measure on reproducible real Kodak. No merge; one PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RESOLVED; rebase satisfied)

- **Mergeability (FIXED):** PR #83 OPEN, head `1415814` (`14158142845f617562443f468ed1453033b3712e`), `mergeable: MERGEABLE`, base `8f4c15b` (== origin/main), valid merge base (verified live this run). `--rebase` is possible whenever the gate is met. No new PR needed.
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is now measurable reproducibly.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `1415814`). Real Kodak (effort 4) numbers, 24-image PCD0992 set (reproducible, durably committed corpus):
  - **DEFAULT shipped codec = CMARC auto-selected best = 9.7093 bpp mean.** Beats JPEG-LS (9.71); PNG 13.05 MET; **WebP 9.61 MISSED by ~0.10 bpp** (14+ of 24 above); **JPEG XL 8.71 MISSED by ~1.0 bpp** (22 of 24 above). Bit-exact.
  - **KEY DIAGNOSIS (empirical, not theoretical):** the codec has hit the **JPEG-LS floor (~9.71)**, and the remaining gap is gated by the **entropy-model structure**, not by prediction or transforms. Two attempts to exploit a neighbor-residual context both failed:
    - **R3-A residual-context is INERT.** `cmarc-force+resctx` == `cmarc-force` byte-for-byte on every Kodak image. The per-`(cid,bin)` binary-model table balloons to ~365x contexts under the JPEG-LS DIFF context; each rare bin stays pinned at its prior and emits the same bits as the non-context path. The Builder tried to fix it twice (`0efc83c`, `311c5bc`) and it stayed a no-op. The 9.7093 headline is entirely from R5 (Rice quotient fix).
    - **R6-B color cache is a DEAD END.** Forced `ENTROPY_MODE_CARC_CACHE=6` (size-32 = 12.88 bpp; size-512 = 14.58 bpp) regresses; the never-expand net correctly never selects it. The binary-coder floor exceeds the cache's savings on low-entropy photographic residuals.
  - So: R3-A (context) and R6-B (cache) are both exhausted as levers on the current per-(cid,bin) model design. The structural fix is a QM-class coder (context selects a small adaptive state / Rice parameter on a single shared binary arithmetic coder, JPEG-LS style) that does not starve.
- **CMARC lineage (R1 -> R5) built; entropy core correct (CACM87):**
  - **R4 coder = CACM87 (Witten-Neal-Cleary binary arithmetic coder)** - proven correct; efficiency gates pass (ratio < 1.10/1.20).
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` learns the geometric quotient like JPEG-LS QM; dropped forced CARC 11.11 -> 9.71 bpp. This is what actually delivers the 9.7093 headline.
  - **Faithful R3-A (residual DIFF context conditions the whole CMARC residual):** wired at `311c5bc`, but **currently a NO-OP** (model-starvation; `cmarc-force+resctx` == `cmarc-force`).
  - **R3-C (JPEG-LS run mode):** implemented; neutral on real Kodak.
  - All CMARC variants ship behind the never-expand safety net, which now ALSO engages by default.
- **R6 blueprint DELIVERED + CORRECTED (`f137881`), but its central premise is now disproven:** R6-A (pixel-domain LZ77) is a byte-for-byte duplicate of existing `CARC_LZ` (Builder finding `7170586`, proven to tie), and R6-B (color cache) is a dead end (this run's Builder escalation, head `1415814`). Only Component B (R3-A quotient-context) was absorbed into R5.

## In flight

- **Architect (run `32245495346`, owner `/oc architect` 11:00:43Z):** design **R7** - a QM-class adaptive entropy coder conditioned on the neighbor-residual DIFF context WITHOUT the per-(cid,bin) model multiplication that made R3-A inert. The context should select a small adaptive state / Rice parameter on a single shared binary arithmetic coder (JPEG-LS QM style) so rare contexts adapt quickly instead of starving. Target: clear WebP 9.61 first, then JXL 8.71. Deliver the blueprint on PR #83; then the Builder resumes via `continue` (the Architect run writes `continue` on delivery).
- **No Builder / Researcher / Factory in flight.** Corrected R6 blueprint present and empirically disproven (R6-B dead, R3-A inert); R7 Architect pass is the active step.
- **Review is STALE:** last `/oc approve` was at 2026-08-18 07:52Z (head ~`96a6075`); current head `1415814` un-reviewed. Fresh strict review required before any merge, deferred until the codec stabilizes near the gate.

## PENDING (deferred)

- **Clear WebP 9.61 gate:** default 9.7093 is ~0.10 above; R7 (QM-class coder on neighbor-residual context) is the most plausible single structural fix.
- **Clear JPEG XL 8.71 gate:** ~1.0 bpp above; the hard long pole - likely needs R7 + possibly beyond (weighted predictor / context tree / LZ77 re-woven).
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near).
- **Factory infra hardening:** `continue-on-error` still pending but non-blocking.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `1415814`, `mergeable: MERGEABLE` (orphan break resolved). R6-B proven dead end; R3-A inert; default 9.7093 (PNG + JPEG-LS met; WebP/JXL unmet). R7 Architect in flight (run `32245495346`).
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Architect delivers R7 blueprint on PR #83 (run `32245495346` in flight):** QM-class adaptive coder conditioned on neighbor-residual DIFF context without per-(cid,bin) model starvation. Targets WebP 9.61 then JXL 8.71.
2. **After R7 blueprint lands (Architect writes `continue`):** resume Builder via `continue` to implement R7, re-measuring REAL Kodak effort-4 reproducibly on the durably committed corpus. Keep every prior seam OFF by default behind the never-expand net.
3. **If R7 design cannot plausibly clear WebP:** that finding escalates to the Researcher for a deeper algorithmic redesign (do not loop on band-aids). Do NOT merge until all three gates clear.
4. **Re-fire strict `/oc review`** on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
5. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
6. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
7. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Can a QM-class coder (context selects a small adaptive state on a single shared arithmetic coder) exploit the neighbor-residual DIFF context without starving?** This is the exact JPEG-LS mechanism and is the proven path below 9.71; R3-A failed only because it multiplied independent per-(cid,bin) models. R7 must avoid that.
- **Will R7 clear the ~0.10 bpp WebP gap?** Most plausible structural single win. JXL (~1.0 bpp) likely needs more (weighted predictor / context tree / LZ77).
- **Merge gate (owner override #2):** NOT met - default 9.7093 bpp > WebP 9.61 > JXL 8.71. Even best CMARC+R5 beats JPEG-LS but misses WebP by ~0.10 and JXL by ~1.0.
- **Review staleness:** last approve at head ~96a6075; current head `1415814` un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.
- **Orphan-main break:** RESOLVED (PR MERGEABLE). Branch re-linked to main; no new PR needed.

- Mae, the Maintainer
