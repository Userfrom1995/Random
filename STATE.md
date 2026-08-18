# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~15:00Z, maintainer run 32151273635, triggered by PR #83 event). **DECISIONS:** `continue` (#83) + `ping` (#83). Re-routed the Kodak measurement blocker from the Factory (wrong tool) to the Builder. No `factory` dispatch (Factory's Domain Scope forbids touching `/obsidian`, and the data folder is git-ignored by design). No merge (gates unmet / measurement still not reproducible).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: this is currently NOT satisfied (see Open questions) - flagged for a Builder/Factory pass, not a direct `main` edit by Mae.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (measurement BLOCKER - root cause now understood)

- **Mergeability:** PR #83 OPEN, head `7f7684219e77df3fa6941f310d407ed45226a71d` = `main` (`30fd150`) + clean commits, valid merge base, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. `--rebase` of #83 is possible once the target is met.
- **Root cause of the data blocker (NEW, this run):** the Kodak PPMs can never be committed to git because `obsidian/benchmarks/data/kodak/` is **git-ignored by design** (only `obsidian/benchmarks/data/kodak.sha256` is tracked - per `obsidian/docs/benchmark-methodology.md` and `obsidian/.gitignore`). Furthermore the **Factory Engineer is the WRONG agent for this**: its own prompt (`.github/agents/factoryengineer.md`, Domain Scope) forbids modifying user project source including `/obsidian/`. That is why every Factory dispatch for "provision data/kodak" silently misrouted into prompt/workflow hardening instead of landing data. The correct owner is the **Builder**, who runs in the build env and already once obtained matching PPMs (the 10.0906 bpp run). The PPMs must be fetched+normalized into the working tree at benchmark time and verified against `kodak.sha256`; they are not meant to live in git.
- **Net:** the gate is measurable ONLY if the Builder makes Kodak acquisition reproducible in CI. This run's `continue` + `ping` directs it to do exactly that.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `7f76842`). Last NON-reproducible real-Kodak effort-4 = **10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.48; JPEG XL 8.71 MISSED by 1.38). Reproducibility pending a reproducible in-CI Kodak fetch.
- **CMARC RESEARCH DELIVERED** (`obsidian/docs/research-breakthrough.md`): the ~10.1 bpp ceiling is the single-k/per-(cid,bin) GR-style coder, not the image; JPEG-LS reaches 9.71 bpp on the SAME Kodak corpus with the SAME LOCO-I GAP predictor but a context-based arithmetic (QM) coder.
- **CMARC ARCHITECT BLUEPRINT DELIVERED** (`obsidian/docs/architect-cmarc-blueprint.md`): CMARC as `entropy_mode` values (CARC=2, CARC_LZ=3, CARC_MIX=4).
- **CMARC BUILT END-TO-END (R1 -> R2.4), all OFF by default.** Production stays byte-identical to v1 GR. 106 lib tests pass.
- **R3 CORRECTED BLUEPRINT DELIVERED (14:29:43Z, run `32148118020`):** `architect-r3-residual-context-blueprint.md`. R3-B Golomb-Rice-through-binary using `CarcCtx.k` -> constant `cmarc_bins_per_ctx()=35`; neutral `CMARC_PRIOR=2048`; R3-A residual DIFF context capped <=365 ids; per-image winner-selection flag.
- **R3 IMPLEMENTED & PUSHED (head `7f76842`):** R3-B (neutral prior + Rice-through-binary magnitude, 35 bins) and R3-A (residual DIFF context as CMARC coding context, capped, winner-selection flag). UNMEASURED on real Kodak because the PPMs are git-ignored and were never reproducibly fetched in CI.

## In flight

- **Builder (resumed this run via `continue`):** must (1) make Kodak acquisition reproducible in CI - fetch+normalize the 24 PPMs so `sha256sum -c data/kodak.sha256` passes, reusing the source behind the 10.0906 bpp run (Kaggle `sherylmehta/kodak-dataset` or r0k.us PNGs -> P6 PPM); (2) if CI cannot reach an exact-hash source, report cleanly (no faked data); (3) run `run_kodak.sh --effort 4` and report REAL Kodak R3 vs WebP 9.61 / PNG 13.05 / JPEG XL 8.71. Keep seams OFF by default + never-expand net + per-image winner flag.
- **Factory run `32151205413` (owner-fired, in_progress):** being WATCHED. It is the wrong tool for obsidian data; if it opens any PR for #68 it will be closed next survey, keeping #83 canonical. Prior Factory runs (`160`/PR #84, `32148116537`/PR #85, `32150104809`, `32151115174`) did NOT land Kodak data (misrouted to prompt hardening) - confirming the misroute.

## PENDING (deferred to a quiet run)

- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Needs a Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Factory hardening (one-PR rule):** dispatch the Factory Engineer to harden the workflow/agent so it NEVER opens a new PR for an issue that already has an open Obsidian/codec PR; it must reuse/push to the existing branch. Deferred (owner said stop opening new PRs; also the Factory is the wrong data tool, so this is lower priority now).
- **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive).

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `main` workflow agent steps (factory/review/test) pin `opencode/hy3-free` (via merged PR #85). `opencode.json` `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free).
- **Mergeability:** PR #83 OPEN, head `7f76842` = main (`30fd150`) + clean commits, valid merge base, `mergeable: MERGEABLE` (CLEAN). `--rebase` possible once target met.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Builder (fired this run):** make Kodak acquisition reproducible in CI + re-measure R3 on REAL Kodak effort-4 vs WebP 9.61 / PNG 13.05 / JPEG XL 8.71. If a reproducible exact-hash source is unreachable in CI, the Builder reports and Mae escalates to the owner for a data strategy (download token, or accept locally-produced measurement). No autopilot `continue` past this point.
2. **After a reproducible real-Kodak number:** if R3 clears the gates -> continue toward merge; if it still stalls above JPEG-LS 9.71 -> re-engage Researcher/Architect for a true QM-class adaptive arithmetic coder.
3. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
4. **Merge gate (only when met AND reproducible):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact, reproducible). Then merge (branch preserved per owner directive), close #68.

## Open questions

- **Will the Builder's CI run reproduce the exact Kodak PPMs?** The 10.0906 bpp run proves a working source existed in-env; the Builder must recover/automate it. If Kaggle needs auth unavailable in CI, a fallback (r0k.us PNGs normalized to P6 PPM) must be validated against `kodak.sha256` - if it does not match, the hash set itself may have been generated from a different source and must be reconciled honestly.
- **Will corrected R3 clear the WebP (9.61) / JPEG XL (8.71) gates on real Kodak?** Neutral `CMARC_PRIOR` + Rice-through-binary + bounded DIFF context is designed to avoid the sparse-context regression; the Builder will measure it once data is reproducible. If it still stalls above 9.71 (JPEG-LS), a true QM-class adaptive arithmetic backend is the remaining path.
- **In-flight Factory `32151205413`:** watch for any PR it opens for #68; close it and keep #83 canonical if so.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **One-PR integrity:** #83 is the sole canonical Obsidian PR; the Builder pushes to it, never opens a codec PR.

- Mae, the Maintainer
