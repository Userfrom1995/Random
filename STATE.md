# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~10:36Z, maintainer run 32243491358 on PR #83). **DECISIONS:** `continue` PR #83 - resume the Builder to fix the R3-A residual-context INERT bug test-first (mandatory `cmarc-force+resctx != cmarc-force` test), and NOT re-measure the proven-dead R6-B color cache. No merge (default 9.7094 bpp still above WebP 9.61 / JPEG XL 8.71); one PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RESOLVED; rebase satisfied)

- **Mergeability (FIXED):** PR #83 OPEN, head `b01b87a230c742ce6b73ab7682b91d65903344ee`, `mergeable: MERGEABLE`, base `8f4c15b` (== origin/main), valid merge base. `--rebase` is possible whenever the gate is met. No new PR needed.
- **Kodak corpus durable in git** (`obsidian/benchmarks/data/kodak/` PPMs tracked, plus `kodak.sha256` + `run_kodak.sh`/`fetch_kodak.sh`/`measure_kodak.sh`). Gate is now measurable reproducibly.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `b01b87a`). Real Kodak (effort 4) numbers, 24-image PCD0992 set:
  - **DEFAULT shipped codec = CMARC auto-selected best (never-expand net, with faithful R3-A wiring) = 9.7094 bpp mean.** Beats JPEG-LS (9.71); PNG 13.05 MET; WebP 9.61 MISSED by ~0.10 bpp; JPEG XL 8.71 MISSED by ~1.0 bpp. Bit-exact.
  - **KEY DIAGNOSIS:** the **R3-A residual-context is INERT** - `cmarc-force+resctx` is byte-identical to `cmarc-force` on every Kodak image. So the 9.7094 headline is from R5 quotient fix + faithful wiring at `311c5bc`, NOT from an actually-engaged residual DIFF context. The Builder "fixed" R3-A twice (`0efc83c`, `311c5bc`) and it stayed inert because auto-selection never keeps the residual-context candidate (365-way context starves the per-(cid,bin) binary models, so its bits are identical to the non-context path).
  - **R6-B color cache is a PROVEN DEAD END for this codec.** Wired at `7eaef45`/`b01b87a` (`ENTROPY_MODE_CARC_CACHE=6`); measured byte-identical 9.7094 bpp on all 24 Kodak images. The binary-coder floor (~1 bit/pixel for `cache_flag` + gamma rank) exceeds what the cache saves vs CMARC's near-optimal integer residual coding on low-entropy photographic residuals. Do NOT re-measure a known tie.
- **CMARC lineage (R1 -> R5) built; entropy core correct (CACM87):**
  - **R4 coder = CACM87 (Witten-Neal-Cleary binary arithmetic coder)** - proven correct; efficiency gates pass (ratio < 1.10/1.20).
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` learns the geometric quotient like JPEG-LS QM; dropped forced CARC 11.11 -> 9.71 bpp.
  - **Faithful R3-A (residual DIFF context conditions the whole CMARC residual):** wired at `311c5bc`, but **currently a NO-OP** (auto-selection never keeps it because the 365-way context starves the per-(cid,bin) binary models, and the model keying does not actually change which bin model is used). Must be fixed test-first.
  - **R3-C (JPEG-LS run mode):** implemented; neutral on real Kodak.
  - All CMARC variants ship behind the never-expand safety net, which now ALSO engages by default.
- **R6 blueprint DELIVERED + CORRECTED (`f137881`), but its central premise is now disproven:**
  - **R6-A (pixel-domain spatial LZ77):** DISPROVEN by the Builder - `CARC_LZ` IS already pixel-domain LZ77 (byte-for-byte duplicate); ties because photographic content has too few exact pixel repeats of length >= `MIN_MATCH=3`.
  - **Component B (R3-A quotient-context fix):** DONE at `0efc83c`/`311c5bc` (clears JPEG-LS 9.71 on paper) but the residual-context path is still INERT (no-op). This is the bug to fix next, test-first.
  - **Component A (R6-B LRU color cache, `ENTROPY_MODE_CARC_CACHE = 6`):** wired (`7eaef45` + `b01b87a`) but PROVEN A DEAD END (ties on all 24 Kodak images).
  - **Component C (tuned matches):** `MIN_MATCH=2` + 2D distance model + cache competition; marginal on photos; the Builder oriented on it (run 32243228032) but did not push.

## In flight

- **Builder (resume via `continue` this run):** FIX the **R3-A inert bug test-first** - write and pass the mandatory test `cmarc-force+resctx != cmarc-force` (forced residual-context must emit DIFFERENT bits than non-context); fix the `(cid,bin)` model keying so the residual DIFF context genuinely changes which `BinModel` each bin uses; code the residual-context candidate unconditionally on its candidate path (do NOT rely on auto-selection that starves on sparse contexts); re-measure REAL Kodak effort-4 reproducibly on the durably committed corpus; keep every prior seam OFF by default behind the never-expand net. Do NOT re-measure the dead R6-B cache. If the fix clears WebP 9.61, keep going toward JXL; if, after a real attempt, the context still cannot be engaged without regression, STOP and report (do not ship another no-op).
- **No Architect / Researcher / Factory in flight.** Corrected R6 blueprint present and now empirically partially disproven; next escalation (if a properly-engaged R3-A still misses WebP) would be an Architect pass for R7 (adaptive weighted predictor / MA-tree).
- **Review is STALE:** last `/oc approve` was at 2026-08-18 07:52Z (head ~`96a6075`); current head `b01b87a` un-reviewed. Fresh strict review required before any merge, deferred until the codec stabilizes near the gate.

## PENDING (deferred)

- **Clear WebP 9.61 gate:** default 9.7094 is ~0.10 above; fixing R3-A (free additive win if genuinely engageable) is the most plausible single step.
- **Clear JPEG XL 8.71 gate:** ~1.0 bpp above; the hard long pole - needs R3-A fix + possibly R7 (Architect explicitly does not promise JPEG XL from R6 alone).
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near).
- **Factory infra hardening:** `continue-on-error` still pending but non-blocking.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `b01b87a`, `mergeable: MERGEABLE` (orphan break resolved). R6-B proven dead end; R3-A inert bug pending fix. No held runs.
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Let the resumed Builder (this run's `continue`) fix the R3-A inert bug test-first** (`cmarc-force+resctx != cmarc-force` passes), then re-measure on REAL Kodak effort-4 reproducibly. Do NOT re-measure the dead R6-B cache.
2. **After R3-A lands:** re-measure real Kodak; if default mean < 9.61 (WebP), continue toward JXL; if JXL (< 8.71) also cleared, proceed to merge prep.
3. **If R3-A fix still misses WebP:** re-fire `architect`/`research` on PR #83 for R7 (adaptive weighted predictor / MA-tree); do NOT merge until all three gates clear.
4. **Re-fire strict `/oc review`** on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
5. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
6. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
7. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Can the R3-A residual-context be genuinely engaged without regression?** Prior two "fixes" stayed no-ops because the model keying/auto-selection never actually changed the bits. The mandatory test `cmarc-force+resctx != cmarc-force` must be met this time; if the residual DIFF context cannot be made to matter on this codec's binary-coder budget, that is itself a finding (the JPEG-LS QM uses one adaptive coder per context, not a per-(cid,bin) table that starves).
- **Will fixing R3-A let the codec clear the ~0.10 bpp WebP gap?** Most plausible single win; JXL (~1.0 bpp) likely needs more.
- **Merge gate (owner override #2):** NOT met - default 9.7094 bpp > WebP 9.61 > JXL 8.71. Even best CMARC+R3-A (if engaged) beats JPEG-LS but misses WebP by ~0.10 and JXL by ~1.0.
- **Review staleness:** last approve at head ~96a6075; current head `b01b87a` un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.
- **Orphan-main break:** RESOLVED (PR MERGEABLE). Branch re-linked to main; no new PR needed.
- **Trigger storm:** sibling maintainer runs may also emit `continue`; the Builder re-implements the corrected R3-A idempotently (no harm). This run deliberately re-fires `continue` because no Builder build is in flight (run 32243228032 oriented but did not push).

- Mae, the Maintainer
