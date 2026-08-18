# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~05:22Z, `/oc maintainer` event run on PR #80, run
  32102083809). PR #80 MERGED, issue #68 CLOSED, factory round for the
  fix-trigger-guard relaxation dispatched. Lab idle.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP,
  Kodak-benchmarked).** CLOSED (by merge of PR #80 at 05:22Z). The umbrella is
  done for M1; M2/M3 remain as follow-on optimization milestones.
- **Checklist 10 shipped on main** (first Obsidian Kodak row: 27.8226 mean bpp,
  bit-exact). Reference baseline within ~0.5% of WangXuan95 2024 (JXL 8.7062, WebP
  9.6130, JLS 9.7113, J2K 9.5762, PNG ~13.05).
- Owner's standing directive: iterate until Obsidian beats the other codecs on
  Kodak (lossless + performance). M1 shipped; M2/M3 are the optimization milestones.

## M1 - MERGED (PR #80)

- **PR #80 MERGED** at 05:21:34Z: head `967ba1b3` -> main `d646dfa39` via
  `gh pr merge 80 --rebase --delete-branch`. Branch `opencode/issue68-20260818034514`
  deleted. Merge commit: `d646dfa39e7fd32b1ca9b126581b32fa60d90dc3`.
- Gate satisfied: Reviewer approved (run 32101635901) resolving all 3 findings;
  Tester approved (`/oc approve-test`, run 32101889905, 47/47 pass) with no newer
  `/oc fix` findings after it. Obsidian continuation, no shipping cap applied.
- Issue #68 CLOSED (05:22:01Z). pages.yml re-deployed (run 32102615491).

## Factory round - IN FLIGHT (fix-trigger-guard relaxation)

- Dispatched this run: `factory` on issue #72 (decision.json). Goal: make
  opencode.yml's fix matcher re-trigger the Fixer when Reviewer/Tester finding
  comments do not match the exact `/oc fix` string. Safe to run - no build/
  review/test in flight after the merge.
- Prior factory round (M1 build-loop hardening, PR #79) already merged at 03:42Z.

## In flight

- **Factory fix-trigger-guard round** (issue #72) - the only active work.
- This maintainer run: 32102083809 (completed; merge done, comment + memory pending
  hardcoded commit).

## Issues

- **#68 (Obsidian umbrella)** - CLOSED via PR #80 merge.
- **#77 (checklist 10)** - CLOSED via PR #78.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves (M1 done; can reopen
  for M2/M3 idea generation).
- **#72 (build-verify guard gap)** - CLOSED; the fix-trigger-guard relaxation is the
  remaining QUEUED factory item, now dispatched.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model:
  opencode/mimo-v2.5-free`. All workflow `.yml` agent steps pinned to `opencode/hy3-free`.
  Reviewer/test/factory on mimo-v2.5-free. No CreditsError expected.

## Next steps

1. **Watch the factory fix-trigger-guard round** (issue #72): review -> test -> merge
   once the Factory Engineer lands it.
2. **Resume Obsidian optimization (M2/M3):** self-correcting weighted predictor /
   context tuning toward WebP 9.61 / optipng PNG 13.05. Open a new issue when ready
   and route research -> architect -> build, or continue directly on the codec.
3. **Brainstorm board (#42):** once M2/M3 is scoped, the Ideator can resume generating
   candidates (lab was idle, good window).

## Open questions

- After M1 on main, how far does Obsidian's Kodak mean bpp (27.82) move toward/under
  WebP 9.61 / optipng PNG 13.05? M2/M3 are the lever.
- Does the factory fix-trigger-guard relaxation cleanly match Reviewer/Tester finding
  comments without false negatives? Track in the factory round.
- PR #80 body still opens with stale "decode still desyncs" text; harmless (merged).
