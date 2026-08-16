# STATE - Random factory checkpoint

- **Updated:** 2026-08-16 (~08:47Z event run 31937305741; Meridian Level 3
  Architect round routed to the Builder; Obsidian research handoff repaired
  with an architect trigger on PR #69).

## Priority project (the fundamental goal)

- **Issue #68 Obsidian - lossless image-compression codec competitive with
  JPEG XL / WebP / conventional methods, benchmarked on Kodak.** Research
  phase COMPLETE: Dr. Ada delivered PR #69 (branch
  `opencode/issue68-20260816082105`, head `aa274f3c`) with
  `obsidian/docs/research.md` (SOTA survey: MED/GAP/predictor banks, YCoCg-R,
  context modeling, Huffman/Golomb-Rice/arithmetic/ANS, published Kodak rates
  PNG ~4.2 / JPEG-LS ~3.7 / WebP ~3.4 / FLIF ~3.1 / JPEG XL ~3.1 / MRP ~2.6),
  `algorithmic-spec.md` (v1 codec: container, YCoCg-R, predictor bank with
  per-context map, gradient+activity contexts, adaptive rANS 12-bit, effort
  levels, O(n), bit-exact fidelity), and `benchmark-methodology.md` (pinned
  toolchain, canonical PPM ground truth, M1 beat WebP/PNG, M2 within 10% of
  JPEG XL, M3 within ~3%). Her `architect` handoff was MISDIRECTED by the
  forward-step target bug to PR #67; the Architect trigger on PR #69 has now
  been emitted this run, so the design phase starts from the spec. Flow:
  Researcher (done) -> Architect (design) -> Builder (build) -> review ->
  test -> merge. Every iteration benchmarked on Kodak and documented. NO new
  projects or board picks until Obsidian resolves.

## In flight

- **PR #67 (Meridian, Rust search engine) - Level 3 Architect round done
  (design-only); Builder routed via `/oc continue` to implement milestones
  19-25.** Head `4a39b82a5c7053a53697154718e9d19c0ab496a7` (Architect commit
  `4a39b82`, pushed 08:45Z), mergeable CLEAN. Level 3 blueprint: wildcard/
  prefix search (`term*`, `term?`), fielded search (`title:`/`source:`),
  phrase slop (`"a b"~N`), term boosting (`term^N`), pagination
  (`--offset`/`--limit` + `total_hits`/`pages` + UI pager), `suggest`/
  typeahead, `--threads` + `--stopwords`; index stays v2, 9296-check
  consistency baseline holds and grows. Level 2 work remains fully approved
  (Reviewer 05:18Z + Tester 05:22:47Z on `91d46d8`) but the head has moved, so
  Level 3 must clear the full review + test rounds before merge. Merge held by
  today's 2/2 cap (resets 00:00Z Aug 17) regardless.
- **PR #69 (Obsidian research/spec) - awaiting the Architect design round.**
  Zero comments so far; the Researcher's `/oc architect` was misdirected to
  PR #67 by the forward-step target bug (confirmed in run log:
  `pull/67#issuecomment-5306531116`). Architect trigger emitted this run.
  4 held PR-preview/trigger runs on this head; approve via the held-run sweep.

## Board status (#42)

- **FROZEN by the owner's directive** - no picks until Obsidian resolves.
  Candidates parked: Corundum (C crypto), Tundra (Go VCS), Ravel (Elixir/Phoenix
  CRDT whiteboard). Zero owner reactions across the board's life. No ideate
  (frozen anyway; board not thin).

## Reviewer/Tester model status

- `opencode/mimo-v2.5-free` (reviewer + tester), `deepseek-v4-flash-free`
  (build/fixer/maintainer/ideate/research/architect) unchanged after the
  2026-08-16 Sunday check. Researcher integrated by the owner (`b1116ff2`).

## Watch items (owner-side / wiring)

- **Forward-step target-selection bug bit again:** the Researcher's forward
  step posts to the `last` opencode/* PR in `gh pr list`, which picked #67
  instead of #69. Architect's `continue` handoff also still falls through to
  `/oc maintainer` (only `build` is handled). Both are owner-side wiring fixes.
- Architect forward step only handles `{"action":"build"}` - a `continue`
  decision falls through to `/oc maintainer`; Architect should write `build`.
- Auto-retry counter pollution: stale `/oc build this (auto-retry N)` comments
  still count - re-emit, never delete owner comments.
- Durable Pages-after-bot-merge trigger still owner-side (manual dispatch per
  merge; maintainer.yml re-dispatches if main advanced).

## Next steps

1. **PR #67**: Builder implements milestones 19-25 (`/oc continue` emitted);
   then Reviewer -> Tester; merge at a cap-open run (`gh pr merge 67 --rebase
   --delete-branch`), close #66, dispatch pages.yml, verify `/meridian/`
   serves. Do not re-review Level 2's old approval - Level 3 changes the head.
2. **Obsidian (#68)**: Architect design round on PR #69 (`/oc architect`
   emitted) -> Builder (`build`) -> review -> test -> merge. Shepherd with
   `continue` while in-progress.
3. No board picks until Obsidian resolves (owner's freeze).
4. Next Sunday (2026-08-23): weekly model upgradation check.

## Open questions

- Does the Architect's Obsidian round land from the research spec and hand
  `build` to the Builder, or does the forward step drop the handoff again?
- Does the Builder implement Meridian Level 3 cleanly (wildcard/fields/slop/
  boost/pagination/suggest/stopwords, JS mirror parity, 9296 baseline grows)?
- When Obsidian produces a competitive lossless result, does the owner call it
  done or keep iterating? "Proven unviable" = documented research conclusion.
- Obsidian's PR is a new-project PR - subject to the 2/day merge cap when it
  ships.