# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~07:00Z, maintainer run 32108949269). PR #82 Reviewer **approved**; Tester **in progress** (run 32108957704). Standing by to merge M0 on `/oc approve-test`. Standing directives enforced.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it. Incremental improvement PRs may merge as the loop runs; only the *project* is "done" when the codecs are beaten.
- **Never delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. (PR #78's branch is already gone and cannot be recovered.)
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html (meta description fixed). Verify on every Obsidian merge.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED 2026-08-18; stays OPEN until codecs beaten.
- **M1 (v1) shipped** via PR #78 (merged): Obsidian v1 = 27.8226 mean bpp (bit-exact), vs WebP 9.6130 / optipng PNG 13.0518 / JPEG XL 8.7062. NOT competitive - the entropy stage expanded the container.
- **Research + Architecture delivered** (PR #82, by Dr. Mob / the Architect): defect is purely entropy-coding; fix = per-context adaptive Golomb-Rice (Design A, `ENTROPY_GR` flag), provably non-expanding.
- **M0 COMPLETE** (PR #82, Builder, run 32105937514, finished 2026-08-18T06:43:34Z): GR entropy implemented, wired into encoder/decoder, `ENTROPY_GR` flag added, `model.rs::analyze.entropy_gr` hook, 53/53 tests pass. Synthetic probe: 11.6 bpp @ effort 4, 15.6 @ effort 0 (both < PNG 13.05); real Kodak row pending (no data/toolchain in env). #68 kept open (M1 = beat WebP 9.61 still pending).
- **M0 REVIEWED & APPROVED** (Reviewer run 32108392514, `/oc approve` at 06:54:22). One non-blocking doc note: `obsidian/docs/entropy-architecture.md` line 62 `gr_unmap` pseudocode (`-(u+1)>>1`) is wrong; implementation correctly uses `-(u>>1)`. Doc-only correction to fold into a future Obsidian PR.

## In flight

- **Tester (M0, #68 / PR #82):** opencode-test run `32108957704` **IN PROGRESS** (started 2026-08-18T06:54:27Z, after owner `/oc test`). It will run `cargo test --workspace` (53/53 expected) and attempt the Kodak harness. Kodak data/toolchain are git-ignored and absent in this env, so the real Kodak mean row is expected pending; the Tester should approve-test on the suite + synthetic probe (M0 acceptance = no expansion + lossless, already met). On `/oc approve-test`, Mae merges M0 incremental (no `--delete-branch`, #68 stays open).

## Issues

- **#68 (Obsidian umbrella)** - REOPENED; active fundamental goal, stays open until codecs beaten.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule (last update 2026-08-17).
- **#42 (Brainstorm board)** - frozen until Obsidian resolves (owner directive).
- **#71** - DELETED. Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2.5-free`. No CreditsError expected.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Wait for Tester (run 32108957704)** on PR #82 -> if `/oc approve-test`, Mae merges M0 incremental (no `--delete-branch`, #68 stays open). If `/oc fix`, the workflow routes the Fixer; re-review after.
2. **Fold `gr_unmap` doc correction** into a future Obsidian PR (M1 or a small follow-up) so `entropy-architecture.md` line 62 matches the implementation.
3. **Loop M1/M2/M3:** M1 = per-context predictor selection + GR to beat WebP 9.61; M2/M3 = capped escaped rANS / squeeze to approach JPEG XL 8.71.
4. **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command so the branch-preservation directive is durable (owner directive). Deferred: not blocking; enforced by Mae on every merge. Dispatch Factory when pipeline is quiet.

## Open questions

- M0 GR entropy: does it stop the container expansion on real Kodak data? (Synthetic says yes; real Kodak row pending env data/toolchain.)
- Will the Tester approve-test M0 given the missing Kodak harness, or request a fix? (M0 acceptance is no-expansion + lossless, already met by the suite.)
- Will the durable branch-preservation rule (maintainer.md update via Factory PR) land cleanly and stop future `--delete-branch` merges?
- M1 (per-context predictor selection + GR) must get under WebP 9.61; M2/M3 must approach JPEG XL 8.71. Will the staged plan hold?
