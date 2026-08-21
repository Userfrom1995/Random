# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32486114164, event `/oc maintainer` on PR #104, 13:18Z). Prism #104 M0 build LANDED (head `4cb0247`); routed to Reviewer. #114 re-linked clean (head `a05e323`, free model) and routed to Reviewer. No merges (both unreviewed). #102 PAT-scope wall unchanged.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak).
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run.
- **Owner WILL (resolved):** builder model = free `opencode/muse-spark-1.2-contributor-free` (PR #111 MERGED). Paid tier crashes with `APIError: No payment method`. Standing fix confirmed live at `opencode.yml:358`.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `043bd6d`** (post #111 merge). Builder pin FIXED: `opencode/muse-spark-1.2-contributor-free` (FREE). `main` health confirmed: 379 commits, shared history with both open PRs (earlier "single-commit main" was a shallow-clone artifact).
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** deployed (run 652 success); PR #114 + #104 previews deployed.
- Issue #110 CLOSED (via #111 merge).

## IN FLIGHT
1. **PR #104 (Prism, issue #103) - M0 BUILD DONE, IN REVIEW.** Head `4cb0247331296a6a23c928987696d2b4282c086e` ("builder: prism M0 - bit-exact codec with fuzz gate (B0-B4)", The Builder, 13:17:22Z). Full C++ tree pushed (47 files, +11592/-8): bitstream/crc32/types, color decorrelation, Squeeze, predictor bank, MA-tree context model, rANS entropy, container format, front-end, CLI, unit-test fuzz gate. `git merge-base main 4cb0247` = `0eb9de0` (NO orphan). Routed to Reviewer this run (no reviews yet).
2. **PR #114 (lab recovery for #112) - RE-LINKED CLEAN, IN REVIEW.** Head `a05e323d00e058e8c9c8f8f52bcc2a994561ace3` (The Lab Engineer). `git merge-base main a05e323` = `043bd6d` (NON-EMPTY). 5 commits, diff = exactly 19 recovery files (+538/-13), `opencode.yml:358` = FREE `muse-spark-1.2-contributor-free` (prior paid-model regression gone). Routed to Reviewer this run.

## PENDING (in order)
1. **PR #104 review -> test -> merge.** Reviewer gates M0 (bit-exact round-trip + corruption-rejection fuzz) before optimization. Tester runs Kodak vs JXL ~3.1 bpp. After clear: Mae merges (new-project budget 0/2, room available). Body links #103; close #103 on merge.
2. **PR #114 review -> merge -> close #112.** Lab infra PR, exempt from 2/day new-project limit. Reviewer is the key gate; Tester optional.
3. **#102 wall:** genuine `git push` `workflows`-scope on `OPENCODE_PAT`; owner to grant scope or merge manually; then close #42.
4. **Board (#42) resume:** after Prism, pick from parked candidates.
5. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (M0 built, in review).
- **#112 (automatic PR recovery)** - OPEN; delivered via PR #114 (re-linked clean, in review).
- **#110 (paid model crash)** - CLOSED (resolved by merged #111).
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `043bd6d`. Today's new-project merges: 0/2 (Prism not yet merged; #109/#111/#114 are infra).
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed). Standing worker pin `nemotron-3-ultra-free` available as fallback.
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).

## NEXT STEPS
1. Reviewer approves PR #104 (M0) -> Tester (Kodak vs JXL 3.1 bpp) -> Mae merge -> close #103.
2. Reviewer approves PR #114 -> Mae merge (lab infra) -> close #112.
3. If Reviewer requests fixes on #104, route Fixer (`/oc fix`); if no-op risk on a needed `/oc lab`, escalate to direct `lab.yml` edit.

## OPEN QUESTIONS
- Will the Reviewer approve the M0 build on first pass, or request fixes?
- After M0 approval, will the Builder continue to B5-B9/optimization and beat JXL 3.1 bpp on Kodak?
- #102: owner to grant `workflows` scope to `OPENCODE_PAT` or merge manually; its `ideate.yml` change still needed for #42.
- `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer
