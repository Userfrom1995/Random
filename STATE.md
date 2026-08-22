# STATE - Random factory checkpoint
- **Updated:** 2026-08-22 (maintainer run 32541547825, EVENT `issue_comment`/Reviewer escalation `/oc maintainer` on PR #119, ~00:49Z). This run resolves the PR #119 systemic roadblock as an owner-action escalation.
- **PR #118 (Prism M1-M4) REMAINS the active priority and is IN FLIGHT.** Branch `opencode/117-prism-m1-m4-optimization` = head `02153a3bfc5e8cfba0c2a55f30b272e358f8d7c0` (past B5.17, ~11.120 bpp, byte-exact, MERGEABLE, shares `main` ancestry NOT orphan). A `continue` build `32540331936` is `in_progress` (driving B6-B8); queued duplicate `32540394102` behind it. M3 < 8.71 bpp gate firmly UNMET -> NO merge.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; docs cleaned by merged PR #116). Obsidian is the current codec in `main`; last confirmed REAL-Kodak baseline **9.5209 bpp**.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - upgrade over Obsidian, beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation in flight (issue #117, PR #118). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71). The merge gate is tied to the ACTUAL project goal, not any iteration/round limit; never merge incomplete work simply because a round or iteration limit was reached.
- **One-PR rule + NEVER delete PR branches:** satisfied (PR #116 and #104 branches retained after merge).
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Quality-gate directive:** quality gates are the ONLY merge criteria.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `02c0fb556d50be4ea056a734da7957420e9357b5`** (post PR #116 merge). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/117-prism-m1-m4-optimization` = `02153a3` shares M0 ancestry (NOT orphan).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** production deploy `32536272428` succeeded (main). PR #118 preview deploy is `action_required` (env approval, not the production path).
- **`lab` PATH IS STILL BROKEN (critical finding, unchanged):** `opencode.yml` has NO `lab` job (only research/architect/build/fix/general) and there is NO `opencode-lab.yml` workflow file. Therefore `/oc lab` (and `/oc auditor`) comments produce only SKIPPED runs (seen as `32540394100`/`32540388073`, conclusion=skipped). This means The Lab Engineer CANNOT be dispatched via `/oc lab` - so the silent-stall root-cause fix escalated in run 32540175107 was a NO-OP, and (newly relevant) NO bot can self-heal workflow-file PRs either. The maintainer model-fallback policy restricts direct workflow edits to model switching only, so Mae cannot wire the `lab` job herself; this needs the owner to add the job (or authorize it).
- **NEW (this run): WORKFLOW-FILE PUSH WALL.** Even when a `lab` job exists, the lab's GitHub App lacks the `workflows` scope, so pushes that touch `.github/workflows/*.yml` are rejected at push. This was proven by PR #119: four `/oc fix` attempts (`32540846493`, `32540975338`, `32541117980`, `32541211675`, `32541362195`) were all `remote rejected ... without workflows permission`. Consequence: **any future workflow-file PR cannot be fixed by the Fixer/Lab Engineer; the owner must grant `workflows: write` or apply the change manually.**

## IN FLIGHT
- **Prism M1-M4 (issue #117, PR #118, branch `opencode/117-prism-m1-m4-optimization`):** optimization loop. Head `02153a3` (past B5.17, ~11.120 bpp, byte-exact, harness 134s). A `continue` build `32540331936` is `in_progress` (resumes B6-B8 from B5.17). Queued duplicate owner `/oc continue` `32540394102` (harmless).
  - B6: 5/3 lifting + int32 color widening for BD16 (M2 < 9.71).
  - B7: Squeeze + MA-tree greedy split with mandatory llc_class/sibling_class (M3 < 8.71 - the crux, ~2.41 bpp gap).
  - B8 (CM + LZP never-expand net, M4 < 8.0) deferred until M3 in reach.
- **PR #119 (`[Infra] Lab update for #70`) - ESCALATED TO OWNER (systemic roadblock, NOT in flight by a bot).** Branch `opencode/lab-98-runaway-fix-retry`, `mergeable=CONFLICTING`/`mergeStateStatus=DIRTY`. Core #98 fix (pagination + API refusal) is correct and must be preserved, but the Reviewer's blocking guard-short-circuit finding and `set +e` hardening CANNOT be applied by any bot (workflows permission wall). Owner action required (see PENDING #2).

## PENDING (in order)
1. **Prism M1-M4 (PR #118):** the in-flight `continue` (`32540331936`) resumes B6-B8 toward M3 < 8.71 bpp on real Kodak bit-exactly; then Reviewer -> Tester (real Kodak, bit-exact, bpp gates M1<13.05 & <9.61, M2<9.71, M3<8.71). HOLD merge until M3 met bit-exactly per owner override. Do NOT dispatch a second `continue` while one is active.
2. **PR #119 OWNER ESCALATION (CRITICAL, this run):** bot cannot self-heal a workflow-file PR. Required owner actions:
   (a) Apply the Guard short-circuit fix from the Reviewer (set `skip` output + gate `Capture baseline`/`Run opencode fix agent`/`Verify fix`/`Post /oc review` with `if: steps.guard.outputs.skip != 'true'`) - exact YAML in PR #119 comment;
   (b) `set +e` hardening in `Verify fix pushed` (re-enable `set -e` before the POST);
   (c) Resolve `Closes` target mismatch (body says #70, but branch/commits/code say #98);
   (d) Rebase/resolve the `CONFLICTING` state against current `main`;
   (e) OPTIONAL BUT RECOMMENDED: grant the GitHub App `workflows: write` so future workflow-file PRs can self-heal.
   The substantive #98 pagination/API-refusal fix must be kept either way.
3. **WIRE THE `lab` JOB (CRITICAL BLOCKER):** opencode.yml has no `lab` job and `opencode-lab.yml` does not exist, so `/oc lab` is a no-op. The owner must add a `lab` job to opencode.yml (modeled on the build job but running the Lab Engineer / LAB mode) so The Lab Engineer can run and fix the silent-stall dispatch logic AND (now also) future workflow-file PRs. Until then, the silent-stall root cause cannot be fixed by the Lab Engineer, and Mae's only mitigation is re-dispatching `continue` on detection.
4. **Silent-stall diagnosis (BLOCKED by #3):** owner `/oc continue` produced skipped/cancelled opencode runs THREE times (23:16:28Z `32536270442`; 23:58:52Z `32538794937`+`32538801477`; 00:23:08Z `32540175109`+`32540168896`) and a `continue` was re-dispatched each time. The underlying opencode.yml issue_comment dispatch bug remains undiagnosed because the Lab Engineer cannot run. Keep re-dispatching `continue` as the mitigation.
5. **#42 Board resume (parked):** Ideator batch posted; PARKED behind Prism per owner directive.
6. **entropy-architecture.md archive follow-up (non-blocking, Reviewer design note):** authoritative doc for the shipped rANS backend, still cited by live code; consider un-archiving or a clearer label.
7. **Circuit-breaker false-trip fix (root cause):** breaker counts Maintainer's own status comments (embedding dispatch keywords). Harden `loop-budget.sh` to exclude Maintainer status comments (a `lab` change, blocked by #3 + the workflows-scope PAT wall until owner regenerates `OPENCODE_PAT`). Short-term: keep bot comments free of literal dispatch-keyword phrases.
8. **Benign agent `git push` fatal-error noise (non-blocking):** the opencode agent sometimes runs a bare `git push` (upstream mismatch) inside the session; the harness push (explicit refspec + verify/auto-retry) still delivers, as proven by the branch advancing. Optional `lab` follow-up to steer the agent away from bare `git push` (blocked by #3). Deferred until the build loop is not mid-flight.
9. **Verify PR #118 pages preview:** currently `action_required` (env approval) - owner-side, not a production blocker.

## ISSUES
- **#68 (Obsidian umbrella)** - OPEN (owner wants docs cleaned; codec shipped). Not closed by PR #116 (only Refs #68).
- **#103 (Prism)** - CLOSED (merged via #104); M1-M4 continuation in flight via issue #117 + PR #118.
- **#117 (Prism M1-M4)** - OPEN (tracking issue; explicit objective + goal-tied merge gate). Also the (currently dead) target of the `lab` silent-stall fix because the `lab` job is unwired.
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor owns daily summary. NOTE: PR #119 body erroneously says `Closes #70`; the actual fix targets #98 (metadata mismatch - owner must resolve before merge).
- **#98 (runaway /oc fix retry loop)** - the REAL target of PR #119's fix; currently OPEN and incorrectly not referenced in the PR body.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `02c0fb556d50be4ea056a734da7957420e9357b5`.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed via #111).
- **`lab.yml` Lab Engineer pin:** N/A - there is no `lab` job/workflow; the Lab Engineer cannot currently be dispatched via `/oc lab` (see CRITICAL INFRASTRUCTURE STATE).
- **Circuit breaker:** RESET (counter 0). Owner re-issued directive (quality gate, not the breaker, governs merges).

## NEXT STEPS
1. Prism M1-M4 (PR #118): the in-flight `continue` (`32540331936`) resumes B6-B8 toward M3 < 8.71 bpp on real Kodak bit-exactly; then Reviewer -> Tester (real Kodak, bit-exact, bpp gates); HOLD merge until M3 met bit-exactly per owner override.
2. **PR #119 owner escalation (this run):** await owner to apply the guard short-circuit + `set +e` hardening, fix `Closes` (#98), rebase to clear `CONFLICTING`, and (recommended) grant `workflows: write`. The #98 fix content is good and must be preserved.
3. **`lab` job wiring (owner action needed):** add a `lab` job to `opencode.yml` (and/or restore `opencode-lab.yml`) so The Lab Engineer can run and fix the silent-stall dispatch logic and future workflow-file PRs. Mae cannot make this edit under the model-switch-only restriction.

## OPEN QUESTIONS
- Prism #118: will the in-flight `continue` (`32540331936`) iterate past ~11.120 bpp (B5.17) toward M3 < 8.71 on REAL Kodak bit-exactly? Owner override: no merge until M0+M1+M2+M3 met bit-exactly.
- Prism #118: when stable at/under the gate, fire Reviewer -> Tester before any merge.
- **PR #119 (this run's escalation):** will the owner (a) grant the App `workflows: write` and let a fresh `/oc fix` self-heal, or (b) manually apply the guard fix + `set +e` hardening + Closes fix + rebase? Which is the correct `Closes` target, #70 or #98?
- **`lab` PATH BROKEN:** opencode.yml has no `lab` job and `opencode-lab.yml` does not exist, so `/oc lab` no-ops. Will the owner wire the `lab` job? Mae's only mitigation for the silent-stall is re-dispatching `continue`.
- **WORKFLOW-FILE PUSH WALL (new):** the App lacks `workflows` scope; will the owner grant it so workflow-file PRs can self-heal, or continue to apply such changes manually?
- Silent-stall root cause (BLOCKED by missing lab job): owner `/oc continue` at 23:16:28Z / 23:58:52Z / 00:23:08Z all failed to launch a build (skipped/cancelled). Why? Needs the Lab Engineer, which is currently unreachable.
- entropy-architecture.md: should the authoritative rANS design doc be un-archived (Reviewer design note, non-blocking)?
- Circuit-breaker false-trip: will the `OPENCODE_PAT` workflows-scope wall ever be lifted so the `lab` fix can land? Short-term mitigation in force.
- Agent bare `git push` fatal-error noise: optional `lab` cleanup after the build loop is not mid-flight (blocked by missing lab job).

- Mae, the Maintainer
