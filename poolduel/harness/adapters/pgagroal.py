"""pgagroal adapter (M1: transaction pipeline; M2: session/performance + I/O).

Refs: https://pgagroal.github.io/doc/CONFIGURATION.html,
https://pgagroal.github.io/doc/PIPELINES.html,
https://pgagroal.github.io/doc/ARCHITECTURE.html

M2 variants come from the cell's ``variant`` dict (grid.md section 1):
``pipeline`` in {transaction, session, performance} (default transaction,
the M1 arm; ``auto`` is never benchmarked, modes.md section 1) and
``ev_backend`` in {auto, io_uring, epoll} (default auto, the M1 arm).
Cells without a variant render the M1 baseline byte-identically.
"""

from .base import BaseAdapter


class PgAgroalAdapter(BaseAdapter):
    NAME = "pgagroal"
    BINARY = "pgagroal"
    DEFAULT_PORT = 6432

    PIPELINES = ("transaction", "session", "performance")
    EV_BACKENDS = ("auto", "io_uring", "epoll")

    def variant(self, cell):
        return dict(cell.get("variant") or {})

    def pipeline(self, cell):
        pipe = self.variant(cell).get("pipeline", "transaction")
        if pipe not in self.PIPELINES:
            raise ValueError("pgagroal: unknown pipeline %r" % (pipe,))
        return pipe

    def ev_backend(self, cell):
        ev = self.variant(cell).get("ev_backend", "auto")
        if ev not in self.EV_BACKENDS:
            raise ValueError("pgagroal: unknown ev_backend %r" % (ev,))
        return ev

    def config_text(self, cell):
        pool_size = int(cell["pool_size"])
        pipe = self.pipeline(cell)
        ev = self.ev_backend(cell)
        track = "on" if cell.get("protocol") == "prepared" else "off"
        # grid.md: blocking_timeout 0 in transaction mode, 30s in sessions.
        blocking = "0" if pipe == "transaction" else "30s"
        label = ("M1 baseline (transaction pipeline)" if pipe == "transaction"
                  and ev == "auto"
                  else "M2 variant (pipeline=%s, ev_backend=%s)" % (pipe, ev))
        return (
            "# pgagroal %s\n" % label +
            "# refs: CONFIGURATION.html, PIPELINES.html, ARCHITECTURE.html\n"
            "[pgagroal]\n"
            "host = 127.0.0.1\n"
            "port = %d\n" % self.port +
            "unix_socket_dir = /tmp\n"
            "max_connections = %d\n" % pool_size +
            "pipeline = %s\n" % pipe +
            "ev_backend = %s\n" % ev +
            "blocking_timeout = %s\n" % blocking +
            "idle_timeout = 0\n"
            "max_connection_age = 0\n"
            "validation = off\n"
            "track_prepared_statements = %s\n" % track +
            "nodelay = on\n"
            "keep_alive = on\n"
            "allow_unknown_users = true\n"
            "log_type = console\n"
            "log_level = info\n"
            "# backend server section (CONFIGURATION.html: sections other\n"
            "# than [pgagroal] each configure one PostgreSQL backend;\n"
            "# without one the pooler has no server to pool)\n"
            "[primary]\n"
            "host = 127.0.0.1\n"
            "port = %d\n" % self.pg_port +
            "primary = on\n"
            "# per-db pool (pgagroal_databases.conf): benchdb benchuser %d\n" % pool_size +
            "# HBA (pgagroal_hba.conf, CI-only): scram-sha-256 so the\n"
            "# client password (PGPASSWORD=benchpass in CI) is collected\n"
            "# and benchuser authenticates against PostgreSQL itself\n"
            "# (allow_unknown_users passthrough, CONFIGURATION.html).\n"
        )

    def hba_text(self):
        return "host benchdb benchuser 127.0.0.1/32 scram-sha-256\n"

    def setup(self, workdir, cell):
        super().setup(workdir, cell)
        pool_size = int(cell["pool_size"])
        self.write_file("pgagroal.conf", self.config_text(cell))
        self.write_file("pgagroal_databases.conf",
                        "benchdb benchuser %d\n" % pool_size)
        self.write_file("pgagroal_hba.conf", self.hba_text())

    def start_argv(self, cell):
        # Flags per pgagroal CLI: -c config, -a HBA, -l limit/databases
        # file; -d is a daemon flag taking no argument. Foreground run.
        return [self.BINARY, "-c",
                self.workdir + "/pgagroal.conf", "-a",
                self.workdir + "/pgagroal_hba.conf", "-l",
                self.workdir + "/pgagroal_databases.conf"]
