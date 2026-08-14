# STATE — Random factory checkpoint

- **Updated:** 2026-08-14 (event run 31789476416 — owner `/oc maintainer` on board #42)
- **Gambit BUILDING (issue #51 → PR #52):** build run 31789291626 in_progress; branch `opencode/issue51-20260814094408`, head `e9772bb6` (scaffold), progress in-progress. No review yet (correct — build incomplete).
- **Pages refresh dispatched** (run 31789757302): bot merges don't trigger `on: push` deploys (GITHUB_TOKEN), so the live site was stale at 9189600 and lacked `/granite/`. Dispatch rebuilds from current main + stages all PR previews.

## In flight

- **Gambit — issue #51 / PR #52** — OPEN, `agent-generated`, branch `opencode/issue51-20260814094408`, head `e9772bb6`, MERGEABLE. Builder actively working (scaffold done; bitboard core next). Next: once progress flips `Status: complete`, emit `review` on PR #52 with the head sha.

## Just completed

- **Pages deploy dispatched** (run 31789757302, queued 09:50:33Z) to refresh the stale site after the 09:25/09:27 bot merges (GITHUB_TOKEN pushes don't trigger `on: push` workflows). Held runs on PR #52 (preview + pr-trigger) will clear via the next schedule sweep or the build's own approve steps.

## Board status (#42)

- Fresh Ideator batch (09:46:17Z): Aftershock (Rust/simulation), Beambus (Zig/game), Glyphforge (Kotlin/tooling) — all pass dedup + diversity. No owner reactions yet. **Next pick held until Gambit clears review.** Owner can request a parallel build (offered in the board comment).

## Reviewer model status

- `opencode/mimo-v2.5-free` proven (two clean rounds, both `/oc approve`). Weekly Sunday upgradation check still pending (not a Sunday today).

## Next steps

1. Confirm the dispatched pages deploy (31789757302) lands and serves `/`, `/docs/`, `/granite/`, plus the PR #52 preview.
2. Watch the Gambit build; emit `review` on PR #52 once its progress file is `Status: complete`.
3. Pick the next project from the fresh board batch after Gambit clears review (owner reactions may steer it).
4. Held runs on PR #52 (pages preview + pr-trigger) clear via the next PR-less schedule sweep or the build's own stable-head approval.

## Open questions

- Durable Pages fix for bot merges: owner adds a schedule trigger to `pages.yml`, or the merge step dispatches a deploy after merging? (Flagged in the board comment; recurs on every bot merge until changed.)
- Which of Aftershock/Beambus/Glyphforge for the next pick (reactions pending; my lean: Aftershock or Beambus)?
- Reviewer `/oc approve` prefix discipline on the Gambit round.

This file is rewritten every run — it is the instant catch-up for any new Maintainer instance. Historical detail lives in `logs/`.