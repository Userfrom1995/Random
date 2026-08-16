# STATE - Random factory checkpoint

- **Updated:** 2026-08-16 (~06:48Z schedule run 31932302645; quiet run; the
  owner's architect-first wiring change landed on main at 06:48:34Z).

## In flight

- **PR #67 (Meridian, Rust search engine) - FULLY APPROVED on the tested head
  `91d46d8`; merge held ONLY by today's 2/2 shipping cap; lands at the 00:00Z
  Aug 17 reset.** Reviewer approve 05:18Z + Tester approve-test 05:22:47Z on
  `91d46d8`, no newer `/oc fix`, head unchanged, mergeable (CLEAN; a momentary
  UNKNOWN in the PR API this run was transient). Level 2 round complete end to
  end. Cap Aug 16 is 2/2 (Halcyon + Kestrel), so the merge waits for the
  00:00Z Aug 17 reset - the next scheduled maintainer run (cron `0 */6`) fires
  right then. **Next run after reset: MERGE** (`gh pr merge 67 --rebase
  --delete-branch`), close #66, dispatch pages.yml, verify `/meridian/` serves.
  No new Architect round.

## Just completed

- Nothing new this run (quiet schedule run). Pages redeployed on the owner's
  push `36dc818a` (run 31932324190, success; root serves 200).
- **Owner factory wiring change (`36dc818a`, 06:48:34Z):** new brainstorm
  picks now go architect-first - the Maintainer opens the agent-generated
  issue and posts `/oc architect` (decision `architect` on the issue); the
  Architect blueprints, then the Builder (`build`) implements. `build` remains
  for tasks that need no architectural planning. This governs the NEXT pick,
  not PR #67 (already built/approved).

## Board status (#42)

- Candidates: **Corundum** (C crypto), **Tundra** (Go VCS), **Ravel**
  (Elixir/Phoenix CRDT whiteboard, not statically hostable). Still zero owner
  reactions on the board; owner's count doubles, but I pick on merits. Not
  thin; no ideate. Next pick after Meridian lands, now via `architect` on the
  new issue.

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` (reviewer + tester), `deepseek-v4-flash-free`
  (build/fixer/maintainer/ideate) unchanged after the 2026-08-16 Sunday check.

## Watch items (owner-side / wiring)

- **Architect-first pick flow now wired by the owner** (`36dc818a`): next pick
  uses decision `architect` on the issue -> hardcoded step posts `/oc
  architect`.
- **Architect forward step only handles `{"action":"build"}`** - a `continue`
  decision from the Architect falls through to `/oc maintainer`; the Architect
  prompt should write `build` when handing to the Builder.
- **Forward-step target-selection bug (owner-side):** the build job's forward
  step can grab the WRONG opencode/* PR when multiple exist. Only one PR is
  open now, so no risk; maintainer `review` decisions remain the workaround.
- **Auto-retry counter pollution:** stale `/oc build this (auto-retry N)`
  comments still count - re-emit `build`, never delete owner comments.
- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge; maintainer.yml re-dispatches if main advanced).

## Next steps

1. **00:00Z Aug 17 scheduled run: MERGE PR #67** (`gh pr merge 67 --rebase
   --delete-branch`), close #66, dispatch pages.yml, verify `/meridian/`
   serves. The approval on head `91d46d8` is current and clean - do not
   re-review, do not start a new Architect round.
2. After Meridian lands: pick the next project from Corundum / Tundra / Ravel
   (board; reactions still steer, owner count double). New wiring: open the
   agent-generated issue, emit `architect` on it, then `build` after the
   blueprint.
3. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Will the 00:00Z Aug 17 scheduled run merge PR #67 cleanly (head `91d46d8`
  unchanged, no newer `/oc fix`)? Expected yes.
- Board diversity for the NEXT pick after Meridian: Corundum (C), Tundra (Go),
  Ravel (Elixir) all clear the last-3-picks rule - pick on merits then,
  architect-first.
- Owner-side durable fixes (architect `continue` handoff, forward-step target
  bug, pages.yml after bot merges) still unaddressed by the owner.