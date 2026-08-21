# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32484559688, event `/oc maintainer` on PR #104, 12:59Z). Build pin fixed (free `muse-spark-1.2-contributor-free`); Prism build now LIVE via owner's direct `/oc continue` (run 1097) + `/oc build this` (run 1099). Lab recovery #112 in flight (run 398). No duplicate triggers emitted this run.

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
1. **PR #104 (Prism spec, issue #103).** Docs-only research/architecture spec on branch `opencode/issue103-20260821075928`. NOW THE CANONICAL BUILD VEHICLE: owner's `/oc continue` (run 1097, in_progress) resumes the Builder here on the free model. Must ship `prism/` C++ through M0 (bit-exact round-trip + corruption-rejection fuzz gate) before optimization.
2. **Prism build - second run (run 1099).** Owner's `/oc build this` on issue #103 (12:59:31Z) also in progress on the free model. If it opens a fresh branch/PR, consolidate at review in favor of #104 (which holds the binding architecture contract).
3. **Lab recovery (issue #112).** Run `398` (`Opencode Lab Engineer`, in_progress, 12:59:35Z) - automatic PR-recovery mechanism. Risk: `lab.yml:59` still pins `hy3-free` (no-op model); if run 398 no-ops, next maintainer run escalates to a direct edit of `lab.yml` per emergency policy.

## PENDING (in order)
1. **Prism build:** Builder (free model) implements `prism/` through M0 fuzz gate on PR #104. Review -> test (Kodak vs JXL ~3.1 bpp) -> merge.
2. **Lab recovery #112:** deliver automatic PR-recovery; if Lab Engineer no-ops, direct-edit `lab.yml` Lab Engineer pin off `hy3-free`.
3. **#102 wall:** genuine `git push` `workflows`-scope on `OPENCODE_PAT`; owner to grant scope or merge manually; then close #42.
4. **Board (#42) resume:** after Prism, pick from parked candidates.
5. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** becomes priority if run 398 no-ops.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build now live).
- **#112 (automatic PR recovery)** - OPEN; Lab Engineer (run 398) dispatched.
- **#110 (paid model crash)** - CLOSED (resolved by merged #111).
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `043bd6d`. Today's new-project merges: 0/2 (Prism not yet built; #109/#111 were infra).
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed). Standing worker pin `nemotron-3-ultra-free` available as fallback.
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (nondeterministic no-op risk; escalates if run 398 no-ops).

## NEXT STEPS
1. Builder (free model) ships `prism/` on PR #104 through M0 fuzz gate (run 1097 in progress).
2. Review -> test (Kodak vs JXL ~3.1 bpp) -> merge Prism.
3. Monitor Lab recovery run 398; if no-op, direct-edit `lab.yml:59` off `hy3-free`.

## OPEN QUESTIONS
- Will the Builder on free `muse-spark-1.2-contributor-free` execute + push C++ and hit M0 fuzz gate, then beat JXL 3.1 bpp on Kodak?
- Does run 1099 (`/oc build this` on #103) open a second PR, or reuse #104's branch? Consolidate at review if so.
- #102: owner to grant `workflows` scope to `OPENCODE_PAT` or merge manually; its `ideate.yml` change still needed for #42.
- `lab.yml` Lab Engineer pin still `hy3-free`: if run 398 no-ops, direct-edit per emergency policy.
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer
