# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32526276557, EVENT `issue_comment` on PR #116, owner `/oc maintainer` ~20:58:53Z).
- **Obsidian doc cleanup PR #116 MERGED:** merged into `main` via rebase at `02c0fb556d50be4ea056a734da7957420e9357b5` (21:01:03Z); branch `opencode/issue68-20260821202612` retained per owner directive. Gate was fully green: Reviewer fourth-pass approval (20:54:24Z, run 32525671105) + Tester `/oc approve-test` (20:58:50Z, run 32525917492, 148 passed/0 failed/2 ignored, benchmarks re-verified). Issue **#68 stays OPEN** (PR only Refs the codec umbrella). After merge, `pages.yml` did not auto-fire on the merge push, so Mae re-triggered it (run `32526518200`, queued) to deploy the merged docs.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; docs cleaned by merged PR #116). Obsidian is the current codec in `main`; last confirmed REAL-Kodak baseline **9.5209 bpp**.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - upgrade over Obsidian, beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation in flight (build `32525037234`, tracking #117, PR #118 open at 11.29 bpp). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71).
- **One-PR rule + NEVER delete PR branches:** satisfied (PR #116 branch retained after merge).
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Owner quality-gate directive:** quality gates are the ONLY merge criteria; the circuit-breaker runaway guard was NEVER a merge trigger (self-trip reset 20:43Z run).

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `02c0fb556d50be4ea056a734da7957420e9357b5`** (post PR #116 merge). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/117-prism-m1-m4-optimization` = `b97b60b` shares M0 ancestry (NOT orphan).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** re-triggered production deploy (run `32526518200`, queued) after the #116 merge; PR #118 preview deploy `32526467955` is `action_required` (needs env approval).

## IN FLIGHT
- **Prism M1-M4 (build `32525037234`, #117, PR #118):** BUILD mode, adopting `opencode/117-prism-m1-m4-optimization` (`b97b60b`, 11.29 bpp / WebP gap 1.68). Optimization loop in progress. Owner override: NO merge until M3 (<8.71 bpp) met bit-exactly on REAL Kodak. No review trigger yet while the build iterates.

## PENDING (in order)
1. **Prism M1-M4 (build `32525037234`, #117, PR #118):** let the build continue iterating toward the M3 < 8.71 bpp gate; when stable + green on real Kodak bit-exactly, fire Reviewer -> Tester (real Kodak, bit-exact, bpp gates M1<13.05 & <9.61, M2<9.71, M3<8.71). HOLD merge until M3 met bit-exactly per owner override.
2. **#42 Board resume (parked):** Ideator batch posted; PARKED behind Prism per owner directive.
3. **entropy-architecture.md archive follow-up (non-blocking, Reviewer design note):** authoritative doc for the shipped M3.5 rANS backend, still cited by live code; consider un-archiving or a clearer label. Fixer left the archive move intact. Track for a future docs sweep.
4. **Circuit-breaker false-trip fix (root cause):** breaker counts Maintainer's own status comments (embedding dispatch keywords). Harden `loop-budget.sh` to exclude Maintainer status comments (a `lab` change, blocked by workflows-scope PAT wall until owner regenerates `OPENCODE_PAT`). Short-term: keep bot comments free of literal dispatch-keyword phrases.
5. **Verify `pages.yml` run `32526518200`** completes success and the production site reflects PR #116's merged docs.

## ISSUES
- **#68 (Obsidian umbrella)** - OPEN (owner wants docs cleaned; codec shipped). Closed by PR #116? NO - PR only Refs #68, does not close it.
- **#103 (Prism)** - CLOSED (merged via #104); M1-M4 continuation in flight via issue #117 + build `32525037234` + PR #118.
- **#117 (Prism M1-M4)** - OPEN (tracking issue opened by build `32525037234`).
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `02c0fb556d50be4ea056a734da7957420e9357b5`.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed via #111).
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- **Circuit breaker:** RESET (counter 0). Owner re-issued directive.

## NEXT STEPS
1. Prism M1-M4 (build `32525037234`, #117, PR #118): let the build iterate toward M3 < 8.71 bpp on real Kodak bit-exactly; then Reviewer -> Tester (real Kodak, bit-exact, bpp gates); HOLD merge until M3 met bit-exactly.
2. Verify `pages.yml` run `32526518200` deploys the merged #116 docs to production.

## OPEN QUESTIONS
- Prism #118: does the ongoing build `32525037234` iterate past 11.29 bpp toward M3 < 8.71 on REAL Kodak bit-exactly? Owner override: no merge until M0+M1+M2+M3 met bit-exactly.
- Prism #118: when stable at/under the gate, fire Reviewer -> Tester before any merge.
- entropy-architecture.md: should the authoritative rANS design doc be un-archived (Reviewer design note, non-blocking)?
- Did `pages.yml` run `32526518200` complete and publish PR #116's merged docs?

- Mae, the Maintainer