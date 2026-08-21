# STATE - Random factory checkpoint

- **Updated:** 2026-08-21 (maintainer run 32456311942, EVENT issue_comment on PR #93). The Obsidian priority project is fully shipped (owner manually merged PR #93 into `main` as orphan root `60748e88`, 9.5209 bpp; PNG 13.05 + WebP 9.61 MET; JPEG XL 8.71 gate LIFTED by owner). Issue #68 CLOSED. Priority lock LIFTED. The next-project pipeline is BLOCKED by a 3rd consecutive Ideator stall; this run escalates to `lab` (issue #42) to fix the Ideator prompt + the self-pinging notify step.

## STANDING OWNER DIRECTIVES (active)

- **Obsidian shipped.** Owner manually merged PR #93's branch `opencode/issue68-20260818070512` (`d6fbd1cd`) into `main`; `main` is now the orphan root `60748e88` ("lab: empower Maintainer as sovereign to recover closed/orphaned PRs and resolve conflicts"), containing obsidian (128 files) + all prior projects. Default codec = 9.5209 bpp; R11-R15 experimental predictors gated OFF; 152 lib tests pass.
- **Issue #68 CLOSED** by owner. Priority-project freeze LIFTED; new projects allowed again.
- **One-PR rule + NEVER delete PR branches:** satisfied; PR #93 CLOSED, branch preserved (no `-d`).
- **Runaway-loop guard shipped** (PRs #95/#97/#99): `/oc fix` refused against a closed PR / bare issue; retry counter no longer falls back to phantom `0`. Monitor for recurrence.

## CRITICAL INFRASTRUCTURE STATE

- **`main` = `60748e88`** - an intentional single-root (orphan) commit by the owner's recovery. Contains obsidian + glyphforge/halcyon/kestrel/meridian/etc.
- **PR #93 permanently CLOSED + unreopenable** (head `e184c3c` gc'd); its code is in `main`. Branch `opencode/issue68-20260818070512` intact at `d6fbd1cd` (25 commits).
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`; `opencode.json` `hy3-free`/`mimo-v2.5-free` (free).
- **Ideator soft-stall defect OPEN:** 3 consecutive ideate runs (32452471052 held, 32452715519 asked, 32453237328 no-post) failed to post candidates to #42; notify step self-pings `/oc maintainer`. Fix dispatched this run (`lab` on #42).

## NEXT-PROJECT DECISION (active)

- **Decision:** resume normal project flow via the Ideator + Brainstorm Board (#42). BUT the Ideator is currently broken (3rd stall). This run escalates `lab` on #42 to harden `.github/agents/ideator.md` (unconditional post rule) and gate `ideate.yml`'s notify step. Once fixed, the Ideator posts fresh candidates -> Mae picks the next build and routes research -> architect -> build.
- Parked eligible candidates on #42: Corundum (C crypto), Tundra (Go VCS), Ravel (Elixir/Phoenix) - remain eligible if the new batch does not displace them.

## IN FLIGHT

- None (no open PRs). Pending: the `lab` fix to the Ideator (issue #42); then fresh candidates on #42; then next build.

## PENDING (in order)

1. **Get the Ideator fixed + posting** - `lab` dispatched this run on #42: harden ideator.md + gate the notify step. Await the fix, then re-dispatch `ideate` and pick the next build.
2. **builder.md hollow-docs fix** - optional `lab` pass to patch ONLY `.github/agents/builder.md` (resume re-task on newest directive). Low priority; queue when convenient.
3. **NEW JXL-beating project (optional):** a separate codebase/new name on its own issue/branch (research -> architect -> build). Issue #68 closed, so a new issue would be needed (owner opens, or future ideate). Not urgent; owner lifted the JXL gate for the shipped Obsidian codec.

## ISSUES

- **#68 (Obsidian umbrella)** - CLOSED by owner.
- **#98 (Runaway /oc fix loop)** - CLOSED (PR #99 merged, guard shipped).
- **#96 (Circuit breaker)** - CLOSED (PR #97 merged).
- **#94 (Detect silent no-op builds)** - CLOSED (PR #95 merged).
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - freeze lifted; Ideator stalled 3x -> `lab` fix dispatched this run.

## REVIEWER/TESTER/MODEL STATUS

- Model config: worker workflows `opencode/nemotron-3-ultra-free`; `opencode.json` `hy3-free`/`mimo-v2.5-free`. `origin/main` = `60748e88`.
- pages.yml: last deployed at 05:34:07Z for the merged Obsidian site; triggers only on `pull_request`/`workflow_dispatch`, so the owner's `60748e88` site-content push (if any) would redeploy; no action needed from me.
- No open PRs require merge/review/test this run.

## NEXT STEPS

1. Await the `lab` fix to the Ideator (issue #42), then re-dispatch `ideate`; once candidates land, pick the next build and route research -> architect -> build.
2. (Optional) Queue a `lab` pass to fix `.github/agents/builder.md` hollow-docs root cause.
3. Monitor next lab runs for any stray `/oc fix` on a closed PR/issue to confirm the #99 guard holds.

## OPEN QUESTIONS

- **Ideator fix efficacy:** will the Lab Engineer's hardening make the Ideator reliably post 2-3 candidates? If it stalls again after the fix, escalate further (rewrite the ideate workflow or add a deterministic candidate generator).
- **Recovery root cause (answered):** PR #93 unrecoverable by the factory because its head was gc'd -> unreopenable, and the Maintainer is forbidden from creating PRs/pushing branches. Owner's manual merge + `60748e88` recovery landed it; nothing stranded. The new `60748e88` commit explicitly empowers the Maintainer to recover orphaned PRs in future.
- **Single-root `main`:** intentional owner recovery (`60748e88`); per the owner's directive, no action from me. Worth a `lab` audit note for future merges (ensure new PRs share history with `60748e88` to avoid re-orphaning).
- **builder.md lab (optional):** re-engage a targeted `lab` when convenient.
- **New-project issue:** now allowed (issue #68 closed); a fresh JXL-class project would need its own issue/branch, owner-opened or via ideate.

- Mae, the Maintainer
