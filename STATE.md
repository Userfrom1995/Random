# STATE - Random factory checkpoint

- **Updated:** 2026-08-17 (~08:45Z event run 32011787697, PR #69 /oc
  maintainer forward from the failed 08:30Z build). This run **landed the
  model switch on main** (all remaining `deepseek-v4-flash-free` pins ->
  `opencode/mimo-v2.5-free`), **re-dispatched the Obsidian continue**, and
  **closed #73**. The Obsidian billing stall's root cause (small/title model
  resolving to PAID `gpt-5.4-nano` at session start against a workspace with
  no payment method) is addressed by moving every lab job to the empirically
  proven free model `mimo-v2.5-free`.

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec (Kodak-benchmarked,
  vs JPEG XL / WebP).** PR #69 open, head `2377f3cc` (research/spec/
  architecture docs + empty Cargo scaffold, NO codec source). Billing
  `CreditsError` blocked every build since ~15:18Z Aug 16. **This run: model
  switched to mimo-v2.5-free on main and the continue trigger is dispatched
  on PR #69** - the Builder resumes effort 0 with the new model and pushes.

## In flight

- **PR #69 (Obsidian) - CONTINUE DISPATCHED this run** (post-model-switch).
  Watch the branch `opencode/issue68-20260816082105` for a push past
  `2377f3cc`. On push: auto-reviewer runs -> shepherd review -> test ->
  merge (new-project PR, cap 0/2 today, merge legal on approval).
- **Issue #73 (opencode-review crash on non-PR) - CLOSED this run.** Fix
  verified on main (`3ea8390`: opencode-review.yml line 13 now guards
  `issue.pull_request != null`).
- **Issue #72 (build-verify false positive) - OPEN, half-fixed.** The FIX
  job got a baseline head capture (line 508), but the BUILD job verify (line
  330) still compares local HEAD vs remote branch SHA and false-positives on
  an unchanged head. Not a silent stall (no-decision builds still forward
  /oc maintainer), but the auto-retry is skipped. Needs a factory round
  (after Obsidian moves) or the owner's patch.
- **Issue #75 (audit: Obsidian billing-blocked) - OPEN, actioned this run.**
  Model switch landed + continue dispatched. Close once the build verifiably
  pushes codec source.
- **Issue #70 (Lab Health)**: Auditor owns the daily summary on its schedule.
- **Issue #68** (Obsidian project), **#42** (Brainstorm board, frozen until
  Obsidian resolves).

## Reviewer/Tester/model status

- **All workflows now on `opencode/mimo-v2.5-free`**: reviewer/test/factory
  already were; opencode.yml (5 jobs), maintainer.yml, auditor.yml, ideate.yml
  switched this run and landed on main via the maintainer PAT workflow-push
  step. No `deepseek-v4-flash-free` pins remain.

## Next steps

1. **Watch PR #69**: the continue build should push real codec source. If it
   pushes: shepherd review -> test -> merge (cap 0/2 today). If it STILL only
   orients: the small-model billing error is model-independent -> tag the
   owner (add a payment method or harden the action input), stop blind
   re-triggers.
2. **#72**: route the remaining BUILD-job verify gap to a factory round once
   no opencode build is in flight.
3. **#75**: close once the Obsidian build verifiably pushes.
4. **#70**: Auditor owns the daily health summary; watch for anomalies.
5. No board picks until Obsidian resolves (owner's freeze).
6. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the Obsidian continue push real codec source on `mimo-v2.5-free`, or
  does the paid-default small-model CreditsError follow the new model too?
- Who closes #72's BUILD-job verify gap - a factory round or the owner's
  patch?
- Does the owner add a payment method to the opencode.ai workspace to end the
  recurring CreditsError class of failures permanently?
