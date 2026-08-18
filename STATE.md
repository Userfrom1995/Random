# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~07:03Z, maintainer run 32109518716). **M0 MERGED** (PR #82 -> `main`, commit `eee5a31`, branch preserved). M1 launched via `build` on #68. Standing directives enforced.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it. Incremental improvement PRs (M0, M1, ...) may merge as the loop runs; only the *project* is "done" when the codecs are beaten.
- **Never delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. (PR #78's branch is already gone and cannot be recovered; PR #82's branch `opencode/issue68-20260818055633` is preserved.)
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html (meta description fixed). Verify on every Obsidian merge.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED 2026-08-18; stays OPEN until codecs beaten.
- **M1 (v1) shipped** via PR #78 (merged): Obsidian v1 = 27.8226 mean bpp (bit-exact), vs WebP 9.6130 / optipng PNG 13.0518 / JPEG XL 8.7062. NOT competitive - the entropy stage expanded the container.
- **Research + Architecture delivered** (PR #82): defect is purely entropy-coding; fix = per-context adaptive Golomb-Rice (Design A, `ENTROPY_GR` flag), provably non-expanding.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z, commit `eee5a31`): GR entropy implemented, wired into encoder/decoder, `ENTROPY_GR` flag added, 53/53 tests pass, 768x512 @ effort 4 = 21.3 bpp (no expansion). Synthetic probe 11.6 bpp @ effort 4 / 15.6 @ effort 0. Real Kodak row pending. #68 kept open.
- **M0 REVIEWED & APPROVED** (Reviewer `/oc approve` 32108392514; Tester `/oc approve-test` 32108957704). Non-blocking doc note: `entropy-architecture.md` line 62 `gr_unmap` pseudocode wrong; implementation correct (`-(u>>1)`).
- **M1 IN FLIGHT** (launched 2026-08-18T07:03Z via `build` on #68): per-context predictor selection + GR to beat WebP 9.61. Builder resumes from `progress/68-obsidian-lossless-image-codec.md`. PR must NOT close #68.

## In flight

- **Builder (M1, #68):** triggered by this run's decision `[{"action":"build","issue":68}]`. Next build run will open a PR on a new branch (e.g. `opencode/issue68-...`), implement per-context predictor selection + GR tuning, target WebP 9.61 on Kodak, report the real Kodak mean bpp row. Standing directives ride along: #68 stays open, README/index.html track Obsidian, preserve branch.

## Issues

- **#68 (Obsidian umbrella)** - REOPENED; active fundamental goal, stays open until codecs beaten. M0 merged; M1 building.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule (last update 2026-08-17).
- **#42 (Brainstorm board)** - frozen until Obsidian resolves (owner directive).
- **#71** - DELETED. Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2.5-free`. No CreditsError expected.
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **M1 (Builder, #68):** per-context predictor selection + GR tuning to beat WebP 9.61 on real Kodak. Report Kodak mean bpp row in the PR. PR must NOT close #68; branch preserved on merge.
2. **Loop M2/M3:** M2/M3 = capped escaped rANS / squeeze toward JPEG XL 8.71 once M1 lands.
3. **Fold `gr_unmap` doc correction** (`entropy-architecture.md` line 62) into M1 or a small Obsidian docs PR so spec matches implementation.
4. **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command so the branch-preservation directive is durable (owner directive). Dispatch Factory when pipeline is quiet. (PR #82 branch already preserved by Mae; the durable rule is still worth landing.)
5. **Verify pages.yml** re-ran after `main` advanced with the M0 merge (hardcoded trigger step handles it; confirm it deployed cleanly).

## Open questions

- M1: will per-context predictor selection + GR get under WebP 9.61 on real Kodak? M0 already removed the expansion (21.3 bpp @ effort 4); M1 must add the efficiency gain.
- Real Kodak mean bpp row: pending env data/toolchain; must be reported in the M1 PR.
- Will the durable branch-preservation rule (maintainer.md update via Factory PR) land cleanly and stop future `--delete-branch` merges?
- M2/M3: capped escaped rANS / squeeze to approach JPEG XL 8.71 - will the staged plan hold?
