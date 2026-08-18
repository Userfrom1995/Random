# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~05:12Z, `/oc maintainer` event run on PR #80, run
  32101948167). PR #80 is APPROVED by the Reviewer and the Tester is IN FLIGHT.
  Gate held; no new trigger posted this run.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP,
  Kodak-benchmarked).** REOPENED (the factory round PR #79 auto-closed it on
  merge; the umbrella must stay open for M1-M3). Main build trigger target.
- **Checklist 10 shipped on main** (first Obsidian Kodak row: 27.8226 mean bpp,
  bit-exact). Reference baseline within ~0.5% of WangXuan95 2024 (JXL 8.7062, WebP
  9.6130, JLS 9.7113, J2K 9.5762, PNG ~13.05).
- Owner's standing directive: iterate until Obsidian beats the other codecs on
  Kodak (lossless + performance). M1-M3 are the optimization milestones.

## M1 build loop - APPROVED, IN TEST (PR #80)

- **PR #80 OPEN** by The Builder: branch `opencode/issue68-20260818034514`, head
  `967ba1b3a660f04c98de3dbeb08da509cbdddabe` (Fixer's final commit; the head moved
  past `e2a5119b` documented in earlier STATE snapshots after further fixer
  commits). Commits: `e858ea00` (broken milestone) -> `584a5565` (Builder lockstep
  fix) -> Fixer commits -> `967ba1b3`. `mergeable: MERGEABLE` /
  `mergeStateStatus: CLEAN`. `Closes #68` in body.
- **Reviewer APPROVED (run 32101635901, 05:10:51Z).** All three findings resolved:
  - Finding 1 (BLOCKING): `adapt` constant-`M` "steal from richest" scheme restored,
    recovering flat-image compression efficiency (the `large_flat_compresses` /
    `decode_accepts_large_flat_stream` failures were REGRESSIONS, not pre-existing).
  - Finding 2 (doc): module doc says `sum(freq) == M`.
  - Finding 3 (tests): `encoder_invariant_window`, `normalize_exact_sum`,
    `decoder_errors_on_truncation` restored. 47 tests pass.
- **Tester IN FLIGHT.** Owner's `/oc test` (05:10:54Z) -> opencode-test run
  **32101889905 IN_PROGRESS**. A redundant duplicate opencode-test run 32101948150
  is PENDING (spawned by this `/oc maintainer` event batch at 05:11:53Z; serializes
  behind the first). Mae posted NO `/oc test` (avoid duplicate trigger while a test
  is in flight).

## Factory round - COMPLETE (PR #79 merged at 03:42Z)

- Builder prompt hardened; `opencode.json` model -> hy3-free. Both applied to main.
- Workflow YAML model switch (hy3-free) already on origin/main. No CreditsError expected.

## In flight

- **M1 test (PR #80)** - the driver. opencode-test run **32101889905** IN_PROGRESS
  on head `967ba1b3`; redundant 32101948150 PENDING. No build/review in flight.
- **This maintainer run:** 32101948167 (in_progress, `/oc maintainer` on PR #80).

## Issues

- **#68 (Obsidian umbrella)** - REOPENED; M1 addressed by PR #80 (in test).
- **#77 (checklist 10)** - CLOSED via PR #78.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.
- **#72 (build-verify guard gap)** - CLOSED by owner's baseline fix; the
  fix-trigger-guard relaxation remains a QUEUED factory item.

## Factory rounds

- **M1 build-loop hardening** - DONE (PR #79 merged at 03:42Z).
- **Fix-trigger guard relaxation (QUEUED)**: Reviewer/Tester findings comments
  don't match opencode.yml's exact `/oc fix` trigger. NOT dispatched (a test is in
  flight on PR #80). Dispatch in the next idle window (after PR #80 merges and no
  opencode build/review/test is in flight).

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model:
  opencode/mimo-v2.5-free`. All workflow `.yml` agent steps pinned to `opencode/hy3-free`.
  Reviewer/test/factory on mimo-v2.5-free. No CreditsError expected.

## Next steps

1. **Watch test run 32101889905 on head `967ba1b3`.** On `/oc approve-test`:
   merge (`gh pr merge 80 --rebase --delete-branch`), close #68, verify `pages.yml`
   ran. Obsidian continuation, no shipping cap concern.
2. **After merge:** route `factory` for the fix-trigger-guard relaxation (safe then
   - no build/review/test in flight). Then continue M1 (self-correcting weighted
   predictor / context tuning toward WebP 9.61 / optipng PNG 13.05) and M2/M3.
3. **Polish (non-blocking):** PR #80 body still opens with "decode still desyncs"
   text - stale since the fix landed; the Fixer/Builder can refresh on next touch.

## Open questions

- Does the Tester pass on head `967ba1b3` (losslessness + Kodak performance per
  owner directive)? It should - 47 tests green and the prior Tester round on the
  same fix lineage already exercised round-trips + fuzz.
- After merge: how far does M1 move Obsidian's Kodak mean bpp (27.82) toward/under
  WebP (9.61) and optipng PNG (13.05)?
