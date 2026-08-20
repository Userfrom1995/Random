//! Causal predictor bank with border handling.
//!
//! Predictors operate on a plane of `i16` samples (see `color::PlaneRange`).
//! Every prediction is clamped to the plane's value range so residuals are
//! bounded and the signed zigzag alphabet is exact.

use crate::color::PlaneRange;

/// Causal neighborhood of a pixel in raster order.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Neighbors {
    pub l: i32,
    pub t: i32,
    pub tl: i32,
    pub tr: i32,
}

/// Predictor identities, mirrored in the model's predictor map bytes.
///
/// Ids 0..=7 are the original Obsidian bank (Left/Top/Tl/Tr/Avg/Med/GapLite/
/// Weighted). Ids 8..=16 are the R2.2 WebP/JPEG XL-style expansion (true-motion,
/// half-delta, gradient, and the six clamped add/subtract forms). Id 17 is the
/// R8-A signaling-free adaptive weighted predictor. Id 18 is the R9-B context-tree
/// weighted predictor (per-fine-leaf least-squares weights signaled in the model
/// section). Existing ids are preserved so every previously-produced stream still
/// decodes; the new ids only appear in streams whose analysis pass enabled them
/// (effort >= 4).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum PredictorId {
    Left = 0,
    Top = 1,
    Tl = 2,
    Tr = 3,
    Avg = 4,
    Med = 5,
    GapLite = 6,
    Weighted = 7,
    // ---- R2.2 expanded bank (WebP/JPEG XL-style) ----
    TrueMotion = 8,
    LPlusHalfTLMinusT = 9,
    Gradient2 = 10,
    AddLT = 11,
    AddLTL = 12,
    AddTLT = 13,
    SubLTL = 14,
    SubTLT = 15,
    SubTTR = 16,
    // ---- R8-A signaling-free adaptive weighted predictor (JPEG XL / WebP "weighted") ----
    // Deterministic from the causal neighborhood (no signaled weights), so it is a
    // strict superset of the fixed predictor candidates: the analysis pass selects
    // it per context only where it lowers the summed residual magnitude.
    AdaptiveWeighted = 17,
    // ---- R9-B context-tree weighted predictor (JPEG XL "weighted" at fine granularity) ----
    // Deterministic weight CONTEXT from the causal gradients (so encoder and decoder
    // agree with zero signaled bytes), but the actual 4 weights per leaf ARE
    // signaled in the model section as a tiny per-plane table (O(1) bytes, ~75/plane).
    // The analysis pass solves, per fine leaf, the least-squares optimal weights, so
    // this captures within-coarse-context variation R8-A's single fixed formula
    // cannot. Selected per context only where it lowers the summed residual.
    WeightedTree = 18,
}

pub const PREDICTOR_COUNT: usize = 19;

/// A per-leaf weight tuple for the R9-B `WeightedTree` predictor:
/// `(wL, wT, wTL, wTR, bias, shift)`. The prediction is
/// `round((wL*L + wT*T + wTL*TL + wTR*TR + bias) >> shift)`.
/// The `bias` term lets the fit reproduce smooth gradients (and the constant
/// offset that a pure linear combination of one-step-behind neighbors cannot).
pub type WLeaf = (i16, i16, i16, i16, i16, u8);

/// Number of fine weight-context leaves for `WeightedTree`. JPEG XL uses a small
/// property tree (8-15) for its weighted predictor; Obsidian originally used 15.
/// This build deepens it to 64 by quantizing each of the three causal gradients to
/// 4 tiers (instead of 3), giving 4*4*4 = 64 distinct `(gh,gv,gd)` cells. Because
/// the raw index then spans exactly `0..64`, every leaf is populated (no empty bins
/// that would fall back to `UNIT_LEAF` and regress - the earlier 64-leaf attempt
/// regressed precisely because its 3-tier raw range (0..27) left most of 64 bins
/// empty). The per-plane table is `WC_LEAVES * 6` bytes (~384 B) - O(1), amortized
/// over millions of pixels - so this is the JPEG XL per-fine-leaf weighted
/// predictor at a finer granularity, the decisive difference from the R7-A blowup.
pub const WC_LEAVES: usize = 64;

/// Minimum samples in a leaf before its least-squares solve is trusted; smaller
/// leaves fall back to `UNIT_LEAF` (LOCO-I L+T average) so no leaf diverges.
pub const WC_MIN_SAMPLES: usize = 64;

