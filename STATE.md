# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32462702690, EVENT `created` on PR #104, owner `/oc maintainer` 08:20:05Z). `main` = `60748e88` (owner orphan root). Prism build has green-no-op'd TWICE (runs 32461984795 + 32462425172) on `opencode/hy3-free`; dispatched **Lab Engineer** (`/oc lab` #104) to switch the build model + fix the auto-retry gap instead of re-triggering a 3rd no-op. #102 recover still blocked by PAT workflow-scope wall; escalated (no re-spam).

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (2026-08-21, owner, overrides board):** build the **Obsidian-upgrade image codec** (Prism, issue #103) - all major input formats, beat JPEG XL. Prism is the active project. No other new ideas until Prism competitive.
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved on close.
- **Maintainer sovereign-recovery directive:** `60748e88` empowers `recover` of orphaned/closed PRs; main must never become a divergent/orphan ROOT.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `60748e88`** (orphan root from PR #93). Contains obsidian + all prior projects.
- **BUILD MODEL NO-OP (NEW ROOT CAUSE, this run):** the opencode build agent pinned to `opencode/hy3-free` (opencode.yml line 358) *answers with a plan* ("I'll scaffold B0, commit and push") and ends its run without executing tool calls. Observed twice (32461984795, 32462425172), both ~3 min (far under the 105-min timeout). The auto-retry/verify step (lines 410-445) also did NOT self-heal - no `/oc build this (auto-retry N)` was ever posted, so its branch-detection/trigger-matching has a gap. **Fix:** Lab Engineer switches build model to `opencode/nemotron-3-ultra-free` (standing worker pin) and fixes the retry trigger (the `contains(..., ' /oc build')` leading-space guard can miss `/oc build this (auto-retry N)`).
- **WORKFLOW-PUSH PERMISSION WALL (CONFIRMED ROOT CAUSE):** `OPENCODE_PAT` lacks the `workflows` scope, so the recover/merge step cannot push any PR that touches `.github/workflows/*`. This blocks PR #102 (touches `ideate.yml`) AND any Lab Engineer PR that edits `opencode.yml`. Only the owner granting `workflows` scope to OPENCODE_PAT, or a manual owner merge, can land such PRs. Non-workflow PRs (e.g. Prism #104) are unaffected.
- **OPEN-PR MERGE-PATH GAP (durable):** this workflow only lands CLOSED PRs via `recover`; OPEN approved+tested PRs have no clean merge step. Durable `lab` fix recommended.

## IN FLIGHT
1. **PR #104 - Prism research/architecture spec + BUILD (issue #103).** OPEN on `opencode/issue103-20260821075928` (head `0e8c2c5`, docs only - no C++). Researcher + Architect delivered `prism/docs/*.md` (research, algorithmic-spec, architecture w/ PRSM magic + MA-tree + M0 fuzz gate, benchmark-methodology). Build runs 32461984795 + 32462425172 both green-NO-OP'd (hy3-free agent planned but pushed no code). THIS run dispatched **Lab Engineer** (`/oc lab` #104) to fix the build-model no-op + auto-retry gap; the build will be re-triggered (via `continue`) AFTER the Lab Engineer's opencode.yml fix merges. Closes #103.
2. **PR #102 - `[Infra] Lab update for #42` (Ideator-stall hardening).** CLOSED, branch `opencode/issue42-20260821070030` preserved, head `f58834b4` NOT in main. Recover fails repeatedly due to PAT `workflows`-scope wall. Escalated to owner (ping on #102). Not re-attempting recover until scope granted.

## PENDING (in order)
1. **Lab Engineer fix (#104):** switch build model hy3-free -> nemotron-3-ultra-free; fix auto-retry trigger; (secondary) open-PR merge-path gap. Lab Engineer PR will touch `opencode.yml` -> needs OWNER merge (PAT wall).
2. **Prism build (after lab fix):** re-trigger `continue` so Builder implements `prism/` per architecture.md, gated on M0 (bit-exact round-trip + corruption rejection fuzz gate) before optimization. Benchmark each iteration on Kodak; target under JPEG XL ~3.1 bpp (Obsidian stopped at 9.52).
3. **#102 wall:** owner grants `workflows` scope to OPENCODE_PAT, OR manually lands #102; then close #42.
4. **Board (#42) resume:** after Prism, pick from parked candidates - but no new projects until Prism competitive.
5. **Superseded orphans (#84/#83/#69/#60):** intentionally NOT recovered - their work already shipped via merged counterparts (#76/#61/#93). No action.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build blocked on lab fix).
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#68 (Obsidian)** - CLOSED by owner.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `60748e88`. Today's new-project merges: 0/2 (clear for Prism #104 once it builds + clears review/test).
- PR #104: build no-op'd twice on hy3-free; Lab Engineer dispatched this run to fix the model + retry gap. #102: recover blocked (PAT scope), escalated.
- pages.yml: triggers only on PR/workflow_dispatch; Prism build touches no workflow files, so no pages issue on land.

## NEXT STEPS
1. Wait for Lab Engineer PR (build model switch + auto-retry fix). It touches `opencode.yml` -> will need OWNER merge (PAT wall). After it lands, re-trigger `continue` on #104 and confirm the Builder actually pushes C++ and reaches M0 fuzz gate; then route review -> test -> merge.
2. Await owner resolution of #102 PAT-scope wall (ping already sent).
3. OPEN-PR merge-path `lab` fix: fold into the Lab Engineer pass (#104) or a follow-up.

## OPEN QUESTIONS
- Will switching the build model to nemotron-3-ultra-free make the Builder actually execute + push (the hy3-free agent planned but never acted)? Lab Engineer to confirm.
- Why didn't the auto-retry/verify step post `/oc build this (auto-retry N)` after the two no-ops? Likely the branch-detection/leading-space trigger guard; Lab Engineer to fix.
- #102: will the owner grant `workflows` scope to OPENCODE_PAT, or land manually? Until then it stays orphaned.
- Prism: can MA-tree context model + Squeeze close 9.52 -> under JXL 3.1 bpp on Kodak? Builder/Reviewer/Tester to validate (post-lab-fix).
- Single-root `main` (`60748e88`): intentional owner recovery; no action.
- Superseded orphans (#84/#83/#69/#60): work already in main via merged counterparts; intentionally not recovered.

- Mae, the Maintainer
