# Obsidian - Architect blueprint R3: residual-context (DIFF) conditioning + corrected Rice decomposition

- **Issue:** #68
- **Author:** the Architect
- **Date:** 2026-08-18
- **Mode:** Mode 2 iterative enhancement on PR #83 (branch `opencode/issue68-20260818070512`).
- **Supersedes/supplants in part:** `obsidian/docs/architect-cmarc-blueprint.md` (R1/R2). R2's CMARC backend is correct, lossless, and safe (never-expands), but on the real 24-image Kodak set at effort 4 it plateaus at **10.0906 bpp** - only ~0.065 bpp below v1 GR (10.1556) and **+0.38 bpp above JPEG-LS (9.71)**, which uses the *exact same* LOCO-I GAP predictor. This blueprint diagnoses why and prescribes the fix that actually reaches the WebP (9.61) and JPEG XL (8.71) gates.
- **Companion docs:** `docs/research-breakthrough.md`, `docs/architect-cmarc-blueprint.md`, `docs/m2-bias-run-architecture.md`, `docs/m3-lz77-weighted-predictor.md`, `docs/entropy-architecture.md`, `progress/68-obsidian-lossless-image-codec.md`.
- **In scope (Builder):** `context.rs` (residual-context / DIFF context), `rans.rs` (corrected per-context Rice-through-binary-coder magnitude), `encoder.rs`/`decoder.rs` (compute neighbor predictions and form the new `cid` in the CMARC loop). R2.1-R2.4 (cross-channel, predictor bank, LZ, mixing) compose unchanged on top.

---

## 0. Diagnosis: why 10.09 and not 9.3-9.6

The Researcher proved (correctly) that the ~10.1 bpp figure is the ceiling of the single-k Golomb-Rice *symbol* coder, not the image: JPEG-LS reaches **9.71 bpp on the same Kodak corpus with the same LOCO-I GAP predictor**. So the predictor is sound and the entropy backend is the bottleneck. R1/R2 replaced GR with CMARC (a context-modeled binary range coder) and added a WebP/JPEG XL-class pipeline, but real Kodak still measured **10.0906 bpp**. Two concrete defects explain the entire gap:

### 0.1 PRIMARY defect (the decisive ~0.4 bpp): CMARC conditions on the wrong context.

`context.rs::context_id` (`context.rs:170`) builds `cid` from the **spatial gradients** `g1 = t-l`, `g2 = l-tl`, `g3 = tl-t`, quantized and merged with an activity class. Those gradients are exactly the inputs LOCO-I uses to **select the predictor** - not the inputs a residual coder should use to model the residual itself.

JPEG-LS's regular-mode residual coder context is the **quantized neighboring *residuals*** (the "DIFF" context): `Q(|dL|)`, `Q(|dU|)`, `Q(|dUl|)` plus the sign triple `(sign(dL), sign(dU), sign(dUl))`, where `dL = L - pred(L)`, `dU = U - pred(U)`, `dUl = Ul - pred(Ul)` are the already-decoded residuals of the causal left/up/up-left neighbors. With the *same* predictor, this residual context is the *only* structural difference between Obsidian-at-10.09 and JPEG-LS-at-9.71.

Without it, CMARC's per-`(cid, bin)` models average over many heterogeneous residual scales (a smooth region and a detailed region share a gradient/activity bucket), so they cannot specialize to the local residual *distribution*. The "specialization-budget theorem" (research doc) still holds in principle, but the per-bin probabilities converge to a *smoothed, wrong* `p` - so the realized cost is `H(smoothed_p) + epsilon`, and `H(smoothed_p)` is far above the true per-symbol entropy. That is precisely the ~0.38 bpp we are missing. **Fixing the context (R3-A) is the single highest-leverage change and is what clears the WebP gate.**

### 0.2 SECONDARY defect: R2 silently dropped the blueprint's Rice/Exp-Golomb quotient.

`architect-cmarc-blueprint.md` R1.3.1 specified the magnitude as an **Exp-Golomb quotient + remainder** decomposition: `q = m >> k` coded binary (removing the unary `+1` overhead), `rem = m & (2^k-1)` coded as `k` bits. The R2 implementation (`cmarc_write_residual`, `rans.rs:1286`) instead codes the magnitude as **fixed-width MSB-first binary** over `mag_bits = ceil(log2(max-min+1))` positions, each position a per-`(position, window)` model.

Fixed-width binary reintroduces two redundancies the Rice quotient removes:
- Every residual pays the full `mag_bits` bit *slots*; the leading-zero bits are coded with per-position models whose probability is floored at `1/4095` (the Laplace prior), so each "free" leading zero still costs `H2(1/4095) ≈ 0.0035` bits - multiplied across millions of residuals this is a few centi-bpp.
- The geometric run of leading zeros (the dominant structure of a peaked residual) is not captured by a *single* geometric model; it is smeared across `mag_bits` independent position models, each of which must re-learn "usually zero", wasting adaptation budget and model count.

R3-B restores the per-context Rice decomposition (quotient run + remainder) but routes it through the *binary* range coder (so it stays adaptive and context-conditioned), exactly as JPEG-LS's QM coder does. This recovers the redundancy the blueprint promised to remove and lowers the per-context model footprint.

---

## 1. R3-A: residual-context (DIFF) conditioning (the decisive change)

### 1.1 Neighbor residual computation (encoder and decoder, identical)

In the CMARC coding loop (both `code_planes` and `decode_planes`), for the pixel at `(x, y)` the causal neighbors `L = (x-1, y)`, `U = (x, y-1)`, `Ul = (x-1, y-1)` are already decoded (raster order). For each, compute the prediction using the **same** per-context predictor map and `predict_clamped` the CMARC path already uses:

```rust
// after the current pixel's neighbor samples are known (L, U, Ul are decoded):
let pred_l  = predict_clamped(model.predictor(pi, cid_l),  &nb_l,  w, range);
let pred_u  = predict_clamped(model.predictor(pi, cid_u),  &nb_u,  w, range);
let pred_ul = predict_clamped(model.predictor(pi, cid_ul), &nb_ul, w, range);
let d_l  = (plane[idx_l]  as i32) - pred_l;
let d_u  = (plane[idx_u]  as i32) - pred_u;
let d_ul = (plane[idx_ul] as i32) - pred_ul;
```

where `nb_l/nb_u/nb_ul` are the neighborhoods of those neighbors (all already in the reconstructed buffer) and `cid_l/...` are their contexts. The decoder reproduces these bit-exactly by induction: at `(x, y)` its `L, U, Ul` equal the encoder's, so `d_l/d_u/d_ul` match, so the resulting `cid` matches. Lockstep is preserved.

Border handling: at `x == 0` or `y == 0` one or more neighbors are absent - fall back to `d = 0` (the neutral "no information" state), exactly as JPEG-LS treats border contexts.

### 1.2 Quantization and context assembly

Reuse a JPEG-LS-style magnitude quantization "QT" for each neighbor residual. A compact, cheap table (no per-image signal - it is a fixed, mirrored function):

```
Q(d): for |d| in 0 -> 0, 1 -> 1, 2..3 -> 2, 4..7 -> 3, 8..15 -> 4, 16..31 -> 5, 32..63 -> 6, 64..127 -> 7, 128+ -> 8
```

Combine into the residual-context index:

```rust
pub fn residual_context(d_l: i32, d_u: i32, d_ul: i32) -> usize {
    let ql  = quantize_residual(d_l);   // 0..=8
    let qu  = quantize_residual(d_u);   // 0..=8
    let qul = quantize_residual(d_ul);  // 0..=8
    let sl  = (d_l < 0) as usize;      // 0/1
    let su  = (d_u < 0) as usize;
    let sul = (d_ul < 0) as usize;
    // pack: signs (3 bits) + 3 magnitudes (each 4 bits) -> 15 bits, 0..=32767.
    // Reduce via a small LUT (SignSymmetryLut-style) to a compact id, mirroring the
    // existing gradient LUT reduction so symmetric sign flips share a context.
    RC_LUT.reduce((sl | (su<<1) | (sul<<2) | (ql<<3) | (qu<<7) | (qul<<11)) as usize)
}
```

The CMARC coding context becomes:

```rust
let rc = residual_context(d_l, d_u, d_ul);
let act = activity_class(g1, g2, g3);          // keep the existing activity refinement
let cid = rc * ACTIVITY_CLASSES + act;          // replaces the gradient-only base
```

The per-context **predictor selection** is unchanged (still driven by the gradient/activity map from `analyze`); only the *residual-coding* context changes. This is the exact JPEG-LS separation: gradient context picks the predictor, residual context models the residual.

### 1.3 Model budget

The residual context is **not signaled** (mirrored); only the optional static priors (R1-c) touch the bitstream. `RC_LUT` reduction targets `N_RC ≈ 256` residual contexts; with `ACTIVITY_CLASSES = 4` that is ~1024 contexts per plane, all in RAM. With the R3-B bin layout (section 2) the per-context bin count drops to ~16, so the runtime model is ~32 KB/plane in RAM and **zero bytes in the file** (or a sparsified static-prior table well under `MODEL_SIZE_FRACTION`). No header flag, no `VERSION` bump - the context assembly is internal to the CMARC path and every legacy stream still decodes.

### 1.4 Expected impact

This is the proven JPEG-LS delta. Target after R3-A alone: **~9.4-9.7 bpp** on real Kodak (JPEG-LS territory), clearing the WebP gate (9.61). If R3-A alone lands at, say, 9.6-9.7, R3-B/C finish the margin.

---

## 2. R3-B: corrected per-context Rice magnitude through the binary coder

Replace `cmarc_write_residual`'s fixed-width MSB-first loop (`rans.rs:1304-1311`) with the blueprint's Rice decomposition, but keep it adaptive via the binary range coder:

```rust
// magnitude m, per-context k from CarcCtx (EMA of |r|), unchanged logic:
let k = ctx.k();
let q = m >> k;                       // Rice quotient
let rem = m & ((1u32 << k) - 1);      // Rice remainder
// Quotient: code a run of `q` zero-bits then a stop-one, using ONE geometric
// per-context model (CMARC_BIN_Q_STOP), then the floor(log2(q+1)) VALUE bits
// of (q+1) conditioned on the run length via the trailing-window state.
code_binary_run(enc, w, models, cid_bins, q);
// Remainder: code the k bits of `rem` LSB-first, each a per-(cid, bin) model
// indexed by (position, quotient-state window). This captures non-uniform rem.
for j in 0..k { enc.put(w, &mut models[cid_bin(cid, bins, CMARC_BIN_REM + j)], (rem>>j)&1 == 1); }
```

- **Quotient model is geometric and single:** the run of `q` zeros + stop bit costs `~H_geom(q) ≈ log2(q+1) - 1` bits through one model, with no per-bit floor on the whole run (the floor applies once, at the stop-model, not once per position).
- **Remainder is conditioned on the quotient** (via the same trailing-window state machine already in R2), so a large quotient biases the remainder models toward the appropriate sub-distribution - exactly the cross-bit conditioning R2 added, now applied to the *correct* (Rice) decomposition.
- **Sign** remains one binary bit (the `CMARC_BIN_SIGN` model).

New bin layout (replaces the `mag_bits * CMARC_MAG_STATES` region):

```rust
pub const CMARC_BIN_ZERO: usize = 0;
pub const CMARC_BIN_SIGN: usize = 1;
pub const CMARC_BIN_Q:    usize = 2;   // quotient run/value region (bounded, e.g. 2 + 14 = 16 bins)
pub const CMARC_BIN_REM:  usize = 2 + CMARC_Q_BINS;  // k remainder models (k <= GR_MAX_K)
pub fn cmarc_bins_per_ctx() -> usize { 2 + CMARC_Q_BINS + GR_MAX_K as usize }
```

This **reduces** bins-per-context versus the R2 layout (which used `2 + mag_bits*4`, up to `2 + 64 = 66` for `mag_bits=16`), shrinking the model table and the static-prior footprint while improving compression. `cmarc_mag_bits` / `CMARC_MAG_WIN` become unused for the magnitude path and are retained only for the LZ literal region (section 4).

### 2.1 No-expansion proof (unchanged)

Each bin is a convergent binary model with a `+C` Laplace start bounded by `log2(2C)`; photographic residuals have `H(p) < 8` bits/symbol, strictly below the raw 8-bit pixel. The early-symbol overhead decays within `O(C)` symbols, exactly as GR/CMARC. The Rice decomposition only lowers the per-symbol cost, so the never-expand net still holds.

---

## 3. R3-C (follow-on): run mode for near-constant regions

JPEG-LS separates a **run mode** (when both `d_l` and `d_u` quantize to 0, i.e. the local neighborhood is near-constant) from regular mode. In run mode the residual coding cost collapses to a single run-length gamma (through the binary coder) plus a copy of `prev_val`, removing the per-pixel zero/sign/quotient/remainder cost on flat and low-activity runs. This adds margin toward JPEG XL and is cheap: a binary `run_flag` bin gated on the residual context, then an Elias-gamma run length (reuse `cmarc_lz_write_gamma` / `read_gamma`). Decoder copies `prev_val` for the run body (exact by induction). Add only after R3-A/B are measured; it is dormant behind the never-expand net.

---

## 4. Integration with R2.1-R2.4 (no changes to those stages)

- **R2.1 cross-channel:** subtract-green / YCoCg-R still apply first; the residual context is computed on the *transformed* planes, so it decorrelates chroma automatically. Unchanged.
- **R2.2 predictor bank:** the per-context predictor map still selects the predictor; R3-A only changes which context *codes* the residual. Unchanged.
- **R2.3 LZ:** the CMARC-LZ literal residual uses the same `cid` (now residual-context) and the same Rice decomposition; matches win more often because the literal baseline is cheaper. Unchanged except the literal now goes through R3-B.
- **R2.4 mixing:** logistic mixing blends the now-correct per-`(cid, bin)` estimates; with a correct base context the mix has signal to exploit, so R2.4 should finally beat the single model (its earlier +3.57 bpp regression was on the smoothed/distorted R2 context). Re-measure after R3-A/B.

