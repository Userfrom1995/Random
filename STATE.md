# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~12:55Z, maintainer run 32139398302, scheduled). PR #83 (the single canonical Obsidian PR) is OPEN on `opencode/issue68-20260818070512`, head `a1220ee0858ae5e93098d5335f8b85f06c73cae5`, with the **Builder actively in flight** (run `32138130336`, started 12:41Z, implementing CMARC R1). The CMARC breakthrough design (`obsidian/docs/research-breakthrough.md`, `obsidian/docs/architect-cmarc-blueprint.md`) is DELIVERED. Production still **10.16 bpp** (PNG gate MET; WebP/JPEG XL PENDING). The CRITICAL infra break persists: `main` is still the single orphan commit `30fd150873da6578c639ef1d569df4d948712aef`, so PR #83 is `CONFLICTING` and `--rebase` merge is impossible. The Factory dispatch from the 11:10Z run was **CANCELLED without running** (run `32130517040`, 0 jobs); `data/kodak` is still absent (404). This run re-dispatches the Factory on #68.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. (PR #78's branch is already gone; preserve all others.)
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Do NOT autopilot with bare `/oc continue`. Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. The Researcher/Architect auto-chain is DANGEROUS here because it would open a second codec PR - so I trigger them only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE BREAK (found 2026-08-18 ~11:08Z, STILL OPEN)

