# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32481346223, EVENT `closed` on #107, 12:19Z). `main` = `15801d8` (owner infra push; STILL pins `opencode/hy3-free` at build 358 / fix 880 / lab / reviewer / researcher - 5 pins, 0 nemotron). PR #107 **CLOSED unmerged** by owner (12:19:30Z) - a recreation of #106 from the same branch `opencode/lab-105-fix-build-loop`, head `0505577`. Prism #104 remains blocked on the absent model switch.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak). Prism is the active project.
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run.
- **Owner OVERROLE (11:56:57Z):** "you already has access to pat to merge this how to merged #99 then you are hallucinating" - confirmed the PAT merges via API; prior "PAT `workflows`-scope wall" framing was imprecise. The genuine restriction is only `git push` of workflow files (affects #102's closed-PR recover `git push` path, not `gh pr merge`). Recorded as dissent; complied.
- **Owner CLOSED #106 (12:04:54Z) then #107 (12:19:30Z), BOTH unmerged** - read as an informed, repeated decision to avoid reintroducing the redundant `lab:` job that duplicates `lab.yml`. Holding BOTH closed; NOT force-recovering (would override sovereign owner authority + reintroduce redundancy).

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `15801d8`** (OWNER manual infra push; fresh orphan root lineage from `668222b`). Contains: separate `lab.yml` workflow (sole `/oc lab` handler), all agent prompts, hardened `maintainer-recover.py` (OPEN-PR merge uses `gh pr merge --rebase`).
- **MERGE MECHANISM (clarified in run 32479670237, unchanged):** `gh pr merge` via the **API** does NOT require `workflows` scope and handles unrelated histories. Only `git push` of workflow files needs the scope (affects `recover.py`'s closed-PR `git push` path for #102).
- **PR #107 CLOSED unmerged (12:19:30Z, owner).** Same head `0505577` / branch `opencode/lab-105-fix-build-loop` as #106. Its opencode.yml diff onto main = (a) `lab:` job added ~+179 lines [REDUNDANT with lab.yml - verified lab.yml exists on main and handles /oc lab], (b) build model 358 hy3-free->nemotron, (c) fix model 884 hy3-free->nemotron, (d) `/oc build this (auto-retry` guard. Only (b)+(c) unblock Prism. **Holding: not recovered, not recreated.** A clean API merge is possible (`gh pr merge --merge`, 0 conflicts) but WOULD reintroduce the redundant lab job, so it is withheld per owner intent.
- **MODEL SWITCH NOT ON MAIN:** `opencode.yml` still pins `hy3-free` at build(358), fix(884), lab, reviewer(50), researcher(151). So BOTH build/fix AND a future `/oc lab` still no-op until switched.
- **BUILD MODEL NO-OP (root cause):** build agent pinned `opencode/hy3-free` ends without executing tool calls (observed 2x). Only the switch to `nemotron-3-ultra-free` in `main` fixes it. Until that lands, #104 cannot build.

## IN FLIGHT
1. **PR #107 - `[Infra] Lab update for #104`.** CLOSED unmerged (head `0505577`, branch preserved). Carrier for the #104-unblocking model switch, but bundles a `lab:` job duplicating `lab.yml`. Owner closed it TWICE (#106 then #107). HOLDING - no recover, no recreate. Auto-retry loop from this branch is to be broken; if it recreates again, hold again.
2. **PR #104 - Prism research/architecture spec + BUILD (issue #103).** OPEN, docs-only (head `0e8c2c5`), no C++. Builder no-op'd twice on `hy3-free`. BLOCKED on the model switch reaching main.
3. **PR #102 - `[Infra] Lab update for #42`.** CLOSED, branch preserved, head `f58834b4` NOT in main. Recover blocked ONLY by the genuine `git push` `workflows`-scope restriction on `OPENCODE_PAT` (its `ideate.yml` edit is a workflow file). Owner to grant `workflows` scope or merge manually. Already escalated; no re-spam.

## PENDING (in order)
1. **Unblock Prism:** land the build/fix model switch (`opencode.yml` 358 + 884 -> `nemotron-3-ultra-free`) on main via owner's chosen path: (a) manual 2-line edit [fastest], or (b) grant `workflows` scope -> Lab Engineer lands a slimmed switch-only PR (no redundant lab job). Also switch `lab.yml`'s Lab Engineer pin so `/oc lab` executes.
2. **Prism build (after switch lands):** emit `continue` on #104 so the Builder (now `nemotron-3-ultra-free`) implements `prism/` per `prism/docs/architecture.md`, gated on M0 (bit-exact round-trip + corruption rejection fuzz gate) before optimization. Benchmark Kodak; target under JXL ~3.1 bpp. Then review -> test -> merge.
3. **#102 wall:** genuine `git push` `workflows`-scope on `OPENCODE_PAT` (NOT the merge API). Owner grants scope, or manually merges #102; then close #42.
4. **Board (#42) resume:** after Prism, pick from parked candidates - no new projects until Prism competitive.
5. **Follow-up tiny PR (post-unblock):** if any switch PR is merged as-is with the redundant lab job, drop the `lab:` job from `opencode.yml` so `/oc lab` does not double-trigger `lab.yml`.
6. **`recover.py` hardening:** fall back to `gh pr merge --merge` when `--rebase` fails on unrelated history, so the bot self-merges orphaned open PRs without owner intervention.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build blocked on model switch).
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#68 (Obsidian)** - CLOSED by owner.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `15801d8`. Today's new-project merges: 0/2 (clear for Prism #104 once the switch lands + build clears review/test).
- PR #107: CLOSED unmerged by owner (recreation of #106); held (no recover, no recreate).
- PR #106: CLOSED unmerged by owner; held.
- PR #104: build no-op'd twice on `hy3-free`; unblocked only by the model switch in main.
- PR #102: recover blocked by genuine `git push` `workflows`-scope (workflow file); escalated.
- pages.yml: triggers only on PR/workflow_dispatch; Prism build touches no workflow files, so no pages issue on land.

## NEXT STEPS
1. Owner picks the unblock path for the model switch: (a) manual 2-line edit on main [fastest], or (b) grant `workflows` scope -> I dispatch the Lab Engineer to land a slimmed switch-only PR (no redundant lab job). Also switch `lab.yml` Lab Engineer pin.
2. After switch lands in main: emit `continue` on #104; confirm Builder pushes C++ and reaches M0 fuzz gate; then route review -> test -> merge.
3. Break the #106/#107 auto-retry loop: do not recreate the bundled PR; if the bot recreates it from `opencode/lab-105-fix-build-loop`, hold it again (owner intent).

## OPEN QUESTIONS
- #107/#106: owner closed both unmerged (informed, redundancy-aware). Will the owner do the 2-line manual edit, or grant `workflows` scope for a slimmed switch PR? Prism stays blocked until the switch is in main.
- #104: after the switch lands, can the Builder on `nemotron-3-ultra-free` execute + push and hit M0 fuzz gate? Then under JXL 3.1 bpp on Kodak?
- #102: owner to grant `workflows` scope to `OPENCODE_PAT` (for the `git push` recover path of workflow files) or merge manually; its `ideate.yml` change still needed for #42.
- `lab.yml` Lab Engineer pin is still `hy3-free` - needs the same switch for `/oc lab` to execute; secondary but real.
- Superseded orphan PRs (#84/#83/#69/#60): work already in main via merged counterparts; intentionally not recovered.
- `main` `15801d8`: owner re-sync (fresh orphan root lineage); the unrelated-history state is why rebase-based recover fails (API `--merge` is the workaround, but withheld here due to the redundant lab job).

- Mae, the Maintainer
