# STATE - Random factory checkpoint

- **Updated:** 2026-08-15 (~20:25Z event run 31906612308, the merge handover
  after the v3 round's Tester approve-test at 20:24:40Z).

## In flight

- **PR #61 (Halcyon -> issue #59): v3 COMPLETE, APPROVED, HELD BY CAP.** The
  v3 round finished all 21 milestones on head `861830bb` (MERGEABLE/CLEAN):
  M17 top-level defs + module system (`--lib`, `halcyon/lib/*.hly` split),
  M18 record types, M19 type classes (dictionary passing), M20 Char + string
  ops, M21 VM profiler (`--profile`/`--stats`) + optimizer expansion (DCE +
  copy/constant propagation) + JS mirror/playground/docs sync. Fresh Reviewer
  approve 20:20:25Z (596/596, all 13 items); Tester approve-test 20:24:40Z
  (596/596, all green). No newer `/oc fix` after. Landing pages verified:
  Halcyon = Current / Live now, Glyphforge + Beambus + Aftershock = Previous
  newest first; hero GitHub repo link present (owner's #62 ask, on main via
  merged #63).
  - **Daily shipping cap Aug 15: 2/2 REACHED** (Beambus 00:02:40Z + Glyphforge
    01:43:39Z). Halcyon merge legal after 00:00Z Aug 16.
  - **Shipping-limit round in flight:** per the owner's playbook (`f1fbae9`)
    the Architect is dispatched for the v4 enhancement round (third
    consecutive Architect shipping-limit round; v2 = ADTs/pattern-matching/
    TCO/optimizer, v3 = modules/records/classes/strings/profiler). Merge
    stays held by the cap; the v4 head will need a fresh review/test before
    the post-reset merge.

## Just completed

- PR #61's v3 build + fresh review/test cycle (20:17-20:24Z) - fully cleared
  on head `861830bb`. This run routed the Architect v4 round per the
  shipping-limit playbook.
- Earlier today: PR #63 (Glyphforge promotion + hero GitHub link, `Closes
  #62`) merged as `4f31a3b` 17:54Z (factory fix, no cap); #62 closed.

## Board status (#42)

- Candidates remaining: **Ravel** (Elixir/Phoenix CRDT whiteboard),
  **Kestrel** (Julia NN + draw-to-classify). Zero reactions. Next pick waits
  for Halcyon to merge (sequential policy).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` validated (reviewer + tester); Sunday weekly
  upgradation check due 2026-08-16.

## Watch items (owner-side / wiring)

- **Forward-step target-selection bug (owner-side; PR #63/#61 precedent):**
  the build job's forward step (`gh pr list ... startswith("opencode/") |
  last`) can grab the WRONG opencode/* PR when multiple exist - it misfired
  #63's `/oc review` onto #61 (17:35:18Z). Maintainer `review` decisions are
  the workaround. Only #61 is open now, so no active risk.
- **Auto-retry counter pollution:** the three stale `/oc build this
  (auto-retry N)` comments (12:36-13:02Z) still count, so a `build` run
  ending without a push skips auto-retry and pings me - re-emit `build`,
  never delete owner comments. `continue` runs are unaffected.
- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch
  per merge).
- Process gap (keep watching): Reviewer landing-page checks should verify
  section placement (Current vs Previous), not just links. Confirmed
  correct on the current head this round.
- Owner commit `f1fbae9` - shipping-limit rounds route to the Architect.
- Owner commit `767b901` - increased workflow timeouts + builder
  instructions (the milestone-push contract is in the Builder prompt).

## Next steps

1. Watch the Architect v4 round on PR #61 (expect blueprint appended to
   `ideas/2026-08-15-halcyon-functional-language-vm.md` + `/oc build this`
   handoff -> Builder milestones on the existing branch).
2. When the v4 build completes: route the new head to a fresh Reviewer then
   Tester cycle (stale-retry/quirk-proofed `review` decision if the JSON
   handoff misfires).
3. On `/oc approve-test` for PR #61 **after 00:00Z Aug 16** (cap reset):
   merge `gh pr merge 61 --rebase --delete-branch`, close #59, dispatch
   pages.yml, verify `/halcyon/docs/`. Confirm landing-page placement
   (Halcyon Current, Glyphforge + Beambus + Aftershock Previous newest
   first) and the hero GitHub link before merging. Aug 16's 1st (of max 2)
   new-project merge.
4. After Halcyon merges: pick from Ravel/Kestrel (reactions steer; owner's
   count double).
5. Sunday weekly model upgradation check on 2026-08-16.

## Open questions

- What does the Architect design for v4 (modules/records/classes/strings/
  profiler already landed)? Third shipping-limit round, so it needs to find
  genuinely next-level depth to justify another full review+test cycle.
- Will the v4 cycle land before or after 00:00Z Aug 16? Merge timing follows
  the reset either way; merge immediately the moment an approve-test passes
  on a post-reset head.
- Loop caution: each Architect round grows the PR and delays the merge. The
  playbook is owner-mandated, so keep routing Architect rounds while the cap
  holds, but do not let the round block the merge past the reset if a
  standing approval exists on a head that has not moved.