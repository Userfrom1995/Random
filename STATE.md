# STATE - Random factory checkpoint

- **Updated:** 2026-08-17 (~19:10Z event run 32058743360, owner `/oc maintainer`
  on PR #76). PR #76's Obsidian build is one step from green: the Builder's
  continue (run 32056096450) COMPLETED and pushed head `16658d50` with the
  rANS rewrite passing static tests; only adaptive-lockstep remains (fix
  diagnosed). This run re-dispatched `/oc continue`.

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec (Kodak-benchmarked,
  vs JPEG XL / WebP).** OPEN, still the priority project. Research + spec +
  architecture committed on PR #76; Builder mid-build on the rANS core. Status:
  `static_roundtrip`, `normalize_exact_sum`, `encoder_invariant_window` pass;
  adaptive-lockstep (rans.rs:501) fails because encoder/decoder update tables
  on reverse vs forward streams - fix is to apply `adapt()` after `put()`/`get()`
  on both sides. The Builder knows the exact change.

## In flight

- **PR #76 (Obsidian) - BUILD RESUMING (`continue` dispatched this run).** Head
  `16658d50`, 64 files changed. `mergeable: CONFLICTING` (no common ancestor
  with main after the squash + main's `86f1328`; rebase/alignment needed before
  review). RED FLAG: `obsidian/target/debug/` build artifacts were committed to
  the branch - need `git rm -r --cached target` + `.gitignore` clean-up. Progress
  file `68-obsidian-lossless-image-codec.md` NOT updated by the Builder yet
  (still "Ready for the Builder", 0/15 build milestones checked).
  On green push + rebase: dispatch `review` -> test -> merge (new-project PR,
  cap 0/2 today, merge legal on approval).

## Issues

- **#68 (Obsidian)** - OPEN, priority project, being built on PR #76.
- **#70 (Lab Health)** - Auditor owns the daily summary on its schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.
- All billing/infra issues (#72/#73/#74/#75) closed; owner's `ae5160b` + pin
  fixed model resolution, `86f1328` fixed the silent-stall timeout.

## Reviewer/Tester/model status

- **Model config (owner's pin):** opencode.json `model:
  opencode/deepseek-v4-flash-free`, `small_model: opencode/mimo-v2.5-free`.
  Workflows pin per-job models (build/maintainer/auditor/ideate on
  deepseek-v4-flash-free; reviewer/test/factory on mimo-v2.5-free). Owner's
  `86f1328` raised all agent steps to 60m (jobs 75m). No CreditsError expected.
- **Reviewer dispatch:** opencode-review.yml triggers ONLY on `/oc review`
  comments - the Maintainer dispatches review via decision.json, it is not
  automatic on push.

## Next steps

1. **Watch the `continue` on PR #76** to completion. The Builder should land
   green effort 0 (adaptive lockstep + roundtrips + fuzz), update the progress
   file, remove `target/` artifacts, and ideally align the branch with main.
2. Once effort 0 is green and the branch is aligned, dispatch `review` on PR #76.
   On `/oc approve` -> test -> merge (new-project cap 0/2 today, merge legal).
3. **#70**: Auditor owns the daily health summary; watch for anomalies.
4. No board picks until Obsidian resolves (owner's freeze).
5. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the Builder land green effort 0 this continue, and does it clean the
  committed `target/` tree + update the progress file?
- Who rebases the branch onto main (no common ancestor) - the Builder in the
  continue, or the Fixer after the Reviewer flags the conflict?
- Will the owner merge Obsidian today (new-project cap 0/2 so far)?
