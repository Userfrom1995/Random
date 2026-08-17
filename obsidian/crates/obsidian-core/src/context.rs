//! Context model and residual symbol mapping.
//!
//! For each pixel we compute the three JPEG-LS causal gradients, quantize
//! each to one of 9 bins, fold the triple's sign (a gradient triple and its
//! negation map to the same context), and add an activity class derived from
//! the gradient magnitudes. Border regions (origin, top row, left column)
//! get dedicated context ranges so degenerate neighborhoods never pollute
//! interior statistics.
//!
//! Context id layout per plane:
//!
//! ```text
//! ctx = (region * BASE_CTX + base_id) * classes + activity
//! ```
//!
//! where `region in 0..4`, `base_id in 0..365`, `activity in 0..classes`,
//! and `classes in {1, 2, 4}` depending on the activity mode.

use std::sync::OnceLock;

use crate::container::consts::{BASE_CTX, REGIONS};

/// The 9-bin gradient quantizer (JPEG-LS thresholds T1=3, T2=7, T3=21).
#[inline]
pub fn quantize(g: i32) -> i8 {
    if g <= -21 {
        -4
    } else if g <= -7 {
        -3
    } else if g <= -3 {
        -2
    } else if g <= -1 {
        -1
    } else if g == 0 {
        0
    } else if g < 3 {
        1
    } else if g < 7 {
        2
    } else if g < 21 {
        3
    } else {
        4
    }
}

/// Map a quantized triple to its sign-canonicalized gradient class
/// (`0..365`). The triple and its negation map to the same id.
#[inline]
pub fn base_id(q1: i8, q2: i8, q3: i8) -> u16 {
    let table = ctx_table();
    table[((q1 + 4) as usize) * 81 + ((q2 + 4) as usize) * 9 + ((q3 + 4) as usize)]
}

/// Reverse lookup: gradient class id -> its canonical quantized triple.
pub fn gradient_of_base(id: u16) -> (i8, i8, i8) {
    GRAD_TABLE.get_or_init(|| build_grad_table())[id as usize]
}

/// The context table mapping all `9^3 = 729` quantized triples to `365`
/// sign-canonicalized ids.
fn ctx_table() -> &'static [u16; 729] {
    static TABLE: OnceLock<[u16; 729]> = OnceLock::new();
    TABLE.get_or_init(|| {
        let mut table = [0u16; 729];
        // First-seen order over canonical triples gives a deterministic,
        // bijective id assignment.
        let mut canonical_ids = [0u16; 729];
        let mut assigned = [false; 729];
        let mut next = 0u16;
        for q1 in -4i8..=4 {
            for q2 in -4i8..=4 {
                for q3 in -4i8..=4 {
                    let (c1, c2, c3) = canonicalize(q1, q2, q3);
                    let idx = ((c1 + 4) as usize) * 81 + ((c2 + 4) as usize) * 9 + ((c3 + 4) as usize);
                    if !assigned[idx] {
                        canonical_ids[idx] = next;
                        assigned[idx] = true;
                        next += 1;
                    }
                    let orig_idx = ((q1 + 4) as usize) * 81 + ((q2 + 4) as usize) * 9 + ((q3 + 4) as usize);
                    table[orig_idx] = canonical_ids[idx];
                }
            }
        }
        debug_assert_eq!(next, 365);
        table
    })
}

/// Reduce a quantized triple to its canonical sign form: the first non-zero
/// gradient is positive (all-zero stays all-zero).
#[inline]
fn canonicalize(q1: i8, q2: i8, q3: i8) -> (i8, i8, i8) {
    let first_nonzero_negative = (q1 < 0) || (q1 == 0 && q2 < 0) || (q1 == 0 && q2 == 0 && q3 < 0);
    if first_nonzero_negative {
        (-q1, -q2, -q3)
    } else {
        (q1, q2, q3)
    }
}

fn build_grad_table() -> [(i8, i8, i8); 365] {
    let mut table = [(0i8, 0i8, 0i8); 365];
    let mut assigned = [false; 729];
    let mut next = 0usize;
    for q1 in -4i8..=4 {
        for q2 in -4i8..=4 {
            for q3 in -4i8..=4 {
                let (c1, c2, c3) = canonicalize(q1, q2, q3);
                let idx = ((c1 + 4) as usize) * 81 + ((c2 + 4) as usize) * 9 + ((c3 + 4) as usize);
                if !assigned[idx] {
                    table[next] = (c1, c2, c3);
                    assigned[idx] = true;
                    next += 1;
                }
            }
        }
    }
    debug_assert_eq!(next, 365);
    table
}

/// The reverse lookup table for gradient classes.
static GRAD_TABLE: OnceLock<[(i8, i8, i8); 365]> = OnceLock::new();

/// Border region of a pixel.
#[inline]
pub fn region_of(x: i64, y: i64) -> usize {
    if x == 0 && y == 0 {
        0
    } else if y == 0 {
        1
    } else if x == 0 {
        2
    } else {
        3
    }
}

/// Activity class from gradient magnitudes, for the given class count.
#[inline]
pub fn activity_of(g1: i32, g2: i32, g3: i32, classes: usize) -> usize {
    if classes <= 1 {
        return 0;
    }
    let mag = (g1.abs() + g2.abs() + g3.abs()) as usize;
    if classes == 2 {
        if mag < 30 {
            0
        } else {
            1
        }
    } else {
        if mag < 15 {
            0
        } else if mag < 60 {
            1
        } else if mag < 150 {
            2
        } else {
            3
        }
    }
}

