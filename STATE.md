# STATE - Random factory checkpoint

- **Updated:** 2026-08-17 (~11:47Z event run 32026655048, triggered by the
  Auditor's issue #75). The owner has taken over the unblock: commit `ae5160b`
  squashed the entire repo into one commit and pinned `opencode.json` with
  `model: opencode/deepseek-v4-flash-free` + `small_model: opencode/mimo-v2.5-free`
  (the real root-cause fix for the CreditsError - the action's small/title run
  no longer resolves to the paid default). PR #69 was closed unmerged; issue
  #75 was closed by the owner as resolved. **This run re-dispatches the
  Obsidian continue (issue #68)** so the Builder rebuilds the branch on the new
  main and resumes the codec.

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec (Kodak-benchmarked,
  vs JPEG XL / WebP).** OPEN, still the priority project. The codec source
  exists on remote branch `opencode/issue68-20260816082105` at head `05a9f4ab`
  (encoder.rs, decoder.rs, rans.rs, etc. - Builder was mid-fix on failing
  tests when PR #69 was closed). The owner's squash rewrote main's history, so
  this branch is now unrelated to main; the builder prompt on main carries the
  explicit rebuild guidance (checkout -B onto origin/main + cherry-pick own
  commits when merge-base fails). **This run: /oc continue dispatched on #68.**

## In flight

- **Issue #68 (Obsidian) - CONTINUE DISPATCHED this run.** Builder should
  fetch the existing branch, rebuild onto new main, resume effort, push a fresh
  PR. Watch for a push and a new PR past the closed #69. On push: auto-reviewer
  runs -> shepherd review -> test -> merge (new-project PR, cap 0/2 today,
  merge legal on approval).
- **PR #69 - CLOSED unmerged by the owner** (11:43Z). Head/branch preserved;
  no lost work.

## Issues

- **#75 (audit: Obsidian billing-blocked) - CLOSED by the owner** as resolved
  via the `opencode.json` small_model pin (no payment method needed). Nothing
  further to action.
- **#74 (billing CreditsError) - closed by the owner** previously; root cause
  now fixed at config layer.
- **#72/#73 (build-verify / review crash) - fixed by the owner's `ae5160b`
  rewrite** (build baseline capture, unrelated-histories guidance, non-PR
  guard). Closed.
- **#70 (Lab Health)**: Auditor owns the daily summary on its schedule.
- **#42 (Brainstorm board)**: frozen until Obsidian resolves.

## Reviewer/Tester/model status

- **Model config (owner's pin, supersedes my earlier workflow switch):**
  opencode.json `model: deepseek-v4-flash-free`, `small_model: mimo-v2.5-free`.
  Workflows still pin per-job models (build/fix/general/maintainer/auditor/
  ideate on deepseek-v4-flash-free; reviewer/test/factory on mimo-v2.5-free).
  The small/title resolution to paid gpt-5.4-nano is eliminated - no more
  CreditsError class of failures expected.

## Next steps

1. **Watch issue #68**: the continue build should rebuild the branch on the new
   main, resume the codec, and push a fresh PR. Shepherd review -> test ->
   merge (cap 0/2 today).
2. If the continue still cannot produce source, check run logs for any new
   model-resolution errors before re-triggering (the pin should have fixed the
   class).
3. **#70**: Auditor owns the daily health summary; watch for anomalies.
4. No board picks until Obsidian resolves (owner's freeze).
5. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the Builder's continue find the unrelated-history branch and rebuild it
  cleanly onto the squashed main?
- Does the Obsidian codec (mid-fix, failing tests) land on a fresh PR and pass
  review/test this time?