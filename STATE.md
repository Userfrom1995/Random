# STATE - Random factory checkpoint

- **Updated:** 2026-08-16 (~15:48Z event run 31956363832, owner comment on
  PR #67 at 15:40:30Z "/oc maintainer merge it."). **PR #67 (Meridian)
  MERGED as `c44736f`** - owner explicit override of the 2/2 daily cap;
  #66 closed; pages redeploying. Obsidian `continue` re-dispatched (billing
  retry); the model auto-switch fallback is BLOCKED (bot token lacks
  `workflows: write`). #72 infra build still in flight. main at `c44736f`.

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec competitive with
  JPEG XL / WebP / conventional methods, benchmarked on Kodak.** Research +
  architecture COMPLETE (PR #69 docs). Builder STILL STALLED on billing:
  4 attempts (1 + 3 auto-retries) hit `AI_APICallError: No payment method`
  (CreditsError) 15:07-15:18Z; PR #69 head `2377f3cc` (docs + Cargo scaffold
  only, no codec source). **`continue` RE-DISPATCHED this run** (wait-and-
  retry branch of the owner's 14:43Z billing policy, ~40 min after the last
  failure). Flow: Researcher (done) -> Architect (done) -> Builder (retrying)
  -> review -> test -> merge. Board freeze on new picks until Obsidian
  resolves stays in place.

## In flight

- **PR #69 (Obsidian) - `continue` DISPATCHED this run.** Head `2377f3cc`,
  CLEAN, MERGEABLE. If the retry fails again on CreditsError, TAG THE OWNER
  on #69 (their 15:04Z instruction) and request payment on the opencode.ai
  workspace OR an owner-side model switch (the bot cannot edit the workflow
  files - `workflows: write` missing from the Actions token). If it pushes:
  review -> test -> merge (cap resets to 0/2 at 00:00Z Aug 17; legal
  tomorrow).
- **Issue #72 (infra fix) BUILD ACTIVE - run 31954533349** (opencode build,
  in_progress since 15:03:54Z, no `opencode/72-*` branch/PR yet). Scope:
  build-verify scoped to the target PR head + force-with-lease guidance.
  **WATCH: the fix edits opencode.yml - if its push hits the same
  `workflows: write` wall that blocked my model-switch, route the fix via the
  owner or reassess.** Lab-improvement, cap-exempt, extra-hard review
  expected. On `/oc approve-test`: merge, close #72, dispatch pages.yml, THEN
  dispatch `build` on #73.
- **Issue #73 (opencode-review crash on non-PR targets) - QUEUED behind #72.**
  Never dispatched concurrently with another opencode build.
- **Issue #74 (billing) - CLOSED by the owner 15:04Z** ("try the suggested
  fixes, and if it happens again, tag me on the issue or PR where it
  occurs"). Standing auto-switch policy adopted but is OWNER-DEPENDENT until
  the bot gets `workflows: write` or the workspace gets a payment method.
- **PR #67 (Meridian) - MERGED `c44736f`, issue #66 CLOSED, pages
  redeploying.** No further action needed. `/meridian/` live after deploy.

## Lab Health & Audit Logs (#70)

- The Auditor owns the daily health summary on #70 (ran 11:30Z, found the
  build-verify false positive -> reopened as #72/#73/#74; #74 closed by the
  owner). Watch #72/#73 as the actionable infra threads. Owner's `d0f6adcd`
  auditor PAT-forwarding wiring is live on main.

## Board status (#42)

- **FROZEN by the owner's directive** - no picks until Obsidian resolves.
  Candidates parked: Corundum, Tundra, Ravel. No ideate (frozen).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` (reviewer + tester), `deepseek-v4-flash-free`
  (build/fixer/maintainer/ideate/research/architect) unchanged. Billing gate
  (#74) keeps degrading the build agent; the auto-switch to a free fallback
  (hy3-free / nemotron-3-ultra-free / nemotron-3.5-lightning-free /
  laguna-s-2.1-free; all live on the zen endpoint) is blocked by the bot's
  missing `workflows: write` permission. Next Sunday (2026-08-23): weekly
  model upgradation.

## Next steps

1. **Watch the Obsidian retry** (continue posted on PR #69): if it pushes,
   shepherd review -> test -> merge (legal after 00:00Z Aug 17). If it fails
   on billing again, TAG THE OWNER per their instruction; request payment or
   an owner-side model switch.
2. **Watch the #72 build** (31954533349): on `/oc approve-test`, merge, close
   #72, dispatch pages.yml, then dispatch `build` on #73. If its push fails
   on `workflows: write`, alert the owner.
3. **#73**: dispatch `build` only after #72 merges (never concurrent).
4. **#70**: Auditor owns the daily health summary; watch for anomalies.
5. No board picks until Obsidian resolves (owner's freeze).
6. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the Obsidian retry finally push (billing cleared when the owner closed
  #74, or transient), or fail again on CreditsError -> owner tag?
- Does the #72 build open its PR, and can it push its opencode.yml fix with
  the bot token, or does it hit the `workflows: write` wall?
- Who grants the bot `workflows: write`, or does the owner hand-switch the
  build model on the next billing failure?
- Does `/meridian/` serve correctly after the pages deploy (31956858812)?