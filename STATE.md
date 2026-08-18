# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~09:20Z, maintainer run 32121074876). PR #83 (the single canonical Obsidian PR) is OPEN on `opencode/issue68-20260818070512`, head `e228850fa15bd9b90312ad865933b7afa23ae09a`, still at **10.16 bpp** (PNG gate MET; WebP/JPEG XL PENDING). Review APPROVED (07:52Z), Tester PASSED (07:55Z). M2 (dead-zone bias + run mode) and M2.5 (context mixing) are IMPLEMENTED but both ship **OFF by default** and do NOT beat v1 on photographic Kodak (10.38 / 11.14 / +0.5% vs 10.16), so production is unchanged. Mae is re-engaging the Architect (Mode 2) on the PR to design **M3 (LZ77 + self-correcting weighted predictor, `GR_LZ`)** - the last roadmap item that can clear WebP 9.61 / JPEG XL 8.71. No merge (override).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. (PR #78's branch is already gone; preserve all others.)
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Do NOT autopilot with bare `/oc continue`. Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. The Researcher/Architect auto-chain (researcher -> architect -> builder) is DANGEROUS here because it would open a second codec PR - so I trigger them only when they can target the existing single PR, never to spawn a fresh build.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z, commit `eee5a31`): GR entropy backend, 53/53 tests pass, no expansion. NOT competitive vs WebP 9.61 / PNG 13.05 / JPEG XL 8.71.
- **M1 OPEN as PR #83** (canonical single PR, branch `opencode/issue68-20260818070512`, head `e228850` as of this run). Real Kodak effort-4: PPM fix 12.47 bpp -> separate-sign Golomb-Rice 10.19 bpp -> textbook LOCO-I GAP 10.16 bpp. PNG gate (13.05) **MET**; WebP (9.61) + JPEG XL (8.71) **PENDING**.
- **M2 IMPLEMENTED, OFF by default (09:05Z, run `32115354125`):** dead-zone bias cancellation (`GrState.bias` + dead-zone `|r_raw| > 2`) + JPEG-LS-style run mode (Elias-gamma, `GR_M2` flag 0x20). Result on real Kodak effort-4: v1 GR 10.1556; run-only 10.38 (+0.22, net-negative); bias+run 11.14 (+0.98). Both seams `OBSIDIAN_M2_BIAS`/`OBSIDIAN_M2_RUN` default OFF, so production unchanged. `gr_unmap` doc bug fixed (`-(u>>1)`).
- **M2.5 IMPLEMENTED, OFF by default (09:20Z, run `32119799911`):** context mixing (mixture of Rice experts, Hedge-style weights) behind `GR_CM` flag + `OBSIDIAN_CM` seam. Regresses ~0.5% vs v1 on photographic residuals; 65 tests pass. Default OFF -> production unchanged at 10.16 bpp.
- **M3 (NEXT, PENDING design):** LZ77 back-references + self-correcting weighted predictor (`GR_LZ`) per the Architect's roadmap, to clear WebP 9.61 then JPEG XL 8.71. Design-B capped rANS as fallback.

## In flight

- **PR #83 (single canonical Obsidian PR):** Review APPROVED (07:52Z). Tester PASSED (07:55Z). M2 + M2.5 IMPLEMENTED on-branch (head `e228850`), both OFF-by-default, production 10.16 bpp. **Builder's latest `continue` (M2.5) completed** (run `32119799911`, 09:20Z) and asked "next? - start M3 or open for review?". Mae is re-engaging the **Architect (Mode 2)** on this PR to design M3 (no in-flight architect run right now). No merge (override) - 10.16 bpp clears PNG but not WebP/JPEG XL.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule (last update 2026-08-17).
- **#42 (Brainstorm Board)** - frozen until Obsidian resolves (owner directive).
- **#71** - DELETED. Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2.5-free`. No CreditsError expected.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Architect designs M3 (this run, `architect` on PR #83):** LZ77 back-references + self-correcting weighted predictor (`GR_LZ`), targeting WebP 9.61 first then JPEG XL 8.71; Design-B capped rANS fallback. Returns `continue` for the Builder on the same branch. No second PR.
2. **Builder implements M3 (via `continue`),** re-benchmarks real Kodak effort-4; keep M2/M2.5 seams intact (default OFF, no v1 regression).
3. **Re-engage `research`** for the LZ77 match-finding / weighted-predictor bottleneck if the Builder stalls (feeds Architect, targets existing PR only - no second PR).
4. **Merge gate (only when target met):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact). Then merge (branch preserved), close #68.
5. **Verify README + index.html** still promote Obsidian as Current on every Obsidian advance.
6. **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive). Dispatch Factory when pipeline is quiet.

## Open questions

- M3 LZ77 + weighted predictor: can it clear WebP 9.61 on real Kodak (residual floor ~10.1 bpp; needs ~0.5 bpp of match/context lift), then JPEG XL 8.71 (needs ~1.45 bpp)? M2/M2.5 both failed to help photographic data, so M3 is now the only roadmap path to the gates.
- Will the Architect-on-PR (Mode 2) -> continue loop converge to a competitive codec without fracturing into multiple PRs? Hazard mitigated by only triggering R/A against the existing PR.
- Will the durable one-PR + branch-preservation rule (maintainer.md update via Factory PR) land cleanly and stop future multi-PR merges?
