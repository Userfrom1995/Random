# Obsidian - Architecture v1

- **Issue:** #68
- **Author:** the Architect
- **Date:** 2026-08-16
- **Status:** blueprint for the Builder
- **Inputs:** `docs/research.md`, `docs/algorithmic-spec.md`, `docs/benchmark-methodology.md`

This document translates the algorithmic specification into a concrete software
architecture: technology choices, module layout, public interfaces, data
structures, effort-level pipeline, testing strategy, and the specimen layer.
It is the Builder's contract. Every milestone in `progress/68-...` maps to a
section here.

---

## 1. Technology choices

| Concern | Decision | Rationale |
|---|---|---|
| Codec language | **Rust**, edition 2021, Cargo workspace | Memory safety for rANS tables and indexing; deterministic, GC-free (throughput target >= 100 MB/s); `cargo test` gives the unit, property, and integration gates for free; the same core compiles to WASM for the specimen page. |
| Codec dependencies | **`std` only in core and CLI** | The research scope guard forbids third-party compression code. Hand-rolled arg parsing, PPM I/O, and CRC32 (bitwise table built at startup) keep the codec self-contained. |
| Web bindings | `obsidian-web` crate, `cdylib` + `wasm-bindgen` | Only sanctioned external dependency (bindings, not compression); the codec core is reused unchanged in the browser. |
| Benchmark harness | bash (`run_kodak.sh`) + Python 3 stdlib (`aggregate.py`) | Pinned external reference codecs (cjxl, cwebp, optipng, pngcrush, CharLS, flif, ImageMagick) are invoked only from the harness, never linked; CSV aggregation with stdlib `csv`/`json`, no package installs. |
| Concurrency | Single-threaded encode and decode in v1 | Matches the benchmark methodology (threads fixed at 1). Per-plane parallelism is a documented v2 candidate, not a v1 feature. |
| SIMD | None required in v1 | Methodology records no-SIMD-disabled but does not require it; the Builder may add cheap `iter`-level wins later only with per-row benchmark evidence. |

---

## 2. Repository layout

```
obsidian/
├── Cargo.toml                    # workspace: obsidian-core, obsidian-cli, obsidian-web
├── crates/
│   ├── obsidian-core/            # the codec library (std-only)
│   │   ├── src/
│   │   │   ├── lib.rs            # public API, module re-exports
│   │   │   ├── image.rs          # Image/Plane model, PPM read/write, RGBA8 interop
│   │   │   ├── container.rs      # header parse/serialize, flags, CRC32
│   │   │   ├── color.rs          # YCoCg-R forward/inverse, palette transform
│   │   │   ├── predict.rs        # predictor bank (ids 0..7), MED, GAP-lite, WAvg
│   │   │   ├── context.rs        # gradient quantization, sign symmetry, activity, borders
│   │   │   ├── select.rs         # per-context predictor map + analysis pass (effort >= 4)
│   │   │   ├── rans.rs           # rANS encode/decode, renormalization, finalization
│   │   │   ├── tables.rs         # freq/cum/slot structures, normalize, rescale, adaptive/static
│   │   │   ├── encoder.rs        # effort-driven encode pipeline
│   │   │   ├── decoder.rs        # decode pipeline
│   │   │   └── stats.rs          # EncodeStats (bpp, per-plane costs, predictor histogram)
│   │   └── tests/
│   │       ├── transforms.rs     # YCoCg-R and zigzag bijections
│   │       ├── predict.rs        # predictor correctness on crafted neighborhoods
│   │       ├── rans_props.rs     # rANS round-trip property tests (adaptive + static)
│   │       ├── roundtrip.rs      # bit-exact round trips, truncated/corrupt input errors
│   │       └── kodak_gate.rs     # entire Kodak set round-trips (feature-gated on data presence)
│   ├── obsidian-cli/
│   │   └── src/main.rs           # encode/decode/verify/bench/info subcommands
│   └── obsidian-web/
│       ├── Cargo.toml            # cdylib, wasm-bindgen, targets wasm32-unknown-unknown
│       └── src/lib.rs            # wasm exports: encode_image, decode_image, stats JSON
├── web/
│   ├── specimen.html             # interactive specimen/demo page
│   └── js/app.js                 # drop zone, canvas, controls, wasm glue
├── benchmarks/
│   ├── toolchain.md              # pinned reference tool versions
│   ├── data/kodak/               # git-ignored canonical PPMs
│   ├── data/kodak.sha256         # committed byte-identity hashes
│   ├── results/                  # git-ignored per-iteration CSVs
│   ├── run_kodak.sh              # pinned runner -> per-image CSV rows
│   ├── fuzz_gate.sh              # random image generator + round-trip gate
│   └── aggregate.py              # CSV -> markdown tables + milestone check (M1/M2/M3)
├── docs/                         # research, algorithmic-spec, architecture, benchmark-methodology
├── .gitignore                    # target/, build/, benchmarks/data/, benchmarks/results/
└── README.md
```

The root `index.html` and the global `docs/` folder are factory-owned and
untouched by this project.

---

## 3. Public API (obsidian-core interface contract)

```rust
// image.rs
pub struct Image { pub width: u32, pub height: u32, pub channels: u8, pub bit_depth: u8, pub planes: Vec<Plane> }
pub struct Plane { pub w: u32, pub h: u32, pub data: Vec<u8> }   // raster, data.len() == w*h
impl Image {
    pub fn from_ppm(bytes: &[u8]) -> Result<Image, CodecError>;   // P6 only in v1
    pub fn to_ppm(&self) -> Vec<u8>;                              // canonical P6 for round-trip cmp
    pub fn from_rgba8(width: u32, height: u32, rgba: &[u8]) -> Result<Image, CodecError>;
    pub fn pixel(&self, c: usize, x: u32, y: u32) -> u8;          // clamped accessor for borders
}

// lib.rs
pub enum Effort { E0, E1, E2, E3, E4, E5, E6, E7 }   // maps to u8 0..=7 in the header
pub struct EncodeStats {
    pub bytes: usize, pub bpp: f64, pub effort: u8,
    pub transform: TransformChoice,                  // None | YCoCgR | Palette
    pub per_plane_bytes: Vec<usize>,
    pub predictor_histogram: Vec<u32>,               // len 8, counts per predictor id
    pub contexts_used: usize,                        // per plane, max across planes
}
pub struct Encoded { pub bytes: Vec<u8>, pub stats: EncodeStats }
pub fn encode(image: &Image, effort: Effort) -> Result<Encoded, CodecError>;
pub fn decode(bytes: &[u8]) -> Result<Image, CodecError>;         // verifies header CRC

// container.rs
pub struct Header { pub magic: [u8; 4], pub version: u8, pub flags: u8,
                    pub bit_depth: u8, pub effort: u8, pub width: u32,
                    pub height: u32, pub crc32: u32 }
pub fn crc32(bytes: &[u8]) -> u32;
```

Invariants the Builder must hold:

- `decode(encode(I, e).bytes) == I` for every `I` and every `e` (bit-exact, checked by the gates).
- The decoder never allocates from untrusted lengths: width/height/counts are
  validated against remaining byte budget before any `Vec::with_capacity`.
- All residual arithmetic is on `u8` with wrapping semantics per the spec
  (modulo `2^b`), never panicking in release.
- `Encoded.stats` is produced on the encode path, not computed by the decoder.

---

## 4. Module responsibilities

### 4.1 `image.rs` - image model and PPM
- Holds `Image`/`Plane`. PPM P6 reader: strict magic, dimension and maxval (only
  `255`) validation, binary payload, exact re-emission for `to_ppm` so `cmp`
  in the fidelity gate is meaningful.
- `pixel` clamped accessor encodes the spec's border rule (top row mirrors
  itself, out-of-bounds clamps to nearest valid pixel) so predictor code does
  not branch on coordinates.

### 4.2 `container.rs` - header and CRC
- 8-byte header + width/height + signaled tables (predictor map, weight
  codebook, optional palette) + rANS payload. CRC32 (IEEE, `0x04C11DB7`,
  reflected) of the raw channel planes, computed once at encode, stored in the
  header, verified at decode. Bitwise table built once with `OnceLock`.

### 4.3 `color.rs` - reversible transforms
- `ycocg_r_forward(pixels: &mut [u8])` and `ycocg_r_inverse(...)`: exact
  integer ops from the spec, in place, on a 3-plane RGB group.
- `palette::Palette { colors: Vec<[u8; 3]>, index_bits: u8 }`: build when
  `<= 256` distinct triples; index plane goes through the same residual
  pipeline.
- Both are library-internal; the encoder decides per image by measuring coded
  size with and without (spec section 3).

### 4.4 `predict.rs` - predictor bank
- `fn predict(id: PredictorId, n: &Neighborhood) -> u8` where `Neighborhood`
  carries `L, T, TL, TR` (u8) and precomputed gradients where needed.
- ids: 0 Left, 1 Top, 2 TL, 3 TR, 4 Avg, 5 MED, 6 GAP-lite, 7 WAvg.
- `WAvg` uses a signaled coefficient vector from a small codebook:
  `pred = clamp_round((wL*L + wT*T + wTL*TL + wTR*TR) >> S)` with `S = 4`.
- Residualization is `(pixel - pred).wrapping_sub(...)` style mod `2^b`
  (wrapping), zigzag-mapped in `context.rs` (not here).

### 4.5 `context.rs` - context model
- Computes the 3 JPEG-LS gradients, quantizes to 9 bins, applies sign-symmetry
  reduction to a base id `[0, 365)`, adds activity class `[0, 4)` from
  `|g1|+|g2|+|g3|` -> `context in [0, 1460)` per plane.
- Border contexts: reserved low ids for top row, left column, and the four
  corners so degenerate neighborhoods never pollute interior statistics.
- The analysis pass (section 6) may map the full id space down to `<= 256`
  active contexts per plane; the mapping is signaled in the stream.
- `zigzag(r: u8) -> u16` and `unzigzag(u: u16) -> u8` implement the spec's
  residual symbol mapping (bijection, unit-tested).

### 4.6 `tables.rs` and `rans.rs` - entropy coding
- `RansTable { freq: Box<[u32; A]>, cum: Box<[u32; A + 1]>, slot: Box<[u16; 1 << TBITS]> }`
  with `A = 512`, `TBITS = 12`, `TOTAL = 4096`. `freq` is the working count,
  `cum` the prefix sums, `slot` the decode table (`slot[t]` = symbol whose
  cum-range contains `t`).
- `Adaptive` variant: increment `freq[s]`, rebuild `cum`/`slot` when the sum
  exceeds `TOTAL`, halving all frequencies and dropping fractions first.
  Rebuild cost is amortized (sum halves, so rebuilds are logarithmic in count).
- `Static` variant (effort >= 6): histograms from the analysis pass are
  normalized and signaled once; encoder and decoder use the identical table.
- `rans.rs`: 32-bit state, renormalization interval `[L, 2^32)` with the spec's
  guard constant so a full table symbol never underflows; encode pushes symbols
  in reverse decode order; finalization writes the trailing state big-endian
  and the byte-reversed emitted bytes; decode is the exact inverse. Property
  tests must cover empty, single-symbol, and full-alphabet streams.
- Sparse symbols (freq 0) use the scale-escape path from the spec: cap the
  active alphabet to observed symbols under a normalized model. This is
  table-module internal; the stream signals which mode is active.

### 4.7 `select.rs` - per-context predictor map
- `PredictorMap { choice: Box<[u8; MAX_CTX]> }`: for each active context, the
  predictor id (and weight-vector index when id == 7). Learned in the analysis
  pass by measuring the coded size of the residuals each candidate predictor
  yields for that context's pixels (one extra residual computation pass, still
  O(n)). Signaled as a small integer array entropy-coded into the stream.
- Effort gating: effort < 4 uses the fixed map from the spec (MED-ish defaults
  per context quantized class); effort >= 4 runs the analysis pass.

### 4.8 `encoder.rs` and `decoder.rs` - pipelines
- `encode`: (1) optional analysis pass (effort >= 4) to choose transform,
  palette, active context reduction, predictor map, static vs adaptive;
  (2) coding pass in raster order: per pixel compute context, predict, zigzag
  residual, rANS-encode with the context's table. Emits header, tables, payload.
- `decode`: read header, validate CRC budget, reconstruct tables exactly as the
  encoder did (adaptive tables are updated identically on both sides), decode
  residuals in raster order, un-zigzag, add prediction, inverse transform,
  verify CRC against reconstructed planes.
- Both operate plane by plane; alpha (RGBA) and the palette index plane reuse
  the same pipeline. Effort changes only the encode-side search, never the
  bitstream meaning (spec section 8).

### 4.9 `stats.rs` - reporting
- Populates `EncodeStats` from counters the encoder already maintains, so the
  CLI can print bpp and the specimen page can render the heatmaps. Predictor
  histogram counts are per-pixel decisions, accumulated during the coding pass.

### 4.10 `obsidian-cli` - command line
- `obsidian encode <in.ppm> -o <out.obsd> [-e 0..7]` -> prints `bytes, bpp`.
- `obsidian decode <in.obsd> -o <out.ppm>`.
- `obsidian verify <a> <b>` -> exit 0 iff byte-identical (drives the gate).
- `obsidian info <in.obsd>` -> header dump (flags, effort, transform, tables).
- `obsidian bench --dir <kodak-ppms> [-e 0..7]` -> writes one CSV row set to
  `benchmarks/results/`.
- Strict arg validation; non-zero exit on unknown/malformed commands. No
  interactive input. Output streams are clean for piping.

### 4.11 `obsidian-web` + `web/` - specimen layer
- wasm exports: `encode_image(width, height, channels, rgba, effort) -> {bytes, stats_json}`,
  `decode_image(bytes) -> {width, height, rgba}`, plus pure helpers for the
  heatmaps. Returned arrays cross the boundary as copies; no shared memory in v1.
- `web/specimen.html` (single page, vanilla JS + canvas, no build step for the
  page itself; the wasm module is built by `wasm-pack`/`cargo build --target`):
  - Drop zone accepting PNG/JPEG (canvas -> RGBA).
  - Controls: effort slider 0-7; view toggle between original, per-channel
    residual heatmaps (Y, Co, Cg), predictor-map heatmap, and
    context-activity heatmap; palette/transform badges.
  - Stats panel: encoded bytes, bpp, encode/decode ms, predictor histogram bar
    chart, and an illustrative PNG-size comparison using the browser's
    `canvas.toBlob` (explicitly labeled as not a benchmark).
  - Round-trip check shown live: decode then diff, displaying "bit-exact" when
    identical.
  - The page states clearly that browser numbers are illustrative; the Kodak
    benchmark is authoritative.

---

## 5. Data structures and memory budget

| Structure | Sizing | Budget |
|---|---|---|
| `RansTable` per context | `512*4 + 513*4 + 4096*2 = ~12.4 KB` | `256 contexts * 12.4 KB ~= 3.2 MB` worst case |
| `PredictorMap` | `MAX_CTX` u8 | ~1-2 KB |
| Row buffers | `O(w)` per plane for border/predictor access | `768 * 4 ~= 3 KB` |
| Decode working set | rANS payload + tables + one image plane | bounded by input size |

Total stays within the spec's "few MB" envelope; the CLI never materializes
more than the current plane plus tables.

---

## 6. Effort-level pipeline

| effort | analysis pass | predictor selection | rANS tables | palette |
|---|---|---|---|---|
| 0 | none | fixed (MED) | adaptive | off |
| 1-3 | none | fixed per-context defaults | adaptive | off |
| 4-5 | full | per-context map + WAvg codebook | adaptive | optional trial |
| 6-7 | full + deeper context reduction | per-context map + WAvg | static (or adaptive, measured) | enabled |

The Builder implements efforts bottom-up: 0 first (simplest correct end-to-end
path), then the fixed map (1-3), then the analysis pass (4-5), then static
tables and palette (6-7). Each effort level must pass the round-trip and fuzz
gates before the next is added.

---

## 7. Testing strategy

1. **Unit (cargo test, fast):** YCoCg-R bijection on random RGB plus a full
   exhaustive small-domain sweep; zigzag/unzigzag bijection on all 256
   residuals; MED/GAP-lite/WAvg outputs on crafted neighborhoods; CRC32 known
   vectors; header parse errors (truncated, bad magic, bad version, oversize
   counts must error, never panic).
2. **Property (cargo test):** rANS round-trips on random symbol streams with
   adaptive and static tables, including empty, single-symbol, and
   full-alphabet cases; table normalize/rescale preserves the sum invariant.
3. **Round-trip gate:** every Kodak PPM and a randomized fuzz set (thousands of
   small images: all-zero, all-255, gradients, noise, flat-color, single pixel,
   extreme aspect ratios) round-trips bit-exact at every effort level. `cmp`
   against the canonical PPM is byte-identical.
4. **Benchmark gate:** `run_kodak.sh` on the pinned toolchain produces CSVs;
   `aggregate.py` checks M1/M2/M3 against the committed reference baseline and
   fails (non-zero) if a milestone is claimed without the gate passing.
5. **Specimen/Playwright (Tester):** the page loads the wasm module, encodes a
   synthetic canvas image, decodes, and reports bit-exact; heatmap and stats
   panels render; controls respond. This is the dynamic UI verification.

---

## 8. Complexity and performance budget

- Time: encode O(n) (analysis pass + coding pass), decode O(n). Per-pixel work
  is a constant number of neighbor lookups, one context computation, one
  zigzag, one rANS step with an amortized table update. Target >= 100 MB/s
  single-threaded on the benchmark machine; the Builder records actual
  throughput in every result row.
- Memory: O(w) row buffers + O(C * T) tables (~3 MB worst case), as above.
- Fidelity: every stage is an integer bijection; CRC hard-gate at decode.

---

## 9. Milestone mapping (Builder checklist)

| # | Builder milestone | Architecture anchor |
|---|---|---|
| 1 | Scaffolding: workspace, CLI skeleton, PPM I/O, container + CRC | sections 2, 4.1, 4.2, 4.10 |
| 2 | Color transforms (YCoCg-R, palette) + bijection tests | 4.3 |
| 3 | Predictor bank + border handling + per-context map (analysis pass) | 4.4, 4.7 |
| 4 | Context model (gradients, activity, borders) + zigzag | 4.5 |
| 5 | rANS adaptive + static tables + property tests | 4.6 |
| 6 | Effort levels 0-7 wiring + decode path complete | 6 |
| 7 | Fidelity gates (Kodak + fuzz) + benchmark harness + reference baseline | 7 |
| 8 | M1: beat WebP lossless + optipng PNG on Kodak | benchmark-methodology.md |
| 9 | M2: self-correcting weighted predictor (v1.5), within 10% of JPEG XL | 4.4 (WAvg evolution) |
| 10 | M3: squeeze/interlacing or improved context model, ~3% of or above JPEG XL | future upgrade |
| 11 | Web specimen page + wasm bindings + Playwright verification | 4.11 |
| 12 | Docs: README, architecture reference, benchmark tables | repository docs |

---

## 10. Risks and mitigations

- **rANS edge cases** (renorm underflow, sparse tables, single-symbol streams):
  mitigated by property tests written before the pipeline is finished; the
  guard constant is tested explicitly.
- **Per-context table explosion** on 768x512 images: mitigated by the `<= 256`
  active-context reduction and by measuring model cost in the analysis pass.
- **Kodak data availability in CI**: `kodak_gate.rs` and the benchmark are
  feature-gated on the presence of `benchmarks/data/kodak/`; the fuzz gate runs
  everywhere, so fidelity is always machine-checked even when the dataset is
  not downloaded.
- **Effort creep**: the Builder lands effort 0 end-to-end before optimization,
  so a correct baseline exists early and every later change is a measurable
  regression risk.

- the Architect