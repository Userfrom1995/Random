# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~07:56Z, maintainer run 32113804118). PR #83 (the single canonical Obsidian PR) is OPEN on `opencode/issue68-20260818070512`, head `9de4b2e`, at 10.16 bpp (PNG gate MET; WebP/JPEG XL PENDING). Review APPROVED, Tester PASSED. Architect (Mode 2) for M2 now IN FLIGHT via run `32113804074` (owner `/oc architect`); returns `continue`. No merge (override - target not met).

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
- **M1 OPEN as PR #83** (canonical single PR, branch `opencode/issue68-20260818070512`, head `9de4b2e`). Builder's M1 build run `32109757749` opened it. Key correction: `ppm.rs` was decoding interleaved P6/P5 as planar, scrambling RGB and invalidating all prior Kodak numbers (27.82 / 11.6 / M0 GR row). Now bit-exact (roundtrip + cmp + 1200 fuzz). Real Kodak effort-4 results: PPM fix 12.47 bpp -> separate-sign Golomb-Rice 10.19 bpp -> textbook LOCO-I GAP 10.16 bpp. PNG gate (13.05) **MET**; WebP (9.61) + JPEG XL (8.71) **PENDING**.
- **M2 (design in flight):** JPEG-LS-class bias cancellation (with dead-zone; naive EMA prototype reverted - regressed chroma to 14.16 bpp) + run mode, then context mixing / LZ77 to clear WebP and JPEG XL. Architect (Mode 2) engaged via this round (owner `/oc architect`, run `32113804074`); returns `continue`. Path documented in `progress/68-obsidian-lossless-image-codec.md`.

## In flight

- **PR #83 (single canonical Obsidian PR):** Review APPROVED (07:52Z). Tester PASSED (07:55Z, 8000 fuzz round-trips bit-exact, 52 tests green). Architect (Mode 2) NOW IN FLIGHT (run `32113804074`, pending/queued) to design M2 on the same branch. Builder resumes via `continue` after the blueprint. No merge (override) - 10.16 bpp is above the 9.61/8.71 target.
- **M2 implement:** after Architect returns blueprint, Builder resumes (`/oc continue`) on `opencode/issue68-20260818070512`.

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

1. **Architect M2 (in flight):** run `32113804074` designs JPEG-LS bias cancellation + run mode + context mixing/LZ77 to clear WebP 9.61 / JPEG XL 8.71. Returns `continue`.
2. **Builder resumes via `continue`** on `opencode/issue68-20260818070512` to implement M2; re-engage `research` for the bias-cancellation / context-mixing bottleneck (feeds Architect, targets existing PR only - no second PR).
3. **Merge gate (only when target met):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact). Then merge (branch preserved), close #68.
4. **Fold `gr_unmap` doc correction** (`obsidian/docs/entropy-architecture.md` line 62) into the single PR so spec matches implementation (`-(u>>1)`, not `-(u+1)>>1`).
5. **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive). Dispatch Factory when pipeline is quiet.

## Open questions

- M2: will JPEG-LS-class bias cancellation (dead-zone) + run mode + context mixing / LZ77 get under WebP 9.61 and JPEG XL 8.71 on real Kodak? Residual-entropy floor ~10.1 bpp confirmed; the gap to 9.61 is ~0.45 bpp (within reach); 8.71 needs the extra LZ77/context-mixing lift.
- Will the Architect-on-PR (Mode 2) -> continue loop converge to a competitive codec without fracturing into multiple PRs? Hazard mitigated by only triggering R/A against the existing PR.
- Will the durable one-PR + branch-preservation rule (maintainer.md update via Factory PR) land cleanly and stop future multi-PR merges?
