# STATE - Random factory checkpoint

- **Updated:** 2026-08-16 (~18:38Z event run 31965100782, owner "/oc
  maintainer, please use the factory engineer for this." on #72 at
  18:36:38Z). **Owner directed the Factory Engineer path for #72.** The
  Factory Engineer (CTO) was integrated by the owner at 18:33Z (commit
  `2761885`, `factory.yml` + `.github/agents/factoryengineer.md`), and the
  PAT-backed `factory.yml` push step can land `.github/workflows/*.yml`
  changes - resolving the `workflows: write` blocker that killed #72's two
  build attempts. This run dispatches `factory` on #72 (fixes #72 + #73 in
  the round) and `factory` on PR #69 (Mode 2 model switch for the Obsidian
  billing stall, per the owner's #74 auto-switch policy).

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec competitive with
  JPEG XL / WebP / conventional methods, benchmarked on Kodak.** PR #69 open,
  head `2377f3cc` (research/spec/architecture docs + Cargo workspace scaffold
  only, NO codec source). Billing `CreditsError` has failed 5+ continue
  attempts. **This run dispatches `factory` on PR #69** (Mode 2): the CTO
  edits the `opencode.yml` build model to a free fallback (hy3-free /
  nemotron-3-ultra-free / nemotron-3.5-lightning-free / laguna-s-2.1-free)
  directly on main via the PAT step. On its `{"action":"maintainer"}`
  handoff, re-trigger the Obsidian `continue` so the Builder re-implements
  effort 0 and pushes.

## In flight

- **Issue #72 (infra fix) - FACTORY DISPATCHED this run.** Owner ordered the
  Factory Engineer path. `factory` on #72: the CTO opens an infra PR (`Closes
  #72`) that (1) scopes the build baseline/verify to the target PR head (fix
  path lines 555-556 pattern), (2) adds force-with-lease guidance to the
  BUILD/FIX prompts + builder.md/fixer.md, and (3) fixes #73 (opencode-review
  crash on non-PR) so the factory review forward (which posts /oc review on
  the issue number) works. PR branch pattern `opencode/factory-72-*`; pushed
  by the PAT step; `{"action":"review"}` -> reviewer, then test, then merge
  (`gh pr merge <N> --rebase --delete-branch`), close #72, dispatch pages.yml.
- **Issue #73 (opencode-review crash on non-PR) - FOLDED INTO the #72
  factory round** (not a separate dispatch; the factory review handoff needs
  it). No separate trigger.
- **PR #69 (Obsidian) - model-switch FACTORY DISPATCHED this run** (Mode 2,
  direct main edit, PAT-pushed). Watch for the CTO's `{"action":"maintainer"}`
  handoff, then re-trigger Obsidian `continue`. Do NOT run the two factory
  dispatches concurrently with any opencode build.
- **PR #67 (Meridian) - MERGED `c44736f` earlier, #66 closed, pages
  deployed.** No further action.
- **Issue #74 (billing) - CLOSED by the owner.** Standing auto-switch policy
  active; the factory Mode 2 path finally makes it executable.

## Lab Health & Audit Logs (#70)

- The Auditor owns the daily health summary on #70 (ran 11:30Z/12:33Z, found
  the build-verify false positive -> #72/#73/#74). This run acts on the
  reopened #72/#73 via the factory path the owner just integrated.

## Board status (#42)

- **FROZEN by the owner's directive** - no picks until Obsidian resolves.
  Candidates parked: Corundum, Tundra, Ravel. No ideate (frozen).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` (reviewer + tester), `deepseek-v4-flash-free`
  (build/fixer/maintainer/ideate/research/architect) unchanged. The
  Factory Engineer runs on `mimo-v2.5-free`. The billing gate (#74) keeps
  degrading the build agent; the auto-switch to a free fallback is now
  possible via the factory Mode 2 PAT path (this run's PR #69 dispatch).

## Next steps

1. **#72: shepherd the factory PR** (`opencode/factory-72-*`): on
   `{"action":"review"}` the reviewer runs; on `/oc approve-test` merge,
   close #72 (+ #73 if linked), dispatch pages.yml.
2. **PR #69: on the CTO's `{"action":"maintainer"}` handoff**, re-trigger
   the Obsidian `continue` (model now free-tier fallback). Shepherd -> review
   -> test -> merge per the pipeline.
3. **#73**: covered inside the #72 factory round; verify the review workflow
   handles non-PR gracefully once the factory PR review runs.
4. **#70**: Auditor owns the daily health summary; watch for anomalies.
5. No board picks until Obsidian resolves (owner's freeze).
6. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the factory PR for #72 open cleanly (PAT push of `opencode/factory-72-*`)
  and survive the extra-hard lab review?
- Does the Mode 2 model switch on PR #69's factory dispatch land on main, and
  does the free fallback model clear the billing CreditsError for the next
  Obsidian continue?
- Did the schedule maintainer run 31965038788 (18:35-18:37Z) also post any
  triggers that double up with this run's factory dispatches?