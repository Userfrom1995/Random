//! R10 transforms: JPEG XL-class Squeeze (recursive group transform) and
//! chroma-from-luma (CFL) decorrelation.
//!
//! Both are *reversible pre-processing* applied to the plane samples before the
//! existing per-plane coding loop runs. Squeeze splits a plane into sub-bands
//! (each its own `i16` plane with its own `(w, h)`); the coding loop treats each
//! sub-band as an ordinary coding plane. CFL subtracts a scaled luma prediction
//! from chroma planes in the original plane space, before Squeeze, so it composes
//! transparently: CFL subtract, then Squeeze on encode; unsqueeze, then CFL
//! add-back on decode. Both are gated by the never-expand safety net and are
//! bit-exact round-trip by construction.

/// Minimum sub-band dimension. A sub-band smaller than this stops recursing, so
/// the leaf is the whole remaining plane as a single band.
pub const MIN_SQ: usize = 4;

/// Split a `w x h` plane into the four even/odd quadrants (LL, HL, LH, HH), each
/// `(w/2) x (h/2)`. Halves use integer (floor) division, so an odd trailing row
/// or column is absorbed; the decoder mirrors the exact same split.
/// Split a `w x h` plane into the four even/odd quadrants (LL, HL, LH, HH).
/// `LL` = even row, even col (`ew x eh`); `HL` = even row, odd col (`ow x eh`);
/// `LH` = odd row, even col (`ew x oh`); `HH` = odd row, odd col (`ow x oh`).
/// `ew = ceil(w/2)`, `ow = w/2`, `eh = ceil(h/2)`, `oh = h/2`. Floor (integer)
/// division means an odd trailing row/column is folded into the even group, so
/// the split is total and invertible; the decoder mirrors it exactly.
fn split4(plane: &[i16], w: usize, h: usize) -> (Vec<i16>, Vec<i16>, Vec<i16>, Vec<i16>) {
    let ew = w.div_ceil(2);
    let ow = w / 2;
    let eh = h.div_ceil(2);
    let oh = h / 2;
    let mut ll = vec![0i16; ew * eh];
    let mut hl = vec![0i16; ow * eh];
    let mut lh = vec![0i16; ew * oh];
    let mut hh = vec![0i16; ow * oh];
    for j in 0..eh {
        for i in 0..ew {
            ll[j * ew + i] = plane[(2 * j) * w + (2 * i)];
        }
    }
    for j in 0..eh {
        for i in 0..ow {
            hl[j * ow + i] = plane[(2 * j) * w + (2 * i + 1)];
        }
    }
    for j in 0..oh {
        for i in 0..ew {
            lh[j * ew + i] = plane[(2 * j + 1) * w + (2 * i)];
        }
    }
    for j in 0..oh {
        for i in 0..ow {
            hh[j * ow + i] = plane[(2 * j + 1) * w + (2 * i + 1)];
        }
    }
    (ll, hl, lh, hh)
}

/// Bordered LL sample accessor: out-of-bounds indices clamp to the in-bounds edge
/// so the encoder and decoder agree on the predicted value (border rule from the
/// R10 blueprint: an out-of-bounds LL neighbor is replaced by the in-bounds one).
#[inline]
fn ll_at(ll: &[i16], bw: usize, bh: usize, x: usize, y: usize) -> i32 {
    let cx = x.min(bw.saturating_sub(1));
    let cy = y.min(bh.saturating_sub(1));
    ll[cy * bw + cx] as i32
}

/// JPEG XL-class Squeeze. Returns the sub-bands in post-order: LL's own bands
/// first (because the decoder needs LL before it can predict the HF bands), then
/// the HL, LH, HH residuals of this level. Each band is `(data, bw, bh)`.
///
/// Recurses on the LL band first; stops when `levels == 0` or the plane is at
/// most `MIN_SQ` on a side (the leaf is the whole remaining plane as one band).
pub fn squeeze(plane: &[i16], w: usize, h: usize, levels: u8) -> Vec<(Vec<i16>, usize, usize)> {
    if levels == 0 || w <= MIN_SQ || h <= MIN_SQ {
        return vec![(plane.to_vec(), w, h)];
    }
    let (ll, hl, lh, hh) = split4(plane, w, h);
    let ew = w.div_ceil(2);
    let ow = w / 2;
    let eh = h.div_ceil(2);
    let oh = h / 2;
    // Predict each HF band from the LL band only, with pure integer interpolation
    // (i32 arithmetic; `>> 1` / `>> 2` are floor shifts). Residuals are exact.
    let mut hl_res = vec![0i16; ow * eh];
    let mut lh_res = vec![0i16; ew * oh];
    let mut hh_res = vec![0i16; ow * oh];
    for j in 0..eh {
        for i in 0..ow {
            let pred_hl = (ll_at(&ll, ew, eh, i, j) + ll_at(&ll, ew, eh, i, j + 1)) >> 1;
            hl_res[j * ow + i] = (hl[j * ow + i] as i32 - pred_hl) as i16;
        }
    }
    for j in 0..oh {
        for i in 0..ew {
            let pred_lh = (ll_at(&ll, ew, eh, i, j) + ll_at(&ll, ew, eh, i + 1, j)) >> 1;
            lh_res[j * ew + i] = (lh[j * ew + i] as i32 - pred_lh) as i16;
        }
    }
    for j in 0..oh {
        for i in 0..ow {
            let pred_hh = (ll_at(&ll, ew, eh, i, j)
                + ll_at(&ll, ew, eh, i + 1, j)
                + ll_at(&ll, ew, eh, i, j + 1)
                + ll_at(&ll, ew, eh, i + 1, j + 1))
                >> 2;
            hh_res[j * ow + i] = (hh[j * ow + i] as i32 - pred_hh) as i16;
        }
    }
    // Recurse on LL first (post-order) so LL's bands precede the HF residuals.
    let mut out = squeeze(&ll, ew, eh, levels - 1);
    out.push((hl_res, ow, eh));
    out.push((lh_res, ew, oh));
    out.push((hh_res, ow, oh));
    out
}

/// Mirror of `squeeze`: reconstruct the full `w x h` plane from its sub-bands.
/// Reads the LL subtree first, then adds the LL-based predictions back to the HF
/// bands, then combines the four quadrants. Inverts `squeeze` exactly.
pub fn unsqueeze(bands: &[(Vec<i16>, usize, usize)], w: usize, h: usize, levels: u8) -> Vec<i16> {
    let mut idx = 0usize;
    unsqueeze_rec(bands, &mut idx, w, h, levels)
}

fn unsqueeze_rec(
    bands: &[(Vec<i16>, usize, usize)],
    idx: &mut usize,
    w: usize,
    h: usize,
    levels: u8,
) -> Vec<i16> {
    if levels == 0 || w <= MIN_SQ || h <= MIN_SQ {
        let (data, bw, bh) = &bands[*idx];
        *idx += 1;
        debug_assert_eq!(*bw, w, "squeeze band width mismatch");
        debug_assert_eq!(*bh, h, "squeeze band height mismatch");
        return data.clone();
    }
    let ew = w.div_ceil(2);
    let ow = w / 2;
    let eh = h.div_ceil(2);
    let oh = h / 2;
    // LL subtree first (post-order).
    let ll = unsqueeze_rec(bands, idx, ew, eh, levels - 1);
    let (hl_res, hbw, hbh) = &bands[*idx];
    debug_assert_eq!(*hbw, ow, "squeeze HL band width mismatch");
    debug_assert_eq!(*hbh, eh, "squeeze HL band height mismatch");
    let hl_res = hl_res.clone();
    *idx += 1;
    let (lh_res, lbw, lbh) = &bands[*idx];
    debug_assert_eq!(*lbw, ew, "squeeze LH band width mismatch");
    debug_assert_eq!(*lbh, oh, "squeeze LH band height mismatch");
    let lh_res = lh_res.clone();
    *idx += 1;
    let (hh_res, hbbw, hbbh) = &bands[*idx];
    debug_assert_eq!(*hbbw, ow, "squeeze HH band width mismatch");
    debug_assert_eq!(*hbbh, oh, "squeeze HH band height mismatch");
    let hh_res = hh_res.clone();
    *idx += 1;
    // Add the LL-based predictions back to the HF residuals.
    let mut hl = vec![0i16; ow * eh];
    let mut lh = vec![0i16; ew * oh];
    let mut hh = vec![0i16; ow * oh];
    for j in 0..eh {
        for i in 0..ow {
            let pred_hl = (ll_at(&ll, ew, eh, i, j) + ll_at(&ll, ew, eh, i, j + 1)) >> 1;
            hl[j * ow + i] = (hl_res[j * ow + i] as i32 + pred_hl) as i16;
        }
    }
    for j in 0..oh {
        for i in 0..ew {
            let pred_lh = (ll_at(&ll, ew, eh, i, j) + ll_at(&ll, ew, eh, i + 1, j)) >> 1;
            lh[j * ew + i] = (lh_res[j * ew + i] as i32 + pred_lh) as i16;
        }
    }
    for j in 0..oh {
        for i in 0..ow {
            let pred_hh = (ll_at(&ll, ew, eh, i, j)
                + ll_at(&ll, ew, eh, i + 1, j)
                + ll_at(&ll, ew, eh, i, j + 1)
                + ll_at(&ll, ew, eh, i + 1, j + 1))
                >> 2;
            hh[j * ow + i] = (hh_res[j * ow + i] as i32 + pred_hh) as i16;
        }
    }
    // combine4: interleave LL/HL/LH/HH back into the full plane, honoring odd
    // trailing rows/columns (the even group holds ceil(w/2) / ceil(h/2) samples).
    let mut out = vec![0i16; w * h];
    for j in 0..eh {
        for i in 0..ew {
            out[(2 * j) * w + (2 * i)] = ll[j * ew + i];
        }
    }
    for j in 0..eh {
        for i in 0..ow {
            out[(2 * j) * w + (2 * i + 1)] = hl[j * ow + i];
        }
    }
    for j in 0..oh {
        for i in 0..ew {
            out[(2 * j + 1) * w + (2 * i)] = lh[j * ew + i];
        }
    }
    for j in 0..oh {
        for i in 0..ow {
            out[(2 * j + 1) * w + (2 * i + 1)] = hh[j * ow + i];
        }
    }
    out
}

