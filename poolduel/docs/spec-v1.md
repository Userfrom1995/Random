# Poolduel Benchmark Spec v1 (draft skeleton, M5)

> **Status**: draft v0.1 skeleton, to be completed in M6-M8 as methods,
> Supavisor onboarding, and calibration land. Refs #302.
> **Intent (plan section 12.1)**: the Poolduel Benchmark Spec v1.0 in
> SPEC/TPC style. Anyone with other iron must be able to run this spec
> and compare against our numbers. The report is an instance of the spec;
> the spec is what becomes the standard. Spec changes rev the version and
> re-run affected cells, never silently.

## 1. Run rules

- One harness, identical adapter contract for every contender: same
  timeouts, same warmup, same JSON schema, same failure semantics
  (`poolduel/docs/harness-contract.md`).
- Warmup discarded before every measured run (length proven by the M8
  sensitivity curve; until then the provisional 30 s with its provenance).
- Repeats: flagship cells n>=10, standard cells n>=7, at least 3 seeds,
  paired seeds across arms (M9; M1/M2 ran n=3-5 unpaired and are labeled
  as such wherever shown).
- Medians over repeats; per-repeat p99/p999 feed CI machinery at repeat
  level, never pooled raw transactions across repeats.
- Per-chunk direct control in every chunk; interleaved round-robin arm
  order.

## 2. Allowed vs prohibited tuning

- Allowed: any pooler setting that cites its upstream documentation, with
  the citation committed beside the config (`poolduel/docs/configs/`).
- Prohibited: home-team tuning without citation; sabotage by omission
  (withholding a documented setting that the contender needs to function);
  pipeline mode (forbidden with written reason: it changes protocol
  semantics rather than pooling behavior).
- Best-mode per pooler on shared load (SPEC.md, methodology.md): compare
  each contender's best documented mode on identical workload geometry,
  never identical knobs, always beside at least one iso-region slice.

## 3. Required disclosures (minimums)

- Pinned pooler versions plus SHAs; PG build; kernel, CPU model,
  frequency governor, nproc, runner topology per raw record.
- Effective `SHOW` values for `shared_buffers`, `max_connections`,
  `synchronous_commit`, `fsync` (M6: the runner applies the claimed
  baseline or the effective values become the published claim).
- Full verbatim configs with upstream citations; dataset policy
  (per-chunk init plus `CHECKPOINT` plus `VACUUM ANALYZE` rule, M6);
  isolation records (CPU pinning, fixed pgbench `-j`, M6).

## 4. Hardware envelope

- Numbers are valid for the stated iron only. Cross-hardware comparisons
  are never made; no absolute capacity claims are registered
  (`claims.md` section 4).
- CI iron is the reference platform; bare-metal reproduction follows the
  same spec with its own disclosure record.

## 5. Versioning and changelog policy

- This spec revs (`v1.0`, `v1.1`, ...) on any run-rule, metric, or
  disclosure change. Spec changes re-run affected cells, never silently.
- Report corrections land in a public errata log with date, affected
  cells, cause, and new values (M12 trust machinery).

## 6. Open items (to be closed by M6-M8)

- M6 (closed 2026-09-13): PG config enforcement wording (section 3:
  runner applies `harness/pgconf.py:apply_sql`, per-row
  `pg_config_status` enforced/disclosed/unknown with divergence list;
  disclosed divergence is a blocking defect for the fairness re-check);
  equalized-auth churn control arm defined
  (`harness/auth.py:EQUALIZED_CHURN_SPEC` M9-E1, SCRAM everywhere,
  beside labeled asymmetric arms, measured in M9); dataset policy text
  (per-chunk `pgbench -i -s 10` + `CHECKPOINT` + `VACUUM (ANALYZE)` +
  bloat accounting via `bloat_accounting_sql`); isolation record
  schema (`harness/isolate.py:collect_isolation`: cpu_model, kernel,
  nproc, governor, threads, pgbench_j pinned to threads, pinning,
  topology, per raw row, nullable for old rows).
- M7: Supavisor provisioning and smoke-gate entry criteria.
- M8: warmup sensitivity curve result; scale-100 pilot parameters;
  resource-field schema; workload breadth additions (Zipf, think-time,
  multi-statement, JSONB/COPY-adjacent, fixed-offer `-R`).
