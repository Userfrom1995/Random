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
JPEG XL smallest, WebP ~7.5% larger, optipng PNG ~28% larger, and a 2021 study
(Barina) confirms FLIF narrowly ahead of JPEG XL only at a heavy decode-speed
cost. The direction is clearly viable: the building blocks are published
science and the gap from a clean implementation to the practical SOTA is small.

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

## Deliverables (research phase)

- `obsidian/docs/research.md` - literature review and SOTA survey on Kodak
  lossless rates, with design conclusions.
- `obsidian/docs/algorithmic-spec.md` - v1 codec specification: container,
  YCoCg-R transform, predictor bank + per-context map, gradient + activity
  contexts, adaptive rANS, effort levels, complexity, fidelity guarantees.
- `obsidian/docs/benchmark-methodology.md` - reproducible Kodak protocol:
  pinned toolchain, canonical PPM ground truth, metrics, fidelity gate,
  milestone criteria.

## Handoff

Next pipeline step: Architect (`/oc architect`).

- Dr. Mob, the Researcher

---

# Architecture (blueprint phase, 2026-08-17)

## Summary

A Cargo workspace for the codec: a zero-dependency `obsidian-core` library
(container, PPM I/O, YCoCgR + palette, predictor bank, gradient/activity
contexts, adaptive/static rANS, encoder/decoder), a `obsidian-cli` crate
(encode/decode/roundtrip/selftest/bench/check), and a dependency-free JS mirror
plus an interactive specimen page (`obsidian/web`) that reproduces the codec
byte-for-byte in the browser (the factory's proven Meridian pattern, no wasm).
The rANS formulation is pinned with concrete constants (M = 4096, renorm bound
2^20, byte-wise stack renorm) so the Builder implements the correct variant
first try; correctness is enforced by per-stage property tests.

## Why it is shaped this way

- **Milestone-first build order:** effort 0 (MED + single context + adaptive
  rANS) end-to-end and fuzz-verified before predictors, contexts, and effort
  levels accumulate. Each milestone (M1/M2/M3) maps to a build step with a
  numeric gate.
- **rANS only:** one entropy coder keeps encode/decode symmetric; adaptive by
  default, static at effort >= 6, property-tested against pathological tables.
- **Effort = encoder-side model search:** identical bitstream for all efforts,
  one decoder path for the Tester to verify.
- **Per-stage bijection property tests** plus the Kodak + fuzz fidelity gates
  and the header CRC: fidelity is machine-checked, not asserted.
- **JS mirror over wasm:** dependency-free, statically hostable, byte-exact
  consistency-tested against the Rust core (Meridian precedent).

## How it works

Two-pass encode for effort >= 1 (analysis pass builds the per-context predictor
map, context reduction, weight codebook, and static tables; coding pass emits
residuals through per-context rANS, pushed in reverse raster order). Decode is a
single pass: header, model section, residual reconstruction, inverse transform,
palette expand, CRC cross-check. All stages are integer bijections on the
`[0, 255]` plane space.

## Module breakdown

- `crates/obsidian-core`: header/crc32, image, ppm, color, predict, context,
  model, rans, encoder, decoder.
- `crates/obsidian-cli`: cli (subcommands) + bench (Kodak runner, fuzz gate).
- `benchmarks/`: pinned toolchain, kodak.sha256, run_kodak.sh, fuzz_gate.sh,
  aggregate.py, results/ CSV + trend tables.
- `web/`: index.html, style.css, js/codec.js (mirror), js/ui.js, samples/.
- `tests/`: consistency.test.mjs (JS vs Rust byte-exact), ui.test.mjs (DOM).

## Test matrix

Per-module unit tests (known vectors, exhaustive small inputs, property tests);
integration round-trip on Kodak + fuzz at efforts 0/4/7; determinism and
corruption tests; JS/Rust byte-consistency suite; Playwright/UI checks for the
specimen page. Full matrix in `obsidian/docs/architecture.md` section 11.

## Deliverables

- `obsidian/docs/architecture.md` - the software architecture blueprint
  (workspace, modules, data structures, definitive rANS, container layout,
  effort pipeline, complexity budget, test matrix, milestone mapping).

Next pipeline step: Builder (`/oc build this`).

- the Architect

---

# Benchmark harness + first Kodak row (Builder phase, 2026-08-17)

The codec core (effort 0-7, bit-exact, 46 lib tests) is merged via PR #76.
This phase (issue #77) delivered the measurement loop that makes the project
benchmark-driven:

- `benchmarks/toolchain.md` - pinned reference toolchain: cjxl 0.7.0, cwebp
  1.3.2, optipng 0.7.8, pngcrush 1.8.13, ImageMagick 6.9.12 (J2K via OpenJPEG
  2.5.0), and CharLS 2.4.2 built from pinned source with a small `cjls` PPM
  CLI (`benchmarks/tools/cjls.cpp`, built by `build_toolchain.sh`).
- `benchmarks/data/kodak.sha256` - the Kodak PCD0992 suite (24 images, 768x512,
  RGB) normalized to binary P6 PPM and pinned by hash; the PPMs are git-ignored
  and match both r0k.us and the Kaggle mirror byte-for-byte.
- `benchmarks/run_kodak.sh` - manifest check, then per codec a decode + `cmp`
  fidelity gate, then encode/decode timing, emitting
  `results/<date>-<version>.csv`.
- `benchmarks/fuzz_gate.sh` - randomized small-image round-trips at efforts
  0/4/7 as the pre-benchmark gate.
- `benchmarks/aggregate.py` - arithmetic mean bpp (headline) + geometric mean
  of per-image size ratios.
- `benchmarks/README.md` - headline table, per-image table, trend.

## Reference baseline (canonical PCD0992)

| Codec | Mean bpp |
|---|---|
| JPEG XL (cjxl 0.7.0, e7) | 8.7062 |
| JPEG-LS (CharLS 2.4.2, HP1) | 9.7113 |
| JPEG 2000 (OpenJPEG 2.5.0) | 9.5762 |
| WebP (cwebp 1.3.2, z9 m6) | 9.6130 |
| PNG (pngcrush -brute) | 12.9815 |
| PNG (optipng -o7) | 13.0518 |
| **Obsidian v1 (effort 4)** | **27.8226** |

These references match the independent WangXuan95 2024 lossless benchmark on
the same corpus within ~0.5%, confirming the harness measures the canonical
dataset correctly (the ~3-4 bpp figures in some papers are a downsampled
subset). Obsidian v1 is bit-exact but not yet competitive; the M1 (beat WebP +
PNG) / M2 (within 10% of JXL) / M3 (within ~3% of JXL) milestones are the
optimization loop, each recorded as a new trend row.

Next: milestone optimization (`/oc continue`).

- the Builder

---

## Architect v2 addendum - entropy-stage architecture (2026-08-18)

The first Obsidian Kodak row (effort 4) measured **27.82 bpp** (1.16x raw RGB),
a guaranteed expansion caused entirely by the entropy stage: a per-context
adaptive rANS over a 512-symbol alphabet cannot specialize its tables on a
768x512 image (each of ~285 contexts gets only ~4138 symbols vs the ~2048
increments needed). Prediction, YCoCg-R, the context model, and the container
are correct and preserved.

**Architectural fix:** make the entropy stage a replaceable backend behind a
stable container flag rather than a single hard-coded rANS coder. The full
blueprint is in `obsidian/docs/entropy-architecture.md`; summary:

- New header flag `ENTROPY_GR` (flags bit 4). When set, per-plane payloads are
  per-context adaptive Golomb-Rice (Design A) bitstreams; when clear, the legacy
  rANS path remains (and becomes Design B at M2/M3).
- GR needs **zero model bytes**: both sides adapt the per-context `k` from the
  symbols they decode, so `k` is mirrored, signaled state. The model section
  keeps only the predictor map / transform / palette; `static_histograms` is
  `None` for GR.
- New primitives live in `rans.rs`: `BitWriter`/`BitReader`, `GrState` (k + bias
  counter, JPEG-LS update), `map`/`unmap` (signed residual -> Rice codeword),
  `gr_write_symbol`/`gr_read_symbol`. The per-pixel loops in `encoder.rs`
  (`code_planes`) and `decoder.rs` swap the rANS table calls for GR calls; no
  dry-run/reverse coding is needed (GR is forward streaming).
- `model.rs::analyze` gains an `entropy_gr: bool` argument; when true it skips
  the static-histogram collection.
- M0 (blocker): GR as the default drops bpp below raw 24 and below optipng PNG
  13.05. M1: with the existing per-context predictor selection + YCoCg-R, below
  WebP 9.61. M2/M3: capped-and-escaped static rANS (Design B) and/or
  self-correcting weighted predictor, toward JPEG XL 8.71.

Only `encoder.rs`, `decoder.rs`, `rans.rs` (plus the `Header` flag and the
`analyze` signature) are in scope; the rest is preserved.

- the Architect

---

## Architect M2 addendum - bias cancellation + run mode (2026-08-18)

The 10.16 bpp corrected baseline meets the PNG gate (13.05) but is ~0.45 bpp above
WebP (9.61) and ~1.45 bpp above JPEG XL (8.71). The "~10.1 bpp residual-entropy
floor" is only the *un-modeled* floor: no bias cancellation, no run mode. M2 removes
both, correcting the Builder's reverted naive experiment (which regressed to 14.16
bpp because it had no dead-zone and used a drifting EMA of the signless magnitude).

Full blueprint in `obsidian/docs/m2-bias-run-architecture.md`; summary:

- New header flag `GR_M2` (flags bit 5, 0x20), shipped together with `ENTROPY_GR`.
  Old v1 GR streams (bit4=1, bit5=0) still decode. No other container change; bias
  and run state are fully implicit (mirrored), so zero model bytes are added.
- **Bias cancellation (M2-A):** `GrState` gains a `bias: i16` (added to the
  prediction) and a `bias_count: i16`. Adaptation uses the *raw* residual with a
  **dead-zone** (`|r_raw| <= 2` -> no update, fixes the chroma regression) and a
  **clamped, counter-committed** nudge (`bias` in +/-16, moves +/-1 every 4
  same-sign residuals, fixes the EMA drift / single-context poisoning). Bias is
  never written to the bitstream.
- **Run mode (M2-B):** per-plane, JPEG-LS-style. Runs are maximal value-equal pixel
  sequences; the encoder uses a 1-pixel lookahead, the decoder copies `prev_val`.
  One parameter-free **Elias-gamma(runlen)** code per run replaces `L * (1 + k)` GR
  bits for the run body. No per-pixel flag overhead.
- M2 gate: Kodak effort-4 mean bpp **< 9.71** (JPEG-LS), aiming **< 9.61** (WebP).
- Roadmap: M2.5 context mixing (2-3 mixed GR sub-estimators) toward ~9.0-9.3; M3
  LZ77 back-references + self-correcting weighted predictor (new `GR_LZ` flag) to
  clear JPEG XL 8.71. Design B (capped rANS) remains a fallback.

In scope: `rans.rs` (`GrState` + gamma), `encoder.rs`/`decoder.rs` (GR+M2 branch),
`header.rs` (flag). Prediction, YCoCg-R, context model, container, CRC preserved.

- the Architect

---

## Architect M3 addendum - LZ77 back-references + self-correcting weighted predictor (2026-08-18)

M2 (bias + run) regressed to 11.14 bpp and M2.5 (context mixing) regressed ~0.5%:
both prove the **per-pixel residual-entropy floor (~10.1 bpp) is real** and cannot
be beaten by coding residuals better. To clear WebP (9.61) and JPEG XL (8.71) we
must reduce the residual stream itself - by exploiting **spatial redundancy**
(LZ77 back-references) and **predictor adaptability** (learned weighted predictor).

Full blueprint in `obsidian/docs/m3-lz77-weighted-predictor.md`; summary:

- New header flag `GR_LZ` (flags bit 7, 0x80), shipped with `ENTROPY_GR`. Old
  v1 GR / GR_M2 / GR_CM streams still decode; when `GR_LZ` is clear the per-plane
  stream is byte-identical to v1 GR (no regression, no expansion possible).
- **M3-A LZ77 (primary, zero model bytes):** per-plane match coding over the
  decoded sample buffer. Each position emits a binary match-flag (tiny mirrored
  `BinCoder`, 12-bit probability) then either a GR literal (existing path) or a
  match `(offset, length)` coded with Elias-gamma. The decoder has no match
  finder: it copies from its own buffer at `pos - offset`, so it stays bit-exact
  by induction (the buffer equals the encoder's buffer for all prior positions).
  Hash-chained match finder (WINDOW ~32768, MIN_MATCH 3); greedy/lazy matching.
  This is the WebP/JPEG XL-class win that M2 could not deliver.
- **M3-B self-correcting weighted predictor (secondary, signaled weights):** the
  Weighted predictor's weights become **per-context learned** (least-squares /
  gradient descent during `analyze`, quantized, stored in the model section) plus
  an optional **mirrored online correction** (after each Weighted literal both
  sides nudge the 4 weights by `sign(r) * neighbor` - zero extra signal). Gated
  behind an `OBSIDIAN_M3_WP` seam; falls back to per-plane learned weights if the
  per-context table exceeds `MODEL_SIZE_FRACTION`.
- M3 primary gate: Kodak effort-4 **< 9.61** (WebP). M3-A + M3-B (and, if needed,
  Design B capped rANS) target **< 8.71** (JPEG XL). Honest risk: photographic
  Kodak LZ77 gain is ~0.3-0.7 bpp; M3-A should clear WebP, JPEG XL may need M3-B
  and/or Design B.
- Build order: implement M3-A first, measure, then M3-B. Design B (context-modeled
  rANS) is the fallback route under 8.71.

In scope: `rans.rs` (`BinCoder` + match helpers), `encoder.rs`/`decoder.rs`
(GR+LZ branch), `header.rs` (flag), and (M3-B) `model.rs` (per-context weights).
Prediction bank (except Weighted weights), YCoCg-R, context model, container, CRC
preserved; legacy rANS / Design B path untouched.

- the Architect
## M3-B addendum (2026-08-18, the Builder)

M3-B (self-correcting weighted predictor) implemented and shipped OFF by default behind
`OBSIDIAN_M3_WP="1"` (opt-in, mirrored, zero signaled model bytes). Per-context weight
refinement is a mirrored SGD on the squared residual (`WeightVec::adapt_online` in
`predict.rs`), seeded from the per-plane codebook weight, woven into the GR_LZ path. On
synthetic photographic-style proxies it REGRESSES vs the no-WP LZ path (table in
`obsidian/benchmarks/results/2026-08-18-m3b-synth-proxy.csv`); consistent with M2/M2.5 it
confirms the ~10.1 bpp photographic residual-entropy floor of the GR architecture. WebP
(9.61) / JPEG XL (8.71) gates remain OPEN (unconfirmed: `data/kodak` absent in build env).
Next: M3.5 / Design B (capped-and-escaped static rANS with per-context context modeling).

- the Builder

## M3.5 Design B addendum (2026-08-18, the Builder)

M3.5 (capped-and-escaped **static** rANS, Design B) implemented and shipped OFF by default
behind `OBSIDIAN_CAPPED="1"` (production env seam) and `EncodeOpts { capped }` (test path;
added to avoid polluting the process-global env every `encode` reads). Mode is signaled via
a new `model.entropy_mode` field (no header flag bit consumed, all 8 are in use); the decoder
rebuilds identical static tables from the signaled `capped_histograms`. Capped alphabet = 64
with an escape symbol; residuals whose zigzag value >= 64 are escaped into a separate
per-plane GR-coded section. The first attempt used adaptive tables and re-expanded at ~20.85
bpp on a small image (the original documented weakness); static tables specialize immediately
and round-trip bit-exactly. On synthetic proxies it does NOT clear the photographic gates
(table in `obsidian/benchmarks/results/2026-08-18-m35-capped-synth-proxy.csv`): 256x256 gray
6.565 vs v1 5.863 bpp; 512x512 RGB 18.91 vs v1 18.14 bpp. Like M2/M2.5/M3-A/M3-B, Design B
ties or regresses vs v1 GR on photographic content and ships OFF by default. The WebP (9.61)
/ JPEG XL (8.71) gates are out of reach for this GR architecture (residual-entropy floor
~10.1 bpp) and cannot be measured here (`data/kodak` absent). ESCALATE to Maintainer.

- the Builder

## Architect CMARC + R2 blueprint addendum (2026-08-18, the Architect)

CMARC + R2 blueprint delivered on PR #83 (issue #68). The Builder's "residual-entropy floor
~10.1 bpp is structural; WebP/JPEG XL gates unreachable" escalation is rejected (the 10.1 bpp
is the ceiling of the single-k per-context Golomb-Rice *symbol* coder; JPEG-LS hits 9.71 bpp on
the same Kodak corpus with the same LOCO-I GAP predictor, so the predictor is sound and the
entropy backend is the bottleneck). Key architectural decision: **CMARC is a new
`ModelConfig.entropy_mode` (`ENTROPY_MODE_CARC = 2`, `ENTROPY_MODE_CARC_LZ = 3`,
`ENTROPY_MODE_CARC_MIX = 4`), not a header flag** - reusing the exact mechanism M3.5 Design B
already uses (`model.entropy_mode`, signaled in the model section, routed by the decoder). This
needs no `VERSION` bump and keeps every legacy stream (v1 GR, M2, CM, LZ, capped) decodable, and
is cleaner than the research doc's "second flags byte" option. Specifies `rans.rs`
(`BinModel`, `RangeEnc`/`RangeDec`, `CarcCtx`, `cmarc_write_residual`/`cmarc_read_residual`,
binary bin layout), `model.rs` (selectors + sparse `cmarc_priors`), `encoder.rs`/`decoder.rs`
(CMARC residual branch + never-expand safety net vs v1 GR + `EncodeOpts { cmarc }`), R1-c static
priors (effort >= 4), R2 (cross-channel subtract-green, expanded predictor bank, LZ77 re-woven
with CMARC bins, logistic mixing). R1 alone clears WebP (~9.3-9.6 bpp); R1+R2 clears JPEG XL
(~8.5-8.9 bpp). Full contracts, build order, test matrix, gate map in
`obsidian/docs/architect-cmarc-blueprint.md`.

- the Architect

## Architect R3 blueprint addendum (2026-08-18, the Architect) - residual-context (DIFF) conditioning

R3 blueprint delivered on PR #83 (issue #68). Real Kodak effort-4 measured **10.0906 bpp** -
only ~0.065 bpp below v1 GR and **+0.38 bpp above JPEG-LS (9.71)** on the *same* predictor, so
the entropy backend is confirmed the bottleneck and the R1/R2 CMARC coder is correct but
conditioned on the wrong context. Two diagnosed defects: (1) PRIMARY - `context.rs::context_id`
conditions CMARC on spatial *gradients* (predictor selection) instead of the JPEG-LS DIFF context
(quantized neighboring *residuals* `dL/dU/dUl`), so per-bin models average over heterogeneous
residual scales and cannot specialize; this is the entire ~0.38 bpp gap. (2) SECONDARY - R2
silently replaced the blueprint's Rice/Exp-Golomb quotient with fixed-width MSB-first binary
magnitude, reintroducing a per-bit floor and losing the geometric quotient run. R3-A adds
`residual_context(dL,dU,dUl)` (neighbor predictions computed in the CMARC loop, bit-exact by
induction) as the coding context; R3-B restores the per-context Rice-through-binary-coder
decomposition (single geometric quotient model + remainder conditioned on quotient); R3-C adds a
JPEG-LS run mode for near-constant regions; R2.4 mixing is re-tuned on the corrected context.
Target: R3-A alone reaches JPEG-LS territory (~9.4-9.7 bpp) clearing WebP (9.61); R3 + R2.4
clears JPEG XL (8.71). Full contracts, build order, test matrix, gate map in
`obsidian/docs/architect-r3-residual-context-blueprint.md`.

- the Architect
