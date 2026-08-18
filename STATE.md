# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~08:00Z, maintainer run 32114013479). PR #83 (the single canonical Obsidian PR) is OPEN on `opencode/issue68-20260818070512`, head `96a6075`, at 10.16 bpp (PNG gate MET; WebP/JPEG XL PENDING). Review APPROVED, Tester PASSED. Architect (Mode 2) for M2 DELIVERED its blueprint on the branch; Builder now resuming M2 via `continue`. No merge (override - target not met).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. (PR #78's branch is already gone; preserve all others.)
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** (owner directive 2026-08-18T07:29:31Z). Do NOT autopilot with bare `/oc continue`. Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. The Researcher/Architect auto-chain (researcher -> architect -> builder) is DANGEROUS here because it would open a second codec PR - so I trigger them only when they can target the existing single PR, never to spawn a fresh build.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z, commit `eee5a31`): GR entropy backend, 53/53 tests pass, no expansion. NOT competitive vs WebP 9.61 / PNG 13.05 / JPEG XL 8.71.
- **M1 OPEN as PR #83** (canonical single PR, branch `opencode/issue68-20260818070512`, head `96a6075` as of this run). Builder's M1 build run `32109757749` opened it. Key correction: `ppm.rs` was decoding interleaved P6/P5 as planar, scrambling RGB and invalidating all prior Kodak numbers (27.82 / 11.6 / M0 GR row). Now bit-exact (roundtrip + cmp + 1200 fuzz). Real Kodak effort-4 results: PPM fix 12.47 bpp -> separate-sign Golomb-Rice 10.19 bpp -> textbook LOCO-I GAP 10.16 bpp. PNG gate (13.05) **MET**; WebP (9.61) + JPEG XL (8.71) **PENDING**.
- **M2 (Architect blueprint DELIVERED):** `obsidian/docs/m2-bias-run-architecture.md` committed on the branch (run `32113387449`, head `96a6075`). Design: M2-A dead-zone bias cancellation (`GrState` gains `bias` + `bias_count`, mirrored, zero model bytes; `|r_raw| <= 2` dead-zone keeps bias 0 on zero-peaked chroma; clamped counter-committed bias in ±16, ±1 every 4 same-sign residuals) + M2-B JPEG-LS-style run mode (per-plane, parameter-free Elias-gamma(runlen), 1-pixel encoder lookahead, decoder copies `prev_val`) + new `GR_M2` header flag (bit 5, 0x20) shipping with `ENTROPY_GR` (old v1 GR streams still decode). Gate target: Kodak effort-4 < 9.71 (JPEG-LS), aim < 9.61 (WebP). Roadmap M2.5 context mixing (~9.0-9.3), M3 LZ77 + self-correcting weighted predictor (`GR_LZ`) to clear JPEG XL 8.71; Design B capped rANS fallback.

## In flight

- **PR #83 (single canonical Obsidian PR):** Review APPROVED (07:52Z). Tester PASSED (07:55Z, 8000 fuzz round-trips bit-exact, 52 tests green). Architect (Mode 2) DELIVERED blueprint (07:58Z, run `32113387449`, head `96a6075`). **Builder resuming via `continue`** (this run, run `32114013479`) to implement M2-A + M2-B on the same branch. No merge (override) - 10.16 bpp is above the 9.61/8.71 target.

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

1. **Builder implements M2 (in flight via `continue`):** M2-A dead-zone bias cancellation + M2-B run mode per blueprint on `opencode/issue68-20260818070512`; re-benchmark real Kodak effort-4; fold in `gr_unmap` doc correction.
2. **Re-engage `research`** for the bias-cancellation / context-mixing bottleneck if the Builder stalls (feeds Architect, targets existing PR only - no second PR).
3. **After M2 lands:** re-engage `architect` (Mode 2) for M2.5 context mixing / M3 LZ77 if M2 alone does not clear WebP 9.61.
4. **Merge gate (only when target met):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact). Then merge (branch preserved), close #68.
5. **Fold `gr_unmap` doc correction** (`obsidian/docs/entropy-architecture.md` line 62) into the single PR so spec matches implementation (`-(u>>1)`, not `-(u+1)>>1`).
6. **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive). Dispatch Factory when pipeline is quiet.

## Open questions

- M2: will dead-zone bias cancellation + run mode get under WebP 9.61 / JPEG-LS 9.71 on real Kodak? Residual floor ~10.1 bpp; ~0.45 bpp gap to WebP looks reachable with run mode alone; 8.71 needs M2.5 context mixing / M3 LZ77 lift.
- Will the Architect-on-PR (Mode 2) -> continue loop converge to a competitive codec without fracturing into multiple PRs? Hazard mitigated by only triggering R/A against the existing PR.
- Will the durable one-PR + branch-preservation rule (maintainer.md update via Factory PR) land cleanly and stop future multi-PR merges?
