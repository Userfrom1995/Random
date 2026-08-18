# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~05:44Z, event run on PR #81, run 32103883487). PR #81 MERGED (commit a94186f) - the audit #72 factory round is now live on main. Pages re-deployed manually. Lab otherwise idle.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** CLOSED (by merge of PR #80). M2/M3 (context/predictor tuning toward WebP 9.61 / optipng PNG 13.05) remain as follow-on optimization milestones; no active build right now. Checklist 10 shipped on main (first Obsidian Kodak row: 27.8226 mean bpp, bit-exact). Owner's standing directive: iterate until Obsidian beats the other codecs on Kodak (lossless + performance).

## Audit #72 - RESOLVED (PR #81 merged 2026-08-18T05:43:02Z)

- **Audit title:** "[Audit] Issue #71 deleted and its root-cause fix never landed: build-verify false positive still live on main." CLOSED 2026-08-17T11:47Z. Its META critique ("fixes reported done, never landed") was TRUE; this time the factory round genuinely landed.
- **PR #81 "[Infra] Factory update for #72"** - MERGED via rebase at 05:43:02Z (merge commit `a94186fd4755229f02fa3e31d8da0e0b81410f0a`), branch `opencode/factory-72-build-verify-and-73-review-crash` deleted. Carried both unlanded fixes:
  - `opencode-review.yml`: non-PR `/oc review` no longer crashes (resolves linked PR via `opencode/issue<N>-*`, else maintenance note). #73 closed.
  - `opencode.yml`: fix-trigger relaxed to `startsWith('/oc fix')`; general-command guard updated. Reviewer/Tester `/oc fix: ...` findings re-trigger the Fixer.
  - `builder.md` / `fixer.md`: `--force-with-lease` after rebase.
- **Loop outcome:** Reviewer `/oc approve` (05:38:15Z) -> Tester `/oc approve-test` (05:41:52Z) -> Maintainer merged on approval (no newer `/oc fix` findings). Quality gate ran clean end to end.
- **pages.yml:** did not auto-fire on the merge push; manually triggered run 32104019787 (in progress) to keep the live site synced.

## In flight

- None. No opencode build / fix / factory / review / test runs in flight.
- pages.yml run 32104019787 in progress (re-deploy after merge).

## Issues

- **#68 (Obsidian umbrella)** - CLOSED via PR #80 merge. M2/M3 follow-ons unscoped.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian M2/M3 scopes.
- **#71** - DELETED (HTTP 410). Root cause (build-verify) fixed on main. Propose a hard "do not delete audit issues" rule in AGENTS.md / Auditor runbook.
- **#72 (audit issue)** - CLOSED; meta critique satisfied by merged PR #81.
- **#73 (review crash on non-PR)** - CLOSED; fix landed via merged PR #81.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. All workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2.5-free`. No CreditsError expected.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Close-the-loop live confirmation:** watch the next real non-PR `/oc review` (should post a maintenance note, not crash) and the next real `/oc fix: ...` finding (should re-trigger the Fixer). The two audit test cases are now structurally covered.
2. **Resume Obsidian optimization (M2/M3):** self-correcting weighted predictor / context tuning toward WebP 9.61 / optipng PNG 13.05. Open a new issue when ready and route research -> architect -> build.
3. **Brainstorm board (#42):** once M2/M3 scoped, the Ideator can resume.
4. **Process guard:** codify "never close audit/infra issues until the root-cause fix is merged and verified on main" in AGENTS.md / the Auditor runbook (lesson from #71/#73).

## Open questions

- Does a live non-PR `/oc review` and a live `/oc fix: ...` finding both flow through cleanly now that #81 is on main? Final confirmation of the audit's two test cases.
- After M1 on main, how far does Obsidian's Kodak mean bpp (27.82) move toward/under WebP 9.61 / optipng PNG 13.05? M2/M3 are the lever.
- Should #71's deletion be codified as a "do not delete audit issues" hard rule in AGENTS.md / the Auditor runbook?
