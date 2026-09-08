"""Empirical ledger: append / check / plot over ledger/ledger.csv.

Schema (one row per model per seed per (vocab, window, slots, use_accumulator);
empty = not yet measured):
model,params,train_tokens,seed,vocab,window,slots,use_accumulator,
g1_mqar_8,g1_mqar_16,g1_mqar_64,g1_mqar_256,
g1_induction,g1_copy,g1_2hop,g2_bpb_1x,g2_bpb_4x,g2_bpb_8x,
g2_delta_4x,g2_delta_8x,g3_valid_bpb,g3_test_bpb,
g4_state_bytes,g4_ms_per_token,gpu_hours,notes

vocab is the eval/train vocab both arms shared (migrated M1 smoke rows use
the G1 vocab 256; G2/G4 smoke cells used 8192 - conflated there, pinned to
one vocab going forward). window is the p1/p2/p3/p4/p5 sliding-window W ("" for the
transformer, which has none); A2 variants share (model, seed) and are
disambiguated by window. slots is the P2 global-slot count G ("" for
non-p2 arms; "0" is the pure-SSD control); use_accumulator is the P3
accumulator flag ("True"/"False", "" for non-p3 arms). Ledger model names
are always valid --model values (p2-toy, never p2-G0-toy) so a row replays
via train.py flags plus the slots/use_accumulator columns. g1_mqar_8 holds
toy N=train-N recall; the 16/64/256 cells stay literal (toy N16 there is an
extrapolation point, and notes must say so).

check: schema lint (every row's keys against SCHEMA, no NaN/inf in filled
gate cells or params, every row carries at least one gate cell or an
explicit deferred/probe/fixture notes tag) plus the binding +-2%
param-drift rule (candidate vs transformer arm, same scale and vocab).
plot: regenerate g2 degradation + g4 latency curves from CSV only (SVG, no deps).
"""

import argparse
import csv
import json
import math
import os
import re

SCHEMA = ["model", "params", "train_tokens", "seed", "vocab", "window",
          "slots", "use_accumulator",
          "g1_mqar_8", "g1_mqar_16", "g1_mqar_64", "g1_mqar_256",
          "g1_induction", "g1_copy", "g1_2hop",
          "g2_bpb_1x", "g2_bpb_4x", "g2_bpb_8x", "g2_delta_4x", "g2_delta_8x",
          "g3_valid_bpb", "g3_test_bpb",
          "g4_state_bytes", "g4_ms_per_token", "gpu_hours", "notes"]
GATE_COLS = ["g1_mqar_8", "g1_mqar_16", "g1_mqar_64", "g1_mqar_256",
             "g1_induction", "g1_copy", "g1_2hop",
             "g2_bpb_1x", "g2_bpb_4x", "g2_bpb_8x", "g2_delta_4x", "g2_delta_8x",
             "g3_valid_bpb", "g3_test_bpb",
             "g4_state_bytes", "g4_ms_per_token"]
EMPTY_ROW_TAGS = ("defer", "pend", "todo", "probe", "fixture",
                  "not measured", "empty by design")


def _norm(v):
    return str(v if v is not None else "").strip()


def _key(r):
    # A2 window variants, A4 slot variants, and A3 accumulator variants
    # share (model, seed); the full key keeps those legitimate variants
    # distinct while catching silent dupes. Normalized: CSV rows are
    # strings but run-json values may be ints/None with whitespace, so
    # bare str() comparison leaves dedup dead for real inputs.
    return (_norm(r.get("model", "")), _norm(r.get("seed", "")),
            _norm(r.get("vocab", "")), _norm(r.get("window", "")),
            _norm(r.get("slots", "")), _norm(r.get("use_accumulator", "")))


