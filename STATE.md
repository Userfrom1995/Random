# STATE - Random factory checkpoint

- **Updated:** 2026-08-15 (~12:00Z event run 31883518718, triggered by the
  Architect's orientation comment on #59). The Halcyon build is restarting
  through the new Architect-first flow; the Architect is actively drafting the
  blueprint. Quiet run: no triggers.

## In flight

- **Halcyon (issue #59 -> Architect drafting blueprint):** Owner's `/oc
  architect` at 11:58:46Z started run 31883428853 (IN PROGRESS). It posted its
  orientation comment 12:00:46Z (PR #60 confirmed closed unmerged, no
  `opencode/59-*` branch, studying conventions/blueprint formats) and is
  drafting the blueprint. No blueprint PR yet. Expect: blueprint PR on a fresh
  `opencode/59-*` branch ("Blueprint for #59. Closes #59") -> its forward step
  posts `/oc build this` -> Builder implements in resume mode. Wiring quirk
  confirmed live: the Architect's comment spawned a parallel `general` run
  (31883518702) that auto-posts `/oc maintainer` on #59 (noise, benign).

## Just completed

- **Factory change by the owner (this morning):** `d97281c` JSON decision
  handoff schema (permanently fixes reviewer-handover drops) + `5df3bce`
  Architect agent integration (`architect` job in opencode.yml, REGISTRY/
  AGENTS/FACTORY/docs updated). All workflow YAML validated. PR #60 (Halcyon
  scaffold) closed by the owner 11:48:35Z, unmerged; nothing of Halcyon on main.
- Daily shipping cap Aug 15: 2/2 (Beambus + Glyphforge). Cap resets 00:00Z Aug
  16, so the Halcyon merge is legal then.

## Board status (#42)

- Candidates remaining: **Ravel** (Elixir/Phoenix CRDT whiteboard), **Kestrel**
  (Julia NN + draw-to-classify). Zero reactions. Halcyon was picked earlier
  (06:46Z) and is restarting via the Architect.

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` validated; Sunday weekly upgradation check due
  2026-08-16.

## Watch items (owner-side / wiring)

- The `general` job in opencode.yml is NOT excluded from `/oc architect`, so
  architect comments spawn parallel general jobs that auto-post `/oc
  maintainer` on #59. Confirmed live this run (31883518702); noisy but benign.
- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge until then).

## Next steps

1. Watch the Architect run (31883428853) on #59: expect a blueprint PR
   ("Blueprint for #59. Closes #59") and a `/oc build this` handoff to the
   Builder. If the run dies before pushing, re-emit `architect` on #59.
   While the build is `Status: in-progress`, `continue`; on `/oc approve-test`
   merge `gh pr merge <N> --rebase --delete-branch`, close #59, dispatch
   pages.yml, verify `/halcyon/docs/`. Merge legal after 00:00Z cap reset.
2. After Halcyon clears: pick from Ravel/Kestrel (reactions steer; owner's
   count double).
3. Sunday weekly model upgradation check on 2026-08-16.

## Open questions

- Does the Architect -> Builder handoff (new JSON schema + fresh Architect flow)
  work first try on #59?
- Does the parallel general job on `/oc architect` cause interference on the
  `/oc build this` handoff, or just noise?
- GHC toolchain install friction on the Builder's run (expect `continue` needs).

This file is rewritten every run - it is the instant catch-up for any new Maintainer instance. Historical detail lives in `logs/`.
