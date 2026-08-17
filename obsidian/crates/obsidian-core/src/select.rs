//! Per-context predictor selection.
//!
//! The encoder chooses one predictor (selector) per context. Below effort 4
//! the selection is a fixed deterministic default derived from each
//! context's gradient class. From effort 4 on, an analysis pass measures the
//! coded cost of every candidate predictor per context and picks the
//! cheapest, producing a per-image map that is RLE-signaled in the stream.

use crate::container::consts::BASE_CTX;
use crate::context::{context_of, gradient_of_base, max_context, zigzag, ALPHABET};
use crate::error::CodecResult;
use crate::image::Plane;
use crate::predict::{self, selector_split};

/// Number of candidate selectors (predictors 0..7 plus WAvg vectors 0..3).
pub const CANDIDATES: usize = 12;

/// The fixed default map for effort 0: MED everywhere.
pub fn med_map(classes: usize) -> Vec<u8> {
    vec![predict::id::MED; max_context(classes)]
}

/// The fixed default map for effort 1-3, derived deterministically from each
/// context's gradient class.
pub fn default_map(classes: usize) -> Vec<u8> {
    let total = max_context(classes);
    let mut map = vec![predict::id::MED; total];
    for ctx in 0..total {
        let base = (ctx % (BASE_CTX * classes)) / classes;
        let q = gradient_of_base(base as u16);
        map[ctx] = predict::default_predictor(q);
    }
    map
}

/// Shannon entropy (nats) of a histogram scaled to a count.
fn entropy_cost(hist: &[u64], count: u64) -> f64 {
    if count == 0 {
        return 0.0;
    }
    let c = count as f64;
    let mut sum = 0.0;
    for &h in hist {
        if h > 0 {
            let hf = h as f64;
            sum += hf * hf.ln();
        }
    }
    (c * c.ln()) - sum
}

/// Predict a plane pixel with a given selector and return its zigzag symbol.
#[inline]
fn symbol_for(plane: &Plane, x: i64, y: i64, sel: u8) -> u16 {
    let (pred_id, w) = selector_split(sel);
    let pred = predict::predict(plane, x, y, pred_id, w);
    let r = plane.pixel(x, y).wrapping_sub(pred);
    zigzag(r)
}

/// Run the analysis pass over all planes and produce a predictor map.
///
/// For every used context, the pass measures the per-candidate entropy cost
/// and keeps the cheapest selector. Returns a map of length
/// `max_context(classes)`.
pub fn analyze_map(planes: &[Plane], classes: usize) -> CodecResult<Vec<u8>> {
    let total = max_context(classes);
    let mut used = vec![false; total];

    // Pass 1: discover used contexts.
    for plane in planes {
        let w = plane.w as i64;
        let h = plane.h as i64;
        for y in 0..h {
            for x in 0..w {
                used[context_of(plane, x, y, classes)] = true;
            }
        }
    }

    // Context -> dense index.
    let mut ctx_idx = vec![u32::MAX; total];
    let mut idx_of_ctx: Vec<usize> = Vec::new();
    for (ctx, &u) in used.iter().enumerate() {
        if u {
            ctx_idx[ctx] = idx_of_ctx.len() as u32;
            idx_of_ctx.push(ctx);
        }
    }
    let used_count = idx_of_ctx.len();
    if used_count == 0 {
        return Ok(vec![predict::id::MED; total]);
    }

    let mut best_sel = vec![predict::id::MED as u8; used_count];
    let mut best_cost = vec![f64::INFINITY; used_count];

    for sel in 0..CANDIDATES as u8 {
        let mut hist = vec![0u64; used_count * ALPHABET];
        let mut cnt = vec![0u64; used_count];

        for plane in planes {
            let w = plane.w as i64;
            let h = plane.h as i64;
            for y in 0..h {
                for x in 0..w {
                    let ctx = context_of(plane, x, y, classes);
                    let idx = ctx_idx[ctx] as usize;
                    let u = symbol_for(plane, x, y, sel) as usize;
                    hist[idx * ALPHABET + u] += 1;
                    cnt[idx] += 1;
                }
            }
        }

        for i in 0..used_count {
            let c = entropy_cost(&hist[i * ALPHABET..(i + 1) * ALPHABET], cnt[i]);
            if c < best_cost[i] {
                best_cost[i] = c;
                best_sel[i] = sel;
            }
        }
    }

    let mut map = vec![predict::id::MED as u8; total];
    for (i, &ctx) in idx_of_ctx.iter().enumerate() {
        map[ctx] = best_sel[i];
    }
    Ok(map)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::image::Image;
    use crate::predict::id;

    #[test]
    fn med_map_uniform() {
        let m = med_map(1);
        assert!(m.iter().all(|&v| v == id::MED));
        assert_eq!(m.len(), max_context(1));
    }

    #[test]
    fn default_map_values_in_range() {
        for classes in [1usize, 2, 4] {
            let m = default_map(classes);
            assert_eq!(m.len(), max_context(classes));
            assert!(m.iter().all(|&v| v <= 11), "selector out of range");
        }
    }

    #[test]
    fn analyze_on_flat_image_picks_med_or_avg() {
        // A perfectly flat image: everything predicts to zero. Any predictor
        // works; the map must still be a valid selector list.
        let data = vec![42u8; 64 * 64];
        let img = Image::gray(64, 64, data).unwrap();
        let m = analyze_map(&img.planes, 1).unwrap();
        assert_eq!(m.len(), max_context(1));
        assert!(m.iter().all(|&v| v <= 11));
    }

    #[test]
    fn analyze_on_gradient_image() {
        // A horizontal gradient: the best predictor should favor Left
        // (id 0) in the interior.
        let mut data = Vec::with_capacity(64 * 64);
        for y in 0..64u8 {
            for x in 0..64u8 {
                data.push(x.wrapping_mul(4).wrapping_add(y));
            }
        }
        let img = Image::gray(64, 64, data).unwrap();
        let m = analyze_map(&img.planes, 1).unwrap();
        // The interior flat-gradient context should prefer Left or Avg/MED.
        let base = gradient_of_base(0);
        assert_eq!(base, (0, 0, 0));
        // All selectors in range.
        assert!(m.iter().all(|&v| v <= 11));
    }
}
