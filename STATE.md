# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~06:10Z, event run on issue #42, run 32104600383). Owner directive on #42: Obsidian (#68) is NOT finished - resume the full research->architect->build->test->optimize loop until it beats JPEG XL / WebP / PNG on Kodak. #68 REOPENED. README + landing page updates (missed in PR #78) to be fixed in the next Obsidian PR. PR branches to be preserved after merge (no --delete-branch).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it. Incremental improvement PRs may merge as the loop runs; only the *project* is "done" when the codecs are beaten.
- **Never delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. A Factory Engineer PR will harden this into maintainer.md so it survives across runs. (PR #78's branch is already gone and cannot be recovered.)
- **Website + README must track the active project.** PR #78 missed these. The next Obsidian PR must add Obsidian to `README.md` (Current Project) and promote it to Current on `index.html` (currently still Meridian).

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED 2026-08-18 (was closed by PR #78 mistakenly). Status: M1 shipped (PR #78, merged 2026-08-18T00:03:16Z) - benchmark harness + reference baseline + first Kodak row: Obsidian v1 = 27.8226 mean bpp (bit-exact), vs WebP 9.6130 / optipng PNG 13.0518 / JPEG XL 8.7062. NOT competitive yet.
- **Next iteration (M2+):** Researcher spike dispatched this run (decision: research on #68) to design how to close the gap - better spatial/context predictors, context-adaptive entropy coding (rANS/ANS), color decorrelation, LZP, learned predictors. Target: get under WebP 9.61 / optipng PNG 13.05 / JPEG XL 8.71 on Kodak. Each milestone recorded as a new trend row.
- Until target met: no board picks, no new projects.

## Audit #72 - RESOLVED (PR #81 merged 2026-08-18T05:43:02Z)

- `opencode-review.yml`: non-PR `/oc review` no longer crashes. `opencode.yml`: fix-trigger relaxed to `startsWith('/oc fix')`. Reviewer/Tester `/oc fix: ...` findings re-trigger the Fixer. #72 and #73 CLOSED. Changes live on main.
- pages.yml: did not auto-fire on merge; manual run 32104019787 covered it earlier.

## In flight

- **Research (#68):** triggered this run (run 32104600383) - Researcher to design Obsidian M2 optimization. No build/fix/review/test in flight yet.
- No open PRs.

## Issues

- **#68 (Obsidian umbrella)** - REOPENED; active fundamental goal, stays open until codecs beaten.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves (owner directive).
- **#71** - DELETED (HTTP 410). Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2.5-free`. No CreditsError expected.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Research (#68) lands** -> route Architect (blueprint the M2 coder) -> Builder (implement + benchmark) -> Tester (verify fidelity + Kodak row). Keep the loop turning until WebP/PNG/JPEG XL are beaten.
2. **Next Obsidian PR must update README.md + index.html** (Obsidian = Current Project; fix meta description). Verify before merge.
3. **Factory PR to harden maintainer.md** - remove `--delete-branch` so PR branches are preserved after merge (owner directive). Track and merge.
4. **Brainstorm board (#42):** stays frozen until Obsidian resolves.

## Open questions

- How far does Obsidian's Kodak mean bpp (27.82) move after the M2 research spike (predictor + entropy coding)? WebP 9.61 / optipng PNG 13.05 are the first gates; JPEG XL 8.71 is the bar.
- Will the durable branch-preservation rule (maintainer.md update via Factory PR) land cleanly and stop future `--delete-branch` merges?
