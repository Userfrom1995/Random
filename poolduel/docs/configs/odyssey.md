# Odyssey baseline config (Researcher spec, Refs #302)

Reference (normative): https://pg-odyssey.tech/configuration/rules.html,
https://pg-odyssey.tech/configuration/global.html,
https://pg-odyssey.tech/features/pooling.html

## M1 baseline (transaction pool, single worker)

Global: `workers = 1`, `resolvers = 1`,
`backend_connect_timeout_ms = 30000`.

Route:

```ini
pool = transaction
pool_size = 10
pool_discard = yes
pool_smart_discard = no
pool_cancel = yes
pool_rollback = yes
pool_timeout = 0
pool_ttl = 0
server_lifetime = 3600
pool_reserve_prepared_statement = no
server_pstmt_cache_size = 0
```

Rationale cites: mode semantics from the pooling feature page; every
`pool_*` default from the rules reference; `workers` from the global
reference.

## M2 variants

- Session arm: `pool = session`.
- Statement arm (provisional): `pool = statement`, behavior verified
  empirically and labeled provisional.
- Prepared twin: `pool_reserve_prepared_statement = yes`.
- Worker axis: `workers` in {1, 2, 4}.

- Dr. Mob, the Researcher
