# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32473448443, EVENT `created` on #106, owner question "why lab is on halt?" 10:33:53Z). `main` = `668222b`. PR #106 OPEN, fully approved, still gated ONLY by the durable PAT `workflows`-scope wall. Decision this run: do NOT recover (would reintroduce a redundant `lab:` job and still hits the wall); instead `ping` the owner with the clean 2-line manual fix that actually unblocks Prism #104.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak). Prism is the active project.
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `668222b`** (OWNER manual infra push, fresh orphan root). Contains: separate `lab.yml` workflow (handles `/oc lab`), all agent prompts, `maintainer-recover.py` (hardened). `opencode.yml` on main STILL pins `opencode/hy3-free` at build (358), fix (884), lab (700); NO `lab:` job; NO nemotron pin. Confirmed via `git show 668222b:...opencode.yml`.
- **WORKFLOW-PUSH PERMISSION WALL (CONFIRMED, DURABLE):** `OPENCODE_PAT` lacks the `workflows` scope, so NO bot can push any PR that touches `.github/workflows/*`. Blocks:
  - PR #106 (touches `opencode.yml`) - OPEN, fully approved, recover attempted twice (runs 32464378115, 32464936210) and rejected.
  - PR #102 (touches `ideate.yml`) - CLOSED, orphaned, head `f58834b4` not in main.
  - Only the owner granting `workflows` scope to OPENCODE_PAT, or a manual owner merge, can land such PRs.
- **PR #106 fully approved:** Reviewer `/oc approve` + Tester `/oc approve-test`. The Reviewer's prior BLOCKING `/oc fix` (missing Route-decision step in the `lab:` job) was already RESOLVED inside #106's commits. Model id `opencode/nemotron-3-ultra-free` confirmed VALID via `/zen/v1/models`.
- **REDUNDANCY FINDING (this run):** `668222b` added separate `lab.yml` which supersedes #106's in-`opencode.yml` `lab:` job. Landing #106 as-is would make `/oc lab` trigger BOTH workflows (opencode.yml `lab:` job + `lab.yml`) -> duplicate Lab Engineer runs. So a wholesale recover of #106 is NOT advisable. The still-valuable, non-redundant content is the build/fix model switch (lines 358/884 -> nemotron).
- **BUILD MODEL NO-OP (root cause):** build agent pinned `opencode/hy3-free` answers with a plan and ends without executing tool calls (observed 2x: runs 32461984795 + 32462425172). Only the model switch to `nemotron-3-ultra-free` in `main` fixes it. Until that lands, #104 cannot build.

## IN FLIGHT
1. **PR #106 - `[Infra] Lab update for #104`.** OPEN on `opencode/lab-105-fix-build-loop` (head `0505577`), MERGEABLE, fully approved. THIS run did NOT recover (redundant lab: job risk + wall). Instead `ping`ed the owner with the clean 2-line manual fix (switch opencode.yml:358 & :884 to nemotron, close #106 as superseded). Prism unblocks the moment those 2 lines are in main.
2. **PR #104 - Prism research/architecture spec + BUILD (issue #103).** OPEN on `opencode/issue103-20260821075928` (head `0e8c2c5`, docs only - no C++). Researcher + Architect delivered `prism/docs/*.md`. Build no-op'd twice on `hy3-free`. Depends on #106's model switch landing in main before any `continue` will produce code.
3. **PR #102 - `[Infra] Lab update for #42`.** CLOSED, branch preserved, head `f58834b4` NOT in main. Recover blocked by PAT `workflows`-scope wall. Already escalated; no re-spam.

## PENDING (in order)
1. **#106 resolution:** owner applies the 2-line model switch to `opencode.yml` on main and closes #106 (fastest), OR grants `workflows` scope and I slim #106 to just the switch and merge. Either way lands the #104-unblocking change.
2. **Prism build (after switch lands):** emit `continue` on #104 so the Builder (now `nemotron-3-ultra-free`) implements `prism/` per `prism/docs/architecture.md`, gated on M0 (bit-exact round-trip + corruption rejection fuzz gate) before optimization. Benchmark on Kodak; target under JXL ~3.1 bpp. Then review -> test -> merge.
3. **#102 wall:** owner grants `workflows` scope to OPENCODE_PAT, or manually merges #102 (its `ideate.yml` change still needed for issue #42). Then close #42.
4. **Board (#42) resume:** after Prism, pick from parked candidates - no new projects until Prism competitive.
5. **Superseded orphans (#84/#83/#69/#60):** intentionally NOT recovered.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build blocked on #106's switch).
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#68 (Obsidian)** - CLOSED by owner.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `668222b`. Today's new-project merges: 0/2 (clear for Prism #104 once the switch lands + build clears review/test).
- PR #106: Reviewer + Tester approved; recover NOT attempted this run (redundancy + wall); owner pinged with 2-line manual fix.
- PR #104: build no-op'd twice on `hy3-free`; unblocked only by the model switch in main.
- PR #102: recover blocked (PAT scope), escalated.
- pages.yml: triggers only on PR/workflow_dispatch; Prism build touches no workflow files, so no pages issue on land.

## NEXT STEPS
1. Owner applies 2-line switch (opencode.yml:358 & :884 -> nemotron-3-ultra-free) and closes #106, OR grants `workflows` scope so I slim+merge #106. (This run's `ping` carries the exact instructions.)
2. After the switch lands in main: emit `continue` on #104; confirm Builder pushes C++ and reaches M0 fuzz gate; then route review -> test -> merge.
3. #102: owner resolves PAT-scope wall (grant `workflows` scope, or manually merge #102); then close #42.

## OPEN QUESTIONS
- #106: will the owner apply the 2-line manual switch (fastest) or grant `workflows` scope so I slim+merge? Either unblocks Prism.
- #104: after the switch lands, can the Builder on `nemotron-3-ultra-free` execute + push and hit M0 fuzz gate? Then under JXL 3.1 bpp on Kodak?
- #102: owner to grant `workflows` scope or land manually; its `ideate.yml` change still needed for #42.
- Superseded orphan PRs (#84/#83/#69/#60): work already in main via merged counterparts; intentionally not recovered.
- `main` `668222b`: intentional owner re-sync (fresh orphan root); allowed because it is an owner action, not a bot rewrite.
- `lab.yml` (owner-pushed, supersedes #106's `lab:` job) carries the Lab Engineer pin from `opencode.yml` `hy3-free` (line 700) - so a future `/oc lab` run via `lab.yml` would also no-op until the switch lands. This is a secondary reason the 2-line fix helps.

- Mae, the Maintainer
