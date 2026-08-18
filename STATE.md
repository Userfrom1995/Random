# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~06:13Z, event run on PR #82, run 32105947123, owner `/oc maintainer`). This was a redundant re-dispatch: the Builder is already in flight (run 32105937514, `continue`) implementing M0 (Golomb-Rice entropy) on PR #82's branch. No new trigger posted this run. All three standing owner directives on PR #82 are unchanged and enforced.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it. Incremental improvement PRs may merge as the loop runs; only the *project* is "done" when the codecs are beaten.
- **Never delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. (PR #78's branch is already gone and cannot be recovered.)
- **Website + README must track the active project.** The next Obsidian PR must add Obsidian to `README.md` (Current Project) and promote it to Current on `index.html` (currently still Meridian), plus fix the meta description. Verify before merge.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED 2026-08-18; stays OPEN until codecs beaten.
- **M1 (v1) shipped** via PR #78 (merged 2026-08-18T00:03:16Z): Obsidian v1 = 27.8226 mean bpp (bit-exact), vs WebP 9.6130 / optipng PNG 13.0518 / JPEG XL 8.7062. NOT competitive - the entropy stage expands the container.
- **Research + Architecture delivered** (PR #82, by Dr. Mob / the Architect): defect is purely entropy-coding; fix = replace per-context 512-symbol adaptive rANS with per-context adaptive Golomb-Rice (Design A, `ENTROPY_GR` flag), provably non-expanding; Design B (capped escaped static rANS) scoped for M2/M3. Milestones rebased: M0 ~9.7 bpp (JPEG-LS), M1 beat WebP 9.61, M2/M3 approach JPEG XL 8.71.
- **Build M0 in flight (this run):** opencode build run **32105937514** is `in_progress` on branch `opencode/issue68-20260818055633` (build job + general subagent). Implements GR entropy, gates behind `model.rs::analyze.entropy_gr`, re-runs Kodak harness. NOT to be merged until target met.

## In flight

- **Build (M0, #68 / PR #82):** run 32105937514 (`in_progress`), triggered by owner `/oc continue` at 06:12:21. Builder resumes on `opencode/issue68-20260818055633`, implements Golomb-Rice entropy, benchmarks Kodak. This maintainer run (32105947123) did NOT post a duplicate `continue` because the build is already active.
- **Held runs on PR #82** (opencode-pr-trigger, pages deploy) - approved by the prior run's hardcoded PAT step.

## Issues

- **#68 (Obsidian umbrella)** - REOPENED; active fundamental goal, stays open until codecs beaten.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves (owner directive).
- **#71** - DELETED (HTTP 410). Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2.5-free`. No CreditsError expected.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Builder M0 (PR #82, run 32105937514)** -> implement GR entropy, report Kodak mean bpp. Then route Reviewer (`review`) -> Tester (`test`) -> loop M1/M2/M3 until WebP/PNG/JPEG XL beaten. DO NOT merge until target met.
2. **PR #82 must update README.md + index.html** (Obsidian = Current Project) before merge - verify at merge time.
3. **Factory PR to harden maintainer.md** - remove `--delete-branch` so PR branches are preserved after merge (owner directive). Track and merge.
4. **Brainstorm board (#42):** stays frozen until Obsidian resolves.

## Open questions

- How far does Obsidian's Kodak mean bpp move after M0 (GR entropy) - does it hit the ~9.7 bpp JPEG-LS target and stop expanding? (Watch run 32105937514 output.)
- M1 (per-context predictor selection + GR) must get under WebP 9.61; M2/M3 (capped rANS / squeeze) must approach JPEG XL 8.71. Will the staged plan hold?
- Will the durable branch-preservation rule (maintainer.md update via Factory PR) land cleanly and stop future `--delete-branch` merges?
