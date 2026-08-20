# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~01:35Z, maintainer scheduled run 32321546193). Dispatched `lab #68` to re-link orphan `main` to the Obsidian branch and reopen PR #83, plus fix the root-cause orphan-force-rewrite in `lab.yml`. NOTE: the prior run (32295746644) fired `factory #68` - a DEAD keyword (renamed to `lab`) - so the re-link NEVER ran. This run corrects it.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. Still NOT satisfied (deferred); WebP cleared, schedule once JXL nears / #83 reopens.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were CLOSED; their docs preserved on #83. A fresh `/oc build this` does NOT override this - route to `continue` on the existing PR.
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83 (or issue #68 for factory/lab) - not on a new PR.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break - STILL A HARD BLOCKER, root cause identified)

- **PR #83 is CLOSED** (2026-08-19T18:59:40Z, not merged). `gh pr reopen` and `gh api PATCH state=open` both FAIL: branch `opencode/issue68-20260818070512` has no history in common with `main`. Error verbatim: "state cannot be changed. The opencode/issue68-20260818070512 branch has no history in common with main."
- **`main` = `1709943`** (single orphan commit "Rename Factory Engineer agent to Lab Engineer", pushed 2026-08-19T18:59:41Z). `git merge-base origin/main origin/opencode/issue68-20260818070512` is EMPTY (exit 1).
- **Branch is RECOVERABLE and INTACT:** `opencode/issue68-20260818070512` still exists on origin (head `0deef55`) - it simply was not in the prior run's shallow clone, which falsely suggested deletion. It holds the 9.5208 codec + the R11-D blueprint (`obsidian/docs/architect-r11-crossband-predictor-blueprint.md`). Kodak corpus is durable in git.
- **Root cause (confirmed this run):** `lab.yml` lines 131-151 push to `main` (`git push ... HEAD:main`, with a rebase-on-failure fallback) in a way that has repeatedly orphaned `main` as a single root commit with no parent, breaking every feature branch's merge-base. The Lab Engineer must change this path to always apply edits ON TOP of fetched `origin/main` (fetch, reset --hard origin/main, apply, commit, push) so `main` keeps continuous history.
- **Prior fix attempt FAILED due to dead keyword:** run 32295746644 dispatched `factory #68`, but `factory` was renamed to `lab`; the trigger no-op'd. This run (32321546193) dispatches the correct `lab #68`.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close)

- GitHub's naive auto-close regex matches the literal token `Closes #68` ANYWHERE in a merged commit message, even inside quotes/negations. PR #90's merge commit `b85f30e` body said "no longer uses 'Closes #68'", which auto-closed #68. **Future Factory/Builder commits must NEVER write the literal phrase `Closes #68` (even quoted/negated).** #68 was reopened; stays OPEN.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** OPEN (reopened), stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR branch `opencode/issue68-20260818070512`, head `0deef55`):
  - **DEFAULT shipped codec = 9.5208 bpp mean** (R10-B CFL committed; real Kodak effort-4, reproducible). Beats optipng PNG (13.05) and WebP (9.61) - both gates MET. **JPEG XL 8.71 MISSED by ~0.81 bpp** (17/24 images above). Bit-exact.
  - **R11-A (cross-band in-loop predictor) WASHED:** implemented, measured 9.5091 bpp (~0.01 bpp wash) AND made encode 45x slower. Reverted (`c7aa1a3`) and re-verified 9.5208 at `0deef55` (136 tests pass).
  - **R11-D (MA-tree / property-tree in-loop context) is the escalated next step** - fold the co-located LL sample + weight-context (`wc`, R9-B) into the CMARC quotient context for HF bands. The blueprint ALREADY EXISTS in `obsidian/docs/architect-r11-crossband-predictor-blueprint.md` (R11-D section). No new Architect run needed. Worst case ships unchanged 9.5208 (no regression).

## In flight

- **PR #83 (Obsidian, branch `opencode/issue68-20260818070512`, head `0deef55`):** CLOSED and currently UNREOPENABLE (orphan-main hard block). Branch confirmed intact on origin. Will be reopened once `main` is re-linked by the Lab Engineer.
- **Lab #68 (dispatched THIS run, run will post `/oc lab #68`):** durably re-link `main` (rebase branch onto main, force-push branch ONLY, do NOT touch main) + fix the orphan-force-rewrite recurrence root cause in `lab.yml` + reopen PR #83. This unblocks the one-PR rule and any eventual merge.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above; the hard long pole. R11-D (MA-tree context) is the next blueprinted attempt. Needs real-Kodak re-measure after build.
- **Reopen PR #83** once `main` is re-linked (Lab #68) - restores the one-PR rule.
- **Resume Builder (R11-D) via `continue`** immediately after #83 reopens - implement MA-tree context from the existing blueprint, re-measure REAL Kodak effort-4, record `benchmarks/results/2026-08-20-r11d-*.csv`.
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once JXL nears / #83 reopens).
- **Review staleness on #83:** current head `0deef55` un-reviewed (well past last approve ~96a6075). Fresh review required pre-merge.
- **Commit-message hygiene:** never write the literal `Closes #68` token in any commit message.

## Issues

- **#68 (Obsidian umbrella)** - OPEN (reopened); active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#52 / #90 infra** - PR #90 MERGED (infra hardening shipped).
- **#89 (Infra build-loop resilience)** - CLOSED (merged via PR #88).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `1709943` (orphan, single commit).
- **PR #83:** CLOSED (18:59:40Z, not merged), head `0deef55`, UNREOPENABLE until `main` re-linked. Default 9.5208 (PNG 13.05 + WebP 9.61 MET; JXL 8.71 unmet by +0.81). R11-A washed + reverted; R11-D next (blueprint already on-branch).
- **Branch `opencode/issue68-20260818070512`:** confirmed intact on origin (head `0deef55`), NOT deleted. Holds 9.5208 codec + R11-D blueprint + Kodak corpus.

## Next steps

1. **Lab #68 (dispatched THIS run):** re-link `main` to share history with the obsidian branch by rebasing the branch onto `main` and force-pushing ONLY the branch (do NOT touch `main`); then reopen PR #83. FIX the orphan-force-rewrite root cause in `lab.yml` (push-to-main path must keep continuous history).
2. **After `main` re-link + #83 reopen:** resume `continue` on PR #83 to implement **R11-D (MA-tree context)** directly from the existing blueprint (`architect-r11-crossband-predictor-blueprint.md`), re-measure REAL Kodak effort-4 against the JPEG XL 8.71 gate, record `benchmarks/results/2026-08-20-r11d-*.csv`. Worst case ships unchanged 9.5208 (no regression).
3. **After R11-D measured:** if JPEG XL gate clears (default < 8.71 bpp, alongside PNG 13.05 + WebP 9.61), rebase-merge (`--no-delete-branch`) - but ONLY after `main` is re-linked - then close #68.
4. **README / index.html promotion:** schedule a Builder/Lab pass to promote Obsidian as Current now that WebP is cleared.

## Open questions

- **Will `lab #68` re-link succeed this time?** The blocker is now precisely diagnosed (dead keyword last time; root cause = lab.yml push-to-main orphaning). The Lab Engineer rebases the branch onto main, force-pushes the branch only, reopens #83. If rebase conflicts (main holds older M0 obsidian/), the Lab Engineer uses `--onto` or a merge onto a main-based branch. High confidence.
- **Will R11-D (MA-tree / property-tree in-loop context) clear the +0.81 JPEG XL gap on REAL Kodak?** R11-A (cross-band predictor) washed; R11-D (fold co-located LL + weight-context into the CMARC quotient context) is the escalated remaining blueprinted lever, and its blueprint ALREADY EXISTS on the branch. WebP is cleared; JPEG XL is the hard long pole. Empirical verdict pending the Builder's R11-D build + real-Kodak re-measure. NOT yet a 100%-certain unmovable wall (cross-band/property-tree context is exactly how JPEG XL and FLIC win).
- **Merge gate (owner override #2):** NOT met - default 9.5208 bpp beats PNG (13.05) + WebP (9.61) but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **Review staleness on #83:** current head `0deef55` un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current despite the standing directive (WebP gate cleared); schedule once JXL nears / PR reopens.
- **One-PR integrity (TEMPORARILY BROKEN by infra):** #83 CLOSED (unreopenable until main relinks); #84, #87 CLOSED. Issue #68 OPEN until codecs beaten. Upon `main` re-link, reopen #83 as the sole canonical Obsidian PR.

- Mae, the Maintainer
