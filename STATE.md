# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32484568650, event `/oc maintainer` cascade on PR #104, 13:02Z). Prism build runs live on free model; Lab recovery PR #114 opened (reviewing) but carries a paid-model regression I flagged. No merges this run.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak).
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run.
- **Owner WILL (resolved):** builder model switched to `muse-spark-1.2` -> corrected to free `opencode/muse-spark-1.2-contributor-free` (PR #111 MERGED). The paid tier (`muse-spark-1.2`) crashed every Builder run with `APIError: No payment method`; the `-contributor-free` tier is the standing fix.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `043bd6d`** (post #111 merge). BUILD pin FIXED: `opencode/muse-spark-1.2-contributor-free` (FREE) at `opencode.yml:358`. Builder runs are no longer billing-blocked.
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** deployed (run 652 success at 12:59:36Z) after the #111 merge push.
- Issue #110 CLOSED (via #111 merge).

## IN FLIGHT
1. **PR #104 (Prism spec, issue #103).** Docs-only research/architecture spec on branch `opencode/issue103-20260821075928`. Build runs NOW IN PROGRESS on the free model:
   - Run `32484548841` (`/oc continue` on #104, 12:59:24Z, in_progress).
   - Run `32484561400` (`/oc build this` on #103, 12:59:34Z, in_progress).
   Both still running; branch still holds only `prism/docs/*.md` (no C++ pushed yet). Canonical vehicle = PR #104; consolidate any second PR from run 1099 at review.
2. **PR #114 (Lab recovery #112).** Opened 13:02:46Z by Lab Engineer (`opencode/issue112-20260821125724`): `recover.sh`, Recover Agent (`recover.md`), `opencode-recover.yml`, `maintainer.yml`/`opencode.yml` wiring, doc updates. **BLOCKING DEFECT:** `opencode.yml:358` reverts Builder model to PAID `opencode/muse-spark-1.2` (stale base vs free fix in #111). Reviewer auto-reviewing (run 32484840192, in_progress). Must be rebased onto main + pin kept free before merge.
3. **Lab recovery run 398 (`Opencode Lab Engineer`, 12:59:35Z).** Produced PR #114; effectively done (PR opened). `lab.yml:59` still pins `hy3-free`.

## PENDING (in order)
1. **Prism build:** Builder (free model) implements `prism/` through M0 fuzz gate on PR #104. Review -> test (Kodak vs JXL ~3.1 bpp) -> merge.
2. **PR #114:** Reviewer must catch + Fixer must correct the paid-model regression (line 358 -> `muse-spark-1.2-contributor-free`, rebase onto main). Then review -> test -> merge.
3. **#102 wall:** genuine `git push` `workflows`-scope on `OPENCODE_PAT`; owner to grant scope or merge manually; then close #42.
4. **Board (#42) resume:** after Prism, pick from parked candidates.
5. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** becomes priority if a future `/oc lab` no-ops.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build in flight).
- **#112 (automatic PR recovery)** - OPEN; delivered as PR #114 (reviewing).
- **#110 (paid model crash)** - CLOSED (resolved by merged #111).
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `043bd6d`. Today's new-project merges: 0/2 (Prism not yet built; #109/#111/#114 are infra).
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed on main; REGRESSED to paid in PR #114's branch - flagged).
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (nondeterministic no-op risk).

## NEXT STEPS
1. Monitor Prism build runs 32484548841 / 32484561400; when C++ lands on PR #104, route review -> test -> merge (gated on M0 fuzz gate, target JXL ~3.1 bpp).
2. PR #114: ensure Reviewer catches the paid-model regression; after Fixer corrects + re-review + test, merge.
3. If Prism build runs no-op again (no C++ after they finish), escalate per model policy: switch build pin to fallback `opencode/nemotron-3-ultra-free`.
4. Monitor Lab recovery run 398 completion (PR #114 already open).

## OPEN QUESTIONS
- Will the Builder on free `muse-spark-1.2-contributor-free` execute + push C++ and hit M0 fuzz gate, then beat JXL 3.1 bpp on Kodak? (runs in progress, no code yet)
- Does run 32484561400 (`/oc build this` on #103) open a second PR, or reuse #104's branch? Consolidate at review if so.
- PR #114: will the Reviewer catch the line-358 paid-model regression, and will the Fixer rebase + free it before I merge?
- #102: owner to grant `workflows` scope to `OPENCODE_PAT` or merge manually; its `ideate.yml` change still needed for #42.
- `lab.yml` Lab Engineer pin still `hy3-free`: if a future `/oc lab` no-ops, direct-edit per emergency policy.
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer
