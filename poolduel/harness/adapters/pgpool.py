"""pgpool-II adapter (M1/M2: session-class, the only pooling mode).

Refs: https://www.pgpool.net/docs/latest/en/html/runtime-config-connection-pooling.html,
https://www.pgpool.net/docs/latest/en/html/runtime-config-connection.html
"""

from .base import BaseAdapter


class PgPoolAdapter(BaseAdapter):
    NAME = "pgpool"
    BINARY = "pgpool"
    DEFAULT_PORT = 6434

    PG_MAX_CONNECTIONS = 300

    def num_children(self, cell):
        return 200 if int(cell["clients"]) > 100 else 100

    def max_pool(self, cell):
        children = self.num_children(cell)
        if children * 4 <= self.PG_MAX_CONNECTIONS - 20:
            return 4
        return 1

    def effective_backends(self, cell):
        return self.num_children(cell) * self.max_pool(cell)

    def config_text(self, cell):
        return (
            "# pgpool-II M1 baseline (session-class, the only pooling mode)\n"
            "# refs: runtime-config-connection-pooling.html, "
            "runtime-config-connection.html\n"
            "listen_addresses = '127.0.0.1'\n"
            "port = %d\n" % self.port +
            "backend_hostname0 = '127.0.0.1'\n"
            "backend_port0 = %d\n" % self.pg_port +
            "connection_cache = on\n"
            "max_pool = %d\n" % self.max_pool(cell) +
            "num_init_children = %d\n" % self.num_children(cell) +
            "reserved_connections = 0\n"
            "listen_backlog_multiplier = 2\n"
            "serialize_accept = off\n"
            "child_life_time = 300\n"
            "child_max_connections = 0\n"
            "connection_life_time = 0\n"
            "client_idle_limit = 0\n"
            "reset_query_list = 'ABORT; DISCARD ALL'\n"
            "load_balance_mode = off\n"
            "# effective backends (children x max_pool) = %d\n"
            % self.effective_backends(cell)
        )

    def setup(self, workdir, cell):
        super().setup(workdir, cell)
        self.write_file("pgpool.conf", self.config_text(cell))

    def start_argv(self, cell):
        return [self.BINARY, "-f", self.workdir + "/pgpool.conf", "-n"]
