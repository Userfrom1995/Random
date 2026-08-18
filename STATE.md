# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~03:42Z, `/oc maintainer` event run on PR #79, run
  32096300250). Factory round #79 MERGED; M1 build loop RESUMED on the hardened
  Builder (hy3-free build model).

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP,
  Kodak-benchmarked).** REOPENED this run (PR #79's `Closes #68` auto-closed it
  on merge; the factory round only hardened the build loop, so the umbrella must
  stay open for the M1-M3 optimization). Main trigger target for the build.
- **Checklist 10 shipped on main via PR #78** (merge `de0074d3`): benchmark
  harness + reference baseline + first Obsidian Kodak row.
- **First Obsidian Kodak row: 27.8226 mean bpp (effort 4)**, bit-exact through
  the gate. Reference figures within ~0.5% of the independent WangXuan95 2024
  benchmark. JPEG XL 8.7062, WebP 9.6130, JPEG-LS 9.7113, J2K 9.5762, PNG ~13.0.
- Owner's standing directive (20:42:32Z): test BOTH losslessness and
  performance on Kodak, keep iterating until Obsidian beats the other codecs.
  M1-M3 are the optimization milestones.

## Factory round - COMPLETE (PR #79 merged)

- **PR #79 merged at 03:42:16Z** (commit `e856d16ac`, branch deleted). This was
  the factory round I dispatched on #68 at 03:15Z (run 32094693459) to harden
  the exhausted M1 build loop. 3 files: `builder.md` (+2 hardening rules),
  `opencode.json` (model -> hy3-free, small_model stays mimo-v2.5-free),
  `progress/68-*.md` (+8). Reviewer approved (14/14 checks); Tester
  approve-test; no post-approval `/oc fix`. Infra PR, no shipping cap.
- **Workflow model switch** to `hy3-free` applied directly on main earlier by the
  prior maintainer run (commit `11c097c`, "maintainer: update workflow model
  configuration") across opencode/maintainer/ideate/auditor - verified on
  origin/main. Builder/Maintainer/Ideator/Auditor now run on hy3-free.
- **Builder prompt hardened** (builder.md:69-70): `ALWAYS UPDATE PROGRESS FILE
  BEFORE PUSH` + `MILESTONE COMMITMENT`. Directly attacks the root cause: four
  60-min M1 attempts that did real work but never committed.

## M1 build loop - RESUMED this run

- Reopened #68 and dispatched `/oc build this` (decision.json) to resume M1
  (beat WebP lossless + optipng PNG on Kodak). With the hardened commit
  discipline + the hy3-free upgrade, the next run should land the first real
  `builder:` commit on an `opencode/issue68-*` branch instead of a silent no-push.
- Watched branch: an `opencode/issue68-*` branch for the first `builder:` push.

## In flight

- **M1 build (opencode build on #68)** - triggered this run; Builder should open
  its own new issue + PR per the prompt. No open PRs yet.
- No opencode review/test runs in flight (none pending). No held runs.

## Issues

- **#68 (Obsidian umbrella)** - REOPENED; M1 build trigger target (this run).
- **#77 (checklist 10)** - CLOSED via PR #78.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.

## Factory rounds

- **M1 build-loop hardening** - DONE (PR #79 merged this run).
- **Fix-trigger guard relaxation (QUEUED)**: Reviewer/Tester findings comments
  don't match opencode.yml's exact `/oc fix` trigger, so the Fixer only runs on
  an exact `/oc fix`. Not dispatched this run (no-concurrent-factory rule: a
  build is now in flight). Dispatch in the next idle window (no opencode
  build/review/test in flight).

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model:
  opencode/mimo-v2.5-free`. All workflow `.yml` agent steps pinned to
  `opencode/hy3-free`. Reviewer/test/factory on mimo-v2.5-free. No CreditsError
  expected.

## Next steps

1. **Shepherd the M1 build** on #68: watch for the first `builder:` commit on an
   `opencode/issue68-*` branch. On PR open: auto-reviewer -> review -> test ->
   merge (Obsidian continuation, no shipping cap concern).
2. **After M1 lands:** M2 (self-correcting weighted predictor, within 10% of JPEG
   XL) and M3 (squeeze/interlacing or improved context model). Keep the
   iteration loop going until Obsidian wins on Kodak.
3. **Fix-trigger guard factory round:** dispatch in the next idle window (no
   opencode build/review/test in flight).
4. **#70:** Auditor owns the daily health summary; watch for anomalies.
5. **#42:** no board picks until Obsidian resolves (owner's freeze).
6. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the hardened M1 build finally push a real `builder:` commit (and open a
  PR), ending the four-run no-push streak?
- Does hy3-free sustain a 60-minute engineering session better than
  deepseek-v4-flash-free did?
- How far does M1 move Obsidian's Kodak mean bpp (27.82) toward/under WebP (9.61)
  and optipng PNG (13.05)?
