"""Odyssey adapter (M1: transaction pool, single worker).

Refs: https://pg-odyssey.tech/configuration/rules.html,
https://pg-odyssey.tech/configuration/global.html,
https://pg-odyssey.tech/features/pooling.html
"""

from .base import BaseAdapter


class OdysseyAdapter(BaseAdapter):
    NAME = "odyssey"
    BINARY = "odyssey"
    DEFAULT_PORT = 6435

    def config_text(self, cell):
        pool_size = int(cell["pool_size"])
        reserve = ("yes" if cell.get("protocol") == "prepared" else "no")
        return (
            "# Odyssey M1 baseline (transaction pool, workers = 1)\n"
            "# refs: rules.html, global.html, features/pooling.html\n"
            "workers 1\n"
            "resolvers 1\n"
            "backend_connect_timeout_ms 30000\n"
            "listen {\n"
            '  host "127.0.0.1"\n'
            "  port %d\n" % self.port +
            "}\n"
            "route {\n"
            '  service "benchdb"\n'
            '  database "benchdb"\n'
            '  user "benchuser"\n'
            '  backend_host "127.0.0.1"\n'
            "  backend_port %d\n" % self.pg_port +
            "  pool transaction\n"
            "  pool_size %d\n" % pool_size +
            "  pool_discard yes\n"
            "  pool_smart_discard no\n"
            "  pool_cancel yes\n"
            "  pool_rollback yes\n"
            "  pool_timeout 0\n"
            "  pool_ttl 0\n"
            "  server_lifetime 3600\n"
            "  pool_reserve_prepared_statement %s\n" % reserve +
            "  server_pstmt_cache_size 0\n"
            "}\n"
        )

    def setup(self, workdir, cell):
        super().setup(workdir, cell)
        self.write_file("odyssey.conf", self.config_text(cell))

    def start_argv(self, cell):
        return [self.BINARY, self.workdir + "/odyssey.conf"]
