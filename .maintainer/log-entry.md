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

---

# 2026-08-12 — evening scheduled run

The factory's first evening maintainer schedule run after bootstrap.

## State snapshot

- **Repo truth (gh):** no open PRs; no open issues; zero `progress/*.md`
  builds in flight. The foundation landed on `main` (last main commit
  `c7b6035` "factory: state the Maintainer's powers explicitly in its
  prompt"); the pre-bootstrap backlog (Arpeggio → Cadence, PRs #18–#39) is
  all merged/closed. Pipeline is idle and healthy.
- **Brainstorm Board** does not exist yet (`brainstorm` label absent, no
  pinned board issue). The Ideator is prompted to create + pin it if missing,
  so a fresh `ideate` dispatch will seed candidates.
- **GitHub Pages is currently DOWN**: `has_pages == false`, the latest push
  deploys fail at `configure-pages` with "Resource not accessible by
  integration" while trying to re-create the Pages site; the `github-pages`
  environment exists (custom branch policy) but the site is gone. Deploys
  have been failing since 2026-08-10 (all pushes/dispatches since), so the
  root landing page + PR previews are not being served right now.

## Decisions & rationale

- **`ideate` → dispatch `ideate.yml`.** The factory is idle, the board is
  empty, and the last built project landed today. Per the blueprint, an idle
  factory means "brainstorm": get fresh candidates on the board so a future
  run can pick and dispatch `/oc build this`. The Ideator creates and pins
  the board itself if absent (it has issues:write), so no board prep needed.
- **No `build`, `continue`, `fix`, `review`, or `merge`.** Nothing is in
  flight; nothing new to review or merge.
- **Pages breakage:** not fixable by a maintainer trigger alone and not
  caused by agent code — the site must be re-created at the repo level
  (owner/settings or a token path). Flagged as an open question and recorded
  here for the owner; the Reviewer/factory review will catch workflow-level
  aspects if a fix PR ever materializes.

## Callbacks made

- `ideate` dispatch (via decision list → hardcoded step).

## Links

- This run: https://github.com/Userfrom1995/Random/actions/runs/31629147993
- Last successful push deploy: 2026-08-09 dispatch run 31323941212; PR-event
  "successes" since then only ran the `comment` job (deploy skipped).

## Open questions

- GitHub Pages is disabled/not-createable by automation and deploys have
  failed since Aug 10 — the root landing page and PR previews are down. Needs
  owner attention (re-enable Pages / provide a working deploy token path).
- Next run: pick a candidate from the freshly-seeded Brainstorm Board and
  open the `agent-generated` issue + `/oc build this`.