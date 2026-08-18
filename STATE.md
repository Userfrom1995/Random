# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~15:05Z, maintainer run 32152174649, triggered by owner `/oc maintainer` on issue #68). **DECISIONS:** `[]` (no triggers). The Builder `continue` run `32151973192` is already in flight on the single canonical PR #83 - firing any build/architect trigger now would be a duplicate/conflict. Watching the run; will route Architect (next milestone) + continue loop once the Builder frees the branch. No merge (gates unmet / reproducible measurement still being established).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: this is currently NOT satisfied (see Open questions) - flagged for a Builder/Factory pass, not a direct `main` edit by Mae.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. The Factory must NEVER open a redundant codec PR for an issue that already has an open Obsidian PR - it must push to the existing branch.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. They are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE STATE (measurement BLOCKER - root cause understood, path set)

- **Mergeability:** PR #83 OPEN, head `7f7684219e77df3fa6941f310d407ed45226a71d`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`, valid merge base. `--rebase` of #83 is possible once the target is met. (main has advanced to `e4e33928` via infra merges; branch remains cleanly mergeable onto it.)
- **Root cause of the data blocker (resolved as a misroute):** the Kodak PPMs can never be committed to git because `obsidian/benchmarks/data/kodak/` is **git-ignored by design** (only `obsidian/benchmarks/data/kodak.sha256` is tracked - per `obsidian/docs/benchmark-methodology.md` and `obsidian/.gitignore`). The **Factory Engineer is the WRONG agent for this** (its prompt forbids touching `/obsidian/`), so every Factory dispatch for "provision data/kodak" misrouted into prompt/workflow hardening instead of landing data. The correct owner is the **Builder**, who runs in the build env and already once obtained matching PPMs. The PPMs are fetched+normalized into the working tree at benchmark time and verified against `kodak.sha256`; they are not meant to live in git.
- **Harness hardening landed (commit `a06d34a` on PR #83's branch):** `obsidian/benchmarks/run_kodak.sh` is now self-provisioning (`--provision` download+convert+manifest), fail-fast sha256-verifying the 24 PPMs, `--require-refs` gated, with an explicit competitive-gate summary (Obsidian mean bpp vs JXL 8.71 / WebP 9.61 / PNG 13.05). The gate is now reproducible in any Builder env with network + toolchain.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `7f76842`). **ROOT-CAUSE FIX THIS CYCLE:** `ppm.rs` decoded the interleaved P6/P5 raster as planar, scrambling R/G/B, so all pre-15:00Z Kodak numbers were invalid. Fixed; codec bit-exact. Corrected real-Kodak baseline (effort 4) = **10.16 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.45; JPEG XL 8.71 MISSED by 1.45). Residual-entropy floor ~10.1 bpp confirmed as the real limit of the current GAP predictor + Golomb-Rice stack.
- **Next milestone path (progress file):** JPEG-LS-class bias cancellation (dead-zone, not the reverted naive EMA) + run mode, then context mixing / LZ77 preprocessing to clear WebP and approach JPEG XL.

## In flight

- **Builder `continue` run `32151973192`** (owner `/oc continue` at 15:01:49Z, in_progress since 15:01:52Z): making Kodak acquisition reproducible in CI (fetch+normalize 24 PPMs, `sha256sum -c data/kodak.sha256`) + re-measuring REAL Kodak effort-4, and implementing JPEG-LS-class bias cancellation + run mode. This is the active orchestration step - watched, no duplicate trigger.

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
- **Mergeability:** PR #83 OPEN, head `7f76842`, `mergeable: MERGEABLE` (CLEAN). `--rebase` possible once target met.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Watch Builder `continue` run `32151973192`:** it must produce a reproducible real-Kodak number + bias-cancellation attempt. Re-survey on its next push.
2. **If still above JPEG-LS 9.71 (9.71):** route **Architect** on existing PR #83 (Mode 2, NO new PR) to design context-mixing / LZ77 preprocessing; re-engage **Researcher** for bottleneck math. Then `continue` on the same branch. Loop until gates cleared.
3. **After a reproducible real-Kodak number below all three gates:** merge (branch preserved per owner directive), close #68.
4. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.

## Open questions

- **Will the in-flight Builder reproduce the exact Kodak PPMs?** The 10.0906 bpp run proved a working source existed in-env; `run_kodak.sh --provision` must recover/automate it. If Kaggle needs CI-unavailable auth, validate the r0k.us-PNG -> P6 PPM fallback against `kodak.sha256`; if it mismatches, reconcile the hash set honestly (no faked data).
- **Will bias cancellation + run mode clear the WebP (9.61) gate on real Kodak?** Designed to cancel the GAP predictor's systematic residual bias (JPEG-LS-style dead-zone). If it still stalls above 9.71, context mixing / LZ77 is the remaining path; if that fails too, escalate to a true QM-class adaptive arithmetic coder (no autopilot `continue`).
- **One-PR integrity:** #83 is the sole canonical Obsidian PR; the Builder pushes to it, never opens a codec PR.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.

- Mae, the Maintainer
