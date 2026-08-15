# STATE - Random factory checkpoint

- **Updated:** 2026-08-15 (~17:24Z event run 31898196503, the owner's
  `/oc maintainer make sure doc is also properly done.` comment on PR #61).

## In flight

- **Halcyon (issue #59 -> PR #61):** **V3 ENHANCE ROUND - BUILD ACTIVE.**
  Head `9a90ebd` (the Architect's v3 design: milestones 17-21 - top-level
  definitions + module system with `--lib`, record types, type classes with
  dictionary passing, Char + string ops, VM profiler + optimizer expansion +
  JS/playground/docs sync). Build run 31897133922 (started 17:01:22Z) is
  ACTIVELY RUNNING: Builder agent step in_progress since 17:01:24Z (60-min
  agent cap), branch head STILL `9a90ebd` as of 17:33Z - Builder mid-M17,
  first v3 milestone not pushed yet. Do NOT emit duplicate triggers while it
  runs.
  - Approvals on the old head `b1897b1` (16:36Z reviewer + 16:41Z tester) are
    STALE for the v3 head; a fresh review + test cycle is required after
    M17-21 land.
  - **Daily shipping cap Aug 15: 2/2 REACHED** (Beambus 00:02:40Z + Glyphforge
    01:43:39Z). Halcyon merge legal after 00:00Z Aug 16.
  - Owner ask (17:24:04Z): "make sure doc is also properly done." Docs are
    already a hard requirement of the v3 plan (every milestone end-to-end incl.
    docs; M21 bundles docs sync). Acknowledged in comment.md with a
    verification commitment for the review/test gates.

- **Issue #62 "Fix README and website" (opened 17:28:47Z by owner):** claims
  current project on live site + README is wrong (should be Halcyon, Beambus ->
  Previous); second comment 17:30:57Z asks for a GitHub repo link in the
  top-right of the website. IMPORTANT: the placement half is ALREADY fixed on
  PR #61's branch (M16d, `20f63cfb`: Halcyon = Current Project / Live now,
  Beambus = Previous, verified on branch). The live site shows Beambus only
  because PR #61 is unmerged. The NEW ask is the repo-link on the landing page.
  - A CONCURRENT maintainer run 31898418708 (17:28:49Z) owns #62; I did not
    double-handle it. Watch that it folds the repo-link in without conflicting
    with PR #61's landing-page changes.

## Just completed

- Nothing new this run (owner comment + #62 routing noted; no triggers emitted
  because the v3 build is actively running).

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
- Issue #62 (repo-link + placement) - placement resolved by PR #61 merge; the
  repo link needs a fix routed (concurrent run 31898418708 owns it).
- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge).
- `opencode-review-trigger.yml` still absent on main (Maintainer `review`
  decision remains the only bot-PR review path).
- Process gap (resolved for Halcyon): Reviewer landing-page checks should verify
  section placement (Current vs Previous), not just links. Keep watching on
  future projects.
- Owner commit `f1fbae9` - shipping-limit rounds route to the Architect.

## Next steps

1. Watch the active v3 build on PR #61 (M17 first). When it lands milestones,
   `continue` as needed per the milestone-push contract. When it completes
   (`Status: complete`), route the fresh head to the Reviewer then Tester.
2. Watch issue #62's concurrent run (31898418708) - ensure the GitHub repo-link
   lands on the site and that #62's placement half is recognized as already on
   PR #61.
3. On the next `/oc approve-test` for PR #61 **after 00:00Z Aug 16** (cap
   reset): merge PR #61 (`gh pr merge 61 --rebase --delete-branch`), close #59
   (+ confirm #62 placement satisfied), dispatch pages.yml, verify
   `/halcyon/docs/` and the repo-link. That is Aug 16's 1st (of max 2) new-
   project merge.
4. After Halcyon merges: pick from Ravel/Kestrel (reactions steer; owner's
   count double).
5. Sunday weekly model upgradation check on 2026-08-16.

## Open questions

- When does the Builder push M17 (head still `9a90ebd` at 17:33Z)? Expect the
  milestone-push contract to deliver shortly; watch for the retry-counter ping
  if a run ends without pushing.
- Does the concurrent #62 run fold the repo-link in cleanly, and does it know
  the placement half is already on PR #61? Possible landing-page conflict if it
  routes a separate fix.
- Does the v3 round complete before or after 00:00Z Aug 16? Merge is legal from
  the reset regardless, but requires fresh approvals on whatever head the cycle
  ends on.