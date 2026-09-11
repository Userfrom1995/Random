# Supavisor deferral (Researcher spec, Refs #302)

Status: DEFERRED with reason. Supavisor is not silently dropped and not
judged on capability. It is excluded from the M1/M2 matrix because a fair
standalone CI harness for it costs a dedicated milestone the current pipeline
cannot absorb without delaying all five measured poolers.

## Factual basis (each point cites upstream docs)

1. No single binary; Elixir/OTP Mix release. Build and run need Mix or the OTP
   release image plus a Rust toolchain for the `pgparser` NIF
   (`rustler ~> 0.34`, `native/pgparser` wrapping `libpg_query`).
   See https://github.com/supabase/supavisor/blob/main/mix.exs
2. Mandatory second Postgres (metadata DB): `DATABASE_URL`, `DB_POOL_SIZE`,
   `supavisor` schema, `tenants` and `users` tables, migrations before the
   first proxied connection.
   See https://supabase.github.io/supavisor/configuration/env/,
   https://supabase.github.io/supavisor/development/installation/
3. Config via authenticated Management REST API, not a config file: every
   matrix cell needs `PUT /api/tenants/:id` with a JWT signed by
   `API_JWT_SECRET` (`SECRET_KEY_BASE` required in prod, `VAULT_ENC_KEY`
   exactly 32 bytes). Client usernames are rewritten `user.tenant`.
   See https://supabase.github.io/supavisor/development/setup/
4. Auth model assumes Supabase-style credential plumbing (`require_user`,
   per-user rows, or `is_manager` plus `auth_query` against `pg_authid`),
   which needs elevated DB privileges in a throwaway CI database.
   See https://supabase.github.io/supavisor/connecting/authentication/
5. Clustering assumptions leak into single-node runs (`libcluster`,
   `DNS_POLL`, `CLUSTER_NODES`, `RELEASE_COOKIE`, `NODE_IP`).
   See https://supabase.github.io/supavisor/faq/
6. Contrast: pgcat is `cargo build --release` plus one `pgcat.toml`, trivially
   scriptable in CI.
   See https://github.com/postgresml/pgcat/blob/main/CONFIG.md

## What deferral means

- M1 through M3 measure five poolers plus the direct control. No Supavisor
  numbers appear, and no placeholder zeros appear either.
- A future milestone provisions a Supavisor harness (metadata-DB fixture,
  tenant-provisioning script, OTP-release image pinned at v2.9.13, both
  `NAMED_PREPARED_STATEMENTS_ENABLED` settings) and then runs the same
  matrix procedure. Re-entry requires that harness plus a Researcher addendum.
- Supavisor modes for that future work: `transaction` (6543), `session`
  (5432), `native` (passthrough). See
  https://supabase.github.io/supavisor/configuration/pool_modes/

- Dr. Mob, the Researcher
