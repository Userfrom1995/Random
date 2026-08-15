# STATE - Random factory checkpoint

- **Updated:** 2026-08-15 (~17:55Z event run 31899534457, the `/oc maintainer`
  merge-handover the test workflow's forward step posted on PR #63 at 17:52:16Z
  after the Tester's `/oc approve-test` at 17:52:14Z).

## In flight

- **PR #63 (Glyphforge -> Current, Beambus -> Previous, hero GitHub link;
  `Closes #62`): MERGED.** Reviewer approve 17:50:45Z, Tester approve-test
  17:52:14Z, no newer `/oc fix` after. Merged as `4f31a3b4` at 17:54:02Z
  (rebase, branch deleted), issue #62 auto-closed, Pages dispatched
  (31899620395, success) - live site verified 200 with Glyphforge Current +
  hero GitHub link. Factory/landing-page improvement, NO shipping cap.

- **Halcyon (issue #59 -> PR #61): v3 BUILD RESUMED via `/oc continue`.**
  Build run 31897133922 COMPLETED (17:01:22Z -> ~17:49Z, SUCCESS) pushing only
  M17 (`b3e1740d` "builder: implement Halcyon milestone 17 - top-level
  definitions and module system"). The 17:49Z maintainer run (31899384543)
  routed `review` on PR #63 but never resumed the Halcyon build; THIS run
  routed `continue` on PR #61. Progress file: checklist 17 checked, 18-21
  pending (records, type classes, Char/strings, VM profiler), Status
  in-progress.
  - **PR #61 now DIRTY/CONFLICTING**: #63 merged README/index.html placement
    (Glyphforge Current, Beambus Previous) overlapping Halcyon's M16d edits
    (Halcyon Current, Beambus Previous). The continue must keep Halcyon as
    Current and graduate BOTH Beambus + Glyphforge to Previous (newest first)
    on merge.
  - **Daily shipping cap Aug 15: 2/2 REACHED** (Beambus 00:02:40Z + Glyphforge
    01:43:39Z). Halcyon merge legal after 00:00Z Aug 16; the final v3 head
    needs a fresh review + test cycle (existing approvals are pre-v3 / stale).

## Just completed

- Merged PR #63 (factory fix, no cap), #62 auto-closed, Pages dispatched + live
  verified, and resumed the Halcyon v3 build via `continue` on PR #61.

## Board status (#42)

- Candidates remaining: **Ravel** (Elixir/Phoenix CRDT whiteboard), **Kestrel**
  (Julia NN + draw-to-classify). Zero reactions. Next pick waits for Halcyon to
  merge (sequential policy).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` validated (reviewer + tester); Sunday weekly
  upgradation check due 2026-08-16.

## Watch items (owner-side / wiring)

- **Forward-step target-selection bug (owner-side; PR #49 precedent):** the
  build job's forward step (`gh pr list ... startswith("opencode/") | last`)
  can grab the WRONG opencode/* PR when multiple exist - it misfired PR #63's
  `/oc review` onto PR #61 (17:35:18Z). Maintainer `review` decisions are the
  workaround.
- **Auto-retry counter pollution:** the three stale `/oc build this
  (auto-retry N)` comments (12:36-13:02Z) still count, so a build run ending
  without a push skips auto-retry and pings me - re-emit `build`, never delete
  owner comments.
- Landing-page merge conflict between #61 and #63 now real (both touch
  README.md + index.html placement sections) - the continue run must resolve
  it: Halcyon = Current, Beambus + Glyphforge = Previous (newest first).
- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge).
- Process gap (keep watching): Reviewer landing-page checks should verify
  section placement (Current vs Previous), not just links.
- Owner commit `f1fbae9` - shipping-limit rounds route to the Architect.

## Next steps

1. Watch the `continue` run on PR #61 (M18-21 + conflict resolution). If it
   ends mid-milestone, re-emit `continue` as needed. On completion route the
   final v3 head to a fresh Reviewer then Tester cycle.
2. On `/oc approve-test` for PR #61 **on the final v3 head after 00:00Z Aug
   16** (cap reset): merge PR #61 (`gh pr merge 61 --rebase --delete-branch`),
   close #59 (+ confirm landing-page placement: Halcyon Current, Beambus +
   Glyphforge Previous), dispatch pages.yml, verify `/halcyon/docs/`. That is
   Aug 16's 1st (of max 2) new-project merge.
3. After Halcyon merges: pick from Ravel/Kestrel (reactions steer; owner's
   count double).
4. Sunday weekly model upgradation check on 2026-08-16.

## Open questions

- Does the `continue` on PR #61 finish M18-21 in one round and resolve the
  #63-overlap landing-page conflict cleanly (Halcyon Current, Beambus +
  Glyphforge Previous)? If placement is wrong after M21, route a `fix`.
- Will the fresh review/test cycle on the final v3 head land before or after
  00:00Z Aug 16? Merge timing follows the reset either way.
- Does the owner want the forward-step target-selection bug fixed (would need
  an owner-pushed workflow change)?