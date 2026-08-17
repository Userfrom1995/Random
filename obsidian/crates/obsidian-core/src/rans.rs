//! rANS entropy coding.
//!
//! Byte-aligned rANS with a 32-bit state, replicating the well-tested
//! construction of Fabian Giesen's `rans_byte.h`. The encoder processes
//! symbols in reverse (last symbol first) and writes its output bytes
//! backwards from the end of a preallocated buffer; the decoder reads
//! forward and is the exact inverse.
//!
//! Renorm thresholds: the encoder emits while `x >= x_max(s)` with
//! `x_max(s) = freq(s) * ((L >> TBITS) << 8)`; the decoder reads while
//! `x < L`. The interval math guarantees the byte counts match and the state
//! stays in `[L, 2^31)` after every encode step.

use crate::error::{CodecError, CodecResult};
use crate::tables::{RansTable, RANS_L, TBITS, TOTAL};

/// Backward writer: grows a buffer and writes from its end, so the final
/// payload is `buf[ptr..]`.
pub struct RansWriter {
    buf: Vec<u8>,
    ptr: usize,
}

impl RansWriter {
    /// Allocate a writer with room for up to `symbols` symbols (each emits at
    /// most 2 renorm bytes) plus a 4-byte flush and margin.
    pub fn with_capacity(symbols: usize) -> Self {
        let cap = symbols * 3 + 8;
        RansWriter { buf: vec![0u8; cap], ptr: cap }
    }

    #[inline]
    pub fn reserve(&mut self, extra: usize) {
        if self.ptr < extra {
            let cap = (self.buf.len() * 2 + extra).max(self.buf.len() + extra);
            let old = self.buf.len();
            self.buf.resize(cap, 0);
            self.ptr += cap - old;
        }
    }

    #[inline]
    fn push_back(&mut self, b: u8) {
        self.ptr -= 1;
        self.buf[self.ptr] = b;
    }

    /// Write the final 4-byte state (little-endian) and return the payload.
    pub fn finish(mut self, state: u32) -> Vec<u8> {
        self.reserve(4);
        self.ptr -= 4;
        self.buf[self.ptr] = (state & 0xFF) as u8;
        self.buf[self.ptr + 1] = ((state >> 8) & 0xFF) as u8;
        self.buf[self.ptr + 2] = ((state >> 16) & 0xFF) as u8;
        self.buf[self.ptr + 3] = ((state >> 24) & 0xFF) as u8;
        self.buf[self.ptr..].to_vec()
    }
}

/// Forward reader over a byte slice.
pub struct RansReader<'a> {
    bytes: &'a [u8],
    pos: usize,
}

impl<'a> RansReader<'a> {
    pub fn new(bytes: &'a [u8]) -> Self {
        RansReader { bytes, pos: 0 }
    }

    #[inline]
    fn read_byte(&mut self) -> CodecResult<u8> {
        let b = *self.bytes.get(self.pos).ok_or(CodecError::CorruptRans)?;
        self.pos += 1;
        Ok(b)
    }

    /// Read the initial 4-byte little-endian state.
    pub fn init_state(&mut self) -> CodecResult<u32> {
        if self.bytes.len() < 4 {
            return Err(CodecError::CorruptRans);
        }
        let x = u32::from_le_bytes([self.bytes[0], self.bytes[1], self.bytes[2], self.bytes[3]]);
        self.pos = 4;
        Ok(x)
    }

    /// True if all bytes have been consumed (used for a final integrity
    /// check on the plane boundary).
    pub fn exhausted(&self) -> bool {
        self.pos >= self.bytes.len()
    }

    pub fn consumed(&self) -> usize {
        self.pos
    }

    pub fn remaining(&self) -> usize {
        self.bytes.len().saturating_sub(self.pos)
    }
}

/// Encode one symbol with an adaptive table, updating the state in place and
/// emitting renorm bytes into `out`.
pub fn encode_symbol(out: &mut RansWriter, table: &mut RansTable, x: &mut u32, s: usize) {
    let freq = table.freq_of(s);
    let x_max = table.x_max(s);
    // Renormalize.
    while (*x as u64) >= x_max {
        out.push_back((*x & 0xFF) as u8);
        *x >>= 8;
    }
    // x = (x / freq) << TBITS + (x % freq) + cum
    let q = (*x / freq) as u64;
    let r = *x % freq;
    *x = ((q << TBITS) + r as u64 + table.cum_of(s) as u64) as u32;
    table.update(s);
}

