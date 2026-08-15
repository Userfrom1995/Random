# STATE - Random factory checkpoint

- **Updated:** 2026-08-15 (~18:36Z schedule run 31901565618, the 4x/day
  sweep. Builder mid-v3-build on PR #61 (M18 landed, M19 in flight);
  landing-page conflict with merged #63 resolved on the branch.)

## In flight

- **PR #61 (Halcyon -> issue #59): v3 BUILD ACTIVE.** The 17:55Z run's
  `continue` (owner 17:57:13Z) resumed the Builder: M17 already landed
  (b3e1740d), **M18 (record types) pushed** (Builder comment 18:30:55Z, bugs
  found+fixed: record-entry/pattern comma consumption, VM TestRecord field
  order), forward step re-emitted `/oc continue` at 18:30:57Z -> **run
  31901335358 build job IN PROGRESS on M19 (type classes)**. Head
  `75a1eb1c`, MERGEABLE/CLEAN. Progress file: 17-18 checked, 19-21 pending
  (type classes, Char + strings, VM profiler + optimizer expansion), Status
  in-progress.
  - **Landing-page conflict RESOLVED**: PR is CLEAN; verified on branch -
    README + index.html both have Halcyon = Current / Live now, Previous =
    Glyphforge -> Beambus -> Aftershock (newest first), hero GitHub repo
    link present. No fix needed.
  - **Daily shipping cap Aug 15: 2/2 REACHED** (Beambus 00:02:40Z +
    Glyphforge 01:43:39Z). Halcyon merge legal after 00:00Z Aug 16; the
    final v3 head needs a fresh review + test cycle (existing approvals are
    on the pre-v3 head b1897b1, stale once M19-21 land).

## Just completed

- PR #63 (Glyphforge promotion, `Closes #62`) merged as `4f31a3b` 17:54:02Z
  (factory fix, no cap); #62 closed; main Pages live with Glyphforge =
  Current + hero GitHub link. Builder's v3 continue advanced PR #61 through
  M17 + M18.

## Board status (#42)

- Candidates remaining: **Ravel** (Elixir/Phoenix CRDT whiteboard),
  **Kestrel** (Julia NN + draw-to-classify). Zero reactions. Next pick waits
  for Halcyon to merge (sequential policy).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` validated (reviewer + tester); Sunday weekly
  upgradation check due 2026-08-16.

## Watch items (owner-side / wiring)

- **Forward-step target-selection bug (owner-side; PR #49/#63 precedent):**
  the build job's forward step (`gh pr list ... startswith("opencode/") |
  last`) can grab the WRONG opencode/* PR when multiple exist - it misfired
  #63's `/oc review` onto #61 (17:35:18Z). Maintainer `review` decisions are
  the workaround. Only #61 is open now, so no active risk.
- **Auto-retry counter pollution:** the three stale `/oc build this
  (auto-retry N)` comments (12:36-13:02Z) still count, so a build run ending
  without a push skips auto-retry and pings me - re-emit `build`, never
  delete owner comments. `continue` runs are unaffected.
- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch
  per merge).
- Process gap (keep watching): Reviewer landing-page checks should verify
  section placement (Current vs Previous), not just links. The Reviewer must
  confirm placement on the final v3 head this round.
- Owner commit `f1fbae9` - shipping-limit rounds route to the Architect.

## Next steps

1. Watch run 31901335358 (M19 type classes). The Builder's forward step
   re-emits `/oc continue` at each milestone; re-emit `continue` myself only
   if a run ends without a decision file and nothing is in flight.
2. When the v3 build completes (M21 + Status: complete): route the final v3
   head to a fresh Reviewer then Tester cycle (stale-retry/quirk-proofed
   `review` decision if the JSON handoff misfires).
3. On `/oc approve-test` for PR #61 **on the final v3 head after 00:00Z Aug
   16** (cap reset): merge PR #61 (`gh pr merge 61 --rebase --delete-branch`),
   close #59 (+ confirm landing-page placement: Halcyon Current, Glyphforge +
   Beambus + Aftershock Previous newest first), dispatch pages.yml, verify
   `/halcyon/docs/`. That is Aug 16's 1st (of max 2) new-project merge.
4. After Halcyon merges: pick from Ravel/Kestrel (reactions steer; owner's
   count double).
5. Sunday weekly model upgradation check on 2026-08-16.

## Open questions

- Does the Builder finish M19-21 within one more `continue` or several?
  Type classes are the biggest remaining lift (dictionary passing, class/
  instance decls, constraint contexts, instance resolution).
- Will the fresh review/test cycle on the final v3 head land before or after
  00:00Z Aug 16? Merge timing follows the reset either way.
- Does the Builder's forward step keep re-emitting `/oc continue` cleanly at
  each milestone checkpoint (as it did after M18)?
- Does the owner want the forward-step target-selection bug fixed (would need
  an owner-pushed workflow change)?