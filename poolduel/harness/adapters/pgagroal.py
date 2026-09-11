"""pgagroal adapter (M1: transaction pipeline).

Refs: https://pgagroal.github.io/doc/CONFIGURATION.html,
https://pgagroal.github.io/doc/PIPELINES.html,
https://pgagroal.github.io/doc/ARCHITECTURE.html
"""

from .base import BaseAdapter


class PgAgroalAdapter(BaseAdapter):
    NAME = "pgagroal"
    BINARY = "pgagroal"
    DEFAULT_PORT = 6432

    def config_text(self, cell):
        pool_size = int(cell["pool_size"])
        track = "on" if cell.get("protocol") == "prepared" else "off"
        return (
            "# pgagroal M1 baseline (transaction pipeline)\n"
            "# refs: CONFIGURATION.html, PIPELINES.html, ARCHITECTURE.html\n"
            "[pgagroal]\n"
            "host = 127.0.0.1\n"
            "port = %d\n" % self.port +
            "unix_socket_dir = /tmp\n"
            "max_connections = %d\n" % pool_size +
            "pipeline = transaction\n"
            "ev_backend = auto\n"
            "blocking_timeout = 0\n"
            "idle_timeout = 0\n"
            "max_connection_age = 0\n"
            "validation = off\n"
            "track_prepared_statements = %s\n" % track +
            "nodelay = on\n"
            "keep_alive = on\n"
            "allow_unknown_users = true\n"
            "log_type = console\n"
            "log_level = info\n"
            "# per-db pool (pgagroal_databases.conf): benchdb benchuser %d\n" % pool_size +
            "# HBA (pgagroal_hba.conf, CI-only trust): "
            "host benchdb benchuser 127.0.0.1/32 trust\n"
        )

    def setup(self, workdir, cell):
        super().setup(workdir, cell)
        pool_size = int(cell["pool_size"])
        self.write_file("pgagroal.conf", self.config_text(cell))
        self.write_file("pgagroal_databases.conf",
                        "benchdb benchuser %d\n" % pool_size)
        self.write_file("pgagroal_hba.conf",
                        "host benchdb benchuser 127.0.0.1/32 trust\n")

    def start_argv(self, cell):
        return [self.BINARY, "-c",
                self.workdir + "/pgagroal.conf", "-H",
                self.workdir + "/pgagroal_hba.conf", "-d",
                self.workdir + "/pgagroal_databases.conf", "-f"]
