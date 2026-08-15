# STATE - Random factory checkpoint

- **Updated:** 2026-08-15 (~22:38Z event run 31912624683, the merge handover
  after the v4 round's Tester approve-test at 22:37:37Z).

## In flight

- **PR #61 (Halcyon -> issue #59): v4 COMPLETE, APPROVED, HELD BY CAP, RESET IMMINENT.**
  The v4 round finished all 26 milestones on head `26f5bd5` (MERGEABLE/CLEAN):
  M17-21 (v3: modules, records, type classes, Char/strings, profiler) and
  M22-26 (v4: effect system, user-defined operators + type synonyms, prelude +
  REPL colon commands, serialized HALCYONBC1 bytecode artifact + bench,
  JS mirror/playground/docs sync). The v4 final review found one doc finding
  (stale "596 tests" on root landing pages); Fixer corrected to "684 tests"
  (`26f5bd5`). Fresh Reviewer approve 22:32:39Z (684/684, all 13 items);
  Tester approve-test 22:37:37Z (684/684, 53-program corpus byte-identical,
  269/269 JS checks). No newer `/oc fix` after. Landing pages verified:
  Halcyon = Current / Live now, Glyphforge + Beambus + Aftershock = Previous
  newest first.
  - **Daily shipping cap Aug 15: 2/2 REACHED** (Beambus 00:02:40Z + Glyphforge
    01:43:39Z). Halcyon merge legal after 00:00Z Aug 16 - **~1.4h away**.
  - **Holding for the reset - no 5th Architect round.** Per the loop caution,
    a standing approval exists on unmoved head `26f5bd5` and the cap resets
    imminently; routing another round would move the head and delay the merge
    many hours past the reset. The 00:00Z Aug 16 scheduled maintainer sweep
    merges on the standing approval. Owner was offered the choice (comment).

## Just completed

- PR #61's v4 build + fresh review/test cycle (22:21-22:37Z) - fully cleared
  on head `26f5bd5` after the Fixer's stale-count correction. This run held
  for the imminent reset instead of routing a 5th Architect round.
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
- Process gap (reviewer landing-page checks): section placement (Current vs
  Previous) must be verified, not just links. Confirmed correct on the
  current head this round.
- Owner commit `f1fbae9` - shipping-limit rounds route to the Architect.
  Applied for v2/v3/v4; deliberately paused this round because the reset is
  ~1.4h away with a standing approval (loop caution).
- Owner commit `767b901` - increased workflow timeouts + builder
  instructions (the milestone-push contract is in the Builder prompt).

## Next steps

1. **At 00:00Z Aug 16** (cap reset; next scheduled maintainer sweep `0 */6
   * * *`): merge PR #61 on the standing approval (`gh pr merge 61 --rebase
   --delete-branch`), close #59, dispatch pages.yml, verify `/halcyon/docs/`
   serves. Confirm landing-page placement (Halcyon = Current, Glyphforge +
   Beambus + Aftershock = Previous newest first) and the hero GitHub link
   before merging. Aug 16's 1st (of max 2) new-project merge.
2. If the owner instead requests a 5th Architect round (I offered), route
   `architect` on PR #61 before the reset; the standing approval then goes
   stale and needs a fresh review+test on the new head.
3. After Halcyon merges: pick from Ravel/Kestrel (reactions steer; owner's
   count double).
4. Sunday weekly model upgradation check on 2026-08-16.

## Open questions

- Does the 00:00Z Aug 16 scheduled run fire on time and merge PR #61 on the
  standing approval (head `26f5bd5` must not move)? If head moves pre-reset,
  the approval is stale and a fresh review+test cycle is required.
- If the owner wants another Architect round, the loop resumes - but each
  round grows the PR and delays the merge by one full review+test cycle.
  Merge immediately the moment an approve-test passes on a post-reset head.