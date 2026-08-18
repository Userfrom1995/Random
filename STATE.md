# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~01:35Z schedule run 32088693363). M1 build attempt
  1 (run 32083566693) was diagnostic-only and pushed nothing; auto-retry 2
  (run 32087378098) in flight; no PRs open.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP,
  Kodak-benchmarked).** CLOSED (auto-closed on the PR #76 merge); used as the
  `/oc build this` trigger target for the M1 milestone.
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

## In flight

- **M1 build attempt 2 RUNNING (run 32087378098)**, triggered by the
  auto-retry-2 comment on #68 at 01:12:23Z. Branch
  `opencode/issue68-20260818001215` has NO commits on the remote yet.
- **M1 attempt 1 (run 32083566693) pushed nothing**: 60m of real diagnostics
  (release build, Kodak downloads, diag/gain experiments, PPM interleaved-raster
  parse fix in ppm.rs) but no `builder:` commit. The verify step correctly
  detected the no-push (baseline fix from `ae5160b` works) and auto-retried.
- No opencode build/review/test runs beyond the M1 build; no PRs open.

## Issues

- **#68 (Obsidian umbrella)** - CLOSED; /oc build trigger target for M1.
- **#77 (checklist 10)** - CLOSED via PR #78.
- **#70 (Lab Health)** - Auditor owns the daily summary on its schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.

## Factory round (queued)

- **Fix-trigger guard relaxation**: opencode.yml fix job requires an EXACT `/oc
  fix`; the Reviewer/Tester's findings comments don't match. Dispatch `factory`
  only when no opencode build/review/test is in flight (a build is running
  now - do NOT dispatch concurrently). The build-verify baseline gap (#72) is
  CONFIRMED FIXED by `ae5160b` - no round needed for that one.

## Reviewer/Tester/model status

- **Model config (owner's pin):** opencode.json `model:
  opencode/deepseek-v4-flash-free`, `small_model: opencode/mimo-v2.5-free`.
  Reviewer/test/factory jobs on mimo-v2.5-free; all agent steps 60m. No
  CreditsError expected.

## Next steps

1. **Watch run 32087378098 + the `opencode/issue68-20260818001215` branch** for
   the first `builder:` commit. On push: PR opens, auto-reviewer runs; shepherd
   review -> test -> merge (Obsidian continuation, no shipping cap).
2. **If attempt 2 (or 3) also ends with no push**: route `factory`/General to
   fix the build model's commit discipline on the long M1 optimization - do NOT
   keep re-dispatching blindly.
3. **M2/M3 after M1**: self-correcting weighted predictor, then
   squeeze/interlacing or improved context model - drive toward JPEG XL (8.71).
4. **Factory round** (fix-trigger guard): dispatch when no opencode
   build/review/test is in flight.
5. **#70**: Auditor owns the daily health summary; watch for anomalies.
6. **#42**: no board picks until Obsidian resolves (owner's freeze).
7. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does M1 attempt 2 land a real commit + PR, or recon-only again?
- Is deepseek-v4-flash-free underperforming on the open-ended M1 optimization
  (60-min diagnostic session with zero commits)?
- How far does M1 move Obsidian's Kodak mean bpp (27.82) toward/under WebP
  (9.61) and optipng PNG (13.05)?
