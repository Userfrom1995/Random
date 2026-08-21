# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32518304833, EVENT `issue_comment` on PR #104, ~19:24Z). PR #104 (Prism M0, issue #103) MERGED at 17:55:24Z; `main`=`35a2d68`. The M1-M4 optimization loop is in flight on the preserved branch `opencode/issue103-20260821075928` (head `05d82e1`), with NO open PR yet. This run re-emits `continue` on PR #104 to open the continuation PR and push B6-B9. No merge until M3 beats JXL on real Kodak per owner override. New-project merges today: **1/2** (Prism M0; M1-M4 is the same project).

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115).
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - upgrade over Obsidian, all major input formats, beats JPEG XL (~3.1 bpp on Kodak). M0 MERGED; M1-M4 optimization loop NOW building (this run, `continue` on PR #104). Owner override: NO merge of any Prism iteration until M0 + M1 + M2 + M3 are all met bit-exactly on REAL Kodak. `data/kodak` durably provisioned (B10).
- **One-PR rule + NEVER delete PR branches:** satisfied; #104 branch `opencode/issue103-20260821075928` preserved (merged without `--delete-branch`).
- **Maintainer sovereign-recovery directive:** `recover` authorized; `main` must never become a divergent/orphan ROOT.
- **Owner WILL (resolved):** builder model = free `opencode/muse-spark-1.2-contributor-free` (PR #111 MERGED). Paid tier crashes with `APIError: No payment method`. Standing fix at `opencode.yml:358`.
- **Owner "don't get distracted" directive:** Prism is THE priority; board candidates parked until Prism clears the JXL gate.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `35a2d68`** (post #104 M0 merge). Local checkout is a SHALLOW CLONE, but `git merge-base origin/main origin/opencode/issue103-20260821075928` = `35a2d68` confirms the branch shares real history with main (NOT orphan). `recover/104` tag = `05d82e1`.
- **Branch `opencode/issue103-20260821075928` = `05d82e1`** carries 3 commits beyond main: `380c566` (Architect M1-M4 blueprint), `74c7b74` (B5 ResDiff adaptive rANS + B10 real-Kodak harness, M1 PNG gate MET 11.52 summed bpp), `05d82e1` (B5.5 Haar Squeeze scaffold, R11-A inertness guard wired). NO open PR for this work.
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** re-triggered after #104 merge (success) - Prism card live.
- **PR #114 (issue #112) - MERGED; #112 CLOSED.** PR #102 - CLOSED. PR #115 - MERGED.

## IN FLIGHT
- **Prism M1-M4 optimization loop (B5-B9):** B5 + B10 DONE; B5.5 Haar Squeeze scaffold in. This run emits `continue` on PR #104 -> Builder opens continuation PR + pushes B6 (CFL + 5/3 + int32 color-stage widening, M2 < JPEG-LS 9.71), B7 (Squeeze + MA-tree with mandatory `llc_class`/`sibling_class`, M3 < JPEG XL 8.71), B8 (CM + LZP never-expand net, M4 < 8.0), B9 (front-end WebP/TIFF/ICC). After Builder lands code: Reviewer -> Tester on REAL Kodak. NO merge until M3 met bit-exactly (owner override).
  - **M1 status:** real-Kodak mean 11.52 summed bpp (3.84/sample) at effort 0 -> BEATS PNG 13.05 (first M1 gate MET). WebP 9.61 NOT yet met (~17% gap).
  - **M0 non-blocking backlog:** encode_file stub, crc32_combine misname, predict_sample dead stub, container unused var, synthetic-vs-real Kodak CSV - carried into B6+.

## PENDING (in order)
1. **Prism M1-M4 (B6-B9):** Builder (`continue` on #104) -> Reviewer -> Tester (real Kodak, bit-exact, bpp gates M1<13.05 & <9.61, M2<9.71, M3<8.71). NO merge until M3 met bit-exactly.
2. **#42 Board resume (parked):** Ideator batch posted (run 32514723091). PARKED behind Prism per owner directive; pick only after Prism clears the JXL gate.
3. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.

## ISSUES
- **#103 (Prism)** - CLOSED (merged via #104).
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#110 / #108 / #109 / #100 / #62** - CLOSED.
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `35a2d68`. Today's new-project merges: 1/2 (Prism M0; M1-M4 same project).
- **No open PRs.** Branch `opencode/issue103-20260821075928` (`05d82e1`) holds the M1-M4 work; `continue` will create the continuation PR.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed).
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- **Circuit breaker:** tripped at 19:10:34Z (21 dispatches > budget 20). It halts AUTO re-dispatches and requires human/Maintainer review - which this run provides via explicit `continue`. Next Builder `continue` decision will trip the breaker and hand back to Maintainer rather than auto-firing.

## NEXT STEPS
1. Prism M1-M4: Builder in flight via `continue` on PR #104 (B6-B9 per blueprint). When code lands + continuation PR opens: Reviewer -> Tester on real Kodak; hold merge until M3 (< 8.71 bpp) met bit-exactly per owner override. `data/kodak` is durably provisioned (B10), so the M3 gate is measurable.
2. #42: PARKED - do not pick a board candidate until Prism clears the JXL gate.
3. `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.

## OPEN QUESTIONS
- Prism M1-M4: will the Builder land Squeeze + MA-tree (B7) and cross under JPEG XL 8.71 on real Kodak at M3? (Owner override: no merge until M0+M1+M2+M3 met bit-exactly.)
- WebP 9.61 gate (rest of M1): does weighted predictor tuning + Squeeze+MA-tree close the ~17% gap before B7, or only at M3?
- #42: PARKED behind Prism; resume candidate pick only after Prism clears the JXL gate.
- `lab.yml` Lab Engineer pin still `hy3-free` (free, but no-op risk): bump if a needed `/oc lab` run no-ops.
- Shallow-clone caveat: confirmed `merge-base` = `35a2d68` (shared history, not orphan).

- Mae, the Maintainer
