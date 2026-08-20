# STATE - Random factory checkpoint

- **Updated:** 2026-08-20 (~01:44Z, maintainer event run 32322083771, triggered by issue #70 re-creation). Re-dispatched `lab #68` to re-link orphan `main` with the Obsidian branch and reopen PR #83. CRITICAL finding: the 01:35Z run already wrote this same `lab #68` decision but NO executing opencode-lab run resulted, and the only lab run since (32321789222, owner's direct /oc lab) was a DIAGNOSTIC PASS that FALSELY claimed a clean merge base at 1709943 (shallow-clone false positive). The orphan-main blocker is therefore STILL LIVE. This run re-dispatches with an explicit full-fetch + real-merge-base re-verification guard.

## STANDING OWNER DIRECTIVES (do not close / do not delete)

- **Obsidian is the fundamental goal.** Keep iterating until it beats JPEG XL, WebP, and PNG (lossless) on the Kodak dataset. Issue #68 stays OPEN until the target is met. Do NOT close it.
- **NEVER delete PR branches after merge.** Omit `-d` from every `gh pr merge`.
- **Website + README must track the active project.** Obsidian should be in README.md (Current Project) and promoted to Current on index.html. Still NOT satisfied (deferred); WebP cleared, schedule once JXL nears / #83 reopens.

## CRITICAL OWNER OVERRIDES (issue #68)

1. **ONE Obsidian PR only.** Single open PR iterating on the SAME branch via resume (`/oc continue`) until the goal is reached. Redundant codec-rebase PR #84 and redundant research PR #87 were CLOSED; their docs preserved on #83. A fresh `/oc build this` does NOT override this - route to `continue` on the existing PR. (Currently VIOLATED: zero open Obsidian PRs because #83 is closed.)
2. **DO NOT merge the Obsidian PR until the final target is achieved** (Obsidian mean bpp on Kodak < WebP 9.61 AND < optipng PNG 13.05 AND < JPEG XL 8.71, lossless/bit-exact AND reproducible, by the *default* shipped codec). Overrides the prior incremental-per-milestone merge plan.
3. **Orchestrate Researcher + Architect + Builder together** on the existing single PR #83 (or issue #68 for factory/lab) - not on a new PR.

## CRITICAL INFRASTRUCTURE STATE (orphan-main break - STILL A HARD BLOCKER; re-dispatch fired this run)

- **PR #83 is CLOSED** (2026-08-19T18:59:40Z, not merged). `gh pr reopen` / `gh api PATCH state=open` both FAIL: branch `opencode/issue68-20260818070512` has no history in common with `main`. Error verbatim: "state cannot be changed. The opencode/issue68-20260818070512 branch has no history in common with main."
- **`main` = `1709943`** (single orphan commit "Rename Factory Engineer agent to Lab Engineer", pushed 2026-08-19T18:59:41Z). `git merge-base origin/main origin/opencode/issue68-20260818070512` is EMPTY (exit 1) - RE-VERIFIED live this run with a full `git fetch`.
- **Branch is RECOVERABLE and INTACT:** `opencode/issue68-20260818070512` still exists on origin (head `0deef55`) - it holds the 9.5208 codec + the R11-D blueprint (`obsidian/docs/architect-r11-crossband-predictor-blueprint.md`). Kodak corpus durable in git.
- **Root cause (confirmed):** `lab.yml` push-to-`main` path repeatedly orphans `main` as a single root commit with no parent, breaking every feature branch's merge-base. The Lab Engineer must change this path to always apply edits ON TOP of fetched `origin/main` (fetch, reset --hard origin/main, apply, commit, push).
- **FALSE-POSITIVE TRAP (this run learned):** a shallow clone makes `main` appear to be the branch's base, so a naive `git merge-base` check can report a "clean merge base at 1709943" when in reality there is none. The 01:39Z lab diagnostic (32321789222) fell into this and reported success without doing the re-link. Any future re-link verification MUST do a FULL `git fetch` and treat an empty `git merge-base` output as the blocker.
- **Execution gap:** the 01:35Z maintainer run (32321546193) wrote the correct `lab #68` decision, but no opencode-lab run for #68 actually executed. This run (32322083771) re-dispatches `lab #68` with the same repair + the false-positive guard. If this re-dispatch ALSO yields no executing lab run, the next maintainer run must investigate why the hardcoded owner-trigger post is not spawning opencode-lab.yml (see open questions).

## SYSTEMIC INFRASTRUCTURE BLOCKER (commit-message auto-close)

- GitHub's naive auto-close regex matches the literal token `Closes #68` ANYWHERE in a merged commit message, even inside quotes/negations. PR #90's merge commit `b85f30e` body said "no longer uses 'Closes #68'", which auto-closed #68. **Future Factory/Builder commits must NEVER write the literal phrase `Closes #68` (even quoted/negated).** #68 was reopened; stays OPEN.

## Priority project (the fundamental goal)

- **Issue #68 (Obsidian: lossless image-compression codec competitive with JPEG XL / WebP, Kodak-benchmarked).** OPEN (recreated), stays OPEN until codecs beaten.
- **M0 COMPLETE & MERGED** (PR #82).
- **M1 OPEN as PR #83** (single canonical PR branch `opencode/issue68-20260818070512`, head `0deef55`):
  - **DEFAULT shipped codec = 9.5208 bpp mean** (R10-B CFL committed; real Kodak effort-4, reproducible). Beats optipng PNG (13.05) and WebP (9.61) - both gates MET. **JPEG XL 8.71 MISSED by ~0.81 bpp** (17/24 images above). Bit-exact. (Auditor's 08-20 report cites 9.7094 for an R8 adaptive-predictor mid-build variant - that still misses JXL by ~0.1; the default shipped codec is 9.5208.)
  - **R11-A (cross-band in-loop predictor) WASHED:** implemented, measured 9.5091 bpp (~0.01 bpp wash) AND made encode 45x slower. Reverted (`c7aa1a3`) and re-verified 9.5208 at `0deef55` (136 tests pass).
  - **R11-D (MA-tree / property-tree in-loop context) is the escalated next step** - fold the co-located LL sample + weight-context (`wc`, R9-B) into the CMARC quotient context for HF bands. The blueprint ALREADY EXISTS in `obsidian/docs/architect-r11-crossband-predictor-blueprint.md` (R11-D section). No new Architect run needed. Worst case ships unchanged 9.5208 (no regression).

## In flight

- **PR #83 (Obsidian, branch `opencode/issue68-20260818070512`, head `0deef55`):** CLOSED and currently UNREOPENABLE (orphan-main hard block). Branch confirmed intact on origin. Will be reopened once `main` is re-linked by the Lab Engineer.
- **Lab #68 (RE-DISPATCHED THIS run, run will post `/oc lab #68`):** durably re-link `main` (rebase branch onto main, force-push branch ONLY, do NOT touch main) + fix the orphan-force-rewrite recurrence root cause in `lab.yml` + reopen PR #83. MUST verify with a FULL fetch that `git merge-base` is non-empty before claiming success.

## PENDING (deferred)

- **Clear JPEG XL 8.71 gate:** ~0.81 above (default 9.5208); the hard long pole. R11-D (MA-tree context) is the next blueprinted attempt. Needs real-Kodak re-measure after build.
- **Reopen PR #83** once `main` is re-linked (Lab #68) - restores the one-PR rule.
- **Resume Builder (R11-D) via `continue`** immediately after #83 reopens - implement MA-tree context from the existing blueprint, re-measure REAL Kodak effort-4, record `benchmarks/results/2026-08-20-r11d-*.csv`.
- **README / index.html Obsidian promotion** (standing directive, deferred; schedule once JXL nears / #83 reopens).
- **Review staleness on #83:** current head `0deef55` un-reviewed (well past last approve ~96a6075). Fresh review required pre-merge.
- **Commit-message hygiene:** never write the literal `Closes #68` token in any commit message.
- **Investigate why 01:35Z `lab #68` trigger did not spawn an opencode-lab run** if this re-dispatch also fails to execute.

## Issues

- **#68 (Obsidian umbrella)** - OPEN (recreated); active fundamental goal, stays open until codecs beaten. Single-PR + no-merge-until-target + orchestrate-R/A/B overrides active.
- **#52 / #90 / #89 infra** - PR #90 MERGED (infra hardening shipped); #89 CLOSED (merged via #88); #52 related infra merged.
- **#70 (Lab Health)** - Auditor owns the daily summary on schedule; board re-created 01:44Z. Maintainer run 32322083771 acknowledged on #70.
- **#42 (Brainstorm Board)** - frozen until ideas wanted; Obsidian takes priority.
- **#71/#72/#73/#74/#75 (prior audit bugs)** - all CLOSED; root causes fixed on main (build-verify false positive, review-crash guard, billing resolved).

## Reviewer/Tester/model status

- **Model config:** `opencode.json` model `opencode/hy3-free`, `small_model: opencode/mimo-v2.5-free` (both free). `origin/main` = `1709943` (orphan, single commit). All workflow `model:` inputs `opencode/hy3-free`. No `CreditsError` in recent runs (billing block resolved).
- **PR #83:** CLOSED (18:59:40Z, not merged), head `0deef55`, UNREOPENABLE until `main` re-linked. Default 9.5208 (PNG 13.05 + WebP 9.61 MET; JXL 8.71 unmet by +0.81). R11-A washed + reverted; R11-D next (blueprint already on-branch).
- **Branch `opencode/issue68-20260818070512`:** confirmed intact on origin (head `0deef55`), NOT deleted. Holds 9.5208 codec + R11-D blueprint + Kodak corpus.

## Next steps

1. **Lab #68 (RE-DISPATCHED THIS run):** re-link `main` to share history with the obsidian branch by rebasing the branch onto `main` and force-pushing ONLY the branch (do NOT touch `main`); then reopen PR #83; FIX the orphan-force-rewrite root cause in `lab.yml` (push-to-main path must keep continuous history). MANDATORY: full `git fetch` + real `git merge-base` non-empty check before success claim (avoid the shallow-clone false positive).
2. **After `main` re-link + #83 reopen:** resume `continue` on PR #83 to implement **R11-D (MA-tree context)** directly from the existing blueprint (`architect-r11-crossband-predictor-blueprint.md`), re-measure REAL Kodak effort-4 against the JPEG XL 8.71 gate, record `benchmarks/results/2026-08-20-r11d-*.csv`. Worst case ships unchanged 9.5208 (no regression).
3. **After R11-D measured:** if JPEG XL gate clears (default < 8.71 bpp, alongside PNG 13.05 + WebP 9.61), rebase-merge (`--no-delete-branch`) - but ONLY after `main` is re-linked - then close #68.
4. **README / index.html promotion:** schedule a Builder/Lab pass to promote Obsidian as Current now that WebP is cleared.

## Open questions

- **Will THIS `lab #68` re-dispatch actually execute?** The 01:35Z `lab #68` decision never spawned an opencode-lab run. If this re-dispatch also fails to execute, the next maintainer run must inspect `gh run list --workflow opencode-lab.yml` for a #68-triggered run and, failing that, treat it as an infra defect in the trigger-post step. High confidence the repair itself works IF the lab run executes (rebase branch onto main is mechanical).
- **Will R11-D (MA-tree / property-tree in-loop context) clear the +0.81 JPEG XL gap on REAL Kodak?** R11-A (cross-band predictor) washed; R11-D (fold co-located LL + weight-context into the CMARC quotient context) is the escalated remaining blueprinted lever, and its blueprint ALREADY EXISTS on the branch. WebP is cleared; JPEG XL is the hard long pole. Empirical verdict pending the Builder's R11-D build + real-Kodak re-measure. NOT yet a 100%-certain unmovable wall.
- **Merge gate (owner override #2):** NOT met - default 9.5208 bpp beats PNG (13.05) + WebP (9.61) but > 8.71 JXL. No merge until all three gates clear bit-exactly and reproducibly by the default codec.
- **Review staleness on #83:** current head `0deef55` un-reviewed. Fresh review required pre-merge.
- **README/index promotion gap:** Obsidian not promoted as Current despite the standing directive (WebP gate cleared); schedule once JXL nears / PR reopens.
- **One-PR integrity (TEMPORARILY BROKEN by infra):** zero open Obsidian PRs until #83 reopens (orphan-main block). #68 OPEN until codecs beaten. Upon `main` re-link, reopen #83 as the sole canonical Obsidian PR.
- **Billing:** resolved (no `CreditsError` in recent runs; `small_model` correctly pinned free).

- Mae, the Maintainer
