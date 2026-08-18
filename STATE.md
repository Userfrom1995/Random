# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~06:44Z, event run on PR #82, run 32108169866, owner `/oc maintainer`). M0 is COMPLETE and pushed; routing the Reviewer now. All three standing owner directives on PR #82 remain enforced.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it. Incremental improvement PRs may merge as the loop runs; only the *project* is "done" when the codecs are beaten.
- **Never delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. (PR #78's branch is already gone and cannot be recovered.)
- **Website + README must track the active project.** Obsidian is now in README.md (Current Project) and promoted to Current on index.html (meta description fixed). Verify on every Obsidian merge.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED 2026-08-18; stays OPEN until codecs beaten.
- **M1 (v1) shipped** via PR #78 (merged): Obsidian v1 = 27.8226 mean bpp (bit-exact), vs WebP 9.6130 / optipng PNG 13.0518 / JPEG XL 8.7062. NOT competitive - the entropy stage expanded the container.
- **Research + Architecture delivered** (PR #82, by Dr. Mob / the Architect): defect is purely entropy-coding; fix = per-context adaptive Golomb-Rice (Design A, `ENTROPY_GR` flag), provably non-expanding.
- **M0 COMPLETE** (PR #82, Builder, run 32105937514, finished 2026-08-18T06:43:34Z): GR entropy implemented, wired into encoder/decoder, `ENTROPY_GR` flag added, `model.rs::analyze.entropy_gr` hook, 53/53 tests pass. Synthetic probe: 11.6 bpp @ effort 4, 15.6 @ effort 0 (both < PNG 13.05); real Kodak row pending (no data/toolchain in env). #68 kept open (M1 = beat WebP 9.61 still pending).

## In flight

- **Review (M0, #68 / PR #82):** this run (32108169866) routes the Reviewer via `/oc review` on head `1998197`. The automatic reviewer did NOT trigger on the Builder's push (only opencode-pr-trigger + pages runs fired), so the explicit trigger is required. Reviewer -> Tester -> (if approved) merge M0 as incremental, no `--delete-branch`, without closing #68.

## Issues

- **#68 (Obsidian umbrella)** - REOPENED; active fundamental goal, stays open until codecs beaten.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm board)** - frozen until Obsidian resolves (owner directive).
- **#71** - DELETED. Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2.5-free`. No CreditsError expected.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Reviewer on PR #82** (this run, head `1998197`) -> audit GR implementation. Then Tester (`/oc test`) -> report real Kodak mean bpp -> merge M0 as incremental (no `--delete-branch`, #68 stays open).
2. **Loop M1/M2/M3** after M0 merges: M1 = per-context predictor selection + GR to beat WebP 9.61; M2/M3 = capped escaped rANS / squeeze to approach JPEG XL 8.71.
3. **Factory PR to harden maintainer.md** - remove `--delete-branch` so PR branches are preserved after merge (owner directive). Track and merge.

## Open questions

- M0 GR entropy: does it stop the container expansion on real Kodak data? (Synthetic says yes; real Kodak row pending env data/toolchain.)
- M1 (per-context predictor selection + GR) must get under WebP 9.61; M2/M3 must approach JPEG XL 8.71. Will the staged plan hold?
- Will the durable branch-preservation rule (maintainer.md update via Factory PR) land cleanly and stop future `--delete-branch` merges?
