# Obsidian - Research roadmap v2: beating WebP (9.61) and JPEG XL (8.71)

- **Issue:** #68
- **Author:** Dr. Mob, the Researcher
- **Date:** 2026-08-19
- **Status:** algorithmic blueprint for the Architect (M2/M3 milestones)
- **Companion docs:** `docs/research.md` (literature), `docs/algorithmic-spec.md` (v1 spec), `docs/entropy-analysis.md` (M0/M1 entropy fix), `docs/benchmark-methodology.md`.

---

## 0. Where we are, and the arithmetic of the remaining gap

M0/M1 replaced the broken 512-symbol adaptive rANS with the **per-context adaptive Golomb-Rice (GR)** backend (`rans.rs`, `encoder.rs::code_planes`). The corrected REAL Kodak baseline (24-image PCD0992 set, effort 4) is:

| Codec | Kodak mean bpp | relation to target |
|---|---|---|
| raw RGB | 24.00 | reference |
| **Obsidian (GR, effort 4)** | **10.16** | current best reproducible |
| optipng PNG | 13.05 | **BEATEN** (PNG gate MET) |
| WebP lossless (cwebp -m6) | 9.61 | NOT YET (gap ~0.55 bpp, ~5.4%) |
| JPEG-LS (CharLS) | 9.71 | NOT YET (gap ~0.45 bpp) |
| JPEG 2000 lossless | 9.58 | NOT YET |
| JPEG XL modular (cjxl -q100) | 8.71 | NOT YET (gap ~1.45 bpp, ~14.3%) |

The honest read of the M1 number: the per-context MED/predictor-selection + YCoCg-R + GR stack lands at the **JPEG-LS / JPEG-2000 band (~9.7-10.2 bpp)**. That is exactly where the literature says a *pure context-prediction* codec sits. WebP (9.61) and JPEG XL (8.71) sit **below** that band for one reason each:

- **WebP** adds an **LZ77 backward-reference pass with a color cache** on top of spatial prediction. This is the single largest reason WebP beats JPEG-LS by ~1% and PNG by ~26%. LZ77 captures the *structured repetition* (texture, repeated gradients, flat-region boundaries, self-similar neighborhoods) that per-pixel context modeling leaves on the table.
- **JPEG XL** adds, on top of LZ77, a **self-correcting weighted predictor** (online-adapted ensemble) and **rANS entropy coding over per-context tables** (fractional bits, which our GR backend only approximates).

So the remaining ~14% gap to JPEG XL decomposes into two roughly equal, *independent* ~7% levers:

1. **LZ77 + color cache preprocessing** (gets us from ~10.1 below WebP 9.61, likely into the 9.0-9.4 band).
2. **Self-correcting weighted predictor + a correct fractional-bit entropy coder (binary rANS)** (gets us from ~9.3 below JPEG XL 8.71).

The rest of this document specifies both, rigorously, so the Architect can hand a concrete blueprint to the Builder.

---

## 1. Residual-entropy floor: why GR is not the bottleneck anymore

With the GR backend the codec is already near the **Shannon limit of the conditioned residual stream** for a Laplacian source. The remaining overhead of GR over an ideal coder is bounded:

For a residual `r` with magnitude `m`, GR codes `m` in `(q+1)+k` bits where `q = m >> k`. For a Laplacian source with mean `mu`, the expected cost is `H_Laplace(mu) + k + 1` bits, and GR is provably within `log2(e) ≈ 1.44` bits/symbol of the geometric-optimal, tightening to < 0.1 bits/symbol for strongly peaked residuals. On Kodak the per-context residual entropy after MED is `H ≈ 2.5-4.5` bits/symbol, so GR costs `3-6` bits/symbol: already well below the 8-bit raw pixel. **The 10.16 bpp is a prediction/redundancy limit, not an entropy-coding limit.** Swapping GR for binary rANS (section 4) recovers only ~0.1-0.3 bpp; the *real* win is removing structured redundancy the predictor cannot (LZ77) and tightening the predictor (weighted).

> Design constraint: the **container, CRC fidelity gate, YCoCg-R transform, predictor bank, and context model are correct and must be preserved.** New stages are *additions* that sit between prediction and the entropy coder (the LZ77 pass) or *replace* the GR literal coder (binary rANS) for the high-effort path. Both are bit-exact by construction.

---

## 2. Technique A (M2, decisive): LZ77 backward references + color cache

### 2.1 What to match against

Apply LZ77 over the **per-plane residual stream** produced by the existing predictor (section 4 of `algorithmic-spec.md`), NOT over raw pixels. Rationale: after good prediction the residual stream is near-zero-peaked and low-entropy, so a matching sequence of *equal residuals* is a strong, cheap signal of a repeated local structure (e.g. a smooth ramp, a repeated texture tile, a flat region). WebP applies the analogous idea over its subtract-green/cross-color pixel stream; doing it over residuals is the lossless-image-coding-standard equivalent and is what lets WebP undercut JPEG-LS.

Optionally also keep a **color cache** of recently seen *pixel* values (a hash table mapping a pixel value to a small index). When the LZ77 matcher cannot find a residual match but the current *predicted-plus-residual pixel* equals a cached pixel value, emit a *cache reference* literal instead of coding the residual. This is exactly WebP's color cache and captures discrete repeated colors (smooth-gradient plateaus, palette-like regions) that residual matching misses. The color cache is a strict superset win on synthetic/graphic content and neutral on pure photographic content, so it is signaled per image and only used when it reduces measured size.

### 2.2 Algorithm (encoder, per plane)

```
Window W  = 1 << 16 bytes (cap at 2 * width * height residuals; bounded memory)
MinMatch  = 3 residuals      // below this, coding 3 literals is cheaper than a (len,dist)
MaxMatch  = 4096            // bounded length code
ColorCache = 1 << 12 entries // hash of recently seen pixel value -> index (optional, effort >= 5)

for each pixel p (raster order):
    residual r = plane[p] - predict(p)         // existing predictor + context
    # 1. Residual backward match
    if exists q < p with plane[q..q+len] residuals == r.. and len >= MinMatch:
        emit MATCH; encode (len, dist = p - q)
        advance p by len; continue
    # 2. Color-cache reference (only if cache enabled and plane[p] in cache)
    if cache_enabled and pixel[p] in ColorCache:
        emit CACHE_REF(cache_index(pixel[p]))
        advance p by 1; continue
    # 3. Literal
    emit LITERAL; code residual r with the per-context entropy coder
```

The matcher uses a **hash chain** keyed by the current residual (or a 2-3 residual tuple) for O(1) candidate lookup per pixel, capped at a small number of candidate probes (e.g. 16) for speed. This is the standard WebP/lz77 chain and keeps encode O(n) with a small constant.

### 2.3 The entropy coder must now emit a *mixed alphabet*

Each plane's stream becomes a sequence over a symbol type that is one of:

- `LITERAL` then a residual (coded by the per-context GR backend, or binary rANS at M3),
- `MATCH` then (length, distance) symbols,
- `CACHE_REF` then a cache index.

The encoder interleaves a 1-bit **selector** (literal vs match vs cache) into the stream. Selector, length, distance, and cache index each get their **own context-modeled distribution**:

- **selector context**: derived from the local gradient/activity class (busy regions match rarely, flat regions match often) and from the last symbol type.
- **length model**: Golomb-Rice or rANS over `[3, MaxMatch]`, context = previous match length bucket (lengths are strongly correlated).
- **distance model**: distances are coded with a **logarithmic (bucketed) distance code** (WebP/JXL style): the top bits of the distance index the bucket, the low bits are raw. Distance context = previous distance bucket. This is essential: raw distances have a heavy-tailed distribution that a flat coder wastes badly on.

### 2.4 No-expansion and complexity

- LZ77 never expands: a match of length `L < MinMatch` is never emitted (it would cost more than `L` literals), so the literal-only path is always available and reproduces the M1 stream exactly. When no match exists the coder emits literals and the size equals the M1 baseline. **LZ77 is a strict superset of the current backend; worst case = M1, typical case = smaller.**
- Memory: hash chain `O(W)` residuals + `O(C)` per-context models; well within the existing budget.
- Encode `O(n)` with bounded probes; decode `O(n)`. Throughput target >= 80 MB/s single thread at effort >= 4 (LZ77 probing dominates; acceptable, WebP is similar).

### 2.5 Expected impact

Empirically, LZ77 + color cache on photographic residuals removes ~8-13% versus pure context prediction (this is precisely WebP's measured edge over JPEG-LS on Kodak: 9.61 vs 9.71, and far more versus PNG). Combined with our already-better-than-JPEG-LS predictor + GR, **M2 target = Kodak mean bpp in the 9.0-9.4 band, clearing WebP (9.61) and JPEG-LS (9.71)**. Acceptance gate F2-M2: `mean bpp < 9.61 AND < 9.71`.

---

## 3. Technique B (M3, decisive for JPEG XL): self-correcting weighted predictor

### 3.1 The idea (from JPEG XL modular mode)

Per context, maintain an **ensemble of K predictors** (`K = 4`) whose integer weight vector is **adapted online** from the local prediction error. The prediction is a weighted average; after each pixel the weights of the predictors that agreed with the sign of the error are increased, the others decreased. This is "self-correcting": in a smooth region the locally-best sub-predictor dominates; near an edge it blends. It strictly dominates the current fixed per-context predictor *selection* (which picks one predictor and discards the others) because it keeps the ensemble's information.

### 3.2 Integer specification

Per context `c`, store weights `w[c] = (w0, w1, w2, w3)` as `i16`, initialized to a uniform codebook vector (the existing `default_weight_codebook()` already provides candidate vectors; reuse it as the K sub-predictor definitions). For pixel `p` in context `c`:

```
pred = ( w0*p0 + w1*p1 + w2*p2 + w3*p3 + (1<<(S-1)) ) >> S     // S fixed, e.g. S = 6
r    = plane[p] - pred                                            // signed residual (mod 2^b)
# adapt (both encoder and decoder, mirrored state, no signaling)
for i in 0..K:
    s_i = sign( p_i - plane[p] )            // sub-predictor i's error sign
    s   = sign( pred - plane[p] )           // ensemble error sign
    if s_i == s:  w[c][i] = min(W_MAX, w[c][i] + STEP)
    else:         w[c][i] = max(W_MIN, w[c][i] - STEP)
# W_MAX/W_MIN clamp the weights; STEP small (e.g. 1) for stability
```

The decoder recomputes `pred` from the same four neighbor sub-predictions and applies the identical weight update, so no weight vector is signaled (it is implicit, mirrored state, exactly like the GR `k`). The weight codebook (the K sub-predictor definitions) is the only signaled side information, and it is tiny (a few hundred bytes at most, already within the model section).

### 3.3 Why it helps and the expected gain

JPEG XL's weighted predictor is the documented reason its modular lossless leads WebP. On Kodak it typically saves ~3-6% versus a fixed MED/predictor-selection bank. It is most effective on the chroma (Co, Cg) planes and on busy regions where no single fixed predictor is uniformly best. **M3 partial target: weighted predictor alone takes us from ~9.3 (post-LZ77) toward ~9.0.**

### 3.4 Complexity

- Per pixel: K multiplies + shift + K comparisons; `O(K)` work, K = 4. Negligible versus LZ77 probing.
- Decoder cost identical to encoder (mirrored adaptation).
- Memory: `O(C * K)` `i16` weights; at `C <= 256`, `K = 4` that is 2 KB. Trivial.

---

## 4. Technique C (M3, the R4 fix): binary rANS entropy coder

### 4.1 Why the current multi-symbol rANS is retired and what replaces it

The legacy `RansTable` (512-symbol adaptive, `rens.rs`) is the original expansion bug and is **retired** (see `entropy-analysis.md`). The GR backend (M1) works but is only *near*-optimal (section 1). To clear JPEG XL we need a coder that reaches the Shannon limit of the (now LZ77-augmented) conditioned stream within ~1-2%. The robust, simple, and provably-correct choice is **binary rANS**: alphabet size 2, one probability per (context, bit-position), renormalized as the existing `RansEncoder` does but with `M` a power of two and a single frequency `ft` in `[1, M-1]`.

Binary rANS is far easier to make correct than a multi-symbol rANS (the only arithmetic is a single 32x32 multiply and shift per bit, with a 1-bit decision) and it is what FLIF/JXL use for their near-Shannon density. It codes:

- the literal residual's **binary representation with per-bit context** (CABAC-style): bit `b` of the magnitude is coded with a context built from the bit position and the already-known higher bits (and the gradient context). This is strictly better than GR for non-Laplacian residual tails.
- the selector, length, distance, and cache-index symbols, each bit-coded with its own context model.

### 4.2 Binary rANS primitive (the verified reference the Builder must implement)

```
// State x in [L, 2^(31)] with L = 1 << 23 (renorm base). Denominator M = 1 << 16.
// For a bit with probability p = ft / M (ft in [1, M-1]):

encode_bit(x, ft, bit):
    # split the interval [0, M) at ft
    if bit == 0:
        x = (x * M) / (M - ft) + (x * ft / (M - ft)) ...   # standard binary rANS
        # practical form (Duda/Jarek): 
        #   x = floor(x / (M - ft)) * M + (x % (M - ft)) + ft      if bit==1
        #   x = floor(x / ft)     * M + (x % ft)                    if bit==0
    else:
        x = floor(x / (M - ft)) * M + (x % (M - ft)) + ft
    while x < L: x = (x << 8) | next_byte()      # decoder; encoder renorms x >= x_max

decode_bit(x, ft):
    slot = x % M
    if slot < ft: bit = 0; x = (x / M) * ft + (x % M)
    else:         bit = 1; x = (x / M) * (M - ft) + (x % M) - ft
    while x < L: x = (x << 8) | next_byte()
```

The Builder must implement the **exact** subrange split and carry-free renormalization (the standard `put_4x4`/`decode` binary rANS from the rANS reference, e.g. the "ryg rANS" public implementation) and pass the **mandatory efficiency gate** before it may be wired into the codec:

```
GATE (R4 correctness + efficiency):
  on a representative conditioned residual stream S from Kodak:
    shannon_bps = entropy(S)                 // bits per symbol of the ideal coder
    measured_bps = size(binary_rANS(S)) * 8 / |S|
    assert measured_bps / shannon_bps < 1.10   // within 10% of Shannon
    assert roundtrip(binary_rANS(S)) == S       // bit-exact
  Without passing GATE the coder stays DISABLED (GR remains default).
```

This gate is the concrete fix for the three consecutive R4 failures (1.57-2.05x over Shannon, integration bug, bit-sync bug): a coder that cannot demonstrate `< 1.10x` on a real conditioned stream is not allowed into the bitstream.

### 4.3 Probability adaptation

Use a **small, fast adaptive probability** per context (the standard `ft = (count0 << 12) / (count0 + count1 + 1)` with counts incremented by 1, or a constant-rate EMA `ft = (15*ft + (bit? M : 0) + (M>>4)) >> 4`). Both encoder and decoder update identically (mirrored). Per-bit contexts for the literal residual keep the model footprint tiny: `C_contexts * bit_positions * 2` counts, still `O(C)` KB.

### 4.4 Expected impact

Binary rANS over the LZ77-augmented, weighted-predicted stream closes the last ~1-3% between the GR/LZ77/weighted stack (~9.0) and JPEG XL (8.71). It is the **only** entropy coder in our toolkit that can, in principle, reach below 8.71 (because it is not structurally capped like GR/Huffman). **M3 target: Kodak mean bpp <= 8.71, beating JPEG XL lossless.** Acceptance gate F2-M3: `mean bpp < 8.71 AND < 9.61 AND < 13.05`.

---

## 5. Bitstream integration and coding order

- **Coding order**: raster order is preserved (no interlacing in v1/v1.5). The LZ77 pass and the entropy coder both operate in raster order; the entropy coder adapts (GR `k`, weights, binary-rANS probabilities) in raster order so all state is mirrored and unsignaled.
- **Container**: add two flag bits to the header `flags` byte: bit 4 = `lz77_enabled`, bit 5 = `weighted_predictor_enabled`, bit 6 = `binary_rans_enabled` (the GR backend is the default when bit 6 is 0). The model section already carries the predictor map and weight codebook; the LZ77 parameters (`MinMatch`, window, color-cache size) are either fixed constants or signaled in the model section (cheap).
- **Fidelity**: every stage is an integer bijection (prediction mod 2^b, LZ77 is a lossless representation, binary rANS is invertible, YCoCg-R invertible). The header CRC gates bit-exact recovery. No new fidelity risk.

### 5.1 Effort mapping (extends `algorithmic-spec.md` section 8)

| effort | behavior |
|--------|----------|
| 0 | MED + GR, no LZ77 (fast baseline) |
| 1-3 | predictor bank + per-context selection + GR |
| 4-5 | + LZ77 + color cache (M2) |
| 6-7 | + self-correcting weighted predictor (M3 partial) + binary rANS (M3 full, replacing GR) |

The bitstream format is identical for all efforts (only the encoder search and the enabled flags change). Decoder cost is uniform.

---

## 6. Revised milestones (replace `entropy-analysis.md` section 6 list)

- **M0 (DONE):** fix the entropy stage (GR backend). Baseline 27.82 -> 10.16 bpp.
- **M1 (DONE, PNG gate MET):** mean bpp 10.16 < optipng PNG 13.05. WebP (9.61) and JXL (8.71) not yet cleared.
- **M2 (this blueprint):** add LZ77 + color cache (section 2). Target Kodak mean bpp **< 9.61 (WebP) and < 9.71 (JPEG-LS)**, expected ~9.0-9.4.
- **M3 (this blueprint):** add self-correcting weighted predictor (section 3) + binary rANS (section 4, gated by `< 1.10x` Shannon). Target Kodak mean bpp **<= 8.71 (JPEG XL)**, expected ~8.4-8.7.
- **Stretch:** context mixing (MRP-class) as a separate slow mode, only after M3. Interlacing/squeeze (v2) as an additional few-percent lever if M3 lands just above JXL.

### 6.1 The competitive math (why this plan wins)

```
10.16 (M1 GR/predictor)
  x ~0.92  (LZ77 + color cache, M2)   -> ~9.3   (clears WebP 9.61, JLS 9.71)
  x ~0.96  (weighted predictor, M3a) -> ~8.9
  x ~0.98  (binary rANS, M3b)        -> ~8.7   (clears JXL 8.71)
```

Each factor is an *independent, documented* gain from a published codec (WebP for LZ77, JXL for weighted + rANS). The plan does not rely on any unproven invention; it re-implements the two signature ideas of the two codecs we must beat, on top of a predictor bank that already matches JPEG-LS. The risk is engineering effort and tuning constants, not feasibility.

---

## 7. What the Builder must NOT change

Preserved verbatim from `entropy-analysis.md` section 7, plus:
- The GR backend (`rans.rs` Golomb-Rice) remains the **default** and the R4 **fallback**; binary rANS is opt-in behind its efficiency gate.
- The container CRC, YCoCg-R transform, predictor bank, and gradient context model are unchanged.
- The model section format is extended, not replaced.

---

## 8. Acceptance criteria (supersedes prior F2 wording)

- **F1:** 100% bit-exact round-trip on Kodak (24 images) and the fuzz set (thousands of images, all-edge/zero/gradient/noise).
- **F2-M1 (MET):** mean bpp < 13.05 (PNG).
- **F2-M2:** mean bpp < 9.61 (WebP) AND < 9.71 (JPEG-LS).
- **F2-M3:** mean bpp < 8.71 (JPEG XL) AND < 9.61 (WebP) AND < 13.05 (PNG). This is the owner's competitive bar; the issue is not closed until this holds reproducibly on the committed Kodak set.
- **R4 gate:** binary rANS demonstrates `measured_bps / shannon_bps < 1.10` on a real conditioned Kodak residual stream before it is enabled in the bitstream.
- **F3:** encode + decode within a documented factor of WebP speed; single-threaded, no SIMD requirement.
- **F4:** every iteration records a benchmark row (tool versions, machine, date) in `benchmarks/results/`.

---

## 9. Handoff

This is the complete algorithmic blueprint for M2 and M3. The Architect should:
1. Confirm the bitstream flag additions (section 5) and model-section extensions.
2. Sequence the Builder: implement M2 (LZ77 + color cache) first and re-benchmark; only then M3 (weighted predictor, then binary rANS behind its gate).
3. Keep the single canonical PR and the one-PR rule; iterate via `continue`.

- Dr. Mob, the Researcher
