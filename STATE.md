# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~02:00Z, maintainer event run 32322660787, triggered by PR #91 review escalation). Merged PR #91 (orphan-main guard). Caught + fixed a second auto-close trap: the PR's commit message `(Closes #68)` auto-closed #68 on merge; reopened #68. Re-dispatched `lab #68` to perform the actual obsidian-branch re-link (the guard shipped but the orphan branch is still unre-linked).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it. (#68 was briefly auto-closed by PR #91's commit-message token and REOPENED this run.)
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`. (PR #91 branch `opencode/lab-68-orphan-main-guard` intentionally left intact.)
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. Still NOT satisfied (deferred); WebP cleared, schedule once JXL nears / #83 reopens.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Currently VIOLATED: zero open Obsidian PRs because #83 is still CLOSED (orphan-branch block not yet resolved this run).
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec).
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83 (or issue #68 for factory/lab) - not on a new PR.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break - guard SHIPPED, branch re-link STILL PENDING)

- **PR #91 MERGED (2026-08-20 ~01:55Z, rebase, no branch delete):** commit `c043b7e` "lab: harden main-push paths against orphan-main rewrite (Closes #68)" is now on `main`. The orphan-main guard (merge-base --is-ancestor check + rebase-before-push, abort-on-conflict) is now live in `lab.yml` and `maintainer.yml`. This PREVENTS future orphaning but did NOT fix the existing orphan.
- **`main` = `c043b7e`** (after PR #91). The obsidian branch `opencode/issue68-20260818070512` (head `0deef55`) STILL has an EMPTY merge-base with `main` - it is still orphaned. PR #83 still CLOSED and UNREOPENABLE until the branch is re-linked.
- **Branch is RECOVERABLE and INTACT:** `opencode/issue68-20260818070512` still exists on origin (head `0deef55`) - holds the 9.5208 codec + R11-D blueprint. Kodak corpus durable in git.
- **Root cause (confirmed):** `lab.yml` push-to-`main` path repeatedly orphaned `main`. The guard now makes that path abort instead of orphaning; but the EXISTING orphan of the obsidian branch must still be repaired by rebasing the BRANCH onto main (force-push branch only).
- **FALSE-POSITIVE TRAP (still live):** shallow clone can fake a clean merge-base. Any re-link verification MUST do a FULL `git fetch` and treat empty `git merge-base` as the blocker.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - RE-TRIGGERED THIS RUN

- GitHub's naive auto-close regex matches the literal token `Closes #68` ANYWHERE in a merged commit message. PR #91's single commit message contained `(Closes #68)`; after the rebase merge, GitHub auto-closed #68 (closedAt 2026-08-20T01:54:59Z). **Maintainer caught it and reopened #68 this run.** #68 is OPEN again.
- **Lesson reinforced:** the Reviewer's `Closes #68` finding covered ONLY the PR body (which I stripped), but MISSED the commit-message token which was the actual auto-closer. Future Factory/Builder/Lab commits must NEVER write the literal phrase `Closes #68` (even quoted/negated/in commit messages). This is now doubly confirmed.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** OPEN (reopened this run), stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 target PR #83** (branch `opencode/issue68-20260818070512`, head `0deef55`):
  - **DEFAULT shipped codec = 9.5208 bpp mean** (R10-B CFL). Beats optipng PNG (13.05) and WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
  - **R11-A (cross-band in-loop predictor) WASHED** (~0.01 bpp wash, 45x slower), reverted.
  - **R11-D (MA-tree / property-tree in-loop context)** is the escalated next step; blueprint ALREADY EXISTS on-branch. Worst case ships unchanged 9.5208.

## In flight

- **PR #91 (Lab infra, orphan-main guard):** MERGED this run (rebase, branch kept). Guard now live on `main`.
- **Lab #68 (RE-DISPATCHED THIS run, run 32322660787, will post `/oc lab #68`):** actually re-link the orphaned obsidian branch onto `main` (rebase branch onto main, force-push BRANCH ONLY) + reopen PR #83. The guard is now merged, so the re-link is safe. MUST verify with a FULL fetch that `git merge-base` is non-empty before claiming success.
- **PR #83 (Obsidian):** CLOSED, UNREOPENABLE until the branch re-link lands.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above (default 9.5208); the hard long pole. R11-D is the next blueprinted attempt.
- **Reopen PR #83** once the branch is re-linked (Lab #68) - restores the one-PR rule.
- **Resume Builder (R11-D) via `continue`** immediately after #83 reopens.
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once JXL nears / #83 reopens).
- **Review staleness on #83:** head `0deef55` un-reviewed. Fresh review required pre-merge.
- **Commit-message hygiene:** never write the literal `Closes #68` token in ANY commit message or PR body (double-confirmed this run).

## Issues

- **#68 (Obsidian umbrella)** - OPEN (reopened this run); active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#52 / #90 / #89 infra** - PR #90 MERGED; #89 CLOSED; #52 related infra merged. PR #91 (the orphan-main guard) now MERGED on top.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule; board live.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.
- **#71/#72/#73/#74/#75 (prior audit bugs)** - all CLOSED; root causes fixed on main.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `c043b7e` (after PR #91). No `CreditsError` in recent runs.
- **PR #91:** MERGED (guard shipped). Code reviewer-approved; the only finding (PR-body `Closes #68`) fixed by Maintainer; the latent commit-message token auto-closed #68 and was reopened.
- **Branch `opencode/issue68-20260818070512`:** confirmed intact on origin (head `0deef55`), NOT deleted. Orphaned from main (empty merge-base) - re-link pending via re-dispatched `lab #68`.

## Next steps

1. **Lab #68 (RE-DISPATCHED THIS run):** re-link the orphaned obsidian branch onto `main` (rebase branch onto origin/main, force-push BRANCH ONLY, do NOT touch main), then reopen PR #83, and re-verify `git merge-base` is non-empty + PR #83 OPEN. The orphan-main guard from #91 now prevents re-orphaning. MANDATORY: full `git fetch` + real `git merge-base` non-empty check.
2. **After branch re-link + #83 reopen:** resume `continue` on PR #83 to implement **R11-D (MA-tree context)** from the existing blueprint, re-measure REAL Kodak effort-4 against the JPEG XL 8.71 gate.
3. **After R11-D measured:** if JPEG XL gate clears (default < 8.71 bpp, alongside PNG 13.05 + WebP 9.61), rebase-merge (`--no-delete-branch`) - but ONLY after `main` is re-linked - then close #68.
4. **README / index.html promotion:** schedule once JXL nears / PR reopens.

## Open questions

- **Will THIS `lab #68` re-dispatch actually re-link?** The prior `lab #68` (01:47Z owner `/oc lab`) produced ONLY the guard PR #91, not the re-link. This re-dispatch explicitly scopes the Lab Engineer to the re-link + PR #83 reopen, now that the guard is merged. If it again only re-asserts the guard, the next run must escalate to a direct re-link inspection.
- **Will R11-D clear the +0.81 JPEG XL gap on REAL Kodak?** Blueprint on-branch; verdict pending the Builder's R11-D build + real-Kodak re-measure. NOT yet a 100%-certain unmovable wall.
- **Merge gate (owner override #2):** NOT met - default 9.5208 bpp beats PNG (13.05) + WebP (9.61) but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **Review staleness on #83:** head `0deef55` un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current despite standing directive (WebP gate cleared); schedule once JXL nears / PR reopens.
- **One-PR integrity (TEMPORARILY BROKEN by infra):** zero open Obsidian PRs until #83 reopens (orphan-branch block). #68 OPEN until codecs beaten.
- **pages.yml:** triggered manually this run (run 32322786103) because it had not auto-started after the PR #91 merge. Verify it completes.
- **Billing:** resolved (no `CreditsError` in recent runs; `small_model` correctly pinned free).

- Mae, the Maintainer
