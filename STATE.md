# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32521962463, EVENT `issue_comment` on PR #104, ~20:08Z). PR #104 (Prism M0, issue #103) MERGED at 17:55:24Z; `main`=`35a2d68`. The M1-M4 optimization loop is in flight on the preserved branch `opencode/issue103-20260821075928` (head `a87118b`), with **NO open PR** (PR #104 is merged). This run resumes the Builder via `continue` on PR #104 to push B6-B9 and re-open a continuation PR. No merge until M3 beats JXL 8.71 on real Kodak per owner override. New-project merges today: **1/2** (Prism M0; M1-M4 is the same project).

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115).
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - upgrade over Obsidian, all major input formats, beats JPEG XL (~8.71 bpp on Kodak). M0 MERGED; M1-M4 optimization loop NOW building (this run, `continue` on PR #104). Owner override: NO merge of any Prism iteration until M0 + M1 + M2 + M3 are all met bit-exactly on REAL Kodak. `data/kodak` durably provisioned (B10).
- **One-PR rule + NEVER delete PR branches:** satisfied; #104 branch `opencode/issue103-20260821075928` preserved (merged without `--delete-branch`).
- **Maintainer sovereign-recovery directive:** `recover` authorized; `main` must never become a divergent/orphan ROOT.
- **Owner WILL (resolved):** builder model = free `opencode/muse-spark-1.2-contributor-free` (PR #111 MERGED). Paid tier crashes with `APIError: No payment method`. Standing fix at `opencode.yml:358`.
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.
- **Owner 20:08Z challenge:** quality gates are the ONLY merge criteria; the 20-round Lab circuit breaker is a runaway guard that has never merged and did not cause the #104 merge. Recorded; no dissent.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `35a2d68`** (post #104 M0 merge). Branch `opencode/issue103-20260821075928` = `a87118b` is 4 commits ahead (architect blueprint + B5/B10 + B5.5 + B5.6), shares M0 ancestry (NOT orphan). `recover/104` tag exists.
- **Branch work to date:** B5 (predictor bank + ResDiff adaptive rANS), B5.5 (Haar Squeeze scaffold, R11-A inertness guard), B5.6 (176-context activity model + CFL + header fix). Real-Kodak mean **11.43 summed bpp**: M1 PNG gate MET; WebP 9.61 NOT met (gap 1.83); JXL 8.71 NOT met.
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** re-triggered after #104 merge (success).
- **PR #114 (issue #112) - MERGED; #112 CLOSED.** PR #102 - CLOSED. PR #115 - MERGED.

## IN FLIGHT
- **Prism M1-M4 optimization loop (B5-B9):** B5 + B5.5 + B5.6 DONE. This run emits `continue` on PR #104 -> Builder re-opens a continuation PR + pushes B6 (CFL + 5/3 + int32 color-stage widening, M2 < JPEG-LS 9.71), B7 (Squeeze + MA-tree with mandatory `llc_class`/`sibling_class`, M3 < JPEG XL 8.71), B8 (CM + LZP never-expand net, M4 < 8.0), B9 (front-end WebP/TIFF/ICC). After Builder lands code: Reviewer -> Tester on REAL Kodak. NO merge until M3 met bit-exactly (owner override).
  - **M1 status:** real-Kodak mean 11.43 summed bpp (3.81/sample) at effort 0 -> BEATS PNG 13.05 (first M1 gate MET). WebP 9.61 NOT yet met (~17% gap via M1 alone).
  - **M0 non-blocking backlog:** encode_file stub, crc32_combine misname, predict_sample dead stub, container unused var, synthetic-vs-real Kodak CSV - carried into B6+.

## PENDING (in order)
1. **Prism M1-M4 (B6-B9):** Builder (`continue` on #104) -> Reviewer -> Tester (real Kodak, bit-exact, bpp gates M1<13.05 & <9.61, M2<9.71, M3<8.71). NO merge until M3 met bit-exactly.
2. **#42 Board resume (parked):** Ideator batch posted (run 32514723091). PARKED behind Prism per owner directive; pick only after Prism clears the JXL gate.
3. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.
4. **Circuit breaker tuning (owner question):** the 20-round Lab circuit breaker in `lab.yml` is a runaway guard, not a merge trigger. If the owner wants it raised/removed, that is a `lab` change (Lab Engineer) for their merge. No change needed for correctness.

## ISSUES
- **#103 (Prism)** - CLOSED (merged via #104).
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#110 / #108 / #109 / #100 / #62** - CLOSED.
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `35a2d68`. Today's new-project merges: 1/2 (Prism M0; M1-M4 same project).
- **No open PRs.** Branch `opencode/issue103-20260821075928` (`a87118b`) holds the M1-M4 work; `continue` will re-open a continuation PR.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed).
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- **Circuit breaker:** tripped (count >20 on #104) - it halts AUTO re-dispatches only; this run's explicit `continue` is the human-authorized resumption. Next Builder `continue` decision will trip the breaker and hand back to Maintainer rather than auto-firing.

## NEXT STEPS
1. Prism M1-M4: Builder in flight via `continue` on PR #104 (B6-B9 per blueprint). When code lands + continuation PR opens: Reviewer -> Tester on real Kodak; hold merge until M3 (< 8.71 bpp) met bit-exactly per owner override. `data/kodak` is durably provisioned (B10), so the M3 gate is measurable.
2. #42: PARKED - do not pick a board candidate until Prism clears the JXL gate.
3. `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.

## OPEN QUESTIONS
- Prism M1-M4: will the Builder land Squeeze + MA-tree (B7) and cross under JPEG XL 8.71 on real Kodak at M3? (Owner override: no merge until M0+M1+M2+M3 met bit-exactly.)
- WebP 9.61 gate (rest of M1): does weighted predictor tuning + Squeeze+MA-tree close the ~17% gap before B7, or only at M3?
- #42: PARKED behind Prism; resume candidate pick only after Prism clears the JXL gate.
- `lab.yml` Lab Engineer pin still `hy3-free` (free, but no-op risk): bump if a needed `/oc lab` run no-ops.
- Shallow-clone caveat: branch shares M0 ancestry with main (not orphan).

- Mae, the Maintainer
