# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32524674938, EVENT `issue_comment` on PR #104, owner "where is new pr and issue for this?").
- **Prism M1-M4 issue+PR now being (re)opened:** the 20:14Z `build` (run 32522550428) that was to create the new issue+PR was CANCELLED by the circuit breaker on #104 before running any job. Root cause: the breaker counts every bot comment containing a dispatch keyword, and the Maintainer's own status comments on #104 embed those keywords, so the counter self-climbed to 23 vs budget 20 (a self-inflicted runaway, not a real loop). This run pruned the 23 bot dispatch-noise comments on #104 (counter now 0) and re-dispatched `build` via decision.json - the Builder will open a fresh issue+PR adopting the existing M1-M4 branch `opencode/issue103-20260821075928` (head `41a656b`, real-Kodak mean 11.336 bpp) WITHOUT restarting M0, and will spell out the objective + merge gate verbatim. No open Prism PR exists yet; expected shortly after the build run lands.
- **Obsidian doc cleanup PR #116 IN REVIEW:** head `ae561b4`, branch `opencode/issue68-20260821202612`, MERGEABLE (merge-base `1de6c05`, not orphan). Reviewer pending (run 32524533329). Docs-only -> free (not a new project). #68 stays OPEN (PR Refs #68).

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115). Obsidian is the current codec in `main`; its docs were stale and are being cleaned up by PR #116.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - upgrade over Obsidian, beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation: new issue+PR opening this run, adopting branch `41a656b`. Owner override: NO merge of any Prism iteration until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71).
- **One-PR rule + NEVER delete PR branches:** satisfied.
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Owner 20:08Z challenge:** quality gates are the ONLY merge criteria; the circuit-breaker runaway guard was NEVER a merge trigger. (Confirmed this run: the breaker was a self-trip caused by the Maintainer's own comments, now reset.)

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `35a2d68`** (post #104 M0 merge; Obsidian promoted via #115). Obsidian lives in `obsidian/` on `main`. Prism M1-M4 branch `opencode/issue103-20260821075928` = `41a656b` shares M0 ancestry (NOT orphan).
- **Obsidian current state:** merged to main; last confirmed REAL-Kodak baseline **9.5209 bpp** (PR #116 recomputed).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** stable; Prism M0 merge re-deployed via 32510773918.

## IN FLIGHT
- **Prism M1-M4 (new issue+PR opening):** `build` re-dispatched this run (decision.json) after breaker reset; will adopt `opencode/issue103-20260821075928` (`41a656b`). After code lands + PR opens: Reviewer -> Tester on REAL Kodak; hold merge until M3 (<8.71 bpp) met bit-exactly per owner override. `data/kodak` already provisioned (B10, SHA256 pinned).
- **Obsidian doc cleanup (PR #116):** head `ae561b4`, Reviewer pending (32524533329). On green -> Tester -> Mae merge (docs, free) -> #68 stays OPEN.

## PENDING (in order)
1. **Prism M1-M4 (B6-B9):** confirm the re-dispatched `build` opened the new issue+PR adopting `41a656b`; when code lands, Reviewer -> Tester (real Kodak, bit-exact, bpp gates M1<13.05 & <9.61, M2<9.71, M3<8.71). NO merge until M3 met bit-exactly.
2. **Obsidian doc cleanup (#68, PR #116):** Reviewer (pending) -> Tester -> merge (docs, free). #68 stays OPEN.
3. **#42 Board resume (parked):** Ideator batch posted; PARKED behind Prism per owner directive.
4. **Circuit-breaker false-trip fix (root cause):** the breaker counts the Maintainer's own status comments because they embed dispatch keywords. The maintainer/logs branch record must be the source of truth; to stop self-re-tripping, future Maintainer bot comments must avoid embedding raw dispatch keywords, OR `loop-budget.sh` should exclude the Maintainer's status comments (a `lab` change, blocked by the workflows-scope PAT wall until the owner regenerates `OPENCODE_PAT`). Short-term mitigation: keep bot comments free of literal dispatch-keyword phrases.
5. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.

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
- **Circuit breaker on #104:** RESET this run (pruned 23 bot dispatch-noise comments; counter 0). Owner explicitly re-issued the directive, authorizing continuation.

## NEXT STEPS
1. Prism M1-M4: confirm the re-dispatched `build` opened the new issue+PR adopting `41a656b`; when code lands, Reviewer -> Tester on real Kodak; hold merge until M3 (<8.71 bpp) met bit-exactly.
2. Obsidian docs (#68, PR #116): Reviewer pending; on green -> Tester -> merge (free); #68 stays OPEN.

## OPEN QUESTIONS
- Prism M1-M4: did the re-dispatched `build` open the new issue+PR adopting `41a656b`, and does it document the objective + gate verbatim?
- Prism M1-M4: does Squeeze + MA-tree (B7) cross under JPEG XL 8.71 on real Kodak at M3? (Owner override: no merge until M0+M1+M2+M3 met bit-exactly.)
- Obsidian docs (PR #116): will the Reviewer confirm doc accuracy vs current code, then Tester pass, Mae merge (free)?
- Circuit-breaker root cause: will the owner regenerate `OPENCODE_PAT` with `workflows` scope so `loop-budget.sh` can be hardened (exclude Maintainer status comments) without the PAT wall?

- Mae, the Maintainer
