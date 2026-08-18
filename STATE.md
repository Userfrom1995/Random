# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~04:27Z, `/oc maintainer` event run on issue/PR #80, run
  32099177407). The M1 build loop (resumed at 03:42Z) opened PR #80 but The Builder
  pushed a BROKEN milestone and stopped; resuming via `/oc continue`.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP,
  Kodak-benchmarked).** REOPENED earlier today (the factory round PR #79 auto-closed
  it on merge; the umbrella must stay open for M1-M3). Main build trigger target.
- **Checklist 10 shipped on main** (first Obsidian Kodak row: 27.8226 mean bpp,
  bit-exact). Reference baseline within ~0.5% of WangXuan95 2024 (JXL 8.7062, WebP
  9.6130, JLS 9.7113, J2K 9.5762, PNG ~13.05).
- Owner's standing directive: iterate until Obsidian beats the other codecs on
  Kodak (lossless + performance). M1-M3 are the optimization milestones.

## M1 build loop - STALLED BROKEN, RESUMING (PR #80)

- **PR #80 OPEN** by The Builder: branch `opencode/issue68-20260818034514`, head
  `e858ea0001bef32ce7cd71e6e33ae74171507a56`. 1 commit, +145/-335 across 3 files
  (`rans.rs` rewritten, `encoder.rs` FREQ_BITS=14, new `rans_adapt_test.rs`).
- **Broken:** the PR body admits adaptive tests still desync at `rans.rs:379/414`
  (decoder renorm/stream-exhaust line); "the encoder/decoder lockstep for the
  single-symbol and renorm-pressure cases is not yet balanced." The Builder pushed a
  broken milestone (per the hardened MILESTONE COMMITMENT rule) and stopped.
- **Drift:** `progress/68-*.md` still lists the older branch
  `opencode/issue68-20260817231515` while the live PR branch is
  `opencode/issue68-20260818034514`. The Builder should refresh this on resume.
- **Action this run:** `continue` (PR #80) -> `/oc continue` resumes the build loop
  from `progress/68-*.md` so the Builder fixes the lockstep. The lockstep was solved
  once before (progress log 2026-08-17T20:30, "fixed the adaptive rANS lockstep...
  forward dry-run recording (freq,cum), code in reverse via put_fc") then regressed in
  the subsequent variable-total rewrite, so the proven pattern exists to reuse.
- **No review/test yet:** code fails its own adaptive tests, so the quality gate is
  premature. Pipeline order: Builder -> Reviewer -> Tester -> merge.

## Factory round - COMPLETE (PR #79 merged at 03:42Z)

- Builder prompt hardened (`ALWAYS UPDATE PROGRESS FILE BEFORE PUSH` +
  `MILESTONE COMMITMENT`); `opencode.json` model -> hy3-free. Both applied to main.
- Workflow YAML model switch (hy3-free) already on origin/main. No CreditsError expected.

## In flight

- **M1 build (PR #80)** - RESUMING via `/oc continue` this run (Builder fixes the
  adaptive rANS lockstep). Also a GENERAL opencode run (32099177354) is in_progress,
  triggered by the owner's `/oc maintainer` comment; it is a general assistant and
  will not push a fix, so `/oc continue` is the driver.
- No opencode review/test runs in flight (none pending on PR #80). No held runs.

## Issues

- **#68 (Obsidian umbrella)** - REOPENED; M1 build trigger target (PR #80).
- **#77 (checklist 10)** - CLOSED via PR #78.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.

## Factory rounds

- **M1 build-loop hardening** - DONE (PR #79 merged at 03:42Z).
- **Fix-trigger guard relaxation (QUEUED)**: Reviewer/Tester findings comments don't
  match opencode.yml's exact `/oc fix` trigger. NOT dispatched (no-concurrent-factory
  rule: a build is in flight). Dispatch in the next idle window.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model:
  opencode/mimo-v2.5-free`. All workflow `.yml` agent steps pinned to `opencode/hy3-free`.
  Reviewer/test/factory on mimo-v2.5-free. No CreditsError expected.

## Next steps

1. **Shepherd the resumed M1 build (PR #80):** watch for the Builder's passing commit
   (adaptive tests green). On push: auto-reviewer -> review -> test -> merge (Obsidian
   continuation, no shipping cap concern).
2. **If the build stalls again on the lockstep** (same wall after resume), dispatch
   `research` on #68 for the adaptive rANS correctness math before another build attempt.
3. **After M1 lands:** M2 (self-correcting weighted predictor, within 10% of JPEG XL)
   and M3 (squeeze/interlacing or improved context model).
4. **Fix-trigger guard factory round:** dispatch in the next idle window (no opencode
   build/review/test in flight).
5. **#70:** Auditor owns the daily health summary; watch for anomalies.
6. **#42:** no board picks until Obsidian resolves (owner's freeze).
7. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the resumed M1 build fix the lockstep and land a real passing `builder:` commit,
  or does it hit the same wall again (escalate to Researcher)?
- Does hy3-free sustain the 60-minute engineering session well enough to finish M1?
- How far does M1 move Obsidian's Kodak mean bpp (27.82) toward/under WebP (9.61) and
  optipng PNG (13.05)?
