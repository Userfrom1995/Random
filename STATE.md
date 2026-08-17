# STATE - Random factory checkpoint

- **Updated:** 2026-08-17 (~22:08Z event run 32074608848, owner `/oc maintainer`
  on PR #76 at 22:08:18Z, right after the Tester's `/oc approve-test`). PR #76
  (Obsidian codec core, checklist 1-9) is **MERGED** (`324da65d`, 22:09:09Z),
  issue **#68 auto-closed**, pages.yml re-deployed on the merged head. The
  Builder is now dispatched for **checklist 10** (Kodak benchmark harness +
  first Obsidian Kodak row) per the owner's directive.

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec (Kodak-benchmarked,
  vs JPEG XL / WebP).** CLOSED (auto-close on PR #76 merge) for the codec core.
  The priority project CONTINUES via a new Builder issue: checklist 10 (benchmark
  harness: `run_kodak.sh`, `fuzz_gate.sh`, `aggregate.py`, `toolchain.md`,
  reference baseline + first Obsidian Kodak row), then M1-M3 (beat WebP/PNG,
  close in on JPEG XL). The owner's standing directive (20:42:32Z): test BOTH
  losslessness and performance on the Kodak dataset, keep iterating until
  Obsidian beats the other codecs on Kodak. Codec shipped: 46 lib tests green,
  bit-exact round trips efforts 0-7, corruption rejection with dimension caps.

## In flight

- **Checklist 10 build (dispatched this run).** `build` on issue #68 posts
  `/oc build this` as the owner; the Builder opens its own new issue for the
  benchmark-harness task and a fresh PR. Watch for the new issue + branch, then
  shepherd build -> review -> test -> merge.
- **pages.yml**: run 32074760993 completed/success on merged head `324da65d`
  (22:10:18Z) - production site serves the Obsidian landing card.

## Issues

- **#68 (Obsidian)** - CLOSED for the codec core; continues via a new Builder
  issue for checklist 10 (Kodak benchmark harness).
- **#70 (Lab Health)** - Auditor owns the daily summary on its schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.
- **Factory round QUEUED (do NOT run concurrent with a build):** the
  build-verify baseline false positive (#72 BUILD-job gap) plus the fix-trigger
  guard relaxation (opencode.yml fix job requires an EXACT `/oc fix`; the
  Reviewer/Tester's findings comments don't match). Dispatch `factory` once no
  opencode build/review/test is in flight.

## Reviewer/Tester/model status

- **Model config (owner's pin):** opencode.json `model:
  opencode/deepseek-v4-flash-free`, `small_model: opencode/mimo-v2.5-free`.
  Reviewer/test/factory jobs on mimo-v2.5-free; all agent steps 60m. No
  CreditsError expected.
- **Reviewer/Tester gates** all passed on PR #76 (round 5 approve -> approve-test).

## Next steps

1. **Checklist 10 build (in flight)**: shepherd the new Builder issue + PR through
   review -> test -> merge. The Tester's rounds must cover losslessness AND Kodak
   performance (owner's directive).
2. **Kodak iteration (M1-M3)**: once the first Obsidian Kodak row exists, drive
   the predictor/context improvements to beat WebP/PNG (M1), then close in on
   JPEG XL (M2/M3).
3. **Route `factory`** for the build-verify baseline false positive + fix-trigger
   guard relaxation - safe once the checklist-10 build is no longer in flight.
4. **#70**: Auditor owns the daily health summary; watch for anomalies.
5. **#42**: no board picks until Obsidian resolves (owner's freeze).
6. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Will the checklist-10 build land the benchmark harness and the first Obsidian
  Kodak row cleanly?
- How close is Obsidian's first Kodak row to WebP/PNG and JPEG XL (M1-M3 gap)?
- Factory round timing: dispatch as soon as no opencode workflow is in flight.