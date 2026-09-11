# Poolduel methodology (Researcher spec, Refs #302)

## 1. Question and yardstick

Which PostgreSQL connection pooler delivers the best throughput and tail
latency under real frontend fan-in (`clients >> pool_size`)? The primary
yardstick is `pgbench` TPC-B-like read-write (the industry standard for
Postgres throughput), plus SELECT-only, reconnect-per-transaction churn, and
prepared-statement traffic. References: https://www.postgresql.org/docs/17/pgbench.html,
https://www.pgpool.net/docs/latest/en/html/runtime-config-connection-pooling.html (pooling context),
https://www.pgbouncer.org/features.html (mode semantics).

## 2. Why pgbench

pgbench ships with Postgres, speaks both simple and extended protocols,
supports built-in TPC-B-like, SELECT-only, and simple-update workloads,
scales with `-s`, and reports a parseable `tps (without initial connection
time)` line plus latency averages. Percentiles come from offline analysis of
per-transaction logs (`-l`, microsecond `time_us` column), because pgbench
has no native percentile output. Aggregate-interval logs
(`--aggregate-interval`) give steady-state trimming and variance checks.
Flags used (`-b -c -C -j -l -L -M -P -r -R -S -N -t -T --aggregate-interval
--sampling-rate --log-prefix --random-seed`) are stable across PG 15/16/17/18.

## 3. Dataset and run shape

Scale `-s 10` (1M accounts, roughly 150-200 MB with indexes): satisfies the
pgbench rule that scale must meet or exceed the largest client count, fits in
CI RAM next to PG plus pooler plus pgbench, and keeps pooler overhead visible
instead of drowned in buffer-miss noise. Fresh `pgbench -i -s 10` per run,
`CHECKPOINT` before each measured run, default vacuum behavior held constant.
Warmup `-T 30` discarded, measured `-T 60` (flagship `-T 120`). Three repeats
per cell, five for flagship; median headline with min-max band and CV.
Threads `-j` equal vCPU count. Per-cell caps: 8 min standard, 12 min flagship.

## 4. Metrics

Throughput: `tps (without initial connection time)`. Latency: pgbench average
and stddev plus offline p50/p90/p99/p999 from per-transaction logs (filter
`skipped`, `failed`, serialization and deadlock markers before quantile math).
Errors: `number of failed transactions`, over-limit counts under `-L`,
skipped counts under `-R`, and exit codes (0 ok, 1 setup failure, 2 mid-run
SQL errors). Any SQLSTATE 26000 (`prepared statement does not exist`) in a
prepared twin fails that arm cell. No hidden errors; every number ships with
its full pgbench header block and exact pooler config.

## 5. Fairness discipline (structural)

One harness, identical adapter contract (same timeouts, warmup, JSON schema,
failure semantics). Same machine, same PG build and config, freshly
initialized dataset per run, same client load, interleaved round-robin order,
medians. Every non-default pooler setting cites that pooler's own tuning docs
(`docs/configs/<pooler>.md`) or fails review. Best-vs-best per workload plus
iso-region slices on shared axes (clients, backends, duration). Unsupported
cells are `N/A (unsupported)`, never zero. Peaks carry exact configs plus
surface-flatness analysis (fast everywhere versus fast at one magic setting).

## 6. Comparison logic

Headline deltas require non-overlapping min-max bands across repeats AND
same-direction agreement of tps and p99; otherwise the comparison is
`inconclusive` and the issue stays open on `Refs`, never `Closes`, for
negative or marginal results. Claims are comparative deltas inside stated
hardware envelopes only, never absolute capacity claims. Version upgrades
invalidate carried-forward numbers and trigger re-runs.

## 7. Threats to validity (mandatory in the report)

1. Co-location: PG, pooler, and pgbench share 2-4 vCPUs; pgbench itself can
   bottleneck (documented `-j` sensitivity). Results rank arms on this
   hardware only.
2. Prepared-mode incompatibility: transaction pooling breaks server-side
   prepares unless the pooler tracks them; errors are findings, not harness
   bugs; every prepared cell has a simple-protocol twin.
3. Auth and startup asymmetry: `-C` cells measure connect plus auth; reset
   queries and auth methods are held constant and logged.
4. Session-state leakage: custom scripts must stay transaction-scoped
   (`SET LOCAL`, `pg_advisory_xact_lock`); builtins already do.
5. Reset-query cost: `DISCARD ALL` style resets are part of the fair cost of
   multiplexing, held constant and reported.
6. Autovacuum and checkpoints: fixed `CHECKPOINT`, identical vacuum defaults,
   warmup trimming via aggregate-interval logs.
7. Shared-runner noise: handled by interleaving and medians, never by static
   baselines or single runs.

## 8. Reproducibility by adversary

Disclosure must let any pooler's own maintainers reproduce a cell or file a
founded objection: exact versions and SHAs, verbatim configs, full pgbench
invocations with seeds, raw logs, median math, and a one-command local repro
(`poolduel/repro.sh` plus `poolduel/README.md`). The Tester independently
reproduces at least one sample cell.

- Dr. Mob, the Researcher
