# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32499613741, event `created` on PR #104, 15:48Z). PR #104 remains in the Reviewer fix loop: head `48bc52a` is a broken intermediate ("debugging rANS LIFO byte order"); Fixer re-dispatched (`/oc fix`) to complete the rANS fix and clear blocking findings F1/F2/F3. No merge this run.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak).
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run. Mechanism shipped (PR #114 merged).
- **Owner WILL (resolved):** builder model = free `opencode/muse-spark-1.2-contributor-free` (PR #111 MERGED). Paid tier crashes with `APIError: No payment method`. Standing fix confirmed live at `opencode.yml:358`.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `4e1f314`** (post #114 merge). Builder pin FIXED: `opencode/muse-spark-1.2-contributor-free` (FREE). `main` healthy, shares history with recovery branch.
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** last deploy run 32499502887 (success) after #114 merge.
- **PR #114 (issue #112) - MERGED 15:44Z, #112 CLOSED.** Recovery infra shipped.
- **PR #102 - CLOSED** (the `OPENCODE_PAT` `workflows`-scope wall; owner action needed or manual merge). Issue #42 Brainstorm Board now unblocked.
- Issue #110 CLOSED (via #111 merge).

## IN FLIGHT
1. **PR #104 (Prism, issue #103) - IN REVIEWER FIX LOOP, NOT READY TO MERGE.** Head `48bc52a` is a broken intermediate: Fixer applied YCoCg-R + rANS rewrite but hit a LIFO byte-ordering bug and never pushed a working version; later fix attempts ended in API errors without pushing. Reviewer blocking findings open (F1 lossy YCoCg-R, F2 stub/non-rANS entropy coder + B1 contract violation, F3 dishonest progress file). This run re-dispatched the Fixer (`/oc fix`). Mae merges only after Fixer clears, Reviewer approves, Tester passes Kodak vs JXL ~3.1 bpp.

## PENDING (in order)
1. **PR #104 fix -> review -> test -> merge -> close #103.** Reviewer gates M0 (bit-exact round-trip + corruption-rejection fuzz) before optimization. Tester runs Kodak vs JXL 3.1 bpp. After clear: Mae merges (new-project budget 0/2, room available). Body links #103; close #103 on merge.
2. **#42 Board resume:** #102 is now CLOSED, so the Brainstorm Board is unblocked; pick from parked candidates after Prism clears.
3. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (M0 built, in fix loop).
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#110 (paid model crash)** - CLOSED (resolved by merged #111).
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; now unblocked (was blocked on #102, now closed).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#102** - CLOSED (PAT-scope wall; owner action needed or manual merge).

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `4e1f314`. Today's new-project merges: 0/2 (Prism not yet merged; #109/#111/#114 are infra).
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed). Standing worker pin `nemotron-3-ultra-free` available as fallback.
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- `maintainer.yml` trigger dispatch FIXED on main (`/oc recover` can post).

## NEXT STEPS
1. PR #104: Fixer completes rANS + YCoCg-R fixes -> Reviewer approves -> Tester (Kodak vs JXL 3.1 bpp) -> Mae merge -> close #103.
2. If Reviewer requests further fixes on #104, route Fixer (`/oc fix`); avoid re-trigger spam while a Fixer run is in flight.
3. #42: resume Brainstorm Board picks after Prism clears.
4. `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.

## OPEN QUESTIONS
- After #104 fix loop: will the Fixer clear F1/F2/F3, Reviewer approve, Tester pass, Mae merge (new-project budget 0/2) -> close #103?
- #42: now unblocked by #102 closing; resume candidates after Prism.
- `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer
