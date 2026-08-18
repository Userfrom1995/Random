# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~14:18Z, maintainer run 32147556736, event: owner `/oc maintainer` on PR #83 after the Builder reverted R3 and asked for direction). **NEW DECISION:** the Builder reverted R3 (it regressed: R3-A sparse-context penalty, R3-B mis-wired as unary) back to the R2.4 baseline and recommended blocking on durably provisioning real Kodak. I answered **B**. **THE decisive blocker is re-confirmed:** `obsidian/benchmarks/data/kodak/*.ppm` is NOT in git (only `kodak.sha256` + `run_kodak.sh`), so the earlier "real Kodak 10.0906 bpp" is not reproducible and no gate can be measured. I dispatched the Factory to commit the Kodak PPMs to the EXISTING branch (no new PR) and the Architect to re-blueprint R3 from the empirical failure. Holding the Builder until both land. **REAL KODAK = 10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.48; JPEG XL 8.71 MISSED by 1.38) - but this number is currently non-reproducible pending data/kodak.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`.
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch (this run it pushes `data/kodak` to `opencode/issue68-20260818070512`).
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Do NOT autopilot with bare `/oc continue`. Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (mergeability RESOLVED; measurement BLOCKER OPEN)

- **Mergeability RESOLVED.** PR #83 head `89891e84f9934f5887c0a97fe8495704f62e6c4b` = `main` (`30fd150`) + 1 commit, valid merge base `30fd150`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. PR #84 remains CLOSED (erroneous duplicate; its content is mirrored in #83's head). `--rebase` of #83 is possible once the target is met.
- **Measurement blocker OPEN (THE decisive issue this run):** `obsidian/benchmarks/data/kodak/*.ppm` is NOT committed to the repo (only `kodak.sha256` + `run_kodak.sh`). The earlier real-Kodak measurement (run ~13:15Z, 10.0906 bpp) used transient PPMs that were never committed, so it is not reproducible and no further gate can be measured. The Factory (this run) must durably commit the PPMs to the existing branch.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`). Last trustworthy real-Kodak effort-4 = **10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED; JPEG XL 8.71 MISSED). That number is currently NON-reproducible (data/kodak absent).
- **CMARC RESEARCH DELIVERED** (`obsidian/docs/research-breakthrough.md`): the ~10.1 bpp ceiling is the single-k/per-(cid,bin) GR-style coder, not the image; JPEG-LS reaches 9.71 bpp on the SAME Kodak corpus with the SAME LOCO-I GAP predictor but a context-based arithmetic (QM) coder.
- **CMARC ARCHITECT BLUEPRINT DELIVERED** (`obsidian/docs/architect-cmarc-blueprint.md`): CMARC as `entropy_mode` values (CARC=2, CARC_LZ=3, CARC_MIX=4).
- **CMARC BUILT END-TO-END (R1 -> R2.4), all OFF by default.** Production stays byte-identical to v1 GR. 106 lib tests pass.
- **REAL KODAK MEASUREMENT (now non-reproducible):** `obsidian/benchmarks/results/2026-08-18-real-kodak-2.csv` - 10.0906 bpp mean, but the source PPMs are gone from the repo.
- **R3 ARCHITECT BLUEPRINT DELIVERED (13:32Z, run `32142354868`, `architect-r3-residual-context-blueprint.md`):** diagnosed CMARC as conditioning on spatial-gradient context instead of quantized neighbor residuals, plus R2 dropped the geometric quotient. THIS BLUEPRINT IS NOW KNOWN FLAWED (Builder's 14:18Z empirical test disproved its key assumptions).
- **R3 BUILDER IMPLEMENTATION ATTEMPTED THEN REVERTED (14:18Z):** R3-A (165-context DIFF) regressed synthetic CARC ~14 -> ~28 bpp (sparse-context penalty for per-(cid,bin) binary models); R3-B mis-wired as unary not geometric; header/payload desync bug. Builder reverted ALL R3 to the R2.4 baseline (106 tests pass, bit-exact). No R3 code in flight.

## In flight

- **PR #83 (single canonical Obsidian PR, OPEN, MERGEABLE, head `89891e8`):** Review APPROVED (07:52Z). Tester PASSED (07:55Z). Full CMARC R1-R2.4 stack BUILT (all OFF-by-default). R3 attempt reverted. **Builder HOLDING** (asked A/B/C, I answered B). Waiting on: (a) Factory commits `data/kodak` to this branch; (b) Architect delivers corrected R3 blueprint. Then I trigger `continue`.
- **Factory (`/oc factory` on #68, this run):** durably provision `obsidian/benchmarks/data/kodak/*.ppm` (commit to `opencode/issue68-20260818070512`, no new PR) + harden `run_kodak.sh`. No Factory run was in flight provisioning data (prior run `160`/PR #84 is CLOSED and its data subtask never landed), so this is not a duplicate.
- **Architect (`/oc architect` on PR #83, this run):** re-blueprint R3 incorporating the Builder's empirical failure (sparse-context regression, geometric-quotient necessity, corrected R2 understanding). No Architect in flight, so not a duplicate.

## PENDING (deferred to a quiet run)

- **Factory hardening (one-PR rule):** dispatch the Factory Engineer to harden the workflow/agent so it NEVER opens a new PR for an issue that already has an open Obsidian/codec PR; it must reuse/push to the existing branch. Deferred to honor the owner's explicit "stop opening new PRs" instruction (a factory fix PR would itself be a new PR).
- **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive).

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.
- **#79 / #81 / #82 / #84** - factory/infra and M0 PRs; #84 is the closed erroneous duplicate.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2-free`. No CreditsError expected.
- **Mergeability:** PR #83 OPEN, head `89891e8` = main (`30fd150`) + 1 commit, valid merge base `30fd150`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. `--rebase` possible once target met.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Factory (this run):** durably commit `obsidian/benchmarks/data/kodak/*.ppm` to `opencode/issue68-20260818070512` (no new PR); harden `run_kodak.sh` (fail fast + sha256 verify). Confirm `run_kodak.sh` reproduces JXL 8.7062 / WebP 9.6130 / JLS 9.7113 / PNG 13.0518.
2. **Architect (this run):** deliver corrected R3 blueprint on PR #83 (account for sparse-context regression + geometric quotient; drop the false "R2 dropped quotient" claim).
3. **Builder (via `continue` AFTER both land):** re-implement R3 per corrected blueprint; re-measure on REAL (now-durable) Kodak effort-4. Keep all seams OFF by default; keep never-expand safety net.
4. **After R3 build:** if gates still unmet on real Kodak, re-engage Researcher/Architect (existing PR only) for a true QM-class adaptive arithmetic coder - do NOT autopilot with bare `continue`.
5. **Merge gate (only when met AND reproducible AND main repaired):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact, reproducible). Then merge (branch preserved per owner directive), close #68.
6. **Verify README + index.html** still promote Obsidian as Current on every Obsidian advance.

## Open questions

- **THE decisive blocker is now unambiguous:** `data/kodak/*.ppm` is not in git, so the 10.0906 bpp "real Kodak" number is not reproducible and no further gate measurement is possible. The Factory must durably commit the PPMs to the existing branch. Until then, R3 (and any codec change) is unverifiable against the actual gate.
- **Is R3 salvageable for CMARC's model structure?** The Builder proved naive context expansion REGRESSES CMARC (sparse-model penalty). The Architect must find a context/quotient scheme that reaches `H(p)+epsilon` on real Kodak residuals, or recommend a true QM-class adaptive arithmetic backend.
- **Mergeability (RESOLVED):** branch `89891e8` = main + 1 commit, valid merge base, MERGEABLE.
- **One-PR integrity (RESOLVED):** #83 is the sole canonical Obsidian PR; the Factory pushes data to it, never opens a codec PR.
- Will the Architect-on-PR (Mode 2) -> continue loop converge to a competitive codec without fracturing into multiple PRs? Hazard mitigated by targeting only the existing PR.

- Mae, the Maintainer
