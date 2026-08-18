# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~03:15Z, `/oc maintainer` event run on #68,
  run 32094693459). M1 build loop EXHAUSTED: 1 initial + 3 auto-retries, all
  four 60-minute attempts pushed nothing; verify errored with "Manual
  intervention required." Factory round dispatched to harden the loop.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP,
  Kodak-benchmarked).** CLOSED (auto-closed on the PR #76 merge); used as the
  `/oc build this` / `/oc factory` trigger target for the M1 milestone.
- **Checklist 10 shipped on main via PR #78** (merge commit `de0074d3`):
  `obsidian/benchmarks/` - run_kodak.sh, fuzz_gate.sh, aggregate.py,
  build_toolchain.sh + toolchain.md, pinned Kodak manifest (PCD0992, 24x
  768x512 P6 PPM), 168 fidelity-gated result rows (7 codecs x 24 images),
  reference-baseline CSV, README, docs/progress/ideas updates.
- **First Obsidian Kodak row: 27.8226 mean bpp (effort 4)**, bit-exact through
  the gate but not competitive. Reference figures land within ~0.5% of the
  independent WangXuan95 2024 benchmark on the same corpus (harness is honest):
  JPEG XL 8.7062, WebP 9.6130, JPEG-LS 9.7113, J2K 9.5762, PNG ~13.0.
- The owner's standing directive (20:42:32Z): test BOTH losslessness and
  performance on the Kodak dataset, keep iterating until Obsidian beats the
  other codecs. M1-M3 are the optimization milestones.

## M1 build loop - FAILED, paused pending factory fix

- **Attempt 1 (run 32083566693, 00:11Z)**: 60m diagnostic-only, no commit.
- **Attempt 2 (run 32087378098, auto-retry 2, 01:12Z)**: 60m, still no commit;
  auto-retry 3 posted.
- **Attempt 3 (run 32091030864, auto-retry 3, 02:12Z)**: 60m, no commit; verify
  step hit the 4-attempt cap and errored "Build agent finished without pushing
  after 4 attempts (1 initial + 3 auto-retries). Manual intervention required."
  Attempt branches (`opencode/issue68-20260818001215`,
  `opencode/issue68-20260818021307`, ...) all empty on the remote.
- All attempts ran deepseek-v4-flash-free (owner's pin) and did real diagnostics
  (release builds, Kodak downloads, gain experiments, PPM interleaved-raster fix)
  but never committed. Root cause is commit discipline / task scoping on long
  open-ended optimization, not a billing error.
- **Factory round dispatched (this run) on #68** to harden the loop: enforce
  incremental commit/push discipline for long builds, review build-model fit.
  Build loop stays paused until the factory PR lands.

## In flight

- **Factory round (opencode/issue68)**: triggered this run; the Factory Engineer
  will open its own infra issue/PR for the build-loop hardening.
- No opencode build/review/test runs in flight (auto-retry-3 failed at
  03:13:16Z; this maintainer run is the only active run). No open PRs.

## Issues

- **#68 (Obsidian umbrella)** - CLOSED; /oc build + /oc factory trigger target.
- **#77 (checklist 10)** - CLOSED via PR #78.
- **#70 (Lab Health)** - Auditor owns the daily summary on its schedule (ran
  01:40Z today, success).
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.

## Factory rounds

- **M1 build-loop hardening (ACTIVE)**: commit discipline for long optimization
  builds + build-model review. Dispatched this run on #68.
- **Fix-trigger guard relaxation (still queued)**: opencode.yml fix job requires
  an EXACT `/oc fix`; the Reviewer/Tester's findings comments don't match. May
  be bundled into the active factory round; otherwise dispatch after it lands
  when no opencode run is in flight.

## Reviewer/Tester/model status

- **Model config (owner's pin):** opencode.json `model:
  opencode/deepseek-v4-flash-free`, `small_model: opencode/mimo-v2.5-free`.
  Reviewer/test/factory jobs on mimo-v2.5-free; all agent steps 60m. No
  CreditsError expected.

## Next steps

1. **Shepherd the factory round** on #68: build-loop hardening (incremental
   commit discipline + build-model review). When its PR opens: review -> test ->
   merge (infra PR, no shipping cap).
2. **After the factory fix lands**, resume M1: `/oc build this` on #68 with the
   hardened loop; watch for the first `builder:` push on a
   `opencode/issue68-*` branch.
3. **M2/M3 after M1**: self-correcting weighted predictor, then
   squeeze/interlacing or improved context model - drive toward JPEG XL (8.71).
4. **Fix-trigger guard**: dispatch or bundle once the build-loop round lands.
5. **#70**: Auditor owns the daily health summary; watch for anomalies.
6. **#42**: no board picks until Obsidian resolves (owner's freeze).
7. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the factory round land a hardening PR, and does a hardened M1 then
  produce real builder: commits?
- Is deepseek-v4-flash-free actually the wrong build model for a sustained
  60-minute engineering session (vs. a scoping/commit-discipline problem)?
- How far does M1 move Obsidian's Kodak mean bpp (27.82) toward/under WebP
  (9.61) and optipng PNG (13.05)?