# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32487540817, event `created` on PR #114, 13:34Z). PR #114's blocker is a `workflows: write` permission wall on `.github/workflows/maintainer.yml` (IndentationError at lines 333/339). Maintainer will NOT self-edit/self-merge; escalated to owner. No merge, no bot trigger this run. PR #104 still in review.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak).
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run.
- **Owner WILL (resolved):** builder model = free `opencode/muse-spark-1.2-contributor-free` (PR #111 MERGED). Paid tier crashes with `APIError: No payment method`. Standing fix confirmed live at `opencode.yml:358`.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `043bd6d`** (post #111 merge). Builder pin FIXED: `opencode/muse-spark-1.2-contributor-free` (FREE). `main` healthy.
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** deployed; PR #114 + #104 previews deployed.
- **PR #114 blocker (ROOT CAUSE this run):** Python `IndentationError` in `.github/workflows/maintainer.yml` lines 333 + 339 (`lab`/`recover` `elif` at 15 spaces vs 14; bodies 19 vs 18). The bot `GITHUB_TOKEN` lacks `workflows: write`, so no bot (Fixer/Lab Engineer/Maintainer dedicated step) can push the fix to the PR branch. Maintainer's dedicated PAT step pushes to `HEAD:main` only and the envelope safety net restricts Maintainer workflow edits to model changes, so a direct edit would self-merge #114 into main without Reviewer approval (hard-rule violation) and is deliberately avoided. Fix is a pure 1-level indent correction (14-space `elif`, 18-space bodies); all other findings already clear on head `a05e323`.
- Issue #110 CLOSED (via #111 merge).

## IN FLIGHT
1. **PR #104 (Prism, issue #103) - M0 BUILD DONE, IN REVIEW.** Head `4cb0247331296a6a23c928987696d2b4282c086e`. 47 files, +11592/-8, merge-base `0eb9de0` (NO orphan). Routed to Reviewer (run 32486114164); reviews=[] still. Unaffected by #114 blocker.
2. **PR #114 (lab recovery for #112) - BLOCKED on `workflows: write` permission wall.** Branch `opencode/issue112-20260821125724` head `a05e323` (re-linked clean, free model, doc synced, Reviewer's doc-sync findings cleared). Only the `maintainer.yml` IndentationError remains, and only the owner can push it. Awaiting owner: (a) push the indent fix + merge #114, or (b) grant `workflows: write` to the maintainer workflow so a future Maintainer run applies it. NOT merged, NOT re-reviewed until the fix actually lands.

## PENDING (in order)
1. **PR #114 permission-wall resolution (owner action) -> re-review -> test -> merge -> close #112.** Lab infra PR, exempt from 2/day new-project limit.
2. **PR #104 review -> test -> merge.** Reviewer gates M0 (bit-exact round-trip + corruption-rejection fuzz) before optimization. Tester runs Kodak vs JXL ~3.1 bpp. After clear: Mae merges (new-project budget 0/2, room available). Body links #103; close #103 on merge.
3. **#102 wall:** genuine `git push` `workflows`-scope on `OPENCODE_PAT`; owner to grant scope or merge manually; then close #42.
4. **Board (#42) resume:** after Prism, pick from parked candidates.
5. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (M0 built, in review).
- **#112 (automatic PR recovery)** - OPEN; delivered via PR #114 (blocked on permission wall, not on content).
- **#110 (paid model crash)** - CLOSED (resolved by merged #111).
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `043bd6d`. Today's new-project merges: 0/2 (Prism not yet merged; #109/#111/#114 are infra).
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed). Standing worker pin `nemotron-3-ultra-free` available as fallback.
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- `maintainer.yml` trigger dispatch STILL broken on the PR branch (IndentationError at 333/339) - `/oc recover` cannot post until the owner lands the fix.

## NEXT STEPS
1. Owner pushes the `maintainer.yml` indent fix to `opencode/issue112-20260821125724` (or grants `workflows: write`) -> re-review clears -> Tester -> Mae merge (lab infra) -> close #112.
2. Reviewer approves PR #104 (M0) -> Tester (Kodak vs JXL 3.1 bpp) -> Mae merge -> close #103.
3. If Reviewer requests further fixes on either PR, route Fixer (`/oc fix`); note #114 workflow-file fixes need owner `workflows: write` (bot blocked).

## OPEN QUESTIONS
- Will the owner grant `workflows: write` to the maintainer GITHUB_TOKEN, or manually push+merge the indent fix on #114? (Only path to unblock #112.)
- After M0 approval, will the Builder continue to B5-B9/optimization and beat JXL 3.1 bpp on Kodak?
- #102: owner to grant `workflows` scope to `OPENCODE_PAT` or merge manually; its `ideate.yml` change still needed for #42.
- `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer