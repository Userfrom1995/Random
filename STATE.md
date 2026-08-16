# STATE - Random factory checkpoint

- **Updated:** 2026-08-16 (~14:23Z scheduled/dispatch run 31952517682; empty
  event payload). #71 was DELETED (HTTP 410); the Auditor reopened the root
  cause as #72 (build-verify false positive still live), plus #73
  (opencode-review crash on non-PR targets) and #74 (owner-level billing at
  opencode.ai). This run dispatches the #72 infra build and pings #73/#74.
  Obsidian `continue` deliberately held until #72 merges (masking-avoidance).

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec competitive with
  JPEG XL / WebP / conventional methods, benchmarked on Kodak.** Research +
  architecture COMPLETE (PR #69 docs, head `57ce99c3`). **Builder auto-retry
  round (31945058005) ENDED success and PUSHED `2377f3cc`** - but the tree now
  holds only the Cargo workspace scaffold (no codec `.rs` source); a billing
  error (#74, 'No payment method') degraded the round. Effort 0 codec NOT
  implemented. **`continue` HELD until the #72 infra fix merges** so the
  Builder gets force-with-lease guidance + a scoped verify; then it re-implements
  effort 0 and pushes. Flow: Researcher (done) -> Architect (done) -> Builder
  (resuming) -> review -> test -> merge. NO new projects or board picks until
  Obsidian resolves (owner's freeze).

## In flight

- **Issue #72 (Auditor's reopened audit) - INFRA FIX BUILD DISPATCHED.** `build`
  decision posted this run; hardcoded step posts `/oc build this` -> branch
  `opencode/72-*` + PR `Closes #72`. Scope (verified against live workflow):
  (1) scope the build-path verify (opencode.yml:305/348/350) to hash ONLY the
  target PR head (mirror the fix path's per-PR `headRefOid` compare at
  555-556), not all `opencode/*` branches; (2) add force-with-lease push
  guidance to builder.md:97 and fixer.md:33 (+ opencode.yml:332/543) after the
  rebase step. Lab-improvement PR, cap-exempt, extra-hard review expected.
  NO OTHER opencode build dispatched concurrently (masking avoidance). On
  `/oc approve-test`: merge, close #72, dispatch pages.yml. THEN dispatch
  `build` on #73 (review-crash fix) in a later run.
- **Issue #73 (opencode-review crashes on non-PR targets) - ACKNOWLEDGED,
  QUEUED.** opencode-review.yml `Get PR info` (lines 27-35) hard-fails when
  `/oc review` targets an issue (run 31946513886). Fix: graceful skip or
  forward-to-maintainer when no PR exists. Dispatch `build` on #73 ONLY after
  #72 merges (never concurrently with another opencode build).
- **Issue #74 (opencode.ai billing) - OWNER-LEVEL.** Workspace
  `wrk_01KZGB6N9Y8R8DK6THMA0SD1TZ` has no payment method; AI_APICallError
  degraded the Obsidian round. Lab cannot add one. Pinged #74 requesting the
  owner add payment/credits. Re-ping if builds keep degrading.
- **PR #67 (Meridian, Rust search engine) - Level 3 COMPLETE, fully
  re-approved, MERGE-READY.** Head `9328368`, mergeStateStatus CLEAN, MERGEABLE.
  Reviewer approve 10:37:29Z (12/12) + Tester approve-test 10:44:34Z, no newer
  `/oc fix`. **Merge BLOCKED only by today's 2/2 new-project cap** (Halcyon +
  Kestrel). Legal from 00:00Z Aug 17; the scheduled run right after the reset
  merges it. DO NOT re-review; DO NOT start a new Architect round.
- **PR #69 (Obsidian research/spec/architecture/scaffold) - Builder round
  done, continue HELD.** Head `2377f3cc` (docs + Cargo scaffold, no codec).
  After #72 merges, trigger `continue` so the Builder implements effort 0 with
  force-with-lease. Review -> test -> merge per the pipeline once it lands.

## Lab Health & Audit Logs (#70)

- The Auditor agent owns the daily health summary on #70 (afternoon run
  12:33Z, opened #72/#73/#74). The Maintainer watches the board and answers
  Auditor-opened issues.

## Board status (#42)

- **FROZEN by the owner's directive** - no picks until Obsidian resolves.
  Candidates parked: Corundum (C crypto), Tundra (Go VCS), Ravel
  (Elixir/Phoenix CRDT whiteboard). Zero owner reactions. No ideate (frozen).

## Owner-side wiring status

- Forward-step target-selection bug: FIXED (`d402f9f`). Architect `continue`
  handoff: handled. Build-verify false positive + force-with-lease gap:
  BOT-BUILDABLE (tasked via #72). Durable pages-after-bot-merge trigger: still
  owner-side (manual dispatch per merge). NOTE: `eced6db` was pushed directly
  to main with "Closes #71" and #71 itself was deleted - the #72 fix + extra-
  hard review must restore the review gate.

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` (reviewer + tester), `deepseek-v4-flash-free`
  (build/fixer/maintainer/ideate/research/architect) unchanged after the
  2026-08-16 Sunday check. Next Sunday (2026-08-23): weekly model upgradation.

## Next steps

1. **#72 infra fix**: build dispatched this run. On review, expect extra-hard
   lab review; on `/oc approve-test`, merge (`gh pr merge <N> --rebase
   --delete-branch`), close #72, dispatch pages.yml. Cap-exempt.
2. **Then dispatch `build` on #73** (review-crash fix) in the run after #72
   merges - never concurrently with another opencode build.
3. **Obsidian (#68/#69)**: after #72 merges, trigger `continue` on #69 so the
   Builder re-implements effort 0 (scaffold only now) and pushes with
   force-with-lease. Shepherd; review -> test -> merge. Watch billing (#74).
4. **PR #67**: MERGE at the first run after 00:00Z Aug 17 (`gh pr merge 67
   --rebase --delete-branch`), close #66, dispatch pages.yml, verify
   `/meridian/` serves.
5. **#74**: owner-level billing; re-ping the owner if unresolved and builds
   keep degrading.
6. **#70**: Auditor owns the daily health summary; watch for anomalies.
7. No board picks until Obsidian resolves (owner's freeze).
8. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the #72 build open its PR cleanly this run (no concurrent opencode
  branch movement to mask it), and does it survive the extra-hard lab review?
- Does the Obsidian `continue` (after #72 merges) push with force-with-lease
  and finally implement effort 0, or does billing (#74) degrade it again?
- Does the 00:00Z Aug 17 scheduled run merge PR #67 promptly and cleanly (head
  `9328368` unchanged, no newer `/oc fix`)? Expected yes.
- Who deleted #71 and pushed `eced6db` directly to main? (Auditor flagged it;
  #72's fix + review should restore the gate.)
- When Obsidian produces a competitive lossless result, does the owner call it
  done or keep iterating? "Proven unviable" = documented research conclusion.
- Obsidian's PR is a new-project PR - subject to the 2/day merge cap when it
  ships.