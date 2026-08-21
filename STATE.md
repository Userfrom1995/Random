# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32464936210, EVENT `created` on PR #106, owner `/oc maintainer` 08:49:10Z). `main` = `668222b` (owner manual fresh infra push at 08:48:40 UTC, supersedes prior orphan root `60748e88`). PR #106 (Lab Engineer infra fix for #104) is OPEN, fully Reviewer+Tester approved, and is being re-landed this run via the hardened `recover` path (`gh pr merge --rebase`). Only blocker is the durable PAT `workflows`-scope wall.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner, overrides board):** build the **Obsidian-upgrade image codec (Prism, issue #103)** - beat JPEG XL (~3.1 bpp on Kodak). Prism is the active project. No other new ideas until Prism competitive.
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `668222b`** (OWNER manual infra push, fresh orphan root, 08:48:40 UTC). Contains: separate `lab.yml` workflow, all agent prompts (`labengineer.md`, etc.), `maintainer-recover.py` (hardened), and the unchanged `opencode.yml` still on `hy3-free` for build/fix/lab (NO `lab:` job, NO `Route lab decision` step, NO nemotron pin).
- **WORKFLOW-PUSH PERMISSION WALL (CONFIRMED, DURABLE):** `OPENCODE_PAT` lacks the `workflows` scope, so NO bot (Builder/Fixer/Lab Engineer/Maintainer recover/merge) can push any PR that touches `.github/workflows/*`. Blocks:
  - PR #106 (touches `opencode.yml`) - OPEN, fully approved, recover re-attempted this run.
  - PR #102 (touches `ideate.yml`) - CLOSED, orphaned, head `f58834b4` not in main, already escalated.
  - Only the owner granting `workflows` scope to OPENCODE_PAT, or a manual owner merge, can land such PRs.
- **PR #106 fully approved:** Reviewer `/oc approve` (08:40:00Z) + Tester `/oc approve-test` (08:41:59Z). The prior BLOCKING `/oc fix` (missing Route-decision step in the `lab:` job) was already resolved inside #106's commits (Lab Engineer added Route step + strip guard; the push was rejected only by the scope wall). Model id `opencode/nemotron-3-ultra-free` confirmed VALID via `/zen/v1/models`, so #106's fix is sound.
- **OWNER SUPERSESSION:** `668222b` added a separate `lab.yml`, superseding #106's in-`opencode.yml` `lab:` job. The still-valuable, non-redundant content of #106 is the `build`/`fix` model switch to `nemotron-3-ultra-free` (unblocks Prism).
- **BUILD MODEL NO-OP (root cause):** build agent pinned `opencode/hy3-free` answers with a plan and ends without executing tool calls (observed 2x: runs 32461984795 + 32462425172). #106's switch to `nemotron-3-ultra-free` is the fix. Until #106 lands, #104 cannot build.

## IN FLIGHT
1. **PR #106 - `[Infra] Lab update for #104`** (Lab Engineer deliverable). OPEN on `opencode/lab-105-fix-build-loop` (head `0505577`), MERGEABLE, fully approved. **Recover re-attempted THIS run** (decision `recover` #106) via hardened `maintainer-recover.py` (`gh pr merge --rebase`). If `OPENCODE_PAT` has `workflows` scope it lands; else the script tags `@Userfrom1995` with the exact grant-scope/manual-merge fix and #106 stays open. Closes the infra portion of #104.
2. **PR #104 - Prism research/architecture spec + BUILD (issue #103).** OPEN on `opencode/issue103-20260821075928` (head `0e8c2c5`, docs only - no C++). Researcher + Architect delivered `prism/docs/*.md`. Build no-op'd twice on `hy3-free`. Depends on #106 landing before any `continue` will produce code.
3. **PR #102 - `[Infra] Lab update for #42`.** CLOSED, branch preserved, head `f58834b4` NOT in main. Recover blocked by PAT `workflows`-scope wall. Already escalated; no re-spam.

## PENDING (in order)
1. **#106 landing:** this run's `recover` either lands it (if scope present) or tags owner. If landed: Prism unblocks.
2. **Prism build (after #106 lands):** emit `continue` on #104 so the Builder (now `nemotron-3-ultra-free`) implements `prism/` per `prism/docs/architecture.md`, gated on M0 (bit-exact round-trip + corruption rejection fuzz gate) before optimization. Benchmark on Kodak; target under JXL ~3.1 bpp. Then review -> test -> merge.
3. **#102 wall:** owner grants `workflows` scope to OPENCODE_PAT, or manually merges #102 (its `ideate.yml` change still needed for issue #42). Then close #42.
4. **Board (#42) resume:** after Prism, pick from parked candidates - no new projects until Prism competitive.
5. **Superseded orphans (#84/#83/#69/#60):** intentionally NOT recovered.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build blocked on #106).
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#68 (Obsidian)** - CLOSED by owner.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `668222b`. Today's new-project merges: 0/2 (clear for Prism #104 once #106 lands + build clears review/test).
- PR #106: Reviewer + Tester approved; recover re-attempted this run; only `workflows`-scope wall remains.
- PR #104: build no-op'd twice on `hy3-free`; unblocked only by #106's model switch.
- PR #102: recover blocked (PAT scope), escalated.
- pages.yml: triggers only on PR/workflow_dispatch; Prism build touches no workflow files, so no pages issue on land.

## NEXT STEPS
1. This run: `recover` #106. Outcome decided by the workflows-scope wall: land (if scope) or owner tag (if not).
2. After #106 lands: emit `continue` on #104; confirm Builder pushes C++ and reaches M0 fuzz gate; then route review -> test -> merge.
3. #102: owner resolves PAT-scope wall (grant `workflows` scope, or manually merge #102); then close #42.
4. If #106 cannot land by bot, keep it open; the recover script's owner tag carries the exact fix.

## OPEN QUESTIONS
- #106: will the hardened recover land it this run (i.e., does `OPENCODE_PAT` now have `workflows` scope)? If not, owner must grant scope or `gh pr merge 106 --rebase` manually.
- #104: after #106 lands, can the Builder on `nemotron-3-ultra-free` execute + push and hit M0 fuzz gate? Then under JXL 3.1 bpp on Kodak?
- #102: owner to grant `workflows` scope or land manually; its `ideate.yml` change still needed for #42.
- Superseded orphan PRs (#84/#83/#69/#60): work already in main via merged counterparts; intentionally not recovered.
- `main` `668222b`: intentional owner re-sync (fresh orphan root); allowed because it is an owner action, not a bot rewrite.
- Does the owner's separate `lab.yml` (superseding #106's `lab:` job) also carry the model pin intended for the Lab Engineer, or does the Lab Engineer still use `opencode.yml`'s `hy3-free` pin? If the latter, a future `lab` run would also no-op until #106 lands.

- Mae, the Maintainer
