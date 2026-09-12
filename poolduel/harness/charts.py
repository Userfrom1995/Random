"""Poolduel M4 chart generator: bundles in, ECharts option JSON out.

Reads the committed ``results/m1/medians.json`` + ``results/m2/medians.json``
+ ``results/report.json`` and writes one ECharts option file per page under
``results/charts/`` plus a ``manifest.json`` with the source SHAs.

Every number in the emitted options comes from the input bundles; no
hand-typed chart values exist anywhere (Tier-1 ``test_charts`` re-runs this
module on fixtures and deep-equals the committed JSON shape).

Conventions (owner-ordered, blueprint-pinned):
- ECharts 5.5.1 vendored at ``poolduel/vendor/``; pages render with the SVG
  renderer only via ``poolduel/assets/poolduel-charts.js``.
- Shared Okabe-Ito palette, one color per pooler on every page.
- yAxis min is 0 (no truncated axes); a zoomed view is only ever offered
  through dataZoom on top of the full-range axis.
- N/A and timeout cells are explicit marker points, never gap-filled with
  zeros and never interpolated.
- Min-max bands are ``line`` series named ``"<pooler> min"`` /
  ``"<pooler> max"`` (JSON-serializable error bands; ``custom`` series
  would need a JS renderItem function that cannot live in JSON).
- Every figure carries markers, axis tooltips with exact values plus cell
  id, dataZoom + legend toggles, and ``toolbox.saveAsImage`` PNG export.

Stdlib only. No interactive prompts; everything via flags.
"""

import argparse
import copy
import hashlib
import json
import os
import sys

PALETTE = {
    "pgagroal": "#D55E00",
    "pgbouncer": "#56B4E9",
    "pgpool": "#E69F00",
    "odyssey": "#009E73",
    "pgcat": "#CC79A7",
    "direct": "#9AA7B4",
}

NA_COLOR = "#484F58"
TIMEOUT_COLOR = "#D29922"

DISPLAY = {
    "direct": "direct",
    "pgagroal": "pgagroal",
    "pgbouncer": "PgBouncer",
    "pgpool": "pgpool-II",
    "odyssey": "Odyssey",
    "pgcat": "pgcat",
}

# Fixed pooler rotation used for series order, page order, and prev/next
# nav on the per-pooler pages.
POOLERS = ["direct", "pgagroal", "pgbouncer", "pgpool", "odyssey", "pgcat"]
PAGE_POOLERS = ["pgagroal", "pgbouncer", "pgpool", "odyssey", "pgcat"]

TEXT_COLOR = "#E6EDF3"
GRID_BG = "#161B22"


def _median(entry):
    tps = (entry or {}).get("tps") or {}
    return tps.get("median")


def _band(entry):
    tps = (entry or {}).get("tps") or {}
    return tps.get("min"), tps.get("max")


def _base_option(title, subtitle, x_labels, y_name="tps"):
    return {
        "backgroundColor": "transparent",
        "textStyle": {"color": TEXT_COLOR},
        "title": {"text": title, "subtext": subtitle,
                  "left": "center", "textStyle": {"color": TEXT_COLOR}},
        "tooltip": {"trigger": "axis",
                    "axisPointer": {"type": "shadow"}},
        "legend": {"top": "bottom", "textStyle": {"color": TEXT_COLOR}},
        "toolbox": {"feature": {"saveAsImage": {"title": "Save PNG"}}},
        "dataZoom": [{"type": "slider"}, {"type": "inside"}],
        "grid": {"left": "8%", "right": "6%", "bottom": "18%",
                 "containLabel": True},
        "xAxis": {"type": "category", "data": list(x_labels),
                  "name": "cell",
                  "axisLabel": {"color": TEXT_COLOR, "rotate": 30}},
        "yAxis": {"type": "value", "min": 0, "name": y_name,
                  "axisLabel": {"color": TEXT_COLOR}},
        "series": [],
    }


def _bar_series(pooler, medians, na_idx, timeout_idx):
    """Bar series of medians; null where the cell is N/A or timeout.

    ``na_idx``/``timeout_idx`` are x positions covered by the explicit
    marker series so the gap is never mistaken for zero.
    """
    _ = (na_idx, timeout_idx)
    return {
        "name": DISPLAY[pooler],
        "type": "bar",
        "itemStyle": {"color": PALETTE[pooler]},
        "emphasis": {"focus": "series"},
        "data": list(medians),
    }


def _band_series(pooler, mins, maxs):
    color = PALETTE[pooler]
    return [
        {"name": DISPLAY[pooler] + " min", "type": "line",
         "symbol": "circle", "showSymbol": True, "symbolSize": 6,
         "lineStyle": {"type": "dashed", "color": color},
         "itemStyle": {"color": color},
         "data": list(mins)},
        {"name": DISPLAY[pooler] + " max", "type": "line",
         "symbol": "circle", "showSymbol": True, "symbolSize": 6,
         "lineStyle": {"type": "dashed", "color": color},
         "itemStyle": {"color": color},
         "data": list(maxs)},
    ]


def _marker_series(name, positions, color, symbol):
    return {
        "name": name,
        "type": "scatter",
        "symbol": symbol,
        "symbolSize": 14,
        "itemStyle": {"color": color},
        "label": {"show": True, "formatter": name, "color": color},
        "data": [[pos, 0] for pos in positions],
    }


def _index_maps(entries):
    """Map (cell_id, pooler) -> entry for fast lookup."""
    return {(e["cell_id"], e["pooler"]): e for e in entries}


def comparison_m1_chart(m1_entries):
    cells = sorted({e["cell_id"] for e in m1_entries})
    by_key = _index_maps(m1_entries)
    opt = _base_option(
        "M1 best-vs-best per workload",
        "median tps with min-max bands; N/A and timeout cells marked, never zero-filled",
        [])
    opt["xAxis"]["data"] = list(cells)
    na_pos, timeout_pos = [], []
    for pooler in POOLERS:
        meds, mins, maxs = [], [], []
        for i, cell in enumerate(cells):
            entry = by_key.get((cell, pooler))
            if entry is None:
                meds.append(None)
                mins.append(None)
                maxs.append(None)
            elif entry.get("status") == "measured":
                meds.append(_median(entry))
                lo, hi = _band(entry)
                mins.append(lo)
                maxs.append(hi)
            elif entry.get("status") == "N/A (unsupported)":
                meds.append(None)
                mins.append(None)
                maxs.append(None)
                na_pos.append(i)
            else:
                meds.append(None)
                mins.append(None)
                maxs.append(None)
                timeout_pos.append(i)
        opt["series"].append(_bar_series(pooler, meds, na_pos, timeout_pos))
        opt["series"].extend(_band_series(pooler, mins, maxs))
    if na_pos:
        opt["series"].append(
            _marker_series("N/A (unsupported)", sorted(set(na_pos)),
                           NA_COLOR, "cross"))
    if timeout_pos:
        opt["series"].append(
            _marker_series("timeout/inconclusive", sorted(set(timeout_pos)),
                           TIMEOUT_COLOR, "triangle"))
    return opt


def _m2_block_chart(m2_entries, prefix, title):
    cells = sorted({e["cell_id"] for e in m2_entries
                    if e["cell_id"].startswith(prefix)})
    if not cells:
        return None
    by_key = _index_maps(m2_entries)
    opt = _base_option(title, "median tps with min-max bands; prefix " + prefix, [])
    opt["xAxis"]["data"] = list(cells)
    na_pos, timeout_pos = [], []
    for pooler in POOLERS:
        meds, mins, maxs = [], [], []
        for i, cell in enumerate(cells):
            entry = by_key.get((cell, pooler))
            if entry is None:
                meds.append(None)
                mins.append(None)
                maxs.append(None)
            elif entry.get("status") == "measured":
                meds.append(_median(entry))
                lo, hi = _band(entry)
                mins.append(lo)
                maxs.append(hi)
            elif entry.get("status") == "N/A (unsupported)":
                meds.append(None)
                mins.append(None)
                maxs.append(None)
                na_pos.append(i)
            else:
                meds.append(None)
                mins.append(None)
                maxs.append(None)
                timeout_pos.append(i)
        opt["series"].append(_bar_series(pooler, meds, na_pos, timeout_pos))
        opt["series"].extend(_band_series(pooler, mins, maxs))
    if na_pos:
        opt["series"].append(
            _marker_series("N/A (unsupported)", sorted(set(na_pos)),
                           NA_COLOR, "cross"))
    if timeout_pos:
        opt["series"].append(
            _marker_series("timeout/inconclusive", sorted(set(timeout_pos)),
                           TIMEOUT_COLOR, "triangle"))
    return opt


def flatness_chart(bundle):
    flat = (bundle or {}).get("flatness") or {}
    poolers = sorted(flat.keys())
    peaks = [((flat[p] or {}).get("peak") or {}).get("tps_median")
             for p in poolers]
    opt = _base_option("Surface flatness: peak tps per pooler",
                       "peak of each pooler's own measured configs; spread verdict in the table", [])
    opt["xAxis"]["data"] = [DISPLAY.get(p, p) for p in poolers]
    opt["series"].append({
        "name": "peak tps",
        "type": "bar",
        "itemStyle": {"color": {"type": "linear", "x": 0, "y": 0,
                                "x2": 0, "y2": 1,
                                "colorStops": [
                                    {"offset": 0, "color": "#58A6FF"},
                                    {"offset": 1, "color": "#1F6FEB"}]}},
        "label": {"show": True, "position": "top", "color": TEXT_COLOR},
        "data": [{"value": v,
                  "itemStyle": {"color": PALETTE.get(p, "#58A6FF")}}
                 for p, v in zip(poolers, peaks)],
    })
    return opt


def iso_overlay_chart(bundle):
    regions = (bundle or {}).get("iso_regions") or []
    matched = [r for r in regions if r.get("matched")]
    if not matched:
        return None
    # Deepest matched slice: most rows, tie-break on first sorted key.
    region = max(matched, key=lambda r: (len(r.get("rows", [])), 0))
    rows = region.get("rows", [])
    labels = sorted({r["cell_id"] + " " + r["pooler"] for r in rows})
    values = []
    for label in labels:
        row = next(r for r in rows
                   if r["cell_id"] + " " + r["pooler"] == label)
        values.append(((row.get("tps") or {}).get("median")))
    colors = []
    for label in labels:
        pooler = label.rsplit(" ", 1)[-1]
        colors.append(PALETTE.get(pooler, "#58A6FF"))
    title = ("Iso-region overlay: %s c=%s pool=%s T=%s %s%s"
             % (region.get("workload"), region.get("clients"),
                region.get("pool_size"), region.get("duration_s"),
                region.get("protocol"),
                " churn" if region.get("churn") else ""))
    opt = _base_option(title, "matched cells: "
                       + ", ".join(region.get("matched_cells", [])), [])
    opt["xAxis"]["data"] = labels
    opt["xAxis"]["axisLabel"] = {"color": TEXT_COLOR, "rotate": 30}
    opt["series"].append({
        "name": "median tps",
        "type": "bar",
        "label": {"show": True, "position": "top", "color": TEXT_COLOR},
        "data": [{"value": v, "itemStyle": {"color": c}}
                 for v, c in zip(values, colors)],
    })
    return opt


def pooler_page_charts(pooler, m1_entries, m2_entries):
    """Own-surface charts for one pooler page: own-m1 + own-m2."""
    m1_cells = sorted({e["cell_id"] for e in m1_entries})
    by_key = _index_maps(m1_entries + m2_entries)
    m2_cells = sorted({e["cell_id"] for e in m2_entries
                       if (e["cell_id"], pooler) in by_key})
    charts = {}
    for chart_id, cells in (("own-m1", m1_cells), ("own-m2", m2_cells)):
        opt = _base_option(
            DISPLAY[pooler] + " " + ("M1" if chart_id == "own-m1" else "M2")
            + " own surface",
            "median tps with min-max bands; N/A and timeout cells marked", [])
        opt["xAxis"]["data"] = list(cells)
        meds, mins, maxs = [], [], []
        na_pos, timeout_pos = [], []
        for i, cell in enumerate(cells):
            entry = by_key.get((cell, pooler))
            if entry is None or entry.get("status") == "measured":
                meds.append(_median(entry) if entry else None)
                lo, hi = _band(entry) if entry else (None, None)
                mins.append(lo)
                maxs.append(hi)
            elif entry.get("status") == "N/A (unsupported)":
                meds.append(None)
                mins.append(None)
                maxs.append(None)
                na_pos.append(i)
            else:
                meds.append(None)
                mins.append(None)
                maxs.append(None)
                timeout_pos.append(i)
        opt["series"].append(_bar_series(pooler, meds, na_pos, timeout_pos))
        opt["series"].extend(_band_series(pooler, mins, maxs))
        if na_pos:
            opt["series"].append(
                _marker_series("N/A (unsupported)", na_pos,
                               NA_COLOR, "cross"))
        if timeout_pos:
            opt["series"].append(
                _marker_series("timeout/inconclusive", timeout_pos,
                               TIMEOUT_COLOR, "triangle"))
        charts[chart_id] = opt
    return charts


def build_options(m1_entries, m2_entries, bundle):
    """Return {page: {chart_id: option}} for all six pages."""
    pages = {}
    comparison = {"m1-best": comparison_m1_chart(m1_entries)}
    for prefix, chart_id, title in (
            ("M2-S", "m2-session", "M2 session block heads"),
            ("M2-T", "m2-statement", "M2 statement block heads"),
            ("M2-I", "m2-io", "M2 I/O block heads"),
            ("M2-W", "m2-workloads", "M2 workload twins"),
            ("M2-P", "m2-prepared", "M2 prepared twins")):
        chart = _m2_block_chart(m2_entries, prefix, title)
        if chart is not None:
            comparison[chart_id] = chart
    comparison["flatness"] = flatness_chart(bundle)
    iso = iso_overlay_chart(bundle)
    if iso is not None:
        comparison["iso-overlay"] = iso
    pages["comparison"] = comparison
    for pooler in PAGE_POOLERS:
        pages[pooler] = pooler_page_charts(pooler, m1_entries, m2_entries)
    return pages


def _sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_parser():
    p = argparse.ArgumentParser(
        description="Poolduel M4 chart builder: bundles in, "
                    "ECharts option JSON out.")
    p.add_argument("--m1", default="poolduel/results/m1/medians.json")
    p.add_argument("--m2", default="poolduel/results/m2/medians.json")
    p.add_argument("--report", default="poolduel/results/report.json")
    p.add_argument("--out", default="poolduel/results/charts")
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    missing = [p for p in (args.m1, args.m2, args.report)
               if not os.path.isfile(p)]
    if missing:
        for path in missing:
            print("poolduel charts FAILED: missing input %s "
                  "(run repro.sh --report first; not inventing numbers)"
                  % path, file=sys.stderr)
        return 1
    try:
        with open(args.m1) as f:
            m1_entries = json.load(f)
        with open(args.m2) as f:
            m2_entries = json.load(f)
        with open(args.report) as f:
            bundle = json.load(f)
    except (ValueError, OSError) as exc:
        print("poolduel charts FAILED: unreadable input (%s)" % exc,
              file=sys.stderr)
        return 1
    if not isinstance(m1_entries, list) or not m1_entries:
        print("poolduel charts FAILED: %s has no median entries" % args.m1,
              file=sys.stderr)
        return 1
    if not isinstance(m2_entries, list) or not m2_entries:
        print("poolduel charts FAILED: %s has no median entries" % args.m2,
              file=sys.stderr)
        return 1
    pages = build_options(m1_entries, m2_entries, bundle)
    os.makedirs(args.out, exist_ok=True)
    manifest = {"sources": {}, "pages": {}}
    for label, src in (("m1/medians.json", args.m1),
                       ("m2/medians.json", args.m2),
                       ("report.json", args.report)):
        manifest["sources"][label] = _sha256_file(src)
    for page, charts in sorted(pages.items()):
        path = os.path.join(args.out, page + ".json")
        with open(path, "w") as f:
            json.dump(charts, f, indent=2, sort_keys=True)
        manifest["pages"][page] = {
            "file": page + ".json",
            "charts": sorted(charts.keys()),
            "sha256": _sha256_file(path),
        }
    with open(os.path.join(args.out, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
    print("poolduel charts: %d pages (%s) -> %s"
          % (len(pages), ", ".join(sorted(pages)), args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
