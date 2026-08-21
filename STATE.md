# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32485778245, EVENT `/oc maintainer`/`/oc review` on PR #114, 13:14Z). PR #114 ORPHAN RE-LINKED CLEAN: remote head `a05e323` shares history with `main` (`043bd6d`), carries exactly the 5 intended recovery commits, free model pin, doc-sync done (reviewer's blocking findings cleared). Reviewer re-review IN FLIGHT (run 32485778137). Merge held until approval + test pass.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak).
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run.
- **Owner WILL (resolved):** builder model = free `opencode/muse-spark-1.2-contributor-free` (PR #111 MERGED). Paid tier crashes with `APIError: No payment method`. Standing fix confirmed live at `opencode.yml:358`.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `043bd6d`** (post #111 merge). Builder pin FIXED: `opencode/muse-spark-1.2-contributor-free` (FREE).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** deployed (run 32485779246 success); PR #114 preview deployed (run 32485769167).
- Issue #110 CLOSED (via #111 merge).

## IN FLIGHT
1. **PR #114 (lab recovery for #112) - ORPHAN RE-LINKED, review in flight.** Remote head `a05e323` (13:13:28Z) shares history with `main`; `git log origin/main..HEAD` = 5 intended recovery commits (`a05e323 88a4c7c 4f2305a 330afb2 6367d38`, all "Recover #112"); stray paid commit `9aeea30` + 15 ancient commits gone. `git diff` vs main = 23 files (+538/-13); `opencode.yml:358` = FREE `muse-spark-1.2-contributor-free`. Doc-sync (reviewer blocking findings 1&2) present in `a05e323`. Reviewer re-review RUNNING: 32485778137 (pending) + 32485767787 (in_progress), both after the re-link. On approval -> Tester auto-fires -> Mae merges (lab infra, no daily-project limit) -> #112 closes. NON-BLOCKING follow-up noted: switch recover-tag step in `opencode.yml` to `github.token` + scope `opencode-recover.yml` `actions: write`.
2. **PR #104 (Prism, issue #103).** Build in flight on free `muse-spark-1.2-contributor-free`: owner `/oc continue` run 1097 + `/oc build this` run 1099. Must ship `prism/` C++ through M0 fuzz gate before optimization. Not re-triggered.
3. **#112 lab recovery mechanism** - delivered as PR #114 (content correct; branch now cleanly re-linked).

## PENDING (in order)
1. **PR #114 review -> test -> Mae merge -> close #112.** (Reviewer in flight now.)
2. **PAT-scope hygiene PR (non-blocking):** `opencode.yml` recover-tag step -> `github.token`; scope `opencode-recover.yml` `actions: write`. Schedule via Lab Engineer later.
3. **Prism build (#104):** Builder ships `prism/` through M0; review -> test (Kodak vs JXL ~3.1 bpp) -> merge (0/2 new-project budget used today).
4. **#102 wall:** genuine `git push` `workflows`-scope on `OPENCODE_PAT`; owner to grant scope or merge manually; then close #42.
5. **Board (#42) resume:** after Prism, pick from parked candidates.
6. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build in flight).
- **#112 (automatic PR recovery)** - OPEN; delivered via PR #114 (re-linked, review in flight).
- **#110 (paid model crash)** - CLOSED (resolved by merged #111).
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `043bd6d`. Today's new-project merges: 0/2 (Prism not yet built; #109/#111/#114 are infra).
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed). Standing worker pin `nemotron-3-ultra-free` available as fallback.
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).

## NEXT STEPS
1. Reviewer (32485778137) approves re-linked #114 -> Tester passes -> Mae merges #114 -> close #112.
2. Schedule non-blocking PAT-scope hygiene PR for `opencode.yml` / `opencode-recover.yml`.
3. Prism build (#104) completes on free model -> review -> test -> merge.

## OPEN QUESTIONS
- Will the in-flight reviewer (32485778137) approve the re-linked branch? (Expected yes - blocking findings cleared by `a05e323`.)
- Will the Builder on free `muse-spark-1.2-contributor-free` execute + push `prism/` C++ and hit M0 fuzz gate, then beat JXL 3.1 bpp on Kodak?
- Does run 1099 (`/oc build this` on #103) open a second PR, or reuse #104's branch? Consolidate at review if so.
- #102: owner to grant `workflows` scope to `OPENCODE_PAT` or merge manually; its `ideate.yml` change still needed for #42.
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer
