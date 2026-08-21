# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32510142864, EVENT `created` on PR #104, 17:49Z). PR #104 (Prism, issue #103) head `47a3a98` carries the complete M0 codec + the three checklist fixes the Reviewer flagged at 17:47 (ideas/ entry, root index.html Prism link, removed CLI-tool web entrypoints). An `opencode-review` run is **in_progress** (32510132470) on the latest head, so no review trigger was emitted. Merge waits on Reviewer approve -> Tester (Kodak vs JXL ~3.1 bpp) approve-test.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 manually merged by owner as orphan root `60748e88`; promoted to Current via merged PR #115; #62 CLOSED).
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak). Active and in the Reviewer gate now.
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run. Mechanism shipped (PR #114 merged).
- **Owner WILL (resolved):** builder model = free `opencode/muse-spark-1.2-contributor-free` (PR #111 MERGED). Paid tier crashes with `APIError: No payment method`. Standing fix confirmed live at `opencode.yml:358`.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `6042785`** (post #115 merge; the PR #104 branch tip `47a3a98` descends from it, so `main` and #104 share full history - NOT orphan). PR #104 head `47a3a98` is an ancestor-safe descendant (merge-base with `origin/main` exists - verified NOT orphan).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** last successful deploy served Obsidian as Current after the #115 merge (run 32504672348 success); a PR-preview deploy for #104 also re-fired on the fixer push (32509620542).
- **PR #114 (issue #112) - MERGED** (recovery infra shipped). **#112 CLOSED.**
- **PR #102 - CLOSED.** Issue #42 Brainstorm Board now unblocked.
- Issue #110 CLOSED (via #111 merge).

## IN FLIGHT
1. **PR #104 (Prism, issue #103) - OPEN, in Reviewer gate after final Fixer checklist fixes.** Head `47a3a98` (branch `opencode/issue103-20260821075928`). The Fixer resolved: F1 (lossy YCoCg-R -> reversible), F2 (stub/non-rANS -> faithful 32-bit rANS with H(p)+epsilon gate + Elias-gamma residuals), F3 (dishonest progress file corrected), plus the 17:47 checklist items (ideas/ entry, root index.html Prism link, removed `prism/index.html` + `prism/web/index.html`). `opencode-review` run 32510132470 is **in_progress** on head `47a3a98`; a pending 32510142859 is queued. Decision list this run = `[]` (no duplicate review trigger). After `/oc approve` -> Tester (Kodak vs JXL ~3.1 bpp) -> Mae merge -> close #103. New-project budget 0/2, room to merge.

## PENDING (in order)
1. **PR #104 review -> test -> merge:** wait for the in-flight Reviewer (32510132470) to approve the fixed build; then the Tester runs Kodak vs JXL 3.1 bpp; then Mae merges (budget 0/2, allowed) and closes #103.
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
- **#115 (Obsidian landing sync)** - MERGED (this run's predecessor); `main` = `6042785`.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `6042785`. Today's new-project merges: 0/2 (PR #115 docs, #109/#111/#114 infra - none count).
- PR #104: `opencode-review` 32510132470 **in_progress** (reviewing head `47a3a98`); no merge until `/oc approve-test` arrives.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed). Standing worker pin `nemotron-3-ultra-free` available as fallback.
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- `maintainer.yml` trigger dispatch FIXED on main (`/oc recover` can post).

## NEXT STEPS
1. PR #104: let the in-flight Reviewer (32510132470) finish -> if approved, Tester runs Kodak vs JXL -> Mae merges (budget 0/2) and closes #103.
2. #42: resume Brainstorm Board picks after Prism clears.
3. `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.

## OPEN QUESTIONS
- PR #104: will the Reviewer (32510132470) approve the full build (F1/F2/F3 resolved at `0c305ff` + checklist items 7/8 closed at `47a3a98`), then Tester pass Kodak vs JXL 3.1 bpp, Mae merge -> close #103? (New-project budget 0/2, room available.)
- #42: now unblocked by #102 closing; resume candidates after Prism.
- `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer
