# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~07:21Z, maintainer run 32343616153, owner `/oc maintainer` nudge). PIVOT: the held R13-B build (run 32336195985) completed as a NO-OP (branch head unchanged at `99fdfed`, no summary comment, no commit). Decision = re-drive `continue` on PR #93 to obtain a REAL R13-B measurement (the documented escape hatch needs that data; we never got it). Gates unchanged (JXL 8.71 still +0.81 unmet).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge` (#91 + #92 branches `opencode/lab-68-orphan-main-guard` and `opencode/orphan-main-guard-2` intentionally left intact).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. Still deferred; schedule once JXL nears.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** PR #93 is the single canonical, open Obsidian PR (supersedes closed #83), branch `opencode/issue68-20260818070512`.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec).
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #93 (or issue #68 for factory/lab) - not on a new PR.

## CRITICAL INFRASTRUCTURE STATE (orphan-main guard MERGED; branch RE-LINKED & PR #93 OPEN)

- **PR #91 MERGED:** orphan-main guard (literal `Closes #68` commit token reopened #68 same run).
- **PR #92 MERGED:** `main` = `d6b2894`. Determinism guard + "do not auto-close umbrella" rule + force-with-lease pin. Body `Refs #68`.
- **`main` = `d6b2894`** (healthy, 370 commits, clean descendant of prior main).
- **Branch `opencode/issue68-20260818070512` RE-LINKED** (head `99fdfed0da3d89200e45e950da789f1ff13bfe79`, merge-base `d6b2894` non-empty). PR #93 is the single canonical Obsidian PR (`Refs #68`). ORPHAN PROBLEM RESOLVED.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub auto-closes #68 if the literal `Closes #68` token appears ANYWHERE. Future Builder/Architect/Lab commits MUST use `Refs #68` / `Refs to #68`. PR #93 body is correctly `Refs #68`.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian):** OPEN, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **Default shipped codec = 9.5208 bpp mean** (R10-B CFL, CMARC backend). Beats PNG (13.05) + WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
- **R0-R11 codec shipped on PR #93:** Golomb-Rice, CMARC binary range coder (R4, H(p)+epsilon), context-tree weighted predictor (R9-B), R10 Squeeze + chroma-from-luma, R11 cross-band in-loop predictor, R11-D MA-tree-lite combined gradient+residual context (opt-in). R11-A cross-band `wLL` reverted (45x slowdown, wash). R12-A per-band weighted predictor committed but moot (Squeeze rejected on photographic Kodak; `transforms::squeeze` is quincunx subsampling, not a wavelet).
- **R13 blueprint (Architect, committed `3e1f88c`):** two levers - R13-A (recursive self-correcting adaptive multi-tap predictor, TM-WP class) + R13-B (CDF 5/3 lifting wavelet replacing inert quincunx subsampling). R13-A implemented (`ba0ac46` + progress fix `99fdfed`), **REGRESSED** (auto-selected -> 9.9065 bpp; muted to keep 9.5209), 139 tests pass. **R13-B NOT yet implemented - the dispatch run 32336195985 no-op'd.**

## CURRENT BUILD STATE (R13-B dispatch NO-OP'd; re-driving for a real measurement)

- **R13-A result (Builder run, completed 2026-08-20T05:32:44):** forced-standalone ~11.18 bpp; auto-net 9.9065 bpp (sum-of-zigzag proxy over-selects the 9-feature LMS: lower training RSS but fatter-tailed residuals); **muted to keep production at 9.5209 bpp** (baseline 9.5208). 139 lib tests pass. Head `99fdfed`.
- **R13-B build run 32336195985 (dispatched by run 32336016252 via `continue` at 05:35:43Z):** ran ~1h45m, ALL workflow steps reported `success` (build, verify-pushed, forward-builder-decision, strip-trailers, approve-CI), but it was a **NO-OP** - branch head unchanged at `99fdfed`, no builder summary comment, and `git ls-remote` confirms the PR branch still points at `99fdfed0da`. So no R13-B code was committed and no Kodak measurement was produced. The prior three maintainer runs (32341545978 / 32341749235 / 32341762231) held for ~1.5h waiting on a measurement that never landed.
- **Verdict (robust, 7 axes + a hollow R13-B attempt):** the +0.81 bpp JXL gap is a **STRUCTURAL ARCHITECTURAL CEILING** of the single-pixel 4-tap linear predictor pipeline. Failed axes: R11-D MA context (wash), R11-A cross-band `wLL` (wash + slowdown, reverted), 64-leaf weight context x2 (regression, reverted), R12-A per-band decorrelation (moot; Squeeze rejected), CMARC backend (near-optimal), R13-A adaptive multi-tap (regressed under never-expand net). R13-B (lifting) is the ONLY remaining designed lever in the blueprint, but we have NO measurement for it because its build no-op'd.
- **Architect's R13-B gate math:** ~9.0-9.3 bpp alone; combined with a fairly-evaluated R13-A the target is < 8.71. Honest risk: R13-B alone likely still MISSES 8.71 even when real - so a fresh Researcher brief is the probable next step, but only AFTER we have the actual number.

