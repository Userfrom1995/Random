"""pgcat adapter (M1: transaction pool_mode; M2: session + worker_threads).

Refs: https://github.com/postgresml/pgcat/blob/main/CONFIG.md,
https://github.com/postgresml/pgcat/blob/main/README.md

M2 variants from the cell's ``variant`` dict (grid.md section 5):
``pool_mode`` in {transaction, session} (default transaction; statement is
declared but documented UNSUPPORTED, modes.md section 5, so the harness
never renders it) and ``worker_threads`` in {1, 5} (default 5, the M1 arm).
Cells without a variant render the M1 baseline byte-identically.
"""

from .base import BaseAdapter


class PgCatAdapter(BaseAdapter):
    NAME = "pgcat"
    BINARY = "pgcat"
    DEFAULT_PORT = 6436

    POOL_MODES = ("transaction", "session")

    def variant(self, cell):
        return dict(cell.get("variant") or {})

    def pool_mode(self, cell):
        mode = self.variant(cell).get("pool_mode", "transaction")
        if mode not in self.POOL_MODES:
            raise ValueError(
                "pgcat: pool_mode %r unsupported (statement is N/A)" % (mode,))
        return mode

    def worker_threads(self, cell):
        threads = int(self.variant(cell).get("worker_threads", 5))
        if threads not in (1, 5):
            raise ValueError("pgcat: worker_threads must be 1 or 5")
        return threads

    def config_text(self, cell):
        pool_size = int(cell["pool_size"])
        mode = self.pool_mode(cell)
        threads = self.worker_threads(cell)
        label = ("M1 baseline (transaction mode, file: pgcat.toml)"
                 if mode == "transaction" and threads == 5
                 else "M2 variant (pool_mode=%s, worker_threads=%d)"
                 % (mode, threads))
        return (
            "# pgcat %s\n" % label +
            "# refs: CONFIG.md, README.md\n"
            "[general]\n"
            'host = "0.0.0.0"\n'
            "port = %d\n" % self.port +
            "connect_timeout = 1000\n"
            "idle_timeout = 30000\n"
            "server_lifetime = 86400000\n"
            "worker_threads = %d\n" % threads +
            "\n[pools.benchdb]\n"
            'pool_mode = "%s"\n' % mode +
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
