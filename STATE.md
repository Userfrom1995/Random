# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32524533132, EVENT `created` on PR #116, owner `/oc review` + `/oc maintainer` re-review).
- **Obsidian doc-cleanup PR #116 IN RE-REVIEW (post-Fixer):** head `1e1b59d`, branch `opencode/issue68-20260821202612`, MERGEABLE (shallow-clone `merge-base` false-negative; GH API `mergeStateStatus: CLEAN`; shares `1de6c05`/`35a2d68` ancestry with main). Reviewer re-review PENDING (run 32524533329) after Fixer repaired 4 dead entropy-doc links (moved to `docs/archive/`). NO merge until Reviewer + Tester green. Docs-only -> free. Issue #68 is now CLOSED, so nothing to close on merge.
- **Prism M1-M4:** branch `opencode/issue103-20260821075928` advanced to `41a656b` (commits via 20:10Z resume build); NO open PR. The 20:14Z `build` to open a fresh issue+PR was CANCELLED - gap flagged; re-dispatch `build` on #103 when owner signals (adopt branch, no M0 restart). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71).

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115). Obsidian is the current codec in `main`; its docs were stale and are being cleaned up by PR #116.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - upgrade over Obsidian, beats JPEG XL (~8.71 bpp on Kodak). M1-M4 in progress on branch `41a656b` with NO open PR (20:14Z build cancelled). Owner override: NO merge until M0+M1+M2+M3 all met bit-exactly on REAL Kodak.
- **One-PR rule + NEVER delete PR branches:** satisfied.
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears JXL gate.
- **Owner 20:08Z challenge:** quality gates are the ONLY merge criteria; the 20-round Lab circuit breaker is a runaway guard, never a merge trigger.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `9a1573e`** (post lab-infra commits `1de6c05` "grant Maintainer issue and PR creation capabilities" + `9a1573e` "ensure Maintainer created issues/PRs are authored by bot"). Obsidian lives in `obsidian/` on `main`. Prism M1-M4 branch `opencode/issue103-20260821075928` = `41a656b` shares M0 ancestry (NOT orphan).
- **Obsidian current state:** merged to main; last confirmed REAL-Kodak baseline **9.5209 bpp** (PR #116 recomputed; Reviewer to confirm vs code).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** stable; Prism M0 + #115 deploys re-run.

## IN FLIGHT
- **Obsidian doc cleanup (PR #116):** head `1e1b59d`, Reviewer re-review PENDING (32524533329). On green -> Tester -> Mae merge (docs, free) -> #68 already closed (no issue close).
- **Prism M1-M4 optimization loop (B6-B9):** branch `41a656b`, NO open PR (20:14Z build cancelled). Resume build landed commits. Re-dispatch `build` on #103 to open issue+PR when owner signals; then Reviewer -> Tester on REAL Kodak; hold merge until M3 (<8.71 bpp) met bit-exactly per owner override. `data/kodak` provisioned.

## PENDING (in order)
1. **Obsidian doc cleanup (#68, PR #116):** Reviewer re-review (pending) -> Tester -> merge (docs, free). #68 already CLOSED.
2. **Prism M1-M4 (B6-B9):** re-dispatch `build` on #103 when owner signals (20:14Z build cancelled, no PR); when code lands, Reviewer -> Tester (real Kodak, bit-exact, bpp gates). NO merge until M3 met bit-exactly.
3. **#42 Board resume (parked):** Ideator batch posted; PARKED behind Prism per owner directive.
4. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.
5. **Circuit breaker tuning:** runaway guard, not a merge trigger; no change needed for correctness.

## ISSUES
- **#68 (Obsidian umbrella)** - CLOSED (was OPEN; PR #116 only Refs it).
- **#103 (Prism)** - CLOSED (merged via #104).
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `9a1573e`.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed via #111).
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- **Circuit breaker:** tripped on #104 - halts AUTO re-dispatches only; human-authorized runs exempt.

## NEXT STEPS
1. Obsidian docs (#68, PR #116): Reviewer re-review pending (32524533329); on green -> Tester -> merge (free); #68 already closed.
2. Prism M1-M4: re-dispatch `build` on #103 when owner signals (20:14Z build cancelled, no PR); when code lands, Reviewer -> Tester on real Kodak; hold merge until M3 (<8.71 bpp) met bit-exactly.
3. #42: PARKED - resume candidate pick only after Prism clears the JXL gate.

## OPEN QUESTIONS
- Obsidian docs (PR #116): will the re-Reviewer (32524533329) confirm the dead-link repairs and approve doc accuracy vs current code?
- Prism M1-M4: re-dispatch `build` on #103 when owner signals to open the issue+PR (adopt `41a656b`, no M0 restart)? Does Squeeze + MA-tree (B7) cross under JPEG XL 8.71 on real Kodak at M3?
- `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.

- Mae, the Maintainer
