# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~07:00Z, scheduled maintainer run 32225253381). **DECISIONS:** `[]` - a Builder is already in flight on PR #83 (run 32224220746, `build` job `in_progress`), so no duplicate `/oc continue` was fired. The CMARC path now **clears the WebP 9.61 gate** (forced cross-channel CARC = 9.7093 bpp; 13/24 images below WebP); the **JPEG XL 8.71 gate is still open** (9.71 > 8.71). No merge (owner override: ALL THREE gates must be met by the *default* shipped codec, and the branch is CONFLICTING). One PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred quiet run).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break STILL OPEN; rebase deferred)

- **Mergeability (BROKEN):** PR #83 OPEN, head `ccba7feac234ee217ff149fd1ee9b3dfaab0cd65`, `mergeable: CONFLICTING`, `origin/main` = `8f4c15b0871f7a3d70612726d76efccb48ab3654`, **no common ancestor with `main`** - `git merge-base origin/main opencode/issue68-20260818070512` returns EMPTY (verified live this run). Blocks the eventual `--rebase` merge.
- **Owner-mandated repair (overdue, deferred):** the Builder must rebase `opencode/issue68-20260818070512` onto `origin/main` (replay all codec commits on top of the new main, preserving every commit) and force-push the SAME branch - NO new PR. Deferred until the default codec actually beats GR on real Kodak (the performance gate is still unmet at the default layer).

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `ccba7fe`). Real Kodak (effort 4) numbers:
  - **Default shipped codec = adaptive GR (v1) at 10.16 bpp** (PNG 13.05 MET; WebP 9.61 MISSED by ~0.55; JPEG XL 8.71 MISSED by ~1.45).
  - **CMARC / CARC backend (forced via `OBSIDIAN_CARC=1`, OFF by default):** forced CARC = **9.7579 bpp**; with cross-channel = **9.7093 bpp** (13/24 images below WebP 9.61). This **clears the WebP gate** but is still **0.80 bpp above JPEG XL 8.71**. Bit-exact: 8000 fuzz round-trips, md5/CRC verified.
- **CMARC lineage (R1 -> R4) built; the entropy core is now correct:**
  - **R4 coder FIXED as CACM87 (Witten-Neal-Cleary binary arithmetic coder)** - replaces the broken LZMA/WNC range-coder ports (commits `aca6650`, `7f636a4`). Efficiency gates `range_coder_skew_efficiency` + `cmarc_efficiency_vs_shannon` PASS.
  - **Decoder dispatch FIXED (commit `7b08964`):** encoder now signals CMARC so the decoder reaches the CMARC/CAPPED branch (the old routing no-op is resolved).
  - **CMARC Rice quotient FIXED (commit `ccba7fe`):** per-position adaptive bins (CMARC_QCAP=20) learn the geometric quotient like JPEG-LS QM, dropping forced CARC 11.11 -> 9.76 / 9.71 bpp, clearing WebP.
  - **CMARC ships OFF by default** behind `OBSIDIAN_CARC` / `EncodeOpts { cmarc }`; the never-expand safety net engages it only when it beats the model's best GR backend. So the *default* Obsidian is still GR 10.16 bpp.

## In flight

- **Builder (run 32224220746, `opencode`, event `issue_comment`, `build` job `in_progress` as of this run).** Spawned by the owner's `/oc continue` (last PR comment 08:03:10Z). It is the NEXT iteration after ccba7fe, expected to drive toward the **JPEG XL 8.71 gate** (per the Architect roadmap: M2.5 context mixing ~9.0-9.3, then M3 LZ77 + self-correcting weighted predictor to clear 8.71) and/or to **wire CMARC as the default shipped entropy backend** so the measured codec reflects the 9.71 bpp win. NOT re-fired by Mae this run (would duplicate). Watch for a new head + a real-Kodak CSV.
- **Review is STALE:** last `/oc approve` was at 07:52Z when head was ~`96a6075`; since then R3/R4/CMARC commits (incl. the CACM87 coder and the WebP-clearing quotient fix) were added. A fresh strict review is required before any merge, but deferred until the code stabilizes near the gate.
- No Architect / Researcher in flight.

## PENDING (deferred)

- **Wire CMARC/CARC as the DEFAULT shipped entropy backend** (or per-image auto-selection that picks the best of {GR, CMARC, CARC_LZ, CARC_MIX} by default) so Obsidian's *default* measurement clears WebP and heads toward JXL. Currently default = GR 10.16 bpp.
- **Clear JPEG XL 8.71 gate:** implement M2.5 (context mixing) + M3 (LZ77 + weighted predictor) on the now-correct CACM87 core; target < 8.71 on real Kodak effort-4, reproducible.
- **Branch rebase onto `main`** (owner directive): after the default codec beats GR; Builder force-pushes the SAME branch, verify MERGEABLE.
- **README / index.html Obsidian promotion** (standing directive, deferred).
- **Factory infra hardening:** `continue-on-error` still pending but non-blocking.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #88:** MERGED (commit 8f4c15b), branch preserved, #89 closed.
- **PR #83:** OPEN, head `ccba7fe`, `mergeable: CONFLICTING` (NO common ancestor with main - orphan break still open; rebase deferred until default codec beats GR). Builder `continue` in flight (run 32224220746).
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Let in-flight Builder (32224220746) finish** - do NOT re-fire `continue` (duplicate risk). Expect: CMARC wired as default and/or M2.5/M3 toward JXL 8.71, plus a fresh real-Kodak CSV.
2. **After it lands + re-measures:** assess whether the *default* Obsidian mean bpp is now < 9.61 (WebP) AND < 8.71 (JPEG XL) AND < 13.05 (PNG), reproducible + bit-exact. If WebP cleared but JXL not, re-fire `continue` for M2.5/M3; if JXL cleared, proceed to merge prep.
3. **Rebase branch onto `origin/main`** + force-push the SAME branch (clear CONFLICTING, preserve all codec work, no new PR) once the default codec beats GR.
4. **Re-fire strict `/oc review`** on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
5. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
6. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
7. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Is Builder run 32224220746 going to land the JXL-clearing stage (M2.5/M3) or just wire CMARC default?** Awaits the push.
- **Will the default shipped codec reach < 8.71 (JPEG XL) on real Kodak?** CMARC forced = 9.71; needs context mixing / LZ77 to close the last ~1 bpp. The CACM87 core reaches H(p)+epsilon, so the headroom is real.
- **Will CMARC become the default (auto-selected) or stay opt-in?** The owner gate is about the *default* Obsidian; if CMARC stays off by default, the gate cannot be met. The Builder must make the best backend default.
- **Will the branch rebase onto `main` succeed and make PR #83 MERGEABLE without a new PR?** Owner-requested, deferred until default codec beats GR.
- **One-PR integrity:** #83 sole canonical Obsidian PR; #84, #87 CLOSED.
- **Merge gate (owner override #2):** NOT met - default GR 10.16 bpp > WebP 9.61 > JXL 8.71. Even forced CMARC 9.71 clears WebP but not JXL.
- **Review staleness:** last approve at head ~96a6075; current head ccba7fe has CACM87 + WebP-clearing fix un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.

- Mae, the Maintainer
