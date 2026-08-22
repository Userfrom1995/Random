# STATE - Random factory checkpoint
- **Updated:** 2026-08-22 (maintainer run 32540175107, EVENT `created` on PR #118, owner `/oc continue` ~00:23Z).
- **Obsidian docs cleanup PR #116 MERGED:** merged into `main` via rebase at `02c0fb556d50be4ea056a734da7957420e9357b5`. Issue **#68 stays OPEN**. Production `pages.yml` deploy succeeded (`32536272428`).
- **PR #118 (Prism M1-M4) is the active priority and is IN FLIGHT.** Branch `opencode/117-prism-m1-m4-optimization` = `f5faad7cf2e6ad7ddbb07d78eb106b97d6eb8069` (B5.17, 11.120 bpp, byte-exact, MERGEABLE, shares `main` ancestry NOT orphan). A fresh `continue` was just dispatched by this maintainer run (32540175107) after catching a THIRD silent stall at 00:23:08Z. A `lab` diagnostic was ALSO dispatched (on issue #117) for the now-recurring silent-stall.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; docs cleaned by merged PR #116). Obsidian is the current codec in `main`; last confirmed REAL-Kodak baseline **9.5209 bpp**.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - upgrade over Obsidian, beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation in flight (issue #117, PR #118). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71). The merge gate is tied to the ACTUAL project goal, not any iteration/round limit; never merge incomplete work simply because a round or iteration limit was reached.
- **One-PR rule + NEVER delete PR branches:** satisfied (PR #116 and #104 branches retained after merge).
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Quality-gate directive:** quality gates are the ONLY merge criteria.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `02c0fb556d50be4ea056a734da7957420e9357b5`** (post PR #116 merge). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/117-prism-m1-m4-optimization` = `f5faad7` shares M0 ancestry (NOT orphan).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** production deploy `32536272428` succeeded (main). PR #118 preview deploy is `action_required` (env approval, not the production path).

## IN FLIGHT
- **Prism M1-M4 (issue #117, PR #118, branch `opencode/117-prism-m1-m4-optimization`):** optimization loop. Current branch head `f5faad7` (B5.17, 11.120 bpp, byte-exact, harness 134s). A fresh `continue` is being dispatched by this run (32540175107) after the owner's `/oc continue` at 00:23:08Z produced only `skipped`/`cancelled` opencode runs (silent stall #3), with no build in_progress. It resumes B6-B8 from B5.17.
  - B6: 5/3 lifting + int32 color widening for BD16 (M2 < 9.71).
  - B7: Squeeze + MA-tree greedy split with mandatory llc_class/sibling_class (M3 < 8.71 - the crux, ~14% gap).
  - Burns: B8 (CM + LZP never-expand net, M4 < 8.0) deferred until M3 in reach.

## PENDING (in order)
1. **Prism M1-M4 (PR #118):** the freshly-dispatched `continue` resumes B6-B8 toward M3 < 8.71 bpp on real Kodak bit-exactly. Do NOT dispatch a second `continue` while one is active. When stable + green on real Kodak bit-exactly at/under the gate, fire Reviewer -> Tester (real Kodak, bit-exact, bpp gates M1<13.05 & <9.61, M2<9.71, M3<8.71). HOLD merge until M3 met bit-exactly per owner override.
2. **Silent-stall fix (ESCALATED -> `lab` DISPATCHED this run, issue #117):** owner `/oc continue` produced skipped/cancelled opencode runs THREE times (23:16:28Z `32536270442`; 23:58:52Z `32538794937`+`32538801477`; 00:23:08Z `32540175109`+`32540168896`). The Lab Engineer must diagnose opencode.yml issue_comment dispatch for the continue/B5 trigger and fix it so `/oc continue` reliably launches a build. Short-term mitigation: the Maintainer re-dispatches `continue` itself on detection (done this run).
3. **#42 Board resume (parked):** Ideator batch posted; PARKED behind Prism per owner directive.
4. **entropy-architecture.md archive follow-up (non-blocking, Reviewer design note):** authoritative doc for the shipped rANS backend, still cited by live code; consider un-archiving or a clearer label.
5. **Circuit-breaker false-trip fix (root cause):** breaker counts Maintainer's own status comments (embedding dispatch keywords). Harden `loop-budget.sh` to exclude Maintainer status comments (a `lab` change, blocked by workflows-scope PAT wall until owner regenerates `OPENCODE_PAT`). Short-term: keep bot comments free of literal dispatch-keyword phrases.
6. **Benign agent `git push` fatal-error noise (non-blocking):** the opencode agent sometimes runs a bare `git push` (upstream mismatch) inside the session; the harness push (explicit refspec + verify/auto-retry) still delivers, as proven by the branch advancing. Optional `lab` follow-up to steer the agent away from bare `git push`. Deferred until the build loop is not mid-flight.
7. **Verify PR #118 pages preview:** currently `action_required` (env approval) - owner-side, not a production blocker.

## ISSUES
- **#68 (Obsidian umbrella)** - OPEN (owner wants docs cleaned; codec shipped). Not closed by PR #116 (only Refs #68).
- **#103 (Prism)** - CLOSED (merged via #104); M1-M4 continuation in flight via issue #117 + PR #118.
- **#117 (Prism M1-M4)** - OPEN (tracking issue; explicit objective + goal-tied merge gate). Now also the target of the `lab` silent-stall fix.
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `02c0fb556d50be4ea056a734da7957420e9357b5`.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed via #111).
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- **Circuit breaker:** RESET (counter 0). Owner re-issued directive (quality gate, not the breaker, governs merges).

## NEXT STEPS
1. Prism M1-M4 (PR #118): the freshly-dispatched `continue` resumes B6-B8 toward M3 < 8.71 bpp on real Kodak bit-exactly; then Reviewer -> Tester (real Kodak, bit-exact, bpp gates); HOLD merge until M3 met bit-exactly per owner override.
2. **Silent-stall `lab` fix (issue #117):** monitor the dispatched `lab` run; ensure opencode.yml `/oc continue` dispatch is repaired so the loop never silently pauses again.
3. After the gate is cleared and PR #118 is reviewed + Tester-approved, merge via rebase (branch retained) and close #117.

## OPEN QUESTIONS
- Prism #118: will the freshly-dispatched `continue` iterate past 11.120 bpp (B5.17) toward M3 < 8.71 on REAL Kodak bit-exactly? Owner override: no merge until M0+M1+M2+M3 met bit-exactly.
- Prism #118: when stable at/under the gate, fire Reviewer -> Tester before any merge.
- Silent-stall (ESCALATED -> `lab` dispatched, issue #117): owner `/oc continue` at 23:16:28Z (skipped `32536270442`), 23:58:52Z (cancelled `32538794937` + skipped `32538801477`), and 00:23:08Z (skipped `32540175109` + cancelled `32540168896`) all failed to launch a build. Will the `lab` diagnostic fix opencode.yml dispatch so `/oc continue` reliably enters BUILD/continue mode?
- entropy-architecture.md: should the authoritative rANS design doc be un-archived (Reviewer design note, non-blocking)?
- Circuit-breaker false-trip: will the `OPENCODE_PAT` workflows-scope wall ever be lifted so the `lab` fix can land? Short-term mitigation in force.
- Agent bare `git push` fatal-error noise: optional `lab` cleanup after the build loop is not mid-flight.

- Mae, the Maintainer