/// Compute the full context id for a pixel in a plane.
#[inline]
pub fn context_of(plane: &crate::image::Plane, x: i64, y: i64, classes: usize) -> usize {
    let t = plane.causal_pixel(x, y, x, y - 1) as i32;
    let l = plane.causal_pixel(x, y, x - 1, y) as i32;
    let tl = plane.causal_pixel(x, y, x - 1, y - 1) as i32;
    let g1 = t - l;
    let g2 = l - tl;
    let g3 = tl - t;
    context_from_gradients(g1, g2, g3, x, y, classes)
}

/// Build a context id directly from gradient values and coordinates.
/// Shared by the encoder (full plane) and decoder (partially decoded plane).
#[inline]
pub fn context_from_gradients(g1: i32, g2: i32, g3: i32, x: i64, y: i64, classes: usize) -> usize {
    let q1 = quantize(g1);
    let q2 = quantize(g2);
    let q3 = quantize(g3);
    let base = base_id(q1, q2, q3) as usize;
    let region = region_of(x, y);
    let activity = activity_of(g1, g2, g3, classes);
    (region * BASE_CTX + base) * classes + activity
}

/// The maximum context id for a given class count.
pub fn max_context(classes: usize) -> usize {
    REGIONS * BASE_CTX * classes
}

// ---------------------------------------------------------------------------
// Residual symbol mapping (zigzag).
// ---------------------------------------------------------------------------

/// Map a residual `r in 0..=255` to a symbol `u in 0..=511`, preserving the
/// peaked-at-zero distribution:
///
/// ```text
/// u = 2*r          if r <= 128
/// u = 2*(256-r)-1  otherwise
/// ```
#[inline]
pub fn zigzag(r: u8) -> u16 {
    let r = r as u32;
    if r <= 128 {
        (2 * r) as u16
    } else {
        (2 * (256 - r) - 1) as u16
    }
}

/// Inverse of [`zigzag`].
#[inline]
pub fn unzigzag(u: u16) -> u8 {
    let u = u as u32;
    if u & 1 == 0 {
        (u >> 1) as u8
    } else {
        (256 - ((u + 1) >> 1)) as u8
    }
}

/// Number of residual symbols (alphabet size).
pub const ALPHABET: usize = 512;

#[cfg(test)]
mod tests {
    use super::*;
    use crate::image::Plane;

    #[test]
    fn zigzag_bijection_all() {
        let mut seen = vec![false; 512];
        for r in 0u16..=255 {
            let u = zigzag(r as u8);
            assert!(u < 512);
            assert!(!seen[u as usize]);
            seen[u as usize] = true;
            assert_eq!(unzigzag(u), r as u8);
        }
        // All 512 symbols used.
        assert!(seen.iter().all(|&s| s));
    }

    #[test]
    fn zigzag_peaks_at_zero() {
        assert_eq!(zigzag(0), 0);
        assert_eq!(zigzag(1), 2);
        assert_eq!(zigzag(128), 256);
        assert_eq!(zigzag(255), 1);
        assert_eq!(zigzag(129), 253);
    }

    #[test]
    fn context_table_is_365() {
        let table = ctx_table();
        let mut max = 0;
        for &v in table.iter() {
            if v > max {
                max = v;
            }
        }
        assert_eq!(max, 364);
        assert_eq!(table[0], 0); // all-zero triple
        assert_eq!(table[((0 + 4) * 81 + (0 + 4) * 9 + (0 + 4)) as usize], 0);
    }

    #[test]
    fn sign_symmetry() {
        // (1,2,3) and (-1,-2,-3) must map to the same id.
        assert_eq!(base_id(1, 2, 3), base_id(-1, -2, -3));
        // (0,1,0) and (0,-1,0) too.
        assert_eq!(base_id(0, 1, 0), base_id(0, -1, 0));
        // And the reverse mapping is consistent.
        let id = base_id(2, -3, 1);
        let (c1, c2, c3) = gradient_of_base(id);
        assert_eq!(base_id(c1, c2, c3), id);
    }

    #[test]
    fn gradients_and_context() {
        // Flat region: all-zero gradients.
        let p = Plane::new(3, 3, vec![5, 5, 5, 5, 5, 5, 5, 5, 5]).unwrap();
        // Interior pixel (1,1): gradients all 0 -> base 0, region 3.
        assert_eq!(context_of(&p, 1, 1, 1), 3 * BASE_CTX);
        // Top row pixel: region 1.
        assert_eq!(context_of(&p, 1, 0, 1), 1 * BASE_CTX);
        // Left column: region 2.
        assert_eq!(context_of(&p, 0, 1, 1), 2 * BASE_CTX);
        // Origin: region 0.
        assert_eq!(context_of(&p, 0, 0, 1), 0);
    }

    #[test]
    fn activity_classes_bound() {
        let classes = 4;
        let n = classes;
        let mut seen = vec![false; n];
        for a in 0..n {
            seen[a] = true;
        }
        assert!(seen.iter().all(|&s| s));
        // Activity thresholds produce values in range.
        assert_eq!(activity_of(0, 0, 0, 4), 0);
        assert_eq!(activity_of(100, 100, 100, 4), 3);
        assert_eq!(activity_of(0, 0, 0, 2), 0);
        assert_eq!(activity_of(100, 100, 100, 2), 1);
        assert_eq!(activity_of(0, 0, 0, 1), 0);
    }
}
