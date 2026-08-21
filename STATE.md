# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32531554019, EVENT `created` on PR #118, owner `/oc maintainer` + `/oc continue` ~22:06Z).
- **Obsidian docs cleanup PR #116 MERGED:** merged into `main` via rebase at `02c0fb556d50be4ea056a734da7957420e9357b5`. Issue **#68 stays OPEN**. Production `pages.yml` deploy succeeded (`32526596392`).
- **PR #118 (Prism M1-M4) is the active priority and is IN FLIGHT.** Branch `opencode/117-prism-m1-m4-optimization` = `02153a3bfc5e8cfba0c2a55f30b272e358f8d7c0` (advanced past B5.9, ~11.27 bpp, improving), MERGEABLE, shares `main` ancestry (NOT orphan). A `/oc continue` build is currently running (run `32531541339`) targeting B6-B8.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; docs cleaned by merged PR #116). Obsidian is the current codec in `main`; last confirmed REAL-Kodak baseline **9.5209 bpp**.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - upgrade over Obsidian, beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation in flight (issue #117, PR #118). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71). The merge gate is tied to the ACTUAL project goal, not any iteration/round limit; never merge incomplete work simply because a round or iteration limit was reached.
- **One-PR rule + NEVER delete PR branches:** satisfied (PR #116 and #104 branches retained after merge).
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Quality-gate directive:** quality gates are the ONLY merge criteria.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `02c0fb556d50be4ea056a734da7957420e9357b5`** (post PR #116 merge). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/117-prism-m1-m4-optimization` = `02153a3b` shares M0 ancestry (NOT orphan).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** production deploy `32526596392` succeeded (main). PR #118 preview deploy runs are `action_required` (needs env approval; not the production path).

## IN FLIGHT
- **Prism M1-M4 (issue #117, PR #118, branch `opencode/117-prism-m1-m4-optimization`):** optimization loop. Current branch head `02153a3b` (~11.27 bpp, B5.9+). A `/oc continue` build (run `32531541339`, started 22:06:25Z) is IN FLIGHT driving B6 (CFL + 5/3 lifting + 16-bit widening -> M2 < 9.71), B7 (Squeeze + MA-tree with mandatory `llc_class`/`sibling_class` -> M3 < 8.71), B8 (CM + LZP never-expand net -> M4 < 8.0). A prior `/oc continue` (run `32529129203`, 21:34Z) completed and force-pushed successfully despite a benign agent-side `git push` fatal error (the harness explicit-refspec push + verify/auto-retry delivers). Owner override: NO merge until M3 (<8.71 bpp) met bit-exactly on REAL Kodak.

## PENDING (in order)
1. **Prism M1-M4 (PR #118):** let the in-flight `continue` (32531541339) run; it iterates B6-B8 toward M3 < 8.71 bpp on real Kodak bit-exactly. Do NOT dispatch a second `continue` while one is active (would race on the same branch). When stable + green on real Kodak bit-exactly at/under the gate, fire Reviewer -> Tester (real Kodak, bit-exact, bpp gates M1<13.05 & <9.61, M2<9.71, M3<8.71). HOLD merge until M3 met bit-exactly per owner override.
2. **#42 Board resume (parked):** Ideator batch posted; PARKED behind Prism per owner directive.
3. **entropy-architecture.md archive follow-up (non-blocking, Reviewer design note):** authoritative doc for the shipped rANS backend, still cited by live code; consider un-archiving or a clearer label.
4. **Circuit-breaker false-trip fix (root cause):** breaker counts Maintainer's own status comments (embedding dispatch keywords). Harden `loop-budget.sh` to exclude Maintainer status comments (a `lab` change, blocked by workflows-scope PAT wall until owner regenerates `OPENCODE_PAT`). Short-term: keep bot comments free of literal dispatch-keyword phrases.
5. **Benign agent `git push` fatal-error noise (non-blocking):** the opencode agent sometimes runs a bare `git push` (upstream mismatch) inside the session; the harness push (explicit refspec + verify/auto-retry) still delivers, as proven by the branch advancing. Optional `lab` follow-up to steer the agent away from bare `git push` (or make it `git push origin HEAD:<branch>`). Deferred until the build loop is not mid-flight.
6. **Verify PR #118 pages preview:** currently `action_required` (env approval) - owner-side, not a production blocker.

## ISSUES
- **#68 (Obsidian umbrella)** - OPEN (owner wants docs cleaned; codec shipped). Not closed by PR #116 (only Refs #68).
- **#103 (Prism)** - CLOSED (merged via #104); M1-M4 continuation in flight via issue #117 + PR #118.
- **#117 (Prism M1-M4)** - OPEN (tracking issue; explicit objective + goal-tied merge gate).
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `02c0fb556d50be4ea056a734da7957420e9357b5`.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed via #111).
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- **Circuit breaker:** RESET (counter 0). Owner re-issued directive (quality gate, not the breaker, governs merges).

## NEXT STEPS
1. Prism M1-M4 (PR #118): allow in-flight `continue` (32531541339) to iterate B6-B8 toward M3 < 8.71 bpp on real Kodak bit-exactly; then Reviewer -> Tester (real Kodak, bit-exact, bpp gates); HOLD merge until M3 met bit-exactly per owner override.
2. After the gate is cleared and PR #118 is reviewed + Tester-approved, merge via rebase (branch retained) and close #117.

## OPEN QUESTIONS
- Prism #118: does the in-flight `continue` build iterate past ~11.27 bpp toward M3 < 8.71 on REAL Kodak bit-exactly? Owner override: no merge until M0+M1+M2+M3 met bit-exactly.
- Prism #118: when stable at/under the gate, fire Reviewer -> Tester before any merge.
- entropy-architecture.md: should the authoritative rANS design doc be un-archived (Reviewer design note, non-blocking)?
- Circuit-breaker false-trip: will the `OPENCODE_PAT` workflows-scope wall ever be lifted so the `lab` fix can land? Short-term mitigation in force.
- Agent bare `git push` fatal-error noise: optional `lab` cleanup after the build loop is not mid-flight.

- Mae, the Maintainer
