# STATE - Random factory checkpoint

- **Updated:** 2026-08-17 (~19:15Z event run 32059328470, owner `/oc maintainer`
  on PR #76). PR #76's Obsidian build is one step from green: the Builder's
  latest continue (run 32059047889) was RECON-ONLY (oriented, ran cargo test,
  made no code changes, pushed nothing - head still `16658d50`). This run
  re-dispatched `/oc continue` to land the diagnosed adaptive-lockstep fix.

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec (Kodak-benchmarked,
  vs JPEG XL / WebP).** OPEN, still the priority project. Research + spec +
  architecture committed on PR #76; Builder mid-build on the rANS core. Status:
  `static_roundtrip`, `normalize_exact_sum`, `encoder_invariant_window` pass;
  3 failures remain - `adaptive_roundtrip_lockstep` + `renorm_pressure`
  (rans.rs:501, adaptive-lockstep table divergence; fix = apply `adapt()` after
  `put()`/`get()` on both sides) and `static_tables_model_size_guard`
  (encoder.rs). The Builder knows the exact changes.

## In flight

- **PR #76 (Obsidian) - BUILD RESUMING (`continue` dispatched this run).** Head
  `16658d50`, 64 files changed. `mergeable: CONFLICTING` (no common ancestor
  with main after the squash + main's `86f1328`; rebase/alignment needed before
  review). RED FLAGS: (1) `obsidian/target/debug/` build artifacts committed to
  the branch - need `git rm -r --cached target` + `.gitignore`; (2) progress
  file `68-obsidian-lossless-image-codec.md` still un-updated by the Builder;
  (3) the build-verify baseline captures main's SHA on comment-triggered runs,
  so recon-only sessions false-positive "pushed" and skip the auto-retry (log
  this for a factory round once the build lands). On a real green push + rebase:
  dispatch `review` -> test -> merge (new-project PR, cap 0/2 today, merge legal
  on approval).

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
   green effort 0 (adaptive lockstep + model-size guard + roundtrips + fuzz),
   update the progress file, remove `target/` artifacts, and ideally align the
   branch with main.
2. Once effort 0 is green and the branch is aligned, dispatch `review` on PR #76.
   On `/oc approve` -> test -> merge (new-project cap 0/2 today, merge legal).
3. **Route `factory`** for the build-verify baseline false positive (capture
   baseline on the branch, not main) as soon as NO opencode build is in flight.
4. **#70**: Auditor owns the daily health summary; watch for anomalies.
5. No board picks until Obsidian resolves (owner's freeze).
6. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the Builder land green effort 0 on this resume, or recon-only a second
  consecutive time (-> route a factory/model round instead of blind re-dispatch)?
- Does the Builder clean the committed `target/` tree + update the progress file?
- Who rebases the branch onto main (no common ancestor) - the Builder in the
  continue, or the Fixer after the Reviewer flags the conflict?
- Will the owner merge Obsidian today (new-project cap 0/2 so far)?