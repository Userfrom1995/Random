# STATE - Random factory checkpoint

- **Updated:** 2026-08-21 (maintainer run 32456348253, scheduled). The Ideator's
  third dispatch (run 32453237328, success) finally posted a fresh 3-candidate
  batch on #42: Resonata (audio DSP synth, C->WASM), Aether (P2P file-sync,
  Elixir), Nimbus (roguelike, Nim). Mae picked **Resonata**, opened issue #100,
  and routed it to research. Normal project flow has resumed.

## STANDING OWNER DIRECTIVES (active)

- **Obsidian PR #93 = finished + landed.** Owner manually merged branch
  `opencode/issue68-20260818070512` (`d6fbd1cd`) into `main` as `0eb9de0f`
  ("Merge PR #93: Obsidian lossless codec") on 2026-08-21. 128 obsidian files
  present in `main`; the codec (R10-B CFL + CMARC backend, 9.5209 bpp) beats
  PNG 13.05 + WebP 9.61.
- **Issue #68 CLOSED** by owner (2026-08-21T05:34:05Z). The priority-project
  freeze is LIFTED; new projects are allowed again.
- **ONE Obsidian PR rule:** satisfied historically; PR #93 closed/merged via
  manual merge. Branch preserved (no `-d`).
- **NEVER delete PR branches after merge.** Kept.
- **Runaway-loop guard shipped** (PRs #95/#97/#99): `opencode.yml` now refuses
  `/oc fix` against a non-OPEN PR or a bare issue, and the retry counter no
  longer falls back to a phantom `0`. Monitor for recurrence.

## CRITICAL INFRASTRUCTURE STATE

- **`main` = `0eb9de0f`** (owner's manual merge of PR #93 as a merge-commit of
  unrelated histories). 128 obsidian files present; build artifacts intact.
- **Branch `opencode/issue68-20260818070512` intact** at `d6fbd1cd` (25
  commits). Default codec = 9.5209 bpp; all R11-R15 experimental predictors
  gated OFF. 152 lib tests pass.
- **PR #93 permanently CLOSED + unreopenable** (head `e184c3c` gc'd), but its
  code is now in `main` via the owner's manual merge - nothing stranded.
- **MODEL PINS:** worker workflows `opencode/nemotron-3-ultra-free`.
  `opencode.json` on main still `hy3-free`/`mimo-v2.5-free` (free).
- **Runaway guard verified shipped** (#99 merged, closes #98). Monitor next lab
  runs for any stray `/oc fix` on a closed PR/issue to confirm it holds.

## NEXT-PROJECT DECISION (active, run 32456348253)

- **Decision:** Resume normal project flow. The Ideator's fresh batch landed on
  #42 (Resonata / Aether / Nimbus). Mae picked **Resonata** and opened the real
  project issue #100; the Researcher is dispatched to spec the synthesis
  algorithms. Follow-on: architect -> build. Aether and Nimbus stay eligible as
  parked candidates for subsequent builds.
- **Resonata (#100):** real-time audio synthesizer in C compiled to WASM;
  hostable on Pages (entrypoint /resonata/index.html). Core first (oscillator +
  ADSR + biquad as a tested C library), then WASM + browser UI; WebUSB MIDI is a
  stretch goal. Fresh language (C) for the factory; strong showcase demo.

## IN FLIGHT

- **Resonata (#100):** research dispatched this run. Awaiting Researcher spec,
  then architect, then build.

## PENDING (in order)

1. **Resonata research spec** - Researcher on #100 (dispatched). Then architect
   blueprints, then Builder build.
2. **builder.md hollow-docs fix** - optional `lab` pass to patch ONLY
   `.github/agents/builder.md`. Low priority; queue when convenient.
3. **Follow-on builds (optional):** Aether (#42 parked, Elixir distributed
   systems) and Nimbus (#42 parked, Nim roguelike) remain eligible candidates
   for later builds once Resonata ships.

## ISSUES

- **#68 (Obsidian umbrella)** - CLOSED by owner (2026-08-21T05:34:05Z).
- **#98 (Runaway /oc fix loop)** - CLOSED (PR #99 merged, guard shipped).
- **#96 (Circuit breaker)** - CLOSED (PR #97 merged).
- **#94 (Detect silent no-op builds)** - CLOSED (PR #95 merged).
- **#100 (Resonata)** - OPEN, agent-generated, research dispatched this run.
- **#70 (Lab Health)** - Auditor owns daily summary.
- **#42 (Brainstorm Board)** - fresh batch posted (Resonata/Aether/Nimbus);
  Resonata picked; Aether/Nimbus parked.

## REVIEWER/TESTER/MODEL STATUS

- Model config: worker workflows `opencode/nemotron-3-ultra-free`;
  `opencode.json` `hy3-free`/`mimo-v2.5-free`. `origin/main` = `0eb9de0f`.
- pages.yml: triggers only on `pull_request`/`workflow_dispatch`, not push to
  main; the manual merge of a branch (no site-content change) did not trigger a
  Pages deploy, which is correct. Pages last deployed at 05:34:07Z.
- No open PRs require merge/review/test this run.

## NEXT STEPS

1. Await the Researcher's synthesis spec on #100; then dispatch architect, then
   build (research -> architect -> build pipeline).
2. (Optional) Queue a `lab` pass to fix `.github/agents/builder.md`
   hollow-docs root cause when convenient.
3. Monitor next lab runs for any stray `/oc fix` on a closed PR/issue to confirm
   the #99 guard holds.
4. Keep issue #68 closed per the owner's action; do not reopen unless the owner
   directs a new JXL-class effort.

## OPEN QUESTIONS

- **Ideator freeze heuristic (resolved for now):** the Ideator's third dispatch
  (32453237328) posted a fresh batch, breaking the prior stale-narrative stall.
  If it stalls again on future dispatches, escalate to `lab` to harden
  `.github/agents/ideator.md` (always post 2-3 candidates) and gate the
  self-pinging notify step - per the escalation guard logged in run
  32452805905.
- **Recovery root cause (answered):** PR #93 unrecoverable by the factory
  because (a) its head commit was gc'd -> unreopenable, and (b) the Maintainer
  is forbidden from creating PRs/pushing branches. The branch `d6fbd1cd` was
  preserved, so the owner's manual merge landed it cleanly; no work lost.
- **Single-commit `main`:** main is a single root commit with PR #93 merged as a
  merge-commit of unrelated histories (orphan branch). Intentional
  (circuit-breaker) but worth a `lab` audit note; not escalated.
- **builder.md lab (optional):** re-engage a targeted `lab` when convenient.
- **New-project issue:** now allowed (issue #68 closed); Resonata #100 opened
  by Mae to resume flow. Aether/Nimbus remain parked candidates on #42.

- Mae, the Maintainer
