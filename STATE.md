# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32517107998, EVENT `issue_comment` on PR #104, ~19:10Z). PR #104 (Prism M0, issue #103) MERGED at 17:55:24Z; `main`=`35a2d68`. The M1-M4 optimization loop is in flight on the preserved branch `opencode/issue103-20260821075928` (head `749cc5e`), NOT yet re-merged. This run re-emits `continue` on PR #104 to push B6-B9 (M2/M3/M4) toward the owner's JXL-beating goal. New-project merges today: **1/2** (Prism M0; M1-M4 is the same project, not a new one).

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115).
- **NEXT PRIORITY (owner, 07:49Z):** build **Prism (issue #103)** - upgrade over Obsidian, all major input formats, beats JPEG XL (~3.1 bpp on Kodak). M0 MERGED; M1-M4 optimization loop NOW being built (this run, `continue` on PR #104). Owner override: NO merge of any Prism iteration until M0 + M1 + M2 + M3 are all met bit-exactly on REAL Kodak. `data/kodak` must be durably provisioned (Obsidian lesson).
- **One-PR rule + NEVER delete PR branches:** satisfied; #104 branch `opencode/issue103-20260821075928` preserved (merged without `--delete-branch`).
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT.
- **Owner WILL (resolved):** builder model = free `opencode/muse-spark-1.2-contributor-free` (PR #111 MERGED). Paid tier crashes with `APIError: No payment method`. Standing fix confirmed live at `opencode.yml:358`.
- **Owner "don't get distracted" directive (07:49Z/18:46Z):** Prism is THE priority; board candidates parked until Prism clears the JXL gate.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `35a2d68`** (post #104 M0 merge). NOTE: local checkout is a SHALLOW CLONE (`.git/shallow`), so `origin/main` shows only 1 commit locally and `merge-base` vs the PR branch reads empty - FALSE NEGATIVE. The branch shares real history with `main` (it was rebased onto `35a2d68` before the M1 work); not orphan. Final rebase-merge dedupes identical M0 commits by patch-id.
- **Branch `opencode/issue103-20260821075928` = `749cc5e`** carries M0 commits (already rebase-merged into main) + the Architect's M1-M4 blueprint (`prism/docs/architecture-m1-m4.md`, `647a3f1`) + B5/B10 M1 work (predictor bank + ResDiff rANS + real-Kodak harness). `recover/104` tag = `749cc5e`.
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** re-triggered after #104 merge (runs 32510773918 / 32510898951, success) - Prism card live.
- **PR #114 (issue #112) - MERGED**; **#112 CLOSED**.
- **PR #102 - CLOSED.** #42 Brainstorm Board unblocked.
- **PR #115 (issue #62/README+site) - MERGED.** Obsidian promoted to Current.

## IN FLIGHT
- **Prism M1-M4 optimization loop (B5-B9):** M1 B5 + B10 DONE. Builder `continue` (this run, PR #104) to implement B6 (CFL + 5/3 + int32 color-stage widening, M2 < JPEG-LS 9.71), B7 (Squeeze + MA-tree with mandatory `llc_class`/`sibling_class`, M3 < JPEG XL 8.71), B8 (CM + LZP never-expand net, M4 < 8.0 stretch), B9 (front-end WebP/TIFF/ICC). After Builder lands code: Reviewer -> Tester on REAL Kodak. NO merge until M3 met bit-exactly (owner override).
  - **M1 status:** real-Kodak mean 11.523 summed bpp (3.841/sample) at effort 0 -> BEATS PNG 13.05 (first M1 gate MET). WebP 9.61 NOT yet met (~17% gap); needs weighted predictor / Squeeze+MA-tree.

## PENDING (in order)
1. **Prism M1-M4 (B6-B9):** Builder (`continue` on #104) -> Reviewer -> Tester (real Kodak, bit-exact, bpp gates M1<13.05 & <9.61, M2<9.71, M3<8.71). M0 non-blocking backlog (encode_file stub, crc32_combine misname, predict_sample dead stub, container unused var) carries into B6+.
2. **#42 Board resume (parked):** Ideator batch posted earlier. PARKED behind Prism per owner directive; pick only after Prism clears the JXL gate.
3. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.

## ISSUES
- **#103 (Prism)** - CLOSED (merged via #104).
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#110 (paid model crash)** - CLOSED (resolved by merged #111).
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#62 (Fix README and website)** - CLOSED (by #63; #115 synced the files).
- **#115 (Obsidian landing sync)** - MERGED.
- **#42 (Brainstorm Board)** - OPEN; parked behind Prism.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` (remote) = `35a2d68`. Today's new-project merges: 1/2 (Prism M0; M1-M4 same project).
- No open PRs for the branch yet (PR #104 merged). The Builder's `continue` resume will re-open/continue a PR for the M1-M4 branch as needed via `gh pr create` in builder.md resume mode.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed).
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- **Circuit breaker:** autonomous auto-continue guard tripped at 19:10:34Z (21 dispatches > budget 20). It halts *auto* re-dispatches and requires human/Maintainer review - which is the path taken here (explicit `continue`). Next Builder `continue` decision will trip the breaker and hand back to Maintainer rather than auto-firing.

## NEXT STEPS
1. Prism M1-M4: Builder in flight via `continue` on PR #104 (B6-B9 per blueprint). When code lands: Reviewer -> Tester on real Kodak; hold merge until M3 (< 8.71 bpp) met bit-exactly per owner override. `data/kodak` is now durably provisioned (B10), so the M3 gate is measurable.
2. #42: PARKED - do not pick a board candidate until Prism clears the JXL gate.
3. `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.

## OPEN QUESTIONS
- Prism M1-M4: will the Builder land Squeeze + MA-tree (B7) and cross under JPEG XL 8.71 on real Kodak at M3? (Owner override: no merge until M0+M1+M2+M3 met bit-exactly.)
- WebP 9.61 gate (rest of M1): does weighted predictor tuning + Squeeze+MA-tree close the ~17% gap before B7, or only at M3?
- `data/kodak` provisioning: durably present (B10, SHA256-pinned) for the Tester's M3 gate - confirmed.
- #42: PARKED behind Prism; resume candidate pick only after Prism clears the JXL gate.
- `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.
- Shallow-clone caveat: confirm at merge time that `main` truly shares history with the PR branch (the local empty `merge-base` is a shallow false negative).

- Mae, the Maintainer
