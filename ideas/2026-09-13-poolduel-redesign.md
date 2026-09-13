# Poolduel Redesign Blueprint: The Bible of PostgreSQL Connection Poolers (Refs #302)

Date: 2026-09-13. Operative plan: `864738b38f5d458533cfa0faf1bf7e0eef54527f`
(`poolduel/REDESIGN_PLAN.md` v2.2, branch `opencode/302-poolduel-redesign-plan`).
Status of plan: draft v2.2, owner-approved as the operative rev for execution.
This blueprint structures it into autonomous milestones per plan section 0.
No `Closes #302` until the full gate in plan section 11 passes. No owner
notification until publishable grade (plan section 0, rule 6).

## Summary

Rebuild Poolduel from an honest M1/M2 benchmark harness into the definitive,
conference-grade reference on PostgreSQL connection pooling: PgBouncer,
pgagroal, Odyssey, pgcat, pgpool-II, plus Supavisor as a first-class sixth
contender, on PostgreSQL 17. Static-first Pages site under `/poolduel/`:
master report, six per-pooler dossiers, buyer guide, architecture taxonomy,
methodology, reproducibility runbook. Every public number pre-rendered in
table plus chart plus CSV plus raw JSON. Statistics rebuilt on paired 95
percent bootstrap CIs with multiplicity control. Scale 10 plus scale 100,
soak arms, resource metrics, enforced PG config, equalized-auth churn
control. Common ground preserved: best-mode per pooler on shared load
(SPEC.md:37-38, methodology.md:48-56), never identical knobs.

## Deliverables

- `poolduel/docs/claims.md` (pre-registered claim registry, plan section 4)
- `poolduel/docs/spec-v1.md` (versioned benchmark spec, plan section 12.1)
- Supavisor adapter + onboarding milestone + deferral lift note (section 8)
- Calibration evidence: warmup sensitivity curve, scale-100 pilot (section 7)
- Full resweep at both scales, powered repeats n>=7/10, paired seeds (section 7)
- Soak evidence (30-60 min arms: RSS/FD drift, tail drift) (section 7)
- Statistics rebuild: paired-difference bootstrap CIs, Holm correction,
  outlier rule, p90/p99 quarantine citations (section 5)
- Website rebuild: static-first index, six dossiers, `/guide/`,
  `/architecture/`, `/methodology/`, `/reproducibility/` (sections 3, 10, 12)
- Reproducibility package: manifest-hash build, pinned digests, log corpus
  with SHAs, DOI snapshot, challenge flow, errata log, verified-by table
  (sections 11, 12.2)
- Drift test (page text vs medians byte-match), Tier-1 chart tests,
  Tier-2 vision read green (sections 6, 10 step 0, 12)

## Why

M1/M2 proved the harness and CI discipline (42 + 111 medians, 469 raw,
clients>>pool verified) but the public surface still carries internal cell
IDs, pending-cell artifacts, cramped charts, skeleton dossiers, n=3-5
min-max headlines, scale-10-only short runs without resource mechanism, and
a deferred sixth contender. Any one of these fails conference rigor or HN
teardown readability. The redesign closes all of them in one autonomous
chain under the section-0 mandate: decide everything, fix everything, burn
what it takes, notify once.

## How It Works

Execution runs fully self-sufficient per plan section 0: no owner waits,
no mid-flight approval gates. Each milestone is one Builder PR (`Refs #302`)
through review/test/pages chaining autonomously to the next. CI minutes and
parallel sharding are uncapped; results commit incrementally so work is never
lost. Forced owner-click batches (held-run approvals on bot PRs, merges of
workflow-touching PRs) are the only exception and batch into a single message
with exact click paths while other tracks keep moving. Milestone order is
fixed: charter, methods, Supavisor onboarding, calibration, main matrix,
soak plus seeds, statistics rebuild, website rebuild, reproducibility
package, red-team pass. Statistics and resweep ordering is deliberate: claims
register before the matrix (no cherry-picking), calibration proves scale and
warmup before burning the matrix budget, soak/seeds run with the matrix iron
warm, CIs rebuild after all raw lands, pages render only from committed
bundles (no hand-typed values).

## Module Breakdown

- **Charter + registry + spec (M5):** IA lock (section 3, relative links,
  no CDN, Mermaid-as-text/SVG rule), `claims.md` (primary tps-without-connect
  metric, secondaries p99/p999/errors/CPU/RSS/FD, headline comparisons,
  non-goals), `spec-v1.md` skeleton (run rules, allowed/prohibited tuning,
  disclosure minimums, hardware envelope, versioning), generated-count drift
  test (step 0: generator-emitted page metadata, delete hand-typed counts).
