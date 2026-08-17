//! Causal predictor bank.
//!
//! Eight predictors, ids `0..=7`: Left, Top, TL, TR, Avg, MED, GAP-lite, and
//! the weighted average (WAvg). WAvg selects one of four fixed coefficient
//! vectors from the v1 codebook; the vector index is carried by the
//! predictor-map selector value (`8..=11`).
//!
//! All predictors return a `u8` clamped to `[0, 255]`. Residualization is
//! `(pixel - pred) mod 256` (wrapping), so any predictor magnitude is
//! reversible regardless of clamping.

/// Predictor ids.
pub mod id {
    pub const LEFT: u8 = 0;
    pub const TOP: u8 = 1;
    pub const TL: u8 = 2;
    pub const TR: u8 = 3;
    pub const AVG: u8 = 4;
    pub const MED: u8 = 5;
    pub const GAP: u8 = 6;
    pub const WAVG: u8 = 7;
}

/// Selector value space: `0..=7` are predictors, `8..=11` are WAvg with
/// weight-vector index `sel - 8`.
pub const MAX_SELECTOR: u8 = 11;

/// The fixed weight codebook for WAvg: four vectors `(wL, wT, wTL, wTR)`
/// with shift `S = 4`. Deterministic so the decoder reproduces it exactly;
/// the map only signals the index.
pub const WEIGHT_CODEBOOK: [[u8; 4]; 4] = [
    [8, 8, 0, 0],
    [6, 6, 3, 1],
    [4, 12, 0, 0],
    [12, 4, 0, 0],
];

pub const WAVG_SHIFT: u32 = 4;

/// Map a selector value to a predictor id plus optional weight index.
#[inline]
pub fn selector_split(sel: u8) -> (u8, Option<usize>) {
    if sel < id::WAVG {
        (sel, None)
    } else {
        (id::WAVG, Some((sel - id::WAVG) as usize))
    }
}

/// Compute a prediction for a plane pixel from its causal neighborhood.
///
/// `x`, `y` are the coordinates of the pixel being coded; neighbors outside
/// the causal region read 0 (see [`Plane::causal_pixel`]), which keeps the
/// border rule symmetric for encoder and decoder.
#[inline]
pub fn predict(plane: &crate::image::Plane, x: i64, y: i64, pred_id: u8, weight_idx: Option<usize>) -> u8 {
    let l = plane.causal_pixel(x, y, x - 1, y) as i32;
    let t = plane.causal_pixel(x, y, x, y - 1) as i32;
    let tl = plane.causal_pixel(x, y, x - 1, y - 1) as i32;
    let tr = plane.causal_pixel(x, y, x + 1, y - 1) as i32;
    let v = match pred_id {
        id::LEFT => l,
        id::TOP => t,
        id::TL => tl,
        id::TR => tr,
        id::AVG => (l + t) >> 1,
        id::MED => med(l, t, tl),
        id::GAP => gap_lite(l, t, tl, tr),
        id::WAVG => {
            let w = WEIGHT_CODEBOOK[weight_idx.unwrap_or(0)];
            let sum = (w[0] as i32) * l + (w[1] as i32) * t + (w[2] as i32) * tl + (w[3] as i32) * tr;
            (sum + (1 << (WAVG_SHIFT - 1))) >> WAVG_SHIFT
        }
        _ => l,
    };
    v.clamp(0, 255) as u8
}

/// JPEG-LS median edge detector.
#[inline]
fn med(l: i32, t: i32, tl: i32) -> i32 {
    let mn = l.min(t);
    let mx = l.max(t);
    if tl >= mx {
        mn
    } else if tl <= mn {
        mx
    } else {
        l + t - tl
    }
}

/// CALIC-style gradient-adjusted predictor (GAP), reduced to the causal
/// neighborhood. Uses the three gradients around `TL` and a thresholded
/// blend, mirroring the GAP design from CALIC.
#[inline]
fn gap_lite(l: i32, t: i32, tl: i32, tr: i32) -> i32 {
    let dh = (l - tl).abs();
    let dv = (t - tl).abs();
    let mut pred: i32;
    if dv - dh > 80 {
        pred = l;
    } else if dh - dv > 80 {
        pred = t;
    } else {
        let w: i32;
        if dv - dh > 32 {
            w = 6;
        } else if dv - dh > 8 {
            w = 4;
        } else if dv - dh >= -8 {
            w = 0;
        } else if dv - dh >= -32 {
            w = -4;
        } else {
            w = -6;
        }
        pred = (l + t) / 2 + (t - tl) * w / 16;
        if dh <= 8 && dv <= 8 {
            // Very smooth region: blend more neighbors.
            pred = pred / 2 + (tr + t) / 4 + l / 4;
        } else if dh <= 32 && dv <= 32 {
            // Mild texture: small diagonal correction.
            pred = pred + (tr + t) / 16 - (l + tl) / 16;
        }
    }
    pred
}

/// The fixed, deterministic per-context default predictor used at effort
/// 1-3 (before the analysis pass). Derived from the quantized gradient
/// class of the context.
pub fn default_predictor(q: (i8, i8, i8)) -> u8 {
    let (q1, q2, q3) = q;
    if q1 == 0 && q2 == 0 && q3 == 0 {
        return id::MED;
    }
    // Canonical form has the first non-zero gradient positive.
    let (a1, a2, a3) = (q1 as i32, q2 as i32, q3 as i32);
    let va = a2.abs();
    let ha = a1.abs();
    let da = a3.abs();
    if va > ha && va >= da {
        id::TOP
    } else if ha >= va && ha > da {
        id::LEFT
    } else if da > 0 {
        if a3 > 0 {
            id::TL
        } else {
            id::TR
        }
    } else {
        id::MED
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::image::Plane;

    fn plane(w: i64, h: i64, data: &[u8]) -> Plane {
        Plane::new(w as u32, h as u32, data.to_vec()).unwrap()
    }

    #[test]
    fn med_classic_cases() {
        // Flat: all equal.
        assert_eq!(med(10, 10, 10), 10);
        // Vertical edge: TL is high, use min(L, T).
        assert_eq!(med(50, 60, 200), 50);
        // Horizontal edge: TL is low, use max(L, T).
        assert_eq!(med(200, 50, 0), 200);
        // Otherwise L + T - TL.
        assert_eq!(med(200, 50, 100), 150);
    }

    #[test]
    fn predictors_on_crafted_neighborhood() {
        let p = plane(5, 5, &[
            10, 20, 30, 40, 50, //
            11, 21, 31, 41, 51, //
            12, 22, 32, 42, 52, //
            13, 23, 33, 43, 53, //
            14, 24, 34, 44, 54, //
        ]);
        // Pixel (2,2) = 32. L=22, T=31, TL=21, TR=41.
        assert_eq!(predict(&p, 2, 2, id::LEFT, None), 22);
        assert_eq!(predict(&p, 2, 2, id::TOP, None), 31);
        assert_eq!(predict(&p, 2, 2, id::TL, None), 21);
        assert_eq!(predict(&p, 2, 2, id::TR, None), 41);
        assert_eq!(predict(&p, 2, 2, id::AVG, None), 26);
        assert_eq!(predict(&p, 2, 2, id::MED, None), 31); // 21 >= max(22,31)? no; 21 <= min? yes -> max = 31
    }

    #[test]
    fn wavg_weights() {
        // Vector 0 = (8,8,0,0)/16 = Avg.
        let p = plane(5, 5, &[
            0, 0, 0, 0, 0, //
            0, 10, 20, 30, 0, //
            0, 0, 0, 0, 0, //
            0, 0, 0, 0, 0, //
            0, 0, 0, 0, 0, //
        ]);
        // Pixel (1,2): L=10, T=0, TL=0, TR=0 -> (8*10 + 8*0)>>4 = 5.
        assert_eq!(predict(&p, 1, 2, id::WAVG, Some(0)), 5);
        // Vector 2 = (4,12,0,0)/16 vertical-heavy: (4*10 + 12*0)>>4 = 2 (2.5 -> round down? sum=40, +8=48, >>4 = 3).
        assert_eq!(predict(&p, 1, 2, id::WAVG, Some(2)), 3);
    }

    #[test]
    fn borders_do_not_panic() {
        let p = plane(2, 2, &[1, 2, 3, 4]);
        for pred in 0..=7 {
            let _ = predict(&p, 0, 0, pred, Some(0));
            let _ = predict(&p, 1, 0, pred, Some(0));
            let _ = predict(&p, 0, 1, pred, Some(0));
            let _ = predict(&p, 1, 1, pred, Some(0));
        }
    }

    #[test]
    fn defaults_cover_classes() {
        assert_eq!(default_predictor((0, 0, 0)), id::MED);
        assert_eq!(default_predictor((3, 0, 0)), id::LEFT);
        assert_eq!(default_predictor((0, 3, 0)), id::TOP);
        let d = default_predictor((0, 0, 3));
        assert!(d == id::TL);
        let d2 = default_predictor((1, 2, 4));
        assert!(d2 >= 0 && d2 <= 7);
    }
}