/// The sub-band layout `(bw, bh)` that `squeeze` would produce, in the same order
/// (so the decoder can allocate and read the right number of bands without any
/// signaled sub-band metadata). The geometry `(W, H, levels)` fully determines it.
pub fn squeeze_band_layout(w: usize, h: usize, levels: u8) -> Vec<(usize, usize)> {
    if levels == 0 || w <= MIN_SQ || h <= MIN_SQ {
        return vec![(w, h)];
    }
    let ew = w.div_ceil(2);
    let ow = w / 2;
    let eh = h.div_ceil(2);
    let oh = h / 2;
    let mut out = squeeze_band_layout(ew, eh, levels - 1);
    out.push((ow, eh));
    out.push((ew, oh));
    out.push((ow, oh));
    out
}

/// CFL prediction: `round(s * luma / 8)` clamped into `[rmin, rmax]` so the
/// subtracted residual stays within the chroma plane's value range. Encoder and
/// decoder call this identical function, so the round-trip is bit-exact.
pub fn cfl_predict(s: u8, luma: i32, rmin: i32, rmax: i32) -> i32 {
    let x = (s as i32) * luma;
    // Round half up. Both encoder and decoder use the same expression, so any
    // rounding convention is fine as long as it is shared.
    let v = (x + 4) >> 3;
    v.clamp(rmin, rmax)
}

/// Maximum Squeeze level allowed for a given image dimension: the smaller of
/// `MAX_SQ_LEVELS = 4` and `log2(min(W, H)) - 1` (so the smallest sub-band stays
/// at least `MIN_SQ` on each side). Always >= 0.
pub fn max_squeeze_levels(w: usize, h: usize) -> u8 {
    let m = w.min(h);
    if m < (1usize << (MIN_SQ.trailing_zeros() + 1)) {
        // MIN_SQ is 4 = 2^2; a level is valid only if the smallest sub-band side
        // (w >> L, h >> L) stays >= MIN_SQ. Solve L <= log2(min) - 2.
        return 0;
    }
    let max_by_dim = (m.ilog2() as i32) - (MIN_SQ.ilog2() as i32);
    let max_by_dim = max_by_dim.max(0) as u8;
    4u8.min(max_by_dim)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn roundtrip_one(w: usize, h: usize, levels: u8) {
        let mut plane: Vec<i16> = (0..w * h).map(|i| ((i * 7 + 13) % 256) as i16).collect();
        // Add some structure so HF residuals are non-trivial.
        for y in 0..h {
            for x in 0..w {
                plane[y * w + x] = ((x as i32 * 3 + y as i32 * 5) % 256) as i16;
            }
        }
        let bands = squeeze(&plane, w, h, levels);
        let layout = squeeze_band_layout(w, h, levels);
        assert_eq!(bands.len(), layout.len(), "band count must match layout");
        for (b, (bw, bh)) in bands.iter().zip(layout.iter()) {
            assert_eq!(b.1, *bw);
            assert_eq!(b.2, *bh);
        }
        let back = unsqueeze(&bands, w, h, levels);
        assert_eq!(back, plane, "squeeze/unsqueeze must invert ({}x{} l{})", w, h, levels);
    }

    #[test]
    fn squeeze_inverts_various_sizes() {
        for &(w, h) in &[(8usize, 8), (16, 12), (7, 5), (1, 1), (4, 4), (32, 24), (64, 64), (5, 9)] {
            for l in 0..=4u8 {
                roundtrip_one(w, h, l);
            }
        }
    }
}
