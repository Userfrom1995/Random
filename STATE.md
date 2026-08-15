# STATE - Random factory checkpoint

- **Updated:** 2026-08-15 (~15:37Z event run 31893202814, the owner's comment
  on PR #61 at 15:36:39Z flagging Halcyon's mis-placement on the root landing
  pages).

## In flight

- **Halcyon (issue #59 -> PR #61):** **Architect v2 enhance round MID-BUILD.**
  The Architect's enhance round (run 31891252822, 15:01:03Z, commit `8be5008`)
  designed milestones 13-16: ADTs, pattern matching, tail calls + `Halcyon.Optimize`
  deterministic pass (`compile --opt` / `run-vm --opt`), JS mirror + self-hosted
  stdlib (map/filter/foldl/foldr/zip/...), docs + root pages. Build run
  31891529680 started 15:01:19Z, **job "build" STILL in_progress**; pushed
  `c9b291e` ("builder: add algebraic data types") and `a959ea4` ("builder: add
  pattern matching"). Progress file: checklist 13-14 checked, 15-16 pending.
  Head `a959ea4`, branch `opencode/59-halcyon-functional-language-vm`.
  - **OWNER FINDING (valid, actioned this run):** root `README.md` and
    `index.html` list Halcyon under "Previous Ideas/Projects" while "Current
    Project" still reads **Beambus** - incorrect; Halcyon is the live build and
    Beambus should graduate into Previous. The Reviewer's "Docs & site" check
    verified link presence but never section placement. Routed `fix` on PR #61
    (queues in group `opencode-61` behind the active build, applies on the
    final head).
  - **Owner policy (binding, commit `f1fbae9`):** on cap-full with an approved
    PR, leave it open and trigger the **Architect** (`{"action":"architect","pr":N}`).
  - **Daily shipping cap Aug 15: 2/2 REACHED** (Beambus 00:02:40Z + Glyphforge
    01:43:39Z). Halcyon merge legal after 00:00Z Aug 16.
  - **Stale approvals:** the 14:22Z reviewer + 14:51Z tester approvals were on
    head `f90c3e37`; the head has moved (v2 milestones), so the merge needs a
    fresh review/test cycle on the new head once the build + fix complete.

## Just completed

- The owner's root-page placement finding confirmed and routed to the Fixer
  (`fix` on PR #61, this run).

## Board status (#42)

- Candidates remaining: **Ravel** (Elixir/Phoenix CRDT whiteboard), **Kestrel**
  (Julia NN + draw-to-classify). Zero reactions. Next pick waits for Halcyon to
  merge (sequential policy).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` validated (reviewer + tester); Sunday weekly
  upgradation check due 2026-08-16.

## Watch items (owner-side / wiring)

- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge).
- `opencode-review-trigger.yml` still absent on main (Maintainer `review`
  decision remains the only bot-PR review path).
- Process gap (this run): Reviewer landing-page checks verify link presence but
  not section placement (Current vs Previous) - raise with the Reviewer for
  future rounds.
- Owner commit `767b901` today ("general: increase timeouts and update builder
  instructions") - not yet verified against a live build.
- Owner commit `f1fbae9` today - shipping-limit rounds route to the Architect.

## Next steps

1. Watch the v2 build (31891529680) finish milestones 15-16; the queued `fix`
   round then corrects the root-page placement on the final head.
2. After the build + fix complete: expect the JSON-handoff review/test cycle on
   the new head (14:22Z/14:51Z approvals are stale).
3. On `/oc approve-test` after 00:00Z Aug 16 (cap reset): merge PR #61
   (`gh pr merge 61 --rebase --delete-branch`), close #59, dispatch pages.yml,
   verify `/halcyon/docs/`. That is Aug 16's 1st (of max 2) new-project merge.
4. After Halcyon merges: pick from Ravel/Kestrel (reactions steer; owner's
   count double).
5. Sunday weekly model upgradation check on 2026-08-16.

## Open questions

- Does the Builder finish M15 (TCO + Optimize) and M16 (JS mirror + stdlib +
  docs + root pages) within the 25-min caps, or need a `continue`? Milestone
  pushes preserve the checkpoint either way.
- Does the Fixer's placement correction land cleanly after the v2 pushes (no
  residual conflict with the Builder's own root-page edits in M16)?
- Auto-retry 1's instant ~0s no-op (during the exhausted retry chain) remains
  unexplained; no recurrence since.