- `main` is a **single orphan commit** `30fd150873da6578c639ef1d569df4d948712aef` (1 commit, 586 files, NO history - a squashed/rewritten main). Verified again this run: local checkout HEAD = `30fd150`.
- **Every** open PR branch shares **no common ancestor** with `main`. PR #83 (`opencode/issue68-20260818070512`, roots at `cc00515`) reports `mergeable: CONFLICTING`, `mergeStateStatus: DIRTY`. Affected: #83 plus `opencode/issue68-20260816082105`, `opencode/issue68-20260818055633`, `opencode/issue32-20260809154312`, etc.
- Consequence: the mandated `gh pr merge --rebase` is **impossible** (no base to rebase onto). This silently blocks the eventual merge of the fundamental goal.
- **Remedy in flight:** Factory Engineer (re-dispatched this run, 32139398302, on #68) to (1) restore `main`'s history so the orphaned PR branches re-link and become rebase-mergeable again (force-restoring the pre-rewrite main history that contained `cc00515`'s ancestors, or equivalent), and (2) provision `data/kodak` so the gates become measurable. The Factory's own fix PR is based on current `main` so it lands fine; the fix then re-links the worker branches.
- **Do NOT attempt to merge until this is resolved** - a rebase merge would fail and a merge-commit would orphan further.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z, commit `eee5a31`): GR entropy backend, 53/53 tests pass, no expansion.
- **M1 OPEN as PR #83** (canonical single PR, branch `opencode/issue68-20260818070512`). Real Kodak effort-4: PPM fix 12.47 -> separate-sign GR 10.19 -> textbook LOCO-I GAP 10.16 bpp. PNG gate (13.05) **MET**; WebP (9.61) + JPEG XL (8.71) **PENDING**.
- **M2 / M2.5 / M3-A / M3-B / M3.5 IMPLEMENTED, all OFF by default**, all regress/tie v1 GR on photographic content; production unchanged at 10.16 bpp.
- **CMARC RESEARCH DELIVERED (11:01Z, run `32129298608`):** `obsidian/docs/research-breakthrough.md`. The ~10.1 bpp "floor" is the ceiling of the single-k per-context Golomb-Rice *symbol* coder, not the image. JPEG-LS reaches 9.71 bpp on the same Kodak corpus with the same LOCO-I GAP predictor but a context-based arithmetic (QM) coder - proof the predictor is sound and the entropy backend is the bottleneck. Design: R1 (CMARC - context-modeled adaptive binary range coder, each residual coded bit-by-bit, cost `H(p)+epsilon`) clears WebP; R2 (subtract-green/color cache, expanded predictor bank, LZ77 re-woven with the binary coder, logistic mixing) targets JPEG XL.
- **CMARC ARCHITECT BLUEPRINT DELIVERED (11:07Z, run `32129665095`):** `obsidian/docs/architect-cmarc-blueprint.md`. CMARC is a new `ModelConfig.entropy_mode` value (`ENTROPY_MODE_CARC=2`, `CARC_LZ=3`, `CARC_MIX=4`), NOT a header flag - reuses M3.5's mechanism (model-section signaled, decoder-routed) so every legacy stream (v1 GR, M2, CM, LZ, capped) stays decodable. Specifies `rans.rs` (`BinModel` per-(cid,bin) 16-bit WNC prob, `RangeEnc`/`RangeDec` refactored from `BinEnc`/`BinDec`, `CarcCtx` mirroring `GrState`, `cmarc_write_residual`/`cmarc_read_residual`), `model.rs` (selectors + sparse `cmarc_priors`), `encoder.rs`/`decoder.rs` (CMARC branch + never-expand safety net vs v1 GR + threaded `EncodeOpts{cmarc}`), R1-c static priors in `analyze` (effort >= 4), then R2.
- **Builder ACTIVELY IN FLIGHT (this run, 12:55Z):** run `32138130336` started 12:41Z on PR #83 implementing CMARC R1 (then R2), re-measuring on REAL Kodak effort-4 (requires the Factory's `data/kodak`). Head moved to `a1220ee`. Per override #3 the Builder implements the delivered blueprint on the single branch; I did NOT re-fire `continue` because a build is already in flight (spam-avoidance + it is working).
- **No merge (override #2 + infra break):** 10.16 bpp clears PNG but not WebP/JPEG XL, AND the merge mechanism itself is broken until the Factory repairs `main`.

## In flight

- **PR #83 (single canonical Obsidian PR):** Review APPROVED (07:52Z). Tester PASSED (07:55Z). M2/M2.5/M3-A/M3-B/M3.5 IMPLEMENTED on-branch (all OFF-by-default, production 10.16 bpp). CMARC R+A DELIVERED. **Builder run `32138130336` ACTIVE (12:41Z) implementing CMARC R1.** **BLOCKED at merge by the orphaned-main infra break** (Factory re-dispatched). No merge.
- **Factory task on #68:** PRIOR dispatch (run `32130517040`, 11:11Z) **CANCELLED at 11:32Z with 0 jobs - never ran**. RE-DISPATCHED this run (32139398302) to (a) restore `main` history so orphaned PR branches (#83 et al.) re-link and become rebase-mergeable; (b) provision `data/kodak` (+ `data/kodak.sha256`) so gates become measurable.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active. Now ALSO the target of the Factory's main-history repair + data/kodak provisioning (re-dispatched 32139398302).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.
- **#71** - DELETED. Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2-free`. No CreditsError expected.
- **Mergeability:** BROKEN at infra level (see CRITICAL INFRASTRUCTURE BREAK). Factory must fix before any merge.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Factory (re-dispatched, #68, this run 32139398302):** (a) URGENT - restore `main`'s history so all orphaned open PR branches re-link and become rebase-mergeable (resolving the CONFLICTING state); (b) provision `data/kodak` (+ `data/kodak.sha256`) and confirm `run_kodak.sh` reproduces the reference baseline (JXL 8.7062 / WebP 9.6130 / JLS 9.7113 / PNG 13.0518). If the factory run is cancelled/stalls again, retry (it failed once at 32130517040 with 0 jobs - likely a queuing/runner issue, not a logic fault).
2. **Builder (`continue` on PR #83 when current run `32138130336` finishes):** implements CMARC R1 (context-modeled adaptive binary range coder via new `entropy_mode`), then R2; re-measures on REAL Kodak effort-4 (requires the Factory's `data/kodak`). Keep all prior seams OFF by default; keep never-expand safety net vs v1 GR. Do NOT fire `continue` while a build is in flight.
3. **Fresh review/test** auto-triggers on each Builder push; no manual re-fire needed.
4. **Merge gate (only when target met AND main repaired):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact). Then merge (branch preserved), close #68.
5. **Verify README + index.html** still promote Obsidian as Current on every Obsidian advance.
6. **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive). Dispatch Factory when pipeline is quiet.

## Open questions

- Can CMARC (context-modeled adaptive binary range coder, `H(p)+epsilon`) break below the ~10.1 bpp GR coding floor on real Kodak? JPEG-LS proves ~9.71 is reachable with the same predictor; CMARC's bit-by-bit conditioning should reach the WebP 9.61 gate and, with R2, JPEG XL 8.71.
- Does the WebP/JPEG XL-class pipeline (color transforms + multi-predictor + integrated LZ77) take the codec below 9.61 and 8.71? Those codecs prove it is achievable; the open question is the engineering cost on this single PR.
- **Measurement gap (BLOCKING):** `data/kodak` is absent (404 this run); the Factory must close this before any codec number can be trusted.
- **Mergeability (BLOCKING):** `main` is a single orphan commit (30fd150), orphaning all PR branches and making `--rebase` merge impossible. The Factory must restore `main`'s history before the eventual merge. Prior Factory dispatch (32130517040) cancelled without running; re-dispatched 32139398302.
- Will the Researcher-on-PR -> Architect -> continue loop converge to a competitive codec without fracturing into multiple PRs? Hazard mitigated by targeting only the existing PR.

- Mae, the Maintainer
