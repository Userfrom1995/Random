# STATE - Random factory checkpoint

- **Updated:** 2026-08-17 (~23:52Z event run 32082224130, PR #78 created by the
  Builder at 23:51:35Z for checklist 10). The Builder LANDED the Obsidian
  benchmark harness + reference baseline + first Kodak row on PR #78 (head
  `e91d902a`, MERGEABLE/CLEAN). The owner posted `/oc review` at 23:51:46Z ->
  opencode-review run 32082213271 is IN_PROGRESS. No duplicate dispatch made.

## Priority project (the fundamental goal)

- **Issue #77 Obsidian checklist 10 (benchmark harness + reference baseline +
  first Kodak row).** OPEN, PR #78 references `Closes #77`. PR #78 adds:
  `obsidian/benchmarks/run_kodak.sh`, `fuzz_gate.sh`, `aggregate.py`,
  `build_toolchain.sh` + `toolchain.md`, pinned Kodak manifest
  (`data/kodak.sha256`, PCD0992 24x 768x512 P6 PPM), result CSV
  (2026-08-17-v1.csv, 7 codecs x 24 images, 168 fidelity-gated rows),
  reference-baseline CSV, README, docs/progress/ideas updates.
  Progress file checklist: item 10 now `[x]`.
- **First Obsidian Kodak row: 27.8226 mean bpp (effort 4)**, bit-exact through
  the gate but not competitive. Reference figures land within ~0.5% of the
  independent WangXuan95 2024 benchmark on the same corpus (harness is honest).
  M1-M3 (beat WebP/PNG -> approach/match JPEG XL) are the next milestones.
- The owner's standing directive (20:42:32Z): test BOTH losslessness and
  performance on the Kodak dataset, keep iterating until Obsidian beats the
  other codecs. Codec core (checklist 1-9) shipped on main via PR #76 (46 lib
  tests green).

## In flight

- **Review on PR #78** (run 32082213271, owner's `/oc review` 23:51:46Z) -
  IN_PROGRESS. Shepherding review -> test -> merge. A duplicate opencode-review
  run 32082224144 spawned by the preview comment sits `pending` with zero jobs
  (job guard self-skips).
- **pages.yml**: run 32082202250 (pull_request) deployed the PR preview
  (preview/pr-78 live); a workflow_dispatch run 32082225006 completed/success
  on main.

## Issues

- **#77 (Obsidian checklist 10)** - OPEN; PR #78 closes it on merge.
- **#70 (Lab Health)** - Auditor owns the daily summary on its schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.
- **Factory round QUEUED (do NOT run concurrent with a build/review/test):**
  the build-verify baseline false positive (#72 BUILD-job gap) plus the
  fix-trigger guard relaxation (opencode.yml fix job requires an EXACT
  `/oc fix`; the Reviewer/Tester's findings comments don't match). Dispatch
  `factory` once no opencode build/review/test is in flight.

## Reviewer/Tester/model status

- **Model config (owner's pin):** opencode.json `model:
  opencode/deepseek-v4-flash-free`, `small_model: opencode/mimo-v2.5-free`.
  Reviewer/test/factory jobs on mimo-v2.5-free; all agent steps 60m. No
  CreditsError expected.
- **Reviewer/Tester gates** all passed on PR #76 (round 5 approve ->
  approve-test -> merged).

## Next steps

1. **Watch PR #78** for the reviewer's decision. On `/oc approve`: review
   workflow auto-dispatches the Tester (losslessness AND Kodak performance per
   owner's directive). On `/oc approve-test`: merge
   (`gh pr merge 78 --rebase --delete-branch`), close #77, verify pages.yml,
   then route `factory` for the verify-baseline bug (safe then).
2. **On `/oc fix`**: the Fixer applies findings; re-dispatch `review` after the
   fix push (opencode-review fires on `/oc review`).
3. **Kodak iteration (M1-M3)**: once the first Obsidian Kodak row is recorded,
   drive predictor/context improvements to beat WebP/PNG (M1), then close in on
   JPEG XL (M2/M3). Owner's directive: keep iterating until Obsidian wins.
4. **Route `factory`** for the build-verify baseline false positive +
   fix-trigger guard relaxation - only when no opencode build/review/test is in
   flight.
5. **#70**: Auditor owns the daily health summary; watch for anomalies.
6. **#42**: no board picks until Obsidian resolves (owner's freeze).
7. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Reviewer on PR #78: approve or fix? (Harness design: are the reference
  figures and fidelity gate sound?)
- Does the Tester's round cover losslessness AND Kodak performance (owner's
  directive) and pass on head `e91d902a`?
- How close is Obsidian's first Kodak row to WebP/PNG and JPEG XL (M1-M3 gap)?
- Factory round timing: dispatch as soon as no opencode workflow is in flight.