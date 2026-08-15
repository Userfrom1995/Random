# STATE - Random factory checkpoint

- **Updated:** 2026-08-15 (~17:32Z issues-event run 31898418708, the owner opened
  issue #62 "Fix README and website" - Glyphforge is listed under Previous on main
  while Beambus still claims Current; a `build` was routed for the landing fix).

## In flight

- **Issue #62 (README + website landing fix, NEW):** owner finding verified on
  main: `README.md` "Current Project" = Beambus (line 47), `index.html` "Live now"
  card = Beambus (line 102), while Glyphforge (merged 01:43:39Z, AFTER Beambus)
  sits as the first "Previous" entry in both. Root cause: Glyphforge's build
  commit `65f7f9df40` only ADDED it to Previous, never promoted it. **`build`
  routed** - Builder lands branch `opencode/62-*`, promotes Glyphforge to Current
  (with links + "Live now" tag) and graduates Beambus into Previous (top,
  newest-first) in BOTH `README.md` and `index.html`, PR with `Closes #62`.
  Landing fix, NOT a new project, so NOT shipping-cap constrained. Review -> test
  -> merge -> close #62 -> dispatch pages.yml -> verify `/` placement.
- **Halcyon (issue #59 -> PR #61):** **V3 BUILD ACTIVE** - opencode run
  31897133922, build job in_progress since 17:01:25Z, head still `9a90ebd` (the
  Architect's v3 design). Builder implementing M17-21 (top-level defs + module
  system with `--lib`, record types, type classes with dictionary passing, Char +
  string ops, VM profiler + optimizer expansion + JS/playground/docs sync). No
  milestone push visible yet. The owner's 17:24:04Z "/oc maintainer make sure doc
  is also properly done." is owned by parallel maintainer run 31898196503 (and
  opencode run 31898196561 pending) - I did NOT double-trigger PR #61 this run.
  - Approvals on `b1897b1` (16:36Z/16:41Z) are STALE for the v3 head; fresh
    review + test required after M17-21 land.
  - **Daily shipping cap Aug 15: 2/2 REACHED** (Beambus + Glyphforge). Halcyon
    merge legal after 00:00Z Aug 16.

## Just completed

- Routed `build` on issue #62 for the root landing fix (Glyphforge promotion).

## Board status (#42)

- Candidates remaining: **Ravel** (Elixir/Phoenix CRDT whiteboard), **Kestrel**
  (Julia NN + draw-to-classify). Zero reactions. Next pick waits for Halcyon to
  merge (sequential policy).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` validated (reviewer + tester); Sunday weekly
  upgradation check due 2026-08-16.

## Watch items (owner-side / wiring)

- **Landing-page placement (recurring gap):** checks must verify section
  placement (Current vs Previous), not just links/200s. Third recurrence
  (PR #61 branch 15:36Z, Glyphforge-on-main root cause, pattern itself).
- **Auto-retry counter pollution:** the three stale `/oc build this (auto-retry N)`
  comments from the first build round still count, so a build run ending without a
  push skips auto-retry and pings me. Handle by re-emitting; do not delete owner
  comments.
- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge).
- `opencode-review-trigger.yml` still absent on main (Maintainer `review`
  decision remains the only bot-PR review path).
- Owner commit `f1fbae9` - shipping-limit rounds route to the Architect.

## Next steps

1. Watch the #62 build (landing fix, Glyphforge -> Current, Beambus -> Previous);
   `continue` as needed, then review/test, merge (not cap-bound), close #62,
   dispatch pages.yml.
2. Watch the Halcyon v3 build (31897133922); `continue` per the milestone-push
   contract until M21 `Status: complete`.
3. After M21: route the fresh head to the Reviewer then Tester (stale on
   `b1897b1`).
4. On the next `/oc approve-test` for PR #61 **after 00:00Z Aug 16**: merge PR #61
   (`gh pr merge 61 --rebase --delete-branch`), close #59, dispatch pages.yml,
   verify `/halcyon/docs/`. That is Aug 16's 1st (of max 2) new-project merge.
5. After Halcyon merges: pick from Ravel/Kestrel (reactions steer; owner's count
   double).
6. Sunday weekly model upgradation check on 2026-08-16.

## Open questions

- Does the #62 Builder land the two-file promotion/graduation cleanly, and does
  its PR merge before or after Halcyon's (both touch the same root sections)?
- Can the Builder land M17-21 milestone-by-milestone within the 25-min caps
  (several `continue` rounds likely)?
- Will the v3 round complete before or after 00:00Z Aug 16? Merge is legal from
  the reset regardless, but requires fresh approvals on whatever head the cycle
  ends on.
- Did the parallel maintainer run (31898196503) handle the owner's doc-check on
  PR #61 cleanly?