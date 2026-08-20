# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~02:14Z, maintainer event run 32323750782, late firing of the PR #92 creation event). PR #92 was ALREADY fully merged by the prior run 32323492937 (`main` = `d6b2894`, body `Refs #68`, #68 OPEN, pages green). This run found nothing pending for #92. The sole live blocker remains the orphaned obsidian project branch, and a `lab #68` re-link run (32323874365) is IN PROGRESS (started 02:13:30Z). Awaiting its result; did NOT re-dispatch (no-duplicate-while-in-progress rule).

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it. (#68 reopened 02:00Z; safe through PR #91/#92 merges.)
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`. (PR #91 + #92 branches `opencode/lab-68-orphan-main-guard` intentionally left intact.)
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. Still NOT satisfied (deferred); schedule once JXL nears / #83 reopens.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Currently VIOLATED: zero open Obsidian PRs because #83 is still CLOSED (orphan-branch block not yet resolved).
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec).
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83 (or issue #68 for factory/lab) - not on a new PR.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break - GUARDS MERGED, branch re-link STILL PENDING + IN PROGRESS)

- **PR #91 MERGED (02:00Z):** commit `c043b7e` orphan-main guard live on `main`.
- **PR #92 MERGED (02:11Z, prior run 32323492937):** `main` = `d6b2894`. Adds integrity guard (`efe286f`, `dd902b1`), the "do not auto-close Obsidian umbrella" rule (`dd902b1`), and the force-with-lease pin on integrity-guard restore (`d6b2894`). The Reviewer's advisory is RESOLVED by `d6b2894`.
- **`main` = `d6b2894`** (after PR #92). The obsidian branch `opencode/issue68-20260818070512` (head `0deef55`) STILL has an EMPTY merge-base with `main` - it is still orphaned (confirmed by full `git fetch` + real merge-base test THIS run). PR #83 still CLOSED.
- **Branch is RECOVERABLE and INTACT:** `opencode/issue68-20260818070512` still exists on origin (head `0deef55`) - holds the 9.5208 codec + R11-D blueprint. Kodak corpus durable in git.
- **Root cause (long confirmed):** `lab.yml` push-to-`main` path repeatedly orphaned `main`. The guard(s) now make that path abort instead of orphaning; but the EXISTING orphan of the obsidian branch must still be repaired by rebasing the BRANCH onto main (force-push branch only).
- **FALSE-POSITIVE TRAP (still live):** shallow clone can fake a clean merge-base. Any re-link verification MUST do a FULL `git fetch` and treat empty `git merge-base` as the blocker.
- **IN-PROGRESS RE-LINK ATTEMPT:** `lab #68` run 32323874365 (`Opencode Lab Engineer`, status in_progress, started 02:13:30Z) is the explicit re-link mandate from the prior run. Awaiting its outcome; this run did NOT re-dispatch a duplicate.

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close) - UNDER CONTROL

- GitHub's naive auto-close regex matches the literal token `Closes #68` ANYWHERE in a merged commit message. PR #91's commit `c043b7e` contained `(Closes #68)`; after its merge GitHub auto-closed #68; the 02:00Z run reopened it. PR #92's merge added ONLY `Refs`-token commits (`efe286f`, `dd902b1`, `d6b2894`), so NO new auto-close was triggered; #68 is OPEN.
- **Lesson locked in:** never write the literal `Closes #68` token in ANY commit message or PR body. Future Factory/Builder/Lab commits must avoid it (use `Refs #68` / `Refs to #68`).

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** OPEN, stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 target PR #83** (branch `opencode/issue68-20260818070512`, head `0deef55`):
  - **DEFAULT shipped codec = 9.5208 bpp mean** (R10-B CFL). Beats optipng PNG (13.05) and WebP (9.61). **JPEG XL 8.71 MISSED by ~0.81 bpp.** Bit-exact.
  - **R11-D (MA-tree / property-tree in-loop context)** is the escalated next step; blueprint ALREADY EXISTS on-branch. Worst case ships unchanged 9.5208.

## In flight

