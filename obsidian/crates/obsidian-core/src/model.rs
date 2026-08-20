//! The learned model: per-context predictor maps, weight selection, static
//! histograms, and model serialization.
//!
//! The analysis pass (effort >= 1) runs once over the transformed planes and
//! picks, for every context, the predictor that minimizes the summed residual
//! magnitude. At effort >= 4 the Weighted predictor is enabled with a
//! per-plane weight vector chosen from a small codebook. At effort >= 6 the
//! pass also collects per-context symbol histograms for static rANS tables.

use crate::color::{Palette, PlaneRange, TransformChoice};
use crate::context::{zigzag, Alphabet, ContextModel, ContextParams};
use crate::error::CodecError;
use crate::image::Channels;
use crate::predict::{
    default_weight_codebook, neighbors, predict_clamped, solve_weighted_tree, weight_context,
    PredictorId, WLeaf, WC_LEAVES, WC_MIN_SAMPLES, UNIT_LEAF, WeightVec,
};
use crate::rans::{RansTable, CAPPED_SYMBOLS, CAPPED_ALPHABET};
use std::io::{Read, Write};

/// Per-plane model: a predictor map over all contexts plus the chosen weight
/// vector index.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PlaneModel {
    pub map: Vec<u8>,
    /// Index into the weight codebook, or `u8::MAX` when no Weighted use.
    pub weight_index: u8,
}

/// Entropy backend selector signaled in the model section. The 8-bit header
/// `flags` byte is exhausted (channels/transform/palette + ENTROPY_GR, GR_M2,
/// GR_CM, GR_LZ), so the fine-grained entropy mode lives here instead of as a
/// header flag. The decoder reads it and routes the per-plane residual pass.
pub const ENTROPY_MODE_GR: u8 = 0;
/// M3.5 Design B: per-context adaptive rANS over a capped residual alphabet with
/// an escape-to-Golomb-Rice fallback for large residuals (capped-and-escaped
/// static/adaptive rANS, `obsidian/docs/entropy-architecture.md` section 7).
pub const ENTROPY_MODE_CAPPED: u8 = 1;
/// R1 CMARC: context-modeled adaptive binary range coder (the WebP/JPEG XL
/// backend). Replaces the single-k GR *symbol* coder with a per-`(cid, bin)`
/// binary range coder so the cost is `H(p) + epsilon` rather than `H(p) + O(1)`.
/// Signaled via `entropy_mode` (not a header flag), so every legacy stream
/// decodes unchanged. See `obsidian/docs/architect-cmarc-blueprint.md`.
pub const ENTROPY_MODE_CARC: u8 = 2;
/// R1 + R2.3: CMARC literals with an LZ77 match layer (match flag/length coded
/// by CMARC bins). Planned (R2); reserved here so streams decode.
pub const ENTROPY_MODE_CARC_LZ: u8 = 3;
/// R1 + R2.1/2.2 + R2.4: CMARC + cross-channel + expanded predictor bank +
/// logistic mixing. Planned (R2); reserved here so streams decode.
pub const ENTROPY_MODE_CARC_MIX: u8 = 4;
/// R6-B color cache (Component A): CMARC residuals with a per-plane LRU color
/// cache of reconstructed sample values. A literal whose value hits the cache is
/// coded as a `cache_flag` (1) plus a small cache-index code, instead of the full
/// residual, exploiting the repeated-value redundancy WebP/JPEG XL use. Signaled
/// via `entropy_mode` (no header flag bit), so every legacy stream still decodes.
/// See `obsidian/docs/architect-r6-corrected-blueprint.md` Component A.
pub const ENTROPY_MODE_CARC_CACHE: u8 = 6;

/// The complete signaled model.
#[derive(Clone)]
pub struct ModelConfig {
    pub transform: TransformChoice,
    /// R2.1 cross-channel subtract-green decorrelation (`R'=R-G, G'=G, B'=B-G`)
    /// applied to the first three planes before `transform`. Signaled in the
    /// model section (zero extra header bit); the decoder applies the inverse
    /// after the inverse color transform. Mirrored: both sides read it from the
    /// model, so no cross-process env must be set.
    pub cross_channel: bool,
    pub palette: Option<Palette>,
    pub context: ContextParams,
    pub context_count: usize,
    pub planes: Vec<PlaneModel>,
    pub weight_codebook: Vec<WeightVec>,
    /// Static per-context histograms, `[plane][context]`, when effort >= 6.
    pub static_histograms: Option<Vec<Vec<Option<Vec<(u32, u32)>>>>>,
    /// Selected entropy backend (see `ENTROPY_MODE_*` constants). 0 = Golomb-Rice.
    pub entropy_mode: u8,
    /// Per-context histograms over the capped residual alphabet (`CAPPED_SYMBOLS`)
    /// for the M3.5 Design B capped-and-escaped rANS backend. Built from the same
    /// analysis residuals as the coding pass and signaled in the model section so
    /// the decoder rebuilds identical static tables; `None` when Design B is off.
    pub capped_histograms: Option<Vec<Vec<Option<Vec<(u32, u32)>>>>>,
    /// R1-c static per-`(cid, bin)` Laplace priors for the CMARC binary coder.
    /// Sparse `[plane][cid]` -> list of `(bin, n1, n0)` count pairs (only
    /// contexts/bins with counts present). Signaled in the model section so the
    /// decoder seeds its `BinModel`s from `BinModel::from_counts`; `None` when the
    /// CMARC priors are off (the coder still works from the uniform prior).
    pub cmarc_priors: Option<Vec<Vec<Option<Vec<(u32, u32, u32)>>>>>,
    /// R3-A JPEG-LS DIFF residual context for the CMARC coding context. When set,
    /// the CMARC coding context is the quantized neighboring-residual context
    /// (see `context::residual_context`) instead of the gradient context. Signaled
    /// in the model section (zero extra header bit); the per-image selection
    /// (computed in `analyze`) keeps it on only when it actually wins so a
    /// regression can never ship. Mirrored: both sides read it from the model.
    pub cmarc_residual_ctx: bool,
    /// R3-C JPEG-LS-style run mode for the CMARC coder. When set, near-constant
    /// regions (both causal neighbor residuals quantize to ~0) are coded as a
    /// single run length instead of per-pixel residuals. Signaled in the model
    /// section; the never-expand safety net keeps it on only when it actually
    /// wins, so a regression can never ship. Mirrored: both sides read it from
    /// the model (zero extra header bit).
    pub cmarc_run: bool,
    /// R11-D MA-tree-lite: when set, the CMARC coding context folds a coarse
    /// local-gradient bucket into the residual-DIFF context (see
    /// `context::combined_ma_context`), so the binary coder conditions on both
    /// the neighboring residual pattern and the local gradient structure (the
    /// JPEG XL MA "property"). Signaled in the model section (zero extra header
    /// bit); the per-image auto-selection (computed in the encoder safety net)
    /// keeps it on only when it actually wins, so a regression can never ship.
    /// Mirrored: both sides read it from the model.
    pub cmarc_ma_context: bool,
    /// R6-B color cache (Component A): per-plane LRU of reconstructed sample values.
    /// When set, the CMARC coding pass maintains the LRU and codes a literal whose
    /// value hits the cache as a `cache_flag` + small index instead of the full
    /// residual. Signaled in the model section; the never-expand safety net keeps
    /// it on only when it actually wins, so a regression can never ship. Mirrored:
    /// both sides read it from the model (zero extra header bit).
    pub cmarc_use_color_cache: bool,
    /// R9-B context-tree weighted predictor: per-plane (optional) table of
    /// `WC_LEAVES` weight tuples `(wL,wT,wTL,wTR,bias,shift)` solved per fine leaf in
    /// `analyze`. Tiny (O(1) bytes/plane, ~75), so it does not regress like the
    /// R7-A per-coarse-context codebook. Entry is `None` for planes that do not
    /// use `WeightedTree` (so no model bytes are wasted). The whole field is
    /// `None` when `WeightedTree` is not enabled/used on this image. Both encoder
    /// and decoder read it from the model, so lockstep is exact with zero online
    /// state.
    pub weighted_wc_table: Option<Vec<Option<Vec<WLeaf>>>>,
    /// R10-A JPEG XL-class Squeeze (recursive group transform) level per plane.
    /// `0` (the default) means the plane is coded as a single band (no Squeeze);
    /// a value `L >= 1` means the plane is split recursively `L` times into
    /// sub-bands before coding. Signal in the model section; both sides read it
    /// so no extra header bits are needed. Chosen per plane by the never-expand
    /// safety net, so enabling Squeeze can never regress the file.
    pub squeeze_levels: Vec<u8>,
    /// R10-B chroma-from-luma (CFL) scale per plane. `None` (the default, and the
    /// value for the luma plane) means no CFL; `Some(s)` with `s in 0..=7` means
    /// the chroma plane is pre-subtracted by `round(s * luma / 8)` before coding
    /// and added back on decode. Scale 0 is the identity, so CFL is a strict
    /// superset and provably cannot regress. Signal in the model section; both
    /// sides read it so lockstep is exact.
    pub cfl_scale: Vec<Option<u8>>,
    /// R10: per-band value range. A Squeeze sub-band (or CFL-pre-subtracted
    /// plane) can hold values outside the original plane's `[min, max]`, so each
    /// coded band is clamped/reconstructed against its OWN range. Indexed by
    /// band (stream) order, which matches `squeeze_band_layout` plane-major.
    /// Length is `total_bands`; empty only for legacy streams (decoder falls
    /// back to the per-plane range).
    pub band_ranges: Vec<PlaneRange>,
}

impl ModelConfig {
    /// Predictor for a plane/context pair.
    pub fn predictor(&self, plane: usize, context: usize) -> PredictorId {
        PredictorId::from_u8(self.planes[plane].map[context]).unwrap_or(PredictorId::Med)
    }

    pub fn weight_for(&self, plane: usize) -> Option<WeightVec> {
        let idx = self.planes[plane].weight_index;
        if idx == u8::MAX {
            None
        } else {
            self.weight_codebook.get(idx as usize).copied()
        }
    }

    /// The R9-B weighted-tree table for a plane, if `WeightedTree` is in use.
    pub fn weighted_tree_for(&self, plane: usize) -> Option<&[WLeaf]> {
        self.weighted_wc_table
            .as_ref()
            .and_then(|v| v.get(plane).and_then(|o| o.as_ref()).map(|x| x.as_slice()))
    }
}

/// The set of predictor candidates for an effort level.
pub fn predictors_for(effort: u8) -> Vec<PredictorId> {
    if effort == 0 {
        return vec![PredictorId::Med];
    }
    if effort <= 3 {
        return vec![
            PredictorId::Left,
            PredictorId::Top,
            PredictorId::Tl,
            PredictorId::Tr,
            PredictorId::Avg,
            PredictorId::Med,
            PredictorId::GapLite,
        ];
    }
    vec![
        PredictorId::Left,
        PredictorId::Top,
        PredictorId::Tl,
        PredictorId::Tr,
        PredictorId::Avg,
        PredictorId::Med,
        PredictorId::GapLite,
        PredictorId::Weighted,
        // R2.2 expanded WebP/JPEG XL-style bank (effort >= 4): true-motion,
        // half-delta, gradient, and the six clamped add/subtract forms. The
        // per-context analysis pass picks among all candidates by summed residual
        // cost, so the best predictor per context is encoded in the model map at
        // zero per-symbol cost (and, once selected, already partitions the CMARC
        // residual distribution per spatial context).
        PredictorId::TrueMotion,
        PredictorId::LPlusHalfTLMinusT,
        PredictorId::Gradient2,
        PredictorId::AddLT,
        PredictorId::AddLTL,
        PredictorId::AddTLT,
        PredictorId::SubLTL,
        PredictorId::SubTLT,
        PredictorId::SubTTR,
        // R8-A: signaling-free adaptive weighted predictor (JPEG XL / WebP "weighted").
        // Deterministic from the causal neighborhood, so it adds no model bytes and is
        // only ever selected where it lowers the summed residual magnitude.
        PredictorId::AdaptiveWeighted,
        // R9-B: context-tree weighted predictor (per-fine-leaf least-squares weights,
        // signaled as a tiny per-plane table). A strict superset of every fixed
        // candidate, so it is selected per context only where it lowers |residual|.
        PredictorId::WeightedTree,
    ]
}

/// Quick per-plane cost estimate (sum of zigzag-symbol magnitudes of MED
/// residuals). Used for transform and palette selection; monotone in coded
/// size, cheap to compute.
pub fn estimate_cost(plane: &[i16], range: PlaneRange, width: usize, height: usize) -> u64 {
    let mut total: u64 = 0;
    let n = width * height;
    if n == 0 {
        return 0;
    }
    for y in 0..height {
        for x in 0..width {
            let nb = neighbors(plane, x, y, width, height);
            let pred = predict_clamped(PredictorId::Med, &nb, None, None, range);
            let r = plane[y * width + x] as i32 - pred;
            total += zigzag(r) as u64;
        }
    }
    total
}

