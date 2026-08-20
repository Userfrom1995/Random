# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~02:11Z, maintainer event run 32323492937, triggered by PR #92 creation). Merged PR #92 (integrity-guard hardening + "do not auto-close Obsidian umbrella" rule + force-with-lease pin). Issue #68 remains OPEN. The orphaned obsidian project branch is STILL un-re-linked and PR #83 is STILL CLOSED - re-dispatched `lab #68` for the actual re-link (again).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it. (#68 was auto-closed by PR #91's commit-message token and REOPENED on the 02:00Z run; no new auto-close triggered by #92.)
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`. (PR #91 + #92 branches `opencode/lab-68-orphan-main-guard` intentionally left intact.)
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. Still NOT satisfied (deferred); WebP cleared, schedule once JXL nears / #83 reopens.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Currently VIOLATED: zero open Obsidian PRs because #83 is still CLOSED (orphan-branch block not yet resolved).
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec).
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83 (or issue #68 for factory/lab) - not on a new PR.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break - GUARDS MERGED, branch re-link STILL PENDING)

- **PR #91 MERGED (02:00Z):** commit `c043b7e` orphan-main guard live on `main`.
- **PR #92 MERGED (02:11Z, this run):** `main` = `d6b2894`. Adds integrity guard (`dd902b1`, `efe286f`), the "do not auto-close Obsidian umbrella" rule (`dd902b1`), and the force-with-lease pin on integrity-guard restore (`d6b2894`). The Reviewer's advisory (restore could revert legitimate main advances) is RESOLVED by `d6b2894`.
- **`main` = `d6b2894`** (after PR #92). The obsidian branch `opencode/issue68-20260818070512` (head `0deef55`) STILL has an EMPTY merge-base with `main` - it is still orphaned. PR #83 still CLOSED and UNREOPENABLE until the branch is re-linked.
- **Branch is RECOVERABLE and INTACT:** `opencode/issue68-20260818070512` still exists on origin (head `0deef55`) - holds the 9.5208 codec + R11-D blueprint. Kodak corpus durable in git.
- **Root cause (long confirmed):** `lab.yml` push-to-`main` path repeatedly orphaned `main`. The guard(s) now make that path abort instead of orphaning; but the EXISTING orphan of the obsidian branch must still be repaired by rebasing the BRANCH onto main (force-push branch only).
- **FALSE-POSITIVE TRAP (still live):** shallow clone can fake a clean merge-base. Any re-link verification MUST do a FULL `git fetch` and treat empty `git merge-base` as the blocker.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub's naive auto-close regex matches the literal token `Closes #68` ANYWHERE in a merged commit message. PR #91's commit `c043b7e` contained `(Closes #68)`; after its merge GitHub auto-closed #68; the 02:00Z run reopened it. PR #92's merge added ONLY `Refs`-token commits (`dd902b1`, `efe286f`, `d6b2894`), so NO new auto-close was triggered; #68 is OPEN.
- **Lesson locked in:** never write the literal `Closes #68` token in ANY commit message or PR body. Future Factory/Builder/Lab commits must avoid it.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** OPEN, stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 target PR #83** (branch `opencode/issue68-20260818070512`, head `0deef55`):
  - **DEFAULT shipped codec = 9.5208 bpp mean** (R10-B CFL). Beats optipng PNG (13.05) and WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
  - **R11-D (MA-tree / property-tree in-loop context)** is the escalated next step; blueprint ALREADY EXISTS on-branch. Worst case ships unchanged 9.5208.

## In flight

