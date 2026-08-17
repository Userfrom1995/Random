//! Error and result types for the Obsidian codec.

use std::fmt;

/// Errors produced by the Obsidian codec.
///
/// The encoder and decoder never panic on malformed input; every failure
/// path returns a [`CodecError`]. The decoder validates every length it
/// reads from the stream against the remaining byte budget before any
/// allocation, so a hostile file can only ever produce an error, never a
/// crash or an unbounded allocation.
#[derive(Debug)]
pub enum CodecError {
    /// The byte stream is shorter than the operation requires.
    Truncated,
    /// A header field has an invalid value (bad magic, bad version, etc.).
    BadMagic,
    BadVersion,
    /// The bit depth is not supported (only 8-bit is supported in v1).
    UnsupportedBitDepth(u8),
    /// The image dimensions are invalid (zero or absurd).
    InvalidDimensions(u32, u32),
    /// The channel count is invalid.
    InvalidChannels(u8),
    /// The image pixel payload length does not match the header dimensions.
    InvalidPixelData,
    /// A PPM field (magic, dimensions, maxval) is malformed.
    MalformedPpm(&'static str),
    /// The effort level is out of range.
    InvalidEffort(u8),
    /// The rANS stream is malformed (renorm ran out of bytes, bad table).
    CorruptRans,
    /// The header CRC did not match the reconstructed planes.
    CrcMismatch,
    /// The decode produced an inconsistent structure.
    CorruptContainer,
    /// An I/O error occurred (wrapping the underlying error).
    Io(std::io::Error),
    /// The palette is malformed.
    BadPalette,
}

impl PartialEq for CodecError {
    fn eq(&self, other: &Self) -> bool {
        // Compare by variant and payload, not by the wrapped I/O error.
        std::mem::discriminant(self) == std::mem::discriminant(other)
    }
}

impl Eq for CodecError {}

impl Clone for CodecError {
    fn clone(&self) -> Self {
        match self {
            CodecError::UnsupportedBitDepth(b) => CodecError::UnsupportedBitDepth(*b),
            CodecError::InvalidDimensions(w, h) => CodecError::InvalidDimensions(*w, *h),
            CodecError::InvalidChannels(c) => CodecError::InvalidChannels(*c),
            CodecError::MalformedPpm(m) => CodecError::MalformedPpm(*m),
            CodecError::InvalidEffort(e) => CodecError::InvalidEffort(*e),
            CodecError::Io(_) => CodecError::CorruptRans,
            other => clone_unit(other),
        }
    }
}

fn clone_unit(e: &CodecError) -> CodecError {
    match e {
        CodecError::Truncated => CodecError::Truncated,
        CodecError::BadMagic => CodecError::BadMagic,
        CodecError::BadVersion => CodecError::BadVersion,
        CodecError::InvalidPixelData => CodecError::InvalidPixelData,
        CodecError::CorruptRans => CodecError::CorruptRans,
        CodecError::CrcMismatch => CodecError::CrcMismatch,
        CodecError::CorruptContainer => CodecError::CorruptContainer,
        CodecError::BadPalette => CodecError::BadPalette,
        other => panic!("unhandled clone case: {other}"),
    }
}

impl fmt::Display for CodecError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            CodecError::Truncated => write!(f, "truncated input"),
            CodecError::BadMagic => write!(f, "bad magic bytes"),
            CodecError::BadVersion => write!(f, "unsupported container version"),
            CodecError::UnsupportedBitDepth(b) => write!(f, "unsupported bit depth {b} (v1 supports 8)"),
            CodecError::InvalidDimensions(w, h) => write!(f, "invalid dimensions {w}x{h}"),
            CodecError::InvalidChannels(c) => write!(f, "invalid channel count {c}"),
            CodecError::InvalidPixelData => write!(f, "pixel payload length does not match header"),
            CodecError::MalformedPpm(what) => write!(f, "malformed PPM: {what}"),
            CodecError::InvalidEffort(e) => write!(f, "invalid effort level {e}"),
            CodecError::CorruptRans => write!(f, "corrupt rANS stream"),
            CodecError::CrcMismatch => write!(f, "CRC mismatch: decoded planes do not match header"),
            CodecError::CorruptContainer => write!(f, "corrupt container structure"),
            CodecError::Io(e) => write!(f, "I/O error: {e}"),
            CodecError::BadPalette => write!(f, "malformed palette"),
        }
    }
}

impl std::error::Error for CodecError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            CodecError::Io(e) => Some(e),
            _ => None,
        }
    }
}

impl From<std::io::Error> for CodecError {
    fn from(e: std::io::Error) -> Self {
        CodecError::Io(e)
    }
}

/// Convenience result alias for codec operations.
pub type CodecResult<T> = Result<T, CodecError>;