- **PR #92 (Lab infra):** MERGED by prior run 32323492937 (rebase, branch kept). `main` = `d6b2894`. Nothing pending this run.
- **Lab #68 re-link run 32323874365 (IN PROGRESS, started 02:13:30Z):** the mandated branch re-link (rebase branch onto origin/main, force-push BRANCH ONLY) + reopen PR #83. This run AWAITED it (no duplicate dispatch). MUST verify via full `git fetch` that `git merge-base` is non-empty + PR #83 OPEN once it completes. If it again ships only guard work (the recurring misinterpretation), the NEXT run escalates to a DIRECT re-link inspection (verify no #68 run performed the rebase; if the Lab Engineer cannot, ping #68 + ask owner for a manual branch re-link, since Mae cannot push the branch under this envelope).
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
- **#52 / #89 / #90 / #91 / #92 infra** - #90 MERGED; #89 CLOSED; #52 related infra merged; #91 MERGED (guard); #92 MERGED (guard + umbrella rule + force-with-lease pin).
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule; board live.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.
- **#71/#72/#73/#74/#75 (prior audit bugs)** - all CLOSED; root causes fixed on main.

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `d6b2894`. No `CreditsError` in recent runs.
- **PR #92:** MERGED by prior run (reviewer-approved; body `Refs #68`; only `Refs`-token commits; #68 stays OPEN). No action this run.
- **Branch `opencode/issue68-20260818070512`:** confirmed intact on origin (head `0deef55`), NOT deleted. Orphaned from main (empty merge-base) - re-link IN PROGRESS via run 32323874365.
- **pages.yml:** green (32323873980). No action.

## Next steps

1. **Await `lab #68` run 32323874365** (in progress). On completion, re-verify with a FULL `git fetch` that `git merge-base origin/main origin/opencode/issue68-20260818070512` is NON-EMPTY and PR #83 is OPEN.
2. **IF 32323874365 re-linked + reopened #83:** fire `continue` on PR #83 to implement **R11-D (MA-tree context)** from the existing blueprint, re-measure REAL Kodak effort-4 against the JPEG XL 8.71 gate.
3. **IF 32323874365 again shipped only guard work:** ESCALATE next run to a DIRECT re-link inspection - verify via `gh run list --workflow opencode.yml` that no #68 run performed the rebase; then force a re-link-focused `lab #68` whose message names the branch verbatim (`rebase opencode/issue68-20260818070512 onto origin/main, force-push that branch, reopen PR #83`). If the Lab Engineer still cannot (workflows-permission / misinterpretation), ping #68 and ask the owner for a manual branch re-link (Mae cannot push the branch under this envelope).
4. **After R11-D measured:** if JPEG XL gate clears (default < 8.71 bpp, alongside PNG 13.05 + WebP 9.61), rebase-merge (`--no-delete-branch`) - but ONLY after `main` is re-linked - then close #68.
5. **README / index.html promotion:** schedule once JXL nears / PR reopens.

## Open questions

- **Will the IN-PROGRESS `lab #68` run 32323874365 finally re-link?** It is the re-dispatch with the narrow, explicit re-link mandate. Verification pending its completion.
- **Why does `lab #68` keep shipping guards instead of re-linking?** Hypothesis: `lab.yml` resolves "issue #68" to the orphan-main DEFECT and hardens the guard, rather than re-linking the specific orphaned branch. Next attempt must name the branch explicitly.
- **Will R11-D clear the +0.81 JPEG XL gap on REAL Kodak?** Blueprint on-branch; verdict pending the Builder's R11-D build + real-Kodak re-measure. NOT yet a 100%-certain unmovable wall.
- **Merge gate (owner override #2):** NOT met - default 9.5208 bpp beats PNG (13.05) + WebP (9.61) but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **One-PR integrity (TEMPORARILY BROKEN by infra):** zero open Obsidian PRs until #83 reopens (orphan-branch block). #68 OPEN until codecs beaten.
- **pages.yml:** green. No action.
- **Billing:** resolved (no `CreditsError` in recent runs; `small_model` correctly pinned free).
- **workflows-permission gap:** App token lacks `workflows: write`; merges via `gh pr merge` still work, but `lab`/`fix` paths that commit workflow files will fail and need the owner PAT.

- Mae, the Maintainer
