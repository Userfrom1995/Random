# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32482108970, EVENT `created` on #104, 12:29Z). `main` = `15801d8` (owner infra push). Prism #104 STILL blocked: `opencode.yml` build pin (358) is `hy3-free`; the owner wants it switched to `muse-spark-1.2` via a PR. The Lab Engineer's first `/oc lab` (run 32480553596) no-op'd on `hy3-free` and opened no PR, so this run re-dispatches `/oc lab` on #104.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak). Prism is the active project.
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved.
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run.
- **Owner OVERROLE (11:56:57Z):** PAT merges via API; prior "PAT `workflows`-scope wall" framing was imprecise. The genuine restriction is only `git push` of workflow files. Recorded as dissent; complied.
- **Owner CLOSED #106 (12:04:54Z) then #107 (12:19:30Z), BOTH unmerged** - read as an informed, repeated decision to avoid reintroducing the redundant `lab:` job that duplicates `lab.yml`. Holding BOTH closed; NOT force-recovering.
- **Owner WILL (12:09:40Z):** "change builder model to `muse-spark-1.2`, open a pr for it." Verified `muse-spark-1.2` is a real model. This supersedes the earlier nemotron-3-ultra-free preference for the build pin.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `15801d8`** (OWNER manual infra push; fresh orphan root lineage from `668222b`). Contains: separate `lab.yml` workflow (sole `/oc lab` handler), all agent prompts, hardened `maintainer-recover.py`.
- **MERGE MECHANISM (clarified):** `gh pr merge` via the **API** does NOT require `workflows` scope and handles unrelated histories. Only `git push` of workflow files needs the scope (affects `recover.py`'s closed-PR `git push` path for #102).
- **MODEL SWITCH NOT ON MAIN:** `opencode.yml` still pins `hy3-free` at build(358), fix(880), lab(696), reviewer(50), researcher(151). `lab.yml` Lab Engineer pin (line 59) ALSO `hy3-free`. So BOTH build/fix AND `/oc lab` still no-op until switched.
- **BUILD MODEL NO-OP (root cause):** build agent pinned `opencode/hy3-free` ends without executing tool calls. Only the switch to a working model (owner now wants `muse-spark-1.2`) in `main` fixes it.
- **LAB ENGINEER NO-OP (new finding, run 32482108970):** the Lab Engineer's `/oc lab` at 12:09:40Z (run 32480553596) ran but produced no branch/PR - it no-op'd on `hy3-free` just like the Builder. This is a catch-22: to switch models, the Lab Engineer must execute, but it is itself on the no-op model. Re-dispatched this run.

## IN FLIGHT
1. **PR #104 - Prism research/architecture spec + BUILD (issue #103).** OPEN, docs-only (head `0e8c2c5`), no C++. Builder no-op'd twice on `hy3-free`. BLOCKED on the model switch reaching main. Owner wants build pin -> `muse-spark-1.2` via a PR.
2. **Model-switch PR (new, owner will 12:09:40Z).** NOT YET OPEN - Lab Engineer's first attempt no-op'd. This run re-dispatched `/oc lab` on #104 to open a slim PR: only build `model:` 358 hy3-free -> `opencode/muse-spark-1.2`, NO redundant `lab:` job (lab.yml handles `/oc lab`).
3. **PR #106 / #107 - `[Infra] Lab update for #104`.** CLOSED unmerged (head `0505577`, branch preserved). Redundant `lab:` job duplicating `lab.yml`. Owner closed both; HELD (no recover, no recreate).
4. **PR #102 - `[Infra] Lab update for #42`.** CLOSED, branch preserved, head `f58834b4` NOT in main. Recover blocked ONLY by the genuine `git push` `workflows`-scope restriction on `OPENCODE_PAT`. Owner to grant `workflows` scope or merge manually. Already escalated; no re-spam.

## PENDING (in order)
1. **Unblock Prism - land the build model switch:** a PR (Builder `model:` -> `opencode/muse-spark-1.2`) must merge into main. Owner wants a PR; the Lab Engineer is the path. If the re-dispatched `/oc lab` also no-ops, escalate to an emergency direct edit of `lab.yml` line 59 (switch Lab Engineer off `hy3-free`) per the model-management policy, then retry.
2. **Prism build (after switch lands):** emit `continue` on #104 so the Builder (now `muse-spark-1.2`) implements `prism/` per `prism/docs/architecture.md`, gated on M0 (bit-exact round-trip + corruption rejection fuzz gate) before optimization. Benchmark Kodak; target under JXL ~3.1 bpp. Then review -> test -> merge.
3. **#102 wall:** genuine `git push` `workflows`-scope on `OPENCODE_PAT` (NOT the merge API). Owner grants scope, or manually merges #102; then close #42.
4. **Board (#42) resume:** after Prism, pick from parked candidates - no new projects until Prism competitive.
5. **`recover.py` hardening:** fall back to `gh pr merge --merge` when `--rebase` fails on unrelated history, so the bot self-merges orphaned open PRs without owner intervention.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build blocked on model switch).
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#68 (Obsidian)** - CLOSED by owner.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `15801d8`. Today's new-project merges: 0/2 (clear for Prism #104 once the switch lands + build clears review/test).
- PR #104: build no-op'd twice on `hy3-free`; unblocked only by the model switch in main (owner wants `muse-spark-1.2`).
- PR #107/#106: CLOSED unmerged by owner (recreation of each other); held.
- PR #102: recover blocked by genuine `git push` `workflows`-scope (workflow file); escalated.
- `lab.yml` Lab Engineer pin: `hy3-free` (no-op risk for `/oc lab`); secondary but real.
- pages.yml: triggers only on PR/workflow_dispatch; Prism build touches no workflow files, so no pages issue on land.

## NEXT STEPS
1. Confirm the re-dispatched `/oc lab` (this run) opens the muse-spark switch PR. If it no-ops again, edit `lab.yml` line 59 off `hy3-free` (emergency) and retry, OR ask the owner to do the 1-line main edit.
2. After switch merges in main: emit `continue` on #104; confirm Builder pushes C++ and reaches M0 fuzz gate; then route review -> test -> merge.
3. Hold #106/#107 (redundant lab job); do not recreate.

## OPEN QUESTIONS
- Will the re-dispatched `/oc lab` actually open the muse-spark switch PR, or no-op again (Lab Engineer on `hy3-free`)? If no-op, switch `lab.yml` Lab Engineer pin (emergency edit) before retrying.
- #104: after the switch lands, can the Builder on `muse-spark-1.2` execute + push and hit M0 fuzz gate? Then under JXL 3.1 bpp on Kodak?
- #102: owner to grant `workflows` scope to `OPENCODE_PAT` (for the `git push` recover path of workflow files) or merge manually; its `ideate.yml` change still needed for #42.
- Superseded orphan PRs (#84/#83/#69/#60): work already in main via merged counterparts; intentionally not recovered.
- `main` `15801d8`: owner re-sync (fresh orphan root lineage); unrelated-history state resolved earlier.

- Mae, the Maintainer
