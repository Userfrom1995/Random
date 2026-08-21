# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32509651390, EVENT `created` on PR #104, 17:43Z). PR #104 (Prism, issue #103) now carries a complete Fixer rework (head `0c305ff`): reversible YCoCg-R (F1), faithful 32-bit rANS port with H(p)+epsilon gate + Elias-gamma residuals (F2), and an honest progress file (F3). An `opencode-review` run is **in_progress** (32509651373), so no review trigger was emitted. Merge waits on Reviewer approve -> Tester (Kodak vs JXL ~3.1 bpp) approve-test.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; #62 CLOSED).
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak). Active and in the Reviewer gate now.
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved (PR #115 branch deleted post-merge per rebase flow).
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run. Mechanism shipped (PR #114 merged).
- **Owner WILL (resolved):** builder model = free `opencode/muse-spark-1.2-contributor-free` (PR #111 MERGED). Paid tier crashes with `APIError: No payment method`. Standing fix confirmed live at `opencode.yml:358`.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `1f3bd2b`** (post #115 merge; Obsidian promotion landed cleanly). Healthy, shares history with all build branches. PR #104 head `0c305ff` is an ancestor-safe descendant (merge-base with `origin/main` exists - verified NOT orphan).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** last successful deploy served Obsidian as Current after the #115 merge (run 32504672348 success); a PR-preview deploy for #104 also re-fired on the fixer push (32509620542).
- **PR #114 (issue #112) - MERGED** (recovery infra shipped). **#112 CLOSED.**
- **PR #102 - CLOSED.** Issue #42 Brainstorm Board now unblocked.
- Issue #110 CLOSED (via #111 merge).

## IN FLIGHT
1. **PR #104 (Prism, issue #103) - OPEN, in Reviewer gate after Fixer rework.** Head `0c305ff` (branch `opencode/issue103-20260821075928`). The Fixer resolved all three Reviewer blockers (F1 lossy YCoCg-R, F2 stub/non-rANS coder + missing H(p)+epsilon gate, F3 dishonest progress file). `opencode-review` run 32509651373 is **in_progress**; a second review (32509662423) is queued. Decision list this run = `[]` (no duplicate review trigger). After `/oc approve` -> Tester (Kodak vs JXL ~3.1 bpp) -> Mae merge -> close #103. New-project budget 0/2, room to merge.

## PENDING (in order)
1. **PR #104 review -> test -> merge:** wait for the in-flight Reviewer to approve the fixed rANS + YCoCg-R; then the Tester runs Kodak vs JXL 3.1 bpp; then Mae merges (budget 0/2, allowed) and closes #103.
2. **#42 Board resume:** #102 is CLOSED, Brainstorm Board unblocked; pick from parked candidates after Prism clears.
3. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (code in #104, in review).
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#110 (paid model crash)** - CLOSED (resolved by merged #111).
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; now unblocked (was blocked on #102, now closed).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#102** - CLOSED.
- **#62 (Fix README and website)** - CLOSED (since 08-15 by #63; #115 only synced the files).

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `1f3bd2b`. Today's new-project merges: 0/2 (PR #115 docs, #109/#111/#114 infra - none count).
- PR #104: `opencode-review` 32509651373 **in_progress** (re-review of fixed head `0c305ff`); no merge until `/oc approve-test` arrives.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed). Standing worker pin `nemotron-3-ultra-free` available as fallback.
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- `maintainer.yml` trigger dispatch FIXED on main (`/oc recover` can post).

## NEXT STEPS
1. PR #104: let the in-flight Reviewer (32509651373) finish -> if approved, Tester runs Kodak vs JXL -> Mae merges (budget 0/2) and closes #103.
2. #42: resume Brainstorm Board picks after Prism clears.
3. `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.

## OPEN QUESTIONS
- PR #104: will the Reviewer approve the fixed rANS + reversible YCoCg-R (head `0c305ff`), then Tester pass Kodak vs JXL 3.1 bpp, Mae merge -> close #103?
- #42: now unblocked by #102 closing; resume candidates after Prism.
- `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer
