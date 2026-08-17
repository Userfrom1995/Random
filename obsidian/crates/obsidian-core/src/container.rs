//! Container header, flags, and CRC32.
//!
//! Layout of an `.obsd` file (all multi-byte integers big-endian):
//!
//! ```text
//! offset  size  field
//! 0       4     magic "OBSD"
//! 4       1     version (1)
//! 5       1     flags (see [`Flags`])
//! 6       1     bit depth (8)
//! 7       1     effort (0..=7)
//! 8       4     width
//! 12      4     height
//! 16      4     crc32 of the raw channel planes
//! 20      1     num_planes (1, 3, or 4)
//! 21      1     transform (0 none, 1 YCoCg-R)
//! 22      1     model (see [`ModelInfo`])
//! 23      1     palette flag (0 or 1)
//! ...     ...   palette data (if flag): u16 count + count * 3 RGB bytes
//! ...     ...   predictor map (RLE, `map_len` entries)
//! ...     ...   per-plane payloads: u32 length + bytes, repeated `num_planes`
//! ```
//!
//! The CRC is computed over the raw (pre-transform) channel planes and
//! verified against the reconstructed planes at decode, hard-gating
//! bit-exact fidelity.

use crate::error::{CodecError, CodecResult};

/// Channel layout encoded in the low two flag bits.
pub const CHANNELS_GRAY: u8 = 0;
pub const CHANNELS_RGB: u8 = 1;
pub const CHANNELS_RGBA: u8 = 2;

/// Flag bits for the header byte.
pub struct Flags;

impl Flags {
    pub const CHANNELS_MASK: u8 = 0b0000_0011;
    /// Bit 2: reversible color transform applied.
    pub const TRANSFORM: u8 = 0b0000_0100;
    /// Bit 3: palette applied.
    pub const PALETTE: u8 = 0b0000_1000;
    /// Bits 4-7: reserved (must be zero).
    pub const RESERVED: u8 = 0b1111_0000;
}

/// Parsed container header.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Header {
    pub magic: [u8; 4],
    pub version: u8,
    pub flags: u8,
    pub bit_depth: u8,
    pub effort: u8,
    pub width: u32,
    pub height: u32,
    pub crc32: u32,
}

pub const HEADER_LEN: usize = 20;
pub const MAGIC: [u8; 4] = *b"OBSD";
pub const VERSION: u8 = 1;

/// The model selection for one container: activity resolution, static
/// tables flag, and palette presence.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ModelInfo {
    /// Activity resolution: 0 -> 1 class, 1 -> 2 classes, 2 -> 4 classes.
    pub activity_mode: u8,
    /// Whether the rANS tables are static (not used in v1; always false).
    pub static_tables: bool,
}

impl ModelInfo {
    pub fn activity_classes(&self) -> usize {
        match self.activity_mode {
            0 => 1,
            1 => 2,
            _ => 4,
        }
    }
}

/// Fixed parameters of the v1 format.
pub mod consts {
    /// Context space: 4 border regions, 365 gradient classes.
    pub const REGIONS: usize = 4;
    pub const BASE_CTX: usize = 365;
    pub const ACTIVITY_MODES: [usize; 3] = [1, 2, 4];
}

/// Compute the total context count for a given activity mode.
pub fn context_total(activity_mode: u8) -> usize {
    let classes = match activity_mode {
        0 => 1,
        1 => 2,
        _ => 4,
    };
    consts::REGIONS * consts::BASE_CTX * classes
}

// ---------------------------------------------------------------------------
// CRC32 (IEEE, reflected, polynomial 0xEDB88320) with a startup-built table.
// ---------------------------------------------------------------------------

use std::sync::OnceLock;

fn crc32_table() -> &'static [u32; 256] {
    static TABLE: OnceLock<[u32; 256]> = OnceLock::new();
    TABLE.get_or_init(|| {
        let mut table = [0u32; 256];
        for i in 0..256u32 {
            let mut c = i;
            for _ in 0..8 {
                c = if c & 1 != 0 { 0xEDB8_8320 ^ (c >> 1) } else { c >> 1 };
            }
            table[i as usize] = c;
        }
        table
    })
}

/// Compute the CRC-32 of a byte slice (standard zlib value).
pub fn crc32(bytes: &[u8]) -> u32 {
    let table = crc32_table();
    let mut c: u32 = 0xFFFF_FFFF;
    for &b in bytes {
        c = table[((c ^ b as u32) & 0xFF) as usize] ^ (c >> 8);
    }
    c ^ 0xFFFF_FFFF
}

/// Serialize the fixed 20-byte header.
pub fn write_header(h: &Header, out: &mut Vec<u8>) {
    out.extend_from_slice(&h.magic);
    out.push(h.version);
    out.push(h.flags);
    out.push(h.bit_depth);
    out.push(h.effort);
    out.extend_from_slice(&h.width.to_be_bytes());
    out.extend_from_slice(&h.height.to_be_bytes());
    out.extend_from_slice(&h.crc32.to_be_bytes());
}

/// Parse the fixed 20-byte header, validating magic/version.
pub fn read_header(bytes: &[u8]) -> CodecResult<Header> {
    if bytes.len() < HEADER_LEN {
        return Err(CodecError::Truncated);
    }
    let magic: [u8; 4] = [bytes[0], bytes[1], bytes[2], bytes[3]];
    if magic != MAGIC {
        return Err(CodecError::BadMagic);
    }
    let version = bytes[4];
    if version != VERSION {
        return Err(CodecError::BadVersion);
    }
    let flags = bytes[5];
    if flags & Flags::RESERVED != 0 {
        return Err(CodecError::CorruptContainer);
    }
    let bit_depth = bytes[6];
    if bit_depth != 8 {
        return Err(CodecError::UnsupportedBitDepth(bit_depth));
    }
    let effort = bytes[7];
    if effort > 7 {
        return Err(CodecError::InvalidEffort(effort));
    }
    let width = u32::from_be_bytes([bytes[8], bytes[9], bytes[10], bytes[11]]);
    let height = u32::from_be_bytes([bytes[12], bytes[13], bytes[14], bytes[15]]);
    if width == 0 || height == 0 {
        return Err(CodecError::InvalidDimensions(width, height));
    }
    let crc32 = u32::from_be_bytes([bytes[16], bytes[17], bytes[18], bytes[19]]);
    Ok(Header { magic, version, flags, bit_depth, effort, width, height, crc32 })
}

/// Channels stored in the flags.
pub fn channels_from_flags(flags: u8) -> u8 {
    match flags & Flags::CHANNELS_MASK {
        CHANNELS_RGB => 3,
        CHANNELS_RGBA => 4,
        _ => 1,
    }
}

/// RLE encode a predictor map: repeated `(value, run)` pairs, `run` in
/// 1..=255. Values are u8 in `0..=11`.
pub fn write_map_rle(map: &[u8], out: &mut Vec<u8>) {
    let mut i = 0;
    while i < map.len() {
        let v = map[i];
        let mut run = 1usize;
        while i + run < map.len() && map[i + run] == v && run < 255 {
            run += 1;
        }
        out.push(v);
        out.push(run as u8);
        i += run;
    }
}

/// Read an RLE predictor map of exactly `map_len` entries.
pub fn read_map_rle(input: &[u8], pos: &mut usize, map_len: usize) -> CodecResult<Vec<u8>> {
    let mut map = Vec::with_capacity(map_len);
    while map.len() < map_len {
        if *pos + 1 > input.len() {
            return Err(CodecError::Truncated);
        }
        let v = input[*pos];
        let run = input[*pos + 1] as usize;
        *pos += 2;
        if v > 11 {
            return Err(CodecError::CorruptContainer);
        }
        for _ in 0..run {
            map.push(v);
            if map.len() > map_len {
                return Err(CodecError::CorruptContainer);
            }
        }
    }
    Ok(map)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn crc32_known_vector() {
        // The CRC-32 of "123456789" is 0xCBF43926.
        assert_eq!(crc32(b"123456789"), 0xCBF4_3926);
        assert_eq!(crc32(b""), 0);
    }

    #[test]
    fn crc32_detects_flips() {
        let a = crc32(&[1, 2, 3, 4, 5, 6, 7, 8]);
        let mut b = [1, 2, 3, 4, 5, 6, 7, 8];
        b[3] ^= 0x80;
        assert_ne!(a, crc32(&b));
    }

    #[test]
    fn header_roundtrip() {
        let h = Header {
            magic: MAGIC,
            version: VERSION,
            flags: Flags::TRANSFORM | CHANNELS_RGB,
            bit_depth: 8,
            effort: 4,
            width: 768,
            height: 512,
            crc32: 0xDEAD_BEEF,
        };
        let mut bytes = Vec::new();
        write_header(&h, &mut bytes);
        assert_eq!(read_header(&bytes).unwrap(), h);
    }

    #[test]
    fn header_rejects_bad_input() {
        assert_eq!(read_header(&[0; 10]).unwrap_err(), CodecError::Truncated);
        let mut bytes = Vec::new();
        write_header(
            &Header { magic: *b"NOPE", version: VERSION, flags: 0, bit_depth: 8, effort: 0, width: 1, height: 1, crc32: 0 },
            &mut bytes,
        );
        assert_eq!(read_header(&bytes).unwrap_err(), CodecError::BadMagic);
        let mut bytes2 = Vec::new();
        write_header(
            &Header { magic: MAGIC, version: 9, flags: 0, bit_depth: 8, effort: 0, width: 1, height: 1, crc32: 0 },
            &mut bytes2,
        );
        assert_eq!(read_header(&bytes2).unwrap_err(), CodecError::BadVersion);
        // Reserved flags must be rejected.
        let mut bytes3 = Vec::new();
        write_header(
            &Header { magic: MAGIC, version: VERSION, flags: 0b1000_0000, bit_depth: 8, effort: 0, width: 1, height: 1, crc32: 0 },
            &mut bytes3,
        );
        assert_eq!(read_header(&bytes3).unwrap_err(), CodecError::CorruptContainer);
    }

    #[test]
    fn map_rle_roundtrip() {
        let map: Vec<u8> = (0..5840).map(|i| if i < 1460 { 5 } else { (i % 12) as u8 }).collect();
        let mut enc = Vec::new();
        write_map_rle(&map, &mut enc);
        let mut pos = 0;
        let dec = read_map_rle(&enc, &mut pos, map.len()).unwrap();
        assert_eq!(dec, map);
        assert_eq!(pos, enc.len());
    }

    #[test]
    fn map_rle_truncated() {
        let mut pos = 0;
        assert_eq!(read_map_rle(&[5], &mut pos, 10).unwrap_err(), CodecError::Truncated);
        let mut pos = 0;
        assert_eq!(read_map_rle(&[99, 1], &mut pos, 1).unwrap_err(), CodecError::CorruptContainer);
    }
}
