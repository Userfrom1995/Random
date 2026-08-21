# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32483124387, event `created` on issue #109, 12:41Z). **PR #109 MERGED** at `9aeea30` (12:43Z). Build agent pin `opencode.yml:358` is now `opencode/muse-spark-1.2`. Prism #104 is unblocked and `continue` has been emitted.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak). Now UNBLOCKED by #109.
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run.
- **Owner WILL (12:09:40Z):** "change builder model to `muse-spark-1.2`, open a pr for it." DONE: PR #109 opened, reviewed, tested, and MERGED.
- **Owner CLOSED #106 (12:04:54Z) then #107 (12:19:30Z), BOTH unmerged** - held, not recovered, not recreated.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `9aeea30`** (post #109 merge). BUILD pin now `opencode/muse-spark-1.2` at `opencode.yml:358`. Fix(880), lab(696), reviewer(50), researcher(151) pins remain `opencode/hy3-free` - unchanged and acceptable; only the Builder needed the switch for Prism.
- **MODEL SWITCH PR #109: MERGED** (head `4cc83df`, merge commit `9aeea30`). Single change: build `model:` 358 hy3-free -> `opencode/muse-spark-1.2`. Verified merge-base with old main `15801d8` (no orphan risk). ISSUE #108 CLOSED.
- **STRAY DUPLICATE ISSUE #109: CLOSED** as duplicate of #108.
- **pages.yml:** re-triggered manually (run `32483304605`) after merge to confirm clean redeploy - benign, site content unchanged.

## IN FLIGHT
1. **PR (build) - Prism (issue #103).** Re-opened path: `continue` emitted this run on PR #104 (head `0e8c2c5`, docs-only research/architecture spec). The Builder now runs on `muse-spark-1.2` and must implement `prism/` (C++) per `prism/docs/architecture.md`, gated on M0 (bit-exact round-trip + corruption-rejection fuzz gate) before any optimization. Benchmark Kodak; target under JXL ~3.1 bpp. Then review -> test -> merge.
2. **PR #106 / #107 - `[Infra] Lab update for #104`.** CLOSED unmerged (branch preserved). Redundant `lab:` job. HELD; not recreated.
3. **PR #102 - `[Infra] Lab update for #42`.** CLOSED, branch preserved, head `f58834b4` NOT in main. Recover blocked ONLY by genuine `git push` `workflows`-scope on `OPENCODE_PAT`. Escalated; owner action pending.

## PENDING (in order)
1. **Prism build (NOW UNBLOCKED):** `continue` #104 already emitted. Confirm Builder pushes C++ and reaches M0 fuzz gate; then review -> test -> merge.
2. **#102 wall:** genuine `git push` `workflows`-scope on `OPENCODE_PAT`; owner grants scope or merges manually; then close #42.
3. **Board (#42) resume:** after Prism, pick from parked candidates.
4. **`recover.py` hardening:** fall back to `gh pr merge --merge` when `--rebase` fails on unrelated history.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build unblocked by #109).
- **#108 (model switch)** - CLOSED by #109 merge.
- **#109 (stray duplicate)** - CLOSED as duplicate of #108.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `9aeea30`. Today's new-project merges: 0/2 (Prism not yet built; #109 was infra, not counted).
- PR #109: MERGED. Reviewer `/oc approve` (12:40:43) + Tester `/oc approve-test` (12:41:54); no newer `/oc fix` findings.
- PR #104: `continue` emitted; Builder on `muse-spark-1.2` now able to implement.
- PR #107/#106: CLOSED unmerged by owner; held.
- PR #102: recover blocked by genuine `git push` `workflows`-scope; escalated.
- `lab.yml` Lab Engineer pin: `hy3-free` (separate, low-priority; not blocking Prism now that the Builder switch is in main).

## NEXT STEPS
1. Monitor Prism `continue` on #104: confirm Builder pushes `prism/` C++ and reaches M0 fuzz gate; then review -> test (Kodak vs JXL ~3.1 bpp) -> merge.
2. Hold #106/#107 (redundant lab job); do not recreate.
3. Keep #102 escalated; close #42 once it lands.

## OPEN QUESTIONS
- After `continue`, can the Builder on `muse-spark-1.2` execute + push and hit M0 fuzz gate, then beat JXL 3.1 bpp on Kodak?
- #102: owner to grant `workflows` scope to `OPENCODE_PAT` or merge manually; its `ideate.yml` change still needed for #42.
- Superseded orphan PRs (#84/#83/#69/#60): work already in main via merged counterparts; intentionally not recovered.
- `lab.yml` Lab Engineer pin still `hy3-free`: future `/oc lab` runs risk no-op; consider a follow-up Lab Engineer PR to bump it (lower priority, not blocking Prism).

- Mae, the Maintainer
