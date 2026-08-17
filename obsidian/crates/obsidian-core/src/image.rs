//! Image model and PPM I/O.
//!
//! Obsidian operates on integer channel planes. The [`Image`] type holds one
//! [`Plane`] per channel (grayscale: 1, RGB: 3, RGBA: 4). A plane is a flat
//! raster (`data[y * w + x]`).
//!
//! v1 reads and writes PPM: P6 for RGB, P5 for grayscale. Only 8-bit is
//! supported. The writer emits canonical, comment-free PPM so that a fidelity
//! gate can `cmp` the decoded file against the source byte-for-byte.

use crate::error::{CodecError, CodecResult};

/// A single 8-bit channel plane in raster order (`data[y * w + x]`).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Plane {
    pub w: u32,
    pub h: u32,
    pub data: Vec<u8>,
}

impl Plane {
    pub fn new(w: u32, h: u32, data: Vec<u8>) -> CodecResult<Self> {
        let len = (w as usize)
            .checked_mul(h as usize)
            .ok_or(CodecError::InvalidDimensions(w, h))?;
        if data.len() != len {
            return Err(CodecError::InvalidPixelData);
        }
        Ok(Plane { w, h, data })
    }

    /// Clamped pixel accessor for full images (used by tests and tools where
    /// the whole plane is available).
    #[inline]
    pub fn pixel(&self, x: i64, y: i64) -> u8 {
        let w = self.w as i64;
        let h = self.h as i64;
        let cx = x.clamp(0, w - 1);
        let cy = y.clamp(0, h - 1);
        self.data[(cy * w + cx) as usize]
    }

    /// Causal neighbor accessor for coding.
    ///
    /// `(x, y)` is the pixel being coded; `(nx, ny)` is the neighbor
    /// coordinate. A neighbor is readable only if it lies in the already
    /// coded causal region (above, or on the same row strictly to the left).
    /// Anything else returns 0. This makes the border rule symmetric between
    /// encoder and decoder (the encoder reads exactly what the decoder will
    /// have decoded), resolving the "top row mirrors itself" ambiguity in the
    /// spec in favor of a deterministic, non-circular rule.
    #[inline]
    pub fn causal_pixel(&self, x: i64, y: i64, nx: i64, ny: i64) -> u8 {
        let w = self.w as i64;
        if nx < 0 || ny < 0 || nx >= w || ny > y || (ny == y && nx >= x) {
            return 0;
        }
        self.data[(ny * w + nx) as usize]
    }

    #[inline]
    pub fn len(&self) -> usize {
        self.data.len()
    }

    #[inline]
    pub fn is_empty(&self) -> bool {
        self.data.is_empty()
    }
}

/// An image: dimensions, channel layout, and one plane per channel.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Image {
    pub width: u32,
    pub height: u32,
    /// 1 (gray), 3 (RGB), or 4 (RGBA).
    pub channels: u8,
    /// Bit depth of each channel (8 in v1).
    pub bit_depth: u8,
    /// One plane per channel, each `width * height` bytes.
    pub planes: Vec<Plane>,
}

impl Image {
    /// Build an image from per-channel planes, validating consistency.
    pub fn from_planes(width: u32, height: u32, channels: u8, bit_depth: u8, planes: Vec<Plane>) -> CodecResult<Self> {
        if !matches!(channels, 1 | 3 | 4) {
            return Err(CodecError::InvalidChannels(channels));
        }
        if bit_depth != 8 {
            return Err(CodecError::UnsupportedBitDepth(bit_depth));
        }
        if width == 0 || height == 0 {
            return Err(CodecError::InvalidDimensions(width, height));
        }
        if planes.len() != channels as usize {
            return Err(CodecError::InvalidChannels(channels));
        }
        for p in &planes {
            if p.w != width || p.h != height {
                return Err(CodecError::InvalidDimensions(width, height));
            }
        }
        Ok(Image { width, height, channels, bit_depth, planes })
    }

    /// Construct a grayscale image from a single plane.
    pub fn gray(width: u32, height: u32, data: Vec<u8>) -> CodecResult<Self> {
        let p = Plane::new(width, height, data)?;
        Self::from_planes(width, height, 1, 8, vec![p])
    }

    /// Construct an RGB image from three equal-length channel planes.
    pub fn rgb(width: u32, height: u32, r: Vec<u8>, g: Vec<u8>, b: Vec<u8>) -> CodecResult<Self> {
        let planes = vec![
            Plane::new(width, height, r)?,
            Plane::new(width, height, g)?,
            Plane::new(width, height, b)?,
        ];
        Self::from_planes(width, height, 3, 8, planes)
    }

    /// Parse a PPM byte stream (P5 gray or P6 RGB, 8-bit only).
    pub fn from_ppm(bytes: &[u8]) -> CodecResult<Self> {
        let mut pos = 0usize;

        // Magic.
        let m1 = *bytes.get(pos).ok_or(CodecError::Truncated)?;
        pos += 1;
        let m2 = *bytes.get(pos).ok_or(CodecError::Truncated)?;
        pos += 1;
        let channels = match (m1, m2) {
            (b'P', b'5') => 1u8,
            (b'P', b'6') => 3u8,
            _ => return Err(CodecError::MalformedPpm("expected P5 or P6 magic")),
        };
        // Next byte after magic must be whitespace.
        let ws = *bytes.get(pos).ok_or(CodecError::Truncated)?;
        pos += 1;
        if ws != b' ' && ws != b'\n' && ws != b'\t' && ws != b'\r' {
            return Err(CodecError::MalformedPpm("whitespace after magic"));
        }

        let read_token = |pos: &mut usize| -> CodecResult<u32> {
            loop {
                let b = *bytes.get(*pos).ok_or(CodecError::Truncated)?;
                if b == b'#' {
                    while *pos < bytes.len() && bytes[*pos] != b'\n' {
                        *pos += 1;
                    }
                    continue;
                }
                if b == b' ' || b == b'\n' || b == b'\t' || b == b'\r' {
                    *pos += 1;
                    continue;
                }
                break;
            }
            let mut val: u32 = 0;
            let mut any = false;
            while *pos < bytes.len() {
                let b = bytes[*pos];
                if b.is_ascii_digit() {
                    any = true;
                    val = val.saturating_mul(10).saturating_add((b - b'0') as u32);
                    *pos += 1;
                } else {
                    break;
                }
            }
            if !any {
                return Err(CodecError::MalformedPpm("expected numeric token"));
            }
            Ok(val)
        };

        let width = read_token(&mut pos)?;
        let height = read_token(&mut pos)?;
        let maxval = read_token(&mut pos)?;

        if width == 0 || height == 0 {
            return Err(CodecError::InvalidDimensions(width, height));
        }
        if maxval != 255 {
            return Err(CodecError::UnsupportedBitDepth(maxval as u8));
        }
        if width > (1 << 20) || height > (1 << 20) {
            return Err(CodecError::InvalidDimensions(width, height));
        }

        // Skip the single whitespace character before the binary payload.
        while pos < bytes.len()
            && (bytes[pos] == b' ' || bytes[pos] == b'\n' || bytes[pos] == b'\t' || bytes[pos] == b'\r')
        {
            pos += 1;
        }

        let expected = (width as usize)
            .checked_mul(height as usize)
            .and_then(|n| n.checked_mul(channels as usize))
            .ok_or(CodecError::InvalidDimensions(width, height))?;
        if bytes.len() < pos + expected {
            return Err(CodecError::Truncated);
        }

        let n = width as usize * height as usize;
        let mut planes = Vec::with_capacity(channels as usize);
        for c in 0..channels as usize {
            let mut data = Vec::with_capacity(n);
            let mut off = pos + c;
            for _ in 0..n {
                data.push(bytes[off]);
                off += channels as usize;
            }
            planes.push(Plane::new(width, height, data)?);
        }

        Self::from_planes(width, height, channels, 8, planes)
    }

    /// Emit canonical PPM (P5 for gray, P6 for RGB). The output is
    /// deterministic and comment-free so it is directly comparable with
    /// `cmp`.
    pub fn to_ppm(&self) -> Vec<u8> {
        let magic = if self.channels == 1 { "P5" } else { "P6" };
        let header = format!("{magic}\n{} {}\n255\n", self.width, self.height);
        let mut out = Vec::with_capacity(header.len() + self.width as usize * self.height as usize * self.channels as usize);
        out.extend_from_slice(header.as_bytes());
        let w = self.width as usize;
        let h = self.height as usize;
        for y in 0..h {
            for x in 0..w {
                for c in 0..self.channels as usize {
                    out.push(self.planes[c].data[y * w + x]);
                }
            }
        }
        out
    }