## In flight

- **R13-B build RE-DRIVEN by this run (32343616153) via `continue`:** re-drive the R13-B CDF 5/3 lifting implementation + fair R13-A re-evaluation, and REQUIRE a real-Kodak effort-4 measurement posted as a summary comment. No collision risk now (run 32336195985 is `completed`). If this re-drive also no-ops, the next survey fires `research` for a fresh paradigm rather than retrying a third time.
- **No other builds in flight:** only this maintainer run is `in_progress` (32343616153); the opencode PR-trigger/deploy runs are short success/skipped, no other Builder active.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above (default 9.5208); current lever = R13-B lifting (re-driven this run; need a real measurement).
- **If R13-B misses (likely per Architect):** fresh Researcher brief (learned / context-tree weighted predictor at the transform level) - NOT R7-class single-pixel tuning. Documented escape hatch; fire on the next survey if the re-driven R13-B run confirms the miss or no-ops again.
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once JXL nears).
- **Review staleness on #93:** head `99fdfed` is clean (139 tests pass); fresh Reviewer + Tester gate required before any merge (and still premature until R13-B resolves).
- **Commit-message hygiene:** never write literal `Closes #68` token in ANY commit message or PR body.

## Issues

- **#68 (Obsidian umbrella)** - OPEN, active fundamental goal, stays open until codecs beaten.
- **#52 / #89 / #90 / #91 / #92 infra** - #90 MERGED; #89 CLOSED; #52 related; #91 MERGED (guard); #92 MERGED (guard + umbrella rule + force-with-lease pin). Both branches kept.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule; board live.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError` in recent runs.
- **pages.yml:** green.
- **PR #93 checks:** opencode-pr-trigger SUCCESS on recent pushes; pages deploy SKIPPED (expected for PR preview), GitGuardian SUCCESS.

## Next steps

1. **Await the re-driven R13-B build (this run's `continue`):** when it pushes + measures, re-survey (a maintainer run auto-triggers on the PR push). If R13-B + fairly-evaluated R13-A approach < 8.71, continue refining toward the gate; if it still misses (or no-ops again), dispatch `research` for a fresh paradigm (context-tree weighted prediction at transform level, or a learned predictor) - NOT R7-class tuning.
2. **After gates clear:** fresh Reviewer + Tester gate, then rebase-merge (`--no-delete-branch`) and close #68. NOT before.
3. **README / index.html promotion:** schedule once JXL nears / PR clears.

## Open questions

- **Will R13-B (lifting) + fairly-evaluated R13-A clear the JXL 8.71 gap?** UNKNOWN - run 32336195985 no-op'd with no measurement. Architect estimates ~9.0-9.3 for R13-B alone (likely still short); combined target < 8.71. Re-driven this run; must produce a real number.
- **If R13-B misses, what next paradigm?** Fresh Researcher brief (learned / context-tree predictor at the transform level), since all single-pixel and context-tuning axes are exhausted. Documented escape hatch; fire next survey if the re-drive confirms the miss or no-ops again.
- **Merge gate (owner override #2):** NOT met - default 9.5208 beats PNG + WebP but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **One-PR integrity:** INTACT (PR #93 single canonical, OPEN, shares history with main).
- **Orphan-main break:** RESOLVED (merge-base `d6b2894` non-empty; PR #93 healthy).
- **Build collision:** CLEARED - run 32336195985 is `completed`; the re-driven `continue` in this run is safe (no second Builder on the branch).
- **R13-B no-op root cause:** unknown - run 32336195985 reported all steps success but pushed no commit and posted no comment. Treated as a hollow/half-failed build; re-drive once before escalating. If it repeats, the opencode.yml "verify pushed" / "forward builder decision" steps need a Lab Engineer look (possible silent drop of the agent's decision/commit).
- **Review/Tester:** neither has run on PR #93 yet; both required pre-merge.
- **pages.yml:** green.
- **Billing:** resolved (no `CreditsError`; `small_model` correctly pinned free).
- **Commit-message hygiene:** PR #93 body is correctly `Refs #68`; future commits/blueprints must avoid literal `Closes #68`.

- Mae, the Maintainer
