"""PgBouncer adapter (M1: transaction pool_mode).

Refs: https://www.pgbouncer.org/config.html,
https://www.pgbouncer.org/features.html, https://www.pgbouncer.org/faq.html
"""

from .base import BaseAdapter


class PgBouncerAdapter(BaseAdapter):
    NAME = "pgbouncer"
    BINARY = "pgbouncer"
    DEFAULT_PORT = 6433

    def config_text(self, cell):
        pool_size = int(cell["pool_size"])
        max_prepared = 200 if cell.get("protocol") == "prepared" else 0
        return (
            "# PgBouncer M1 baseline (transaction mode)\n"
            "# refs: config.html, features.html, faq.html\n"
            "[pgbouncer]\n"
            "listen_addr = 127.0.0.1\n"
            "listen_port = %d\n" % self.port +
            "pool_mode = transaction\n"
            "default_pool_size = %d\n" % pool_size +
            "max_client_conn = 500\n"
            "min_pool_size = 0\n"
            "reserve_pool_size = 0\n"
            "reserve_pool_timeout = 5.0\n"
            "server_reset_query = DISCARD ALL\n"
            "server_lifetime = 3600.0\n"
            "server_idle_timeout = 600.0\n"
            "query_wait_timeout = 120.0\n"
            "max_prepared_statements = %d\n" % max_prepared +
            "\n[databases]\n"
            "benchdb = host=127.0.0.1 port=%d dbname=benchdb\n" % self.pg_port
        )

    def setup(self, workdir, cell):
        super().setup(workdir, cell)
        self.write_file("pgbouncer.ini", self.config_text(cell))

    def start_argv(self, cell):
        return [self.BINARY, self.workdir + "/pgbouncer.ini"]
