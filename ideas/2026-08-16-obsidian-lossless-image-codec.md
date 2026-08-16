# Obsidian - lossless image-compression codec (Kodak-benchmarked)

The factory's priority project (issue #68, owner-directed, 2026-08-16T08:17Z).
A lossless image codec that competes with, and ideally outperforms, JPEG XL and
WebP lossless on the Kodak dataset. No new ideas or projects are started until
this is achieved or shown unviable.

## What it is

A from-scratch lossless codec: encoder + decoder, bit-exact reversible, with a
rigorous benchmark loop on Kodak (24 images, 768x512, 24-bit RGB). The design
marries the two proven ideas that make JPEG XL the practical lossless leader:

- **Per-pixel-quality prediction**: a bank of causal predictors (Left, Top,
  TL, TR, Avg, MED, GAP-lite, weighted average) where the encoder learns a
  per-context predictor map, plus a self-correcting weighted predictor as the
  v1.5 upgrade.
- **Context-modeled rANS entropy coding**: quantized-gradient contexts with
  sign symmetry and an activity class, coded with adaptive rANS (12-bit
  tables), giving fractional-bit coding that Huffman-based WebP structurally
  cannot reach.

Plus a reversible YCoCg-R color transform, an optional palette transform, and
a per-image adaptive selection between all of the above. Complexity is O(pixels)
in time for encode and decode, with a few MB of context tables.

## Realistic trajectory (from the literature review)

Kodak mean bpp, literature ranges: PNG optimized ~4.2, JPEG-LS ~3.7, WebP
lossless ~3.4-3.5, FLIF ~3.1, JPEG XL lossless ~3.1-3.3, MRP/context-mixing
~2.6-2.8 (impractical speed). An independent 2024 aggregate benchmark confirms
JPEG XL smallest, WebP ~7.5% larger, optipng PNG ~28% larger. The direction is
clearly viable: the building blocks are published science and the gap from a
clean implementation to the practical SOTA is small.

Milestones: M1 beat WebP + PNG; M2 within 10% of JPEG XL; M3 within ~3% of or
above JPEG XL. Every iteration records a benchmark row.

## Why the factory

- **Researcher** (this entry): literature review + algorithmic spec + benchmark
  methodology (see `obsidian/docs/`).
- **Architect**: software architecture for the encoder/decoder + benchmark CLI.
- **Builder / Fixer**: benchmark-driven implementation, iteration by iteration.
- **Reviewer / Tester**: quality gate and dynamic verification (bit-exact
  round trips, Kodak comparisons, speed).
- **Maintainer**: tracks the milestone curve; resumes via `/oc continue` until
  the goal is met or evidence shows it is not.

## Architecture (the Architect, 2026-08-16)

Full blueprint in `obsidian/docs/architecture.md`. Summary:

### Deliverables
- `obsidian-core`: a std-only Rust library implementing the v1 spec: container
  header + CRC, YCoCg-R and palette transforms, an 8-predictor bank with a
  per-context predictor map, a gradient + activity context model, and adaptive
  (12-bit) rANS with a static-table variant. Public API: `encode(&Image, Effort)`
  and `decode(&[u8])` with `EncodeStats` reporting.
- `obsidian-cli`: encode / decode / verify / info / bench subcommands, strict
  arg validation, non-zero exit on error, clean stdout for piping.
- `obsidian-web` + `web/specimen.html`: the same core compiled to WASM behind
  an interactive specimen page (drop an image, effort slider, residual /
  predictor / activity heatmaps, live bit-exact round-trip check, stats panel).
- `benchmarks/`: pinned Kodak runner (`run_kodak.sh`), fuzz gate, and a Python
  aggregator that renders the milestone table and checks M1/M2/M3.
- Docs: `docs/architecture.md` + README updates.

### How it works
A Cargo workspace with three crates sharing one codec core. The encoder runs an
optional O(n) analysis pass (effort >= 4) to pick the transform, active-context
reduction, per-context predictor map, and static vs adaptive tables, then a
raster-order coding pass. The decoder reconstructs the tables identically and
inverts every stage; the header CRC hard-gates bit-exact recovery. Effort only
changes encoder search, never the bitstream meaning.

### Module breakdown
- `image` (Image/Plane model, PPM P6, clamped border accessor)
- `container` (header, flags, CRC32)
- `color` (YCoCg-R forward/inverse, palette)
- `predict` (predictor bank: Left, Top, TL, TR, Avg, MED, GAP-lite, WAvg)
- `context` (gradient quantization, sign symmetry, activity, border contexts,
  zigzag residual map)
- `select` (per-context predictor map + analysis pass)
- `tables` + `rans` (freq/cum/slot 12-bit tables, adaptive and static, rANS
  encode/decode with renorm guard)
- `encoder` / `decoder` (effort-driven pipelines)
- `stats` (EncodeStats for CLI and specimen reporting)
- `obsidian-cli` / `obsidian-web` (thin wrappers over the core)

### Test matrix
- Unit: transform bijections, zigzag bijection, predictor correctness,
  CRC known vectors, malformed-input errors (never panic).
- Property: rANS round-trips on empty/single-symbol/full-alphabet streams,
  table normalization invariants.
- Gates: bit-exact round-trips on all Kodak PPMs plus thousands of fuzz images
  (all-zero, all-255, gradients, noise, flat, single-pixel, extreme aspect
  ratios) at every effort level; `cmp` byte-identity.
- Benchmark: `aggregate.py` enforces M1/M2/M3 against the pinned baseline.
- Specimen (Playwright): page loads wasm, encodes/decodes a synthetic image,
  reports bit-exact, renders heatmaps and stats.

- Dr. Ada, the Researcher
- the Architect