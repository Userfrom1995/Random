# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~04:49Z, `/oc maintainer` event run on PR #80, run
  32100484981). The resumed M1 build FIXED the adaptive rANS lockstep (head
  `584a556`); review is already in flight (run 32100476833, owner's `/oc review`
  + run 32100484990, Builder's auto-forward). NO new trigger posted by Mae.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP,
  Kodak-benchmarked).** REOPENED earlier today (the factory round PR #79 auto-closed
  it on merge; the umbrella must stay open for M1-M3). Main build trigger target.
- **Checklist 10 shipped on main** (first Obsidian Kodak row: 27.8226 mean bpp,
  bit-exact). Reference baseline within ~0.5% of WangXuan95 2024 (JXL 8.7062, WebP
  9.6130, JLS 9.7113, J2K 9.5762, PNG ~13.05).
- Owner's standing directive: iterate until Obsidian beats the other codecs on
  Kodak (lossless + performance). M1-M3 are the optimization milestones.

## M1 build loop - FIXED, IN REVIEW (PR #80)

- **PR #80 OPEN** by The Builder: branch `opencode/issue68-20260818034514`, head
  `584a556566eb62bd3fbe361898019a852a51dfa1` ("builder: fix adaptive rANS lockstep
  desync (constant-M interval + renorm bound)", pushed 04:47:54Z). 2 commits,
  +179/-332 across 4 files. `mergeable: MERGEABLE` / `mergeStateStatus: CLEAN`.
- **Lockstep FIXED.** Root cause: the variable running `total` was mixed with the
  decoder's fixed renorm bound `RNB`, breaking the rANS bijection `(x%f)+c < D`. Fix:
  both the interval-coding step and renorm upper bound in `put_fc` use constant `M`;
  decoder divides/mods by `M`; `adapt` halves at `total > M` (keeps `total <= M`); a
  `t >= table.total` guard returns `InvalidStream` instead of tripping `find`'s
  `debug_assert`. All 5 `rans` tests pass + `corruption_rejected`. The 2 remaining
  failures (`large_flat_compresses`, `decode_accepts_large_flat_stream`) are
  pre-existing compression-efficiency issues, out of scope for #68.
- **Review IN FLIGHT:** owner `/oc review` at 04:48:11Z -> run **32100476833**
  IN_PROGRESS (review job `95599861374`). Builder's decision file also forwarded
  `/oc review` at 04:48:23Z -> run **32100484990** PENDING (same head; redundant).
  Mae posted NO new review (avoid duplicate trigger).

## Factory round - COMPLETE (PR #79 merged at 03:42Z)

- Builder prompt hardened (`ALWAYS UPDATE PROGRESS FILE BEFORE PUSH` +
  `MILESTONE COMMITMENT`); `opencode.json` model -> hy3-free. Both applied to main.
- Workflow YAML model switch (hy3-free) already on origin/main. No CreditsError expected.

## In flight

- **M1 review (PR #80)** - the driver. Runs 32100476833 (in_progress) + 32100484990
  (pending, redundant) reviewing head `584a556`. No build/test in flight. No held runs.
- **This maintainer run:** 32100484981 (pending/executing), `/oc maintainer` on PR #80.

## Issues

- **#68 (Obsidian umbrella)** - REOPENED; M1 addressed by PR #80 (in review).
- **#77 (checklist 10)** - CLOSED via PR #78.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.

## Factory rounds

- **M1 build-loop hardening** - DONE (PR #79 merged at 03:42Z).
- **Fix-trigger guard relaxation (QUEUED)**: Reviewer/Tester findings comments don't
  match opencode.yml's exact `/oc fix` trigger. NOT dispatched (no-concurrent-factory
  rule: a review is in flight on PR #80). Dispatch in the next idle window (after PR
  #80 merges and no opencode build/review/test is in flight).

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model:
  opencode/mimo-v2.5-free`. All workflow `.yml` agent steps pinned to `opencode/hy3-free`.
  Reviewer/test/factory on mimo-v2.5-free. No CreditsError expected.

## Next steps

1. **Watch the review on PR #80 (run 32100476833) on head `584a556`.** On `/oc approve`:
   the review workflow auto-dispatches the Tester -> on `/oc approve-test`: merge
   (`gh pr merge 80 --rebase --delete-branch`), close #68, verify pages.yml ran.
   Obsidian continuation, no shipping cap concern.
2. **On `/oc fix`:** the Fixer applies findings on the branch; re-dispatch `review` after
   the fix push. Likely quick doc fixes (stale PR-body "decode still desyncs" text,
   progress-file branch drift).
3. **After PR #80 lands:** continue M1 (self-correcting weighted predictor / context
   tuning toward WebP 9.61 / optipng PNG 13.05) and M2/M3.
4. **Fix-trigger guard factory round:** dispatch in the next idle window (no opencode
   build/review/test in flight).
5. **#70:** Auditor owns the daily health summary; watch for anomalies.
6. **#42:** no board picks until Obsidian resolves (owner's freeze).
7. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the in-flight review (run 32100476833) approve the fixed head `584a556`, or
  return `/oc fix` findings (stale PR-body text / progress-file drift)?
- Does the Tester pass on head `584a556` (losslessness + Kodak performance per directive)?
- How far does M1 move Obsidian's Kodak mean bpp (27.82) toward/under WebP (9.61) and
  optipng PNG (13.05)?
