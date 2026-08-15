# STATE - Random factory checkpoint

- **Updated:** 2026-08-15 (~17:41Z event run 31898982743, the `/oc maintainer`
  merge-handover the test workflow's forward step posted on PR #61 at 17:40:35Z
  after the Tester's `/oc approve-test`).

## In flight

- **Halcyon (issue #59 -> PR #61):** **V3 BUILD ACTIVE, head `9a90ebd`.**
  Build run 31897133922 (started 17:01:22Z, 60-min agent step) is ACTIVELY
  RUNNING: job "build" in_progress, agent step since 17:01:29Z, branch head
  STILL `9a90ebd` as of 17:44Z - Builder mid-M17 (top-level defs + module
  system), no v3 milestone pushed yet. Do NOT emit duplicate triggers while it
  runs.
  - **IMPORTANT - the review/test approvals that just landed (Reviewer
    `/oc approve` 17:37:54Z + Tester `/oc approve-test` 17:40:34Z) are on the
    PRE-V3 head `9a90ebd` (v2 complete + v3 design, v3 NOT built) and were a
    ROUTING MISFIRE** - see PR #63. They go stale the moment the Builder pushes
    M17-21. The binding approvals for the final v3 head come after the build
    completes + a fresh review/test cycle passes.
  - **Daily shipping cap Aug 15: 2/2 REACHED** (Beambus 00:02:40Z + Glyphforge
    01:43:39Z). Halcyon merge legal after 00:00Z Aug 16.

- **Issue #62 / PR #63 (Glyphforge -> Current, Beambus -> Previous, + GitHub
  repo link in the hero; `Closes #62`):** PR #63 OPEN, head `de8cb8aa`,
  MERGEABLE/CLEAN, created 17:35:16Z by the Builder (run 31898630233, success).
  **Never routed to review** - the #62 build's forward step misfired its
  `/oc review` onto PR #61 instead (the `last opencode/* PR` target pick).
  THIS RUN routes `review` on PR #63 (head `de8cb8aa`). It is a factory/
  landing-page improvement PR, NOT a new project, so it is NOT subject to the
  2/day shipping cap and can merge freely once review + test pass; then #62
  closes and the live site shows Glyphforge Current + the hero GitHub link.

## Just completed

- Routed `review` on PR #63 (correcting the misfire); posted the corrected
  status comment on PR #61 (no merge: cap 2/2 + approvals on pre-v3 head).

## Board status (#42)

- Candidates remaining: **Ravel** (Elixir/Phoenix CRDT whiteboard), **Kestrel**
  (Julia NN + draw-to-classify). Zero reactions. Next pick waits for Halcyon to
  merge (sequential policy).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` validated (reviewer + tester); Sunday weekly
  upgradation check due 2026-08-16.

## Watch items (owner-side / wiring)

- **NEW WIRING BUG (owner-side; bot cannot push workflow files - PR #49
  precedent):** the build job's forward-step target selection
  (`gh pr list ... startswith("opencode/") | last | .number`) can grab the
  WRONG opencode/* PR when multiple exist. It misfired PR #63's `/oc review`
  onto PR #61 (17:35:18Z). Flagged for a factory-ops fix; maintainer `review`
  decisions work around it.
- **Auto-retry counter pollution:** the three stale `/oc build this
  (auto-retry N)` comments (12:36-13:02Z) still count, so a build run ending
  without a push skips auto-retry and pings me - re-emit `build`, never delete
  owner comments.
- Issue #62 placement half (Halcyon vs Glyphforge vs Beambus ordering): PR #63
  promotes Glyphforge now (correct for the live site); PR #61's M16d promotes
  Halcyon when it merges - Halcyon supersedes. Watch for landing-page merge
  conflicts between the two PRs (both touch README.md + index.html sections).
- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge).
- Process gap (resolved for Halcyon, keep watching): Reviewer landing-page
  checks should verify section placement (Current vs Previous), not just links.
- Owner commit `f1fbae9` - shipping-limit rounds route to the Architect.

## Next steps

1. Watch the active v3 build on PR #61 (31897133922). If it pushes M17-21:
   resume via `continue` as needed per the milestone-push contract; on
   completion, route the FINAL v3 head to a fresh Reviewer then Tester cycle.
   If it dies without a push: expect the stale-retry-counter ping, re-emit
   `build` on the existing branch.
2. PR #63: after its (now-routed) review + test pass, merge freely (factory
   fix, no cap), close #62, dispatch pages.yml.
3. On the next `/oc approve-test` for PR #61 **on the final v3 head after
   00:00Z Aug 16** (cap reset): merge PR #61 (`gh pr merge 61 --rebase
   --delete-branch`), close #59 (+ confirm #62 placement satisfied), dispatch
   pages.yml, verify `/halcyon/docs/`. That is Aug 16's 1st (of max 2) new-
   project merge.
4. After Halcyon merges: pick from Ravel/Kestrel (reactions steer; owner's
   count double).
5. Sunday weekly model upgradation check on 2026-08-16.

## Open questions

- When does the v3 Builder push M17 (head still `9a90ebd` at 17:44Z, ~44 min
  into the 60-min agent cap)? Watch for the retry-counter ping if it ends
  without a push.
- Will PR #63 clear review + test cleanly (small landing-page/README fix +
  hero GitHub link)? Merge it freely on approve-test; watch for landing-page
  conflicts when #61 merges afterward.
- Does the owner want the forward-step target-selection bug fixed (would need
  an owner-pushed workflow change)?