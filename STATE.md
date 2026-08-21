# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32524154129, EVENT `created` on PR #116, owner `/oc review` + `/oc maintainer`).
- **Obsidian doc-cleanup PR #116 IN REVIEW:** Builder rewrote `obsidian/README.md` + `obsidian/benchmarks/README.md`, restructured `obsidian/docs/` (23 blueprints archived, new docs/README.md map + current-architecture.md), bannered v1 blueprint/spec as historical, appended research.md addendum. Head `ae561b4`, branch `opencode/issue68-20260821202612`, MERGEABLE (merge-base `1de6c05`, not orphan). Reviewer pending (run 32524154101). NO merge until Reviewer + Tester green. Docs-only -> free (not a new project). #68 stays OPEN (PR Refs #68).
- **Prism M1-M4:** owner override (20:08Z quality-gate challenge + 20:14Z "new issue+PR with clear gate") -> `build` dispatched at 20:14Z to open a NEW issue+PR adopting branch `a87118b` (B5-B5.6, real-Kodak 11.43 bpp) WITHOUT restarting from M0. NO open Prism PR found this run - status to re-confirm next survey. Owner gate: NO merge of any Prism iteration until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71).

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115). Obsidian is the current codec in `main`; its docs were stale and are being cleaned up by PR #116.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - upgrade over Obsidian, beats JPEG XL (~8.71 bpp on Kodak). M1-M4 in progress on branch `a87118b` (real-Kodak 11.43 bpp) with NO open PR (new issue+PR pending the 20:14Z `build` dispatch). Owner override: NO merge until M0+M1+M2+M3 all met bit-exactly on REAL Kodak.
- **One-PR rule + NEVER delete PR branches:** satisfied.
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Owner 20:08Z challenge:** quality gates are the ONLY merge criteria; the 20-round Lab circuit breaker is a runaway guard, never a merge trigger.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `35a2d68`** (post #104 M0 merge; Obsidian promoted via #115). Obsidian lives in `obsidian/` on `main`. Prism M1-M4 branch `opencode/issue103-20260821075928` = `a87118b` shares M0 ancestry (NOT orphan).
- **Obsidian current state:** merged to main; last confirmed REAL-Kodak baseline **9.5209 bpp** (PR #116 recomputed; prior memory noted 9.5208 - rounding nuance, Reviewer to confirm vs code).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** stable; Prism M0 merge re-deployed via 32510773918.

## IN FLIGHT
- **Obsidian doc cleanup (PR #116):** head `ae561b4`, Reviewer pending (32524154101). On green -> Tester -> Mae merge (docs, free) -> #68 stays OPEN.
- **Prism M1-M4 optimization loop (B6-B9):** `build` dispatched at 20:14Z to open new issue+PR adopting `a87118b`; NO open PR yet. After code lands + PR opens: Reviewer -> Tester on REAL Kodak; hold merge until M3 (<8.71 bpp) met bit-exactly per owner override. `data/kodak` durably provisioned (B10).

## PENDING (in order)
1. **Obsidian doc cleanup (#68, PR #116):** Reviewer (pending) -> Tester -> merge (docs, free). #68 stays OPEN.
2. **Prism M1-M4 (B6-B9):** confirm the 20:14Z `build` opened the new issue+PR adopting `a87118b`; when code lands, Reviewer -> Tester (real Kodak, bit-exact, bpp gates M1<13.05 & <9.61, M2<9.71, M3<8.71). NO merge until M3 met bit-exactly.
3. **#42 Board resume (parked):** Ideator batch posted; PARKED behind Prism per owner directive.
4. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.
5. **Circuit breaker tuning:** runaway guard, not a merge trigger; no change needed for correctness.

## ISSUES
- **#68 (Obsidian umbrella)** - OPEN (owner wants docs cleaned; codec shipped). PR #116 Refs it.
- **#103 (Prism)** - CLOSED (merged via #104).
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `35a2d68`.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed via #111).
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- **Circuit breaker:** tripped on #104 - halts AUTO re-dispatches only; human-authorized runs exempt.

## NEXT STEPS
1. Obsidian docs (#68, PR #116): Reviewer pending; on green -> Tester -> merge (free); #68 stays OPEN.
2. Prism M1-M4: re-confirm the new issue+PR opened by the 20:14Z `build`; when code lands, Reviewer -> Tester on real Kodak; hold merge until M3 (<8.71 bpp) met bit-exactly.
3. #42: PARKED - resume candidate pick only after Prism clears the JXL gate.

## OPEN QUESTIONS
- Obsidian docs (PR #116): will the Reviewer confirm the 9.5209 recompute matches the code baseline, and approve doc accuracy vs current code?
- Prism M1-M4: did the 20:14Z `build` open the new issue+PR adopting `a87118b`? (No open Prism PR found this run.)
- Prism M1-M4: does Squeeze + MA-tree (B7) cross under JPEG XL 8.71 on real Kodak at M3? (Owner override: no merge until M0+M1+M2+M3 met bit-exactly.)
- `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.

- Mae, the Maintainer