- **PR #92 (Lab infra, integrity guard + umbrella rule + force-with-lease pin):** MERGED this run (rebase, branch kept). `main` = `d6b2894`.
- **Lab #68 (RE-DISPATCHED THIS run, run 32323492937, will post `/oc lab #68`):** actually re-link the orphaned obsidian branch onto `main` (rebase branch onto main, force-push BRANCH ONLY) + reopen PR #83. The guard is now merged, so the re-link is safe. MUST verify with a FULL fetch that `git merge-base` is non-empty before claiming success. This is the THIRD+ re-dispatch of the re-link; if it again only re-asserts guard work, the next run must escalate to a direct re-link inspection (verify via `gh run list --workflow opencode.yml` for a #68 run that performed the rebase).
- **PR #83 (Obsidian):** CLOSED, UNREOPENABLE until the branch re-link lands.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above (default 9.5208); the hard long pole. R11-D is the next blueprinted attempt.
- **Reopen PR #83** once the branch is re-linked (Lab #68) - restores the one-PR rule.
- **Resume Builder (R11-D) via `continue`** immediately after #83 reopens.
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once JXL nears / #83 reopens).
- **Review staleness on #83:** head `0deef55` un-reviewed. Fresh review required pre-merge.
- **Commit-message hygiene:** never write the literal `Closes #68` token in ANY commit message or PR body (double-confirmed).

## Issues

- **#68 (Obsidian umbrella)** - OPEN (safe through #92 merge), active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#52 / #89 / #90 / #91 / #92 infra** - #90 MERGED; #89 CLOSED; #52 related infra merged; #91 MERGED (guard); #92 MERGED this run (guard + umbrella rule + force-with-lease pin).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule; board live.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.
- **#71/#72/#73/#74/#75 (prior audit bugs)** - all CLOSED; root causes fixed on main.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894` (after PR #92). No `CreditsError` in recent runs.
- **PR #92:** MERGED this run (reviewer-approved; body already `Refs #68`; only `Refs`-token commits merged; #68 stays OPEN). Reviewer's advisory resolved by commit `d6b2894`.
- **Branch `opencode/issue68-20260818070512`:** confirmed intact on origin (head `0deef55`), NOT deleted. Orphaned from main (empty merge-base) - re-link pending via re-dispatched `lab #68`.
- **pages.yml:** triggered manually this run (run 32323756029) after the PR #92 merge; verify it completes green.

## Next steps

1. **Lab #68 (RE-DISPATCHED THIS run):** re-link the orphaned obsidian branch onto `main` (rebase branch onto origin/main, force-push BRANCH ONLY, do NOT touch main), then reopen PR #83, and re-verify `git merge-base` is non-empty + PR #83 OPEN. The orphan-main guard from #91/#92 now prevents re-orphaning. MANDATORY: full `git fetch` + real `git merge-base` non-empty check. If this re-dispatch again fails to re-link (only guard work), the next run escalates to a direct re-link inspection.
2. **After branch re-link + #83 reopen:** resume `continue` on PR #83 to implement **R11-D (MA-tree context)** from the existing blueprint, re-measure REAL Kodak effort-4 against the JPEG XL 8.71 gate.
3. **After R11-D measured:** if JPEG XL gate clears (default < 8.71 bpp, alongside PNG 13.05 + WebP 9.61), rebase-merge (`--no-delete-branch`) - but ONLY after `main` is re-linked - then close #68.
4. **README / index.html promotion:** schedule once JXL nears / PR reopens.

## Open questions

- **Will THIS `lab #68` re-dispatch actually re-link?** Prior `lab #68` runs (01:47Z owner, 01:35Z, 01:44Z, 02:00Z) produced ONLY guard PRs (#91, #92) and NEVER performed the branch re-link. This re-dispatch is scoped explicitly and narrowly to the re-link + PR #83 reopen, with a warning against guard-only output. If it again skips the re-link, escalate to a direct re-link inspection next run (verify via `gh run list --workflow opencode.yml`).
- **Will R11-D clear the +0.81 JPEG XL gap on REAL Kodak?** Blueprint on-branch; verdict pending the Builder's R11-D build + real-Kodak re-measure. NOT yet a 100%-certain unmovable wall.
- **Merge gate (owner override #2):** NOT met - default 9.5208 bpp beats PNG (13.05) + WebP (9.61) but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **One-PR integrity (TEMPORARILY BROKEN by infra):** zero open Obsidian PRs until #83 reopens (orphan-branch block). #68 OPEN until codecs beaten.
- **pages.yml:** triggered manually (32323756029) after PR #92 merge; verify green.
- **Billing:** resolved (no `CreditsError` in recent runs; `small_model` correctly pinned free).

- Mae, the Maintainer
