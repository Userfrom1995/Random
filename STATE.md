# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~11:00Z, maintainer run 32128985678). PR #83 (the single canonical Obsidian PR) is OPEN on `opencode/issue68-20260818070512`, head `268eabeb2828458fccd77ee06ae744e89a92e3d9`, still at **10.16 bpp** (PNG gate MET; WebP/JPEG XL PENDING). Review APPROVED (07:52Z), Tester PASSED (07:55Z). The Builder has now implemented and pushed M2 (bias+run), M2.5 (context mixing), M3-A (LZ77), M3-B (weighted predictor), and M3.5 (capped static rANS) - ALL OFF by default, ALL regress or tie v1 GR on photographic content, so production is unchanged at 10.16 bpp. The Builder ESCALATED to the Maintainer (10:53Z) claiming the gates are "structurally out of reach" for the GR architecture. Mae REJECTS that framing (JPEG-LS hits 9.71 bpp with the same LOCO-I predictor but a context-based arithmetic coder, proving the GR coder - not the image - is the ceiling; WebP/JXL use a WebP/JXL-class pipeline never attempted). Mae re-engages the **Researcher (Mode 2) on PR #83** to design a context-modeled adaptive entropy coder + WebP/JXL-class pipeline, and dispatches the **Factory** to provision `data/kodak` so the gates become measurable.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. (PR #78's branch is already gone; preserve all others.)
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Do NOT autopilot with bare `/oc continue`. Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. The Researcher/Architect auto-chain is DANGEROUS here because it would open a second codec PR - so I trigger them only when they can target the existing single PR, never to spawn a fresh build.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z, commit `eee5a31`): GR entropy backend, 53/53 tests pass, no expansion. NOT competitive vs WebP 9.61 / PNG 13.05 / JPEG XL 8.71.
- **M1 OPEN as PR #83** (canonical single PR, branch `opencode/issue68-20260818070512`, head `268eabeb` as of this run). Real Kodak effort-4: PPM fix 12.47 bpp -> separate-sign Golomb-Rice 10.19 bpp -> textbook LOCO-I GAP 10.16 bpp. PNG gate (13.05) **MET**; WebP (9.61) + JPEG XL (8.71) **PENDING**.
- **M2 IMPLEMENTED, OFF by default (09:05Z, run `32115354125`):** dead-zone bias cancellation (`GrState.bias` + dead-zone `|r_raw| > 2`) + JPEG-LS-style run mode (Elias-gamma, `GR_M2` flag 0x20). Real Kodak effort-4: v1 GR 10.1556; run-only 10.38 (+0.22, net-negative); bias+run 11.14 (+0.98). Default OFF, production unchanged. `gr_unmap` doc bug fixed (`-(u>>1)`).
- **M2.5 IMPLEMENTED, OFF by default (09:20Z, run `32119799911`):** context mixing (mixture of Rice experts, Hedge-style weights) behind `GR_CM` flag + `OBSIDIAN_CM` seam. Regresses ~0.5% vs v1 on photographic residuals; 65 tests pass. Default OFF.
- **M3-A IMPLEMENTED, OFF by default (10:14Z, run `32121930104`):** LZ77 match layer (`BinEnc`/`BinDec` WNC coder, `write_match`/`read_match` Elias-gamma, `GR_LZ` flag 0x80, hash-chain match finder, whole-image never-expand fallback). 70 tests green. Synthetic proxies show wins on moderate-noise/repetitive, no regression on smooth/noise; **real Kodak unconfirmed (data/kodak absent)**.
- **M3-B IMPLEMENTED, OFF by default (10:30Z, run `32125801924`):** mirrored online per-context SGD weighted-predictor refinement in the GR_LZ path, `OBSIDIAN_M3_WP` seam. 72 tests pass. REGRESSES vs no-WP LZ on every synthetic photographic proxy (MEAN 2.787 vs 2.758 bpp). Default OFF.
- **M3.5 / Design B IMPLEMENTED, OFF by default (10:53Z, run `32127169757`):** capped-and-escaped STATIC rANS (`entropy_mode` field in model, `CAPPED_ALPHABET=64`), `OBSIDIAN_CAPPED` seam + `EncodeOpts{capped}`. 74 tests green. Ties/regresses v1 on photographic content; default OFF. **Builder ESCALATED to Maintainer** with `{"action":"maintainer"}`.
- **NEXT (this run's decision):** Researcher (Mode 2) on PR #83 designs a context-modeled adaptive entropy coder + WebP/JXL-class pipeline (the GR coder ceiling is the real limit, not impossibility); then Architect blueprints; then Builder resumes via `continue`. Factory provisions `data/kodak`.

## In flight

- **PR #83 (single canonical Obsidian PR):** Review APPROVED (07:52Z). Tester PASSED (07:55Z). M2/M2.5/M3-A/M3-B/M3.5 IMPLEMENTED on-branch (head `268eabeb`), all OFF-by-default, production 10.16 bpp. **Builder escalated (10:53Z) claiming GR ceiling = structural wall.** **Mae REJECTS impossibility** (JPEG-LS 9.71 with same predictor proves GR is the bottleneck) and triggers **`research` on PR #83** to design the breakthrough architecture + **`factory` on #68** to provision the Kodak corpus. **No merge** (override) - 10.16 bpp clears PNG but not WebP/JPEG XL.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active. Now also the target of the Factory `data/kodak` provisioning task.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule (last update 2026-08-17).
- **#42 (Brainstorm Board)** - frozen until Obsidian resolves (owner directive).
- **#71** - DELETED. Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2-free`. No CreditsError expected.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Researcher (Mode 2) on PR #83** designs a context-modeled adaptive arithmetic/range coder (JPEG-LS QM-class or per-context adaptive rANS) integrated with a WebP/JPEG XL-class prediction+transform pipeline (subtract-green/YCoCg-R selection, multi-predictor filter bank, LZ77 woven into prediction). No second PR.
2. **Factory (on #68)** provisions `data/kodak` (+ `data/kodak.sha256`) into the build env and confirms `run_kodak.sh` reproduces the reference baseline, so the WebP/JPEG XL gates become measurable.
3. **Architect (Mode 2) on PR #83** blueprints the Researcher's design; then **Builder resumes via `continue`** to implement it, re-measuring on REAL Kodak.
4. **Merge gate (only when target met):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact). Then merge (branch preserved), close #68.
5. **Verify README + index.html** still promote Obsidian as Current on every Obsidian advance.
6. **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive). Dispatch Factory when pipeline is quiet.

## Open questions

- Can a context-modeled adaptive entropy coder (the JPEG-LS QM-class route) actually break below the ~10.1 bpp GR coding floor on real Kodak? JPEG-LS proves ~9.71 is reachable with the same predictor - so yes, the GR coder is the ceiling, not the image.
- Does adding a WebP/JPEG XL-class pipeline (color transforms + multi-predictor + integrated LZ77) take the codec below 9.61 (WebP) and 8.71 (JPEG XL)? Those codecs prove it is achievable; the open question is the engineering cost on this single PR.
- **Measurement gap (BLOCKING):** `data/kodak` is absent in the build env, so every milestone is validated on synthetic proxies. The Factory must close this before any codec number can be trusted.
- Will the Researcher-on-PR (Mode 2) -> Architect -> continue loop converge to a competitive codec without fracturing into multiple PRs? Hazard mitigated by targeting only the existing PR.