The never-expand safety net (keep `min` over {GR, CMARC, CARC_LZ, CARC_MIX}) is preserved and now selects CMARC only when the corrected context + Rice actually win.

---

## 5. Acceptance gates (updated)

- **M1 / WebP (R3-A, likely R3-A+B):** Kodak effort-4 mean bpp **< 9.61**, bit-exact round-trip preserved, `cargo test --workspace` green. This is the JPEG-LS delta and is expected to clear the gate.
- **M2 / JPEG XL (R3 + R2.4):** Kodak effort-4 mean bpp **< 8.71**, same correctness/CI gates.
- **No-expansion invariant:** preserved by the Rice decomposition + never-expand net; flag-off GR/capped fallbacks stay byte-identical.
- **Measurement blocker (Factory):** `obsidian/benchmarks/data/kodak/` PPMs must be present (the `kodak.sha256` checksum exists but the corpus is currently absent in the working tree - the Factory must keep it provisioned). `run_kodak.sh` at effort 4 reads it; the Builder records `benchmarks/results/2026-08-18-real-kodak-r3.csv` and asserts the gates. The orphan-`main` history break is the Maintainer/Factory's job and is non-blocking for the codec work (the branch is preserved).

---

## 6. Build order for the Builder

1. **R3-A:** add `residual_context` + `quantize_residual` + `RC_LUT` to `context.rs`; compute `d_l/d_u/d_ul` (neighbor predictions) in the CMARC loop of `encoder.rs`/`decoder.rs`; form `cid = rc * ACTIVITY_CLASSES + act`. Keep the R2 fixed-width magnitude for this step (isolate the context win). Re-measure real Kodak; assert < 9.61 (WebP). This alone should clear one gate.
2. **R3-B:** switch `cmarc_write_residual`/`cmarc_read_residual` from fixed-width binary to the per-context Rice-through-binary-coder decomposition (new bin layout, `cmarc_bins_per_ctx()`). Re-measure; expect a few more centi-bpp.
3. **R3-C:** run mode for near-constant contexts. Re-measure.
4. **R2.4 re-tune:** re-run logistic mixing on the corrected context; assert < 8.71 (JPEG XL) by the end.
5. Record a benchmark row after each stage; keep all prior M2/M2.5/M3 seams OFF by default.

---

## 7. Test matrix additions (Builder)

| Area | Test |
|---|---|
| residual-context | a smooth-region block and a detailed block produce *different* `cid`s; `residual_context` is sign-symmetric (mirrored LUT) |
| neighbor pred lockstep | encoder/decoder compute identical `d_l/d_u/d_ul` on synthetic Kodak; `cid` equal at every pixel |
| rice decomposition | `cmarc_write_residual`/`cmarc_read_residual` round-trip for `r` in `[-4096, 4096]` with the new bin layout; encoder/decoder models stay equal |
| rice vs fixed-width | on the Laplacian proxy the Rice decomposition costs <= the old fixed-width binary (removes the per-bit floor) |
| no-regression | flag-off (GR) byte-identical to v1 GR; all legacy streams still decode |
| gate | Kodak effort-4 mean bpp recorded; assert < 9.61 (WebP) after R3-A/B; assert < 8.71 (JPEG XL) after R3 + R2.4 |

Existing GR, rANS, M2, M2.5, M3, M3.5, R1, R2.1-R2.4 tests are retained unchanged.

---

## 8. Why this is the correct next step (and the only one left)

Every codec that reaches < 9.71 bpp on Kodak uses (a) a good predictor bank with per-context selection, and (b) a residual coder whose context is the **decoded neighboring residuals** (JPEG-LS DIFF context) fed to an adaptive arithmetic/range coder. Obsidian already has (a). R1/R2 delivered (b)'s *coder* but conditioned it on the *predictor-selection* context instead of the *residual* context, and silently swapped the Rice quotient for fixed-width binary. R3-A fixes the context (the proven JPEG-LS delta, worth ~0.38 bpp) and R3-B restores the Rice decomposition (the blueprint's promised redundancy removal). Together they place Obsidian in JPEG-LS territory (≈9.4-9.7 bpp) and, with R3-C + R2.4, below JPEG XL (8.71). The "~10.1 bpp floor" was the GR coder's floor; after R3 it is the image's floor that governs.

- the Architect
