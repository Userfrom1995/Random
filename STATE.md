# STATE - Random factory checkpoint

- **Updated:** 2026-08-16 (~14:50Z event run 31953646103, owner comment on
  PR #69 at 14:45:33Z). **Owner overruled the Obsidian hold: "Why has work
  stopped on this? Resume it... the 2/day limit caps merges only, not work."**
  Obsidian `continue` DISPATCHED this run; #72 infra build in flight; #74
  billing auto-switch policy adopted (owner-directed). main at `d0f6adcd`
  (owner-pushed auditor PAT-forwarding wiring 14:48:14Z).

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec competitive with
  JPEG XL / WebP / conventional methods, benchmarked on Kodak.** Research +
  architecture COMPLETE (PR #69 docs). Builder round pushed `2377f3cc`
  (docs + Cargo scaffold ONLY, no codec `.rs` source; billing error #74
  degraded the round, effort 0 NOT implemented). **RESUMED this run:**
  `continue` dispatched per the owner's explicit directive. Builder re-implements
  effort 0, pushes (rebase onto `d0f6adcd` first). Flow: Researcher (done) ->
  Architect (done) -> Builder (resuming) -> review -> test -> merge. Owner's
  freeze on new board picks until Obsidian resolves stays in place.

## In flight

- **PR #69 (Obsidian) - `continue` DISPATCHED this run.** Head `2377f3cc`,
  CLEAN, MERGEABLE. Owner ordered the resume (14:45:33Z). The #72 infra build
  is concurrently in flight; masking risk acknowledged and bounded (review
  gate catches a falsely-passing verify). Watch for the Builder's push, then
  review -> test -> merge (Obsidian merge legal from 00:00Z Aug 17, cap 0/2).
- **Issue #72 (infra fix) BUILD ACTIVE - run 31953184148** (started
  14:36:11Z, build job in_progress, no `opencode/72-*` branch/PR yet).
  Triggered by my 14:23Z run (`/oc build this` posted 14:36:08Z). Scope:
  build-verify scoped to the target PR head (mirror fix path 555-556) +
  force-with-lease guidance. Lab-improvement, cap-exempt, extra-hard review
  expected. On `/oc approve-test`: merge, close #72, dispatch pages.yml, THEN
  dispatch `build` on #73.
- **Issue #73 (opencode-review crash on non-PR targets) - QUEUED behind #72.**
  Never dispatched concurrently with another opencode build. Acknowledge
  comment already posted 14:36Z.
- **Issue #74 (opencode.ai billing) - OWNER-LEVEL + auto-switch policy.**
  Owner (14:43:46Z): "Try again. If it still fails, try switching to another
  model that works with the free tier... automatically try switching... wait
  and retry... if none work, notify me." ADOPTED as standing policy: on the
  payment error, retry; then switch the builder model in opencode.yml to a
  free fallback (hy3-free / nemotron-3-ultra-free / nemotron-3.5-lightning-free
  / laguna-s-2.1-free; all confirmed on the zen models endpoint); then notify.
  Pinged #74 this run confirming the plan. Retry in progress (Obsidian resume).
- **PR #67 (Meridian) - Level 3 COMPLETE, fully re-approved, MERGE-READY.**
  Head `9328368`, CLEAN, MERGEABLE. Reviewer approve 10:37:29Z + Tester
  approve-test 10:44:34Z, no newer `/oc fix`. **Cap-held (Halcyon + Kestrel =
  2/2 today). Legal from 00:00Z Aug 17; first run after the reset merges it.**
  Owner confirmed the cap is merge-only; #67 stays prepared.

## Lab Health & Audit Logs (#70)

- The Auditor owns the daily health summary on #70 (afternoon run 12:33Z,
  opened #72/#73/#74). This run the owner pushed `d0f6adcd` ("auditor: Add
  PAT-backed decision forwarding", 14:48:14Z) directly to main - watch whether
  it affects auditor behavior; the #72 fix + extra-hard review still gate the
  build path.

## Board status (#42)

- **FROZEN by the owner's directive** - no picks until Obsidian resolves.
  Candidates parked: Corundum, Tundra, Ravel. No ideate (frozen).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` (reviewer + tester), `deepseek-v4-flash-free`
  (build/fixer/maintainer/ideate/research/architect) unchanged after the
  2026-08-16 Sunday check. Builder model at risk from #74; free fallbacks
  identified. Next Sunday (2026-08-23): weekly model upgradation.

## Next steps

1. **Watch the Obsidian resume** (continue posted on PR #69): shepherd the
   Builder through effort 0; if billing degrades the round, switch the builder
   model (auto-switch policy) and retrigger. Review -> test -> merge when it
   passes (cap is 0/2 after 00:00Z Aug 17, so legal tomorrow).
2. **Watch the #72 build** (31953184148): on `/oc approve-test`, merge, close
   #72, dispatch pages.yml, then dispatch `build` on #73.
3. **PR #67**: merge at the first run after 00:00Z Aug 17 (`gh pr merge 67
   --rebase --delete-branch`), close #66, dispatch pages.yml, verify
   `/meridian/` serves.
4. **#74**: retry happening now; auto-switch models on failure; re-ping the
   owner if all free fallbacks fail.
5. **#70**: Auditor owns the daily health summary; watch for anomalies.
6. No board picks until Obsidian resolves (owner's freeze).
7. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the Obsidian `continue` push cleanly (rebase onto `d0f6adcd`, no
  non-fast-forward rejection) and finally land effort 0, or does billing (#74)
  degrade it again -> model-switch path?
- Does the #72 build (31953184148) open its PR and survive the extra-hard lab
  review, while the Obsidian round moves the issue68 branch concurrently?
- PR #67 merge at 00:00Z Aug 17: head `9328368` unchanged, no newer `/oc fix`?
  Expected yes.
- Does the owner's `d0f6adcd` auditor wiring (PAT-backed decision forwarding)
  change auditor behavior in a way the #72 fix must account for?
- Obsidian's PR is a new-project PR - subject to the 2/day merge cap when it
  ships; merge-legal from 00:00Z Aug 17.