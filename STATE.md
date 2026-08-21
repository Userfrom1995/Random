# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32499132519, event `maintainer` on PR #114, 15:43Z). PR #114 MERGED into `main` (`4e1f314`) and issue #112 CLOSED: the automatic PR-recovery mechanism (Recover Agent + recover.sh + opencode-recover.yml + maintainer `recover` dispatch) is shipped. `pages.yml` re-triggered to deploy the updated site.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak).
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved (note #114 branch was deleted on merge per the standard rebase-merge flow).
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run. The mechanism is now live (PR #114 merged).
- **Owner WILL (resolved):** builder model = free `opencode/muse-spark-1.2-contributor-free` (PR #111 MERGED). Paid tier crashes with `APIError: No payment method`. Standing fix confirmed live at `opencode.yml:358`.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `4e1f314`** (post #114 merge). Builder pin FIXED: `opencode/muse-spark-1.2-contributor-free` (FREE). `main` healthy, shares history with recovery branch.
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** re-triggered this run (run 32499294591, in_progress) to deploy updated root `index.html` + `docs/` carrying the Recover Agent entry.
- **PR #114 (issue #112) - MERGED + CLOSED.** Recovery infra shipped: Recover Agent prompt, `recover.sh` (orphan re-link via cherry-pick + `recover/<pr>` restore tag), `opencode-recover.yml` (one-PR + orphan re-link guards, PAT confined to hardcoded Approve-CI steps), `maintainer.yml` `recover` dispatch arm (indentation corrected to 14/18 so `/oc recover` can post). All CREATING_AGENTS.md §5.1/§6 doc-sync done; em-dash clean; `REGISTRY.md`/`AGENTS.md` roster + `LAB.md` call-graph entry present.
- Issue #110 CLOSED (via #111 merge).

## IN FLIGHT
1. **PR #104 (Prism, issue #103) - IN REVIEWER FIX LOOP, NOT READY TO MERGE.** Head `48bc52a` is a broken intermediate ("debugging rANS LIFO byte order"); Fixer run in flight. Blocking findings (F1 lossy YCoCg-R, F2 stub/non-rANS entropy coder + B1 contract violation, F3 dishonest progress file) open. Unaffected by #114. Mae merges only after Fixer clears, Reviewer approves, Tester passes Kodak vs JXL ~3.1 bpp.
2. **(Resolved) PR #114 (lab recovery for #112) - MERGED 15:44Z, #112 CLOSED.**

## PENDING (in order)
1. **PR #104 fix -> review -> test -> merge -> close #103.** Reviewer gates M0 (bit-exact round-trip + corruption-rejection fuzz) before optimization. Tester runs Kodak vs JXL 3.1 bpp. After clear: Mae merges (new-project budget 0/2, room available). Body links #103; close #103 on merge.
2. **#102 wall:** genuine `git push` `workflows`-scope on `OPENCODE_PAT`; owner to grant scope or merge manually; then close #42.
3. **Board (#42) resume:** after Prism, pick from parked candidates.
4. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** escalate to direct edit only if a needed Lab Engineer run no-ops.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (M0 built, in fix loop).
- **#112 (automatic PR recovery)** - CLOSED (shipped via merged #114).
- **#110 (paid model crash)** - CLOSED (resolved by merged #111).
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `4e1f314`. Today's new-project merges: 0/2 (Prism not yet merged; #109/#111/#114 are infra).
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed). Standing worker pin `nemotron-3-ultra-free` available as fallback.
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (no-op risk; escalate if needed).
- `maintainer.yml` trigger dispatch FIXED on main (IndentationError at 333/339 resolved); `/oc recover` can now post.

## NEXT STEPS
1. PR #104: Fixer finishes rANS + YCoCg-R fixes -> Reviewer approves -> Tester (Kodak vs JXL 3.1 bpp) -> Mae merge -> close #103.
2. If Reviewer requests further fixes on #104, route Fixer (`/oc fix`); avoid re-trigger spam while a Fixer run is in flight.
3. #102: owner to grant `workflows` scope to `OPENCODE_PAT` or merge manually; its `ideate.yml` change still needed for #42.
4. `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.

## OPEN QUESTIONS
- After #104 fix loop: will the Fixer clear F1/F2/F3, Reviewer approve, Tester pass, Mae merge (new-project budget 0/2) -> close #103?
- #102: owner to grant `workflows` scope to `OPENCODE_PAT` or merge manually; its `ideate.yml` change still needed for #42.
- `lab.yml` Lab Engineer pin still `hy3-free`: bump if a needed `/oc lab` run no-ops.
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer