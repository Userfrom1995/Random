# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32503334350, triggered by Userfrom1995 comment on issue #62 "read me and website are outdated", 16:31Z). Routing the Builder (`build`, issue #62) to fix the Meridian/Obsidian promotion gap so README + index.html agree: Obsidian = Current, Meridian = top of Previous.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak).
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run. Mechanism shipped (PR #114 merged).
- **Owner WILL (resolved):** builder model = free `opencode/muse-spark-1.2-contributor-free` (PR #111 MERGED). Paid tier crashes with `APIError: No payment method`. Standing fix confirmed live at `opencode.yml:358`.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `98d891d`** (post #114 merge; latest lab-hardening commit). Healthy, shares history with all build branches.
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** last deploy run 32503025844 (success) after `98d891d`.
- **PR #114 (issue #112) - MERGED** (recovery infra shipped). **#112 CLOSED.**
- **PR #102 - CLOSED** (the `OPENCODE_PAT` `workflows`-scope wall; owner action needed or manual merge). Issue #42 Brainstorm Board now unblocked.
- Issue #110 CLOSED (via #111 merge).

## IN FLIGHT
1. **PR #104 (Prism, issue #103) - OPEN, researcher spec phase, NOT ready to merge.** Current head is the research spec (11,637 additions: `prism/docs/research.md`, `algorithmic-spec.md`, `benchmark-methodology.md`, idea + progress entries). Handoff = next `architect`. No in-flight review/fix run; the earlier broken M0 "fix loop" head (`48bc52a`) was superseded by this research-spec rewrite. Mae merges only after Architect -> Builder -> Reviewer approve -> Tester passes Kodak vs JXL ~3.1 bpp.
2. **Issue #62 (Fix README and website) - re-activated by owner comment at 16:31:10Z.** The Meridian/Obsidian promotion gap is being routed to the Builder (`build`) this run. New branch `opencode/62-*` + PR with `Closes #62` to follow, then normal review/test loop.

## PENDING (in order)
1. **PR #62 fix -> review -> test -> merge -> close #62.** Builder makes Obsidian Current in README + index.html, graduates Meridian to top of Previous (newest-first), and syncs project ordering across both files.
2. **#42 Board resume:** #102 is now CLOSED, so the Brainstorm Board is unblocked; pick from parked candidates after Prism clears.
3. **PR #104 (Prism) -> architect -> build -> review -> test -> merge -> close #103.** Reviewer gates M0 (bit-exact round-trip + corruption-rejection fuzz) before optimization. Tester runs Kodak vs JXL 3.1 bpp. After clear: Mae merges (new-project budget 0/2, room available).
4. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.

## ISSUES
- **#62 (Fix README and website)** - OPEN (re-activated by owner 16:31Z); Builder routed this run.
- **#103 (Prism)** - OPEN; active priority project (research spec in #104).
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#110 (paid model crash)** - CLOSED (resolved by merged #111).
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; now unblocked (was blocked on #102, now closed).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#102** - CLOSED (PAT-scope wall; owner action needed or manual merge).

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `98d891d`. Today's new-project merges: 0/2 (Prism not yet merged; #109/#111/#114 are infra).
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed). Standing worker pin `nemotron-3-ultra-free` available as fallback.
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- `maintainer.yml` trigger dispatch FIXED on main (`/oc recover` can post).

## NEXT STEPS
1. Issue #62: Builder promotes Obsidian to Current + graduates Meridian to Previous in README + index.html (consistent ordering) -> PR (`Closes #62`) -> Reviewer -> Tester -> Mae merge -> close #62.
2. PR #104 (Prism): route `architect` once the researcher spec is approved; then Builder -> Reviewer (M0 gate) -> Tester (Kodak vs JXL) -> Mae merge -> close #103.
3. #42: resume Brainstorm Board picks after Prism clears.
4. `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.

## OPEN QUESTIONS
- Issue #62: will the Builder's PR make README + index.html agree (Obsidian Current, Meridian top Previous, same ordering), pass Reviewer + Tester, Mae merge -> close #62?
- PR #104: will Architect -> Builder clear M0, Reviewer approve, Tester pass Kodak vs JXL 3.1 bpp, Mae merge -> close #103?
- #42: now unblocked by #102 closing; resume candidates after Prism.
- `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer
