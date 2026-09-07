"""Empirical ledger: append / check / plot over ledger/ledger.csv.

Schema (one row per model per seed per (vocab, window); empty = not yet measured):
model,params,train_tokens,seed,vocab,window,
g1_mqar_8,g1_mqar_16,g1_mqar_64,g1_mqar_256,
g1_induction,g1_copy,g1_2hop,g2_bpb_1x,g2_bpb_4x,g2_bpb_8x,
g2_delta_4x,g2_delta_8x,g3_valid_bpb,g3_test_bpb,
g4_state_bytes,g4_ms_per_token,gpu_hours,notes

vocab is the eval/train vocab both arms shared (migrated M1 smoke rows use
the G1 vocab 256; G2/G4 smoke cells used 8192 - conflated there, pinned to
one vocab going forward). window is the p1/p5 sliding-window W ("" for the
transformer, which has none); A2 variants share (model, seed) and are
disambiguated by window. g1_mqar_8 holds toy N=train-N recall; the
16/64/256 cells stay literal (toy N16 there is an extrapolation point, and
notes must say so).

check: schema lint (every row's keys against SCHEMA, no NaN in filled gate
cells, every row carries at least one gate cell or an explicit
deferred/probe/fixture notes tag) plus the binding +-2% param-drift rule
(candidate vs transformer arm, same scale).
plot: regenerate g2 degradation + g4 latency curves from CSV only (SVG, no deps).
"""

import argparse
import csv
import json
import math
import os

SCHEMA = ["model", "params", "train_tokens", "seed", "vocab", "window",
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


def _key(r):
    # A2 window variants and vocab pins share (model, seed); the full key
    # keeps those legitimate variants distinct while catching silent dupes.
    return (r.get("model", ""), r.get("seed", ""),
            r.get("vocab", ""), r.get("window", ""))


def read_ledger(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return list(csv.DictReader(f))


def cmd_append(a):
    with open(a.run_json) as f:
        run = json.load(f)
    row = {c: run.get(c, "") for c in SCHEMA}
    rows = read_ledger(a.ledger)
    if rows and list(rows[0].keys()) != SCHEMA:
        raise SystemExit(f"schema mismatch: {list(rows[0].keys())} != SCHEMA")
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
          f"vocab={row['vocab']} window={row['window']} to {a.ledger}")


def cmd_check(a):
    rows = read_ledger(a.ledger)
    errors = []
    if not rows:
        errors.append("ledger is empty")
    else:
        seen = set()
        for i, r in enumerate(rows):
            if list(r.keys()) != SCHEMA:
                errors.append(f"row {i} schema mismatch: {list(r.keys())} != SCHEMA")
                continue
            if _key(r) in seen:
                errors.append(f"row {i} duplicate key {_key(r)} (append without --force)")
            seen.add(_key(r))
            for c in GATE_COLS:
                v = r.get(c, "")
                if v in ("", None):
                    continue
                try:
                    x = float(v)
                except ValueError:
                    errors.append(f"row {i} col {c}: not a number: {v!r}")
                    continue
                if math.isnan(x):
                    errors.append(f"row {i} col {c}: NaN gate value")
            if all(r.get(c, "") in ("", None) for c in GATE_COLS):
                notes = (r.get("notes") or "").lower()
                if not any(tag in notes for tag in EMPTY_ROW_TAGS):
                    errors.append(
                        f"row {i} ({r.get('model')}) has no gate cells and no "
                        f"explicit empty-row tag in notes {EMPTY_ROW_TAGS}")
        # Binding +-2% param drift: candidate vs transformer arm per scale.
        by_scale = {}
        for r in rows:
            if "-" not in r["model"]:
                errors.append(f"row model name malformed: {r['model']!r}")
                continue
            scale = r["model"].rsplit("-", 1)[1]
            by_scale.setdefault(scale, []).append(r)
        for scale, group in by_scale.items():
            base = [g for g in group if g["model"].startswith("transformer-")]
            if not base:
                continue
            try:
                bp = float(base[0]["params"])
            except ValueError:
                errors.append(f"scale {scale}: baseline params not numeric")
                continue
            for g in group:
                if g["model"].startswith("transformer-"):
                    continue
                try:
                    drift = abs(float(g["params"]) - bp) / bp
                except ValueError:
                    errors.append(f"{g['model']}: params not numeric")
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
    W, H, P = 640, 360, 48
    allx = [x for _, pts in series for x, _ in pts]
    ally = [y for _, pts in series for _, y in pts if y == y]
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
             f"<text x='{W // 2}' y='20' text-anchor='middle' font-size='14'>{title}</text>",
             f"<text x='{W // 2}' y='{H - 6}' text-anchor='middle' font-size='11'>{xlabel}</text>",
             f"<text x='12' y='{H // 2}' text-anchor='middle' font-size='11' "
             f"transform='rotate(-90 12 {H // 2})'>{ylabel}</text>"]
    for i, (label, pts) in enumerate(series):
        c = colors[i % len(colors)]
        d = "M" + " L".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in pts)
        parts.append(f"<path d='{d}' fill='none' stroke='{c}' stroke-width='2'/>")
        for x, y in pts:
            parts.append(f"<circle cx='{sx(x):.1f}' cy='{sy(y):.1f}' r='3' fill='{c}'/>")
        parts.append(f"<text x='{W - P + 4}' y='{P + i * 16}' font-size='11' fill='{c}'>{label}</text>")
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
                        "(model, seed, vocab, window) key instead of failing")
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
