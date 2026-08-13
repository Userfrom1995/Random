# STATE — Random factory checkpoint

- **Updated:** 2026-08-13 (schedule run 31732339923)
- **Pipeline:** Orrery SHIPPED (PR #46 merged, #45 closed). New builds started this
  run: Granite (#47) and the pages.yml staging fix (#48).

## In flight

- **Granite (#47)** — picked from the board this run; `agent-generated` issue opened;
  `/oc build this` posted. Builder will open a branch + PR (`Closes #47`). Watch for the
  PR push; when its progress file reads `Status: complete`, emit `review` with the PR
  head (no auto-review trigger exists on main).
- **Pages.yml staging fix (#48)** — live Pages regression from `ef28dd3`: every project
  subpath 404s (`/cadence/ /orrery/ /rush/ /shaftcast/`) because `[ ! "$dir" == .* ]`
  glob-expands to multiple dotfiles and errors ("too many arguments"), skipping all dirs
  in both the deploy and the PR-preview staging loops. Fix issue written with the exact
  line (both occurrences) + POSIX-safe replacement `[ "${dir#.}" = "$dir" ]`, verified
  locally. Same handling: watch PR → `review` when complete → merge → verify URLs 200.
- **Orrery pages tail RESOLVED (reclassified):** there is no missing `/orrery/` block —
  the ef28dd3 auto-stage loop makes per-project blocks unnecessary; `/orrery/` is down
  purely because of the #48 bug. No owner staging action needed.

## Board status

- #42: **Granite picked → #47**. **Gambit** (C++ chess) remains, unreacted.

## Next steps

1. Wake on the upcoming bot PR pushes (#47, #48); when each progress file is
   `Status: complete`, emit `review` with the PR head.
2. On merge of #48: verify `/cadence/ /orrery/ /rush/ /shaftcast/` return 200 and PR
   previews stage app dirs.
3. Next board pick: watch reactions on Gambit (only candidate left); if the board
   thins, dispatch the Ideator for a fresh batch.
4. Keep watching the reviewer's `/oc approve` format discipline; if prose-without-
   prefix recurs, propose the factory PR (reviewer-prompt tweak or handover fallback).

## Open questions

- Will the Granite build and the pages-fix PR both land clean, and will the reviewer
  keep the fix scoped?
- Owner preference among remaining board candidates (now only Gambit), and whether the
  owner wants to keep the two-builds-at-once cadence.

This file is rewritten every run — it is the instant catch-up for any new
Maintainer instance. Historical detail lives in `logs/`.
