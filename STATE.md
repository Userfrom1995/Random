# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~05:07Z, `/oc maintainer` event run on PR #80, run
  32101656855). The Fixer resolved the BLOCKING review finding (commit `e2a5119b`,
  restores constant-`M` "steal from rich" `adapt`); review is in flight (run
  32101666490). Mae held the gate, NO new trigger.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP,
  Kodak-benchmarked).** REOPENED (the factory round PR #79 auto-closed it on
  merge; the umbrella must stay open for M1-M3). Main build trigger target.
- **Checklist 10 shipped on main** (first Obsidian Kodak row: 27.8226 mean bpp,
  bit-exact). Reference baseline within ~0.5% of WangXuan95 2024 (JXL 8.7062, WebP
  9.6130, JLS 9.7113, J2K 9.5762, PNG ~13.05).
- Owner's standing directive: iterate until Obsidian beats the other codecs on
  Kodak (lossless + performance). M1-M3 are the optimization milestones.

## M1 build loop - FIXED, IN REVIEW (PR #80)

- **PR #80 OPEN** by The Builder: branch `opencode/issue68-20260818034514`, head
  `e2a5119b` ("Splitting into code-fix and restored-tests commits.", Fixer). 3
  commits (+215/-277 across 4 files; current head is the Fixer's). `mergeable:
  MERGEABLE` / `mergeStateStatus: CLEAN`.
- **Reviewer Finding 1 (BLOCKING) RESOLVED.** The Fixer's commit `e2a5119b`
  restored the constant-`M` "steal from rich" `adapt` scheme (total stays exactly
  `M`, steal from the richest *other* symbol with freq >= 2, never starve below 1),
  recovering the flat-image compression efficiency the halving scheme had degraded
  (`large_flat_compresses` / `decode_accepts_large_flat_stream` were REGRESSIONS,
  not pre-existing). Finding 2 (doc comment now says `total == M`) and Finding 3
  (three dropped invariant tests `encoder_invariant_window`, `normalize_exact_sum`,
  `decoder_errors_on_truncation` restored) also fixed. The constant-`M` interval
  coding + `t >= table.total` guard (the real lockstep fix from `584a5565`) are
  preserved.
- **Review IN FLIGHT:** owner `/oc review` at 05:06:55Z -> opencode-review run
  **32101666490** PENDING on head `e2a5119b` (run 32101656869 cancelled; 32101666490
  is the active post-fix review). Mae posted NO new review (avoid duplicate
  trigger while a review is queued).

## Factory round - COMPLETE (PR #79 merged at 03:42Z)

- Builder prompt hardened; `opencode.json` model -> hy3-free. Both applied to main.
- Workflow YAML model switch (hy3-free) already on origin/main. No CreditsError expected.

## In flight

- **M1 review (PR #80)** - the driver. opencode-review run **32101666490** PENDING
  on head `e2a5119b`. No build/test in flight. No held runs.
- **This maintainer run:** 32101656855 (in_progress) + duplicate 32101666501 (pending),
  both `/oc maintainer` on PR #80.

## Issues

- **#68 (Obsidian umbrella)** - REOPENED; M1 addressed by PR #80 (in review).
- **#77 (checklist 10)** - CLOSED via PR #78.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.
- **#72 (build-verify guard gap)** - QUEUED factory round (no concurrent opencode build/review/test).

## Factory rounds

- **M1 build-loop hardening** - DONE (PR #79 merged at 03:42Z).
- **Fix-trigger guard relaxation (QUEUED)**: Reviewer/Tester findings comments don't
  match opencode.yml's exact `/oc fix` trigger. NOT dispatched (review in flight on
  PR #80). Dispatch in the next idle window (after PR #80 merges and no opencode
  build/review/test is in flight).

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model:
  opencode/mimo-v2.5-free`. All workflow `.yml` agent steps pinned to `opencode/hy3-free`.
  Reviewer/test/factory on mimo-v2.5-free. No CreditsError expected.

## Next steps

1. **Watch review run 32101666490 on head `e2a5119b`.** On `/oc approve`: the review
   workflow auto-dispatches the Tester -> on `/oc approve-test`: merge (`gh pr merge 80
   --rebase --delete-branch`), close #68, verify pages.yml ran. Obsidian continuation,
   no shipping cap concern.
2. **On a new `/oc fix`:** the Fixer applies findings on the branch; re-dispatch `review`
   after the fix push. (Likely only non-blocking polish: stale PR-body "decode still
   desyncs" text.)
3. **After PR #80 lands:** continue M1 (self-correcting weighted predictor / context
   tuning toward WebP 9.61 / optipng PNG 13.05) and M2/M3.
4. **Fix-trigger guard factory round (#72):** dispatch in the next idle window (no
   opencode build/review/test in flight).
5. **#70:** Auditor owns the daily health summary; watch for anomalies.
6. **#42:** no board picks until Obsidian resolves (owner's freeze).
7. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does review run 32101666490 APPROVE the fixed head `e2a5119b`, or return new
  findings (e.g., stale PR-body text, non-blocking only)?
- Does the Tester pass on head `e2a5119b` (losslessness + Kodak performance per directive)?
- How far does M1 move Obsidian's Kodak mean bpp (27.82) toward/under WebP (9.61) and
  optipng PNG (13.05)?
