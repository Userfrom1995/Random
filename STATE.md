# STATE - Random factory checkpoint

- **Updated:** 2026-08-17 (~13:10Z event run 32032824329, triggered by the
  owner's second `/oc maintainer` ping on PR #76). The Obsidian research +
  spec + architecture phases are complete on PR #76, but the Builder has never
  run: the `/oc build this` opencode run (32029914699) was cancelled before any
  job started, and my two prior maintainer runs (12:32 event, 12:52 schedule)
  both wrote empty decision lists and posted no trigger. **This run re-dispatches
  the build on PR #76.**

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec (Kodak-benchmarked,
  vs JPEG XL / WebP).** OPEN, still the priority project. Research (SOTA
  survey), algorithmic spec, benchmark methodology, and the Architect's
  blueprint are all committed on PR #76 head `b25f87a`
  (`opencode/issue68-20260817120528`). The codec source from the earlier
  branch (`opencode/issue68-20260816082105` @ `05a9f4ab`) was orphaned by the
  owner's squash; the new branch is unrelated-history and the builder prompt
  carries the rebuild guidance. **This run: build dispatched on PR #76.**

## In flight

- **PR #76 (Obsidian) - BUILD DISPATCHED this run.** Research/spec/architect
  done; Builder should scaffold the Cargo workspace, implement rANS + effort 0
  end-to-end, and push per the 15-step checklist in the progress file. Watch
  for a `builder:` commit push. On push: auto-reviewer -> shepherd review ->
  test -> merge (new-project PR, cap 0/2 today, merge legal on approval).

## Issues

- **#68 (Obsidian)** - OPEN, priority project, being built on PR #76.
- **#70 (Lab Health)** - Auditor owns the daily summary on its schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves.
- All billing/infra issues (#72/#73/#74/#75) closed; owner's `ae5160b` + pin
  fixed the model resolution at config layer.

## Reviewer/Tester/model status

- **Model config (owner's pin):** opencode.json `model:
  opencode/deepseek-v4-flash-free`, `small_model: opencode/mimo-v2.5-free`.
  Workflows pin per-job models (build/maintainer/auditor/ideate on
  deepseek-v4-flash-free; reviewer/test/factory on mimo-v2.5-free). No
  CreditsError class expected.

## Next steps

1. **Watch PR #76**: the dispatched build should scaffold + implement and push.
   Shepherd review -> test -> merge (cap 0/2 today).
2. If the opencode build run cancels a SECOND time before any job starts,
   dispatch `factory` to investigate the concurrency/approval race instead of
   re-dispatching blindly.
3. **#70**: Auditor owns the daily health summary; watch for anomalies.
4. No board picks until Obsidian resolves (owner's freeze).
5. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the build run survive this time (the prior one cancelled with zero
  jobs before starting)?
- Does the Builder land the Cargo scaffold + rANS + effort 0 on PR #76 and
  pass review/test this time?
