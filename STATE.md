# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~13:23Z, maintainer run 32142038771, event: owner `/oc maintainer` on PR #83 after the Researcher run 32141756980 completed). PR #83 (the single canonical Obsidian PR) is OPEN on `opencode/issue68-20260818070512`, head `d232477bfe63e57bf4c93bc784a47598c02f4434`. **REAL KODAK = 10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.48 bpp; JPEG XL 8.71 MISSED by 1.38 bpp). CMARC/R2 (R1->R2.4) built, all OFF by default, production byte-identical to v1 GR (10.1556). This run engages the Architect (Mode 2) on the existing PR to design the plateau-breaking next stage, and re-dispatches the Factory to durably repair the re-opened orphan-`main` break.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. (PR #78's branch is already gone; preserve all others.)
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Do NOT autopilot with bare `/oc continue`. Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. The Researcher/Architect auto-chain is DANGEROUS here because it would open a second codec PR - so they are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE BREAK - RE-OPENED (was "RESOLVED" ~13:00Z; orphan again at ~13:23Z)

- `main` is AGAIN the single orphan commit `30fd150873da6578c639ef1d569df4d948712aef` (1 commit, 586 files, no history). `git merge-base origin/main opencode/issue68-20260818070512` is EMPTY. PR #83 reports `mergeable: CONFLICTING` / `mergeStateStatus: DIRTY`. The Factory's earlier fast-forward (run 32139935703, ~13:00Z) did NOT persist - `main` reverted to the orphan, almost certainly because branch protection on `main` rejected the direct `git push` so the local fast-forward never landed.
- **RE-DISPATCHED this run (Factory on #68, run 32142038771):** the Factory must land a PR to `main` (or a `--allow-unrelated-histories` merge) so a shared history / merge base exists and `gh pr merge --rebase` becomes possible again. Do NOT orphan the worker branches further. This is non-blocking now (performance gate unmet) but must be fixed before the eventual merge.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z, commit `eee5a31`): GR entropy backend, 53/53 tests pass, no expansion.
- **M1 OPEN as PR #83** (canonical single PR, branch `opencode/issue68-20260818070512`). Real Kodak effort-4 (trustworthy): **10.0906 bpp mean** with the never-expand best-backend selection (CMARC/R2 wins only where it beats v1 GR; net ~0.07 bpp below the 10.1556 v1 GR baseline). PNG gate (13.05) **MET**; WebP (9.61) + JPEG XL (8.71) **PENDING / STILL UNMET**.
- **M2 / M2.5 / M3-A / M3-B / M3.5 IMPLEMENTED, all OFF by default**, all regress/tie v1 GR on photographic content; production baseline 10.1556 bpp (v1 GR).
- **CMARC RESEARCH DELIVERED (11:01Z, run 32129298608):** `obsidian/docs/research-breakthrough.md`. The ~10.1 bpp "floor" is the ceiling of the single-k per-context Golomb-Rice *symbol* coder, not the image. JPEG-LS reaches 9.71 bpp on the same Kodak corpus with the same LOCO-I GAP predictor but a context-based arithmetic (QM) coder - proof the predictor is sound and the entropy backend is the bottleneck. Design: R1 (CMARC) clears WebP; R2 (subtract-green/color cache, expanded predictor bank, LZ77 re-woven, logistic mixing) targets JPEG XL.
- **CMARC ARCHITECT BLUEPRINT DELIVERED (11:07Z, run 32129665095):** `obsidian/docs/architect-cmarc-blueprint.md`. CMARC is a new `ModelConfig.entropy_mode` value (`ENTROPY_MODE_CARC=2`, `CARC_LZ=3`, `CARC_MIX=4`), NOT a header flag.
- **CMARC BUILT END-TO-END (R1 -> R2.4), all OFF by default:** R1 binary range coder; R2 cross-bit conditioning; R2.1 subtract-green; R2.2 expanded predictor bank (ids 8..=16); R2.3 CMARC-LZ (dormant); R2.4 logistic mixing (dormant). Production stays byte-identical to v1 GR. 106 lib tests pass.
- **REAL KODAK MEASUREMENT (2026-08-18 ~13:15Z):** `obsidian/benchmarks/results/2026-08-18-real-kodak-2.csv` - 10.0906 bpp mean. Confirms CMARC/R2 did NOT clear WebP (9.61); it sits at the ~10.1 floor, ~0.38 bpp above JPEG-LS (9.71) on the same predictor. The entropy backend / pipeline integration is the proven bottleneck.
- **RESEARCH RE-RUN (13:20Z, run 32141756980) COMPLETED without a committed diagnosis doc** (branch head still `d232477`). This run routes the diagnosis + next blueprint to the Architect instead.

## In flight

- **PR #83 (single canonical Obsidian PR):** Review APPROVED (07:52Z). Tester PASSED (07:55Z). Full CMARC stack R1-R2.4 IMPLEMENTED on-branch (all OFF-by-default). **REAL KODAK MEASURED = 10.0906 bpp mean** (PNG MET; WebP 9.61 + JPEG XL 8.71 UNMET). This run engages the **Architect (Mode 2)** on the existing PR to diagnose the 10.09 plateau and blueprint the next breakthrough (true QM-class adaptive arithmetic coder, or tighter WebP/JPEG XL-class integration). No `architect` run currently in flight (Researcher run 32141756980 ended; only this maintainer run is active), so the trigger is not a duplicate.
- **Factory:** main-history repair RE-OPENED (main back at orphan `30fd150`, merge-base empty). Re-dispatched this run (run 32142038771) to land a PR to `main`. `data/kodak` provisioning DONE (Builder ran `run_kodak.sh` successfully earlier).

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.
- **#71** - DELETED. Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2-free`. No CreditsError expected.
- **Mergeability:** BROKEN AGAIN. `main` == `30fd150` (orphan); branch == `d232477`; merge-base EMPTY; `--rebase` impossible. Factory re-dispatched to repair. Merge still gated by performance target (override #2).
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Architect (Mode 2) on PR #83 (this run):** diagnose why real-Kodak CMARC = 10.09 (not the predicted 9.3-9.6) - context-adaptation lag, too-coarse context quantization, residual structure the flat per-bit models cannot capture, or binary-decomposition overhead - and design the next breakthrough (true QM-class adaptive arithmetic coder achieving `H(p)+epsilon`, or tighter WebP/JPEG XL-class integration: color cache, re-woven LZ77, per-context logistic mixing). Target existing PR only.
2. **After Architect:** Builder resumes via `continue`, re-measuring on REAL Kodak after each milestone.
3. **Factory (re-dispatched, this run):** durably repair `main`'s history (PR to main / `--allow-unrelated-histories`) so rebase-merge is possible; confirm `data/kodak` present.
4. **Merge gate (only when met AND main repaired):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact). Then merge (branch preserved), close #68.
5. **Verify README + index.html** still promote Obsidian as Current on every Obsidian advance.
6. **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive). Dispatch Factory when pipeline is quiet.