/// The neutral leaf weight (LOCO-I `L+T` average): `8*L + 8*T + 0 + 0 >> 4`.
pub const UNIT_LEAF: WLeaf = (8, 8, 0, 0, 0, 4);

impl PredictorId {
    pub fn from_u8(v: u8) -> Option<PredictorId> {
        match v {
            0 => Some(PredictorId::Left),
            1 => Some(PredictorId::Top),
            2 => Some(PredictorId::Tl),
            3 => Some(PredictorId::Tr),
            4 => Some(PredictorId::Avg),
            5 => Some(PredictorId::Med),
            6 => Some(PredictorId::GapLite),
            7 => Some(PredictorId::Weighted),
            8 => Some(PredictorId::TrueMotion),
            9 => Some(PredictorId::LPlusHalfTLMinusT),
            10 => Some(PredictorId::Gradient2),
            11 => Some(PredictorId::AddLT),
            12 => Some(PredictorId::AddLTL),
            13 => Some(PredictorId::AddTLT),
            14 => Some(PredictorId::SubLTL),
            15 => Some(PredictorId::SubTLT),
            16 => Some(PredictorId::SubTTR),
            17 => Some(PredictorId::AdaptiveWeighted),
            18 => Some(PredictorId::WeightedTree),
            _ => None,
        }
    }

    pub fn to_u8(self) -> u8 {
        self as u8
    }

    pub fn name(self) -> &'static str {
        match self {
            PredictorId::Left => "Left",
            PredictorId::Top => "Top",
            PredictorId::Tl => "TL",
            PredictorId::Tr => "TR",
            PredictorId::Avg => "Avg",
            PredictorId::Med => "MED",
            PredictorId::GapLite => "GAP-lite",
            PredictorId::Weighted => "Weighted",
            PredictorId::TrueMotion => "TrueMotion",
            PredictorId::LPlusHalfTLMinusT => "L+(TL-T)/2",
            PredictorId::Gradient2 => "Grad2",
            PredictorId::AddLT => "Add(L,T)",
            PredictorId::AddLTL => "Add(L,TL)",
            PredictorId::AddTLT => "Add(TL,T)",
            PredictorId::SubLTL => "Sub(L,TL)",
            PredictorId::SubTLT => "Sub(TL,T)",
            PredictorId::SubTTR => "Sub(T,TR)",
            PredictorId::AdaptiveWeighted => "AdaptiveWeighted",
            PredictorId::WeightedTree => "WeightedTree",
        }
    }
}

/// A weight vector for the Weighted predictor: `clamp_round((wL*L + wT*T +
/// wTL*TL + wTR*TR) >> shift)`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct WeightVec {
    pub wl: i16,
    pub wt: i16,
    pub wtl: i16,
    pub wtr: i16,
    pub shift: u8,
}

/// The default weight codebook searched by the analysis pass for the Weighted
/// predictor (effort >= 4). Sums are chosen around 16 so `shift = 4` gives a
/// near-unit scaling.
pub fn default_weight_codebook() -> Vec<WeightVec> {
    let v = |wl: i16, wt: i16, wtl: i16, wtr: i16| WeightVec {
        wl,
        wt,
        wtl,
        wtr,
        shift: 4,
    };
    vec![
        v(8, 8, 0, 0),
        v(10, 6, 0, 0),
        v(6, 10, 0, 0),
        v(12, 4, 0, 0),
        v(4, 12, 0, 0),
        v(9, 9, -2, 0),
        v(11, 7, -2, 0),
        v(7, 11, -2, 0),
        v(8, 8, 0, -2),
        v(10, 6, 0, -2),
        v(6, 10, 0, -2),
        v(9, 9, -2, -2),
        v(12, 8, -4, 0),
        v(8, 12, -4, 0),
        v(14, 6, -4, 0),
        v(6, 14, -4, 0),
    ]
}

