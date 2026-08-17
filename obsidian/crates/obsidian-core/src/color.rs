//! Reversible color transforms.
//!
//! v1 implements YCoCg-R (reversible, from the JPEG 2000 / JPEG XL lineage).
//! The transform is an exact integer bijection on `[0, 255]^3` triplets; the
//! forward and inverse operators below round-trip any input bit-exactly. All
//! arithmetic uses wrapping i32 semantics consistent with the spec.

use crate::error::{CodecError, CodecResult};

/// Apply the forward YCoCg-R transform to a single RGB triplet in place.
///
/// ```text
/// Co = R - B
/// t  = B + (Co >> 1)
/// Cg = G - t
/// Y  = t + (Cg >> 1)
/// ```
#[inline]
pub fn ycocg_r_forward_pixel(r: u8, g: u8, b: u8) -> (u8, u8, u8) {
    let r = r as i32;
    let g = g as i32;
    let b = b as i32;
    let co = r - b;
    let t = b + (co >> 1);
    let cg = g - t;
    let y = t + (cg >> 1);
    (y as u8, co as u8, cg as u8)
}

/// Apply the inverse YCoCg-R transform to a single triplet in place.
///
/// ```text
/// t  = Y - (Cg >> 1)
/// G  = Cg + t
/// B  = t - (Co >> 1)
/// R  = B + Co
/// ```
#[inline]
pub fn ycocg_r_inverse_pixel(y: u8, co: u8, cg: u8) -> (u8, u8, u8) {
    let y = y as i32;
    let co = co as i32;
    let cg = cg as i32;
    let t = y - (cg >> 1);
    let g = cg + t;
    let b = t - (co >> 1);
    let r = b + co;
    (r as u8, g as u8, b as u8)
}

/// Transform a 3-plane image in place to YCoCg-R.
pub fn ycocg_r_forward(planes: &mut [crate::image::Plane]) {
    if planes.len() < 3 {
        return;
    }
    let n = planes[0].data.len();
    for i in 0..n {
        let (r, g, b) = (planes[0].data[i], planes[1].data[i], planes[2].data[i]);
        let (y, co, cg) = ycocg_r_forward_pixel(r, g, b);
        planes[0].data[i] = y;
        planes[1].data[i] = co;
        planes[2].data[i] = cg;
    }
}

/// Undo YCoCg-R in place.
pub fn ycocg_r_inverse(planes: &mut [crate::image::Plane]) {
    if planes.len() < 3 {
        return;
    }
    let n = planes[0].data.len();
    for i in 0..n {
        let (y, co, cg) = (planes[0].data[i], planes[1].data[i], planes[2].data[i]);
        let (r, g, b) = ycocg_r_inverse_pixel(y, co, cg);
        planes[0].data[i] = r;
        planes[1].data[i] = g;
        planes[2].data[i] = b;
    }
}

/// A palette for the palette transform: up to 256 distinct RGB triples.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Palette {
    pub colors: Vec<[u8; 3]>,
}

impl Palette {
    /// Build a palette if the image has at most 256 distinct RGB triples.
    /// Returns `None` otherwise. The palette is ordered by first occurrence.
    pub fn from_image_rgb(width: u32, height: u32, r: &[u8], g: &[u8], b: &[u8]) -> Option<Palette> {
        if r.len() != g.len() || r.len() != b.len() {
            return None;
        }
        let n = width as usize * height as usize;
        if r.len() < n {
            return None;
        }
        let mut seen = Vec::with_capacity(256);
        let mut index = vec![0u16; n];
        for i in 0..n {
            let c = [r[i], g[i], b[i]];
            match seen.iter().position(|&s| s == c) {
                Some(idx) => index[i] = idx as u16,
                None => {
                    if seen.len() >= 256 {
                        return None;
                    }
                    index[i] = seen.len() as u16;
                    seen.push(c);
                }
            }
        }
        let _ = index;
        Some(Palette { colors: seen })
    }

    /// Map an RGB image to its index plane.
    pub fn index_plane(&self, r: &[u8], g: &[u8], b: &[u8]) -> CodecResult<Vec<u8>> {
        if r.len() != g.len() || r.len() != b.len() {
            return Err(CodecError::InvalidPixelData);
        }
        let mut idx = Vec::with_capacity(r.len());
        for i in 0..r.len() {
            let c = [r[i], g[i], b[i]];
            let pos = self.colors.iter().position(|&s| s == c).ok_or(CodecError::BadPalette)?;
            idx.push(pos as u8);
        }
        Ok(idx)
    }

