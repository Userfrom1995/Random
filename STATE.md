# STATE - Random factory checkpoint

- **Updated:** 2026-08-18 (~13:55Z, maintainer run 32145156905, event: owner `/oc maintainer` on PR #84; Factory rebase #84 landed, PR #83 superseded/closed). PR #84 is now the OPEN single canonical Obsidian PR on `opencode/factory-68-rebase-obsidian`, head `89891e84f9934f5887c0a97fe8495704f62e6c4b`, MERGEABLE (merge base = main tip `30fd150`). **REAL KODAK = 10.0906 bpp mean** (PNG 13.05 MET; WebP 9.61 MISSED by 0.48; JPEG XL 8.71 MISSED by 1.38). R3 residual-context blueprint delivered; this run resumes the Builder via `continue` to implement R3-A/B/C on the single branch, re-measuring on REAL Kodak. The orphan-`main` mergeability break is RESOLVED via the #84 rebase (merge base exists).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge`. (PR #78's branch is already gone; preserve all others.)
- **Website + README must track the active project.** Obsidian is in README.md (Current Project) and promoted to Current on index.html. Verify on every Obsidian advance.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Do NOT create multiple PRs for the Obsidian work. Keep a single open PR and continue iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. (PR #83 was CONFLICTING and is now CLOSED/superseded by the Factory rebase PR #84; #84 is the single PR.)
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact). This overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together.** Do NOT autopilot with bare `/oc continue`. Each codec milestone must be architected (Architect on the existing PR, Mode 2 -> `continue`) and implementable by the Builder on the single branch; re-engage the Researcher for specific algorithmic bottlenecks. The Researcher/Architect auto-chain is DANGEROUS here because it would open a second codec PR - so they are triggered only when they can target the existing single PR, never to spawn a fresh build.

## CRITICAL INFRASTRUCTURE BREAK - RESOLVED (via Factory rebase PR #84)

- `main` is still the single orphan commit `30fd150873da6578c639ef1d569df4d948712aef` (1 commit, no history). BUT PR #84's branch (`opencode/factory-68-rebase-obsidian`) is based on `30fd150`, so `git merge-base main...branch` == `30fd150` (the merge base EXISTS) and `gh pr merge --rebase` is now possible. The Factory's durable repair was to branch the Obsidian work off `main`'s real tip (a direct `git push` to `main` was rejected by branch protection, so the earlier fast-forward did not persist). No Factory run is in flight now; the repair shipped as PR #84.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image codec competitive with JPEG XL / WebP, Kodak-benchmarked).** REOPENED; stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82, merged 2026-08-18T07:03:12Z, commit `eee5a31`): GR entropy backend, 53/53 tests pass, no expansion.
- **CANONICAL PR = #84** (Factory rebase, branch `opencode/factory-68-rebase-obsidian`), supersedes the old PR #83 (CLOSED). Real Kodak effort-4 (trustworthy): **10.0906 bpp mean** with the never-expand best-backend selection (CMARC/R2 wins only where it beats v1 GR; net ~0.07 bpp below the 10.1556 v1 GR baseline). PNG gate (13.05) **MET**; WebP (9.61) + JPEG XL (8.71) **PENDING / STILL UNMET**.
- **CMARC R1 -> R2.4 BUILT END-TO-END, all OFF by default**, production byte-identical to v1 GR (10.1556). 106 lib tests pass, bit-exact. CMARC/R2 shaved only ~0.07 bpp on real Kodak (plateaued at ~10.1 residual-entropy floor).
- **CMARC RESEARCH + ARCHITECT BLUEPRINT DELIVERED:** `obsidian/docs/research-breakthrough.md`, `obsidian/docs/architect-cmarc-blueprint.md`. The ~10.1 bpp floor is the ceiling of the single-k per-context Golomb-Rice / flat per-bit binary coder, NOT the image - JPEG-LS reaches 9.71 bpp on the same Kodak corpus with the same LOCO-I GAP predictor but a context-based arithmetic (QM) coder.
- **REAL KODAK MEASUREMENT (2026-08-18):** `obsidian/benchmarks/results/2026-08-18-real-kodak-2.csv` - 10.0906 bpp mean. Confirms CMARC/R2 did NOT clear WebP (9.61); it sits at the ~10.1 floor, ~0.38 bpp above JPEG-LS (9.71) on the SAME predictor. The entropy backend / context modeling is the proven bottleneck.
- **R3 ARCHITECT BLUEPRINT DELIVERED (13:32Z, run 32142354868):** `obsidian/docs/architect-r3-residual-context-blueprint.md` (now in #84). Diagnosis: (1) PRIMARY - CMARC conditions on the spatial-gradient context (predictor selection), not on quantized neighboring *residuals* (JPEG-LS DIFF context), so its per-(cid,bin) models never specialize to the local residual distribution; (2) SECONDARY - R2 replaced Rice/Exp-Golomb quotient with fixed-width MSB-first binary magnitude, re-introducing a per-bit floor. Design: R3-A residual-context `residual_context(dL,dU,dUl)` as coding context (expected ~9.4-9.7 bpp, clears WebP); R3-B restore per-context Rice-through-binary (`q=m>>k` geometric quotient model + `k` remainder bits); R3-C JPEG-LS run mode; R2.4 re-tuned on the corrected context to reach JPEG XL.

## In flight

- **PR #84 (single canonical Obsidian PR):** MERGEABLE (merge base = main tip `30fd150`). Real Kodak 10.0906 bpp mean (PNG MET; WebP/JXL UNMET). R3 blueprint DELIVERED (in-branch). This run resumes the **Builder via `continue`** to implement R3-A (residual-context conditioning) first, then R3-B (Rice-through-binary) and R3-C (run mode), re-measuring on REAL Kodak after each. No `continue`/architect/research currently in flight for #84, so the trigger is not a duplicate.
- **PR #83 CLOSED** (was CONFLICTING, superseded by the Factory rebase #84). All codec work preserved in #84. ONE-PR directive honored.
- **Factory:** main-history repair RESOLVED via PR #84 rebase (merge base exists; `--rebase` possible). `data/kodak` provisioned (real Kodak measurable). No Factory run in flight.

## Issues

- **#68 (Obsidian umbrella)** - OPEN; active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas are wanted; Obsidian takes priority.
- **#71** - DELETED. Root cause fixed on main.
- **#72 / #73** - CLOSED; fixes landed via PR #81.
- **#83 (Obsidian PR, old)** - CLOSED this run (superseded by #84 Factory rebase).

## Reviewer/Tester/model status

- **Model config:** opencode.json `model: opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free`. Workflow `.yml` agent steps pinned to `opencode/hy3-free`; review/test/factory on `mimo-v2-free`. No CreditsError expected.
- **Mergeability:** RESOLVED via #84 rebase. `main` == orphan `30fd150`; branch == `89891e84`; merge base == `30fd150` (EXISTS); `--rebase` possible. Merge gated only by performance target (override #2).
- Next Sunday 2026-08-23: weekly free-model upgrade check.

## Next steps

1. **Builder (via `continue`, this run):** implement R3-A (residual-context `residual_context(dL,dU,dUl)` as the CMARC coding context), re-benchmark REAL Kodak effort-4; then R3-B (Rice-through-binary: `q=m>>k` geometric quotient model + `k` remainder bits) and R3-C (JPEG-LS run mode). Measure each against WebP 9.61 / JPEG XL 8.71 on real data. Keep all prior seams OFF by default; keep never-expand safety net.
2. **After R3 build:** if gates still unmet on real Kodak, re-engage Researcher/Architect (existing PR only) for a stronger marginal/context signal (true QM-class adaptive arithmetic coder) - do NOT autopilot with bare `continue`.
3. **Merge gate (only when met AND main repaired):** Obsidian Kodak mean bpp < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71 (lossless, bit-exact). Then merge (branch preserved per owner directive), close #68.
4. **Verify README + index.html** still promote Obsidian as Current on every Obsidian advance.
5. **Factory PR to harden maintainer.md** - remove `--delete-branch` from the documented merge command (owner directive). Dispatch Factory when pipeline is quiet.

## Open questions

- **THE decisive number is known:** real Kodak = 10.0906 bpp mean. CMARC/R2 plateaued ~0.38 bpp above JPEG-LS (9.71) on the SAME predictor. The Architect's R3 diagnosis: CMARC conditions on the wrong context (spatial gradient, not quantized neighbor residuals), and R2 dropped the geometric quotient for fixed-width binary - both fixed by R3-A/B/C.
- **Next breakthrough:** can R3 (residual-context conditioning + Rice-through-binary + run mode) close the ~0.38->1.38 bpp gap to WebP/JPEG XL on the SAME residuals? JPEG-LS (9.71) / WebP (9.61) / JPEG XL (8.71) prove ~9.4-9.7 is reachable; R3-A alone is projected to reach ~9.4-9.7 bpp and clear WebP, with R3-B/C + re-tuned R2.4 aiming at JPEG XL.
- **Measurement gap (CLOSED):** `data/kodak` is provisioned; milestones validated on real Kodak, no longer synthetic proxies.
- **Mergeability (RESOLVED via rebase):** `main` == orphan `30fd150`, but #84 is based on `30fd150` so the merge base exists and `--rebase` is possible; durable fix achieved by branching the Obsidian work off main's real tip.
- Will the Architect-on-PR -> continue loop converge to a competitive codec without fracturing into multiple PRs? Now consolidated: #83 closed, #84 is the single PR.

- Mae, the Maintainer
