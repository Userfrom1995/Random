# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32485029286, event `/oc maintainer` on PR #114, 13:05Z). PR #114 (lab recovery #112) found ORPHAN - dispatched Lab Engineer to re-link (cherry-pick only the 4 recovery commits, drop stray paid-model commit + ancient history). Reviewer/test already in flight on the branch; will re-fire after re-link. Prism build (#104) still in flight on free model.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak).
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run.
- **Owner WILL (resolved):** builder model = free `opencode/muse-spark-1.2-contributor-free` (PR #111 MERGED). Paid tier crashes with `APIError: No payment method`. Standing fix confirmed live at `opencode.yml:358`.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `043bd6d`** (post #111 merge). Builder pin FIXED: `opencode/muse-spark-1.2-contributor-free` (FREE).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** deployed (run 652 success); PR #114 preview deployed (run 32484838365).
- Issue #110 CLOSED (via #111 merge).

## IN FLIGHT
1. **PR #114 (lab recovery for #112) - ORPHAN, being re-linked.** Branch `opencode/issue112-20260821125724` has NO merge base with `main` and carries 15 stray ancient commits + stray paid-model commit `9aeea30`. Net diff vs main = exactly the 9 intended recovery files (+520/-10). Lab Engineer (`/oc lab` on #114, this run) to: branch from `origin/main`, cherry-pick ONLY `eeca80b ca7c74d cf2bb3a ae57f14`, keep free model at `opencode.yml:358`, force-update branch. Reviewer (runs 32484840192 in_progress, 32485029184 pending) + tester already queued; will re-evaluate the re-linked branch. After clean re-link + review approve + test pass -> Mae merges (lab infra, no daily-project limit) and #112 closes.
2. **PR #104 (Prism, issue #103).** Build in flight on free `muse-spark-1.2-contributor-free`: owner `/oc continue` run 1097 (in_progress 32484561400) + `/oc build this` run 1099 (pending 32484568557). Must ship `prism/` C++ through M0 fuzz gate before optimization. Not re-triggered.
3. **#112 lab recovery mechanism** - delivered as PR #114 (content correct; history being fixed).

## PENDING (in order)
1. **PR #114 re-link** (Lab Engineer) -> review -> test -> Mae merge -> close #112.
2. **Prism build (#104):** Builder ships `prism/` through M0; review -> test (Kodak vs JXL ~3.1 bpp) -> merge (0/2 new-project budget used today).
3. **#102 wall:** genuine `git push` `workflows`-scope on `OPENCODE_PAT`; owner to grant scope or merge manually; then close #42.
4. **Board (#42) resume:** after Prism, pick from parked candidates.
5. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build in flight).
- **#112 (automatic PR recovery)** - OPEN; delivered via PR #114 (being re-linked).
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
1. Lab Engineer re-links PR #114 branch (cherry-pick 4 recovery commits, drop paid-model + ancient history).
2. Reviewer re-approves re-linked #114; Tester passes; Mae merges #114 -> close #112.
3. Prism build (#104) completes on free model -> review -> test -> merge.

## OPEN QUESTIONS
- Will the Lab Engineer re-link succeed, or no-op on `hy3-free`? If no-op, escalate to emergency direct edit of `lab.yml` pin (but branch surgery still needs an agent push - fall back to `recover` semantics or owner action).
- Will the Builder on free `muse-spark-1.2-contributor-free` execute + push `prism/` C++ and hit M0 fuzz gate, then beat JXL 3.1 bpp on Kodak?
- Does run 1099 (`/oc build this` on #103) open a second PR, or reuse #104's branch? Consolidate at review if so.
- #102: owner to grant `workflows` scope to `OPENCODE_PAT` or merge manually; its `ideate.yml` change still needed for #42.
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer
