# STATE - Random factory checkpoint
- **Updated:** 2026-08-22 (maintainer run 32544216407, EVENT `created` on issue #120 ~01:42Z). Fresh survey confirms: PR #118 has a genuine `continue` build IN FLIGHT (`32544081395`, head `7fe10e0`, B5.20, 11.119 bpp). PR #119 still stale/conflicting (target #98 already CLOSED; workflow-file push wall). NEW: audit issue #120 confirms the `workflows`-scope wall + missing `lab` job as a blocking infra defect.
- **PR #118 (Prism M1-M4) REMAINS the active priority.** Branch `opencode/117-prism-m1-m4-optimization` = head `7fe10e0c0ccc71776fcd9f03aaf9d98ff30fa422` (B5.20, 11.119 bpp, byte-exact, MERGEABLE, shares `main` ancestry NOT orphan). As of this run a `continue` build IS in flight (run `32544081395`, `in_progress`, started 01:39:49Z). A second owner `/oc continue` (01:39:47Z) queued run `32544088481` (`pending`) - trails behind with `cancel-in-progress: false`, harmless. No duplicate `continue` dispatched. M3 < 8.71 bpp gate firmly UNMET -> NO merge.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; docs cleaned by merged PR #116). Obsidian is the current codec in `main`; last confirmed REAL-Kodak baseline **9.5209 bpp**. #68 (Obsidian umbrella) is now CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - upgrade over Obsidian, beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation in flight (issue #117, PR #118). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71). The merge gate is tied to the ACTUAL project goal, not any iteration/round limit; never merge incomplete work simply because a round or iteration limit was reached.
- **One-PR rule + NEVER delete PR branches:** satisfied (PR #116 and #104 branches retained after merge).
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Quality-gate directive:** quality gates are the ONLY merge criteria.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `02c0fb556d50be4ea056a734da7957420e9357b5`** (post PR #116 merge). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/117-prism-m1-m4-optimization` = `7fe10e0` shares M0 ancestry (NOT orphan).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** production deploy succeeded (main). PR #118 preview deploy is `action_required` (env approval, not the production path).
- **`lab` PATH IS STILL BROKEN (critical, now confirmed by audit #120):** `opencode.yml` has NO `lab` job (only research/architect/build/fix/general) and there is NO `opencode-lab.yml` workflow file. Therefore `/oc lab` (and `/oc auditor`) comments produce only SKIPPED runs, so The Lab Engineer CANNOT be dispatched via `/oc lab` - the silent-stall root-cause fix remains a NO-OP, and no bot can self-heal workflow-file PRs either. Mae's model-fallback policy restricts direct workflow edits to model switching only, so Mae cannot wire the `lab` job herself; this needs the owner to add the job (or authorize it).
- **WORKFLOW-FILE PUSH WALL (now formally audited as #120):** the lab's GitHub App lacks the `workflows` scope, so pushes that touch `.github/workflows/*.yml` are rejected at push. PR #119 proves this (multiple `/oc fix` attempts `remote rejected ... without workflows permission`). Consequence: any future workflow-file PR cannot be fixed by the Fixer/Lab Engineer; the owner must grant `workflows: write` or apply the change manually. Audit #120 proposes the fix: add `workflows: write` to the `permissions:` block of opencode.yml, lab.yml, maintainer.yml, opencode-recover.yml, opencode-review.yml, opencode-test.yml, pages.yml.

## IN FLIGHT
- **Prism M1-M4 (issue #117, PR #118, branch `opencode/117-prism-m1-m4-optimization`):** optimization loop. Head `7fe10e0` (B5.20, 11.119 bpp, byte-exact, harness ~160s). As of run 32544216407 a `continue` build IS in flight (run `32544081395`, `in_progress`, started 01:39:49Z). A duplicate owner `/oc continue` (01:39:47Z) queued run `32544088481` (`pending`) - trails behind, harmless. No duplicate `continue` dispatched.
  - B6: 5/3 lifting + int32 color widening for BD16 (M2 < 9.71).
  - B7: Squeeze + MA-tree greedy split with mandatory llc_class/sibling_class (M3 < 8.71 - the crux, ~2.41 bpp gap).
  - B8 (CM + LZP never-expand net, M4 < 8.0) deferred until M3 in reach.
- **PR #119 (`[Infra] Lab update for #98`/erroneously `#70`) - STALE / OWNER ESCALATION (NOT in flight by a bot).** Branch `opencode/lab-98-runaway-fix-retry`, head `eac12c1`, `mergeable=CONFLICTING`/`DIRTY`. Its body says `Closes #70` but the actual fix targets #98, which is NOW CLOSED (fix landed via PR #99 + Lab Engineer run `32540682703`). So the PR's premise is largely resolved in `main`; what remains is a conflicting workflow-file delta the bot cannot push (workflows-scope wall). Will become fully redundant once audit #120's `workflows: write` fix is applied; Mae will close it as redundant at that point.

## PENDING (in order)
1. **Prism M1-M4 (PR #118):** a `continue` build IS in flight (run `32544081395`, head `7fe10e0`, B5.20, 11.119 bpp) from the owner's `/oc continue` at 01:39:47Z; it resumes B6-B8 toward M3 < 8.71 bpp on real Kodak bit-exactly; then Reviewer -> Tester (real Kodak, bit-exact, bpp gates M1<13.05 & <9.61, M2<9.71, M3<8.71). HOLD merge until M3 met bit-exactly per owner override. Do NOT dispatch a second `continue` while one is active.
2. **OWNER ESCALATION - audit #120 (workflows: write + wire `lab` job):** the Auditor confirmed (issue #120) that the App lacks `workflows` scope and `opencode.yml`/its siblings omit `workflows: write`, and that the `lab` job is wired nowhere. Resolution requires OWNER: (a) grant the GitHub App `Workflows` permission, (b) wire a `lab` job so The Lab Engineer can run. Mae cannot apply this (lab job unwired -> `/oc lab` no-ops; push wall blocks workflow-file pushes; not an extreme emergency since builds/reviews/tests still run). Mae posted the escalation as a bot comment on #120.
3. **PR #119 OWNER ESCALATION (stale):** #98 is CLOSED; the branch is CONFLICTING and carries a workflow-file change the bot cannot push (workflows permission wall). Once audit #120's fix lands, close #119 as redundant. The substantive #98 pagination/API-refusal fix already landed in `main` (PR #99 + run `32540682703`).
4. **Silent-stall diagnosis (BLOCKED by #2):** owner `/oc continue` produced skipped/cancelled opencode runs intermittently earlier (23:16/23:58/00:23/00:55Z stalls). At 01:26:01Z and 01:39:47Z the owner's `/oc continue` launched a real build (`32543408136`, then `32544081395`, both in_progress) - the pattern is intermittent, not a hard block. The underlying opencode.yml issue_comment dispatch bug remains undiagnosed because the Lab Engineer cannot run (no `lab` job). Keep re-dispatching `continue` as the mitigation when a stall is detected; do NOT re-issue `/oc lab` (confirmed no-op, only adds skipped-run noise).
5. **#42 Board resume (parked):** Ideator batch posted; PARKED behind Prism per owner directive.
6. **entropy-architecture.md archive follow-up (non-blocking, Reviewer design note):** authoritative doc for the shipped rANS backend, still cited by live code; consider un-archiving or a clearer label.
7. **Circuit-breaker false-trip fix (root cause):** breaker counts Maintainer's own status comments (embedding dispatch keywords). Harden `loop-budget.sh` to exclude Maintainer status comments (a `lab` change, blocked by #2 + the workflows-scope PAT wall until owner regenerates `OPENCODE_PAT`). Short-term: keep bot comments free of literal dispatch-keyword phrases.
8. **Benign agent `git push` fatal-error noise (non-blocking):** the opencode agent sometimes runs a bare `git push` (upstream mismatch) inside the session; the harness push (explicit refspec + verify/auto-retry) still delivers, as proven by the branch advancing. Optional `lab` follow-up to steer the agent away from bare `git push` (blocked by #2). Deferred until the build loop is not mid-flight.
9. **Verify PR #118 pages preview:** currently `running`? Preview deploy is `action_required` (env approval) - owner-side, not a production blocker.

## ISSUES
- **#68 (Obsidian umbrella)** - CLOSED (docs cleaned by merged #116).
- **#103 (Prism)** - CLOSED (merged via #104); M1-M4 continuation in flight via issue #117 + PR #118.
- **#117 (Prism M1-M4)** - OPEN (tracking issue; explicit objective + goal-tied merge gate). Also the (currently dead) target of the `lab` silent-stall fix because the `lab` job is unwired.
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor owns daily summary. NOTE: PR #119 body erroneously says `Closes #70`; the actual fix targets #98 (now CLOSED).
- **#98 (runaway /oc fix retry loop)** - CLOSED (fix landed via PR #99 + Lab Engineer run `32540682703`); PR #119 is now a stale/conflicting carry of the same work.
- **#120 (Audit: workflows: write missing)** - OPEN (created by Auditor 2026-08-22). Confirms the workflow-file push wall + missing `lab` job as a blocking infra defect. Mae escalated to owner (cannot self-heal). Resolution: owner grants App `workflows` scope + wires `lab` job; then PR #119 can be driven via `/oc fix` and closed as redundant.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `02c0fb556d50be4ea056a734da7957420e9357b5`.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed via #111).
- **`lab.yml` Lab Engineer pin:** N/A - there is no `lab` job/workflow; the Lab Engineer cannot currently be dispatched via `/oc lab` (see CRITICAL INFRASTRUCTURE STATE).
- **Circuit breaker:** RESET (counter 0). Owner re-issued directive (quality gate, not the breaker, governs merges).

## NEXT STEPS
1. Prism M1-M4 (PR #118): build `32544081395` (head `7fe10e0`, B5.20, 11.119 bpp) is in flight from the owner's `/oc continue` 01:39:47Z, resuming B6-B8 toward M3 < 8.71 bpp on real Kodak bit-exactly. Then Reviewer -> Tester (real Kodak, bit-exact, bpp gates); HOLD merge until M3 met bit-exactly per owner override. Do not dispatch a duplicate `continue`.
2. **Audit #120 OWNER ESCALATION:** request owner grant App `workflows: write` + wire the `lab` job so The Lab Engineer can self-heal workflow-file PRs. Until then no bot can apply the fix; Mae's comment on #120 states this plainly.
3. **PR #119 (stale):** close as redundant once audit #120's fix lands (substantive #98 content already in `main`).

## OPEN QUESTIONS
- Prism #118: will the in-flight `continue` (`32544081395`) iterate past ~11.119 bpp (B5.20) toward M3 < 8.71 on REAL Kodak bit-exactly? Owner override: no merge until M0+M1+M2+M3 met bit-exactly.
- Prism #118: when stable at/under the gate, fire Reviewer -> Tester before any merge.
- **Audit #120 / WORKFLOW-FILE PUSH WALL:** will the owner grant the App `workflows: write` and wire the `lab` job? This is the single unblock for every future workflow-file PR (including the stalled PR #119).
- **PR #119:** #98 is now CLOSED. Will become redundant once #120 lands; Mae will close it then.
- **`lab` PATH BROKEN:** opencode.yml has no `lab` job and `opencode-lab.yml` does not exist, so `/oc lab` no-ops. Will the owner wire the `lab` job? Mae's only mitigation for the silent-stall is re-dispatching `continue`.
- Silent-stall root cause: owner `/oc continue` intermittently fails to launch a build (skipped/cancelled) but at 01:26:01Z and 01:39:47Z it DID launch real builds. Intermittent. Needs the Lab Engineer, which is currently unreachable. Mitigation: re-dispatch `continue` on detected stall.
- entropy-architecture.md: should the authoritative rANS design doc be un-archived (Reviewer design note, non-blocking)?
- Circuit-breaker false-trip: will the `OPENCODE_PAT` workflows-scope wall ever be lifted so the `lab` fix can land? Short-term mitigation in force.
- Agent bare `git push` fatal-error noise: optional `lab` cleanup after the build loop is not mid-flight (blocked by missing lab job).

- Mae, the Maintainer
