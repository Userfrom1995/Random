# STATE - Random factory checkpoint

- **Updated:** 2026-08-15 (~14:52Z event run 31891081589, the merge-handover
  run the test workflow's forward step triggered on PR #61 at 14:51:34Z after
  the Tester's clean round post-shipping-limit-round).

## In flight

- **Halcyon (issue #59 -> PR #61):** **RE-CLEARED review + test, merge held by
  the daily shipping cap.** Fixer shipping-limit round (run 31890239629,
  14:33:45Z) landed stdlib list builtins (length/reverse/append/take/drop)
  across both evaluators + VM + JS mirror with partial application, `halcyon
  eval` inline command, and caret source diagnostics. Reviewer `/oc approve`
  14:46:59Z (13/13 items). Tester approve-test 14:51:32Z (166/166 tests,
  18-program differential corpus byte-identical, 31/31 JS checks, clean build,
  exit codes 0/1/2, perf good, REPL + web playground working). Head
  `f90c3e376e07043853aa5e1b6a9e1a794bb054b5` (19 commits), PR OPEN,
  MERGEABLE/CLEAN, checks green. Branch
  `opencode/59-halcyon-functional-language-vm`.
  - **OWNER POLICY CHANGE (binding):** commit `f1fbae9` rewrote the Shipping
    Limit rule - on cap-full with an approved PR, leave it open and trigger the
    **Architect** (`{"action":"architect","pr":N}`) instead of `/oc fix`. Maps
    to `/oc architect` (enhance mode).
  - **Daily shipping cap Aug 15: 2/2 REACHED** (Beambus 00:02:40Z + Glyphforge
    01:43:39Z). Halcyon would be a 3rd new-project merge today - over the limit.
  - **THIS RUN:** `architect` on PR #61 (the Architect's next-level design
    round, per the new playbook). The merge waits for the 00:00Z Aug 16 cap
    reset; the Tester approval is standing, so after the reset it is a clean
    rebase merge.

## Just completed

- Fixer shipping-limit round landed (stdlib builtins, `eval`, caret Diag) ->
  review + test re-approval. PR #61 head `3f0465c` -> `f90c3e37`.

## Board status (#42)

- Candidates remaining: **Ravel** (Elixir/Phoenix CRDT whiteboard), **Kestrel**
  (Julia NN + draw-to-classify). Zero reactions. Halcyon (#59) cleared the
  pipeline but awaits the cap-reset merge; next pick waits for it to merge
  (sequential policy).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` validated (reviewer + tester); Sunday weekly
  upgradation check due 2026-08-16.

## Watch items (owner-side / wiring)

- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge).
- `opencode-review-trigger.yml` still absent on main (Maintainer `review`
  decision remains the only bot-PR review path).
- Owner commit `767b901` today ("general: increase timeouts and update builder
  instructions") - likely raises the build step timeouts; not yet verified
  against a live build.
- Owner commit `f1fbae9` today - shipping-limit rounds now route to the
  Architect, not the Fixer.

## Next steps

1. Watch the Architect enhance round on PR #61 (may add next-level depth).
2. On the next maintainer run after 00:00Z Aug 16 (cap reset): merge PR #61
   (`gh pr merge 61 --rebase --delete-branch`) on the standing Tester
   approval, close #59, dispatch pages.yml, verify `/halcyon/docs/`. That is
   Aug 16's 1st (of max 2) new-project merge.
3. After Halcyon merges: pick from Ravel/Kestrel (reactions steer; owner's
   count double).
4. Sunday weekly model upgradation check on 2026-08-16.

## Open questions

- Does the Architect's enhance round land meaningful next-level depth on top of
  the stdlib/eval/Diag round? Non-blocking either way.
- Will `767b901`'s timeout increases make future builds less reliant on the
  milestone-push contract?
- Auto-retry 1's instant ~0s no-op (during the exhausted retry chain) remains
  unexplained; no recurrence since.