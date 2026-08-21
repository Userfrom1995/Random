# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32464071918, EVENT `created` on PR #106). `main` = `60748e88` (owner orphan root). PR #106 (Lab Engineer infra fix for #104) is blocked on TWO fronts: a Reviewer blocking `/oc fix` finding (missing Route-decision step in the new `lab:` job) AND the PAT `workflows`-scope wall, which prevents any bot (incl. Maintainer) from pushing `.github/workflows/opencode.yml`. Escalated to owner via ping on #106. #104 Prism build stays blocked until #106 lands.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (2026-08-21, owner, overrides board):** build the **Obsidian-upgrade image codec** (Prism, issue #103) - all major input formats, beat JPEG XL. Prism is the active project. No other new ideas until Prism competitive.
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved on close.
- **Maintainer sovereign-recovery directive:** `60748e88` empowers `recover` of orphaned/closed PRs; main must never become a divergent/orphan ROOT.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `60748e88`** (orphan root from PR #93). Contains obsidian + all prior projects.
- **WORKFLOW-PUSH PERMISSION WALL (CONFIRMED, DURABLE):** `OPENCODE_PAT` lacks the `workflows` scope, so NO bot (Builder/Fixer/Lab Engineer/Maintainer recover/merge) can push any PR that touches `.github/workflows/*`. This blocks:
  - PR #102 (touches `ideate.yml`) - CLOSED, orphaned, head `f58834b4` not in main.
  - PR #106 (touches `opencode.yml`) - OPEN, has a Reviewer blocking `/oc fix` finding, Lab Engineer push REJECTED (`remote rejected ... without workflows permission`).
  - Only the owner granting `workflows` scope to OPENCODE_PAT, or a manual owner merge, can land such PRs.
- **PR #106 REVIEWER FINDING (BLOCKING, 08:35:28Z):** the new `lab:` job writes `/tmp/random-lab-decision.json` but has no hardcoded Route-decision step to forward the Lab Engineer's PR to the Reviewer. Fix = add a "Route lab decision" step (supplied by Reviewer) + optional Co-authored-by strip guard. BUT the fix itself edits `opencode.yml` -> also blocked by the wall.
- **BUILD MODEL NO-OP (root cause, to be fixed by #106):** build agent pinned `opencode/hy3-free` answers with a plan and ends without executing tool calls (observed 2x, runs 32461984795 + 32462425172). #106 switches it to `opencode/nemotron-3-ultra-free` + fixes the auto-retry trigger gap. Until #106 lands, #104 cannot build.

## IN FLIGHT
1. **PR #106 - `[Infra] Lab update for #104`** (Lab Engineer deliverable). OPEN on `opencode/lab-105-fix-build-loop` (head rejected at push). Adds `lab:` job, switches build/fix model to nemotron-3-ultra-free, fixes auto-retry guard. **BLOCKED**: Reviewer `/oc fix` (missing route step) + PAT `workflows`-scope wall. Awaiting owner action (grant workflows scope, or manually apply route-step YAML + merge). Closes #104 (infra portion).
2. **PR #104 - Prism research/architecture spec + BUILD (issue #103).** OPEN on `opencode/issue103-20260821075928` (head `0e8c2c5`, docs only - no C++). Researcher + Architect delivered `prism/docs/*.md`. Build no-op'd twice on hy3-free. Depends on #106 landing before any `continue` will produce code.
3. **PR #102 - `[Infra] Lab update for #42`.** CLOSED, branch `opencode/issue42-20260821070030` preserved, head `f58834b4` NOT in main. Recover blocked by PAT `workflows`-scope wall. Escalated (no re-spam).

## PENDING (in order)
1. **Owner resolves #106 wall**: grant `workflows` scope to OPENCODE_PAT, OR manually apply Reviewer's route-step YAML to the `lab:` job in `opencode.yml` and merge #106. Once merged, re-trigger `/oc continue` on #104.
2. **#106 fix applied** (if owner grants scope): re-emit `fix` to apply Reviewer's route step + strip guard, then merge after approval.
3. **Prism build (after #106 lands):** `continue` on #104 so Builder implements `prism/` per architecture.md, gated on M0 (bit-exact round-trip + corruption rejection fuzz gate) before optimization. Benchmark on Kodak; target under JPEG XL ~3.1 bpp.
4. **#102 wall:** same owner resolution as #106; then close #42.
5. **Board (#42) resume:** after Prism, pick from parked candidates - no new projects until Prism competitive.
6. **Superseded orphans (#84/#83/#69/#60):** intentionally NOT recovered.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build blocked on #106).
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#68 (Obsidian)** - CLOSED by owner.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `60748e88`. Today's new-project merges: 0/2 (clear for Prism #104 once #106 lands + build clears review/test).
- PR #106: Reviewer posted BLOCKING `/oc fix` (missing route step); Lab Engineer push rejected by PAT workflow wall. Needs OWNER merge.
- PR #104: build no-op'd twice on hy3-free; unblocked only by #106's model switch.
- PR #102: recover blocked (PAT scope), escalated.
- pages.yml: triggers only on PR/workflow_dispatch; Prism build touches no workflow files, so no pages issue on land.

## NEXT STEPS
1. Await owner action on #106 (grant `workflows` scope, or manually apply Reviewer's route-step YAML + merge). This is the single critical blocker for the entire Prism priority.
2. After #106 lands: re-trigger `/oc continue` on #104; confirm Builder pushes C++ and reaches M0 fuzz gate; then route review -> test -> merge.
3. Await owner resolution of #102 PAT-scope wall (ping already sent).
4. OPEN-PR merge-path `lab` fix: folded into #106's `lab:` job; verify after landing.

## OPEN QUESTIONS
- #106: will the owner grant `workflows` scope to OPENCODE_PAT (then I fix+merge), or manually apply the Reviewer's route-step YAML and merge? Until then Prism #104 stays blocked.
- Why did the auto-retry/verify step never post `/oc build this (auto-retry N)`? Fixed by #106's trigger-guard change; confirm after landing.
- #102: owner to grant `workflows` scope or land manually.
- Prism: can MA-tree context model + Squeeze close 9.52 -> under JXL 3.1 bpp on Kodak? Builder/Reviewer/Tester to validate (post-#106).
- Single-root `main` (`60748e88`): intentional owner recovery; no action.
- Superseded orphans (#84/#83/#69/#60): work already in main via merged counterparts; intentionally not recovered.

- Mae, the Maintainer
