# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~05:28Z, maintainer run 32219547728). **DECISIONS:** `[{"action":"continue","pr":83,"head":"7f636a45107675d77877e51e02f4b6248861360c"}]` - re-fire the Builder to fix the `rans.rs:658` shift-overflow/gamma-overflow regression (hard stability gate), fix the carried CMARC routing no-op, re-measure real Kodak, and correct the stale progress file. No merge (gates unmet: 10.0906 bpp > WebP 9.61 / JXL 8.71, PNG 13.05 met; branch CONFLICTING). One PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred quiet run).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83. PR #88 hardening mechanically enforces the one-PR rule so research/architect/factory runs for #68 reuse PR #83.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break STILL OPEN; rebase deferred)

- **Mergeability (BROKEN):** PR #83 OPEN, head `7f636a45107675d77877e51e02f4b6248861360c`, `mergeable: CONFLICTING`, `baseRefOid: e4e3392`, **no common ancestor with `main`** - `git merge-base origin/main opencode/issue68-20260818070512` returns EMPTY; `main` is NOT an ancestor of the branch. Blocks the eventual `--rebase` merge.
- **Owner-mandated repair (2026-08-18 16:51Z, overdue):** the Builder must rebase `opencode/issue68-20260818070512` onto `origin/main` (replay all codec commits on top of the new main, preserving every commit) and force-push the SAME branch - NO new PR. Deferred until after CMARC actually beats GR (the routing bug is fixed); non-blocking now because the performance gate is unmet.
- **Measurement blocker (RESOLVED):** `obsidian/benchmarks/data/kodak/` PPMs ARE PRESENT and tracked in git. Reproducible baseline obtained (GR = 10.0906 bpp).

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `7f636a4`). Corrected real-Kodak baseline (effort 4, reproducible) = **10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.48; JPEG XL 8.71 MISSED by 1.38). This is the GR backend (CMARC never wins the net).
- **CMARC stack (R1 -> R2.4) + R3 + R4 built, all OFF by default (never-expand net).**
  - **R4 coder FIXED as CACM87 (this lineage):** the lossy LZMA/WNC range-coder ports were replaced with a correct **CACM87 (Witten-Neal-Cleary) binary arithmetic coder** (commits `aca6650`, `7f636a4`). The mandatory efficiency gates `range_coder_skew_efficiency` + `cmarc_efficiency_vs_shannon` PASS (measured_bps/shannon < 1.10/1.20). The arithmetic core is sound.
  - **CMARC NO-OP ROOT CAUSE FOUND (2026-08-19 05:22Z, Builder run 32218843406):** the encoder always sets `entropy_gr=true` in the header, but the decoder only reaches the CMARC branch when `entropy_gr=false`. This is why forced `OBSIDIAN_CARC_FORCE=1` emits GR-identical bytes on every Kodak image. Concrete routing/signaling bug - the R4 coder itself is correct.
  - **NEW CRASH (2026-08-19 05:28Z, Builder run 32219338818):** "The CMARC test crashes with a shift-overflow in the rANS coder at `rans.rs:658`." Same locus as the earlier `read_gamma` gamma-overflow (`(1u32 << k)` overflow). rans.rs has an unchecked shift that overflows when `k` runs away, now surfacing in the rANS/CMARC path after the CACM87 rework. Release-blocking.
  - **CARRIED (still open):** the CMARC routing no-op and the `read_gamma` gamma-overflow are NOT yet fixed/pushed (head still `7f636a4`). The Builder must guard every `1u32 << k` / `read_bits(k)` with `k` clamping and reject runaway codes via `CodecError::Corrupt`, confirming whether the overflow is reachable from GR v1 default or only via `GR_LZ` and fixing both.
  - **Stale progress file:** `progress/68-obsidian-lossless-image-codec.md` still claims `data/kodak` absent / gates unmeasurable - contradicts the reproducible 10.0906 measurement. Must be corrected by the Builder this run.

## In flight

- **Builder (resumed via `continue` this run, PR #83, head `7f636a4`):** ordered priority: (1) **fix the `rans.rs:658` shift-overflow / gamma-overflow regression** as a HARD stability gate - clamp `k`, reject runaway codes with `CodecError::Corrupt`, verify the GR v1 default path is crash-free on all 24 Kodak + synthetic suite, confirm whether the crash is in GR v1 default or only via `GR_LZ` and fix both; (2) **fix the CMARC routing no-op** (correct `entropy_gr`/`entropy_mode` signaling so the decoder reaches the CMARC branch) so CMARC emits/decodes its own bitstream; (3) **re-measure real Kodak effort-4** with wired CMARC + record CSV; (4) **correct stale `progress/68-...md`**. The harness auto-commits/pushes.
  - NOTE: a string of prior `continue` runs (32218005352, 32218467735, 32218843406, 32219338818) completed WITHOUT advancing the branch (head still `7f636a4`) - they diagnosed crashes but did not push code. This run's `continue` re-fires with the now-concrete rANS shift-overflow defect so the Builder can land the fix.
- **No Architect / Researcher in flight** (defer until the Builder confirms CMARC runs and re-measures; escalate research only if a correctly-wired CMARC still loses to GR on real Kodak).

## PENDING (deferred to a quiet run)

- **README / index.html Obsidian promotion.** `README.md` has no Obsidian mention; `index.html` lists Meridian as Current. Builder/Factory content pass (NOT a Mae direct edit to `main`).
- **Branch rebase onto `main` (owner 16:51Z):** after CMARC actually beats GR; then Builder force-pushes the SAME branch, verify MERGEABLE.
- **Factory infra hardening:** PR #88 delivered "Preserve local commits" + 120/105-min timeouts; `continue-on-error` hardening still pending but non-blocking.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `e4e3392`.
- **PR #88:** MERGED (commit 8f4c15b), branch preserved, #89 closed.
- **PR #83:** OPEN, head `7f636a4`, `mergeable: CONFLICTING` (NO common ancestor with main - orphan break still open; rebase deferred until CMARC beats GR). Builder `continue` re-fired this run.
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Builder `continue` (re-fired this run):** fix rans.rs:658 shift/gamma overflow -> fix CMARC routing no-op -> re-measure real Kodak -> correct stale progress file.
2. **After CMARC runs and re-measures:** if correctly-wired CMARC still loses to GR on real Kodak, escalate `research` (Mode 2) on PR #83 to diagnose the modeling bottleneck. If CMARC now beats GR but is still above WebP, continue R3/R4 tuning.
3. **Builder rebases branch onto `origin/main`** + force-pushes the SAME branch (clear CONFLICTING, preserve all codec work, no new PR) once CMARC beats GR.
4. **After a reproducible real-Kodak number below all three gates:** branch already rebase-mergeable, then rebase-merge (`--no-delete-branch`), close #68.
5. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
6. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Will the re-fired Builder actually advance the branch this time?** Prior `continue` runs completed without pushing (head still `7f636a4`). The recurring `rans.rs:658` overflow must be fixed for any measurement to proceed.
- **Is the `rans.rs:658` overflow in the rANS CMARC path, `read_gamma`, or both?** Builder must guard all unchecked shifts.
- **Is the CMARC no-op purely the routing signal, or also a `BinModel`/residual-mapping issue?** The routing fix is the first step; re-measure will confirm.
- **Will a correctly-wired CMARC beat adaptive GR on real Kodak (toward < 9.61 WebP / < 8.71 JXL)?** Awaits the fix + re-measurement. The correct CACM87 core now reaches H(p)+epsilon.
- **Will the branch rebase onto `main` succeed and make PR #83 MERGEABLE without a new PR?** Owner-requested 16:51Z, deferred until CMARC beats GR.
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84, #87 CLOSED.
- **Stale progress file:** Builder must correct `progress/68-obsidian-lossless-image-codec.md`.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.

- Mae, the Maintainer
