# STATE - Random factory checkpoint

- **Updated:** 2026-08-16 (~16:05Z event run 31957537085, owner "/oc
  maintainer" on issue #72 at 16:04:20Z). **Issue #72 is OWNER-BLOCKED**: the
  build-verify fix was fully written twice (run 31953184148 + auto-retry
  31954533349) but the bot's `github.token` cannot push `.github/workflows/*.yml`
  (no `workflows: write`); the auto-retry's verify then FALSE-POSITIVED on PR
  #67's merge (self-confirming the bug #72 exists to fix). Patch + options
  handed to the owner. Obsidian continue failed again on billing (run
  31956999986); maintainer run 31957278010 (in progress) owns the #69 tag.
  main at `c44736f`.

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec competitive with
  JPEG XL / WebP / conventional methods, benchmarked on Kodak.** Research +
  architecture COMPLETE (PR #69 docs). Builder STILL STALLED on billing:
  continue run 31956999986 (15:53Z) failed - verify "No push detected" after
  4 attempts -> "Manual intervention required"; PR #69 head `2377f3cc` (docs
  + Cargo scaffold only, no codec source). Maintainer run 31957278010 (owner
  /oc maintainer on #69, 15:59:20Z) is IN PROGRESS and should tag the owner
  about billing per the #74 policy ("if it happens again, tag me"). Flow:
  Builder (retrying/tagged) -> review -> test -> merge (cap resets to 0/2 at
  00:00Z Aug 17; legal tomorrow).

## In flight

- **Issue #72 (infra fix) - OWNER-BLOCKED, no PR.** The fix (per-PR
  `headRefOid` baseline+verify + force-with-lease guidance) was built in run
  31953184148 but its push was rejected (`github.token` lacks `workflows:
  write`); the Clean working tree step wiped it. Auto-retry run 31954533349
  hit the same wall and its verify false-positived on PR #67's merge - the
  exact bug #72 fixes. **Blocked until the owner either (A) grants the bot
  `workflows: write` or (B) applies the opencode.yml patch directly** (all
  workflow changes on main are owner-pushed: eced6db/d0f6adc/81d84dd/45b1885).
  On `/oc approve-test` (if a PR ever opens): merge, close #72, dispatch
  pages.yml, then `build` on #73.
- **Issue #73 (opencode-review crash on non-PR) - QUEUED behind #72.** Never
  dispatched concurrently with another opencode build.
- **Issue #74 (billing) - CLOSED by the owner 15:04Z** ("try the suggested
  fixes, and if it happens again, tag me on the issue or PR where it
  occurs"). Standing auto-switch policy is OWNER-DEPENDENT: the bot lacks
  `workflows: write`, so the owner must edit workflow files or grant the
  permission.
- **PR #69 (Obsidian) - OPEN, billing-stalled** at head `2377f3cc`, MERGEABLE,
  no codec source, no review/test. Continue 31956999986 failed (billing).
  Maintainer run 31957278010 handling #69; watch for its tag/continue.
- **PR #67 (Meridian) - MERGED `c44736f`, #66 closed, pages deployed**
  (31956858812/31956999681 success). `/meridian/` live. No further action.

## Lab Health & Audit Logs (#70)

- The Auditor owns the daily health summary on #70 (ran 11:30Z; found the
  build-verify false positive -> #72/#73/#74; #74 closed by owner). Watch
  #72 (owner-blocked) and #73 (queued) as the actionable infra threads.

## Board status (#42)

- **FROZEN by the owner's directive** - no picks until Obsidian resolves.
  Candidates parked: Corundum, Tundra, Ravel. No ideate (frozen).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` (reviewer + tester), `deepseek-v4-flash-free`
  (build/fixer/maintainer/ideate/research/architect) unchanged. Billing gate
  (#74) keeps degrading the build agent; the auto-switch to a free fallback
  (hy3-free / nemotron-3-ultra-free / nemotron-3.5-lightning-free /
  laguna-s-2.1-free; all live on the zen endpoint) is blocked by the bot's
  missing `workflows: write` permission (tried, rejected). Next Sunday
  (2026-08-23): weekly model upgradation.

## Next steps

1. **#72: WAIT for the owner** (grant `workflows: write` OR apply the
   opencode.yml patch; patch is in the #72 comment). After owner action,
   re-dispatch `/oc build`; shepherd review -> test -> merge; then dispatch
   #73.
2. **Obsidian: verify maintainer run 31957278010** tagged the owner about
   billing (per 15:04Z policy). If it did not, tag on PR #69. No more blind
   billing retries until the workspace has payment or an owner-side model
   switch.
3. **#73**: dispatch `build` only after #72 merges (never concurrent).
4. **#70**: Auditor owns the daily health summary; watch for anomalies.
5. No board picks until Obsidian resolves (owner's freeze).
6. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the owner grant `workflows: write` (A) or apply the opencode.yml patch
  directly (B)? Either unblocks #72.
- Did maintainer run 31957278010 post the Obsidian billing tag / continue?
- Does Obsidian get a payment method or an owner-side model switch, or does it
  keep degrading on CreditsError?
- Does /meridian/ serve correctly after the deploy?
