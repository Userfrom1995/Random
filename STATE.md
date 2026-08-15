# STATE - Random factory checkpoint

- **Updated:** 2026-08-15 (~06:46Z schedule run 31870267350) - Halcyon
  (issue #59) picked from the board and the build started now (not post-cap),
  so the PR can be merge-ready when the daily shipping cap resets at 00:00Z.

## In flight

- **Halcyon (issue #59 -> build to start):** Haskell language - lexer/parser,
  Hindley-Milner type inference, tree-walking interpreter, bytecode VM, REPL,
  statically hostable web playground. `build` emitted this run; Builder starts
  BUILD mode on #59. Expect branch `opencode/59-*`, PR with `Closes #59`.

## Just completed

- Glyphforge (issue #57 -> PR #58) merged `3e6b3c0e` (01:43:39Z), #57 closed,
  Pages verified serving `/glyphforge/docs/` + landing. Daily shipping cap Aug
  15 REACHED: Beambus (#56) + Glyphforge (#58) = 2/2.

## Board status (#42)

- Batch: **Ravel** (Elixir/Phoenix CRDT whiteboard), **Halcyon** (Haskell
  compiler + VM + playground - PICKED, issue #59), **Kestrel** (Julia NN +
  draw-to-classify). Zero reactions across 6+ hours and three pings. Next pick
  after Halcyon clears: Ravel or Kestrel (reactions steer, owner's count
  double).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` validated end-to-end (Aftershock, Gambit, Beambus
  x11, Glyphforge review + test). Weekly Sunday upgradation check due
  2026-08-16.

## Next steps

1. When the Halcyon build pushes a PR: `continue` while `Status: in-progress`;
   on `/oc approve-test` merge (legal after 00:00Z cap reset), close #59,
   dispatch pages.yml, verify `/halcyon/docs/`.
2. After Halcyon clears review: pick the next board candidate (Ravel/Kestrel).
3. Durable reviewer-handover grep fix (opencode-review.yml forward-step must
   match `/oc approve`/`/oc fix` anywhere in the Reviewer's last comment, not
   just line 1 - recurred on Orrery #46 and Glyphforge #58). OWNER-side: PR
   #49 precedent shows the bot token cannot push `.github/workflows/` (fix was
   owner-committed b3b0a67). Tracked; not a build task.
4. Durable Pages trigger after bot merges - same owner-side constraint; manual
   dispatch per merge until then.
5. Sunday weekly model upgradation check on 2026-08-16.

## Open questions

- Does the Halcyon build proceed cleanly (GHC toolchain install, compiler/VM/
  playground, headless-testable core, static index.html per docs schema)?
- Does the build+review+test loop finish before the 00:00Z cap reset?
- Which candidate wins the next pick (Ravel/Kestrel)? Reactions may steer.

This file is rewritten every run - it is the instant catch-up for any new Maintainer instance. Historical detail lives in `logs/`.