def _validate_row(i, r):
    """Per-row lint shared by check and append. Returns list of errors."""
    errors = []
    if list(r.keys()) != SCHEMA:
        return [f"row {i} schema mismatch: {list(r.keys())} != SCHEMA"]
    for c in ("seed", "vocab", "train_tokens", "gpu_hours"):
        v = r.get(c, "")
        if v in ("", None):
            continue
        try:
            float(str(v).strip())
        except (ValueError, TypeError):
            errors.append(f"row {i} col {c}: not numeric: {v!r}")
    w = r.get("window", "")
    if w not in ("", None) and str(w).strip() != "":
        try:
            wi = int(str(w).strip())
        except (ValueError, TypeError):
            errors.append(f"row {i} col window: not an integer: {w!r}")
        else:
            if wi < 0:
                errors.append(f"row {i} col window: must be >= 0: {w!r}")
    s = r.get("slots", "")
    if s not in ("", None) and str(s).strip() != "":
        try:
            si = int(str(s).strip())
        except (ValueError, TypeError):
            errors.append(f"row {i} col slots: not an integer: {s!r}")
        else:
            if si < 0:
                errors.append(f"row {i} col slots: must be >= 0: {s!r}")
    ua = r.get("use_accumulator", "")
    if ua not in ("", None) and str(ua).strip() != "":
        if str(ua).strip().lower() not in ("true", "false", "1", "0"):
            errors.append(
                f"row {i} col use_accumulator: must be True/False or empty: {ua!r}")
    for c in GATE_COLS:
        v = r.get(c, "")
        if v in ("", None):
            continue
        try:
            x = float(str(v).strip())
        except ValueError:
            errors.append(f"row {i} col {c}: not a number: {v!r}")
            continue
        if math.isnan(x) or math.isinf(x):
            errors.append(f"row {i} col {c}: non-finite gate value: {v!r}")
        elif c.startswith("g1_") and not (0.0 <= x <= 1.0):
            errors.append(f"row {i} col {c}: accuracy {v!r} outside [0, 1]")
    pv = r.get("params", "")
    if pv not in ("", None) and str(pv).strip() != "":
        try:
            px = float(str(pv).strip())
        except ValueError:
            errors.append(f"row {i} col params: not numeric: {pv!r}")
        else:
            if math.isnan(px) or math.isinf(px):
                errors.append(f"row {i} col params: non-finite value: {pv!r}")
    if all(r.get(c, "") in ("", None) for c in GATE_COLS):
        notes = (r.get("notes") or "").lower()
        if not any(tag in notes for tag in EMPTY_ROW_TAGS):
            errors.append(
                f"row {i} ({r.get('model')}) has no gate cells and no "
                f"explicit empty-row tag in notes {EMPTY_ROW_TAGS}")
    return errors


def read_ledger(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return list(csv.DictReader(f))


def cmd_append(a):
    with open(a.run_json) as f:
        run = json.load(f)
    extra = sorted(k for k in run if k not in SCHEMA)
    if extra:
        print(f"note: ignoring extra run-json keys not in SCHEMA: {extra}")
    row = {c: run.get(c, "") for c in SCHEMA}
    rows = read_ledger(a.ledger)
    if rows and list(rows[0].keys()) != SCHEMA:
        raise SystemExit(f"schema mismatch: {list(rows[0].keys())} != SCHEMA")
    errs = _validate_row(len(rows), row)
    if errs:
        raise SystemExit("refusing to append invalid row:\n - " + "\n - ".join(errs))
    dupes = [r for r in rows if _key(r) == _key(row)]
    if dupes and not a.force:
        raise SystemExit(
            f"duplicate ledger entry for key {_key(row)}; re-appending would "
            f"silently double-count. Pass --force to upsert.")
    if dupes:
        rows = [r for r in rows if _key(r) != _key(row)]
    rows.append(row)
    os.makedirs(os.path.dirname(os.path.abspath(a.ledger)), exist_ok=True)
    with open(a.ledger, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA)
        w.writeheader()
        w.writerows(rows)
    print(f"{'upserted' if dupes else 'appended'} {row['model']} seed={row['seed']} "
          f"vocab={row['vocab']} window={row['window']} slots={row['slots']} "
          f"use_accumulator={row['use_accumulator']} to {a.ledger}")


def cmd_check(a):
    rows = read_ledger(a.ledger)
    errors = []
    if not rows:
        errors.append("ledger is empty")
    else:
        seen = set()
        for i, r in enumerate(rows):
            errors.extend(_validate_row(i, r))
            if list(r.keys()) != SCHEMA:
                continue
            if _key(r) in seen:
                errors.append(f"row {i} duplicate key {_key(r)} (append without --force)")
            seen.add(_key(r))
        # Binding +-2% param drift: candidate vs transformer arm per
        # (scale, vocab). The lm_head scales with vocab, so cross-vocab
        # rows (e.g. A6 vocab512 pilot vs vocab64 toy) must not be
        # compared against each other; only same-vocab arms are matched.
        by_scale = {}
        for r in rows:
            m = re.fullmatch(r"(p1|p2|p3|p4|p5|transformer)-(toy|tiny|small)",
                             str(r["model"]).strip())
            if not m:
                errors.append(f"row model name malformed: {r['model']!r} "
                              f"(must look like p1-tiny; curve tags such as "
                              f"p2-G0-toy are filename labels, never ledger names)")
                continue
            scale = m.group(2)
            by_scale.setdefault((scale, _norm(r.get("vocab", ""))), []).append(r)
        for (scale, vocab), group in by_scale.items():
            base = [g for g in group if g["model"].startswith("transformer-")]
            if not base:
                # No baseline at this (scale, vocab): nothing to compare,
                # so skip the drift gate; drift is enforced only when a
                # baseline exists (M4i R1 incremental state).
                print(f"note: no transformer baseline at scale {scale} "
                      f"vocab {vocab!r}; skipping drift gate there")
                continue
            try:
                bps = {float(str(g["params"]).strip()) for g in base}
            except ValueError:
                errors.append(f"scale {scale} vocab {vocab}: baseline params not numeric")
                continue
            if any(math.isnan(b) or math.isinf(b) for b in bps):
                errors.append(
                    f"scale {scale} vocab {vocab}: baseline params non-finite")
                continue
            if len(bps) > 1:
                errors.append(
                    f"scale {scale} vocab {vocab}: transformer baselines disagree "
                    f"on params: {sorted(bps)}")
                continue
            bp = bps.pop()
            for g in group:
                if g["model"].startswith("transformer-"):
                    continue
                try:
                    pv = float(str(g["params"]).strip())
                except ValueError:
                    errors.append(f"{g['model']}: params not numeric")
                    continue
                if math.isnan(pv) or math.isinf(pv):
                    errors.append(f"{g['model']}: params non-finite: {g['params']!r}")
                    continue
                if bp == 0:
                    errors.append(f"{g['model']}: baseline params are zero, drift undefined")
                    continue
                drift = abs(pv - bp) / bp
                if math.isnan(drift) or math.isinf(drift):
                    errors.append(f"{g['model']}: param drift non-finite")
                    continue
                if drift > 0.02:
                    errors.append(f"{g['model']}: param drift {drift * 100:.2f}% > 2%")
    if errors:
        print("LEDGER CHECK FAILED")
        for e in errors:
            print(f" - {e}")
        raise SystemExit(1)
    print(f"ledger OK ({len(rows)} rows)")


def svg_line(path, title, series, xlabel, ylabel):
    """series: list of (label, [(x, y)]). Minimal dependency-free SVG."""
    from xml.sax.saxutils import escape as _xml_escape
    W, H, P = 640, 360, 48
    allx = [x for _, pts in series for x, _ in pts]
    ally = [y for _, pts in series for _, y in pts
            if y == y and y not in (float("inf"), float("-inf"))]
    if not allx or not ally:
        return
    x0, x1 = min(allx), max(allx)
    y0, y1 = min(ally), max(ally)
    if x1 == x0:
        x1 = x0 + 1
    if y1 == y0:
        y1 = y0 + 1
    def sx(x):
        return P + (x - x0) / (x1 - x0) * (W - 2 * P)
    def sy(y):
        return H - P - (y - y0) / (y1 - y0) * (H - 2 * P)
    colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e"]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
             f"<text x='{W // 2}' y='20' text-anchor='middle' font-size='14'>{_xml_escape(title)}</text>",
             f"<text x='{W // 2}' y='{H - 6}' text-anchor='middle' font-size='11'>{_xml_escape(xlabel)}</text>",
             f"<text x='12' y='{H // 2}' text-anchor='middle' font-size='11' "
             f"transform='rotate(-90 12 {H // 2})'>{_xml_escape(ylabel)}</text>"]
    for i, (label, pts) in enumerate(series):
        c = colors[i % len(colors)]
        pts = [(x, y) for x, y in pts if math.isfinite(y)]
        if not pts:
            continue
        d = "M" + " L".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in pts)
        parts.append(f"<path d='{d}' fill='none' stroke='{c}' stroke-width='2'/>")
        for x, y in pts:
            parts.append(f"<circle cx='{sx(x):.1f}' cy='{sy(y):.1f}' r='3' fill='{c}'/>")
        parts.append(f"<text x='{W - P + 4}' y='{P + i * 16}' font-size='11' fill='{c}'>{_xml_escape(label)}</text>")
    parts.append("</svg>")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w") as f:
        f.write("\n".join(parts))


def read_curve_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def cmd_plot(a):
    import glob
    rows = read_ledger(a.ledger)
    curves_dir = a.curves_dir or os.path.join(os.path.dirname(os.path.abspath(a.ledger)),
                                              "curves")
    os.makedirs(a.out_dir, exist_ok=True)
    # G2 degradation from ledger rows.
    g2 = []
    for r in rows:
        try:
            if r.get("g2_bpb_1x") and r.get("g2_bpb_4x") and r.get("g2_bpb_8x"):
                g2.append((r["model"], [(1, float(r["g2_bpb_1x"])),
                                        (4, float(r["g2_bpb_4x"])),
                                        (8, float(r["g2_bpb_8x"]))]))
        except ValueError:
            continue
    if g2:
        svg_line(os.path.join(a.out_dir, "g2_degradation.svg"),
                 "G2 BPB vs length multiple", g2, "length multiple", "BPB")
    # G4 curves from g4_curve CSVs (state bytes + ms/token vs T), recursive so
    # per-milestone subdirs (smoke-*, m2-toy/) join the same scoreboard.
    g4_state, g4_ms = [], []
    for path in sorted(glob.glob(os.path.join(curves_dir, "**", "g4_curve_*.csv"),
                                 recursive=True)):
        try:
            cr = read_curve_csv(path)
        except FileNotFoundError:
            continue
        if not cr:
            continue
        label = cr[0].get("model", os.path.basename(path))
        if cr[0].get("method", "").startswith("analytic"):
            label += " (analytic bytes)"
        try:
            g4_state.append((label, [(int(r["T"]), float(r["state_bytes"])) for r in cr]))
        except (KeyError, ValueError):
            pass
        try:
            g4_ms.append((label, [(int(r["T"]), float(r["ms_per_token_median"])) for r in cr]))
        except (KeyError, ValueError):
            pass
    if g4_state:
        svg_line(os.path.join(a.out_dir, "g4_state_bytes.svg"),
                 "G4 state bytes vs T (flat = O(1))", g4_state, "T", "state bytes")
    if g4_ms:
        svg_line(os.path.join(a.out_dir, "g4_ms_per_token.svg"),
                 "G4 ms/token vs T (flat = O(1))", g4_ms, "T", "ms/token median")
    manifest = {"g2_series": len(g2), "g4_models": [label for label, _ in g4_state],
                "note": "G4 flatness is judged on g4_curve CSVs (state bytes + ms/token vs T)"}
    with open(os.path.join(a.out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
    print(f"plot: wrote {a.out_dir}/manifest.json "
          f"({len(g2)} G2 series, {len(g4_state)} G4 models)")


def main(argv=None):
    p = argparse.ArgumentParser(description="PostFormer empirical ledger")
    sub = p.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("append")
    q.add_argument("--run-json", required=True)
    q.add_argument("--ledger", required=True)
    q.add_argument("--force", action="store_true",
                   help="upsert: replace the existing row with the same "
                        "(model, seed, vocab, window, slots, use_accumulator) "
                        "key instead of failing")
    q.set_defaults(fn=cmd_append)
    q = sub.add_parser("check")
    q.add_argument("--ledger", required=True)
    q.set_defaults(fn=cmd_check)
    q = sub.add_parser("plot")
    q.add_argument("--ledger", required=True)
    q.add_argument("--out-dir", required=True)
    q.add_argument("--curves-dir", default=None)
    q.set_defaults(fn=cmd_plot)
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
