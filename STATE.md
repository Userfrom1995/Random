# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~07:26Z, maintainer run 32227837182 on PR #83). **DECISIONS:** `[]` - a Builder run is already queued (held `opencode-pr-trigger` 32227837502) and will resume on approval, so no duplicate `/oc continue` fired. The orphan-main break is now RESOLVED (PR MERGEABLE, merge-base == origin/main). Best real-Kodak = **9.7094 bpp mean** (CMARC safety-net + cross-channel); still above WebP 9.61 (~0.10) and JPEG XL 8.71 (~1.0). No merge (owner override: default codec must beat all three gates). One PR preserved.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (use `--no-delete-branch`).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred quiet run).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (not on issue #68).

## CRITICAL INFRASTRUCTURE STATE (orphan-main break RESOLVED; rebase satisfied)

- **Mergeability (FIXED):** PR #83 OPEN, head `69af6cf8e106b90bb4433b063cabeb5efeeffd0a`, `mergeable: MERGEABLE`. `git merge-base origin/main opencode/issue68-20260818070512` == `8f4c15b` (== origin/main) - verified live this run. The Builder's `rebuild Obsidian docs and Kodak benchmark corpus onto main` commits (`833597f`, `058e045`) re-anchored the branch onto `main`, so the orphan-history break is gone and `--rebase` is now possible. The owner-requested rebase was satisfied without a new PR.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR, branch `opencode/issue68-20260818070512`, head `69af6cf`). Real Kodak (effort 4) numbers from `obsidian/results/2026-08-19-r3c-runmode.csv` (24-image set):
  - **Default shipped codec = adaptive GR (v1): 10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED; JPEG XL 8.71 MISSED).
  - **CMARC safety-net: 9.7579 bpp mean** (R5 quotient fix + R3-C run mode).
  - **Best auto-selected (CMARC safety-net + cross-channel): 9.7094 bpp mean** - ~0.10 bpp above WebP 9.61 (14+ of 24 above); ~1.0 bpp above JPEG XL 8.71. Bit-exact (8000 fuzz, CRC).
  - Forced CARC: 9.71 bpp; forced CARC + residual-context: 9.7579.
- **CMARC lineage (R1 -> R5) built; entropy core now correct:**
  - **R4 coder = CACM87 (Witten-Neal-Cleary binary arithmetic coder)** - proven correct; efficiency gates `range_coder_skew_efficiency` + `cmarc_efficiency_vs_shannon` PASS.
  - **R5 (CMARC Rice quotient fix):** per-run-position adaptive `BinModel` (`CMARC_QCAP=20`) learns the geometric quotient like JPEG-LS QM; dropped forced CARC 11.11 -> 9.71 bpp.
  - **R3-C (JPEG-LS run mode):** implemented (commits `1fce003`, `69af6cf`); neutral on real Kodak (9.7579 -> 9.7579).
  - CMARC ships OFF by default behind `OBSIDIAN_CARC` / `EncodeOpts { cmarc }`; the never-expand safety net engages it only when it beats the model's best GR backend. So the *default* Obsidian is still GR 10.0906 bpp.

## In flight

- **Builder (held `opencode-pr-trigger` run 32227837502, spawned 07:26:30Z by the PR push, status `action_required`).** Will resume as a build on the same branch once my workflow's hardcoded PAT step approves the held run. It continues toward the **JPEG XL 8.71 gate** (per Architect roadmap: R2.4 logistic context mixing / per-context prediction refinement) and re-measures real Kodak effort-4. NOT re-fired by Mae this run (would duplicate / cause a push race).
- **Review is STALE:** last `/oc approve` was at 2026-08-18 07:52Z (head ~`96a6075`); since then R4 CACM87, R5 quotient fix, R3-C run mode, and the Kodak corpus were added. A fresh strict review is required before any merge, but deferred until the code stabilizes near the gate.
- No Architect / Researcher in flight.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** implement R2.4 (logistic context mixing) and/or per-context predictor refinement on the now-correct CACM87 core; target < 8.71 on real Kodak effort-4, reproducible.
- **Make the best backend the DEFAULT** (or per-image auto-selection that picks the best of {GR, CMARC, CARC_LZ, CARC_MIX} by default) so Obsidian's *default* measurement clears all three gates. Currently default = GR 10.0906 bpp.
- **README / index.html Obsidian promotion** (standing directive, deferred).
- **Factory infra hardening:** `continue-on-error` still pending but non-blocking.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `8f4c15b`.
- **PR #83:** OPEN, head `69af6cf`, `mergeable: MERGEABLE` (orphan break resolved). Builder `opencode-pr-trigger` held (32227837502) -> resumes on approval.
- **PR #84 and PR #87:** both CLOSED (redundant second PRs for #68, rejected per one-PR rule).

## Next steps

1. **Let the held Builder (32227837502) resume** - do NOT re-fire `continue` (duplicate/push-race risk). Expect: R2.4 context mixing toward JXL 8.71 + a fresh real-Kodak CSV.
2. **After it lands + re-measures:** assess whether the *default* Obsidian mean bpp is now < 9.61 (WebP) AND < 8.71 (JXL) AND < 13.05 (PNG), reproducible + bit-exact. If WebP cleared but JXL not, re-fire `continue` for R2.4/LZ77; if JXL cleared, proceed to merge prep.
3. **Re-fire strict `/oc review`** on the stabilized head; only merge after `/oc approve` + `/oc approve-test` with no newer `/oc fix`.
4. **After a reproducible real-Kodak number below all three gates:** rebase-merge (`--no-delete-branch`), close #68.
5. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current.
6. **Factory infra hardening:** `continue-on-error` still pending; non-blocking.

## Open questions

- **Will the resumed Builder clear JPEG XL 8.71?** Best CMARC config = 9.7094 (still ~1.0 bpp above JXL). R2.4 context mixing earlier regressed on synthetic; needs validation on real Kodak. The CACM87 core reaches H(p)+epsilon, so headroom is real.
- **Will CMARC become the default (auto-selected) or stay opt-in?** The owner gate is about the *default* Obsidian; if CMARC stays off by default, the gate cannot be met. The Builder must make the best backend default.
- **Merge gate (owner override #2):** NOT met - default GR 10.0906 bpp > WebP 9.61 > JXL 8.71. Even best auto-selected (9.7094) clears only ~0.10 above WebP; JXL unmet.
- **Review staleness:** last approve at head ~96a6075; current head 69af6cf has CACM87 + R5 + R3-C + Kodak corpus un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current on README.md / index.html despite the standing directive.
- **Factory infra hardening:** `continue-on-error` still pending.
- **Orphan-main break:** RESOLVED (PR MERGEABLE). The branch was re-anchored onto main by the Builder's `rebuild ... onto main` commits; no new PR needed.

- Mae, the Maintainer
