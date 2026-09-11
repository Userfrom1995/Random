# pgpool-II baseline config (Researcher spec, Refs #302)

Reference (normative):
https://www.pgpool.net/docs/latest/en/html/runtime-config-connection-pooling.html,
https://www.pgpool.net/docs/latest/en/html/runtime-config-connection.html,
https://www.pgpool.net/docs/latest/en/html/runtime-config-load-balancing.html,
https://www.pgpool.net/docs/latest/en/html/restrictions.html

## M1/M2 baseline (session-class, the only pooling mode)

```ini
connection_cache = on
max_pool = 1
num_init_children = 100
reserved_connections = 0
listen_backlog_multiplier = 2
serialize_accept = off
child_life_time = 300
child_max_connections = 0
connection_life_time = 0
client_idle_limit = 0
reset_query_list = 'ABORT; DISCARD ALL'
load_balance_mode = off
```

Rationale cites: session-scoped caching model from the pooling page;
`num_init_children = 100` covers M1 client counts up to 100 without blocking
(scale to 200 for the 200-client row); `max_pool = 1` keeps the backend
ceiling (`children x max_pool`) inside PG `max_connections` with headroom;
`reset_query_list` default hygiene; load balancing off so the benchmark
measures pooling, not routing. For the 200-client row use
`num_init_children = 200, max_pool = 1`.

- Dr. Mob, the Researcher
