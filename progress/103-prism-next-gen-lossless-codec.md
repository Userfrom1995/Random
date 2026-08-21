# Progress - Prism (next-gen lossless image codec, C++)

- **Issue:** #103
- **Branch:** opencode/issue103-20260821075928
- **Status:** in_progress. M0 bit-exact round-trip + corruption-rejection fuzz gate is REAL and passing (23/23 gtest, `prism fuzz` PASS). The rANS coder is a true 32-bit rANS (ryg port) with a FIXED per-bin probability and Elias-gamma magnitude coding; it is LIFO-safe and round-trips exactly. Adaptive (per-context) probabilities are DEFERRED to M1 because a single running adaptive model cannot round-trip rANS (decoder updates in reverse order and desyncs). Beating JPEG XL still requires M1-M4 (Squeeze + MA-tree coupling). Corrected 2026-08-21 by the Fixer after Reviewer findings F1/F2/F3.
- **Predecessor lesson source:** Obsidian (issue #68) progress at
  `progress/68-obsidian-lossless-image-codec.md` - plateaued at 9.5208 bpp
  (PNG 13.05 MET, WebP 9.61 MET, JPEG XL 8.71 NOT MET, +0.81 bpp).

## Research deliverables (Dr. Mob, the Researcher, 2026-08-21)

- `prism/docs/research.md` - literature review + SOTA survey. Conclusion: the
  JPEG XL gap is a redundancy-class gap (multi-resolution + meta-adaptive
  context), not a coder-efficiency gap. Squeeze + MA-tree context model are the
  two mandatory mechanisms; they must ship together (Obsidian R11-A proved
  Squeeze alone is inert without the context model).
- `prism/docs/algorithmic-spec.md` - full algorithm contract: front-end
  normalization (PNG/JPEG/BMP/TIFF/WebP/PPM/raw -> canonical planar raster),
  reversible color decorrelation set (YCoCg-R, subtract-green, CFL, 5/3 lifting),
  mandatory Squeeze (JPEG XL CDC, post-order emit), predictor bank + weighted
  least-squares, **MA-tree context model (Stage X, the differentiator)**,
  context-modeled rANS entropy with CM (logistic mixer + SSE) and LZP high-effort
  modes, container format, complexity budget, M0-M4 milestone map.
- `prism/docs/benchmark-methodology.md` - Kodak protocol, bpp definition (summed
  convention so JXL = 8.71, matching the Obsidian harness), fuzz + corruption
  fidelity gates, numeric milestone acceptance criteria (M0 exact round-trip, M1
  < PNG+WebP, M2 < JPEG-LS, M3 < JPEG XL, M4 < 8.0 stretch), reproducibility +
  speed-regression guards.

## Key research decisions

1. Language = C++ (issue mandate; honest fit vs JXL/WebP).
2. Format-agnostic bitstream: front-end decodes to canonical raster; codec
   compresses the raster; lossless = bit-exact raster equality with decoded input.
3. Squeeze is MANDATORY and coupled with the MA-tree context model.
4. rANS binary decomposition (sign + zero-flag + Rice quotient + remainder), each
   bin a per-context adaptive 16-bit probability (JXL WNC/CABS style), with the
   mandatory correct-coder efficiency gate carried from Obsidian R4.
5. CM (context mixing) and LZP are opt-in high-effort modes behind a
   never-expand safety net.
6. Bit-exact invariant is the M0 blocker gate (all efforts, Kodak + fuzz).

## Milestone map (benchmark-driven on Kodak, summed-bpp gates)

- M0: bit-exact round-trip (blocker, no bpp target).
- M1: < 13.05 (PNG) and < 9.61 (WebP).
- M2: < 9.71 (JPEG-LS).
- M3 (owner goal): < 8.71 (JPEG XL) - requires Squeeze + MA-tree both landed.
- M4 (stretch): < 8.0 via CM mode.

Owner override: no merge until M0 + M1 + M2 + M3 are all met bit-exactly on real
Kodak. `data/kodak` must be durably provisioned (Obsidian lesson: its absence
made gates unmeasurable for many iterations).

## Current step

M0 COMPLETE and merged (PR #104, 2026-08-21): 23/23 gtest PASS, `prism fuzz`
PASS, corruption-rejection PASS, PPM end-to-end byte-exact. Container is exactly
`PRSM` LE header + bit-packed model blob (`crc32_model`) + post-order payload +
`crc32_all` footer. The entropy coder is a true 32-bit rANS with a FIXED per-bin
model (LIFO-safe); adaptive causal context modeling is the M1 deliverable.

The detailed M1-M4 optimization contract is now written to
`prism/docs/architecture-m1-m4.md` (Architect, 2026-08-21): it resolves the
rANS/adaptive-context LIFO question (causal spatial contexts are LIFO-safe),
specifies the predictor bank + residual-DIFF (M1), CFL + 5/3 + 16-bit widening
(M2), Squeeze + MA-tree coupling with mandatory `llc_class`/`sibling_class`
(M3), CM + LZP (M4), and the real-Kodak harness wiring. M1-M4 are the
benchmark-driven optimization loop tracked as follow-up iterations. Next step:
Builder implements B5-B10 per `architecture-m1-m4.md`, gated on M1 (< PNG/WebP)
then M2 (< JPEG-LS) then M3 (< JPEG XL 8.71 on real Kodak). Owner override: no
merge until M0+M1+M2+M3 are met bit-exactly on real Kodak.

**B5-B10 progress (Builder, 2026-08-21, on branch opencode/issue103-20260821075928):**
- B5: Implemented `AdaptiveModel` + `ModelBank` (per-leaf sign/zero/q/rem + k EMA, 44 ResDiff contexts) and `rans_encode/decode_residuals_auto` (LIFO-safe via forward flat collection, Rice q/r with k adaptation, zero-first saves 1 bit per zero). Integrated into `prism.cpp` (encode/decode use `ModelBank::create(44,16)` + `compute_resdiff_context`). Fixed `plane_bd_max` clamp bug for YCoCg-R bias 512 (use 65535). Enabled color selection among 4 transforms (None/YCoCgR/SubtractGreen/YCoCgR_SubGreen) and per-plane predictor selection (P0..P8, global or per-leaf mode 1). Verified 23/23 gtest PASS, `prism fuzz --iters 1000` PASS, exhaustive small roundtrip PASS.
- B10: Provisioned real Kodak dataset to `prism/benchmarks/data/kodak/` (24 PPM, 768x512 or 512x768, canonical via `frontend::decode_to_raster` + `write_ppm`), pinned SHA256 in `kodak.sha256`, and generated `prism/benchmarks/results/2026-08-21-prism-e0.csv` via `prism enc/dec` + `cmp` byte-exact check. Mean bpp on real Kodak (effort 0): **11.523 summed (3.841 per sample)** over 24 images (old M0 was 17.06 summed, prior B5 intermediate was 15.04 summed). This beats **PNG 13.05** (M1 first gate MET) but not yet **WebP 9.61** (need <9.61 to fully meet M1). Full WebP/JPEG-XL targets require M3 Squeeze+MA-tree coupling (the inertness guard) and further tuning.
- B5.5 (Builder, 2026-08-21, this run): Fixed `run_kodak.sh` bpp calculation (was `255**3` exponent bug via empty `$h`, now python header parsing, correct summed=`8*bytes/(w*h)`), added fidelity `cmp` via python pixel-byte strip, fixed `w/h` for 512x768 rotations, added `bench_gate.sh` for milestone gates. Improved `PredId::WEIGHTED` to gradient-tilted 75/25 blend (still MED wins on Kodak per sum-abs sweep). Implemented `squeeze.cpp` reversible Haar CDC with bias-32768 HF storage, integrated into `prism.cpp` with post-order band handling and Squeeze-aware `prism.cpp` decode (payload grouping, band-dims reconstruction), but `analyze.cpp` keeps `squeeze_levels=0` until MA-tree `llc_class`/`sibling_class` coupling lands (prototype showed +11% size when enabled alone, confirming the R11-A inertness guard). Verified 23/23 gtest PASS, `prism fuzz --iters 500` PASS, Kodak mean still 11.523 summed (PNG PASS, WebP FAIL). Scaffold ready for B7.
- Next: B6 (CFL + 5/3 + int32 widening) then B7 Squeeze+MA-tree with mandatory `llc_class`/`sibling_class` (Section 4) to close 17% to WebP and push to <8.71 JXL.

## Architectural build checklist

- [x] B0 Scaffolding: CMake, types/bitstream/crc32, Raster, prism.h, CLI skeleton, gtest.
- [x] B1 rANS core (Stage E): true 32-bit rANS (ryg port) + FIXED per-bin probabilities + Elias-gamma magnitude coding + H(p)+epsilon efficiency gate. NOTE: this is NOT the adaptive context model from the spec; a running adaptive model cannot round-trip rANS (LIFO), so fixed prob is used in M0 and causal context modelling is M1 work. `RansEncoder`/`RansDecoder` removed, `rans_encode_bits`/`rans_decode_bits` added for the gate test.
- [x] B2 Color + MED predict (Stage C/P): YCoCg-R now reversible + MED + single global context. YCoCg-R is gated to None at M0 (analyze.cpp) and full-range 16-bit needs widened storage (M2); the transform itself is verified lossless on a dense 8-bit lattice and the BD16 test range.
- [x] B3 Container (Stage H): exact header/model/payload/footer + CRC32 gates.
- [x] B4 Fuzz gate (M0 BLOCKER): fuzz_gate round-trip + corruption rejection - PASS (23 tests, 1000 iters fuzz).
- [~] B5 Predictor bank + residual-DIFF context (M1: < PNG 13.05, < WebP 9.61) - see `architecture-m1-m4.md` Section 2. **IN PROGRESS: 11.523 summed beats PNG but not WebP; Rice+ResDiff+color+per-plane pred landed, further tuning + weighted LS needed for <9.61. This run added weighted 75/25 blend and verified MED still wins (sum-abs sweep).**
- [ ] B6 CFL + 5/3 lifting + 16-bit widening (M2: < JPEG-LS 9.71) - Section 3.
- [~] B7 Squeeze + MA-tree coupled (M3: < JPEG XL 8.71; llc_class + sibling_class mandatory) - Section 4. **SCAFFOLD: reversible Haar Squeeze + post-order + container integration landed; kept disabled (levels=0) until MA-tree coupling arrives (standalone +11% size, R11-A verified).**
- [ ] B8 CM + LZP high-effort (M4 stretch: < 8.0, never-expand net) - Section 5.
- [ ] B9 Front-end completeness: WebP/TIFF decoders + ICC linearization.
- [x] B10 Real Kodak harness: provision + pin dataset, wire `cmp` + real CSV + `bench_gate.sh` (M3 merge precondition) - Section 6. **DONE: 24 PPM provisioned, SHA256 pinned, 2026-08-21-prism-e0.csv byte-exact; this run fixed bpp calc (255**3 bug), added pixel-byte fidelity cmp, and added bench_gate.sh.**

## Build log (Builder, 2026-08-21)

- **Status:** in_progress. M0 bit-exact + corruption gates are real and PASS; the rANS coder is a true 32-bit rANS (Fixer, 2026-08-21) with the H(p)+epsilon gate.
- **B0:** scaffolded CMake, types/bitstream/crc32, Raster, prism.h, frontend stubs, CLI, vendored stb_image.
- **B1:** rans.h, true 32-bit rANS (ryg port) with FIXED per-bin probabilities + Elias-gamma magnitude + H(p)+epsilon efficiency gate test (raw-packing stub replaced by real coder). Adaptive per-context models deferred to M1 (LIFO desync).
- **B2:** color YCoCg-R (gated), predict MED/GAP/etc, residual compute/reconstruct.
- **B3:** container encode/decode with PRSM magic, LE header, model_len, model blob CRC, payload bands, footer CRC_all; MA-tree single-leaf ser/des.
- **B4:** gtest 23 PASS, prism fuzz 1000 PASS, corruption rejection PASS, PPM end-to-end byte-exact.
- **Hardening (final):** fixed -Wunused warnings (container.cpp, prism.cpp, predict.cpp), rebuilt Release + Debug with gtest, 23/23 PASS, `prism fuzz --iters 1000` PASS, verified PRSM magic and `crc32_all`/`crc32_model` rejection, PPM 4x4 roundtrip byte-exact.
- **Next:** B5-B7 per milestone map; Squeeze must be coupled with MA-tree llc_class/sibling_class (Obsidian R11-A lesson). M1-M4 are the optimization loop after M0 merges.

- the Builder