    /// Construct an image from interleaved RGBA8 bytes (channels is 3 or 4;
    /// the byte layout is RGB(A) per pixel).
    pub fn from_rgba8(width: u32, height: u32, channels: u8, rgba: &[u8]) -> CodecResult<Self> {
        let w = width as usize;
        let h = height as usize;
        let n = w.checked_mul(h).ok_or(CodecError::InvalidDimensions(width, height))?;
        if rgba.len() != n * 4 {
            return Err(CodecError::InvalidPixelData);
        }
        let mut planes = Vec::with_capacity(channels as usize);
        for c in 0..channels as usize {
            let mut data = Vec::with_capacity(n);
            for i in 0..n {
                data.push(rgba[i * 4 + c]);
            }
            planes.push(Plane::new(width, height, data)?);
        }
        Self::from_planes(width, height, channels, 8, planes)
    }

    /// Clamped accessor for a channel plane.
    #[inline]
    pub fn pixel(&self, c: usize, x: i64, y: i64) -> u8 {
        self.planes[c].pixel(x, y)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ppm_roundtrip_rgb() {
        let w = 7;
        let h = 5;
        let mut r = Vec::new();
        let mut g = Vec::new();
        let mut b = Vec::new();
        let mut s = 0u32;
        for _ in 0..(w * h) {
            r.push((s & 0xFF) as u8);
            g.push(((s >> 3) & 0xFF) as u8);
            b.push(((s >> 7) & 0xFF) as u8);
            s = s.wrapping_mul(1103515245).wrapping_add(12345);
        }
        let img = Image::rgb(w, h, r, g, b).unwrap();
        let ppm = img.to_ppm();
        let img2 = Image::from_ppm(&ppm).unwrap();
        assert_eq!(img, img2);
    }

    #[test]
    fn ppm_roundtrip_gray() {
        let data: Vec<u8> = (0..120u8).collect();
        let img = Image::gray(10, 12, data).unwrap();
        let ppm = img.to_ppm();
        assert!(ppm.starts_with(b"P5\n"));
        let img2 = Image::from_ppm(&ppm).unwrap();
        assert_eq!(img, img2);
    }

    #[test]
    fn ppm_accepts_comments() {
        let mut ppm = Vec::new();
        ppm.extend_from_slice(b"P6\n# a comment\n2 2\n# another\n255\n");
        ppm.extend_from_slice(&[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);
        let img = Image::from_ppm(&ppm).unwrap();
        assert_eq!(img.channels, 3);
        assert_eq!(img.planes[0].data, vec![1, 4, 7, 10]);
        assert_eq!(img.planes[1].data, vec![2, 5, 8, 11]);
        assert_eq!(img.planes[2].data, vec![3, 6, 9, 12]);
    }

    #[test]
    fn ppm_rejects_bad_input() {
        assert_eq!(Image::from_ppm(b"P6\n").unwrap_err(), CodecError::Truncated);
        assert_eq!(Image::from_ppm(b"X7\n2 2\n255\n").unwrap_err(), CodecError::MalformedPpm("expected P5 or P6 magic"));
        assert_eq!(Image::from_ppm(b"P6\n0 2\n255\n").unwrap_err(), CodecError::InvalidDimensions(0, 2));
        assert_eq!(Image::from_ppm(b"P6\n2 2\n16\n").unwrap_err(), CodecError::UnsupportedBitDepth(16));
        // Truncated payload.
        assert_eq!(Image::from_ppm(b"P6\n2 2\n255\n\x01\x02\x03").unwrap_err(), CodecError::Truncated);
    }

    #[test]
    fn clamped_accessor() {
        let p = Plane::new(3, 2, vec![1, 2, 3, 4, 5, 6]).unwrap();
        assert_eq!(p.pixel(1, 0), 2);
        assert_eq!(p.pixel(-1, 0), 1); // clamp left
        assert_eq!(p.pixel(3, 1), 6); // clamp right
        assert_eq!(p.pixel(0, -1), 1); // clamp top
        assert_eq!(p.pixel(2, 5), 6); // clamp bottom
        assert_eq!(p.pixel(-5, -5), 1); // corner
    }
}
