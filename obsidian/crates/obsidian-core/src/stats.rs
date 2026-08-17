//! Encoding statistics for reporting.

/// The color transform applied.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransformChoice {
    None,
    YCoCgR,
    Palette,
}

/// Statistics produced by the encoder (not computed by the decoder).
#[derive(Debug, Clone, PartialEq)]
pub struct EncodeStats {
    /// Total encoded bytes.
    pub bytes: usize,
    /// Bits per pixel of the source image.
    pub bpp: f64,
    /// Effort level used.
    pub effort: u8,
    /// Transform applied.
    pub transform: TransformChoice,
    /// Encoded byte count per plane.
    pub per_plane_bytes: Vec<usize>,
    /// Predictor histogram: counts of per-pixel predictor decisions, by base
    /// predictor id 0..=7 (WAvg vector choices are folded into id 7).
    pub predictor_histogram: [u32; 8],
    /// Maximum number of distinct contexts used across planes.
    pub contexts_used: usize,
    /// Activity classes used.
    pub activity_classes: usize,
}

impl EncodeStats {
    pub fn predictor_total(&self) -> u32 {
        self.predictor_histogram.iter().sum()
    }
}
