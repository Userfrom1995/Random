# STATE - Random factory checkpoint

- **Updated:** 2026-08-16 (~08:20Z event run 31936077662; the owner set a new
  priority project on #42 at 08:17:22Z: Obsidian, a Kodak-benchmarked lossless
  image-compression codec, becomes the factory's fundamental goal until
  achieved or proven unviable).

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec competitive with
  JPEG XL / WebP / conventional methods, benchmarked on Kodak.** Created this
  run as the bot; `research` emitted (owner ordered researchers first; the
  Researcher agent was integrated by the owner at 08:06Z, commit `b1116ff2`).
  Flow: Researcher (spec) -> Architect (design) -> Builder (build) -> review ->
  test -> merge. Every iteration benchmarked on Kodak and documented. NO new
  projects or board picks until Obsidian resolves. Owner: no time constraint,
  no rush.

## In flight

- **PR #67 (Meridian, Rust search engine) - FULLY APPROVED on the tested head
  `91d46d8`; merge held ONLY by today's 2/2 shipping cap; lands at the 00:00Z
  Aug 17 reset.** Reviewer approve 05:18Z + Tester approve-test 05:22:47Z on
  `91d46d8`, no newer `/oc fix`, head unchanged, mergeable (mergeStateStatus
  was UNKNOWN transiently this run; earlier `gh pr list` showed CLEAN). This is
  complete work, not a new start, so the owner's freeze does not touch it.
  **Next scheduled run after the reset: MERGE** (`gh pr merge 67 --rebase
  --delete-branch`), close #66, dispatch pages.yml, verify `/meridian/` serves.
  No new Architect round.

## Board status (#42)

- **FROZEN by the owner's directive** - no picks until Obsidian resolves.
  Candidates parked: Corundum (C crypto), Tundra (Go VCS), Ravel (Elixir/Phoenix
  CRDT whiteboard). Zero owner reactions across the board's life. No ideate
  (frozen anyway).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` (reviewer + tester), `deepseek-v4-flash-free`
  (build/fixer/maintainer/ideate/research/architect) unchanged after the
  2026-08-16 Sunday check. Researcher integrated by the owner (`b1116ff2`).

## Watch items (owner-side / wiring)

- Researcher agent now live: `opencode.yml` `research` job (`/oc research`)
  forwards `{"action":"architect"}` to the Architect. First assignment: #68.
- Architect forward step only handles `{"action":"build"}` - a `continue`
  decision falls through to `/oc maintainer`; Architect should write `build`.
- Forward-step target-selection bug (owner-side): can grab the wrong
  opencode/* PR when multiple exist. Only PR #67 open now - no risk.
- Auto-retry counter pollution: stale `/oc build this (auto-retry N)` comments
  still count - re-emit, never delete owner comments.
- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge; maintainer.yml re-dispatches if main advanced).

## Next steps

1. **00:00Z Aug 17 scheduled run: MERGE PR #67** (`gh pr merge 67 --rebase
   --delete-branch`), close #66, dispatch pages.yml, verify `/meridian/`
   serves. Do not re-review, do not start a new Architect round.
2. **Obsidian (#68) is THE project** - shepherd the pipeline:
   Researcher (`research` emitted) -> Architect -> Builder -> review -> test ->
   merge. Resume with `continue` while the build is in-progress.
3. No board picks until Obsidian resolves (owner's freeze).
4. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the Researcher's first round on #68 land clean (Kodak dataset access,
  literature-grounded spec, benchmark methodology, handoff to Architect)?
- Will the 00:00Z Aug 17 run merge PR #67 cleanly (head `91d46d8` unchanged,
  no newer `/oc fix`)? Expected yes.
- Obsidian iteration loop: when a competitive result appears, does the owner
  call it done or keep iterating? Treat "proven unviable" as a documented
  research conclusion, not a failure.
- Obsidian's PR is a new-project PR - subject to the 2/day merge cap when it
  ships.