/// Decode one symbol with an adaptive table: read renorm bytes, pop the
/// symbol, update the table. Returns the decoded symbol index.
pub fn decode_symbol(inp: &mut RansReader, table: &mut RansTable, x: &mut u32) -> CodecResult<usize> {
    // Renormalize forward (read while x < L).
    while *x < RANS_L {
        let b = inp.read_byte()?;
        *x = (*x << 8) | b as u32;
    }
    let t = (*x & (TOTAL - 1)) as usize;
    let s = table.slot(t);
    let freq = table.freq_of(s);
    let cum = table.cum_of_slot(s);
    *x = freq * (*x >> TBITS) + (t as u32 - cum);
    table.update(s);
    Ok(s)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::context::{unzigzag, zigzag, ALPHABET};

    fn encode_stream(symbols: &[usize]) -> Vec<u8> {
        let mut table = RansTable::new();
        let mut out = RansWriter::with_capacity(symbols.len());
        let mut x = RANS_L;
        // Encode in reverse.
        for &s in symbols.iter().rev() {
            encode_symbol(&mut out, &mut table, &mut x, s);
        }
        out.finish(x)
    }

    fn decode_stream(bytes: &[u8], n: usize) -> Vec<usize> {
        let mut table = RansTable::new();
        let mut inp = RansReader::new(bytes);
        let mut x = inp.init_state().unwrap();
        let mut out = Vec::with_capacity(n);
        for _ in 0..n {
            let s = decode_symbol(&mut inp, &mut table, &mut x).unwrap();
            out.push(s);
        }
        out
    }

    fn roundtrip(symbols: Vec<usize>) {
        let bytes = encode_stream(&symbols);
        let got = decode_stream(&bytes, symbols.len());
        assert_eq!(got, symbols, "mismatch for {} symbols", symbols.len());
    }

    #[test]
    fn empty_stream() {
        let bytes = encode_stream(&[]);
        let got = decode_stream(&bytes, 0);
        assert!(got.is_empty());
        assert!(bytes.len() <= 4);
    }

    #[test]
    fn single_symbol() {
        roundtrip(vec![0]);
        roundtrip(vec![255]);
        roundtrip(vec![511]);
    }

    #[test]
    fn one_symbol_many_times() {
        roundtrip(vec![5; 10_000]);
        roundtrip(vec![511; 5000]);
    }

    #[test]
    fn mixed_random_stream() {
        let mut s = 0x9E37_79B9u32;
        let mut symbols = Vec::with_capacity(20_000);
        for _ in 0..20_000 {
            s = s.wrapping_mul(1664525).wrapping_add(1013904223);
            // Skewed distribution favoring low symbols.
            let v = if s % 8 == 0 { 0 } else if s % 8 < 3 { (s >> 4) % 32 } else { (s >> 6) % 512 };
            symbols.push(v as usize);
        }
        roundtrip(symbols);
    }

    #[test]
    fn full_alphabet() {
        let symbols: Vec<usize> = (0..512).collect();
        roundtrip(symbols);
    }

    #[test]
    fn sparse_high_symbols() {
        let symbols: Vec<usize> = (0..512).map(|i| (i * 7) % 512).collect();
        roundtrip(symbols);
    }

    #[test]
    fn zigzag_residual_roundtrip() {
        // Encode the zigzag of every residual, decode, invert.
        let residuals: Vec<u8> = (0..=255u8).collect();
        let symbols: Vec<usize> = residuals.iter().map(|&r| zigzag(r) as usize).collect();
        let bytes = encode_stream(&symbols);
        let got = decode_stream(&bytes, symbols.len());
        let back: Vec<u8> = got.iter().map(|&u| unzigzag(u as u16)).collect();
        assert_eq!(back, residuals);
    }

    #[test]
    fn corrupt_stream_errors_not_panics() {
        // A truncated payload must error, not panic.
        let bytes = encode_stream(&vec![3; 100]);
        let short = &bytes[..bytes.len().saturating_sub(3)];
        let mut table = RansTable::new();
        let mut inp = RansReader::new(short);
        let mut x = inp.init_state().unwrap();
        let mut err = false;
        for _ in 0..100 {
            if decode_symbol(&mut inp, &mut table, &mut x).is_err() {
                err = true;
                break;
            }
        }
        assert!(err);
    }
}
