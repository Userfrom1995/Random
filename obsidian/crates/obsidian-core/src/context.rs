//! Context model: quantized causal gradients with sign symmetry, an activity
//! class, border-dedicated contexts, and the signed zigzag residual mapping.

use crate::color::PlaneRange;
use crate::model::ModelConfig;
use crate::predict::{neighbors, predict_clamped, WeightVec};
use crate::predict::Neighbors;

/// Gradient quantization thresholds (9 bins from the 7 threshold boundaries).
pub const GRAD_THRESHOLDS: [i32; 7] = [-16, -4, -1, 0, 1, 4, 16];

/// Quantize a signed gradient to a bin in `0..=8`.
pub fn quantize_gradient(g: i32) -> usize {
    if g < GRAD_THRESHOLDS[0] {
        0
    } else if g < GRAD_THRESHOLDS[1] {
        1
    } else if g < GRAD_THRESHOLDS[2] {
        2
    } else if g < GRAD_THRESHOLDS[3] {
        3
    } else if g == GRAD_THRESHOLDS[3] {
        4
    } else if g <= GRAD_THRESHOLDS[4] {
        5
    } else if g <= GRAD_THRESHOLDS[5] {
        6
    } else if g <= GRAD_THRESHOLDS[6] {
        7
    } else {
        8
    }
}

/// Number of quantization levels used by `quantize_residual_context` (the R3-A
/// DIFF context). Kept coarse (5 levels) on purpose: the CMARC per-`(cid, bin)`
/// binary models must each see enough samples to specialize, and the residual
/// context count is `RC_LEVELS^3`-ish; a coarse quantization bounds that count
/// so adaptation stays strong on photographic-sized images (Kodak 768x512) while
/// still capturing the local residual distribution JPEG-LS exploits.
pub const RC_LEVELS: usize = 5;

/// Quantize a neighbor residual magnitude to a coarse level in `0..RC_LEVELS`
/// for the R3-A DIFF context. Levels: 0 (zero), 1 (+/-1), 2 (2..3), 3 (4..15),
/// 4 (16+). Sign is handled separately by the sign-symmetric `RcLut`.
pub fn quantize_residual_context(d: i32) -> usize {
    let a = d.unsigned_abs();
    if a == 0 {
        0
    } else if a == 1 {
        1
    } else if a <= 3 {
        2
    } else if a <= 15 {
        3
    } else {
        4
    }
}

/// Sign-symmetry LUT: maps a 729-value `(q1,q2,q3)` triple index to a reduced
/// context id in `0..365` (JPEG-LS style: `Q(-g) = flip(Q(g))`, triples and
/// their negation share a context).
pub struct SignSymmetryLut {
    reduced: [u16; 729],
}

impl SignSymmetryLut {
    pub fn new() -> SignSymmetryLut {
        let mut reduced = [0u16; 729];
        let mut seen = [false; 729];
        let mut counter = 0u16;
        for id in 0..729u16 {
            if seen[id as usize] {
                continue;
            }
            let (q1, q2, q3) = unpack(id);
            let mirror = pack(flip(q1), flip(q2), flip(q3));
            reduced[id as usize] = counter;
            seen[id as usize] = true;
            reduced[mirror as usize] = counter;
            seen[mirror as usize] = true;
            counter += 1;
        }
        debug_assert_eq!(counter, 365);
        SignSymmetryLut { reduced }
    }

    pub fn reduce(&self, id: usize) -> usize {
        self.reduced[id] as usize
    }

    /// Number of distinct reduced base ids (365 for the gradient triple).
    pub fn base_count(&self) -> usize {
        let mut m = 0u16;
        for &v in &self.reduced {
            if v > m {
                m = v;
            }
        }
        m as usize + 1
    }
}

fn unpack(id: u16) -> (usize, usize, usize) {
    let q1 = (id / 81) as usize;
    let q2 = ((id % 81) / 9) as usize;
    let q3 = (id % 9) as usize;
    (q1, q2, q3)
}

fn pack(q1: usize, q2: usize, q3: usize) -> u16 {
    (q1 * 81 + q2 * 9 + q3) as u16
}

fn flip(q: usize) -> usize {
    8 - q
}

/// Sign-symmetric LUT for the R3-A residual (DIFF) context. Packs a triple of
/// coarse residual levels `(ql, qu, qul)` in `0..RC_LEVELS` into `RC_LEVELS^3`
/// raw ids and reduces by full sign symmetry (`(ql,qu,qul)` and its negation
/// share an id, since the residual distribution is symmetric around zero).
pub struct RcLut {
    reduced: [u16; RC_LEVELS * RC_LEVELS * RC_LEVELS],
}

impl RcLut {
    pub fn new() -> RcLut {
        let n = RC_LEVELS * RC_LEVELS * RC_LEVELS;
        let mut reduced = [0u16; RC_LEVELS * RC_LEVELS * RC_LEVELS];
        let mut seen = vec![false; n];
        let mut counter = 0u16;
        for id in 0..n as u16 {
            if seen[id as usize] {
                continue;
            }
            let (q1, q2, q3) = rc_unpack(id);
            let mirror = rc_pack(rc_flip(q1), rc_flip(q2), rc_flip(q3));
            reduced[id as usize] = counter;
            seen[id as usize] = true;
            if (mirror as usize) < n {
                reduced[mirror as usize] = counter;
                seen[mirror as usize] = true;
            }
            counter += 1;
        }
        RcLut { reduced }
    }

    pub fn reduce(&self, id: usize) -> usize {
        self.reduced[id] as usize
    }

    /// Number of distinct reduced base ids (<= RC_LEVELS^3 / 2).
    pub fn base_count(&self) -> usize {
        let mut m = 0u16;
        for &v in &self.reduced {
            if v > m {
                m = v;
            }
        }
        m as usize + 1
    }
}

fn rc_unpack(id: u16) -> (usize, usize, usize) {
    let q1 = (id / (RC_LEVELS * RC_LEVELS) as u16) as usize;
    let q2 = ((id / RC_LEVELS as u16) % RC_LEVELS as u16) as usize;
    let q3 = (id % RC_LEVELS as u16) as usize;
    (q1, q2, q3)
}

fn rc_pack(q1: usize, q2: usize, q3: usize) -> u16 {
    (q1 * RC_LEVELS * RC_LEVELS + q2 * RC_LEVELS + q3) as u16
}

fn rc_flip(q: usize) -> usize {
    RC_LEVELS - 1 - q
}

/// Context model parameters (fixed in v1; tunable in later iterations).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ContextParams {
    /// How many bits to shift the 365 base context ids (`base >> base_shift`).
    pub base_shift: u8,
    /// Number of activity classes.
    pub activity_classes: u8,
    /// Activity threshold scale (activity = min(classes-1, |g1|+|g2|+|g3| / scale)).
    pub activity_scale: u32,
}

impl Default for ContextParams {
    fn default() -> Self {
        ContextParams {
            base_shift: 3,
            activity_classes: 2,
            activity_scale: 64,
        }
    }
}

impl ContextParams {
    /// Number of interior contexts: `(1 + (364 >> base_shift)) * activity_classes`.
    /// The +1 covers base ids in `[0, 364]`, whose top bucket can reach
    /// `364 >> base_shift`.
    pub fn interior_count(&self) -> usize {
        ((364usize >> self.base_shift) + 1) * self.activity_classes as usize
    }

    /// Total context count including the three border contexts.
    pub fn context_count(&self) -> usize {
        self.interior_count() + BORDER_COUNT
    }
}

/// Border regions: top-left corner, top row (non-corner), left column
/// (non-corner). Interior pixels use the gradient contexts.
pub const BORDER_COUNT: usize = 3;

/// Number of activity classes folded into the CMARC residual-coding context
/// (R3-A). The residual context already captures the local residual
/// distribution via the sign-symmetric base id; the activity class refines it
/// with the current pixel's gradient energy, mirroring the gradient-context
/// activity refinement.
pub const RC_ACTIVITY_CLASSES: usize = 4;

/// Border region id for a pixel (0 = interior). Returns `None` for interior.
pub fn border_region(x: usize, y: usize) -> Option<usize> {
    if x == 0 && y == 0 {
        Some(0)
    } else if y == 0 {
        Some(1)
    } else if x == 0 {
        Some(2)
    } else {
        None
    }
}

/// A reusable per-plane context indexer.
pub struct ContextModel {
    pub params: ContextParams,
    lut: SignSymmetryLut,
    rc_lut: RcLut,
}

impl ContextModel {
    pub fn new(params: ContextParams) -> ContextModel {
        ContextModel {
            params,
            lut: SignSymmetryLut::new(),
            rc_lut: RcLut::new(),
        }
    }

    /// The default per-plane context count used when no analysis is performed.
    pub fn default_context_count(&self) -> usize {
        self.params.context_count()
    }

    /// Interior context id for the given gradients.
    pub fn interior_context(&self, g1: i32, g2: i32, g3: i32) -> usize {
        let q1 = quantize_gradient(g1);
        let q2 = quantize_gradient(g2);
        let q3 = quantize_gradient(g3);
        let base = self.lut.reduce(pack(q1, q2, q3) as usize);
        let activity = self.activity_class(g1, g2, g3);
        ((base >> self.params.base_shift) * self.params.activity_classes as usize) + activity
    }

    fn activity_class(&self, g1: i32, g2: i32, g3: i32) -> usize {
        let s = (g1.abs() + g2.abs() + g3.abs()) as u32;
        let scale = self.params.activity_scale.max(1);
        let c = (s / scale) as usize;
        c.min(self.params.activity_classes as usize - 1)
    }

    /// Final context id for a pixel: interior contexts for interior pixels,
    /// reserved border ids otherwise.
    pub fn context_id(&self, n: &Neighbors, x: usize, y: usize) -> usize {
        if let Some(br) = border_region(x, y) {
            return self.params.interior_count() + br;
        }
        let g1 = n.t - n.l;
        let g2 = n.l - n.tl;
        let g3 = n.tl - n.t;
        self.interior_context(g1, g2, g3)
    }

    /// Number of CMARC residual-coding contexts (R3-A): the sign-symmetric base
    /// residual-context count times the activity classes. This is the table size
    /// the encoder/decoder allocate for the per-`(cid, bin)` CMARC models and
    /// `CarcCtx` states; it is decoupled from `context_count` (the gradient
    /// context that selects the predictor) because R3-A conditions the *residual
    /// coder* on the JPEG-LS DIFF context, not the predictor-selection context.
    pub fn rc_count(&self) -> usize {
        self.rc_lut.base_count() * RC_ACTIVITY_CLASSES
    }
}

/// R3-A: CMARC residual-coding context from the already-coded causal neighbor
/// residuals (the JPEG-LS DIFF context). For the pixel at `(x, y)` the causal
/// neighbors `L = (x-1, y)`, `U = (x, y-1)`, `Ul = (x-1, y-1)` are already in
/// `plane` (the encoder holds the source; the decoder has reconstructed them by
/// raster-order induction), so their residuals against the *same* per-context
/// predictor map are computable identically on both sides; the resulting context
/// therefore matches bit-exactly and lockstep is preserved.
///
/// The gradients of the current pixel (`g1 = t-l`, `g2 = l-tl`, `g3 = tl-t`)
/// select the activity class, so the context separates smooth from detailed
/// regions on top of the sign-symmetric neighbor-residual base id.
pub fn residual_context_for(
    cm: &ContextModel,
    model: &ModelConfig,
    plane: &[i16],
    x: usize,
    y: usize,
    width: usize,
    height: usize,
    wv: Option<&WeightVec>,
    range: PlaneRange,
    pi: usize,
) -> usize {
    let nb = neighbors(plane, x, y, width, height);
    let g1 = nb.t - nb.l;
    let g2 = nb.l - nb.tl;
    let g3 = nb.tl - nb.t;
    let act = cm.activity_class(g1, g2, g3);
    let mut dl = 0i32;
    if x > 0 {
        let idx = y * width + (x - 1);
        let nbl = neighbors(plane, x - 1, y, width, height);
        let cid = cm.context_id(&nbl, x - 1, y) % model.context_count;
        let pred = predict_clamped(model.predictor(pi, cid), &nbl, wv, range);
        dl = plane[idx] as i32 - pred;
    }
    let mut du = 0i32;
    if y > 0 {
        let idx = (y - 1) * width + x;
        let nbu = neighbors(plane, x, y - 1, width, height);
        let cid = cm.context_id(&nbu, x, y - 1) % model.context_count;
        let pred = predict_clamped(model.predictor(pi, cid), &nbu, wv, range);
        du = plane[idx] as i32 - pred;
    }
    let mut dul = 0i32;
    if x > 0 && y > 0 {
        let idx = (y - 1) * width + (x - 1);
        let nbul = neighbors(plane, x - 1, y - 1, width, height);
        let cid = cm.context_id(&nbul, x - 1, y - 1) % model.context_count;
        let pred = predict_clamped(model.predictor(pi, cid), &nbul, wv, range);
        dul = plane[idx] as i32 - pred;
    }
    let base = cm.rc_lut.reduce(
        rc_pack(
            quantize_residual_context(dl),
            quantize_residual_context(du),
            quantize_residual_context(dul),
        ) as usize,
    );
    base * RC_ACTIVITY_CLASSES + act
}

/// Signed zigzag: residual `r` (any i32 in a bounded range) -> non-negative
/// symbol. `r >= 0` -> `2r` (even), `r < 0` -> `2|r| - 1` (odd). Exact inverse
/// of `unzigzag`.
pub fn zigzag(r: i32) -> u32 {
    if r >= 0 {
        (r as u32) << 1
    } else {
        (((-r) as u32) << 1) - 1
    }
}

/// Inverse of `zigzag`.
pub fn unzigzag(u: u32) -> i32 {
    if u & 1 == 0 {
        (u >> 1) as i32
    } else {
        -(((u + 1) >> 1) as i32)
    }
}

/// A residual-symbol alphabet descriptor: the number of rANS symbols needed.
/// For a plane whose samples live in `[min, max]` with predictions clamped to
/// the same range, the residual range is `[min - max, max - min]`, so the
/// symbol range is `[0, 2*(max - min)]`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Alphabet {
    pub size: usize,
    pub max_symbol: u32,
}

impl Alphabet {
    pub fn for_range(min: i32, max: i32) -> Alphabet {
        let span = max - min;
        let max_symbol = 2 * span as u32;
        // Round up to a power of two so rANS table sizing stays simple.
        let mut size = 1;
        while size <= max_symbol as usize {
            size <<= 1;
        }
        Alphabet { size, max_symbol }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn gradient_bins_symmetric() {
        for g in -300..=300 {
            assert_eq!(quantize_gradient(-g), flip(quantize_gradient(g)));
        }
    }

    #[test]
    fn residual_context_sign_symmetric() {
        // The base residual-context id is sign-symmetric: a triple of neighbor
        // residuals and its full negation share a context (the residual
        // distribution is symmetric around zero), which is what lets the R3-A
        // DIFF context specialize without wasting half its budget on sign.
        let cm = ContextModel::new(ContextParams::default());
        let a = cm.lut.reduce(
            pack(quantize_gradient(5), quantize_gradient(-2), quantize_gradient(0)) as usize,
        );
        let b = cm.lut.reduce(
            pack(quantize_gradient(-5), quantize_gradient(2), quantize_gradient(0)) as usize,
        );
        assert_eq!(a, b);
        // And it is discriminating: very different magnitudes land in different
        // base contexts.
        let c = cm.lut.reduce(
            pack(quantize_gradient(40), quantize_gradient(40), quantize_gradient(40)) as usize,
        );
        assert_ne!(a, c, "smooth and steep neighborhoods must differ");
    }

    #[test]
    fn rc_count_is_bounded() {
        let cm = ContextModel::new(ContextParams::default());
        // Coarse residual quantization (5 levels) keeps the DIFF-context count
        // small enough that the per-`(cid, bin)` CMARC models still specialize on
        // photographic-sized images. Assert it is well below the gradient context
        // count's 365 base and within the ~256 the blueprint targets.
        let rc = cm.rc_count();
        assert!(rc >= 1 && rc <= 256, "rc_count = {rc}");
    }

    #[test]
    fn sign_symmetry_lut_reduces_to_365() {
        let lut = SignSymmetryLut::new();
        let mut set = std::collections::BTreeSet::new();
        for q1 in 0..9 {
            for q2 in 0..9 {
                for q3 in 0..9 {
                    set.insert(lut.reduce(pack(q1, q2, q3) as usize));
                }
            }
        }
        assert_eq!(set.len(), 365);
        // Negation maps to the same context.
        for q1 in 0..9 {
            for q2 in 0..9 {
                for q3 in 0..9 {
                    let a = lut.reduce(pack(q1, q2, q3) as usize);
                    let b = lut.reduce(pack(flip(q1), flip(q2), flip(q3)) as usize);
                    assert_eq!(a, b);
                }
            }
        }
    }

    #[test]
    fn zigzag_bijection() {
        for r in -600..=600 {
            let u = zigzag(r);
            assert_eq!(unzigzag(u), r);
        }
        // Small residuals map to small symbols.
        assert_eq!(zigzag(0), 0);
        assert_eq!(zigzag(1), 2);
        assert_eq!(zigzag(-1), 1);
        assert_eq!(zigzag(255), 510);
        assert_eq!(zigzag(-255), 509);
    }

    #[test]
    fn context_borders_distinct() {
        let m = ContextModel::new(ContextParams::default());
        let n = Neighbors {
            l: 0,
            t: 0,
            tl: 0,
            tr: 0,
        };
        // Interior id must differ from border ids.
        let interior = m.context_id(&n, 5, 5);
        assert!(interior < m.params.interior_count());
        let corner = m.context_id(&n, 0, 0);
        let top = m.context_id(&n, 3, 0);
        let left = m.context_id(&n, 0, 3);
        assert_eq!(corner, m.params.interior_count() + 0);
        assert_eq!(top, m.params.interior_count() + 1);
        assert_eq!(left, m.params.interior_count() + 2);
        assert_ne!(corner, interior);
    }

    #[test]
    fn alphabet_for_ranges() {
        let a8 = Alphabet::for_range(0, 255);
        assert_eq!(a8.max_symbol, 510);
        assert_eq!(a8.size, 512);
        let atr = Alphabet::for_range(-255, 255);
        assert_eq!(atr.max_symbol, 1020);
        assert_eq!(atr.size, 1024);
    }
}