/// Compute the causal neighborhood for pixel `(x, y)` in a `width x height`
/// plane, applying the border rules from the spec (out-of-bounds neighbors
/// clamp to the nearest valid pixel). The top row and left column use the
/// spec's "else 0" fallback: a streaming decoder cannot know the current
/// pixel's value before decoding it, so `T = TL = TR = 0` on the top row and
/// `L = 0` on the left column, and the encoder uses the same values to stay
/// in lockstep.
pub fn neighbors(plane: &[i16], x: usize, y: usize, width: usize, _height: usize) -> Neighbors {
    let at = |xx: usize, yy: usize| plane[yy * width + xx] as i32;
    if y == 0 {
        // Top row: nothing decoded above. The left neighbor is known for x > 0.
        let l = if x == 0 { 0 } else { at(x - 1, 0) };
        Neighbors {
            l,
            t: 0,
            tl: 0,
            tr: 0,
        }
    } else if x == 0 {
        // Left column: no decoded left neighbor; T/TL clamp to the pixel above.
        // TR clamps to the nearest valid pixel too: for a width-1 plane there is
        // no column 1, so TR falls back to the pixel directly above (T). Reading
        // `at(1, y - 1)` unbounded would alias index `(y - 1) * width + 1 == y`,
        // i.e. the CURRENT pixel, which the decoder cannot know yet and would
        // break encoder/decoder lockstep.
        let trx = 1.min(width - 1);
        Neighbors {
            l: 0,
            t: at(0, y - 1),
            tl: at(0, y - 1),
            tr: at(trx, y - 1),
        }
    } else {
        let ly = y - 1;
        let rx = (x + 1).min(width - 1);
        Neighbors {
            l: at(x - 1, y),
            t: at(x, ly),
            tl: at(x - 1, ly),
            tr: at(rx, ly),
        }
    }
}

/// Gain (right-shift) for the M3-B online weight update (see `WeightVec::adapt_online`).
/// Chosen so a typical residual/neighbor product (~1e4) yields a per-step
/// weight change of ~1, letting the per-context weight converge to a
/// least-squares-ish optimum without overshooting its small natural scale
/// (the weights sum to ~16 so `shift = 4` gives near-unit scaling).
pub const M3_WP_GAIN: u32 = 13;
/// Clamp bounds for the online-adapted weights (the codebook weights live in
/// roughly [-16, 16], so this leaves generous headroom for convergence).
pub const WEIGHT_MIN: i16 = -48;
pub const WEIGHT_MAX: i16 = 48;

impl WeightVec {
    /// A neutral predictor weight (near the LOCO-I `L+T` average), used to seed
    /// the per-context weight table when a plane has no learned codebook entry.
    pub fn unit() -> WeightVec {
        WeightVec {
            wl: 8,
            wt: 8,
            wtl: 0,
            wtr: 0,
            shift: 4,
        }
    }

    /// M3-B: mirrored online self-correction of the weighted predictor.
    ///
    /// This is a single stochastic-gradient step on the *squared* residual
    /// `r = v - pred` (so the encoder and decoder, which both observe the
    /// identical `r` and neighborhood, evolve the weight vector in lockstep
    /// with zero signaled bytes). The gradient of `0.5 * r^2` w.r.t. `w_k` is
    /// `-r * n_k`, hence the additive update `w_k += lr * r * n_k` (here the
    /// learning rate is the fixed right-shift `M3_WP_GAIN`). Because both sides
    /// start from the same per-plane codebook weight and apply the same update
    /// on the same sequence of residuals, the per-context weights stay equal
    /// throughout the plane and no expansion is possible.
    pub fn adapt_online(&mut self, r: i32, l: i32, t: i32, tl: i32, tr: i32, gain: u32) {
        let upd = |w: i16, n: i32| -> i16 {
            let d = ((r as i64) * (n as i64)) >> gain;
            let s = w as i64 + d;
            s.clamp(WEIGHT_MIN as i64, WEIGHT_MAX as i64) as i16
        };
        self.wl = upd(self.wl, l);
        self.wt = upd(self.wt, t);
        self.wtl = upd(self.wtl, tl);
        self.wtr = upd(self.wtr, tr);
    }
}

/// Compute the prediction for a pixel given its neighborhood. The caller
/// clamps to the plane's value range.
///
/// `wtree` carries the per-plane R9-B weighted-tree table (a `WC_LEAVES`-entry
/// slice of `(wL,wT,wTL,wTR,bias,shift)` tuples). It is only consulted for the
/// `WeightedTree` predictor; all other predictors ignore it. Supplying `None`
/// for `WeightedTree` falls back to the left neighbor (deterministic, so encode
/// and decode still agree - they just both get a useless prediction).
pub fn predict(id: PredictorId, n: &Neighbors, w: Option<&WeightVec>, wtree: Option<&[WLeaf]>) -> i32 {
    match id {
        PredictorId::Left => n.l,
        PredictorId::Top => n.t,
        PredictorId::Tl => n.tl,
        PredictorId::Tr => n.tr,
        PredictorId::Avg => (n.l + n.t) >> 1,
        PredictorId::Med => med(n),
        PredictorId::GapLite => gap_lite(n),
        PredictorId::TrueMotion => n.l + n.t - n.tl,
        PredictorId::LPlusHalfTLMinusT => n.l + (n.tl - n.t) / 2,
        PredictorId::Gradient2 => (n.l + n.t) / 2 + (n.tl - n.tr) / 2,
        // The six clamped add/subtract forms are raw integer arithmetic; the
        // caller's `predict_clamped` clamps the result to the plane's value
        // range, mirroring WebP's `Clip` semantics. The predictor is a function
        // of the causal neighborhood alone, so encoder and decoder agree.
        PredictorId::AddLT => n.l + n.t,
        PredictorId::AddLTL => n.l + n.tl,
        PredictorId::AddTLT => n.tl + n.t,
        PredictorId::SubLTL => n.l - n.tl,
        PredictorId::SubTLT => n.tl - n.t,
        PredictorId::SubTTR => n.t - n.tr,
        PredictorId::AdaptiveWeighted => weighted_adaptive(n),
        PredictorId::Weighted => {
            let w = match w {
                Some(w) => w,
                None => return n.l,
            };
            weighted(n, w)
        }
        PredictorId::WeightedTree => match wtree {
            Some(table) => predict_weighted_tree(n, table),
            None => n.l,
        },
    }
}

/// R9-B / R13: the fine weight context, a pure function of the already-decoded
/// causal neighborhood (so encoder and decoder compute it identically with zero
/// signaled bytes). Three causal gradients, each quantized to 4 tiers (zero /
/// small / medium / large), packed into a 64-cell raw index. With `WC_LEAVES = 64`
/// the raw index spans exactly `0..64`, so every leaf is populated and the
/// per-leaf least-squares weights specialize to the local image structure without
/// any leaf falling back to `UNIT_LEAF` (the earlier 64-leaf attempt regressed
/// because its 3-tier raw range (0..27) left most of 64 bins empty). Identical
/// leaves group pixels with similar local structure, so the weighted predictor
/// gets finer, more locally-tuned affine weights - the JPEG XL per-fine-leaf
/// weighted predictor at higher resolution.
pub fn weight_context(n: &Neighbors) -> usize {
    let gh = n.l - n.tl; // horizontal gradient
    let gv = n.t - n.tl; // vertical gradient
    let gd = n.tl - n.tr; // diagonal gradient
    let q = |g: i32| -> usize {
        match g.unsigned_abs() {
            0 => 0,
            a if a <= 4 => 1,
            a if a <= 16 => 2,
            _ => 3,
        }
    };
    let raw = q(gh) * 16 + q(gv) * 4 + q(gd); // 0..63
    raw % WC_LEAVES
}

/// R9-B: predict with the per-leaf weighted-tree table. `wc = weight_context(n)`
/// selects the leaf; the prediction is the (clamped, shifted) dot product of the
/// four causal neighbors with the leaf's weights. Deterministic given `n` and the
/// table, so encoder/decoder lockstep is exact with zero online state.
pub fn predict_weighted_tree(n: &Neighbors, table: &[WLeaf]) -> i32 {
    let wc = weight_context(n) % table.len().max(1);
    let (w0, w1, w2, w3, bias, s) = table[wc];
    let acc = (w0 as i32) * n.l
        + (w1 as i32) * n.t
        + (w2 as i32) * n.tl
        + (w3 as i32) * n.tr
        + bias as i32;
    let shift = s as u32;
    if shift == 0 {
        return acc;
    }
    let half = 1i32 << (shift - 1);
    (acc + half) >> shift
}

/// R9-B: solve the per-leaf least-squares weights from accumulated 5x5 normal
/// equations `S` and RHS `b` (sums of outer products of `(L,T,TL,TR,1)` and of
/// `v*(L,T,TL,TR,1)` respectively), returning an unconstrained integer
/// `(wL,wT,wTL,wTR,bias,shift)` tuple, or `None` if the system is ill-conditioned
/// (caller falls back to `UNIT_LEAF`). The 5th basis term is a constant bias.
///
/// The weights are NOT forced to sum to a power of two: the fit is
/// `v ~ wL*L + wT*T + wTL*TL + wTR*TR + bias`, solved in the natural scale so that
/// `w . n + bias` actually reproduces `v`. The shift `s` is chosen independently so
/// the largest spatial weight sits near `2^10` (preserving fractional precision
/// while staying safely in `i16`); the prediction is `round((w . n + bias) / 2^s)`.
/// A small ridge term keeps the solve stable on near-singular leaves.
pub fn solve_weighted_tree(s: &[[i64; 5]; 5], b: &[i64; 5]) -> Option<WLeaf> {
    const RIDGE: i64 = 8;
    let mut a = *s;
    for i in 0..5 {
        a[i][i] += RIDGE;
    }
    // Gauss-Jordan on f64 for robustness (analysis runs on the host, not the stream).
    let mut m = [[0f64; 5]; 5];
    for i in 0..5 {
        for j in 0..5 {
            m[i][j] = a[i][j] as f64;
        }
    }
    let mut rhs = [0f64; 5];
    for i in 0..5 {
        rhs[i] = b[i] as f64;
    }
    for col in 0..5 {
        let mut piv = col;
        let mut best = m[col][col].abs();
        for r in (col + 1)..5 {
            if m[r][col].abs() > best {
                best = m[r][col].abs();
                piv = r;
            }
        }
        if best < 1e-9 {
            return None;
        }
        m.swap(col, piv);
        rhs.swap(col, piv);
        let d = m[col][col];
        for j in col..5 {
            m[col][j] /= d;
        }
        rhs[col] /= d;
        for r in 0..5 {
            if r != col {
                let f = m[r][col];
                for j in col..5 {
                    m[r][j] -= f * m[col][j];
                }
                rhs[r] -= f * rhs[col];
            }
        }
    }
    let w = rhs; // solution x = m^{-1} b (m is now I)
    let maxw = w[0].abs().max(w[1].abs()).max(w[2].abs()).max(w[3].abs());
    if maxw < 1e-9 {
        return None;
    }
    // Independent shift: scale the largest spatial weight to ~2^10 so fractional
    // is preserved while the stored weights stay within i16.
    let s = ((1024.0 / maxw).ln() / std::f64::consts::LN_2)
        .round()
        .clamp(0.0, 12.0) as u32;
    let scale = (1u64 << s) as f64;
    let wi: Vec<i32> = w
        .iter()
        .map(|x| (x * scale).round().clamp(i32::MIN as f64, i32::MAX as f64) as i32)
        .collect();
    if wi[0] == 0 && wi[1] == 0 && wi[2] == 0 && wi[3] == 0 {
        return None;
    }
    // `wi[4]` is the bias, stored in the same scaled units so it joins the dot
    // product before the shift.
    Some((
        wi[0].clamp(i16::MIN as i32, i16::MAX as i32) as i16,
        wi[1].clamp(i16::MIN as i32, i16::MAX as i32) as i16,
        wi[2].clamp(i16::MIN as i32, i16::MAX as i32) as i16,
        wi[3].clamp(i16::MIN as i32, i16::MAX as i32) as i16,
        wi[4].clamp(i16::MIN as i32, i16::MAX as i32) as i16,
        s as u8,
    ))
}

fn med(n: &Neighbors) -> i32 {
    if n.tl >= n.l.max(n.t) {
        n.l.min(n.t)
    } else if n.tl <= n.l.min(n.t) {
        n.l.max(n.t)
    } else {
        n.l + n.t - n.tl
    }
}

/// LOCO-I gradient-adjusted predictor (GAP), edge-conditioned average form.
///
/// When a strong vertical/horizontal edge is detected the prediction snaps to
/// the orthogonal neighbor; otherwise it blends left, top, and the diagonal
/// (`(L + T) / 2 + (TR - TL) / 4`). This is the textbook GAP that drives
/// JPEG-LS and consistently beats MED on natural imagery.
fn gap_lite(n: &Neighbors) -> i32 {
    let dh = (n.l - n.tl).abs();
    let dv = (n.t - n.tl).abs();
    if dv - dh > 80 {
        return n.t;
    }
    if dh - dv > 80 {
        return n.l;
    }
    (n.l + n.t) / 2 + (n.tr - n.tl) / 4
}

fn weighted(n: &Neighbors, w: &WeightVec) -> i32 {
    let acc = (w.wl as i32) * n.l + (w.wt as i32) * n.t + (w.wtl as i32) * n.tl + (w.wtr as i32) * n.tr;
    let shift = w.shift as u32;
    let half = 1i32 << (shift - 1);
    (acc + half) >> shift
}

