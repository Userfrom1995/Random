# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32515615737, EVENT `created` on issue/PR #104, 18:53Z). Repo idle on open PRs: none. PR #104 (Prism M0, issue #103) MERGED at 17:55:24Z; `main`=`35a2d68`. The Architect's M1-M4 blueprint is on the preserved branch `opencode/issue103-20260821075928` (head `647a3f1`), NOT yet in `main`. This run routes the Builder (`continue` on PR #104) to implement M1-M4 (B5-B9). New-project merges today: **1/2** (Prism M0; M1-M4 is the same project, not a new one).

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115).
- **NEXT PRIORITY (owner, 07:49Z):** build **Prism (issue #103)** - upgrade over Obsidian, all major input formats, beats JPEG XL (~3.1 bpp on Kodak). M0 MERGED; M1-M4 optimization loop NOW being built (this run, `continue` on PR #104). Owner override: NO merge of any Prism iteration until M0 + M1 + M2 + M3 are all met bit-exactly on REAL Kodak. `data/kodak` must be durably provisioned (Obsidian lesson).
- **One-PR rule + NEVER delete PR branches:** satisfied; #104 branch `opencode/issue103-20260821075928` preserved (merged without `--delete-branch`).
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT.
- **Owner WILL (resolved):** builder model = free `opencode/muse-spark-1.2-contributor-free` (PR #111 MERGED). Paid tier crashes with `APIError: No payment method`. Standing fix confirmed live at `opencode.yml:358`.
- **Owner "don't get distracted" directive (07:49Z/18:46Z):** Prism is THE priority; board candidates parked until Prism clears the JXL gate.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `35a2d68`** (post #104 M0 merge). NOTE: local checkout is a SHALLOW CLONE (`.git/shallow`), so `origin/main` shows only 1 commit locally and `merge-base` vs the PR branch reads empty - FALSE NEGATIVE. The branch shares real history with `main`; not orphan. Final rebase-merge dedupes identical M0 commits by patch-id.
- **Branch `opencode/issue103-20260821075928` = `647a3f1`** carries M0 commits (original SHAs, already rebase-merged into main under new SHAs) + the Architect's M1-M4 blueprint (`prism/docs/architecture-m1-m4.md`).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** re-triggered after #104 merge (runs 32510773918 / 32510898951, success) - Prism card live.
- **PR #114 (issue #112) - MERGED**; **#112 CLOSED**.
- **PR #102 - CLOSED.** #42 Brainstorm Board unblocked.
- **PR #115 (issue #62/README+site) - MERGED.** Obsidian promoted to Current.

## IN FLIGHT
- **Prism M1-M4 optimization loop (B5-B9):** this run emitted `continue` on PR #104 to build predictor bank + LOCO-I residual (M1), CFL + 5/3 + int32 color-stage widening (M2), Squeeze + MA-tree with mandatory `llc_class`/`sibling_class` (M3), CM + LZP never-expand (M4), per `prism/docs/architecture-m1-m4.md`. After Builder lands code: Reviewer -> Tester on REAL Kodak (M1 < PNG 13.05, M2 < JPEG-LS 9.71, M3 < JPEG XL 8.71). NO merge until M3 met bit-exactly (owner override).

## PENDING (in order)
1. **Prism M1-M4:** Builder (`continue` on #104) -> Reviewer -> Tester (real Kodak, bit-exact, bpp gates). M0 non-blocking backlog (encode_file stub, crc32_combine misname, predict_sample dead stub, container unused var, real-Kodak byte-cmp wiring) carries into B5.
2. **#42 Board resume (parked):** Ideator batch posted earlier (Cartograph/Lyricon/Quartz + prior candidates). PARKED behind Prism per owner directive; pick only after Prism clears the JXL gate.
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
- No open PRs. Nothing pending review/test until the Builder's M1-M4 run lands.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed).
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- `maintainer.yml` trigger dispatch FIXED on main (`/oc recover` can post).

## NEXT STEPS
1. Prism M1-M4: Builder in flight via `continue` on PR #104 (B5-B9 Squeeze + MA-tree per blueprint). When code lands: Reviewer -> Tester on real Kodak; hold merge until M3 (< 8.71 bpp) met bit-exactly per owner override. Confirm `data/kodak` is durably provisioned before Tester runs.
2. #42: PARKED - do not pick a board candidate until Prism clears the JXL gate.
3. `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.

## OPEN QUESTIONS
- Prism M1-M4: will the Builder land Squeeze + MA-tree and cross under JPEG XL 8.71 on real Kodak at M3? (Owner override: no merge until M0+M1+M2+M3 met bit-exactly.)
- `data/kodak` provisioning: is it durably present for the Tester's M3 gate? (Obsidian lesson - absence made gates unmeasurable.)
- #42: PARKED behind Prism; resume candidate pick only after Prism clears the JXL gate.
- `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.
- Shallow-clone caveat: confirm at merge time that `main` truly shares history with the PR branch (the local empty `merge-base` is a shallow false negative).

- Mae, the Maintainer