/// The analysis pass. Returns per-plane predictor maps and, when `collect
/// histograms` is set, per-context static histograms.
pub fn analyze(
    planes: &[Vec<i16>],
    ranges: &[PlaneRange],
    width: usize,
    height: usize,
    effort: u8,
    context: &ContextParams,
    weight_codebook: &[WeightVec],
    entropy_gr: bool,
) -> ModelConfig {
    let n_planes = planes.len();
    let context_count = context.context_count();
    let cm = ContextModel::new(*context);
    let mut model = ModelConfig {
        transform: TransformChoice::None,
        cross_channel: false,
        palette: None,
        context: *context,
        context_count,
        planes: Vec::new(),
        weight_codebook: weight_codebook.to_vec(),
        static_histograms: None,
        entropy_mode: ENTROPY_MODE_GR,
        capped_histograms: None,
        cmarc_priors: None,
        cmarc_residual_ctx: false,
        cmarc_run: false,
        cmarc_ma_context: false,
        cmarc_use_color_cache: false,
        weighted_wc_table: None,
        squeeze_levels: vec![0u8; n_planes],
        cfl_scale: vec![None; n_planes],
        band_ranges: Vec::new(),
    };

    let predictors = predictors_for(effort);
    let include_weighted = predictors.contains(&PredictorId::Weighted);
    let include_tree = predictors.contains(&PredictorId::WeightedTree);
    let mut wtables: Vec<Option<Vec<WLeaf>>> = Vec::new();

    for (pi, plane) in planes.iter().enumerate() {
        let range = ranges[pi];
        // Choose the per-plane weight vector (effort >= 4) by total cost.
        let mut weight_index = u8::MAX;
        if include_weighted {
            let mut best_cost: u64 = u64::MAX;
            let mut best: u8 = 0;
            for (wi, w) in weight_codebook.iter().enumerate() {
                let mut cost: u64 = 0;
                for y in 0..height {
                    for x in 0..width {
                        let nb = neighbors(plane, x, y, width, height);
                        let pred = predict_clamped(PredictorId::Weighted, &nb, Some(w), None, range);
                        let r = plane[y * width + x] as i32 - pred;
                        cost += zigzag(r) as u64;
                    }
                }
                if cost < best_cost {
                    best_cost = cost;
                    best = wi as u8;
                }
            }
            weight_index = best;
        }

        // R9-B: build the per-fine-leaf weighted-tree table for this plane (only when
        // the `WeightedTree` predictor is a candidate, i.e. effort >= 4). Accumulate
        // the 4x4 normal equations per leaf over (L,T,TL,TR) and the value v, solve
        // the least-squares weights, and keep the table only if some context actually
        // selects `WeightedTree` (so no model bytes are wasted when it does not help).
        let wt_table: Vec<WLeaf> = if include_tree {
            let mut s_leaf: Vec<[[i64; 5]; 5]> = vec![[[0i64; 5]; 5]; WC_LEAVES];
            let mut b_leaf: Vec<[i64; 5]> = vec![[0i64; 5]; WC_LEAVES];
            let mut cnt: Vec<i64> = vec![0i64; WC_LEAVES];
            for y in 0..height {
                for x in 0..width {
                    let idx = y * width + x;
                    let n = neighbors(plane, x, y, width, height);
                    let wc = weight_context(&n);
                    let ns = [n.l as i64, n.t as i64, n.tl as i64, n.tr as i64, 1i64];
                    for i in 0..5 {
                        for j in 0..5 {
                            s_leaf[wc][i][j] += ns[i] * ns[j];
                        }
                        b_leaf[wc][i] += (plane[idx] as i64) * ns[i];
                    }
                    cnt[wc] += 1;
                }
            }
            let mut table = Vec::with_capacity(WC_LEAVES);
            for lc in 0..WC_LEAVES {
                let leaf = if cnt[lc] >= WC_MIN_SAMPLES as i64 {
                    solve_weighted_tree(&s_leaf[lc], &b_leaf[lc]).unwrap_or(UNIT_LEAF)
                } else {
                    UNIT_LEAF
                };
                table.push(leaf);
            }
            table
        } else {
            Vec::new()
        };

        // Per-context predictor selection by cost.
        let mut ctx_costs: Vec<Vec<u64>> = vec![vec![0u64; predictors.len()]; context_count];
        for y in 0..height {
            for x in 0..width {
                let idx = y * width + x;
                let nb = neighbors(plane, x, y, width, height);
                let cid = cm.context_id(&nb, x, y);
                let wv = if include_weighted {
                    weight_codebook.get(weight_index as usize)
                } else {
                    None
                };
                let v = plane[idx] as i32;
                for (k, &p) in predictors.iter().enumerate() {
                    let wtree = if p == PredictorId::WeightedTree {
                        Some(wt_table.as_slice())
                    } else {
                        None
                    };
                    let pred = predict_clamped(p, &nb, wv, wtree, range);
                    ctx_costs[cid][k] += zigzag(v - pred) as u64;
                }
            }
        }
        let mut best_pred: Vec<u8> = vec![predictors[0].to_u8(); context_count];
        for cid in 0..context_count {
            let mut best_k = 0usize;
            let mut best_c = u64::MAX;
            for (k, &c) in ctx_costs[cid].iter().enumerate() {
                let p = predictors[k];
                // `WeightedTree` is a strict superset of every fixed predictor (it
                // can emulate any of them via its per-leaf table), so when its
                // summed residual ties or beats a fixed candidate it wins the
                // context - this is what lets it displace the simpler predictors
                // on structured content without costing extra per-symbol bits.
                if c < best_c || (c == best_c && p == PredictorId::WeightedTree) {
                    best_c = c;
                    best_k = k;
                }
            }
            best_pred[cid] = predictors[best_k].to_u8();
        }
        // Keep the table only if this plane actually uses `WeightedTree` somewhere.
        let used_tree = best_pred.iter().any(|&p| p == PredictorId::WeightedTree.to_u8());
        wtables.push(if used_tree { Some(wt_table) } else { None });
        model.planes.push(PlaneModel {
            map: best_pred,
            weight_index,
        });
    }
    model.weighted_wc_table = if wtables.iter().any(|o| o.is_some()) {
        Some(wtables)
    } else {
        None
    };

    // Static histograms at effort >= 6. Skipped under the Golomb-Rice backend
    // (M0/M1), where per-context k is implicit mirrored state and the histogram
    // pass would be wasted work and memory; `static_histograms` stays `None`.
    if effort >= 6 && !entropy_gr {
        let mut per_plane: Vec<Vec<Option<Vec<(u32, u32)>>>> = Vec::new();
        for (pi, plane) in planes.iter().enumerate() {
            let range = ranges[pi];
            let alphabet = Alphabet::for_range(range.min, range.max);
            let mut hist: Vec<Vec<u64>> = vec![vec![0u64; alphabet.size]; context_count];
            let wv = model.weight_for(pi);
            for y in 0..height {
                for x in 0..width {
                    let idx = y * width + x;
                    let nb = neighbors(plane, x, y, width, height);
                    let cid = cm.context_id(&nb, x, y);
                    let p = model.predictor(pi, cid);
                    let pred = predict_clamped(p, &nb, wv.as_ref(), model.weighted_tree_for(pi), range);
                    let r = plane[idx] as i32 - pred;
                    hist[cid][zigzag(r) as usize] += 1;
                }
            }
            let mut contexts: Vec<Option<Vec<(u32, u32)>>> = Vec::new();
            for h in hist {
                let mut sparse: Vec<(u32, u32)> = Vec::new();
                for (s, &c) in h.iter().enumerate() {
                    if c > 0 {
                        sparse.push((s as u32, c as u32));
                    }
                }
                if sparse.is_empty() {
                    contexts.push(None);
                } else {
                    contexts.push(Some(sparse));
                }
            }
            per_plane.push(contexts);
        }
        model.static_histograms = Some(per_plane);
    }

    model
}

