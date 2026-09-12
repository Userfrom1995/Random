# pgagroal baseline config (Researcher spec, Refs #302)

Reference (normative for every non-default value):
https://pgagroal.github.io/doc/CONFIGURATION.html,
https://pgagroal.github.io/doc/PIPELINES.html,
https://pgagroal.github.io/doc/ARCHITECTURE.html,
https://pgagroal.github.io/doc/manual/en/15-performance.html

## M1 baseline (transaction pipeline)

```ini
[pgagroal]
host = 127.0.0.1
port = 6432
unix_socket_dir = /tmp
max_connections = 10
pipeline = transaction
ev_backend = auto
blocking_timeout = 0
idle_timeout = 0
max_connection_age = 0
validation = off
track_prepared_statements = off
nodelay = on
keep_alive = on
allow_unknown_users = true
log_type = console
log_level = info
```

Per-database pool (`pgagroal_databases.conf`): `benchdb benchuser 10`.
Backend server section (mandatory per CONFIGURATION.html - sections other
than `[pgagroal]` each configure one PostgreSQL backend):

```ini
[primary]
host = 127.0.0.1
port = 5432
primary = on
```

HBA (`pgagroal_hba.conf`): `host benchdb benchuser 127.0.0.1/32 scram-sha-256`
(CI-only; production would use per-user vault entries). The scram method
makes the pooler collect the client password (CI `PGPASSWORD=benchpass`)
so `benchuser` authenticates against PostgreSQL itself via the
`allow_unknown_users` passthrough (CONFIGURATION.html); `trust` cannot be
used because the pooler would then hold no password for the SCRAM backend.
Startup: `pgagroal -c pgagroal.conf -a pgagroal_hba.conf -l
pgagroal_databases.conf` in the foreground (`-d` is a daemon flag taking
no argument).
Rationale cites: transaction-mode advice (`blocking_timeout = 0`,
`idle_timeout = 0`, `max_connection_age = 0`) from PIPELINES; `ev_backend`
choices from ARCHITECTURE.

## M2 variants

- Session arm: `pipeline = session`, `blocking_timeout = 30s`.
- Performance arm: `pipeline = performance`, `blocking_timeout = 30s`.
- I/O axis: `ev_backend = io_uring` versus `epoll` (record resolved `auto`).
- Prepared twin: `track_prepared_statements = on` (transaction only).

- Dr. Mob, the Researcher