- **Methods hardening (M6):** PG config enforcement (runner applies
  shared_buffers/max_connections/synchronous_commit/fsync or effective SHOW
  becomes the claim; divergence blocks), equalized-auth churn control arm
  beside labeled asymmetric arms, dataset policy (per-chunk init +
  CHECKPOINT + VACUUM ANALYZE rule + bloat accounting), isolation records
  (CPU pinning, fixed pgbench -j, cpuinfo/governor/kernel/nproc/topology per
  raw record), pgpool children-x-max_pool labels, budget parity via --list.
- **Supavisor onboarding (M7):** pinned version + SHA, verbatim config with
  upstream citations, identical adapter contract, equal cell budget, smoke
  gate before matrix entry, deferral doc lifted to a lift note, six-way
  taxonomy updates (titles, IA, architecture, feature matrix). Failure to
  meet contract is a published finding, never silent exclusion.
- **Calibration (M8):** warmup sensitivity curve (prove 30 s or raise it),
  scale-100 first-class pilot, per-run resource fields (CPU time, peak RSS,
  FD count, pool wait counters, pg_stat deltas; nullable for old rows),
  workload breadth (Zipf-skew select, think-time variant, multi-statement
  transaction, JSONB/COPY-adjacent write, fixed-offer -R arms), pipeline
  mode stays forbidden with written reason.
- **Main matrix resweep (M9):** full workload set at both scales, flagship
  n>=10 / standard n>=7, >=3 seeds paired across arms, wide parallel
  sharding under per-job caps, incremental result commits.
- **Soak + statistics (M10):** 30-60 min soak arms (leak/tail/stability
  figures), seed weeks for noise floor, paired bootstrap CIs (effect + CI
  first, verdict second, p last-or-omitted), Holm multiplicity, stated
  outlier/partial-success rule with retained forensics, per-repeat p99/p999
  into CI machinery, provisional candidate re-derivation with kill rule
  (CI includes zero or quarantined evidence ships as inconclusive).
- **Website rebuild (M11):** static-first master report (executive cards
  verified-only, flagship baseline 7 workload rows with plain-words titles,
  throughput beside latency, text badges, Throughput|Latency|All-Telemetry
  toggle, pre-rendered matrix blocks, 560 px linear+log ECharts twins with
  clean legends/zoom/numeric sort/off-baseline markers), six dossiers on the
  7-section-ID contract with lifecycle blueprints + full config tables +
  filters + resource-evidenced diagnostics, guide decision tree, architecture
  taxonomy (memory-per-1000-idle measured or absent), methodology
  (registry/design/discipline/manifesto/disclosure), design system
  (type/table/chart theme, dark/light/print, permalinks, BibTeX, contender
  picker, FAQ, glossary, onboarding ladder).
- **Reproducibility + red-team (M12):** manifest-hash deterministic build,
  pinned container/action digests, per-transaction log policy with sampling
  rule, corpus SHAs + size budget, DOI/license snapshot, data-availability
  statement, vendor challenge flow + errata log + verified-by table, Tier-1
  plus Tier-2 plus mobile-width green, fairness byte-match re-check, Tester
  sample-cell repro green. Only then is the single completion notification
  (tag owner, what/where/evidence/limitations) sent.

## Test Matrix

- Full unit + regression suite green, zero failures (never pin a fixed
  count in gate text).
- Chart generator integrity: exit 0, manifest SHA256 checksums match all
  generated JSONs.
- Served-HTTP contract + drift + readability suites: all pages/scripts/chart
  endpoints HTTP 200, page counts match medians, legend/zoom/sort/marker
  rules hold, Tier-2 vision read passes.
- Manual: local static server shows zero pending/loading content, formatted
  numbers with uncertainty, plain-words titles, throughput beside latency,
  clean 560 px charts with log twins; each dossier shows lifecycle diagram,
  full filterable config table, resourced diagnostics, reasoned N/A rows;
  supplementary sections show nav flow, depth, honest provisional labeling.

## Milestone Roadmap (M5-M12, all Refs #302)

- M5 charter + claims + spec skeleton + drift test (PR 1)
- M6 methods hardening: PG enforcement, equalized-auth churn, dataset
  policy, isolation records, labeling, budget parity (PR 2)
- M7 Supavisor onboarding with smoke gate + taxonomy updates (PR 3)
- M8 calibration: warmup curve, scale-100 pilot, resource fields,
  workload breadth (PR 4)
- M9 main matrix resweep both scales, powered paired repeats (PRs 5+,
  chunked commits)
- M10 soak + seeds + statistics rebuild + candidate re-derivation (PR 6)
- M11 website rebuild: report + six dossiers + four supplementary
  sections + design system (PRs 7+)
- M12 reproducibility package + red-team pass + single completion
  notification (final PR, Closes #302 only on section-11 full gate)

- the Architect
