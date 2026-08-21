# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32525067392, EVENT `issue_comment` on PR #116, owner `/oc maintainer` at 20:44:06Z).
- **Obsidian doc cleanup PR #116 IN GREEN GATE:** head `d470747`, branch `opencode/issue68-20260821202612`, MERGEABLE CLEAN. Reviewer approved third pass 20:45:02Z (all prior dead-link findings confirmed fixed). Tester (`opencode-test` run `32525145845`) in_progress from owner `/oc test` 20:45:04Z. Mae merges on Tester approval (docs-only, free). #68 stays OPEN (PR only Refs #68).
- **Prism M1-M4 BUILD IN FLIGHT:** build run `32525037234` (in_progress, BUILD mode, triggered ~20:43:48Z by the prior maintainer run's `build` decision on issue #103). Adopts existing branch `opencode/issue103-20260821075928` (head `41a656b`, real-Kodak mean 11.336 bpp) WITHOUT restarting M0. Expected to open a fresh M1-M4 issue+PR shortly; if no PR appears by next survey, re-dispatch. Owner override: NO merge of any Prism iteration until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71).

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115). Obsidian is the current codec in `main`; its docs were stale and are being cleaned up by PR #116.
- **NEXT PRIORITY (owner):** build **Prism (issue #103, M0 MERGED via #104)** - upgrade over Obsidian, beats JPEG XL (~8.71 bpp on Kodak). M1-M4 continuation in flight (build `32525037234`). Owner override: NO merge until M0+M1+M2+M3 met bit-exactly on REAL Kodak (M3 < JPEG XL 8.71).
- **One-PR rule + NEVER delete PR branches:** satisfied.
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Owner quality-gate directive:** quality gates are the ONLY merge criteria; the circuit-breaker runaway guard was NEVER a merge trigger (self-trip from Maintainer's own status comments, reset 20:43Z run).

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `35a2d68`** (post #104 M0 merge; Obsidian promoted via #115). Obsidian lives in `obsidian/` on `main`. Prism branch `opencode/issue103-20260821075928` = `41a656b` shares M0 ancestry (NOT orphan).
- **Obsidian current state:** merged to main; last confirmed REAL-Kodak baseline **9.5209 bpp** (PR #116 recomputed).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free).
- **pages.yml:** stable; Prism M0 merge re-deployed via 32510773918; PR #116 preview live at `/preview/pr-116/`.

## IN FLIGHT
- **Prism M1-M4 (build `32525037234`):** BUILD mode, adopting `opencode/issue103-20260821075928` (`41a656b`). After code lands + PR opens: Reviewer -> Tester on REAL Kodak; hold merge until M3 (<8.71 bpp) met bit-exactly per owner override. `data/kodak` already provisioned (B10, SHA256 pinned).
- **Obsidian doc cleanup (PR #116):** Reviewer approved (third pass); Tester `32525145845` in_progress; Mae merges on green (docs, free); #68 stays OPEN.

## PENDING (in order)
1. **Obsidian doc cleanup (#68, PR #116):** wait for Tester `32525145845` approval -> Mae merge (free). #68 stays OPEN.
2. **Prism M1-M4 (build `32525037234`):** confirm it opened the new issue+PR adopting `41a656b`; when code lands, Reviewer -> Tester (real Kodak, bit-exact, bpp gates M1<13.05 & <9.61, M2<9.71, M3<8.71). NO merge until M3 met bit-exactly.
3. **#42 Board resume (parked):** Ideator batch posted; PARKED behind Prism per owner directive.
4. **entropy-architecture.md archive follow-up (non-blocking, Reviewer design note):** it is the authoritative doc for the shipped M3.5 rANS backend and is still cited by live code; consider un-archiving or a clearer label. Fixer left the archive move intact. Track for a future docs sweep.
5. **Circuit-breaker false-trip fix (root cause):** breaker counts Maintainer's own status comments (embedding dispatch keywords). Harden `loop-budget.sh` to exclude Maintainer status comments (a `lab` change, blocked by workflows-scope PAT wall until owner regenerates `OPENCODE_PAT`). Short-term: keep bot comments free of literal dispatch-keyword phrases (this run's comment avoided them).
6. **Removed:** the `lab.yml` Lab Engineer pin bump item - no no-op observed, not needed now.

## ISSUES
- **#68 (Obsidian umbrella)** - OPEN (owner wants docs cleaned; codec shipped). PR #116 Refs it.
- **#103 (Prism)** - CLOSED (merged via #104); M1-M4 continuation in flight via new issue+PR (pending build `32525037234`).
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `35a2d68`.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed via #111).
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- **Circuit breaker on #104:** RESET (prior run pruned 23 bot dispatch-noise comments; counter 0). Owner re-issued directive.

## NEXT STEPS
1. Obsidian docs (#68, PR #116): Tester `32525145845` -> Mae merge on green (free); #68 stays OPEN.
2. Prism M1-M4 (build `32525037234`): confirm new issue+PR opened adopting `41a656b`; Reviewer -> Tester on real Kodak; hold merge until M3 (<8.71 bpp) met bit-exactly.

## OPEN QUESTIONS
- Obsidian docs (PR #116): will Tester `32525145845` approve (docs-only, expected pass), then Mae merge?
- Prism M1-M4: did build `32525037234` adopt `41a656b` and open a new issue+PR? If no PR by next survey, re-dispatch `build` on #103.
- Prism M1-M4: does Squeeze + MA-tree (B7) cross under JPEG XL 8.71 on real Kodak at M3? (Owner override: no merge until M0+M1+M2+M3 met bit-exactly.)
- entropy-architecture.md: should the authoritative rANS design doc be un-archived (Reviewer design note, non-blocking)?

- Mae, the Maintainer