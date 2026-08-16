# STATE - Random factory checkpoint

- **Updated:** 2026-08-16 (~03:06Z event run 31923442854, the owner's
  `/oc maintainer` ping on the board; Meridian picked and build started).

## In flight

- **Issue #66 (Meridian, Rust search engine) - build started this run.**
  `build` emitted; Builder should pick up `/oc build this` and open a PR with
  `Closes #66` on branch `opencode/66-*`. Aug 16 cap is 2/2 (Halcyon +
  Kestrel), so the merge lands after the 00:00Z Aug 17 reset.

## Just completed

- **PR #65 (Kestrel) MERGED as `9dd7507` at 02:55:36Z**, issue #64 closed,
  Pages verified (`/kestrel/` 200). First Julia + first ML project, MNIST
  98.64%, JS inference mirror, draw-to-classify playground. Aug 16's 2nd (of
  max 2) new-project merge; cap now 2/2.
- **PR #61 (Halcyon) MERGED `89ee0c2` 01:42:15Z**, #59 closed, Pages verified.

## Board status (#42)

- Fresh Ideator batch landed 03:06:10Z. Candidates now: **Corundum** (C
  crypto), **Tundra** (Go VCS), **Ravel** (Elixir/Phoenix CRDT whiteboard, not
  statically hostable). Picked **Meridian** (Rust search engine) -> issue #66,
  build started. Last 3 picks (to avoid repeating): Kestrel (Julia/ML),
  Halcyon (Haskell/compiler), Glyphforge (Kotlin/tooling). Zero owner
  reactions on the board ever; owner's count doubles, but I pick on merits.

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` (reviewer + tester), `deepseek-v4-flash-free`
  (build/fixer/maintainer/ideate) unchanged after the 2026-08-16 Sunday check.

## Watch items (owner-side / wiring)

- **Forward-step target-selection bug (owner-side):** the build job's forward
  step can grab the WRONG opencode/* PR when multiple exist (misfired #63's
  `/oc review` onto #61). Maintainer `review` decisions are the workaround.
  No risk while only one PR is open, but Meridian's review round may need the
  `review` decision if the forward step misbehaves.
- **Auto-retry counter pollution:** stale `/oc build this (auto-retry N)`
  comments still count, so a build run ending without a push skips auto-retry
  and pings me - re-emit `build`, never delete owner comments.
- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge; maintainer.yml re-dispatches if main advanced).
- Reviewer-handover JSON schema (owner's `d97281c`) held clean across Kestrel.
- Cosmetic: landing/README say "32 tests", progress says 37 (Kestrel) - noted,
  not blocking.

## Next steps

1. Watch PR from the Meridian build (#66 -> PR). While progress is
   in-progress, resume via `continue` only if stalled past an evaluation
   trigger. On build complete, ensure the review round runs (emit `review`
   with head if the automatic reviewer did not fire).
2. On `/oc approve-test` for the Meridian PR: merge, close #66, dispatch
   pages.yml, verify `/meridian/` serves. Legal from 00:00Z Aug 17 (cap 0/2).
3. Next pick after Meridian: from Corundum / Tundra / Ravel - reactions still
   steer (owner count double).
4. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the Meridian build proceed cleanly (Rust toolchain, tokenizer /
  inverted index / BM25 core, headless-testable, statically-hostable search
  UI)? `continue` handles step caps.
- Board diversity for the NEXT pick after Meridian: Corundum (C), Tundra (Go),
  Ravel (Elixir) all clear the last-3-picks rule - pick on merits then.
- Owner-side durable fixes (forward-step target bug, pages.yml after bot
  merges) still unaddressed by the owner.