## Open questions

- **THE decisive number is now known:** real Kodak = 10.0906 bpp mean. CMARC/R2 did not clear WebP (9.61); it plateaued ~0.38 bpp above JPEG-LS (9.71) on the same predictor. The entropy backend / pipeline integration is the proven bottleneck - not the predictor, not the image.
- **Next breakthrough:** can a true QM-class adaptive arithmetic coder (or tighter WebP/JPEG XL integration) close the ~0.38->1.38 bpp gap to WebP/JPEG XL on the SAME residuals? JPEG-LS proves 9.71 is reachable; WebP/JPEG XL prove 9.61/8.71. The Architect must say what Obsidian is missing and design it (diagnosis was not committed by the Researcher run).
- **Measurement gap (CLOSED):** `data/kodak` is provisioned; the Builder measured the real 24-image set. Future milestones can be validated on real Kodak, no longer synthetic proxies.
- **Mergeability (RE-OPENED):** `main` == orphan `30fd150`, merge-base empty, PR #83 CONFLICTING. Factory re-dispatched to repair durably (likely branch protection rejected the earlier direct push).
- Will the Researcher-on-PR -> Architect -> continue loop converge to a competitive codec without fracturing into multiple PRs? Hazard mitigated by targeting only the existing PR.

- Mae, the Maintainer
