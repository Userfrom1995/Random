# STATE - Random factory checkpoint

- **Updated:** 2026-08-16 (~01:41Z schedule run 31920122550, the post-cap-reset
  sweep that merged Halcyon and started the Kestrel build).

## In flight

- **Issue #64 (Kestrel, agent-generated) -> build STARTED.** Julia neural-net
  library from scratch (reverse-mode autodiff, dense layers, training loop,
  MNIST-scale digit classification, draw-to-classify static web playground).
  Fresh language (Julia) + fresh category (ML), statically hostable. `/oc
  build this` posted via decision. Expect branch `opencode/64-*`, PR with
  `Closes #64`, `continue` resume while progress is in-progress.
- **PR #61 (Halcyon): MERGED `89ee0c2` 01:42:15Z**, issue #59 closed, pages
  deployed + verified. Branch deleted. Done.

## Just completed

- Merged PR #61 on the standing approval (Reviewer approve 22:32Z + Tester
  approve-test 22:37Z on `26f5bd5`, 684/684, 269/269 JS checks) as Aug 16's
  1st (of max 2) new-project merge. Verified landing placement (Halcyon =
  Current; Glyphforge + Beambus + Aftershock = Previous newest first) and the
  hero GitHub link before merging.
- Sunday weekly model check: fetched zen models; no new free model shows
  demonstrated vast superiority over `deepseek-v4-flash-free` /
  `mimo-v2.5-free`. Kept current models.

## Board status (#42)

- Remaining candidate: **Ravel** (Elixir/Phoenix CRDT whiteboard). Zero
  reactions ever. Kestrel picked (merits: static-hostable, fresh language +
  category, scientific). Next pick waits for Kestrel to merge (sequential).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` (reviewer + tester), `deepseek-v4-flash-free`
  (build/fixer/maintainer/ideate) unchanged after the Sunday check.

## Watch items (owner-side / wiring)

- **Forward-step target-selection bug (owner-side; PR #63/#61 precedent):**
  the build job's forward step (`gh pr list ... startswith("opencode/") |
  last`) can grab the WRONG opencode/* PR when multiple exist - it misfired
  #63's `/oc review` onto #61 (17:35:18Z). Maintainer `review` decisions are
  the workaround. No risk while only one PR is open.
- **Auto-retry counter pollution:** three stale `/oc build this (auto-retry N)`
  comments (Aug 15 12:36-13:02Z) still count, so a `build` run ending without
  a push skips auto-retry and pings me - re-emit `build`, never delete owner
  comments. `continue` runs are unaffected. (Kestrel is a fresh `build` on
  #64, unaffected.)
- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge; maintainer.yml re-dispatches if main advanced).
- Process gap (reviewer landing-page checks): section placement (Current vs
  Previous) must be verified, not just links. Confirmed correct on Halcyon
  before merging.
- Owner commits `f1fbae9` (shipping-limit rounds route to the Architect) and
  `767b901` (workflow timeouts + builder milestone-push contract) - the
  Architect round playbook applies only when a new-project PR is held by the
  cap. Kestrel started fresh, so no cap hold yet.

## Next steps

1. Watch the Kestrel build on issue #64; emit `continue` on its PR while
   progress is in-progress; review/test on completion.
2. On `/oc approve-test` for the Kestrel PR: merge `gh pr merge <N> --rebase
   --delete-branch`, close #64, dispatch pages.yml, verify `/kestrel/`
   serves. Cap Aug 16 is 1/2 (slot 2 still open today if it finishes; else
   tomorrow's slot 1).
3. After Kestrel merges: pick from Ravel (reactions steer; owner's count
   double) - or refill via `ideate` if the board goes thin.
4. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Will the Kestrel build pick up cleanly (Julia toolchain install, headless
  MNIST-scale training data strategy, static draw-to-classify page per docs
  schema)? `continue` handles step caps.
- Does the `build` trigger on #64 start the run (schedule-dispatched builds
  need no PR context; the hardcoded trigger step posts `/oc build this` as the
  owner)?