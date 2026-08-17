# STATE - Random factory checkpoint

- **Updated:** 2026-08-17 (~18:48Z schedule run 32056592991). PR #76's Obsidian
  build is ACTIVE: the owner issued `/oc continue` at 18:40:55Z and the opencode
  build run 32056096450 is in progress right now. This run made NO triggers to
  avoid double-dispatching. The only open work is watching that build finish.

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec (Kodak-benchmarked,
  vs JPEG XL / WebP).** OPEN, still the priority project. Research + spec +
  architecture are committed on PR #76; the Builder is mid-debug on the rANS
  core (commit `24bf6d4e` "Debugging rANS; will rewrite rans.rs" at 13:56:40Z):
  adaptive lockstep + roundtrip tests fail with "rANS stream exhausted"; the
  Builder fetched the Townsend rANS reference to settle renormalization and is
  rewriting `rans.rs` right now in run 32056096450.

## In flight

- **PR #76 (Obsidian) - BUILD RUNNING (owner's /oc continue, run 32056096450,
  in_progress).** Head `24bf6d4e`, 54 files / +3940 lines. `mergeable:
  CONFLICTING` because main advanced to `86f1328` (owner's agent-timeout fix)
  after the branch was cut - expect a rebase/conflict pass once the Builder
  pushes. On push: auto-reviewer -> shepherd review -> test -> merge
  (new-project PR, cap 0/2 today, merge legal on approval).

## Issues

- **#68 (Obsidian)** - OPEN, priority project, being built on PR #76.
- **#70 (Lab Health)** - Auditor owns the daily summary on its schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.
- All billing/infra issues (#72/#73/#74/#75) closed; owner's `ae5160b` + pin
  fixed model resolution, `86f1328` fixed the silent-stall timeout.

## Reviewer/Tester/model status

- **Model config (owner's pin):** opencode.json `model:
  opencode/deepseek-v4-flash-free`, `small_model: opencode/mimo-v2.5-free`.
  Workflows pin per-job models (build/maintainer/auditor/ideate on
  deepseek-v4-flash-free; reviewer/test/factory on mimo-v2.5-free). Owner's
  `86f1328` raised all agent steps to 60m (jobs 75m), closing the silent-stall
  class of failures. No CreditsError expected.

## Next steps

1. **Watch run 32056096450 to completion** (in_progress now). On its push, PR
   #76 head moves; the auto-reviewer fires. Shepherd review -> test -> merge.
   If the build FAILS (timeout/billing/cancel-before-start), route `factory`
   per the fallback policy instead of blindly re-dispatching.
2. After the Builder pushes, watch for the conflict pass: the branch needs to
   align with main's `86f1328` workflow changes before the Reviewer approves.
3. **#70**: Auditor owns the daily health summary; watch for anomalies.
4. No board picks until Obsidian resolves (owner's freeze).
5. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the rANS rewrite land a green effort 0 end-to-end (property tests +
  roundtrips + fuzz) this push?
- Who handles the rebase onto main (`86f1328` changed workflows post-branch)?
- Will the owner merge Obsidian today (new-project cap 0/2 so far)?
- Progress file `68-obsidian-lossless-image-codec.md` still shows 15 unchecked
  milestones - confirm the Builder updates it on the next push.