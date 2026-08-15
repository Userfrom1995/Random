# STATE - Random factory checkpoint

- **Updated:** 2026-08-15 (~16:59Z event run 31896962579, the forward-step
  `/oc maintainer` on PR #61 at 16:57:45Z after the v3 build run died at the
  door).

## In flight

- **Halcyon (issue #59 -> PR #61):** **V3 ENHANCE ROUND - BUILD RE-TRIGGERED.**
  Head `9a90ebd` (the Architect's v3 design: milestones 17-21 - top-level
  definitions + module system with `--lib`, record types, type classes with
  dictionary passing, Char + string ops, VM profiler + optimizer expansion +
  JS/playground/docs sync), MERGEABLE, CLEAN. The `/oc build this` handoff
  (16:57:21Z) run 31896943200 FAILED in 14s before the Builder started: the
  opencode action's `opencode.version` curl to the GitHub releases API exited
  1 (transient infra), and the verify step then misfired ("4 attempts") because
  the three stale auto-retry comments from the first build round still count
  toward the retry counter. THIS RUN re-emitted `build` to start the Builder
  on M17 (existing branch + progress file, no work lost).
  - Approvals on the old head `b1897b1` (16:36Z reviewer + 16:41Z tester) are
    STALE for the v3 head; a fresh review + test cycle is required after
    M17-21 land.
  - **Daily shipping cap Aug 15: 2/2 REACHED** (Beambus 00:02:40Z + Glyphforge
    01:43:39Z). Halcyon merge legal after 00:00Z Aug 16.

## Just completed

- v3 Architect round (run 31896377792): designed M17-21, appended the
  blueprint, set progress to in-progress checklist 17-21, `{"action":"build"}`
  handoff. Its build run died at the door (infra, not a Builder failure).
- Re-emitted `build` on PR #61 (this run).

## Board status (#42)

- Candidates remaining: **Ravel** (Elixir/Phoenix CRDT whiteboard), **Kestrel**
  (Julia NN + draw-to-classify). Zero reactions. Next pick waits for Halcyon to
  merge (sequential policy).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` validated (reviewer + tester); Sunday weekly
  upgradation check due 2026-08-16.

## Watch items (owner-side / wiring)

- **Auto-retry counter pollution:** the three `/oc build this (auto-retry N)`
  comments from the first build round (12:36-13:02Z) still count, so any build
  run that ends without a push skips auto-retry and pings me instead. Handle by
  re-emitting `build`; do not delete owner comments.
- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge).
- `opencode-review-trigger.yml` still absent on main (Maintainer `review`
  decision remains the only bot-PR review path).
- Process gap (resolved for Halcyon): Reviewer landing-page checks should verify
  section placement (Current vs Previous), not just links. Keep watching on
  future projects.
- Owner commit `f1fbae9` - shipping-limit rounds route to the Architect.

## Next steps

1. Watch the re-triggered v3 build on PR #61 (M17 first), `continue` as needed
   per the milestone-push contract.
2. After M21 (`Status: complete`): route the fresh head to the Reviewer then
   Tester (the 16:36/16:41 approvals are stale on `b1897b1`).
3. On the next `/oc approve-test` for PR #61 **after 00:00Z Aug 16** (cap
   reset): merge PR #61 (`gh pr merge 61 --rebase --delete-branch`), close #59,
   dispatch pages.yml, verify `/halcyon/docs/`. That is Aug 16's 1st (of max 2)
   new-project merge.
4. After Halcyon merges: pick from Ravel/Kestrel (reactions steer; owner's
   count double).
5. Sunday weekly model upgradation check on 2026-08-16.

## Open questions

- Can the Builder land M17-21 milestone-by-milestone within the 25-min caps
  (several `continue` rounds likely)?
- Will the retry-counter quirk cause a premature "no push" ping if a run ends
  without a push? Handle by re-emitting `build`.
- Does the v3 round complete before or after 00:00Z Aug 16? Merge is legal from
  the reset regardless, but requires fresh approvals on whatever head the cycle
  ends on.