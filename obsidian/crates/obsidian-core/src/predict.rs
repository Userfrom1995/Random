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
/// half-delta, gradient, and the six clamped add/subtract forms). Existing ids
/// are preserved so every previously-produced stream still decodes; the new ids
/// only appear in streams whose analysis pass enabled them (effort >= 4).
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
}

pub const PREDICTOR_COUNT: usize = 17;

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
///
/// R7-A expands the codebook well beyond the original 16 entries: the diagonal
/// `(wl, wt)` family is augmented with small off-diagonal `(wtl, wtr)` correction
/// terms and alternate `shift` values (3, 4, 5). The analysis pass picks the best
/// codebook weight *per spatial context* (signaled as `17 + j` in the predictor
/// map), so the codec gets a near-least-squares linear predictor everywhere
/// instead of one shared per-plane weight. All entries are generated
/// deterministically so the encoder and decoder agree without signaling them.
pub fn default_weight_codebook() -> Vec<WeightVec> {
    let v = |wl: i16, wt: i16, wtl: i16, wtr: i16, shift: u8| WeightVec {
        wl,
        wt,
        wtl,
        wtr,
        shift,
    };
    let mut out: Vec<WeightVec> = Vec::new();
    // Base diagonal, shift 4, wl + wt = 16.
    let diag = [
        (8, 8),
        (10, 6),
        (6, 10),
        (12, 4),
        (4, 12),
        (14, 2),
        (2, 14),
        (16, 0),
        (0, 16),
    ];
    for (wl, wt) in diag {
        out.push(v(wl, wt, 0, 0, 4));
    }
    // Diagonal plus small off-diagonal correction terms. `predict_weighted`
    // scales by `(acc + half) >> shift` and assumes the weights sum to
    // `2^shift == 16`, so every correction must keep `wl + wt + wtl + wtr == 16`.
    // We use antisymmetric pairs (`wtr = -wtl`) so the total never drifts.
    for (wl, wt) in [(8, 8), (10, 6), (6, 10), (12, 4), (4, 12)] {
        for wtl in [-2i16, -1, 1, 2] {
            out.push(v(wl, wt, wtl, -wtl, 4));
        }
    }
    // Diagonal with alternate shift values for sharper / softer scaling.
    for (wl, wt) in [(8, 8), (10, 6), (6, 10), (12, 4), (4, 12)] {
        out.push(v(wl, wt, 0, 0, 3));
        out.push(v(wl, wt, 0, 0, 5));
    }
    out
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
pub fn predict(id: PredictorId, n: &Neighbors, w: Option<&WeightVec>) -> i32 {
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
        PredictorId::Weighted => {
            let w = match w {
                Some(w) => w,
                None => return n.l,
            };
            weighted(n, w)
        }
    }
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

/// Predict a single sample with clamping to the plane range.
pub fn predict_clamped(
    id: PredictorId,
    n: &Neighbors,
    w: Option<&WeightVec>,
    range: PlaneRange,
) -> i32 {
    range.clamp(predict(id, n, w))
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
        assert_eq!(predict(PredictorId::Med, &n, None), 95);
        let n2 = Neighbors {
            l: 200,
            t: 10,
            tl: 250,
            tr: 0,
        };
        // tl >= max(200,10) -> min = 10
        assert_eq!(predict(PredictorId::Med, &n2, None), 10);
        let n3 = Neighbors {
            l: 200,
            t: 10,
            tl: 0,
            tr: 0,
        };
        // tl <= min -> max = 200
        assert_eq!(predict(PredictorId::Med, &n3, None), 200);
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
        assert_eq!(predict(PredictorId::Weighted, &n, Some(&w)), 15);
        assert_eq!(predict(PredictorId::Weighted, &n, None), 10);
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
        assert_eq!(predict(PredictorId::TrueMotion, &n, None), 110);
        // L + (TL - T)/2 = 100 + (110 - 120)/2 = 100 - 5 = 95
        assert_eq!(predict(PredictorId::LPlusHalfTLMinusT, &n, None), 95);
        // Gradient2 = (L + T)/2 + (TL - TR)/2 = 110 + 10 = 120
        assert_eq!(predict(PredictorId::Gradient2, &n, None), 120);
        assert_eq!(predict(PredictorId::AddLT, &n, None), 220);
        assert_eq!(predict(PredictorId::AddLTL, &n, None), 210);
        assert_eq!(predict(PredictorId::AddTLT, &n, None), 230);
        assert_eq!(predict(PredictorId::SubLTL, &n, None), -10);
        assert_eq!(predict(PredictorId::SubTLT, &n, None), -10);
        assert_eq!(predict(PredictorId::SubTTR, &n, None), 30);
    }

    #[test]
    fn r22_predictor_count_and_ids() {
        assert_eq!(PREDICTOR_COUNT, 17);
        for id in 0..17u8 {
            assert!(PredictorId::from_u8(id).is_some(), "id {id} must map");
        }
        assert!(PredictorId::from_u8(17).is_none());
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
        assert_eq!(predict_clamped(PredictorId::Avg, &n, None, range), 255);
        let range2 = PlaneRange::U8;
        assert_eq!(predict_clamped(PredictorId::Avg, &n, None, range2), 255);
    }
}