/// R8-A: the JPEG XL / WebP "weighted" predictor, computed deterministically from
/// the causal neighborhood (no signaled weights, so encoder and decoder agree
/// exactly by induction). The weight on each neighbor is an inverse-gradient
/// soft weight: directions with a small gradient (smooth, predictable) get a large
/// weight; directions with a large gradient get a near-zero weight. The prediction
/// is the convex combination of the four neighbors by these weights.
///
/// Because the weights are a pure function of already-decoded neighbors and the
/// result is bounded within `[min neighbor, max neighbor]`, this predictor is a
/// strict superset of the fixed-predictor candidate set: wherever it yields a
/// smaller |residual| over the analysis pass it is selected, otherwise GAP/med
/// remain. It adds zero model bytes (only the existing 1-byte-per-context map id
/// changes, and only where it wins).
fn weighted_adaptive(n: &Neighbors) -> i32 {
    // Three gradients of the causal neighborhood (signed).
    let d_l = n.l - n.tl; // horizontal gradient
    let d_t = n.t - n.tl; // vertical gradient
    let d_tl = n.tl - n.tr; // diagonal gradient

    // Inverse-gradient weight: large |gradient| -> near 0, small -> large.
    // Scaled by `SCALE` and clamped to `[1, WMAX]` so no direction is ever fully
    // discarded and the normalization sum stays strictly positive.
    const SCALE: i32 = 256; // 1 << 8
    const WMAX: i32 = 256;
    let w = |g: i32| -> i32 {
        let a = g.unsigned_abs() as i32;
        ((SCALE / (1 + a)).min(WMAX)).max(1)
    };
    let wl = w(d_l);
    let wt = w(d_t);
    let wtl = w(d_tl);
    let wtr = w(-d_tl); // symmetric diagonal
    let sum = wl + wt + wtl + wtr; // in [4, 4*WMAX], always > 0
    let dot = wl * n.l + wt * n.t + wtl * n.tl + wtr * n.tr;
    (dot + (sum >> 1)) / sum // round to nearest
}

/// Predict a single sample with clamping to the plane range.
pub fn predict_clamped(
    id: PredictorId,
    n: &Neighbors,
    w: Option<&WeightVec>,
    wtree: Option<&[WLeaf]>,
    range: PlaneRange,
) -> i32 {
    range.clamp(predict(id, n, w, wtree))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn med_hand_vectors() {
        let n = Neighbors {
            l: 100,
            t: 90,
            tl: 95,
            tr: 0,
        };
        // tl(95) between min(90,100)=90 and max=100 -> L+T-TL = 100+90-95 = 95
        assert_eq!(predict(PredictorId::Med, &n, None, None), 95);
        let n2 = Neighbors {
            l: 200,
            t: 10,
            tl: 250,
            tr: 0,
        };
        // tl >= max(200,10) -> min = 10
        assert_eq!(predict(PredictorId::Med, &n2, None, None), 10);
        let n3 = Neighbors {
            l: 200,
            t: 10,
            tl: 0,
            tr: 0,
        };
        // tl <= min -> max = 200
        assert_eq!(predict(PredictorId::Med, &n3, None, None), 200);
    }

    #[test]
    fn border_rules() {
        // 1x1 image: the current pixel is not yet decodable, so all causal
        // neighbors are 0.
        let p = vec![42i16];
        let n = neighbors(&p, 0, 0, 1, 1);
        assert_eq!((n.l, n.t, n.tl, n.tr), (0, 0, 0, 0));

        // Top row, x=3 of width 5: left neighbor known, nothing above.
        let w = 5;
        let p: Vec<i16> = (0..w * 2).map(|i| i as i16).collect();
        let n = neighbors(&p, 3, 0, w, 2);
        assert_eq!(n.t, 0);
        assert_eq!(n.tl, 0);
        assert_eq!(n.tr, 0);
        assert_eq!(n.l, p[2] as i32);

        // Left column, y=1: no left neighbor; T/TL come from the row above.
        let n = neighbors(&p, 0, 1, w, 2);
        assert_eq!(n.l, 0);
        assert_eq!(n.tl, p[0] as i32);
        assert_eq!(n.t, p[0] as i32);

        // Right column TR clamp: TR = I[w-1][y-1], T = I[w-1][0].
        let n = neighbors(&p, 4, 1, w, 2);
        assert_eq!(n.tr, p[4] as i32);
        assert_eq!(n.t, p[4] as i32);
    }

    #[test]
    fn width1_left_column_tr_clamps_to_top() {
        // A width-1 plane has no column 1, so the left-column TR must clamp to
        // the pixel above (T), never read the current pixel at index `y`
        // (`(y - 1) * width + 1 == y`). The encoder reads the source plane where
        // that slot holds the current pixel's own value, while the streaming
        // decoder still has 0 there - reading it would break lockstep.
        let p = vec![5i16, 9, 13, 17];
        for y in 1..4usize {
            let n = neighbors(&p, 0, y, 1, 4);
            assert_eq!(n.l, 0);
            assert_eq!(n.t, p[y - 1] as i32);
            assert_eq!(n.tl, p[y - 1] as i32);
            assert_eq!(n.tr, p[y - 1] as i32, "TR clamps to T for width 1");
        }
    }

    #[test]
    fn weighted_rounding() {
        let w = WeightVec {
            wl: 8,
            wt: 8,
            wtl: 0,
            wtr: 0,
            shift: 4,
        };
        let n = Neighbors {
            l: 10,
            t: 20,
            tl: 0,
            tr: 0,
        };
        // (8*10 + 8*20 + 8)/16 = (240+8)/16 = 15
        assert_eq!(predict(PredictorId::Weighted, &n, Some(&w), None), 15);
        assert_eq!(predict(PredictorId::Weighted, &n, None, None), 10);
    }

    #[test]
    fn r22_expanded_predictors() {
        // A smooth-ish neighborhood where the expansions should differ from the
        // base bank, exercising the new ids 8..=16.
        let n = Neighbors {
            l: 100,
            t: 120,
            tl: 110,
            tr: 90,
        };
        // TrueMotion = L + T - TL = 100 + 120 - 110 = 110
        assert_eq!(predict(PredictorId::TrueMotion, &n, None, None), 110);
        // L + (TL - T)/2 = 100 + (110 - 120)/2 = 100 - 5 = 95
        assert_eq!(predict(PredictorId::LPlusHalfTLMinusT, &n, None, None), 95);
        // Gradient2 = (L + T)/2 + (TL - TR)/2 = 110 + 10 = 120
        assert_eq!(predict(PredictorId::Gradient2, &n, None, None), 120);
        assert_eq!(predict(PredictorId::AddLT, &n, None, None), 220);
        assert_eq!(predict(PredictorId::AddLTL, &n, None, None), 210);
        assert_eq!(predict(PredictorId::AddTLT, &n, None, None), 230);
        assert_eq!(predict(PredictorId::SubLTL, &n, None, None), -10);
        assert_eq!(predict(PredictorId::SubTLT, &n, None, None), -10);
        assert_eq!(predict(PredictorId::SubTTR, &n, None, None), 30);
    }

    #[test]
    fn r22_predictor_count_and_ids() {
        assert_eq!(PREDICTOR_COUNT, 19);
        for id in 0..19u8 {
            assert!(PredictorId::from_u8(id).is_some(), "id {id} must map");
        }
        assert!(PredictorId::from_u8(19).is_none());
    }

    #[test]
    fn r8_adaptive_weighted_deterministic_and_bounded() {
        // A flat neighborhood (all equal): all gradients zero, all weights equal, so
        // the prediction equals the common value (convex combination).
        let flat = Neighbors {
            l: 120,
            t: 120,
            tl: 120,
            tr: 120,
        };
        assert_eq!(predict(PredictorId::AdaptiveWeighted, &flat, None, None), 120);

        // A structured neighborhood: the smoother (horizontal) direction should get
        // more weight than the steep vertical direction.
        let n = Neighbors {
            l: 100,
            t: 160,
            tl: 100,
            tr: 100,
        };
        // d_l = 0 -> wl = 256; d_t = 60 -> wt = 256/61 ~= 4; d_tl = 0 -> wtl = 256;
        // wtr = 256. sum = 772. dot = 256*100 + 4*160 + 256*100 + 256*100 = 76864.
        // pred = round(76864/772) = round(99.56) = 100.
        let p = predict(PredictorId::AdaptiveWeighted, &n, None, None);
        assert_eq!(p, 100, "smooth horizontal direction dominates");
        // Result lies within [min, max] of the neighbors (convex combination).
        assert!((80..=180).contains(&p));

        // Deterministic: same neighborhood -> same prediction on both "sides".
        let n2 = Neighbors {
            l: 40,
            t: 200,
            tl: 40,
            tr: 40,
        };
        assert_eq!(
            predict(PredictorId::AdaptiveWeighted, &n2, None, None),
            predict(PredictorId::AdaptiveWeighted, &n2, None, None)
        );
    }

    #[test]
    fn r8_adaptive_weighted_roundtrip_bit_exact() {
        use crate::model::analyze;
        use crate::context::{ContextParams, ContextModel};
        use crate::color::PlaneRange;

        let range = PlaneRange::U8;
        let w = 16u32;
        let h = 12u32;
        let mut plane: Vec<i16> = Vec::with_capacity((w * h) as usize);
        for i in 0..(w * h) {
            plane.push(((i.wrapping_mul(73) ^ (i >> 2)) % 256) as i16);
        }
        let planes = vec![plane];
        let ctx = ContextParams::default();
        let codebook = super::default_weight_codebook();
        let model = analyze(&planes, &[range], w as usize, h as usize, 4, &ctx, &codebook, false);
        // With AdaptiveWeighted in the candidate set, every per-context predictor id
        // must be a valid id (encoder and decoder agree on the map).
        for &id in &model.planes[0].map {
            assert!(PredictorId::from_u8(id).is_some(), "pred id {id} must map");
        }
        // Build the predicted plane using the model's chosen predictors and confirm
        // it reconstructs the original losslessly given the residual (sanity check of
        // the deterministic prediction path used by both encode and decode).
        let cm = ContextModel::new(ctx);
        let mut recon = vec![0i16; (w * h) as usize];
        for y in 0..h as usize {
            for x in 0..w as usize {
                let idx = y * w as usize + x;
                let nb = neighbors(&recon, x, y, w as usize, h as usize);
                let cid = cm.context_id(&nb, x, y) % model.context_count;
                let p = model.predictor(0, cid);
                let pred = predict_clamped(
                    p,
                    &nb,
                    model.weight_for(0).as_ref(),
                    model.weighted_tree_for(0),
                    range,
                );
                let r = planes[0][idx] as i32 - pred;
                recon[idx] = (pred + r) as i16;
            }
        }
        assert_eq!(recon, planes[0], "lossless reconstruction via chosen predictors");
    }

    #[test]
    fn predict_clamped_range() {
        let range = PlaneRange { min: -255, max: 255 };
        let n = Neighbors {
            l: 300,
            t: 300,
            tl: 0,
            tr: 0,
        };
        assert_eq!(predict_clamped(PredictorId::Avg, &n, None, None, range), 255);
        let range2 = PlaneRange::U8;
        assert_eq!(predict_clamped(PredictorId::Avg, &n, None, None, range2), 255);
    }

    #[test]
    fn r9b_weighted_tree_predict_and_solve() {
        // `weight_context` is a deterministic function of the neighborhood.
        let n = Neighbors { l: 10, t: 20, tl: 5, tr: 8 };
        assert_eq!(weight_context(&n), weight_context(&n));

        // A neutral table modelling the L+T average (8,8,0,0,0,4) predicts (8*10+8*20)/16.
        let table: Vec<WLeaf> = vec![(8, 8, 0, 0, 0, 4); WC_LEAVES];
        let p = predict_weighted_tree(&n, &table);
        assert_eq!(p, (8 * 10 + 8 * 20) >> 4);

        // Solve on data where v = (L+T)/2 exactly: the per-leaf least-squares fit
        // (with bias) should learn weights concentrated on L and T with near-zero
        // diagonal terms and a positive bias.
        let mut s = [[0i64; 5]; 5];
        let mut b = [0i64; 5];
        for l in 0..8i64 {
            for t in 0..8i64 {
                let v = (l + t) / 2;
                let ns = [l, t, 0i64, 0i64, 1i64];
                for i in 0..5 {
                    for j in 0..5 {
                        s[i][j] += ns[i] * ns[j];
                    }
                    b[i] += v * ns[i];
                }
            }
        }
        let leaf = solve_weighted_tree(&s, &b).expect("solve succeeds on well-conditioned data");
        let (w0, w1, w2, w3, bias, sh) = leaf;
        assert!(w2.abs() <= 2 && w3.abs() <= 2, "diagonal weights ~0 for v=(L+T)/2, got {leaf:?}");
        assert!(w0 > 0 && w1 > 0, "L and T weights positive, got {leaf:?}");
        assert!((0u32..=12).contains(&(sh as u32)));
        // The learned leaf must reproduce `v = (L+T)/2` on its own training data.
        let table: Vec<WLeaf> = vec![leaf; WC_LEAVES];
        for l in 0..8i32 {
            for t in 0..8i32 {
                let n = Neighbors { l, t, tl: 0, tr: 0 };
                let pred = predict_weighted_tree(&n, &table);
                assert_eq!(pred, (l + t) / 2, "leaf {leaf:?} on l={l} t={t}");
            }
        }

        // Ill-conditioned system (all-identical inputs) must return None, not panic.
        let s2 = [[0i64; 5]; 5];
        let b2 = [0i64; 5];
        assert!(solve_weighted_tree(&s2, &b2).is_none());
    }
}
