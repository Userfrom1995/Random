# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32484047226, event `/oc maintainer` on PR #111, 12:53Z). PR #111 is the free-model infra fix that unblocks Prism #104. Reviewer approved; Tester running; merge deferred to downstream maintainer run queued on approve-test.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak).
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run.
- **Owner WILL (12:09:40Z):** "change builder model to `muse-spark-1.2`, open a pr for it." Delivered as PR #109 (MERGED `9aeea30`) but `muse-spark-1.2` is PAID -> billing crash. Correcting to free tier `muse-spark-1.2-contributor-free` via PR #111 (pending merge).

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `9aeea30`** (post #109 merge). BUILD pin STILL `opencode/muse-spark-1.2` (PAID) at `opencode.yml:358` -> broken until PR #111 merges.
- **PR #111** head `cc864ab` (branch `opencode/lab-110-builder-model-free`): changes line 358 `opencode/muse-spark-1.2` -> `opencode/muse-spark-1.2-contributor-free`. Body `Closes #110`. REVIEWER APPROVED 12:54:05Z (run 32484036004). Tester `in_progress` (run 32484121060) as of this run; no `/oc approve-test` yet.
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine; only the workflow `model:` input is/was paid.
- After #111 merges: build pin free; `continue` #104 to build `prism/` (C++) per `prism/docs/architecture.md`, gated on M0 (bit-exact round-trip + corruption-rejection fuzz gate).

## IN FLIGHT
1. **PR #111 (Lab Engineer free-model fix, issue #110).** Reviewer approved; Tester running. DOWNSTREAM MAINTAINER RUN 32484120784 queued to merge on approve-test. Then issue #110 closes.
2. **PR #104 (build) - Prism (issue #103).** head `0e8c2c5`, docs-only (research/architecture spec). Blocked on paid build model until #111 merges. After #111 merges, emit `continue`; Builder implements `prism/` (C++) per `prism/docs/architecture.md`, gated on M0 fuzz gate before optimization. Benchmark Kodak; target under JXL ~3.1 bpp. Then review -> test -> merge.

## PENDING (in order)
1. **#111 merge:** downstream maintainer run merges on approve-test; close issue #110.
2. **Prism build:** `continue` #104 (after #111); confirm Builder pushes `prism/` C++ and reaches M0 fuzz gate; then review -> test (Kodak vs JXL ~3.1 bpp) -> merge.
3. **#102 wall (CLOSED earlier):** genuine `git push` `workflows`-scope on `OPENCODE_PAT`; owner to grant scope or merge manually; then close #42.
4. **Board (#42) resume:** after Prism, pick from parked candidates.
5. **`recover.py` hardening / `lab.yml` Lab Engineer pin bump (`hy3-free`):** lower priority, not blocking Prism.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build blocked until #111 merges free model).
- **#110 (paid model crash)** - OPEN; resolved by PR #111, closes on merge.
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `9aeea30`. Today's new-project merges: 0/2 (Prism not yet built; #109/#111 are infra).
- PR #111: REVIEWER APPROVED; Tester `in_progress`; merge deferred to run 32484120784 on approve-test.
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2` = PAID -> fixing to `opencode/muse-spark-1.2-contributor-free` via #111.
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (nondeterministic no-op risk; lower priority).

## NEXT STEPS
1. Tester approves-test #111 -> downstream maintainer run 32484120784 merges #111 -> close #110.
2. After merge: `continue` #104 so Builder (free `muse-spark-1.2-contributor-free`) implements `prism/` through M0 fuzz gate.
3. Review -> test (Kodak vs JXL ~3.1 bpp) -> merge Prism.

## OPEN QUESTIONS
- Will `muse-spark-1.2-contributor-free` actually execute + push C++ (agentic), or need `nemotron-3-ultra-free` (standing worker pin)?
- After free model lands + `continue`, can the Builder hit M0 fuzz gate and beat JXL 3.1 bpp on Kodak?
- #102: owner to grant `workflows` scope to `OPENCODE_PAT` or merge manually; its `ideate.yml` change still needed for #42.
- `lab.yml` Lab Engineer pin still `hy3-free`: future `/oc lab` runs risk no-op; follow-up Lab Engineer PR to bump it (lower priority).
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer