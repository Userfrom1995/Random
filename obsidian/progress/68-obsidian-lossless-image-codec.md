# Issue #68 - Obsidian lossless image codec (CMARC program)

Status: in_progress (R2.4 implemented; gates unmeasurable, code complete and verified)
Branch: opencode/issue68-20260818070512
PR: #83

## Goal
Beat PNG (13.05 bpp), WebP (9.61 bpp), and JPEG XL (8.71 bpp) on real Kodak
(effort 4 = 10.16 bpp baseline) with a learning, never-expanding, bit-exact
lossless codec. Single canonical Obsidian PR; never a second PR. Owner override:
do NOT merge until ALL three gates are beaten bit-exactly.

## Why the work is subtle (honesty checkpoint)
10.16 bpp is the ceiling of the single-k GR *symbol* coder on the Kodak
residual distribution, NOT the image. The CMARC program (R1..R2.4) targets the
residual distribution with a context-modeled binary range coder plus cross-bit,
cross-channel, expanded-bank, LZ, and logistic-mix conditioning. Real Kodak is
unmeasurable in this build env because `data/kodak` PPMs are absent (Factory
dispatched to provision; not yet present). All measurements below are on
synthetic near-Laplacian "smooth noise" proxies, which are an EASIER distribution
than Kodak and therefore a LOUSY proxy for the real gates.

## Stages (all shipped OFF by default behind opt-in seams + a never-expand safety net)
- M2 (GR with MED residuals, capped mode) - baseline, on by default.
- M2.5 (context mixing) - default GR backend since M2.
- M3-A / M3-B / M3.5 (MED predictors, M3.1, M3.2 constants) - shipped.
- R1 CMARC (per-(cid,bin) binary range coder, `ENTROPY_MODE_CARC=2`) - implemented.
- R2 CMARC cross-bit context (cross-bit conditioning) - implemented.
- R2.1 CMARC cross-channel (cross-channel prior) - implemented.
- R2.2 CMARC expanded bank (16-ctx, 12-bit magnitude) - implemented.
- R2.3 CMARC + LZ (RLE/gamma match coder, `ENTROPY_MODE_CARC_LZ=3`, force seam
  `OBSIDIAN_CARC_LZ_FORCE`) - implemented.
- R2.4 CMARC logistic context mixing (`ENTROPY_MODE_CARC_MIX=4`) - implemented THIS run.

### R2.4 design (from architect-cmarc-blueprint.md 5.4)
Blend two estimators in log-odds space with a per-bit learned logistic weight:
  - Estimator A: the per-(cid,bin) CMARC model (primary).
  - Estimator B: a per-bin coarse GR model (one BinModel per bin, shared across
    contexts) capturing the marginal distribution.
  - logit_mix = (w * stretch(pA) + (WSUM - w) * stretch(pB)) / WSUM.
  - Weight update: dw = (p_mix - bit) * (loA - loB) >> RATE_SHIFT, clamped to
    +/-WSUM; w += dw, clamped to [0, WSUM].
  - Both models + the per-bin weight are mirrored encoder/decoder (zero signaled
    bytes), so decode is exact.
  - Constants: MIX_WSUM = 4096, MIX_INIT_W = 2048, MIX_RATE_SHIFT = 22.

### R2.4 code
- `rans.rs`: `cmarc_stretch`, `cmarc_squash`, `cmarc_logit_mix`,
  `cmarc_mix_update_w`, `cmarc_mix_put`, `cmarc_mix_get`,
  `cmarc_mix_write_residual`, `cmarc_mix_read_residual`.
- `encoder.rs`: `EncodeOpts.carc_mix: Option<bool>`; env `OBSIDIAN_CARC_MIX`
  (opt-in) and `OBSIDIAN_CARC_MIX_FORCE` (force-select, mirrors CARC_LZ_FORCE);
  `code_planes` gains a `carc_mix: bool` param threaded through all 6 call
  sites; MIX candidate block in the never-expand safety net (keeps MIX only if
  `force_carc_mix || mix_total < best_total`); MIX coding branch allocates
  `mix_models`/`mix_w` and calls `cmarc_mix_write_residual`.
- `decoder.rs`: `is_mix` from `entropy_mode == ENTROPY_MODE_CARC_MIX`; MIX decode
  branch allocates `mix_models`/`mix_w` and calls `cmarc_mix_read_residual`.

### R2.4 verification
- `cargo build -p obsidian_core` / `-p obsidian_cli`: clean (only pre-existing
  snake_case/clippy style warnings; the `code_planes` too-many-args lint was
  already present before R2.4 and is accepted in this crate).
- `cargo test -p obsidian_core`: 106 passed (5 new R2.4 tests:
  `rans::cmarc_mix_residual_roundtrip` [bit-exact codec + mirrored model/weight
  lockstep], `encoder::r24_carc_mix_lossless`, `r24_carc_mix_off_by_default`,
  `r24_carc_mix_forced_decode_branch`, `r24_carc_mix_never_expands`).

### R2.4 measurement (honest, synthetic proxy only)
`bench-synth --count 10 --size 256 --noise 0.25 --effort 4`:
  - v1 = cm = carc = 9.6460 bpp (safety net fell back to GR; CMARC ties GR on
    this near-Laplacian content).
  - carc_mix (forced) = 13.2132 bpp -> +3.5672 bpp WORSE than GR.
  - The coarse per-bin model adds redundancy that GR already captures for free on
    this distribution; the logistic mix therefore loses. The never-expand safety
    net keeps GR, so enabling MIX never regresses a real file.
  - Conclusion: on available synthetic near-Laplacian content R2.4 does NOT beat
    GR, consistent with the architect's note that ~10.1 bpp is the ceiling for
    this synthetic distribution. Real Kodak (richer spatial/cross-channel
    structure) is the only meaningful test, and it is UNMEASURABLE here.

## Gates
- PNG 13.05 bpp: MET on real Kodak (baseline 10.16 < 13.05).
- WebP 9.61 bpp: UNMET and UNMEASURABLE (data/kodak absent).
- JPEG XL 8.71 bpp: UNMET and UNMEASURABLE (data/kodak absent).
- No synthetic proxy can claim these gates: Kodak is a HARDER distribution than
  smooth noise, so a synthetic win would not imply a real win.

## Blocker
`data/kodak` not present in build env. Factory was dispatched to provision it;
until then R2.4 (and R1..R2.3) cannot be measured against the real gates.

## Next actions
1. Provision `data/kodak` (Factory) so real effort-4 Kodak bytes can be measured
   for CARC_MIX (and the whole CMARC stack).
2. If real Kodak shows CARC_MIX still loses, the per-bin coarse estimator needs
   a better marginal (or the context features need more spatial/cross-channel
   signal); that is a research/architecture task, not a bug in R2.4.
3. Maintainer decides merge policy: R2.4 is safe to land off-by-default (no
   regression), but the three gates are NOT cleared, so per owner override the
   PR must stay open until Kodak measurement clears them.
