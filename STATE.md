# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32461650110, EVENT `created` on PR #104, owner directive: build Prism). `main` = `60748e88` (owner orphan root). PR #104 build re-triggered (first build run cancelled). PR #102 recover blocked by PAT workflow-scope wall - escalated.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (2026-08-21, owner, overrides board):** build the **Obsidian-upgrade image codec** (Prism, issue #103) - all major input formats, beat JPEG XL. Prism is the active project. No other new ideas until Prism competitive.
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved on close.
- **Maintainer sovereign-recovery directive:** `60748e88` empowers `recover` of orphaned/closed PRs; main must never become a divergent/orphan ROOT.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `60748e88`** (orphan root from PR #93). Contains obsidian + all prior projects.
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`; `opencode.json` `hy3-free`/`mimo-v2.5-free` (free).
- **WORKFLOW-PUSH PERMISSION WALL (CONFIRMED ROOT CAUSE):** `OPENCODE_PAT` lacks the `workflows` scope, so the recover/merge step cannot push any PR that touches `.github/workflows/*`. This is why PR #102 (touches `ideate.yml`) recovers fail every time. Only the owner granting `workflows` scope to OPENCODE_PAT, or a manual owner merge, can land such PRs. Non-workflow PRs (e.g. Prism #104) are unaffected.
- **OPEN-PR MERGE-PATH GAP (durable):** this workflow only lands CLOSED PRs via `recover`; OPEN approved+tested PRs have no clean merge step. Durable `lab` fix recommended (separate from the PAT-scope wall).

## IN FLIGHT
1. **PR #104 - Prism research/architecture spec (issue #103).** OPEN on `opencode/issue103-20260821075928`. Researcher delivered `prism/docs/*.md`; Architect delivered `prism/docs/architecture.md` (PRSM magic, MA-tree, M0 fuzz gate). Owner posted `/oc build this` (08:06:07) but the build run 1055 was **cancelled with zero jobs** - no code pushed. THIS run re-posted `/oc build this` to actually start the Builder. Closes #103.
2. **PR #102 - `[Infra] Lab update for #42` (Ideator-stall hardening).** CLOSED, branch `opencode/issue42-20260821070030` preserved, head `f58834b4` NOT in main. Recover fails repeatedly due to PAT `workflows`-scope wall. Escalated to owner (ping on #102). Not re-attempting recover until scope granted.

## PENDING (in order)
1. **Prism build:** Builder implements `prism/` per architecture.md, gated on M0 (bit-exact round-trip + corruption rejection fuzz gate) before optimization. Benchmark each iteration on Kodak; target under JPEG XL ~3.1 bpp (Obsidian stopped at 9.52).
2. **#102 wall:** owner grants `workflows` scope to OPENCODE_PAT, OR manually lands #102; then close #42.
3. **OPEN-PR merge-path `lab` fix:** add a clean open-approved-PR merge step (rebase, branch kept) so future merges are clean instead of close-then-recover.
4. **Board (#42) resume:** after Prism, pick from parked candidates - but no new projects until Prism competitive.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build in progress).
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#68 (Obsidian)** - CLOSED by owner.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `60748e88`. Today's new-project merges: 0/2 (clear for Prism #104).
- PR #104: build re-triggered this run. #102: recover blocked (PAT scope), escalated.
- pages.yml: triggers only on PR/workflow_dispatch; Prism build touches no workflow files, so no pages issue on land.

## NEXT STEPS
1. Monitor PR #104 build: confirm the Builder pushes C++ code and reaches M0 fuzz gate; route to review -> test -> merge.
2. Await owner resolution of #102 PAT-scope wall (ping sent).
3. After Prism lands, dispatch `lab` to add the open-approved-PR merge step (durable gap).

## OPEN QUESTIONS
- Will the re-posted `/oc build this` on #104 actually execute (run 1055 was cancelled - cause unknown; possibly a transient concurrency glitch)? If it fails again, investigate before re-triggering.
- #102: will the owner grant `workflows` scope to OPENCODE_PAT, or land manually? Until then it stays orphaned.
- Prism: can MA-tree context model + Squeeze close 9.52 -> under JXL 3.1 bpp on Kodak? Builder/Reviewer/Tester to validate.
- OPEN-PR merge-path gap: route a `lab` pass post-Prism.
- Single-root `main` (`60748e88`): intentional owner recovery; no action.

- Mae, the Maintainer
