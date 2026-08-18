# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~00:03Z event run 32082881438). PR #78 (Obsidian
  checklist 10) MERGED as `de0074d`; issue #77 CLOSED; pages re-deployed; M1
  build routed to the Builder.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP,
  Kodak-benchmarked).** CLOSED (auto-closed on the PR #76 merge); used as the
  `/oc build this` trigger target for the M1 milestone.
- **Checklist 10 shipped on main via PR #78** (merge commit `de0074d`):
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

- **M1 build ROUTED this run** (`build` on issue #68 -> `/oc build this`): the
  Builder creates its own new issue + PR for checklist 11 (beat WebP lossless
  9.61 + optipng PNG 13.05 on Kodak via predictor/context tuning). No
  research/architect first: spec, architecture, methodology already written.
- **No opencode build/review/test in flight** (all skipped/completed). Only this
  maintainer run.

## Issues

- **#68 (Obsidian umbrella)** - CLOSED; /oc build trigger target for M1.
- **#77 (checklist 10)** - CLOSED this run (resolved via PR #78).
- **#70 (Lab Health)** - Auditor owns the daily summary on its schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.

## Factory round (queued)

- Fix-trigger guard relaxation: opencode.yml fix job requires an EXACT `/oc
  fix`; the Reviewer/Tester's findings comments don't match. The build-verify
  baseline false positive was already closed by the owner's fix. Dispatch
  `factory` once the M1 build/review/test cycle is NOT in flight.

## Reviewer/Tester/model status

- **Model config (owner's pin):** opencode.json `model:
  opencode/deepseek-v4-flash-free`, `small_model: opencode/mimo-v2.5-free`.
  Reviewer/test/factory jobs on mimo-v2.5-free; all agent steps 60m. No
  CreditsError expected.
- **Reviewer/Tester gates** passed on PR #78 (round 1 fix x3 -> round 2 approve
  -> approve-test) and the PR merged.

## Next steps

1. **Shepherd the M1 build** (new issue + PR from the Builder on `/oc build
   this` posted on #68): review -> test -> merge.
2. **M2/M3 after M1**: self-correcting weighted predictor, then
   squeeze/interlacing or improved context model - drive toward JPEG XL (8.71).
3. **Factory round** (fix-trigger guard): dispatch when no opencode
   build/review/test is in flight.
4. **#70**: Auditor owns the daily health summary; watch for anomalies.
5. **#42**: no board picks until Obsidian resolves (owner's freeze).
6. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- How far does M1 move Obsidian's Kodak mean bpp (27.82) toward/under WebP
  (9.61) and optipng PNG (13.05)?
- Factory round timing: dispatch after M1's build/review/test cycle finishes.