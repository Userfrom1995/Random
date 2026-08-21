# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32504471736, EVENT `created` on PR #115, 16:45Z). PR #115 (Builder fix for issue #62: Obsidian -> Current, Meridian -> top of Previous, README + index.html synced) is now **MERGED** (`main` = `1f3bd2b`). Reviewer approved 16:43:03Z, Tester approved 16:44:14Z, no later fix findings. Issue #62 was already CLOSED (by PR #63, 08-15), so no further closure. pages.yml re-triggered (32504672348) because the merge push did not auto-deploy.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); now properly promoted to Current via merged PR #115. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak).
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved (PR #115 branch deleted post-merge per rebase flow).
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run. Mechanism shipped (PR #114 merged).
- **Owner WILL (resolved):** builder model = free `opencode/muse-spark-1.2-contributor-free` (PR #111 MERGED). Paid tier crashes with `APIError: No payment method`. Standing fix confirmed live at `opencode.yml:358`.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `1f3bd2b`** (post #115 merge; Obsidian promotion landed cleanly). Healthy, shares history with all build branches. PR #115 head `812ed29` is now an ancestor via the rebased tip.
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** manually re-triggered run 32504672348 (waiting) after the #115 merge; prior auto run 32504280846 (success) was before the merge. Root `index.html` now reflects Obsidian as Current.
- **PR #114 (issue #112) - MERGED** (recovery infra shipped). **#112 CLOSED.**
- **PR #102 - CLOSED.** Issue #42 Brainstorm Board now unblocked.
- Issue #110 CLOSED (via #111 merge).

## IN FLIGHT
1. **PR #115 (issue #62, Fix README + website) - MERGED** (`main`=`1f3bd2b`). Obsidian -> Current in README + index.html; Meridian graduates to top of Previous; Kestrel, Halcyon, Glyphforge, Beambus follow; GitHub corner link retained. Pure docs/landing update (NOT a new project); consumed 0 of 2/day budget. #62 already CLOSED.
2. **PR #104 (Prism, issue #103) - OPEN, researcher spec phase, NOT ready to merge.** Head = research spec (11,637 additions). Handoff = next step `architect`. No in-flight review/fix run; earlier broken M0 "fix loop" head (`48bc52a`) superseded. Mae merges only after Architect -> Builder -> Reviewer approve -> Tester passes Kodak vs JXL ~3.1 bpp.

## PENDING (in order)
1. **pages.yml verification:** confirm run 32504672348 deploys the updated site (Obsidian Current). 
2. **#42 Board resume:** #102 is CLOSED, Brainstorm Board unblocked; pick from parked candidates after Prism clears.
3. **PR #104 (Prism) -> architect -> build -> review -> test -> merge -> close #103.** Tester runs Kodak vs JXL 3.1 bpp. After clear: Mae merges (new-project budget 0/2, room available).
4. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.

## ISSUES
- **#62 (Fix README and website)** - CLOSED (since 08-15 by #63; #115 only synced the files, no-op close).
- **#103 (Prism)** - OPEN; active priority project (research spec in #104).
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#110 (paid model crash)** - CLOSED (resolved by merged #111).
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; now unblocked (was blocked on #102, now closed).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#102** - CLOSED.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `1f3bd2b`. Today's new-project merges: 0/2 (PR #115 was docs, #109/#111/#114 were infra).
- PR #115: Reviewer approved (16:43:03Z), Tester approved (16:44:14Z), MERGED (16:45Z). Done.
- PR #104: no in-flight review/fix run; researcher spec phase.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed). Standing worker pin `nemotron-3-ultra-free` available as fallback.
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- `maintainer.yml` trigger dispatch FIXED on main (`/oc recover` can post).

## NEXT STEPS
1. PR #115: MERGED -> verify pages.yml run 32504672348 deploys (Obsidian Current). #62 already closed.
2. PR #104 (Prism): route `architect` once the researcher spec is approved; then Builder -> Reviewer (M0 gate) -> Tester (Kodak vs JXL) -> Mae merge -> close #103.
3. #42: resume Brainstorm Board picks after Prism clears.
4. `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.

## OPEN QUESTIONS
- PR #115: site deploy via re-triggered pages.yml (32504672348) - will it succeed and serve Obsidian as Current? (#62 already closed.)
- PR #104: will Architect -> Builder clear M0, Reviewer approve, Tester pass Kodak vs JXL 3.1 bpp, Mae merge -> close #103?
- #42: now unblocked by #102 closing; resume candidates after Prism.
- `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer
