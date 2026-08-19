# STATE - Random factory checkpoint

- **Updated:** 2026-08-19 (~19:43Z, maintainer run 32294596041, owner `/oc maintainer` on PR #83 after R11-A washed + PR closure).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Drop `--delete-branch` from every `gh pr merge` (gh has no `--no-delete-branch` flag; simply omit `-d` to preserve the branch).
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. NOTE: still NOT satisfied (deferred until gates near).

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were both CLOSED; their docs preserved on #83. A fresh `/oc build this` does NOT override this - route to `continue` on the existing PR.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83, never spawn a fresh build. research/architect/factory MUST be triggered ON PR #83 (or issue #68 for factory) - not on a new PR.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break - NOW A HARD BLOCKER)

- **PR #83 is CLOSED** (18:59:40Z, not merged). `gh pr reopen` AND `gh api PATCH state=open` BOTH FAIL: GitHub hard-blocks reopening because the branch `opencode/issue68-20260818070512` has **no history in common with `main`**. Error verbatim: "state cannot be changed. The opencode/issue68-20260818070512 branch has no history in common with main." **This violates the one-PR rule** - there is currently NO open Obsidian PR.
- **`main` = `1709943`** (single orphan commit "Rename Factory Engineer agent to Lab Engineer", pushed 18:59:41Z). `git merge-base origin/main origin/opencode/issue68-20260818070512` is EMPTY (exit 1). `main` is NOT an ancestor of the branch; the branch is orphan-root -> `8a36e19`.
- **Root cause of the recurrence:** the Factory's own pushes to `main` (every infra change) force-rewrite `main` as a single orphan commit, orphaning it from all feature branches and re-breaking the merge-base. This is the systemic cause, confirmed this run.
- **Fix (dispatched this run as `factory` #68):** the Factory must (a) durably re-link `main` so it shares history with the obsidian branch WITHOUT merging codec into `main` (so #83 can be reopened), and (b) stop orphan-force-rewriting `main` (fast-forward / proper merge only). Until (a) lands, #83 cannot be reopened and no merge is possible regardless of codec.
- Kodak corpus is durable in git (`obsidian/benchmarks/data/kodak/` PPMs tracked + `kodak.sha256` + scripts). Gate IS measurable reproducibly.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close)

- GitHub's naive auto-close regex matches the literal token `Closes #68` (and Fixes/Resolves) ANYWHERE in a merged commit message, even inside quotes/negations. PR #90's merge commit `b85f30e` body said "no longer uses 'Closes #68'", which auto-closed #68. **Future Factory/Builder commits must NEVER write the literal phrase `Closes #68` (even quoted/negated).** #68 was reopened; stays OPEN.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** OPEN (reopened), stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR branch `opencode/issue68-20260818070512`, head `8a36e19`):
  - **DEFAULT shipped codec = 9.5208 bpp mean** (R10-B CFL committed; real Kodak effort-4, reproducible, `2026-08-19-r10.csv`). Beats optipng PNG (13.05) and WebP (9.61) - **both gates MET**. **JPEG XL 8.71 MISSED by ~0.81 bpp** (17/24 images above). Bit-exact.
  - **R11-A (cross-band in-loop predictor) WASHED:** implemented, measured 9.5091 bpp (vs 9.5208 baseline, ~0.01 bpp wash, no gate progress) AND made encode 45x slower (6.5s vs 0.14s/image). Reverted (`c7aa1a3`) and escalated to R11-D.
  - **R11-D (MA-tree / property-tree in-loop context) is the escalated next step** - fold the co-located LL sample + weight-context (`wc`, R9-B) into the CMARC quotient context for HF bands so the entropy coder specializes per (context, ll-quantized-class). Documented in `obsidian/docs/architect-r11-crossband-predictor-blueprint.md` (lines 144, 152-153). Worst case ships unchanged 9.5208 (no regression).

## In flight

- **PR #83 (Obsidian, branch `opencode/issue68-20260818070512`, head `8a36e19`):** CLOSED and currently UNREOPENABLE (orphan-main hard block). Builder escalated to R11-D after R11-A washed. `continue` dispatched this run to implement R11-D (the Builder's orphan-rebuild will likely self-heal the relink). One-PR rule TEMPORARILY broken by infra; will be restored on `main` re-link + #83 reopen.
- **Factory #68 (dispatched this run, run will post `/oc factory #68`):** durably re-link `main` (no codec merge) + fix the orphan-force-rewrite recurrence root cause.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above; the hard long pole. R11-D (MA-tree context) is the next blueprinted attempt. Needs real-Kodak re-measure after build.
- **Reopen PR #83** once `main` is re-linked (Factory) - restores the one-PR rule.
- **README / index.html Obsidian promotion** (standing directive, deferred until gates near - now that WebP is cleared, schedule soon).
- **Review staleness on #83:** current head `8a36e19` un-reviewed (well past last approve ~96a6075). Fresh review required pre-merge.
- **Commit-message hygiene:** never write the literal `Closes #68` token in any commit message.

## Issues

- **#68 (Obsidian umbrella)** - OPEN (reopened); active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#52 / #90 infra** - PR #90 MERGED (infra hardening shipped).
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `1709943` (orphan, single commit).
- **PR #83:** CLOSED (18:59:40Z, not merged), head `8a36e19`, **unreopenable until `main` re-linked** (orphan-main break). Default 9.5208 (PNG 13.05 + WebP 9.61 MET; JXL 8.71 unmet by +0.81). R11-A washed + reverted; R11-D next.
- **PR #90:** MERGED (infra hardening on `main`; branch preserved; #68 reopened).

## Next steps

1. **Factory #68 (in flight):** re-link `main` to share history with the obsidian branch (no codec merge) AND stop orphan-force-rewriting `main`. This is the prerequisite for reopening #83 and for any eventual merge.
2. **After `main` re-link:** reopen PR #83 (the sole canonical Obsidian PR) and resume `continue` if R11-D is not yet measured.
3. **Builder (R11-D) via `continue`:** implement MA-tree in-loop context, re-measure REAL Kodak effort-4 against the JPEG XL 8.71 gate. Record `benchmarks/results/2026-08-19-r11d-*.csv`. Worst case ships unchanged 9.5208 (no regression).
4. **After R11-D measured:** if JPEG XL gate clears (default < 8.71 bpp, alongside PNG 13.05 + WebP 9.61), rebase-merge (`--no-delete-branch`) - but ONLY after `main` is re-linked - then close #68.
5. **README / index.html promotion:** schedule a Builder/Factory pass to promote Obsidian as Current now that WebP is cleared.

## Open questions

- **Can R11-D (MA-tree / property-tree in-loop context) clear the +0.81 JPEG XL gap on REAL Kodak?** R11-A (cross-band predictor) washed; R11-D (fold co-located LL + weight-context into the CMARC quotient context) is the escalated remaining blueprinted lever. WebP is cleared; JPEG XL is the hard long pole. Empirical verdict pending the Builder's R11-D build + real-Kodak re-measure. NOT yet a 100%-certain unmovable wall (cross-band/property-tree context is exactly how JPEG XL and FLIF win).
- **PR #83 reopening (one-PR rule BLOCKED):** cannot reopen until `main` is re-linked. `factory` #68 dispatched to fix this. Until then no open Obsidian PR exists (infra break, not intent).
- **Merge gate (owner override #2):** NOT met - default 9.5208 bpp beats PNG (13.05) + WebP (9.61) but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **Orphan-main break (recurrence, NOW CRITICAL):** `main` = `1709943` orphan; branch = orphan root -> `8a36e19`. `git merge-base` EMPTY. Caused by Factory pushes force-rewriting `main` as a single orphan. Must be fixed by the Factory before #83 can be reopened or merged.
- **Review staleness on #83:** current head `8a36e19` un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current despite the standing directive (WebP gate cleared); schedule once JXL nears / PR reopens.
- **One-PR integrity (TEMPORARILY BROKEN by infra):** #83 CLOSED (unreopenable until main relinks); #84, #87 CLOSED. Issue #68 OPEN until codecs beaten.

- Mae, the Maintainer
