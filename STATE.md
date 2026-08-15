# STATE - Random factory checkpoint

- **Updated:** 2026-08-15 (~13:20Z event run 31886911855, owner ping on #59
  asking why the build runs did not push and whether the current one is going
  well). Diagnosed the Builder's no-push pattern: the 25-min agent-step timeout,
  NOT GHC.

## In flight

- **Halcyon (issue #59 -> PR #61):** The Architect->Builder flow is proven but
  the **Builder keeps hitting the 25-minute agent-step timeout before its first
  commit**. Root cause diagnosed from run logs: GHC 9.14.1 + cabal are present
  (not a toolchain problem). Each build attempt writes a huge volume of real
  Haskell code (Lexer/Parser/Type/Value/Eval/Op/Compile/Vm) in one session and
  dies with `The action has timed out.` before ever committing/pushing:
  - initial build run 31883951535: full 25-min cap, timeout at 12:36:26Z, no push
  - auto-retry 1 run 31885036527: ~0s instant no-op, nothing written
  - auto-retry 2 run 31885050733: wrote most of the compiler/VM over ~25 min,
    timeout at 13:02:15Z, no push (work lost with the ephemeral runner)
  - **auto-retry 3 run 31886143789: IN PROGRESS since 13:02:29Z** (was ~20 min
    in at this run's snapshot), facing the same ~13:27Z cap.
  PR head unchanged at `ff4568a4` (Architect's blueprint commit). This is the
  3rd and final auto-retry: if it also ends without a push, the verify step
  errors, the forward step posts `/oc maintainer` on PR #61, and I get pinged
  to take over with a `continue` that mandates milestone-by-milestone pushes.

## Just completed

- Answered the owner's direct question on #59 with the log evidence: not GHC,
  it is the 25-min step cap killing sessions before their first commit+push.
- The fix is behavioral (Builder should push after each milestone), not wiring.

## Board status (#42)

- Candidates remaining: **Ravel** (Elixir/Phoenix CRDT whiteboard), **Kestrel**
  (Julia NN + draw-to-classify). Zero reactions. Halcyon (#59) in progress.

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` validated; Sunday weekly upgradation check due
  2026-08-16.

## Watch items (owner-side / wiring)

- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge).
- Builder reliability on Halcyon is the live concern: 3 attempts, 0 pushes, all
  killed by the 25-min step timeout. If auto-retry 3 also ends with no push,
  do NOT blindly re-trigger: emit `continue` (or, if the Builder still cannot
  make progress in segments, consider whether the opencode.yml agent-step
  timeout for the build job should be raised - that is a workflow edit the bot
  cannot push, so it would need the owner).

## Next steps

1. Let auto-retry 3 (run 31886143789) finish. If it pushes, watch for the
   review loop via the JSON handoff. If it times out with no push (expected
   around 13:27Z), the workflow's forward step posts `/oc maintainer` on #61
   and I will be pinged.
2. On that ping: emit `continue` on PR #61 instructing the Builder (via the
   progress file and its prompt) to commit and push after each milestone rather
   than all-at-once, so no work is lost to the step cap. If it still cannot
   segment, raise the step timeout with the owner.
3. Merge is legal after the 00:00Z Aug 16 cap reset regardless; on `/oc
   approve-test` merge `gh pr merge <N> --rebase --delete-branch`, close #59,
   dispatch pages.yml, verify `/halcyon/docs/`.
4. After Halcyon clears: pick from Ravel/Kestrel (reactions steer; owner's
   count double).
5. Sunday weekly model upgradation check on 2026-08-16.

## Open questions

- Will the Builder ever push segment-by-segment within the 25-min cap, or does
  the Halcyon build need either a `continue` nudging it to incremental pushes
  or a raised step timeout (owner-side workflow edit)?
- The two no-push attempts were both killed by the step timeout while writing
  real code; auto-retry 1's instant no-op is a separate, unexplained hiccup.
  Watch whether it recurs.
