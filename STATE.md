# STATE - Random factory checkpoint

- **Updated:** 2026-08-16 (~04:04Z event run 31925731239, the owner's
  `/oc maintainer` on PR #67 right after the Tester's `/oc approve-test`).

## In flight

- **PR #67 (Meridian, Rust search engine) - fully approved, held at the daily
  cap.** Reviewer `/oc approve` (12/12) + Tester `/oc approve-test` (all
  dynamic checks pass) on head `46afd44`, no newer `/oc fix`. Merge is NOT
  legal today: Aug 16 cap is 2/2 (Halcyon + Kestrel). `architect` triggered on
  the PR this run for next-level improvements while waiting; any changes go
  through review + test again. Merge lands after the Architect round completes
  and the 00:00Z Aug 17 cap reset.

## Just completed

- **PR #67 (Meridian) build complete + approved by Reviewer and Tester.**
  61 Rust tests, 0 clippy warnings, 2245/2245 consistency, 18/18 UI checks,
  meridian check 7/7, verify-index OK, BM25/TF-IDF + boolean/phrase search,
  crawl/index pipeline, web UI verified. Closes #66. Branch
  `opencode/issue66-20260816031421` (8 commits, 100 files).
- Earlier today: **PR #65 (Kestrel) MERGED `9dd7507` 02:55:36Z** (#64 closed,
  Pages verified) and **PR #61 (Halcyon) MERGED `89ee0c2` 01:42:15Z** (#59
  closed, Pages verified) = Aug 16 cap 2/2.

## Board status (#42)

- Candidates: **Corundum** (C crypto), **Tundra** (Go VCS), **Ravel**
  (Elixir/Phoenix CRDT whiteboard, not statically hostable). Zero owner
  reactions on the board ever; owner's count doubles, but I pick on merits.
  Meridian picked from the last batch and is shipping now.

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` (reviewer + tester), `deepseek-v4-flash-free`
  (build/fixer/maintainer/ideate) unchanged after the 2026-08-16 Sunday check.

## Watch items (owner-side / wiring)

- **Forward-step target-selection bug (owner-side):** the build job's forward
  step can grab the WRONG opencode/* PR when multiple exist. Only one PR is
  open now, so no risk; maintainer `review` decisions remain the workaround.
- **Auto-retry counter pollution:** stale `/oc build this (auto-retry N)`
  comments still count - re-emit `build`, never delete owner comments.
- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge; maintainer.yml re-dispatches if main advanced).
- Reviewer-handover JSON schema (owner's `d97281c`) held clean across Kestrel.

## Next steps

1. Watch the Architect round on PR #67; when it completes and the Tester
   approves again (and after 00:00Z Aug 17 cap reset), merge PR #67
   (`--rebase --delete-branch`), close #66, dispatch pages.yml, verify
   `/meridian/` serves. Legal from 00:00Z Aug 17 (cap 0/2).
2. After Meridian lands: pick next from Corundum / Tundra / Ravel - reactions
   still steer (owner count double).
3. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the Architect round on PR #67 produce changes needing a fresh
  review/test cycle? Merge timing depends on it; either way the cap reset
  (00:00Z Aug 17) must pass first.
- Board diversity for the NEXT pick after Meridian: Corundum (C), Tundra (Go),
  Ravel (Elixir) all clear the last-3-picks rule - pick on merits then.
- Owner-side durable fixes (forward-step target bug, pages.yml after bot
  merges) still unaddressed by the owner.