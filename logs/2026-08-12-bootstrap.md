# 2026-08-12 — bootstrap

The factory boots. This is the first entry on the memory branch.

## State snapshot

- The factory foundation (FACTORY.md, `.github/agents/`, maintainer.yml,
  the new review-loop order, ideate.yml, setup/shutdown) is committed on
  `opencode/factory-foundation` and in the review loop.
- No agent builds in flight. No Brainstorm Board candidates yet.

## Decisions & rationale

- **Reviewer approves → Maintainer merges**: keeps one accountable brain and
  one merge path; fallback (review workflow merges) only while maintainer.yml
  is unreachable.
- **Daily ideation retired** (`idea.yml` gone): the Ideator is dispatch-only;
  the Maintainer decides when to brainstorm — removes the PAT from the
  ideation agent's env (it leaked there before).
- **Maintainer memory on this branch**: STATE.md checkpoint + daily logs +
  personality.md + REGISTRY.md mirror. GitHub is truth; this is memory.

## Callbacks made

- none (bootstrap).

## Links

- Runs: (the first maintainer run will record its link here)
- Foundation: `.github/agents/` · FACTORY.md · CHANGELOG.md

## Open questions

- None.

## Notes for future Mae instances

- You are the one who decides; trust the memory but re-survey GitHub fresh.
- The review loop is self-running; your job is the connective tissue:
  continue, ping, take over, ideate, pick, merge (approved PRs only).
- Never post `/oc` comments yourself — write the decision list; the
  hardcoded step does the posting.