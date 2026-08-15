# STATE - Random factory checkpoint

- **Updated:** 2026-08-15 (~11:53Z dispatch run 31883206947, triggered by the
  owner right after the factory changes). Owner integrated the Architect agent
  and the JSON handoff schema, then closed PR #60 (Halcyon scaffold). Halcyon
  is restarting through the new Architect-first flow.

## In flight

- **Halcyon (issue #59 -> architect this run):** The owner closed PR #60 at
  11:48:35Z - the build had stalled at a scaffold (3/10 milestones; the
  Reviewer approved it but the handover to the Tester silently dropped on the
  old prose-grep path, the exact bug the owner's new JSON schema fixes). `architect`
  emitted this run on #59: the Architect writes the blueprint (ideas/ + progress/
  with `Status: in-progress`), opens a "Blueprint for #59. Closes #59" PR on a
  fresh `opencode/59-*` branch, and its forward step posts `/oc build this` for
  the Builder.

## Just completed

- **Factory change by the owner (two commits):**
  - `d97281c` (10:56:40Z) "standardize agent handoff via JSON decision schema":
    reviewer/tester/builder now write `/tmp/random-factory-decision.json`
    (`{"action":"test"|"fix"|"maintainer"|"review"|"continue"}`); workflow
    forward-steps read the file instead of grepping prose. This permanently
    fixes the reviewer-handover drops (Orrery #46, Glyphforge #58, PR #60).
  - `5df3bce` (11:45:15Z) "integrate Architect agent, update docs, and ensure
    cleanup guards": new `.github/agents/architect.md`, `architect` job in
    opencode.yml (trigger `/oc architect`/`/oc plan`), REGISTRY/AGENTS/FACTORY/
    setup.sh/docs updated, `.specstory/` gitignored. All workflow YAML valid
    (validated this run).
- **PR #60 (Halcyon scaffold) CLOSED by the owner 11:48:35Z**, unmerged.
  Branch `opencode/59-halcyon-functional-language-vm` (head `e508d7c`) still
  exists; harmless (only open PRs are targeted). Nothing of Halcyon is on main.
- Daily shipping cap Aug 15: 2/2 (Beambus + Glyphforge). Cap resets 00:00Z Aug
  16, so the Halcyon merge is legal then.

## Board status (#42)

- Candidates remaining: **Ravel** (Elixir/Phoenix CRDT whiteboard), **Kestrel**
  (Julia NN + draw-to-classify). Zero reactions. Halcyon was picked earlier
  (06:46Z) and is now restarting via the Architect.

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` validated; Sunday weekly upgradation check due
  2026-08-16.

## Watch items (owner-side / wiring)

- The `general` job in opencode.yml is NOT excluded from `/oc architect`, so
  posting the trigger also starts a parallel general job that auto-posts
  `/oc maintainer` on #59. Benign but noisy; the next maintainer run may see an
  extra run. Noted; not blocking.
- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge until then).

## Next steps

1. Watch the Architect run on #59: expect a blueprint PR ("Blueprint for #59.
   Closes #59") and a `/oc build this` handoff to the Builder. `continue` while
   `Status: in-progress`; on `/oc approve-test` merge `gh pr merge <N> --rebase
   --delete-branch`, close #59, dispatch pages.yml, verify `/halcyon/docs/`.
2. After Halcyon clears: pick from Ravel/Kestrel (reactions steer; owner's
   count double).
3. Sunday weekly model upgradation check on 2026-08-16.

## Open questions

- Does the Architect -> Builder handoff (new JSON schema + fresh Architect flow)
  work first try on #59?
- Does the parallel general job on `/oc architect` cause noise/interference?
- GHC toolchain install friction on the Builder's run (expect `continue` needs).

This file is rewritten every run - it is the instant catch-up for any new Maintainer instance. Historical detail lives in `logs/`.