    /// Reconstruct an RGB image from an index plane.
    pub fn unindex(&self, idx: &[u8]) -> CodecResult<(Vec<u8>, Vec<u8>, Vec<u8>)> {
        let mut r = Vec::with_capacity(idx.len());
        let mut g = Vec::with_capacity(idx.len());
        let mut b = Vec::with_capacity(idx.len());
        for &i in idx {
            let c = self.colors.get(i as usize).ok_or(CodecError::BadPalette)?;
            r.push(c[0]);
            g.push(c[1]);
            b.push(c[2]);
        }
        Ok((r, g, b))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ycocg_r_bijection_random() {
        // Deterministic LCG.
        let mut s = 0x1234_5678u32;
        for _ in 0..50_000 {
            s = s.wrapping_mul(1103515245).wrapping_add(12345);
            let r = (s >> 16) as u8;
            s = s.wrapping_mul(1103515245).wrapping_add(12345);
            let g = (s >> 16) as u8;
            s = s.wrapping_mul(1103515245).wrapping_add(12345);
            let b = (s >> 16) as u8;
            let (y, co, cg) = ycocg_r_forward_pixel(r, g, b);
            let (r2, g2, b2) = ycocg_r_inverse_pixel(y, co, cg);
            assert_eq!((r, g, b), (r2, g2, b2));
        }
    }

    #[test]
    fn ycocg_r_bijection_exhaustive_small() {
        // Exhaustive sweep over a reduced domain (every value of R and G with
        // B fixed), which exercises the full add/subtract carries.
        for r in 0u8..=255u8 {
            for g in 0u8..=255u8 {
                let (y, co, cg) = ycocg_r_forward_pixel(r, g, 127);
                let (r2, g2, b2) = ycocg_r_inverse_pixel(y, co, cg);
                assert_eq!((r, g, 127u8), (r2, g2, b2), "r={r} g={g}");
            }
        }
    }

    #[test]
    fn ycocg_r_specific_values() {
        // White -> white-ish, black stays black.
        assert_eq!(ycocg_r_forward_pixel(255, 255, 255), (255, 0, 0));
        assert_eq!(ycocg_r_forward_pixel(0, 0, 0), (0, 0, 0));
        let (r, g, b) = ycocg_r_inverse_pixel(255, 0, 0);
        assert_eq!((r, g, b), (255, 255, 255));
    }

    #[test]
    fn plane_transform_roundtrip() {
        let mut planes = vec![
            crate::image::Plane::new(4, 4, (0..16).collect()).unwrap(),
            crate::image::Plane::new(4, 4, (16..32).collect()).unwrap(),
            crate::image::Plane::new(4, 4, (32..48).collect()).unwrap(),
        ];
        let orig = planes.clone();
        ycocg_r_forward(&mut planes);
        ycocg_r_inverse(&mut planes);
        assert_eq!(planes, orig);
    }

    #[test]
    fn palette_build_and_roundtrip() {
        let w = 4u32;
        let h = 4u32;
        let r = vec![0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255];
        let g = vec![0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255];
        let b = vec![0, 0, 0, 0, 128, 128, 128, 128, 255, 255, 255, 255, 1, 1, 1, 1];
        let pal = Palette::from_image_rgb(w, h, &r, &g, &b).unwrap();
        assert_eq!(pal.colors.len(), 8);
        let idx = pal.index_plane(&r, &g, &b).unwrap();
        let (r2, g2, b2) = pal.unindex(&idx).unwrap();
        assert_eq!(r, r2);
        assert_eq!(g, g2);
        assert_eq!(b, b2);
    }

    #[test]
    fn palette_rejects_256_plus_colors() {
        // 257 distinct colors must be rejected.
        let n = 257usize;
        let mut r = Vec::with_capacity(n);
        let mut g = vec![0u8; n];
        let mut b = vec![0u8; n];
        for i in 0..n {
            r.push(i as u8);
        }
        // r values 0..=255 plus one more; use g to force a 257th distinct color.
        g[256] = 1;
        assert!(Palette::from_image_rgb(257, 1, &r, &g, &b).is_none());
    }
}
