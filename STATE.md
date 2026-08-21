# STATE - Random factory checkpoint
- **Updated:** 2026-08-21 (maintainer run 32484208346, event `/oc maintainer` on PR #111, 12:55Z). PR #111 MERGED (12:57:30Z); `main` = `043bd6d`; build pin now free `muse-spark-1.2-contributor-free`. Prism build launched on issue #103. Lab recovery dispatched on #112.

## STANDING OWNER DIRECTIVES (active)
- **Obsidian shipped** (#93 merged manually by owner as orphan root `60748e88`); 9.5209 bpp Kodak. Issue #68 CLOSED.
- **NEXT PRIORITY (owner):** build **Prism (issue #103)** - beat JPEG XL (~3.1 bpp on Kodak).
- **One-PR rule + NEVER delete PR branches:** satisfied; branches preserved (note: #111 branch deleted on merge per standard rebase flow - #111 was a tiny lab-infra fix, not a project PR; the project branch for Prism is #104's `opencode/issue103-20260821075928`).
- **Maintainer sovereign-recovery directive:** `recover` of orphaned/closed PRs authorized; `main` must never become a divergent/orphan ROOT via a bot run.
- **Owner WILL (12:09:40Z):** "change builder model to `muse-spark-1.2`." Delivered as #109 (MERGED, PAID -> crash) then corrected to free `muse-spark-1.2-contributor-free` as #111 (NOW MERGED). Resolved.

## CRITICAL INFRASTRUCTURE STATE
- **`main` = `043bd6d`** (post #111 merge). BUILD pin FIXED: `opencode/muse-spark-1.2-contributor-free` (FREE) at `opencode.yml:358`. Builder runs are no longer billing-blocked.
- **opencode.json:** `model` = `opencode/hy3-free` (free), `small_model` = `opencode/mimo-v2.5-free` (free). Both fine.
- **pages.yml:** manually dispatched after merge (run 32484458543, queued) since push-to-main did not auto-trigger it.
- Issue #110 CLOSED (via #111 merge).

## IN FLIGHT
1. **PR #111 (Lab Engineer free-model fix, issue #110).** MERGED 12:57:30Z (`043bd6d`). Issue #110 CLOSED. DONE.
2. **Prism build (issue #103).** Launched THIS run via `build` trigger -> `/oc build this` on #103. Builder must implement `prism/` (C++) per `prism/docs/architecture.md` (spec from PR #104), gated on M0 bit-exact round-trip + corruption-rejection fuzz gate before optimization. Benchmark Kodak; target under JXL ~3.1 bpp. Then review -> test -> merge.
3. **Lab recovery (issue #112).** Launched THIS run via `lab` trigger -> `/oc lab` on #112 (automatic PR recovery: closed/orphan/interrupted-build preservation).
4. **PR #104 (researcher: Prism spec, issue #103).** Docs-only research/architecture spec; its branch `opencode/issue103-20260821075928` holds `prism/docs/`. The new `build` on #103 supersedes it as the implementation vehicle; #104 remains open as the spec reference (or closes when Prism build PR lands).

## PENDING (in order)
1. **Prism build:** Builder runs on free model; confirm `prism/` C++ reaches M0 fuzz gate; review -> test (Kodak vs JXL ~3.1 bpp) -> merge.
2. **Lab recovery #112:** Lab Engineer implements automatic PR recovery.
3. **#102 wall:** genuine `git push` `workflows`-scope on `OPENCODE_PAT`; owner to grant scope or merge manually; then close #42.
4. **Board (#42) resume:** after Prism, pick from parked candidates.
5. **`lab.yml` Lab Engineer pin bump (`hy3-free`):** lower priority, not blocking.

## ISSUES
- **#103 (Prism)** - OPEN; active priority project (build now launched on free model).
- **#110 (paid model crash)** - CLOSED (resolved by merged #111).
- **#112 (automatic PR recovery)** - OPEN; Lab Engineer dispatched.
- **#108 / #109 (model switch)** - CLOSED by #109 merge.
- **#100 (Resonata)** - CLOSED (owner halt); no recover.
- **#42 (Brainstorm Board)** - OPEN; blocked on #102 landing.
- **#70 (Lab Health)** - Auditor owns daily summary.

## REVIEWER/TESTER/MODEL STATUS
- `origin/main` = `043bd6d`. Today's new-project merges: 0/2 (Prism not yet built; #109/#111 were infra).
- Build agent (workflow `model:` input): `opencode/muse-spark-1.2-contributor-free` = FREE (fixed). Standing worker pin `nemotron-3-ultra-free` available as fallback.
- `lab.yml` Lab Engineer pin: `opencode/hy3-free` (nondeterministic no-op risk; lower priority follow-up).

## NEXT STEPS
1. Builder (free model) implements Prism `prism/` through M0 fuzz gate on issue #103.
2. Review -> test (Kodak vs JXL ~3.1 bpp) -> merge Prism.
3. Lab Engineer delivers PR recovery mechanism (#112).

## OPEN QUESTIONS
- Can the Builder on free `muse-spark-1.2-contributor-free` execute + push C++ and hit M0 fuzz gate, then beat JXL 3.1 bpp on Kodak?
- Will the Prism build need a worker-model fallback (`nemotron-3-ultra-free`) if the free spark pin stalls?
- #102: owner to grant `workflows` scope to `OPENCODE_PAT` or merge manually; its `ideate.yml` change still needed for #42.
- `lab.yml` Lab Engineer pin still `hy3-free`: future `/oc lab` runs risk no-op; follow-up Lab Engineer PR to bump it (lower priority).
- Superseded orphan PRs (#84/#83/#69/#60): intentionally not recovered.

- Mae, the Maintainer