/// A default model (effort 0): MED everywhere over a single global context per
/// plane (architecture section 9: "fixed MED for all contexts"), so all adaptive
/// symbols concentrate in one table and the model section stays tiny.
pub fn default_model(
    planes: &[Vec<i16>],
    context: &ContextParams,
    weight_codebook: &[WeightVec],
) -> ModelConfig {
    let n_planes = planes.len();
    let context_count = 1;
    let planes: Vec<PlaneModel> = planes
        .iter()
        .map(|_| PlaneModel {
            map: vec![PredictorId::Med.to_u8(); context_count],
            weight_index: u8::MAX,
        })
        .collect();
    ModelConfig {
        transform: TransformChoice::None,
        cross_channel: false,
        palette: None,
        context: *context,
        context_count,
        planes,
        weight_codebook: weight_codebook.to_vec(),
        static_histograms: None,
        entropy_mode: ENTROPY_MODE_GR,
        capped_histograms: None,
        cmarc_priors: None,
        cmarc_residual_ctx: false,
        cmarc_run: false,
        cmarc_ma_context: false,
        cmarc_use_color_cache: false,
        weighted_wc_table: None,
        squeeze_levels: vec![0u8; n_planes],
        cfl_scale: vec![None; n_planes],
        band_ranges: Vec::new(),
    }
}

/// Build per-context histograms over the capped residual alphabet (`CAPPED_SYMBOLS`)
/// for the M3.5 Design B capped-and-escaped rANS backend. Uses the same per-context
/// predictor selection and `zigzag` mapping as the coding pass, so the resulting
/// static tables exactly match what the encoder/decoder will see. Symbols are
/// `min(zigzag(r), CAPPED_ALPHABET)`; residuals larger than the cap take the escape
/// symbol and are coded by the fallback Golomb-Rice stream, so they are not counted
/// here.
pub fn build_capped_histograms(
    planes: &[Vec<i16>],
    ranges: &[PlaneRange],
    width: usize,
    height: usize,
    model: &ModelConfig,
) -> Vec<Vec<Option<Vec<(u32, u32)>>>> {
    let cm = ContextModel::new(model.context);
    let mut per_plane: Vec<Vec<Option<Vec<(u32, u32)>>>> = Vec::with_capacity(planes.len());
    for (pi, plane) in planes.iter().enumerate() {
        let range = ranges[pi];
        let mut hist: Vec<Vec<u64>> = vec![vec![0u64; CAPPED_SYMBOLS]; model.context_count];
            let wv = model.weight_for(pi);
            let area = width * height;
            for i in 0..area {
                let x = i % width;
                let y = i / width;
                let nb = neighbors(plane, x, y, width, height);
                let cid = cm.context_id(&nb, x, y) % model.context_count;
                let p = model.predictor(pi, cid);
                let pred = predict_clamped(p, &nb, wv.as_ref(), model.weighted_tree_for(pi), range);
            let r = plane[i] as i32 - pred;
            let z = zigzag(r) as usize;
            let sym = z.min(CAPPED_ALPHABET);
            hist[cid][sym] += 1;
        }
        let mut contexts: Vec<Option<Vec<(u32, u32)>>> = Vec::with_capacity(model.context_count);
        for h in hist {
            let mut sparse: Vec<(u32, u32)> = Vec::new();
            for (s, &c) in h.iter().enumerate() {
                if c > 0 {
                    sparse.push((s as u32, c as u32));
                }
            }
            if sparse.is_empty() {
                contexts.push(None);
            } else {
                contexts.push(Some(sparse));
            }
        }
        per_plane.push(contexts);
    }
    per_plane
}

/// Serialize the model to `w`.
pub fn write_model(w: &mut impl Write, m: &ModelConfig) -> Result<(), CodecError> {
    w.write_all(&[match m.transform {
        TransformChoice::None => 0,
        TransformChoice::YCoCgR => 1,
    }])?;
    w.write_all(&[m.context.base_shift, m.context.activity_classes])?;
    w.write_all(&m.context.activity_scale.to_le_bytes())?;
    w.write_all(&(m.context_count as u16).to_le_bytes())?;
    for plane in &m.planes {
        w.write_all(&plane.map)?;
        w.write_all(&[plane.weight_index])?;
    }
    match &m.palette {
        None => w.write_all(&[0])?,
        Some(pal) => {
            w.write_all(&[1])?;
            w.write_all(&(pal.colors.len() as u32).to_le_bytes())?;
            for c in &pal.colors {
                w.write_all(c)?;
            }
        }
    }
    match &m.static_histograms {
        None => w.write_all(&[0])?,
        Some(per_plane) => {
            w.write_all(&[1])?;
            for plane_ctx in per_plane {
                // u16 number of non-empty contexts, then each as
                // (u16 ctx, u16 symbol_count, symbol/freq pairs).
                let non_empty: Vec<usize> = plane_ctx
                    .iter()
                    .enumerate()
                    .filter(|(_, o)| o.is_some())
                    .map(|(i, _)| i)
                    .collect();
                w.write_all(&(non_empty.len() as u16).to_le_bytes())?;
                for cid in non_empty {
                    w.write_all(&(cid as u16).to_le_bytes())?;
                    let pairs = plane_ctx[cid].as_ref().unwrap();
                    w.write_all(&(pairs.len() as u16).to_le_bytes())?;
                    for &(sym, f) in pairs {
                        w.write_all(&(sym as u16).to_le_bytes())?;
                        w.write_all(&(f as u16).to_le_bytes())?;
                    }
                }
            }
        }
    }
    match &m.capped_histograms {
        None => w.write_all(&[0])?,
        Some(per_plane) => {
            w.write_all(&[1])?;
            for plane_ctx in per_plane {
                let non_empty: Vec<usize> = plane_ctx
                    .iter()
                    .enumerate()
                    .filter(|(_, o)| o.is_some())
                    .map(|(i, _)| i)
                    .collect();
                w.write_all(&(non_empty.len() as u16).to_le_bytes())?;
                for cid in non_empty {
                    w.write_all(&(cid as u16).to_le_bytes())?;
                    let pairs = plane_ctx[cid].as_ref().unwrap();
                    w.write_all(&(pairs.len() as u16).to_le_bytes())?;
                    for &(sym, f) in pairs {
                        w.write_all(&(sym as u16).to_le_bytes())?;
                        w.write_all(&(f as u16).to_le_bytes())?;
                    }
                }
            }
        }
    }
    // Entropy backend selector (M3.5 Design B). Appended last so older readers
    // that stop earlier still parse the model body; all writers in this build
    // emit it, so the decoder always reads it back.
    w.write_all(&[m.entropy_mode])?;
    // R1 CMARC per-`(cid, bin)` static priors. Appended after `entropy_mode` so
    // legacy readers (and readers that stop at the backend selector) still parse
    // the model body; the decoder seeds `BinModel`s from these counts. `None`
    // when CMARC priors are off.
    match &m.cmarc_priors {
        None => w.write_all(&[0])?,
        Some(per_plane) => {
            w.write_all(&[1])?;
            for plane_ctx in per_plane {
                let non_empty: Vec<usize> = plane_ctx
                    .iter()
                    .enumerate()
                    .filter(|(_, o)| o.is_some())
                    .map(|(i, _)| i)
                    .collect();
                w.write_all(&(non_empty.len() as u16).to_le_bytes())?;
                for cid in non_empty {
                    w.write_all(&(cid as u16).to_le_bytes())?;
                    let pairs = plane_ctx[cid].as_ref().unwrap();
                    w.write_all(&(pairs.len() as u16).to_le_bytes())?;
                    for &(bin, n1, n0) in pairs {
                        w.write_all(&(bin as u16).to_le_bytes())?;
                        w.write_all(&(n1 as u16).to_le_bytes())?;
                        w.write_all(&(n0 as u16).to_le_bytes())?;
                    }
                }
            }
        }
    }
    // R2.1 cross-channel subtract-green flag. Appended last so legacy readers
    // that stop earlier still parse the model body; the decoder applies the
    // inverse after the inverse color transform when this flag is set.
    w.write_all(&[if m.cross_channel { 1 } else { 0 }])?;
    // R3-A JPEG-LS DIFF residual-context flag for CMARC. Appended after the
    // cross-channel flag so legacy readers that stop earlier still parse the
    // model body; the decoder selects the CMARC coding context accordingly.
    w.write_all(&[if m.cmarc_residual_ctx { 1 } else { 0 }])?;
    // R3-C run-mode flag for CMARC. Appended after the residual-context flag;
    // decoder mirrors it to decide whether to read run lengths.
    w.write_all(&[if m.cmarc_run { 1 } else { 0 }])?;
    // R11-D MA-tree-lite flag for CMARC. Appended after the run-mode flag; the
    // decoder mirrors it to decide whether to fold the local gradient into the
    // residual coding context.
    w.write_all(&[if m.cmarc_ma_context { 1 } else { 0 }])?;
    // R6-B color-cache flag for CMARC. Appended after the run-mode flag; the
    // decoder mirrors it to decide whether to maintain the per-plane LRU.
    w.write_all(&[if m.cmarc_use_color_cache { 1 } else { 0 }])?;
    // R9-B weighted-tree table. Appended last so legacy readers still parse the
    // model body. Format: [flag]; if 1, then per plane [flag]; if a plane's flag
    // is 1, [WC_LEAVES as u16] followed by that many (i16,i16,i16,i16,i16,u8) leaves
    // (spatial weights, bias, shift - all little-endian / shift as one byte). The
    // decoder threads the table into the `WeightedTree` prediction so encoder/
    // decoder lockstep is exact.
    match &m.weighted_wc_table {
        None => w.write_all(&[0])?,
        Some(per_plane) => {
            w.write_all(&[1])?;
            for plane in per_plane {
                if let Some(table) = plane {
                    w.write_all(&[1])?;
                    w.write_all(&(table.len() as u16).to_le_bytes())?;
                    for &(w0, w1, w2, w3, bias, s) in table {
                        w.write_all(&w0.to_le_bytes())?;
                        w.write_all(&w1.to_le_bytes())?;
                        w.write_all(&w2.to_le_bytes())?;
                        w.write_all(&w3.to_le_bytes())?;
                        w.write_all(&bias.to_le_bytes())?;
                        w.write_all(&[s])?;
                    }
                } else {
                    w.write_all(&[0])?;
                }
            }
        }
    }
    // R10-A Squeeze levels and R10-B CFL scales, appended last (after the
    // weighted-tree table) so every legacy reader that stops earlier still parses
    // the model body. Lengths are implied by `alphabet_sizes.len()` (= plane
    // count), so no length prefix is needed; both the encoder (writer) and the
    // decoder (reader) always process these trailing bytes in the same build.
    for &lvl in &m.squeeze_levels {
        w.write_all(&[lvl])?;
    }
    for &scale in &m.cfl_scale {
        // `0xFF` encodes `None`; otherwise the 3-bit scale `s in 0..=7`.
        let byte = match scale {
            Some(s) => s,
            None => 0xFF,
        };
        w.write_all(&[byte])?;
    }
    // R10 per-band value ranges, appended after the CFL scales (still last) so
    // every legacy reader that stops earlier still parses the model body. Length
    // is NOT implied by plane count (it equals `total_bands`), so a u32 count
    // prefixes the `(min as i16, max as i16)` pairs in band/stream order.
    w.write_all(&(m.band_ranges.len() as u32).to_le_bytes())?;
    for r in &m.band_ranges {
        w.write_all(&r.min.to_le_bytes())?;
        w.write_all(&r.max.to_le_bytes())?;
    }
    Ok(())
}

/// Read a model from `r`. `alphabet_sizes` gives the rANS table size per plane.
pub fn read_model(r: &mut impl Read, alphabet_sizes: &[usize]) -> Result<ModelConfig, CodecError> {
    let mut buf = [0u8; 1];
    r.read_exact(&mut buf)?;
    let transform = match buf[0] {
        0 => TransformChoice::None,
        1 => TransformChoice::YCoCgR,
        v => return Err(CodecError::InvalidStream(format!("bad transform {v}"))),
    };
    let mut params = [0u8; 2];
    r.read_exact(&mut params)?;
    let base_shift = params[0];
    let activity_classes = params[1];
    if activity_classes == 0 || base_shift > 8 {
        return Err(CodecError::InvalidStream("bad context params".into()));
    }
    let mut scale = [0u8; 4];
    r.read_exact(&mut scale)?;
    let activity_scale = u32::from_le_bytes(scale);
    let context = ContextParams {
        base_shift,
        activity_classes,
        activity_scale,
    };
    let mut cc = [0u8; 2];
    r.read_exact(&mut cc)?;
    let context_count = u16::from_le_bytes(cc) as usize;
    if context_count > 4096 {
        return Err(CodecError::InvalidStream("context count too large".into()));
    }
    let plane_count = alphabet_sizes.len();
    let mut planes = Vec::with_capacity(plane_count);
    for _ in 0..plane_count {
        let mut map = vec![0u8; context_count];
        r.read_exact(&mut map)?;
        let mut wi = [0u8; 1];
        r.read_exact(&mut wi)?;
        for &p in &map {
            if PredictorId::from_u8(p).is_none() {
                return Err(CodecError::InvalidStream(format!("bad predictor id {p}")));
            }
        }
        planes.push(PlaneModel {
            map,
            weight_index: wi[0],
        });
    }
    let mut pal = [0u8; 1];
    r.read_exact(&mut pal)?;
    let palette = if pal[0] == 1 {
        let mut n = [0u8; 4];
        r.read_exact(&mut n)?;
        let count = u32::from_le_bytes(n) as usize;
        if count == 0 || count > 256 {
            return Err(CodecError::InvalidStream("bad palette size".into()));
        }
        let mut colors = Vec::with_capacity(count);
        let mut triple = [0u8; 3];
        for _ in 0..count {
            r.read_exact(&mut triple)?;
            colors.push(triple);
        }
        Some(Palette {
            colors,
            indices: Vec::new(),
        })
    } else if pal[0] == 0 {
        None
    } else {
        return Err(CodecError::InvalidStream("bad palette flag".into()));
    };

    let mut st = [0u8; 1];
    r.read_exact(&mut st)?;
    let static_histograms = if st[0] == 1 {
        let mut per_plane: Vec<Vec<Option<Vec<(u32, u32)>>>> = Vec::new();
        for _ in 0..plane_count {
            let mut nc = [0u8; 2];
            r.read_exact(&mut nc)?;
            let non_empty = u16::from_le_bytes(nc) as usize;
            if non_empty > context_count {
                return Err(CodecError::InvalidStream("too many static contexts".into()));
            }
            let mut contexts: Vec<Option<Vec<(u32, u32)>>> = vec![None; context_count];
            for _ in 0..non_empty {
                let mut cid = [0u8; 2];
                r.read_exact(&mut cid)?;
                let cid = u16::from_le_bytes(cid) as usize;
                if cid >= context_count {
                    return Err(CodecError::InvalidStream("bad context id".into()));
                }
                let mut sc = [0u8; 2];
                r.read_exact(&mut sc)?;
                let symbol_count = u16::from_le_bytes(sc) as usize;
                if symbol_count == 0 || symbol_count > 2048 {
                    return Err(CodecError::InvalidStream("bad symbol count".into()));
                }
                let mut pairs = Vec::with_capacity(symbol_count);
                for _ in 0..symbol_count {
                    let mut p = [0u8; 4];
                    r.read_exact(&mut p)?;
                    let sym = u16::from_le_bytes([p[0], p[1]]) as u32;
                    let f = u16::from_le_bytes([p[2], p[3]]) as u32;
                    pairs.push((sym, f));
                }
                contexts[cid] = Some(pairs);
            }
            per_plane.push(contexts);
        }
        Some(per_plane)
    } else if st[0] == 0 {
        None
    } else {
        return Err(CodecError::InvalidStream("bad static-tables flag".into()));
    };

    let mut ch = [0u8; 1];
    r.read_exact(&mut ch)?;
    let capped_histograms = if ch[0] == 1 {
        let mut per_plane: Vec<Vec<Option<Vec<(u32, u32)>>>> = Vec::new();
        for _ in 0..plane_count {
            let mut nc = [0u8; 2];
            r.read_exact(&mut nc)?;
            let non_empty = u16::from_le_bytes(nc) as usize;
            if non_empty > context_count {
                return Err(CodecError::InvalidStream("too many capped contexts".into()));
            }
            let mut contexts: Vec<Option<Vec<(u32, u32)>>> = vec![None; context_count];
            for _ in 0..non_empty {
                let mut cid = [0u8; 2];
                r.read_exact(&mut cid)?;
                let cid = u16::from_le_bytes(cid) as usize;
                if cid >= context_count {
                    return Err(CodecError::InvalidStream("bad context id".into()));
                }
                let mut sc = [0u8; 2];
                r.read_exact(&mut sc)?;
                let symbol_count = u16::from_le_bytes(sc) as usize;
                if symbol_count == 0 || symbol_count > 2048 {
                    return Err(CodecError::InvalidStream("bad symbol count".into()));
                }
                let mut pairs = Vec::with_capacity(symbol_count);
                for _ in 0..symbol_count {
                    let mut p = [0u8; 4];
                    r.read_exact(&mut p)?;
                    let sym = u16::from_le_bytes([p[0], p[1]]) as u32;
                    let f = u16::from_le_bytes([p[2], p[3]]) as u32;
                    pairs.push((sym, f));
                }
                contexts[cid] = Some(pairs);
            }
            per_plane.push(contexts);
        }
        Some(per_plane)
    } else if ch[0] == 0 {
        None
    } else {
        return Err(CodecError::InvalidStream("bad capped-tables flag".into()));
    };

    let mut em = [0u8; 1];
    r.read_exact(&mut em)?;
    let entropy_mode = em[0];

    // R1 CMARC per-`(cid, bin)` static priors, appended after `entropy_mode`.
    let mut cp = [0u8; 1];
    r.read_exact(&mut cp)?;
    let cmarc_priors = if cp[0] == 1 {
        let mut per_plane: Vec<Vec<Option<Vec<(u32, u32, u32)>>>> = Vec::new();
        for _ in 0..plane_count {
            let mut nc = [0u8; 2];
            r.read_exact(&mut nc)?;
            let non_empty = u16::from_le_bytes(nc) as usize;
            if non_empty > context_count {
                return Err(CodecError::InvalidStream("too many cmarc contexts".into()));
            }
            let mut contexts: Vec<Option<Vec<(u32, u32, u32)>>> = vec![None; context_count];
            for _ in 0..non_empty {
                let mut cid = [0u8; 2];
                r.read_exact(&mut cid)?;
                let cid = u16::from_le_bytes(cid) as usize;
                if cid >= context_count {
                    return Err(CodecError::InvalidStream("bad cmarc context id".into()));
                }
                let mut sc = [0u8; 2];
                r.read_exact(&mut sc)?;
                let pair_count = u16::from_le_bytes(sc) as usize;
                if pair_count == 0 || pair_count > 8192 {
                    return Err(CodecError::InvalidStream("bad cmarc pair count".into()));
                }
                let mut pairs = Vec::with_capacity(pair_count);
                for _ in 0..pair_count {
                    let mut p = [0u8; 6];
                    r.read_exact(&mut p)?;
                    let bin = u16::from_le_bytes([p[0], p[1]]) as u32;
                    let n1 = u16::from_le_bytes([p[2], p[3]]) as u32;
                    let n0 = u16::from_le_bytes([p[4], p[5]]) as u32;
                    pairs.push((bin, n1, n0));
                }
                contexts[cid] = Some(pairs);
            }
            per_plane.push(contexts);
        }
        Some(per_plane)
    } else if cp[0] == 0 {
        None
    } else {
        return Err(CodecError::InvalidStream("bad cmarc-priors flag".into()));
    };

    // R2.1 cross-channel subtract-green flag, appended last so legacy readers
    // (and readers that stop earlier) still parse the model body.
    let mut xc = [0u8; 1];
    r.read_exact(&mut xc)?;
    let cross_channel = xc[0] != 0;

    // R3-A JPEG-LS DIFF residual-context flag for CMARC, appended after the
    // cross-channel flag so legacy readers still parse the model body.
    let mut rc = [0u8; 1];
    r.read_exact(&mut rc)?;
    let cmarc_residual_ctx = rc[0] != 0;
    let mut rc2 = [0u8; 1];
    r.read_exact(&mut rc2)?;
    let cmarc_run = rc2[0] != 0;

    // R11-D MA-tree-lite flag for CMARC, appended after the run-mode flag so
    // legacy readers still parse the model body.
    let mut rc3 = [0u8; 1];
    r.read_exact(&mut rc3)?;
    let cmarc_ma_context = rc3[0] != 0;

    // R6-B color-cache flag for CMARC, appended after the run-mode flag.
    let mut ccf = [0u8; 1];
    r.read_exact(&mut ccf)?;
    let cmarc_use_color_cache = ccf[0] != 0;

    // R9-B weighted-tree table, appended after the color-cache flag. Format mirrors
    // `write_model`: a flag byte, then per plane a flag byte and (if set) the leaf
    // count followed by the weight tuples.
    let mut wt_flag = [0u8; 1];
    r.read_exact(&mut wt_flag)?;
    let weighted_wc_table = if wt_flag[0] == 1 {
        let mut per_plane: Vec<Option<Vec<WLeaf>>> = Vec::with_capacity(plane_count);
        for _ in 0..plane_count {
            let mut pf = [0u8; 1];
            r.read_exact(&mut pf)?;
            if pf[0] == 1 {
                let mut lc = [0u8; 2];
                r.read_exact(&mut lc)?;
                let n = u16::from_le_bytes(lc) as usize;
                let mut table = Vec::with_capacity(n);
                for _ in 0..n {
                    let mut w0 = [0u8; 2];
                    r.read_exact(&mut w0)?;
                    let mut w1 = [0u8; 2];
                    r.read_exact(&mut w1)?;
                    let mut w2 = [0u8; 2];
                    r.read_exact(&mut w2)?;
                    let mut w3 = [0u8; 2];
                    r.read_exact(&mut w3)?;
                    let mut bias = [0u8; 2];
                    r.read_exact(&mut bias)?;
                    let mut s = [0u8; 1];
                    r.read_exact(&mut s)?;
                    table.push((
                        i16::from_le_bytes(w0),
                        i16::from_le_bytes(w1),
                        i16::from_le_bytes(w2),
                        i16::from_le_bytes(w3),
                        i16::from_le_bytes(bias),
                        s[0],
                    ));
                }
                per_plane.push(Some(table));
            } else if pf[0] == 0 {
                per_plane.push(None);
            } else {
                return Err(CodecError::InvalidStream("bad weighted-tree plane flag".into()));
            }
        }
        Some(per_plane)
    } else if wt_flag[0] == 0 {
        None
    } else {
        return Err(CodecError::InvalidStream("bad weighted-tree flag".into()));
    };

    // R10-A Squeeze levels and R10-B CFL scales, appended last in `write_model`.
    // `plane_count` (= `alphabet_sizes.len()`) gives the exact number of trailing
    // bytes, so no length prefix is needed.
    let mut squeeze_levels: Vec<u8> = Vec::with_capacity(plane_count);
    for _ in 0..plane_count {
        let mut b = [0u8; 1];
        r.read_exact(&mut b)?;
        squeeze_levels.push(b[0]);
    }
    let mut cfl_scale: Vec<Option<u8>> = Vec::with_capacity(plane_count);
    for _ in 0..plane_count {
        let mut b = [0u8; 1];
        r.read_exact(&mut b)?;
        cfl_scale.push(if b[0] == 0xFF { None } else { Some(b[0]) });
    }

    // R10 per-band value ranges (see `write_model`): a u32 count followed by
    // `(min as i16, max as i16)` pairs in band/stream order. An empty vector is
    // only produced by legacy writers; this build always emits it.
    let mut br_len = [0u8; 4];
    r.read_exact(&mut br_len)?;
    let br_len = u32::from_le_bytes(br_len) as usize;
    let mut band_ranges: Vec<PlaneRange> = Vec::with_capacity(br_len);
    for _ in 0..br_len {
        let mut mn = [0u8; 4];
        r.read_exact(&mut mn)?;
        let mut mx = [0u8; 4];
        r.read_exact(&mut mx)?;
        band_ranges.push(PlaneRange {
            min: i32::from_le_bytes(mn),
            max: i32::from_le_bytes(mx),
        });
    }

    Ok(ModelConfig {
        transform,
        cross_channel,
        palette,
        context,
        context_count,
        planes,
        weight_codebook: default_weight_codebook(),
        static_histograms,
        entropy_mode,
        capped_histograms,
        cmarc_priors,
        cmarc_residual_ctx,
        cmarc_run,
        cmarc_ma_context,
        cmarc_use_color_cache,
        weighted_wc_table,
        squeeze_levels,
        cfl_scale,
        band_ranges,
    })
}

/// Build a per-plane, per-context rANS table set from static histograms.
pub fn build_static_tables(
    per_plane: &[Vec<Option<Vec<(u32, u32)>>>],
    alphabet_sizes: &[usize],
) -> Vec<Vec<Option<RansTable>>> {
    per_plane
        .iter()
        .enumerate()
        .map(|(pi, contexts)| {
            let a = alphabet_sizes[pi];
            contexts
                .iter()
                .map(|opt| {
                    opt.as_ref().map(|pairs| {
                        let mut hist = vec![0u32; a];
                        for &(s, f) in pairs {
                            if (s as usize) < a {
                                hist[s as usize] = f;
                            }
                        }
                        RansTable::new_static(&hist)
                    })
                })
                .collect()
        })
        .collect()
}

/// Default context params for a plane count.
pub fn default_context_params() -> ContextParams {
    ContextParams::default()
}

/// The per-plane value ranges for a channel layout and transform choice.
///
/// `cross_channel` is true when subtract-green was applied to the first three
/// planes (`R'=R-G, G'=G, B'=B-G`) before any color transform. With it the
/// plane ranges widen: a bare subtract-green keeps green in `[0,255]` but
/// pushes the two chroma deltas to `[-255,255]`; a subtract-green followed by
/// YCoCg-R stays within `[-1023,1023]` (conservative, exact-bounding). Both
/// encoder and decoder compute these identically from `(channels, transform,
/// cross_channel)`, so the declared ranges are always an upper bound on the
/// real plane values and the predictor clamping stays correct.
pub fn plane_ranges(
    channels: Channels,
    transform: TransformChoice,
    palette_max: Option<u32>,
    cross_channel: bool,
) -> Vec<PlaneRange> {
    if let Some(mx) = palette_max {
        return vec![PlaneRange::index(mx)];
    }
    if cross_channel {
        // Subtract-green widens the chroma-delto planes; we return conservatively
        // bounding ranges so clamping/residual sizing is always correct.
        let mut ranges = vec![
            PlaneRange { min: -1023, max: 1023 },
            PlaneRange { min: -1023, max: 1023 },
            PlaneRange { min: -1023, max: 1023 },
        ];
        if transform == TransformChoice::None {
            // Subtract-green only: green is preserved in [0,255].
            ranges[1] = PlaneRange::U8;
        }
        if channels == Channels::Rgba {
            ranges.push(PlaneRange::U8);
        }
        return ranges;
    }
    match channels {
        Channels::Gray => vec![PlaneRange::U8],
        Channels::Rgb => match transform {
            TransformChoice::None => vec![PlaneRange::U8; 3],
            TransformChoice::YCoCgR => vec![PlaneRange::Y, PlaneRange::CO, PlaneRange::CG],
        },
        Channels::Rgba => match transform {
            TransformChoice::None => vec![PlaneRange::U8; 4],
            TransformChoice::YCoCgR => vec![
                PlaneRange::Y,
                PlaneRange::CO,
                PlaneRange::CG,
                PlaneRange::U8,
            ],
        },
    }
}

/// The rANS alphabet size per plane for a set of plane ranges.
pub fn alphabet_sizes(ranges: &[PlaneRange]) -> Vec<usize> {
    ranges
        .iter()
        .map(|r| Alphabet::for_range(r.min, r.max).size)
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn model_roundtrip() {
        let context = ContextParams::default();
        let codebook = default_weight_codebook();
        let ranges = [PlaneRange::U8; 3];
        let width = 16;
        let height = 8;
        let planes: Vec<Vec<i16>> = (0..3)
            .map(|c| {
                (0..width * height)
                    .map(|i| ((i * (c + 3)) % 256) as i16)
                    .collect()
            })
            .collect();
        let model = analyze(&planes, &ranges, width, height, 5, &context, &codebook, false);
        let mut bytes = Vec::new();
        write_model(&mut bytes, &model).unwrap();
        let sizes = alphabet_sizes(&ranges);
        let back = read_model(&mut std::io::Cursor::new(bytes), &sizes).unwrap();
        assert_eq!(back.transform, model.transform);
        assert_eq!(back.planes, model.planes);
        assert_eq!(back.context_count, model.context_count);
    }

    #[test]
    fn r22_expanded_bank_selected_on_smooth() {
        // A smooth horizontal ramp gives the analysis pass a low-entropy residual
        // where the R2.2 expanded bank (true-motion / gradient / half-delta)
        // can beat the base 8 predictors. At effort >= 4 the chosen predictor
        // map must contain at least one R2.2 id (>= 8).
        let context = ContextParams::default();
        let codebook = default_weight_codebook();
        let range = PlaneRange::U8;
        let width = 64;
        let height = 64;
        let plane: Vec<i16> = (0..width * height)
            .map(|i| {
                let x = (i % width) as i16;
                let y = (i / width) as i16;
                (x + y) % 256
            })
            .collect();
        let model = analyze(
            &[plane],
            &[range],
            width,
            height,
            4,
            &context,
            &codebook,
            false,
        );
        let mut saw_expanded = false;
        for &p in &model.planes[0].map {
            if p >= 8 {
                saw_expanded = true;
            }
        }
        assert!(
            saw_expanded,
            "R2.2 expanded predictor bank should be selected somewhere on smooth content"
        );
    }

    #[test]
    fn static_model_roundtrip() {
        let context = ContextParams::default();
        let codebook = default_weight_codebook();
        let ranges = [PlaneRange::U8];
        let width = 32;
        let height = 32;
        let plane: Vec<i16> = (0..width * height)
            .map(|i| ((i * 7) % 256) as i16)
            .collect();
        let model = analyze(&[plane], &ranges, width, height, 7, &context, &codebook, false);
        assert!(model.static_histograms.is_some());
        let mut bytes = Vec::new();
        write_model(&mut bytes, &model).unwrap();
        let sizes = alphabet_sizes(&ranges);
        let back = read_model(&mut std::io::Cursor::new(bytes), &sizes).unwrap();
        assert!(back.static_histograms.is_some());
        let tables = build_static_tables(
            back.static_histograms.as_ref().unwrap(),
            &sizes,
        );
        assert_eq!(tables.len(), 1);
    }

    #[test]
    fn r9b_weighted_tree_selected_and_table_roundtrips() {
        // R9-B: on smooth structured content the per-fine-leaf least-squares
        // weighted predictor (`WeightedTree`) should be selected somewhere by the
        // analysis pass, and its table (when used) must serialize and deserialize
        // bit-exactly so the encoder and decoder agree on the weights.
        let context = ContextParams::default();
        let codebook = default_weight_codebook();
        let range = PlaneRange::U8;
        let width = 64;
        let height = 64;
        let plane: Vec<i16> = (0..width * height)
            .map(|i| {
                let x = (i % width) as i16;
                let y = (i / width) as i16;
                // Linear (non-wrapping) content: the per-leaf least-squares fit can
                // reproduce `v = x + y` exactly, beating the fixed predictors.
                (x + y) % 256
            })
            .collect();
        let model = analyze(&[plane], &[range], width, height, 4, &context, &codebook, false);
        let used = model
            .planes
            .iter()
            .flat_map(|p| p.map.iter())
            .any(|&p| p == PredictorId::WeightedTree.to_u8());
        assert!(used, "WeightedTree should be selected somewhere on smooth content");

        let table = model
            .weighted_tree_for(0)
            .expect("weighted-tree table present when WeightedTree is used");
        assert_eq!(table.len(), WC_LEAVES);
        for &(w0, w1, w2, w3, bias, s) in table {
            assert!(
                (-32768..=32767).contains(&w0)
                    && (-32768..=32767).contains(&w1)
                    && (-32768..=32767).contains(&w2)
                    && (-32768..=32767).contains(&w3)
                    && (-32768..=32767).contains(&bias)
            );
            assert!(s <= 12);
        }

        // Serialization round-trip of the full model (including the table).
        let mut bytes = Vec::new();
        write_model(&mut bytes, &model).unwrap();
        let sizes = alphabet_sizes(&[range]);
        let back = read_model(&mut std::io::Cursor::new(bytes), &sizes).unwrap();
        assert_eq!(back.weighted_tree_for(0), model.weighted_tree_for(0));
    }

    #[test]
    fn r9b_weighted_tree_full_roundtrip_bit_exact() {
        // End-to-end: encode then decode a synthetic gradient+edge RGB image at
        // effort 4 (where WeightedTree is a candidate) and confirm the output is
        // bit-exact. This exercises the locked encoder/decoder weighted-tree path.
        use crate::image::{Channels, Image};
        use crate::{decode, encode};
        let w = 48u32;
        let h = 40u32;
        let mut planes = vec![vec![0u8; (w * h) as usize]; 3];
        for y in 0..h as usize {
            for x in 0..w as usize {
                let idx = y * w as usize + x;
                planes[0][idx] = ((x + 2 * y) % 256) as u8;
                planes[1][idx] = ((x.wrapping_mul(3) ^ y) % 256) as u8;
                planes[2][idx] = (((x as i32 - 24).unsigned_abs() as u32 + y as u32) % 256) as u8;
            }
        }
        let img = Image {
            width: w,
            height: h,
            channels: Channels::Rgb,
            planes,
        };
        let (bytes, _stats) = encode(&img, 4).unwrap();
        let out = decode(&bytes).unwrap();
        assert_eq!(out.planes, img.planes, "R9-B WeightedTree roundtrip must be bit-exact");
    }
}
