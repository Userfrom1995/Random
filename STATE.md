# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32523313424, EVENT `created` on issue #68, owner `/oc maintainer` doc-cleanup request).
- **Obsidian doc-cleanup task routed:** `build` on issue #68 -> Builder rewrites `obsidian/README.md` + consolidates `obsidian/docs/` to reflect CURRENT code (R1-R15, merged to main) and the REAL-Kodak 9.5208 bpp baseline, with full usage/options. No merge until Reviewer approves (doc-accuracy gate). Doc PR merges freely (not a new project).
- **Prism (issue #103) remains the owner's top priority** (see below); do not let the Obsidian doc task distract from it.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115). Obsidian is the current codec in `main`; its docs are now stale and being cleaned up.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - upgrade over Obsidian, beats JPEG XL (~8.71 bpp on Kodak). M0 MERGED (#104); M1-M4 optimization loop built on branch `opencode/issue103-20260821075928` (head `a87118b`, real-Kodak 11.43 bpp) with NO open PR. Owner override: NO merge of any Prism iteration until M0+M1+M2+M3 all met bit-exactly on REAL Kodak.
- **One-PR rule + NEVER delete PR branches:** satisfied.
- **Maintainer sovereign-recovery directive:** `recover` authorized; `main` must never become a divergent/orphan ROOT.
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Owner 20:08Z challenge:** quality gates are the ONLY merge criteria; the 20-round Lab circuit breaker is a runaway guard, never a merge trigger.
- **Owner 20:14Z directive:** open a NEW issue + PR for the M1-M4 work with objective + merge gate "completely clear" (handled previously via the `build` dispatch; that work lives on branch `a87118b`).
- **Owner THIS run (issue #68):** clean up + bring Obsidian documentation fully up to date (accurate to code, latest benchmarks, usage/options, well structured, no outdated behavior).

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `35a2d68`** (post #104 M0 merge; Obsidian already merged earlier). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/issue103-20260821075928` = `a87118b` shares M0 ancestry (NOT orphan). `recover/104` tag exists.
- **Obsidian current state:** merged to main; last confirmed REAL-Kodak baseline **9.5208 bpp** (bits-per-pixel) -> PNG 13.05 MET, WebP 9.61 MET, JPEG XL 8.71 NOT MET (+0.81). Gap to JXL is the predictor, not entropy/context (per Builder R11-D finding).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** re-triggered after #104 merge (success).

## IN FLIGHT
- **Obsidian doc cleanup (THIS run):** `build` on #68 -> Builder creates branch + PR, reviews current `obsidian/` code, rewrites README + consolidates docs, opens PR. Reviewer gates before merge.
- **Prism M1-M4 optimization loop (B5-B9):** B5/B5.5/B5.6 DONE on branch `a87118b` (real-Kodak 11.43 summed bpp at B10). A `build` was previously dispatched to open a NEW issue+PR adopting branch `a87118b`; status to re-confirm next survey. After code lands + PR opens: Reviewer -> Tester on REAL Kodak; hold merge until M3 (<8.71 bpp) met bit-exactly per owner override. `data/kodak` durably provisioned (B10).

## PENDING (in order)
1. **Obsidian doc cleanup (#68, THIS run):** Builder `build` -> write accurate README + consolidated docs (current design, real-Kodak 9.5208 bpp benchmark table vs JXL/WebP/PNG, usage/CLI/options/flags, archive outdated blueprint clutter) -> Reviewer -> merge (doc PR, free).
2. **Prism M1-M4 (B6-B9):** Builder (new issue+PR adopting `a87118b`) -> Reviewer -> Tester (real Kodak, bit-exact, bpp gates M1<13.05 & <9.61, M2<9.71, M3<8.71). NO merge until M3 met bit-exactly.
3. **#42 Board resume (parked):** Ideator batch posted; PARKED behind Prism per owner directive.
4. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.
5. **Circuit breaker tuning:** runaway guard, not a merge trigger; no change needed for correctness.

## ISSUES
- **#68 (Obsidian umbrella)** - OPEN (owner wants docs cleaned; codec shipped).
- **#103 (Prism)** - CLOSED (merged via #104).
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#104 (Prism M0)** - MERGED.
- **NEW Prism M1-M4 issue** - created by a prior `build` dispatch; number TBD.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `35a2d68`.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed via #111).
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- **Circuit breaker:** tripped on #104 - halts AUTO re-dispatches only; human-authorized runs exempt.

## NEXT STEPS
1. Obsidian docs (#68): Builder PR in flight; on push, Reviewer audits doc accuracy vs code; merge when approved (free, not a new project).
2. Prism M1-M4: confirm the new issue+PR opened by the prior `build`; when code lands, Reviewer -> Tester on real Kodak; hold merge until M3 (<8.71 bpp) met bit-exactly.
3. #42: PARKED - resume candidate pick only after Prism clears the JXL gate.

## OPEN QUESTIONS
- Obsidian docs: will the Builder prune the ~28 blueprint/research markdown files into a coherent accurate set, keeping only what reflects shipped behavior? (Owner: no outdated behavior.)
- Prism M1-M4: does Squeeze + MA-tree (B7) cross under JPEG XL 8.71 on real Kodak at M3? (Owner override: no merge until M0+M1+M2+M3 met bit-exactly.)
- `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.

- Mae, the Maintainer
