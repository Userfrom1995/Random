"""pgbench argv builder, stdout parser, and txn-log percentile math.

Identical flags per cell; only host/port differ per arm. No per-pooler
branches. Flag set follows methodology.md section 2.
"""

import math
import os
import re

TPS_RE = re.compile(
    r"tps\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*\(without initial connection time\)")
LAT_AVG_RE = re.compile(r"latency average\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*ms")
LAT_STD_RE = re.compile(r"latency stddev\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*ms")
PROCESSED_RE = re.compile(
    r"number of transactions actually processed:\s*([0-9]+)")
FAILED_RE = re.compile(r"number of failed transactions:\s*([0-9]+)")
SKIPPED_RE = re.compile(r"number of transactions skipped:\s*([0-9]+)")

# pgbench exit codes: 0 ok, 1 setup failure, 2 mid-run SQL errors.
EXIT_MEANING = {0: "ok", 1: "setup failure", 2: "mid-run SQL errors"}

TXN_LOG_SIZE_GUARD_BYTES = 200 * 1024 * 1024


def workload_flags(cell):
    """pgbench workload flags for a cell (workload + protocol + churn)."""
    flags = []
    workload = cell["workload"]
    if workload == "select-only":
        flags.append("-S")
    elif workload == "simple-update":
        flags.append("-N")
    elif workload == "tpcb-like":
        flags.extend(["-b", "tpcb-like"])
    else:
        raise ValueError("unknown workload %r" % (workload,))
    if cell.get("protocol") == "prepared":
        flags.extend(["-M", "prepared"])
    else:
        flags.extend(["-M", "simple"])
    if cell.get("churn"):
        flags.append("-C")
    return flags


def build_argv(cell, host, port, dbname, user, threads, duration_s=None,
               log_prefix="cell", seed=42, agg_interval_s=10,
               progress_s=10, sampling_rate=None):
    """Build an identical-flags pgbench invocation for one measured run."""
    duration = duration_s if duration_s is not None else cell["duration_s"]
    argv = ["pgbench", "-h", host, "-p", str(port), "-U", user]
    argv.extend(workload_flags(cell))
    argv.extend(["-c", str(cell["clients"]), "-j", str(threads),
                 "-T", str(duration)])
    argv.extend(["-P", str(progress_s), "-l",
                 "--aggregate-interval=%d" % agg_interval_s,
                 "--log-prefix=%s" % log_prefix,
                 "--random-seed=%d" % int(seed)])
    if sampling_rate is not None:
        argv.append("--sampling-rate=%s" % sampling_rate)
    argv.append(dbname)
    return argv


def build_init_argv(pgbench_bin, host, port, dbname, user, scale):
    return [pgbench_bin or "pgbench", "-h", host, "-p", str(port),
            "-U", user, "-i", "-s", str(scale), dbname]


def parse_stdout(text):
    """Parse pgbench stdout into metrics. Raises ValueError if tps missing."""
    m = TPS_RE.search(text)
    if not m:
        raise ValueError("pgbench stdout has no tps line")
    out = {"tps": float(m.group(1))}
    m = LAT_AVG_RE.search(text)
    out["latency_avg_ms"] = float(m.group(1)) if m else None
    m = LAT_STD_RE.search(text)
    out["latency_stddev_ms"] = float(m.group(1)) if m else None
    m = PROCESSED_RE.search(text)
    out["processed"] = int(m.group(1)) if m else None
    m = FAILED_RE.search(text)
    out["failed"] = int(m.group(1)) if m else 0
    m = SKIPPED_RE.search(text)
    out["skipped"] = int(m.group(1)) if m else 0
    return out


def _quantile(sorted_vals, q):
    if not sorted_vals:
        return None
    if len(sorted_vals) == 1:
        return float(sorted_vals[0])
    pos = q * (len(sorted_vals) - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return float(sorted_vals[lo])
    frac = pos - lo
    return sorted_vals[lo] * (1.0 - frac) + sorted_vals[hi] * frac


def percentiles_from_values(values_ms):
    vals = sorted(values_ms)
    return {
        "p50_ms": _quantile(vals, 0.50),
        "p90_ms": _quantile(vals, 0.90),
        "p99_ms": _quantile(vals, 0.99),
        "p999_ms": _quantile(vals, 0.999),
    }


def parse_txn_log(path):
    """Offline p50/p90/p99/p999 from a pgbench -l per-transaction log.

    Uses the microsecond time_us column (field index 2). Skips comment
    lines and unparseable rows. Raises if the file threatens the 200 MB
    guard so callers add --sampling-rate instead of OOMing the runner.
    """
    size = os.path.getsize(path)
    if size > TXN_LOG_SIZE_GUARD_BYTES:
        raise ValueError(
            "txn log %s is %d bytes over the 200 MB guard; rerun with "
            "--sampling-rate=0.1" % (path, size))
    values_ms = []
    with open(path, "r", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            try:
                us = int(parts[2])
            except ValueError:
                continue
            if us < 0:
                continue
            values_ms.append(us / 1000.0)
    if not values_ms:
        return {"p50_ms": None, "p90_ms": None,
                "p99_ms": None, "p999_ms": None, "samples": 0}
    pct = percentiles_from_values(values_ms)
    pct["samples"] = len(values_ms)
    return pct


def failed_ratio_exceeds(parsed, processed=None):
    """True when failed transactions exceed 1% of processed (reject rule)."""
    failed = parsed.get("failed", 0) or 0
    total = parsed.get("processed") or processed
    if not total:
        return failed > 0
    return (failed / total) > 0.01


def has_prepared_statement_error(stderr_text, stdout_text=""):
    """Detect SQLSTATE 26000 (prepared statement does not exist)."""
    blob = (stderr_text or "") + "\n" + (stdout_text or "")
    return "26000" in blob or "prepared statement" in blob.lower()
