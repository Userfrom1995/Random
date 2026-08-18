# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~05:36Z, event run on PR #81, run 32103503380). The factory round re-dispatched on audit #72 has finally landed as a REAL, verified PR (#81) carrying both unlanded workflow fixes. Reviewer in flight; merge deferred to the loop. Lab otherwise idle.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** CLOSED (by merge of PR #80 at 05:21Z, M1 adaptive-rANS lockstep fix). M2/M3 (context/predictor tuning toward WebP 9.61 / optipng PNG 13.05) remain as follow-on optimization milestones; no active build right now.
- Checklist 10 shipped on main (first Obsidian Kodak row: 27.8226 mean bpp, bit-exact). Owner's standing directive: iterate until Obsidian beats the other codecs on Kodak (lossless + performance).

## Audit #72 - resolved by PR #81 (verified real this time)

- **Audit title:** "[Audit] Issue #71 deleted and its root-cause fix never landed: build-verify false positive still live on main." CLOSED 2026-08-17T11:47Z. Its headline claim was a stale false positive (build-verify fixed on main via `ae5160b`); its META critique ("fixes reported done, never landed") was TRUE, with two live examples (#73 non-PR review crash; fix-trigger guard).
- **PR #81 "[Infra] Factory update for #72"** is the genuine factory round. Branch `opencode/factory-72-build-verify-and-73-review-crash` EXISTS on origin (verified via fetch/ls-remote - unlike the phantom `3ea8390` from run 32102754391). 3 commits by The Factory Engineer (CTO), +46/-14, 4 files:
  - `.github/workflows/opencode-review.yml`: `if:` relaxed to `startsWith('/oc review')` + non-PR graceful handling (resolve linked PR via `opencode/issue<N>-*`, else post maintenance note). #73 crash fixed.
  - `.github/workflows/opencode.yml`: fix job trigger relaxed to `startsWith('/oc fix')`; general-command guard updated. Reviewer/Tester `/oc fix: ...` findings now re-trigger the Fixer.
  - `.github/agents/builder.md`, `fixer.md`: `--force-with-lease` added after rebase.
- **Status:** OPEN, Reviewer in flight (two `opencode-review` runs pending/in-progress: 32103493712, 32103503252). Closes #72.

## In flight

- PR #81 review: pending/in-progress (triggered by user `/oc review` + PR open). Maintainer must NOT re-trigger (anti-duplicate rule).
- This maintainer run: 32103503380 (decision.json empty; comment.md posted on #81).
- No opencode build / fix / factory runs in flight.

## Issues

- **#68 (Obsidian umbrella)** - CLOSED via PR #80 merge.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian M2/M3 scopes.
- **#71** - DELETED (HTTP 410). Tracked root cause (build-verify) fixed on main; deletion is the audit-trail loss the Auditor flagged. Propose a hard "do not delete audit issues" rule in AGENTS.md / Auditor runbook.
- **#72 (audit issue)** - CLOSED; its actionable meta critique is satisfied by PR #81 (in review).
- **#73 (review crash on non-PR)** - CLOSED; its fix now genuinely lands via PR #81 (was falsely claimed done before).

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. All workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2.5-free`. No CreditsError expected.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Let the Reviewer finish PR #81** (already triggered - do not duplicate). On approval the review workflow forwards to the Tester (`/oc test`); on Tester approval it forwards to me to merge.
2. **Merge PR #81** (rebase + delete-branch) on Tester approval. Infra PR - no shipping cap. Then confirm `pages.yml`/preview still deploy. Close any remaining linked issue (#72 already closed).
3. **Close-the-loop verification:** after merge, confirm `opencode-review.yml` handles a live non-PR `/oc review` gracefully and `opencode.yml` re-triggers the Fixer on a live `/oc fix: ...` finding - the audit's two test cases.
4. **Resume Obsidian optimization (M2/M3):** self-correcting weighted predictor / context tuning toward WebP 9.61 / optipng PNG 13.05. Open a new issue when ready and route research -> architect -> build, or continue directly on the codec.
5. **Brainstorm board (#42):** once M2/M3 scoped, the Ideator can resume.
6. **Process guard:** never close audit/infra issues until the root-cause fix is merged and verified on main (lesson from #71/#73). Consider codifying in AGENTS.md.

## Open questions

- Does the Reviewer approve #81 cleanly (no em-dash/PAT/loop-breaking issues), forwarding to the Tester, then to me for merge?
- After #81 merges and the two fixes run live: does the "reported done but not pushed" pattern stay broken for good?
- After M1 on main, how far does Obsidian's Kodak mean bpp (27.82) move toward/under WebP 9.61 / optipng PNG 13.05? M2/M3 are the lever.
- Should #71's deletion be codified as a "do not delete audit issues" hard rule in AGENTS.md / the Auditor runbook?
