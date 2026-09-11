"""pgcat adapter (M1: transaction pool_mode, worker_threads = 5).

Refs: https://github.com/postgresml/pgcat/blob/main/CONFIG.md,
https://github.com/postgresml/pgcat/blob/main/README.md
"""

from .base import BaseAdapter


class PgCatAdapter(BaseAdapter):
    NAME = "pgcat"
    BINARY = "pgcat"
    DEFAULT_PORT = 6436

    def config_text(self, cell):
        pool_size = int(cell["pool_size"])
        return (
            "# pgcat M1 baseline (transaction mode, file: pgcat.toml)\n"
            "# refs: CONFIG.md, README.md\n"
            "[general]\n"
            'host = "0.0.0.0"\n'
            "port = %d\n" % self.port +
            "connect_timeout = 1000\n"
            "idle_timeout = 30000\n"
            "server_lifetime = 86400000\n"
            "worker_threads = 5\n"
            "\n[pools.benchdb]\n"
            'pool_mode = "transaction"\n'
            'load_balancing_mode = "random"\n'
            'default_role = "any"\n'
            "query_parser_enabled = true\n"
            "primary_reads_enabled = true\n"
            "prepared_statements_cache_size = 0\n"
            "\n[pools.benchdb.users.0]\n"
            'username = "benchuser"\n'
            'password = "benchpass"\n'
            "pool_size = %d\n" % pool_size
        )

    def setup(self, workdir, cell):
        super().setup(workdir, cell)
        self.write_file("pgcat.toml", self.config_text(cell))

    def start_argv(self, cell):
        return [self.BINARY, self.workdir + "/pgcat.toml"]
