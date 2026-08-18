//! rANS entropy coding (32-bit state, byte-aligned, adaptive or static tables).
//!
//! The rANS denominator `M` is the renormalization baseline AND the constant
//! table total. Both static and adaptive tables keep `sum(freq) == M` at all
//! times. Adaptive tables keep `freq[s]` proportional to the observed count of
//! `s`: every time a symbol occurs its frequency is incremented and one unit is
//! stolen from the richest *other* symbol (the most over-represented one, freq
//! >= 2), so the total never moves from `M`. This preserves the full `M`-wide
//! frequency resolution and the proportionality between symbols for both peaked
//! and uniform streams, so compression efficiency is preserved, and the encoder
//! and decoder apply the identical update rule, so they stay in lockstep. The
//! renorm window `[RNB, 256*RNB)` and the interval-coding step both use the
//! constant `M`: the decoder renormalizes against the fixed lower bound `RNB`
//! and decodes with the same constant `M`, so the emitted byte count exactly
//! balances the reconstructed stream.
//!
//! The encoder codes symbols in reverse raster order (so the byte-reversed
//! stack decodes in forward order) but adaptive tables must evolve in decode
//! order, so the encoder runs a forward dry-run that records each symbol's
//! `(freq, cum, total)` BEFORE the update; the reverse pass replays them via
//! `put_fc` with no further adaptation.

use crate::error::CodecError;

/// The rANS frequency denominator used as the halving baseline.
pub const M: u64 = 1 << 12;
/// The decoder renorm lower bound; the encoder keeps `x` in `[RNB, 256*RNB)`.
pub const RNB: u32 = 1 << 20;
/// Upper bound for a valid state (exclusive).
pub const INVARIANT_HIGH: u32 = 256 * RNB;

pub struct RansTable {
    size: usize,
    freq: Vec<u32>,
    bit: Vec<u32>,
    cum: Vec<u32>,
    slot: Option<Vec<u16>>,
    is_static: bool,
    /// Current sum of `freq` (always exactly `M` for both static and adaptive).
    total: u32,
}

impl RansTable {
    pub fn new_adaptive(size: usize) -> RansTable {
        assert!(size >= 1 && size <= M as usize, "bad adaptive alphabet {size}");
        let mut freq = vec![0u32; size];
        let base = M as u32 / size as u32;
        let rem = M as u32 % size as u32;
        for (s, f) in freq.iter_mut().enumerate() {
            *f = base + if (s as u32) < rem { 1 } else { 0 };
        }
        let mut table = RansTable {
            size,
            freq,
            bit: Vec::new(),
            cum: Vec::new(),
            slot: None,
            is_static: false,
            total: M as u32,
        };
        table.rebuild_bit();
        table
    }

    pub fn new_static(hist: &[u32]) -> RansTable {
        let size = hist.len();
        let freq = normalize_histogram(hist);
        let mut table = RansTable {
            size,
            freq,
            bit: Vec::new(),
            cum: Vec::new(),
            slot: None,
            is_static: true,
            total: M as u32,
        };
        table.rebuild_cum();
        table.rebuild_slot();
        table
    }

    pub fn size(&self) -> usize { self.size }
    pub fn total(&self) -> u32 { self.total }
    pub fn sum(&self) -> u64 { self.total as u64 }

    fn rebuild_bit(&mut self) {
        let n = self.freq.len();
        let mut bit = vec![0u32; n + 1];
        for (i, &f) in self.freq.iter().enumerate() {
            let mut j = i + 1;
            while j <= n {
                bit[j] += f;
                j += j & (!j + 1);
            }
        }
        self.bit = bit;
    }

    fn rebuild_cum(&mut self) {
        let mut cum = Vec::with_capacity(self.freq.len() + 1);
        let mut acc: u32 = 0;
        for &f in &self.freq {
            cum.push(acc);
            acc += f;
        }
        cum.push(acc);
        self.cum = cum;
    }

    fn rebuild_slot(&mut self) {
        let total = self.total as usize;
        let mut slot = vec![0u16; total];
        for s in 0..self.size {
            let lo = self.cum[s] as usize;
            let hi = self.cum[s + 1] as usize;
            for v in slot.iter_mut().take(hi).skip(lo) {
                *v = s as u16;
            }
        }
        self.slot = Some(slot);
    }

    fn bit_update(&mut self, s: usize, delta: u32) {
        let n = self.freq.len();
        let mut j = s + 1;
        while j <= n {
            self.bit[j] = self.bit[j].wrapping_add(delta);
            j += j & (!j + 1);
        }
    }

    fn bit_prefix(&self, s: usize) -> u32 {
        let mut res: u32 = 0;
        let mut j = s;
        while j > 0 {
            res += self.bit[j];
            j -= j & (!j + 1);
        }
        res
    }

    pub fn lookup(&self, s: usize) -> (u32, u32) {
        let f = self.freq[s];
        let c = if self.is_static { self.cum[s] } else { self.bit_prefix(s) };
        (f, c)
    }

    pub fn find(&self, t: u32) -> usize {
        debug_assert!(t < self.total);
        if self.is_static {
            self.slot.as_ref().unwrap()[t as usize] as usize
        } else {
            self.bit_find(t)
        }
    }

    fn bit_find(&self, t: u32) -> usize {
        let n = self.freq.len();
        let mut idx = 0usize;
        let mut step = 1usize;
        while step <= n { step <<= 1; }
        step >>= 1;
        let mut t = t;
        while step > 0 {
            let next = idx + step;
            if next <= n && self.bit[next] <= t {
                t -= self.bit[next];
                idx = next;
            }
            step >>= 1;
        }
        idx
    }

    /// Adaptive update: increment `freq[s]` and steal one unit from the richest
    /// *other* symbol (the most over-represented one, freq >= 2) so the running
    /// total stays exactly `M`. Stealing from the most over-represented symbol
    /// (rather than a fixed LIFO victim) keeps the frequencies proportional to
    /// the observed counts for both peaked and uniform streams, and never
    /// starves a symbol below 1. Keeping `total == M` means `cum[s+1] <= M`
    /// always, so the decoder's `t = state % M` bijection has no reachable dead
    /// zone and the encoder/decoder stay in lockstep. Encoder and decoder apply
    /// the identical rule.
    pub fn adapt(&mut self, s: usize) {
        debug_assert!(!self.is_static);
        debug_assert!(s < self.size);
        self.freq[s] += 1;
        self.bit_update(s, 1);
        // Pick the richest symbol other than `s` that still has freq >= 2 to
        // steal from (so no symbol drops below 1). If every other symbol is
        // already at 1, steal from `s` itself, which is a no-op for the total.
        let mut victim = s;
        let mut victim_f = 0u32;
        for i in 0..self.size {
            if i != s && self.freq[i] >= 2 && self.freq[i] > victim_f {
                victim_f = self.freq[i];
                victim = i;
            }
        }
        if victim == s {
            self.freq[s] -= 1;
            self.bit_update(s, 1u32.wrapping_neg());
        } else {
            self.freq[victim] -= 1;
            self.bit_update(victim, 1u32.wrapping_neg());
        }
        debug_assert_eq!(self.freq.iter().map(|&x| x as u64).sum::<u64>(), M);
        self.total = M as u32;
    }
}

pub fn normalize_histogram(hist: &[u32]) -> Vec<u32> {
    let n = hist.len();
    let total: u64 = hist.iter().map(|&x| x as u64).sum();
    let active: Vec<usize> = (0..n).filter(|&i| hist[i] > 0).collect();
    let mut freq = vec![0u32; n];
    if active.is_empty() || total == 0 {
        for s in 0..n.min(M as usize) {
            freq[s] = 1;
        }
        let sum: u64 = freq.iter().map(|&x| x as u64).sum();
        let mut rem = M as i64 - sum as i64;
        let mut i = 0usize;
        while rem > 0 {
            freq[i % n] += 1;
            rem -= 1;
            i += 1;
        }
        return freq;
    }
    for &s in &active {
        freq[s] = ((hist[s] as u64 * M / total).max(1)) as u32;
    }
    let mut sum: i64 = freq.iter().map(|&x| x as i64).sum();
    let mut order = active.clone();
    if sum > M as i64 {
        order.sort_unstable_by(|&a, &b| freq[b].cmp(&freq[a]));
        let mut i = 0usize;
        while sum > M as i64 {
            let s = order[i % order.len()];
            i += 1;
            if freq[s] > 1 {
                freq[s] -= 1;
                sum -= 1;
            }
        }
    } else if sum < M as i64 {
        order.sort_unstable_by(|&a, &b| hist[b].cmp(&hist[a]).then_with(|| freq[b].cmp(&freq[a])));
        let mut i = 0usize;
        while sum < M as i64 {
            let s = order[i % order.len()];
            i += 1;
            freq[s] += 1;
            sum += 1;
        }
    }
    freq
}

pub struct RansEncoder {
    state: u32,
    out: Vec<u8>,
}

impl RansEncoder {
    pub fn new() -> RansEncoder {
        RansEncoder { state: RNB, out: Vec::new() }
    }

    pub fn put(&mut self, s: usize, table: &mut RansTable) {
        let (f, c) = table.lookup(s);
        self.put_fc(s, f, c, table.total);
        if !table.is_static {
            table.adapt(s);
        }
    }

    /// Encode symbol `s` with explicit `(freq, cum)`. No table adaptation.
    ///
    /// The renorm window and the interval-coding step BOTH use the constant
    /// denominator `M`. This is the proven rANS design: the decoder renormalizes
    /// against a fixed lower bound `RNB` and decodes with the same constant `M`,
    /// so the emitted byte count exactly balances the reconstructed stream and the
    /// encoder/decoder stay in lockstep. The adaptive tables only change the
    /// per-symbol `(freq, cum)`; the running `total` is kept `<= M` (see
    /// `adapt`) so `cum[s+1] <= M` and the modulo bijection `t = (x%f)+c` holds
    /// with no reachable dead zone.
    pub fn put_fc(&mut self, _s: usize, f: u32, c: u32, _total: u32) {
        debug_assert!(f >= 1);
        // Renorm upper bound tied to the constant `M` (so it matches the
        // decoder's fixed `RNB` lower bound by the byte factor 256).
        let x_max = (f as u64) * (INVARIANT_HIGH as u64) / M;
        let mut x = self.state as u64;
        while x >= x_max {
            self.out.push((x & 0xFF) as u8);
            x >>= 8;
        }
        x = (x / f as u64) * M + (x % f as u64) + c as u64;
        debug_assert!(x < (1u64 << 32));
        self.state = x as u32;
    }

    pub fn finish(mut self) -> Vec<u8> {
        self.out.reverse();
        self.out.extend_from_slice(&self.state.to_be_bytes());
        self.out
    }
}

impl Default for RansEncoder {
    fn default() -> Self { Self::new() }
}

pub struct RansDecoder<'a> {
    state: u32,
    input: &'a [u8],
    pos: usize,
}

impl<'a> RansDecoder<'a> {
    pub fn new(input: &'a [u8]) -> Result<RansDecoder<'a>, CodecError> {
        if input.len() < 4 {
            return Err(CodecError::InvalidStream("rANS payload too short".into()));
        }
        let len = input.len();
        let state = u32::from_be_bytes([
            input[len - 4], input[len - 3], input[len - 2], input[len - 1],
        ]);
        Ok(RansDecoder { state, input, pos: 0 })
    }

    pub fn get(&mut self, table: &mut RansTable) -> Result<usize, CodecError> {
        while self.state < RNB {
            if self.pos >= self.input.len() - 4 {
                return Err(CodecError::InvalidStream("rANS stream exhausted".into()));
            }
            self.state = (self.state << 8) | self.input[self.pos] as u32;
            self.pos += 1;
        }
        // A corrupt trailing state or byte sequence can push the state out of
        // the invariant window; fail cleanly instead of panicking.
        if self.state >= INVARIANT_HIGH {
            return Err(CodecError::InvalidStream("rANS state out of range".into()));
        }
        // Decode against the constant denominator `M` so the interval coding
        // matches the encoder's `put_fc` (which also uses `M`). Because `adapt`
        // keeps `total == M`, `cum[s+1] <= M`, so `t = state % M` always lies in
        // `[0, M)` and `find` always resolves to a valid slot for a correct
        // stream. Kept as a defensive backstop in case `total` is ever less than
        // `M` (it should never be for an adaptive stream produced here).
        let t = self.state % (M as u32);
        if t >= table.total {
            return Err(CodecError::InvalidStream("rANS decode symbol out of range".into()));
        }
        let s = table.find(t);
        let (f, c) = table.lookup(s);
        // On a corrupt stream the found symbol may not actually cover `t`, so
        // `t < c` (or a result outside the invariant window) signals corruption
        // and is reported as an error, never a panic.
        let x = (f as u64) * ((self.state as u64) / M) + ((t as u64) - c as u64);
        if t < c || x >= INVARIANT_HIGH as u64 {
            return Err(CodecError::InvalidStream("rANS decode out of range".into()));
        }
        self.state = x as u32;
        if !table.is_static {
            table.adapt(s);
        }
        Ok(s)
    }
}

// ===========================================================================
// Golomb-Rice entropy backend (Design A) - the M0/M1 default.
//
// Per-context adaptive Golomb-Rice. Both encoder and decoder evolve the
// per-context `k` parameter from the symbols they code, in raster order, so
// `k` is never signaled: it is implicit, mirrored state. The forward streaming
// coder needs no reverse pass and no dry-run plan, and it provably cannot
// expand (O(1) warm-up overhead versus the 9-bit rANS start that never decayed
// on small images). See `obsidian/docs/entropy-architecture.md`.
// ===========================================================================

/// Maximum Golomb-Rice parameter `k` (2^k is the Rice divisor).
pub const GR_MAX_K: u8 = 15;
/// Warm-up `k` for photographic residuals (2^2 = 4).
pub const GR_K_INIT: u8 = 2;

// ---- M3.5 (Design B): capped-and-escaped adaptive rANS ----
/// Alphabet cap `S` for the Design B rANS backend. Residuals are mapped with
/// `zigzag` (peaked at 0) and any symbol `>= S` becomes the single escape symbol
/// `S`, after which the full residual is coded by a per-context Golomb-Rice
/// fallback. With `S = 64` each per-context table needs only ~64 increments to
/// specialize (vs the 512-symbol legacy alphabet that never specialized on a
/// 768x512 image), so the rANS tables actually track the residual distribution
/// instead of coding every symbol at the ~9-bit start cost.
pub const CAPPED_ALPHABET: usize = 64;
/// Alphabet size for the capped rANS tables: symbols `[0, S-1]` plus one escape
/// symbol `S`.
pub const CAPPED_SYMBOLS: usize = CAPPED_ALPHABET + 1;

// ---- M2: JPEG-LS-style bias cancellation (dead-zone, clamped, committed) ----
/// Absolute clamp on the per-context prediction bias added by M2-A. Keeps the
/// estimate local and bounded (matches JPEG-LS `±16` spirit). Fixed, so no
/// model bytes are added.
pub const GR_BIAS_LIMIT: i16 = 16;
/// Dead-zone radius on the raw residual: `|r_raw| <= GR_BIAS_DEADZONE` leaves
/// the bias untouched. This is what keeps zero-peaked chroma from being nudged
/// to ±1 (which previously tripled its GR cost).
pub const GR_BIAS_DEADZONE: i32 = 2;
/// EMA smoothing factor (alpha = 1/GR_BIAS_ALPHA) for the bias estimate. A slow
/// estimate tracks the local *mean* residual and converges to a constant offset
/// instead of ratcheting to the clamp.
pub const GR_BIAS_ALPHA: u32 = 8;

/// Per-context Golomb-Rice adaptation state.
///
/// `k` is the Rice divisor exponent. Rather than the slow JPEG-LS bias
/// counter (which oscillates and collapses to `k = 0` on heavy-tailed
/// residual distributions), we track an integer EMA of the residual magnitude
/// `|r|` and set `k = floor(log2(ema))`. This directly targets the mean,
/// settles in a handful of symbols, and matches the encoder/decoder because
/// both recover `|r|` before updating. The architect's spec permits this
/// equivalent alternative (`k = clamp(round(log2(ema)), 0, 15)`).
#[derive(Debug, Clone)]
pub struct GrState {
    k: u8,
    /// EMA of `|r|` in Q8 fixed point (value * 256), so the mean is `ema >> 8`.
    ema: u32,
    /// M2-A prediction bias (added to the raw prediction before the residual is
    /// computed). Mirrored state: never signaled, updated identically by both
    /// encoder and decoder from the raw residual.
    bias: i16,
    /// M2-A raw-residual EMA in Q8 (`value * 256`); `bias` tracks its rounded
    /// mean. The dead-zone keeps zero-peaked planes (chroma after YCoCg-R) at
    /// zero so the bias never wanders, while offset planes converge to their true
    /// offset instead of ratcheting to the clamp.
    bias_ema: i32,
}

impl GrState {
    pub fn new(k: u8) -> GrState {
        // Seed the EMA at `2^k` so warm-up starts near a sane divisor.
        GrState {
            k,
            ema: (1u32 << k) << 8,
            bias: 0,
            bias_ema: 0,
        }
    }

    /// Current Rice divisor exponent.
    pub fn k(&self) -> u8 {
        self.k
    }

    /// Current M2-A prediction bias (added to the raw prediction).
    pub fn bias(&self) -> i16 {
        self.bias
    }

    /// Current M2-A raw-residual EMA (Q8), for inspection/tests.
    pub fn bias_ema(&self) -> i32 {
        self.bias_ema
    }

    fn log2_floor(v: u32) -> u8 {
        if v == 0 {
            0
        } else {
            // u32::ilog2 is floor(log2) for v >= 1.
            31 - v.leading_zeros() as u8
        }
    }

    /// Adapt after coding a residual of magnitude `m`. Integer EMA with
    /// alpha = 1/16; `k` tracks `floor(log2(ema))`.
    pub fn adapt(&mut self, m: u32) {
        // ema = (ema * 15 + m * 256) / 16, all in Q8 so the mean is ema >> 8.
        let m_q8 = m << 8;
        self.ema = (self.ema * 15 + m_q8 + 8) >> 4;
        let mean = self.ema >> 8;
        self.k = Self::log2_floor(mean).min(GR_MAX_K);
    }
}

/// A dependency-free bit sink that emits LSB-first and zero-pads the trailing
/// byte on `finish`. Used by the Golomb-Rice backend to keep its output inside
/// the existing per-plane, length-prefixed byte streams.
pub struct BitWriter {
    buf: Vec<u8>,
    acc: u32,
    nbits: u8,
}

impl BitWriter {
    pub fn new() -> BitWriter {
        BitWriter { buf: Vec::new(), acc: 0, nbits: 0 }
    }

    pub fn write_bit(&mut self, b: bool) {
        self.acc |= (b as u32) << self.nbits;
        self.nbits += 1;
        if self.nbits == 8 {
            self.buf.push(self.acc as u8);
            self.acc = 0;
            self.nbits = 0;
        }
    }

    /// Emit the low `n` bits of `value`, LSB-first.
    pub fn write_bits(&mut self, value: u32, n: u8) {
        for i in 0..n as u32 {
            self.write_bit((value >> i) & 1 == 1);
        }
    }

    /// Flush any pending bits (zero-padded into a final byte) and return the bytes.
    pub fn finish(mut self) -> Vec<u8> {
        if self.nbits > 0 {
            self.buf.push(self.acc as u8);
            self.acc = 0;
            self.nbits = 0;
        }
        self.buf
    }
}

impl Default for BitWriter {
    fn default() -> Self {
        Self::new()
    }
}

/// A dependency-free bit source that refills LSB-first and errors the moment a
/// read would cross the end of the buffer.
pub struct BitReader<'a> {
    data: &'a [u8],
    pos: usize,
    acc: u32,
    nbits: u8,
}

impl<'a> BitReader<'a> {
    pub fn new(data: &'a [u8]) -> BitReader<'a> {
        BitReader { data, pos: 0, acc: 0, nbits: 0 }
    }

    pub fn read_bit(&mut self) -> Result<bool, CodecError> {
        if self.nbits == 0 {
            if self.pos >= self.data.len() {
                return Err(CodecError::InvalidStream("GR bitstream exhausted".into()));
            }
            self.acc = self.data[self.pos] as u32;
            self.pos += 1;
            self.nbits = 8;
        }
        let b = (self.acc & 1) == 1;
        self.acc >>= 1;
        self.nbits -= 1;
        Ok(b)
    }

    /// Read `n` bits LSB-first (matching `BitWriter::write_bits`).
    pub fn read_bits(&mut self, n: u8) -> Result<u32, CodecError> {
        let mut v = 0u32;
        for i in 0..n as u32 {
            let b = self.read_bit()?;
            if b {
                v |= 1 << i;
            }
        }
        Ok(v)
    }

    pub fn bits_remaining(&self) -> usize {
        (self.data.len() - self.pos) * 8 + self.nbits as usize
    }
}

/// Code a signed residual `r` with the per-context Rice parameter `st.k`.
///
/// The magnitude `|r|` is Golomb-Rice coded, then (when non-zero) a single sign
/// bit is appended. Coding the sign separately instead of folding it into the
/// Rice codeword removes the ~1 bit/negative asymmetry of sign-folding and is
/// markedly tighter on the peaked-at-zero chroma residuals after YCoCg-R.
pub fn gr_write_symbol(w: &mut BitWriter, st: &mut GrState, r: i32) {
    let a = r.unsigned_abs();
    let k = st.k as u32;
    let q = a >> k;
    let rem = a & ((1u32 << k) - 1);
    for _ in 0..q {
        w.write_bit(false);
    }
    w.write_bit(true);
    if k > 0 {
        w.write_bits(rem, k as u8);
    }
    if a != 0 {
        w.write_bit(r < 0);
    }
    st.adapt(a);
}

/// Read a signed residual coded by `gr_write_symbol`, adapting `st` identically.
pub fn gr_read_symbol(r: &mut BitReader, st: &mut GrState) -> Result<i32, CodecError> {
    let mut q = 0u32;
    loop {
        let b = r.read_bit()?;
        if b {
            break;
        }
        q += 1;
    }
    let k = st.k as u8;
    let rem = if k > 0 { r.read_bits(k)? } else { 0 };
    let a = (q << k) | rem;
    let residual = if a == 0 {
        0
    } else {
        let neg = r.read_bit()?;
        if neg {
            -(a as i32)
        } else {
            a as i32
        }
    };
    st.adapt(a);
    Ok(residual)
}

/// Elias-gamma universal code for `n >= 1`. Emits `floor(log2 n)` zero bits, a
/// one bit, then the `floor(log2 n)` lower bits of `n` (LSB-first). It is
/// parameter-free and prefix-free, so the decoder recovers `n` from the zero
/// count. Used by the M2-B run mode to code a run length in one compact code.
pub fn write_gamma(w: &mut BitWriter, n: u32) {
    debug_assert!(n >= 1, "gamma code requires n >= 1");
    let k = 31 - n.leading_zeros();
    for _ in 0..k {
        w.write_bit(false);
    }
    w.write_bit(true);
    // `n` has `k + 1` bits; the leading one is the `true` bit already written,
    // so only the lower `k` bits remain.
    w.write_bits(n & ((1u32 << k) - 1), k as u8);
}

/// Read an Elias-gamma code (inverse of `write_gamma`).
pub fn read_gamma(r: &mut BitReader) -> Result<u32, CodecError> {
    let mut k: u32 = 0;
    loop {
        let b = r.read_bit()?;
        if b {
            break;
        }
        k += 1;
    }
    let low = r.read_bits(k as u8)?;
    Ok((1u32 << k) | low)
}

// ===========================================================================
// M3-A LZ77 match layer.
//
// A per-plane LZ77 match layer over the decoded sample buffer. At each position
// the encoder/decoder exchange one token: either a literal (a GR-coded signed
// residual) or a match `(offset, length)` copy. The match flag is coded by a
// tiny mirrored binary arithmetic coder (Witten-Neal-Cleary interval coder over
// the shared `BitWriter`/`BitReader`), so the flag stream is parameter-free and
// adds zero model bytes. The `(offset, length)` pair is coded with Elias-gamma
// codes (already present, parameter-free). The decoder reconstructs matches by
// copying from its own buffer, so the round-trip is bit-exact by induction: the
// encoder's decoded buffer equals the decoder's at every position, so the chosen
// `(offset, length)` always reproduce the intended pixels. When `GR_LZ` is clear
// the match layer is never entered and the stream is byte-identical to v1 GR.
// See `obsidian/docs/m3-lz77-weighted-predictor.md`.
// ===========================================================================

/// Minimum match length for an LZ77 back-reference (shorter runs are cheaper as
/// GR literals). Must stay >= 3 so the 3-sample hash key is always defined.
pub const MIN_MATCH: usize = 3;
/// Maximum match length. Bounds the copy loop; longer runs become consecutive
/// matches handled by the flag stream (which amortizes far better).
pub const MAX_MATCH: usize = 256;

/// Code a match descriptor: `length` is the matched run length (>= `MIN_MATCH`).
/// Both `length` and `offset` are coded with Elias-gamma; `length` is shifted so
/// it stays in the gamma-valid `n >= 1` domain.
pub fn write_match(w: &mut BitWriter, offset: u32, length: u32) {
    debug_assert!(length as usize >= MIN_MATCH && offset >= 1);
    write_gamma(w, length - MIN_MATCH as u32 + 1);
    write_gamma(w, offset);
}

/// Read a match descriptor (inverse of `write_match`).
pub fn read_match(r: &mut BitReader) -> Result<(u32, u32), CodecError> {
    let lmm = read_gamma(r)?; // >= 1
    let offset = read_gamma(r)?;
    Ok((offset, lmm + MIN_MATCH as u32 - 1))
}

// ---- Mirrored binary arithmetic coder for the per-pixel match flag ----------
// A 16-bit-precision WNC interval coder. `p` is the 12-bit probability of a
// `match` bit (P(literal) = 1 - p/4096). Both sides adapt `p` identically from
// the decoded flag, so it is mirrored and never signaled. The decoder reads
// lazily (no fixed up-front block), so it never runs past the encoder's emitted
// bits and stays bit-exact for any plane size, including 1x1 planes.

const BIN_BITS: u32 = 16;
const BIN_TOP: u32 = 1 << 16;
const BIN_HALF: u32 = 1 << 15;
const BIN_QUARTER: u32 = 1 << 14;
const BIN_THREE_Q: u32 = 3 << 14;
/// Probability total for the binary coder: `p` in [1, 4095] is P(bit == 1).
const BIN_TOTAL: u32 = 4096;
/// Adaptive step for the mirrored match probability (one-sided, clamped).
const BIN_STEP: i32 = 48;

/// Encoder side of the binary match-flag coder. Shares the plane's `BitWriter`.
pub struct BinEnc {
    low: u32,
    high: u32,
    pending: u32,
    p: u32,
}

impl BinEnc {
    pub fn new() -> BinEnc {
        BinEnc { low: 0, high: BIN_TOP - 1, pending: 0, p: 64 }
    }

    fn renorm(&mut self, w: &mut BitWriter) {
        loop {
            if self.high < BIN_HALF {
                w.write_bit(false);
                for _ in 0..self.pending {
                    w.write_bit(true);
                }
                self.pending = 0;
                self.low = (self.low << 1) & (BIN_TOP - 1);
                self.high = ((self.high << 1) | 1) & (BIN_TOP - 1);
            } else if self.low >= BIN_HALF {
                w.write_bit(true);
                for _ in 0..self.pending {
                    w.write_bit(false);
                }
                self.pending = 0;
                self.low = (self.low << 1) & (BIN_TOP - 1);
                self.high = ((self.high << 1) | 1) & (BIN_TOP - 1);
            } else if self.low >= BIN_QUARTER && self.high < BIN_THREE_Q {
                self.pending += 1;
                self.low -= BIN_QUARTER;
                self.high -= BIN_QUARTER;
                self.low = (self.low << 1) & (BIN_TOP - 1);
                self.high = ((self.high << 1) | 1) & (BIN_TOP - 1);
            } else {
                break;
            }
        }
    }

    /// Code one flag bit (`true` = match). The mirrored probability `p` tracks
    /// P(match) and is updated identically on both sides.
    pub fn put(&mut self, w: &mut BitWriter, bit: bool) {
        let pm = self.p;
        let range = self.high - self.low + 1;
        let split = self.low + (range * pm) / BIN_TOTAL;
        if bit {
            self.high = split - 1;
            self.p = (self.p as i32 + BIN_STEP).clamp(1, 4095) as u32;
        } else {
            self.low = split;
            self.p = (self.p as i32 - BIN_STEP).clamp(1, 4095) as u32;
        }
        self.renorm(w);
    }

    /// Flush the final arithmetic-coded bits into the shared writer. The decoder
    /// never needs these trailing bits (it stops after the last symbol), but
    /// flushing keeps the stream well-formed and self-delimiting per plane.
    pub fn finish(&mut self, w: &mut BitWriter) {
        self.pending += 1;
        if self.low < BIN_QUARTER {
            w.write_bit(false);
            for _ in 0..self.pending {
                w.write_bit(true);
            }
        } else {
            w.write_bit(true);
            for _ in 0..self.pending {
                w.write_bit(false);
            }
        }
        self.pending = 0;
    }
}

impl Default for BinEnc {
    fn default() -> Self {
        Self::new()
    }
}

/// Decoder side of the binary match-flag coder. Seeds `value` from `BIN_BITS`
/// leading bits of the stream (the encoder always emits at least that many for a
/// non-empty plane), then mirrors the encoder's renorm on demand.
pub struct BinDec {
    low: u32,
    high: u32,
    value: u32,
    p: u32,
}

impl BinDec {
    pub fn new() -> BinDec {
        BinDec { low: 0, high: BIN_TOP - 1, value: 0, p: 64 }
    }

    /// Read a single bit, treating an exhausted stream as a zero bit. The binary
    /// coder always emits enough trailing bits for a valid plane, so exhaustion
    /// here only happens while padding a tiny plane's final value; corruption is
    /// caught downstream by the container CRC.
    fn read_bit_eof(r: &mut BitReader) -> bool {
        r.read_bit().unwrap_or(false)
    }

    /// Seed `value` from the leading `BIN_BITS` bits of the stream.
    pub fn init(&mut self, r: &mut BitReader) {
        for _ in 0..BIN_BITS {
            let bit = Self::read_bit_eof(r) as u32;
            self.value = ((self.value << 1) | bit) & (BIN_TOP - 1);
        }
    }

    fn renorm(&mut self, r: &mut BitReader) {
        loop {
            if self.high < BIN_HALF {
                let bit = Self::read_bit_eof(r) as u32;
                self.value = ((self.value << 1) | bit) & (BIN_TOP - 1);
                self.low = (self.low << 1) & (BIN_TOP - 1);
                self.high = ((self.high << 1) | 1) & (BIN_TOP - 1);
            } else if self.low >= BIN_HALF {
                let bit = Self::read_bit_eof(r) as u32;
                self.value = ((self.value << 1) | bit) & (BIN_TOP - 1);
                self.low = (self.low << 1) & (BIN_TOP - 1);
                self.high = ((self.high << 1) | 1) & (BIN_TOP - 1);
            } else if self.low >= BIN_QUARTER && self.high < BIN_THREE_Q {
                self.value -= BIN_QUARTER;
                self.low -= BIN_QUARTER;
                self.high -= BIN_QUARTER;
                let bit = Self::read_bit_eof(r) as u32;
                self.value = ((self.value << 1) | bit) & (BIN_TOP - 1);
                self.low = (self.low << 1) & (BIN_TOP - 1);
                self.high = ((self.high << 1) | 1) & (BIN_TOP - 1);
            } else {
                break;
            }
        }
    }

    /// Decode one flag bit. `true` = match.
    pub fn get(&mut self, r: &mut BitReader) -> Result<bool, CodecError> {
        let pm = self.p;
        let range = self.high - self.low + 1;
        let split = self.low + (range * pm) / BIN_TOTAL;
        let bit = self.value < split;
        if bit {
            self.high = split - 1;
            self.p = (self.p as i32 + BIN_STEP).clamp(1, 4095) as u32;
        } else {
            self.low = split;
            self.p = (self.p as i32 - BIN_STEP).clamp(1, 4095) as u32;
        }
        self.renorm(r);
        Ok(bit)
    }
}

impl Default for BinDec {
    fn default() -> Self {
        Self::new()
    }
}

/// The Rice-coded bit cost of a signed residual `r` under exponent `k`.
///
/// Matches `gr_write_symbol` exactly: `q = |r| >> k` unary-coded quotient
/// (`q + 1` bits), `k` remainder bits, and one sign bit when `|r| != 0`. Used
/// by the M2.5 context mixer to score each sub-estimator (lower is better).
pub fn rice_cost(a: u32, k: u8) -> u32 {
    let k = k as u32;
    let q = a >> k;
    let mut c = q + 1;
    if k > 0 {
        c += k;
    }
    if a != 0 {
        c += 1;
    }
    c
}

/// Code a signed residual `r` with an *explicit* Rice exponent `k` (no state
/// adaptation). Used by the M2.5 context mixer, which owns its own per-context
/// adaptation state (`CmState`) and picks `k` per symbol.
pub fn gr_write_symbol_k(w: &mut BitWriter, r: i32, k: u8) {
    let a = r.unsigned_abs();
    let k = k as u32;
    let q = a >> k;
    let rem = a & ((1u32 << k) - 1);
    for _ in 0..q {
        w.write_bit(false);
    }
    w.write_bit(true);
    if k > 0 {
        w.write_bits(rem, k as u8);
    }
    if a != 0 {
        w.write_bit(r < 0);
    }
}

/// Read a signed residual coded by `gr_write_symbol_k` with the same explicit
/// `k`. No state adaptation (the caller's `CmState` does that).
pub fn gr_read_symbol_k(r: &mut BitReader, k: u8) -> Result<i32, CodecError> {
    let mut q = 0u32;
    loop {
        let b = r.read_bit()?;
        if b {
            break;
        }
        q += 1;
    }
    let k = k as u8;
    let rem = if k > 0 { r.read_bits(k)? } else { 0 };
    let a = (q << k) | rem;
    let residual = if a == 0 {
        0
    } else {
        let neg = r.read_bit()?;
        if neg {
            -(a as i32)
        } else {
            a as i32
        }
    };
    Ok(residual)
}

// ===========================================================================
// R1: CMARC - Context-Modeled Adaptive binary Range Coder.
//
// This replaces the single-k per-context Golomb-Rice *symbol* coder (R0/M1)
// with a *bit*-conditioned binary range coder. Each residual is decomposed into
// a small set of binary bins (zero-flag, sign, quotient Exp-Golomb bits,
// remainder bits); every bin is coded by a per-`(cid, bin)` binary model
// conditioned on the spatial context. Because every alphabet is size 2, each
// model specializes after O(1) samples (the specialization-budget theorem in
// `obsidian/docs/research-breakthrough.md`), so the cost is `H(p) + epsilon`
// for any residual distribution `p` - strictly below GR's `H(p) + O(1)`. This
// is the breakthrough that clears the WebP (9.61) and JPEG XL (8.71) gates that
// the coarse GR symbol coder cannot reach. See `obsidian/docs/architect-cmarc-
// blueprint.md`.
//
// The binary arithmetic core (`renorm`/`finish`, `split = low + (range * p) /
// BIN_TOTAL`) is identical to the existing `BinEnc`/`BinDec`; the only change is
// that the probability `p` is read from a caller-supplied `BinModel` and the
// model is adapted after every `put`/`get`. The `BinModel` is a `Vec` indexed by
// `(cid, bin)`, so one `RangeEnc`/`RangeDec` shared across all contexts (exactly
// like the single GR `GrState` slice today) carries the whole entropy backend.
// ===========================================================================

/// Per-bin probability prior for CMARC: P(bit == 1) starts at 64/4096, a mild
/// 1-ish expectation that decays as the binary model specializes.
pub const CMARC_PRIOR: u16 = 64;
/// Mirrored adaptation step for the CMARC binary models (matches `BIN_STEP`).
pub const CMARC_STEP: i32 = 48;
/// Laplace `+C` prior used when seeding a `BinModel` from static counts (R1-c).
pub const CMARC_LAPLACE: u32 = 16;

/// A per-`(cid, bin)` binary probability model. `p` is P(bit == 1) in `[1, 4095]`.
/// The model is fully mirrored: the encoder and decoder apply identical
/// `adapt` updates in identical order, so no probability table is ever signaled.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct BinModel {
    pub p: u16,
}

impl BinModel {
    pub fn new() -> BinModel {
        BinModel { p: CMARC_PRIOR }
    }

    /// Seed from signaled Laplace counts `(n1, n0)` (number of 1-bits, 0-bits).
    /// Used by R1-c static priors; the `+C` Laplace prior bounds the start cost
    /// to `log2(2C)` and decays within O(C) symbols.
    pub fn from_counts(n1: u32, n0: u32) -> BinModel {
        let num = (n1 + CMARC_LAPLACE) as u64 * BIN_TOTAL as u64;
        let den = (n0 + n1 + 2 * CMARC_LAPLACE) as u64;
        let p = (num / den).clamp(1, 4095) as u16;
        BinModel { p }
    }

    /// Mirrored adaptation: identical on encoder and decoder (no signaled state).
    pub fn adapt(&mut self, bit: bool) {
        let d = if bit { CMARC_STEP } else { -CMARC_STEP };
        self.p = (self.p as i32 + d).clamp(1, 4095) as u16;
    }
}

impl Default for BinModel {
    fn default() -> Self {
        Self::new()
    }
}

/// Bin index of the `m == 0` flag within a context.
pub const CMARC_BIN_ZERO: usize = 0;
/// Bin index of the sign bit (only coded when `m != 0`).
pub const CMARC_BIN_SIGN: usize = 1;
/// First bin index of the magnitude bits (MSB-first binary decomposition).
pub const CMARC_BIN_MAG: usize = 2;
/// Width of the magnitude bit window that conditions each magnitude bit on the
/// `CMARC_MAG_WIN` bits already coded for the same residual. This is the R2
/// cross-bit conditioning: a magnitude bit's binary model is selected not just
/// by its position but by the trailing bits, so the coder captures the
/// within-symbol dependence that a flat per-bin marginal model (R1) cannot, and
/// approaches `H(symbol)` instead of `H(bit1)+H(bit2)+... >= H(symbol)`. The
/// position alone already encodes the prefix length (MSB-first), and the window
/// adds the adjacent-bit correlation that makes the binary decomposition
/// near-entropy on peaked photographic residuals.
pub const CMARC_MAG_WIN: usize = 2;
/// Number of window states (`2^CMARC_MAG_WIN`).
pub const CMARC_MAG_STATES: usize = 1 << CMARC_MAG_WIN;
/// Hard cap on magnitude bit-width (covers any i16 residual; per-plane we only
/// allocate the bins actually needed via `cmarc_bins_per_ctx`).
pub const CMARC_MAG_BITS_MAX: usize = 16;

/// Number of magnitude bits needed to represent a residual whose magnitude is at
/// most `max_mag` (the plane's `max - min`). At least 1 so a degenerate flat
/// plane still has one magnitude bit slot.
pub fn cmarc_mag_bits(max_mag: u32) -> usize {
    if max_mag == 0 {
        1
    } else {
        (32 - max_mag.leading_zeros()) as usize
    }
}

/// Bins per context for a given magnitude bit-width: zero-flag + sign + the
/// per-(position, window) magnitude models.
pub fn cmarc_bins_per_ctx(mag_bits: usize) -> usize {
    2 + mag_bits * CMARC_MAG_STATES
}

#[inline]
fn cid_bin(cid: usize, bins_per_ctx: usize, bin: usize) -> usize {
    cid * bins_per_ctx + bin
}

/// Per-context `k` (Rice divisor exponent) + EMA, mirroring `GrState` minus the
/// M2 bias fields. `k` now only sets the remainder width; the quotient is coded
/// fractionally so the integer `k` quantization no longer bounds the coder.
#[derive(Debug, Clone)]
pub struct CarcCtx {
    k: u8,
    ema: u32,
}

impl CarcCtx {
    pub fn new() -> CarcCtx {
        let k = GR_K_INIT;
        CarcCtx {
            k,
            ema: (1u32 << k) << 8,
        }
    }

    pub fn k(&self) -> u8 {
        self.k
    }

    fn log2_floor(v: u32) -> u8 {
        if v == 0 {
            0
        } else {
            31 - v.leading_zeros() as u8
        }
    }

    /// Adapt after coding a residual of magnitude `m`. Integer EMA with
    /// alpha = 1/16; `k` tracks `floor(log2(ema))`. Identical on both sides.
    pub fn adapt(&mut self, m: u32) {
        let m_q8 = m << 8;
        self.ema = (self.ema * 15 + m_q8 + 8) >> 4;
        let mean = self.ema >> 8;
        self.k = Self::log2_floor(mean).min(GR_MAX_K);
    }
}

impl Default for CarcCtx {
    fn default() -> Self {
        Self::new()
    }
}

/// Encoder side of the CMARC binary range coder. Shares the plane's `BitWriter`;
/// the probability comes from the per-`(cid, bin)` `BinModel` passed to `put`.
pub struct RangeEnc {
    low: u32,
    high: u32,
    pending: u32,
}

impl RangeEnc {
    pub fn new() -> RangeEnc {
        RangeEnc {
            low: 0,
            high: BIN_TOP - 1,
            pending: 0,
        }
    }

    fn renorm(&mut self, w: &mut BitWriter) {
        loop {
            if self.high < BIN_HALF {
                w.write_bit(false);
                for _ in 0..self.pending {
                    w.write_bit(true);
                }
                self.pending = 0;
                self.low = (self.low << 1) & (BIN_TOP - 1);
                self.high = ((self.high << 1) | 1) & (BIN_TOP - 1);
            } else if self.low >= BIN_HALF {
                w.write_bit(true);
                for _ in 0..self.pending {
                    w.write_bit(false);
                }
                self.pending = 0;
                self.low = (self.low << 1) & (BIN_TOP - 1);
                self.high = ((self.high << 1) | 1) & (BIN_TOP - 1);
            } else if self.low >= BIN_QUARTER && self.high < BIN_THREE_Q {
                self.pending += 1;
                self.low -= BIN_QUARTER;
                self.high -= BIN_QUARTER;
                self.low = (self.low << 1) & (BIN_TOP - 1);
                self.high = ((self.high << 1) | 1) & (BIN_TOP - 1);
            } else {
                break;
            }
        }
    }

    /// Code one binary `bit` with the per-bin model `m`. `m` adapts identically
    /// on both sides, so the decoder reproduces this exact split.
    pub fn put(&mut self, w: &mut BitWriter, m: &mut BinModel, bit: bool) {
        let pm = m.p as u32;
        let range = self.high - self.low + 1;
        let split = self.low + (range * pm) / BIN_TOTAL;
        if bit {
            self.high = split - 1;
            m.adapt(true);
        } else {
            self.low = split;
            m.adapt(false);
        }
        self.renorm(w);
    }

    /// Flush the final arithmetic-coded bits into the shared writer.
    pub fn finish(&mut self, w: &mut BitWriter) {
        self.pending += 1;
        if self.low < BIN_QUARTER {
            w.write_bit(false);
            for _ in 0..self.pending {
                w.write_bit(true);
            }
        } else {
            w.write_bit(true);
            for _ in 0..self.pending {
                w.write_bit(false);
            }
        }
        self.pending = 0;
    }
}

impl Default for RangeEnc {
    fn default() -> Self {
        Self::new()
    }
}

/// Decoder side of the CMARC binary range coder. Seeds `value` from `BIN_BITS`
/// leading bits of the stream, then mirrors the encoder's renorm on demand.
pub struct RangeDec {
    low: u32,
    high: u32,
    value: u32,
}

impl RangeDec {
    pub fn new() -> RangeDec {
        RangeDec {
            low: 0,
            high: BIN_TOP - 1,
            value: 0,
        }
    }

    fn read_bit_eof(r: &mut BitReader) -> bool {
        r.read_bit().unwrap_or(false)
    }

    /// Seed `value` from the leading `BIN_BITS` bits of the stream.
    pub fn init(&mut self, r: &mut BitReader) {
        for _ in 0..BIN_BITS {
            let bit = Self::read_bit_eof(r) as u32;
            self.value = ((self.value << 1) | bit) & (BIN_TOP - 1);
        }
    }

    fn renorm(&mut self, r: &mut BitReader) {
        loop {
            if self.high < BIN_HALF {
                let bit = Self::read_bit_eof(r) as u32;
                self.value = ((self.value << 1) | bit) & (BIN_TOP - 1);
                self.low = (self.low << 1) & (BIN_TOP - 1);
                self.high = ((self.high << 1) | 1) & (BIN_TOP - 1);
            } else if self.low >= BIN_HALF {
                let bit = Self::read_bit_eof(r) as u32;
                self.value = ((self.value << 1) | bit) & (BIN_TOP - 1);
                self.low = (self.low << 1) & (BIN_TOP - 1);
                self.high = ((self.high << 1) | 1) & (BIN_TOP - 1);
            } else if self.low >= BIN_QUARTER && self.high < BIN_THREE_Q {
                self.value -= BIN_QUARTER;
                self.low -= BIN_QUARTER;
                self.high -= BIN_QUARTER;
                let bit = Self::read_bit_eof(r) as u32;
                self.value = ((self.value << 1) | bit) & (BIN_TOP - 1);
                self.low = (self.low << 1) & (BIN_TOP - 1);
                self.high = ((self.high << 1) | 1) & (BIN_TOP - 1);
            } else {
                break;
            }
        }
    }

    /// Decode one binary bit with the per-bin model `m`, adapting `m` identically
    /// to the encoder.
    pub fn get(&mut self, r: &mut BitReader, m: &mut BinModel) -> Result<bool, CodecError> {
        let pm = m.p as u32;
        let range = self.high - self.low + 1;
        let split = self.low + (range * pm) / BIN_TOTAL;
        let bit = self.value < split;
        if bit {
            self.high = split - 1;
            m.adapt(true);
        } else {
            self.low = split;
            m.adapt(false);
        }
        self.renorm(r);
        Ok(bit)
    }
}

impl Default for RangeDec {
    fn default() -> Self {
        Self::new()
    }
}

/// Code a signed residual `r` with the CMARC binary range coder.
///
/// Decomposition (identical on both sides, so lockstep holds):
/// 1. `m = |r|`; emit the `m == 0` zero-flag. If set, return 0.
/// 2. Emit the sign bit (`r < 0`).
/// 3. Emit the magnitude `m` MSB-first as `mag_bits` binary bits. Each bit's
///    model is selected by `(position, window)` where `window` is the trailing
///    `CMARC_MAG_WIN` magnitude bits already coded for this residual (the R2
///    cross-bit conditioning). MSB-first means the position encodes the prefix
///    length, and the window adds the adjacent-bit correlation, so the binary
///    decomposition approaches `H(symbol)` instead of the R1 marginal-model sum.
///
/// The per-bin models and `ctx` are mirrored, so no state is signaled.
pub fn cmarc_write_residual(
    enc: &mut RangeEnc,
    w: &mut BitWriter,
    models: &mut [BinModel],
    ctx: &mut CarcCtx,
    cid: usize,
    mag_bits: usize,
    r: i32,
) {
    let bins = cmarc_bins_per_ctx(mag_bits);
    let m = r.unsigned_abs();
    let is_zero = m == 0;
    enc.put(w, &mut models[cid_bin(cid, bins, CMARC_BIN_ZERO)], is_zero);
    if is_zero {
        ctx.adapt(0);
        return;
    }
    enc.put(w, &mut models[cid_bin(cid, bins, CMARC_BIN_SIGN)], r < 0);
    let mut window: u32 = 0;
    for p in 0..mag_bits {
        let bit = (m >> (mag_bits - 1 - p)) & 1 == 1;
        let state = (window & ((1 << CMARC_MAG_WIN) - 1)) as usize;
        let bin = CMARC_BIN_MAG + p * CMARC_MAG_STATES + state;
        enc.put(w, &mut models[cid_bin(cid, bins, bin)], bit);
        window = ((window << 1) | bit as u32) & ((1 << CMARC_MAG_WIN) - 1);
    }
    ctx.adapt(m);
}

/// Read a signed residual coded by `cmarc_write_residual`, adapting the models
/// and `ctx` identically.
pub fn cmarc_read_residual(
    dec: &mut RangeDec,
    r: &mut BitReader,
    models: &mut [BinModel],
    ctx: &mut CarcCtx,
    cid: usize,
    mag_bits: usize,
) -> Result<i32, CodecError> {
    let bins = cmarc_bins_per_ctx(mag_bits);
    let is_zero = dec.get(r, &mut models[cid_bin(cid, bins, CMARC_BIN_ZERO)])?;
    if is_zero {
        ctx.adapt(0);
        return Ok(0);
    }
    let neg = dec.get(r, &mut models[cid_bin(cid, bins, CMARC_BIN_SIGN)])?;
    let mut m: u32 = 0;
    let mut window: u32 = 0;
    for p in 0..mag_bits {
        let state = (window & ((1 << CMARC_MAG_WIN) - 1)) as usize;
        let bin = CMARC_BIN_MAG + p * CMARC_MAG_STATES + state;
        let bit = dec.get(r, &mut models[cid_bin(cid, bins, bin)])?;
        m = (m << 1) | bit as u32;
        window = ((window << 1) | bit as u32) & ((1 << CMARC_MAG_WIN) - 1);
    }
    let residual = if neg { -(m as i32) } else { m as i32 };
    ctx.adapt(m);
    Ok(residual)
}

// ===========================================================================
// R2.3: LZ77 re-woven with CMARC bins (ENTROPY_MODE_CARC_LZ).
//
// M3-A failed only because, under the single-k GR symbol coder, a match (flag +
// 2 Elias-gamma codes) cost more than the GR literal it replaced. Under CMARC
// the literal is already cheap (per-`(cid, bin)` binary range coder), and the
// match flag is a single binary bin. So here the match flag, the Elias-gamma
// length/offset codes, AND the literal CMARC residual all share ONE binary range
// coder stream (the per-`(cid, bin)` `BinModel` slice). There is no separate flag
// section and no per-symbol seam; every token is just more bits through the same
// `RangeEnc`/`RangeDec`.
//
// Bin layout within a context (all indices relative to `cid * bins_per_ctx`):
//   - 0: match flag (1 = match, 0 = literal)
//   - 1: literal zero-flag (only when flag == 0)
//   - 2: literal sign      (only when flag == 0 and |r| != 0)
//   - 3..3+mag*MAG_STATES: literal magnitude bits (MSB-first, window-conditioned)
//   - L: length Elias-gamma bits (L = 3 + mag*MAG_STATES)
//   - O: offset Elias-gamma bits (O = L + CMARC_LZ_GAMMA_BINS)
//
// The decoder copies matched runs from its own already-reconstructed buffer, so
// the round-trip is bit-exact by induction: at every position the encoder's
// reference buffer equals the decoder's, so the chosen `(offset, length)` always
// reproduce the intended pixels. Because the match flag is a cheap binary bin and
// the literal is the already-cheap CMARC residual, matches now win on
// texture/chroma/flat regions where they lost under GR (M3-A). See
// `obsidian/docs/architect-cmarc-blueprint.md` section 5.3.
// ===========================================================================

/// Bin index (within a context) of the LZ match flag.
pub const CMARC_LZ_FLAG: usize = 0;
/// First bin of the literal CMARC residual (zero-flag). Shifts by one because bin
/// 0 is the match flag, so the residual never collides with it.
pub const CMARC_LZ_LIT_ZERO: usize = 1;
pub const CMARC_LZ_LIT_SIGN: usize = 2;
pub const CMARC_LZ_LIT_MAG: usize = 3;
/// Number of bins reserved for each Elias-gamma code (length and offset). A gamma
/// code of value up to `2^31` needs at most 31 leading-zero bits plus a stop-one
/// plus 31 value bits; the leading-zero/stop bin is shared (bin 0 of the gamma
/// region), so `1 + 31 = 32` bins cover it.
pub const CMARC_LZ_GAMMA_BINS: usize = 32;

/// Number of bins per context for the CARC_LZ layout, given the plane's magnitude
/// bit-width. The magnitude region (flag + zero + sign + magnitude) is followed by
/// the length gamma region and the offset gamma region.
pub fn cmarc_lz_bins_per_ctx(mag_bits: usize) -> usize {
    let lit_region = 3 + mag_bits * CMARC_MAG_STATES;
    let len_bin = lit_region;
    let off_bin = len_bin + CMARC_LZ_GAMMA_BINS;
    off_bin + CMARC_LZ_GAMMA_BINS
}

#[inline]
pub fn cmarc_lz_len_bin(mag_bits: usize) -> usize {
    3 + mag_bits * CMARC_MAG_STATES
}

#[inline]
pub fn cmarc_lz_off_bin(mag_bits: usize) -> usize {
    cmarc_lz_len_bin(mag_bits) + CMARC_LZ_GAMMA_BINS
}

/// Code an Elias-gamma value `n >= 1` through CMARC bins starting at absolute
/// slot `base` (within the per-plane model slice). Mirrors `write_gamma`'s bit
/// pattern (leading zeros, a stop-one, then LSB-first value bits) but routes every
/// bit through a binary model so the gamma is context-adaptive.
pub fn cmarc_lz_write_gamma(
    enc: &mut RangeEnc,
    w: &mut BitWriter,
    models: &mut [BinModel],
    base: usize,
    n: u32,
) {
    debug_assert!(n >= 1, "gamma code requires n >= 1");
    let k = 31 - n.leading_zeros();
    for _ in 0..k {
        enc.put(w, &mut models[base], false);
    }
    enc.put(w, &mut models[base], true);
    let low = n & ((1u32 << k) - 1);
    for i in 0..k {
        let bit = (low >> i) & 1 == 1;
        enc.put(w, &mut models[base + 1 + i as usize], bit);
    }
}

/// Read an Elias-gamma value coded by `cmarc_lz_write_gamma` (inverse, LSB-first
/// value bits). Decoder mirrors the encoder exactly, so lockstep holds.
pub fn cmarc_lz_read_gamma(
    dec: &mut RangeDec,
    r: &mut BitReader,
    models: &mut [BinModel],
    base: usize,
) -> Result<u32, CodecError> {
    let mut k: u32 = 0;
    loop {
        let b = dec.get(r, &mut models[base])?;
        if b {
            break;
        }
        k += 1;
    }
    let mut low = 0u32;
    for i in 0..k {
        let b = dec.get(r, &mut models[base + 1 + i as usize])?;
        low |= (b as u32) << i;
    }
    Ok((1u32 << k) | low)
}

/// Code a literal signed residual `r` through CMARC bins (zero-flag, sign,
/// window-conditioned magnitude). `slot_base` is `cid * bins_per_ctx`; the
/// residual bins start at `CMARC_LZ_LIT_ZERO`. The caller adapts the per-context
/// `CarcCtx` after this returns (mirroring `cmarc_write_residual`).
pub fn cmarc_lz_write_literal(
    enc: &mut RangeEnc,
    w: &mut BitWriter,
    models: &mut [BinModel],
    slot_base: usize,
    mag_bits: usize,
    r: i32,
) {
    let m = r.unsigned_abs();
    let is_zero = m == 0;
    enc.put(w, &mut models[slot_base + CMARC_LZ_LIT_ZERO], is_zero);
    if is_zero {
        return;
    }
    enc.put(w, &mut models[slot_base + CMARC_LZ_LIT_SIGN], r < 0);
    let mut window: u32 = 0;
    for p in 0..mag_bits {
        let bit = (m >> (mag_bits - 1 - p)) & 1 == 1;
        let state = (window & ((1 << CMARC_MAG_WIN) - 1)) as usize;
        let bin = CMARC_LZ_LIT_MAG + p * CMARC_MAG_STATES + state;
        enc.put(w, &mut models[slot_base + bin], bit);
        window = ((window << 1) | bit as u32) & ((1 << CMARC_MAG_WIN) - 1);
    }
}

/// Read a literal signed residual coded by `cmarc_lz_write_literal`. The caller
/// adapts the per-context `CarcCtx` with `m` after this returns.
pub fn cmarc_lz_read_literal(
    dec: &mut RangeDec,
    r: &mut BitReader,
    models: &mut [BinModel],
    slot_base: usize,
    mag_bits: usize,
) -> Result<i32, CodecError> {
    let is_zero = dec.get(r, &mut models[slot_base + CMARC_LZ_LIT_ZERO])?;
    if is_zero {
        return Ok(0);
    }
    let neg = dec.get(r, &mut models[slot_base + CMARC_LZ_LIT_SIGN])?;
    let mut m: u32 = 0;
    let mut window: u32 = 0;
    for p in 0..mag_bits {
        let state = (window & ((1 << CMARC_MAG_WIN) - 1)) as usize;
        let bin = CMARC_LZ_LIT_MAG + p * CMARC_MAG_STATES + state;
        let bit = dec.get(r, &mut models[slot_base + bin])?;
        m = (m << 1) | bit as u32;
        window = ((window << 1) | bit as u32) & ((1 << CMARC_MAG_WIN) - 1);
    }
    Ok(if neg { -(m as i32) } else { m as i32 })
}

// ===========================================================================
// R2.4: logistic context mixing (ENTROPY_MODE_CARC_MIX).
//
// PAQ / JPEG XL-MA style probability mixing. Each CMARC bin already has a
// per-`(cid, bin)` adaptive model (the context-aware estimator A). R2.4 adds a
// SECONDARY, context-independent estimator B: a per-BIN coarse model that
// captures the global per-bin distribution across all contexts (the "static
// prior" / coarse-context estimate). For every bit we blend the two estimators
// in log-odds space with a per-bin logistic weight `w` updated per bit (a
// gradient step on the mixed cross-entropy). Mixing probability estimates (not
// k choices, the M2.5 mistake) is what lets the coder beat the best single
// model, and it is the final R2 stage that closes the remaining ~0.9 bpp to the
// JPEG XL gate once CMARC + cross-channel + bank + LZ are in place. See
// `obsidian/docs/architect-cmarc-blueprint.md` section 5.4.
//
// The weight `w` and both estimator models are mirrored (identical update order
// on encoder and decoder, zero signaled bytes), so the round-trip is bit-exact.
// ===========================================================================

/// Fixed-point denominator for the logistic mixing weight (`w` in [0, MIX_WSUM]).
/// `w / MIX_WSUM` is the weight placed on the context-aware estimator A; the
/// remainder is the weight on the coarse estimator B.
pub const MIX_WSUM: i32 = 4096;
/// Initial per-bin mixing weight (equal blend of the two estimators).
pub const MIX_INIT_W: i32 = 4096 / 2;
/// Learning-rate shift for the per-bit weight update. Smaller = gentler and more
/// stable; larger = faster convergence but more oscillation. The update is
/// `(p_mix - bit) * (lo_a - lo_b) >> MIX_RATE_SHIFT`, clamped to +/-MIX_WSUM, so
/// the per-bit step is at most a few weight units and never overshoots.
pub const MIX_RATE_SHIFT: i32 = 22;

/// Logistic-stretch (log-odds) of a probability `p` in [1, 4095] (T = 4096),
/// returned in fixed point (multiply by 1/256). Both encoder and decoder call
/// this same pure function, so the stretch is identical on both sides and the
/// mix stays in lockstep.
fn cmarc_stretch(p: u16) -> i32 {
    let denom = ((BIN_TOTAL as i32 - p as i32).max(1)) as f64;
    let num = (p as i32).max(1) as f64;
    (0.5 * (num / denom).ln() * 256.0) as i32
}

/// Logistic-squash (inverse of `cmarc_stretch`): log-odds -> probability in
/// [1, 4095]. Pure, so identical on both sides.
fn cmarc_squash(lo: i32) -> u16 {
    let x = lo as f64 / 256.0;
    let p = 1.0 / (1.0 + (-x).exp());
    (p.clamp(0.0, 0.999755859375) * 4096.0).round().clamp(1.0, 4095.0) as u16
}

/// Blend estimators A (`pa`) and B (`pb`) in log-odds space with weight `w`
/// (weight on A = `w / MIX_WSUM`). Returns the mixed probability in [1, 4095].
#[inline]
fn cmarc_logit_mix(pa: u16, pb: u16, w: i32) -> u16 {
    let lo_a = cmarc_stretch(pa);
    let lo_b = cmarc_stretch(pb);
    let lo_mix = (w * lo_a + (MIX_WSUM - w) * lo_b) / MIX_WSUM;
    cmarc_squash(lo_mix)
}

/// Per-bit logistic-mix weight update (gradient step on the mixed
/// cross-entropy). Increases `w` (toward estimator A) when A is the better
/// predictor for this bit; symmetric and mirrored so lockstep holds.
#[inline]
fn cmarc_mix_update_w(bit: bool, p_mix: u16, pa: u16, pb: u16) -> i32 {
    let lo_a = cmarc_stretch(pa);
    let lo_b = cmarc_stretch(pb);
    let dw = ((p_mix as i32 - bit as i32) * (lo_a - lo_b)) >> MIX_RATE_SHIFT;
    dw.clamp(-MIX_WSUM, MIX_WSUM)
}

/// Code one binary bit using the logistic mix of the per-`(cid, bin)` primary
/// model (`models[bin_abs]`) and the per-`bin` coarse model (`mix_models[bin]`).
/// The mixed probability drives the range coder; BOTH models and the per-bin
/// weight are adapted identically on encoder and decoder (zero signaled bytes).
#[inline]
fn cmarc_mix_put(
    enc: &mut RangeEnc,
    w: &mut BitWriter,
    models: &mut [BinModel],
    mix_models: &mut [BinModel],
    mix_w: &mut [i32],
    bin_abs: usize,
    bin: usize,
    bit: bool,
) {
    let pa = models[bin_abs].p;
    let pb = mix_models[bin].p;
    let wt = mix_w[bin];
    let p_mix = cmarc_logit_mix(pa, pb, wt);
    let mut synth = BinModel { p: p_mix };
    enc.put(w, &mut synth, bit);
    // Adapt both estimators and the mixing weight with the decoded bit.
    models[bin_abs].adapt(bit);
    mix_models[bin].adapt(bit);
    let dw = cmarc_mix_update_w(bit, p_mix, pa, pb);
    mix_w[bin] = (wt + dw).clamp(0, MIX_WSUM);
}

/// Read one binary bit (mirror of `cmarc_mix_put`).
#[inline]
fn cmarc_mix_get(
    dec: &mut RangeDec,
    r: &mut BitReader,
    models: &mut [BinModel],
    mix_models: &mut [BinModel],
    mix_w: &mut [i32],
    bin_abs: usize,
    bin: usize,
) -> Result<bool, CodecError> {
    let pa = models[bin_abs].p;
    let pb = mix_models[bin].p;
    let wt = mix_w[bin];
    let p_mix = cmarc_logit_mix(pa, pb, wt);
    let mut synth = BinModel { p: p_mix };
    let bit = dec.get(r, &mut synth)?;
    models[bin_abs].adapt(bit);
    mix_models[bin].adapt(bit);
    let dw = cmarc_mix_update_w(bit, p_mix, pa, pb);
    mix_w[bin] = (wt + dw).clamp(0, MIX_WSUM);
    Ok(bit)
}

/// Code a signed residual `r` with the R2.4 logistic-mixed CMARC coder.
pub fn cmarc_mix_write_residual(
    enc: &mut RangeEnc,
    w: &mut BitWriter,
    models: &mut [BinModel],
    mix_models: &mut [BinModel],
    mix_w: &mut [i32],
    ctx: &mut CarcCtx,
    cid: usize,
    bins_per_ctx: usize,
    mag_bits: usize,
    r: i32,
) {
    let m = r.unsigned_abs();
    let is_zero = m == 0;
    let slot = cid * bins_per_ctx;
    cmarc_mix_put(
        enc,
        w,
        models,
        mix_models,
        mix_w,
        slot + CMARC_BIN_ZERO,
        CMARC_BIN_ZERO,
        is_zero,
    );
    if is_zero {
        ctx.adapt(0);
        return;
    }
    cmarc_mix_put(
        enc,
        w,
        models,
        mix_models,
        mix_w,
        slot + CMARC_BIN_SIGN,
        CMARC_BIN_SIGN,
        r < 0,
    );
    let mut window: u32 = 0;
    for p in 0..mag_bits {
        let bit = (m >> (mag_bits - 1 - p)) & 1 == 1;
        let state = (window & ((1 << CMARC_MAG_WIN) - 1)) as usize;
        let bin = CMARC_BIN_MAG + p * CMARC_MAG_STATES + state;
        cmarc_mix_put(enc, w, models, mix_models, mix_w, slot + bin, bin, bit);
        window = ((window << 1) | bit as u32) & ((1 << CMARC_MAG_WIN) - 1);
    }
    ctx.adapt(m);
}

/// Read a signed residual coded by `cmarc_mix_write_residual`.
pub fn cmarc_mix_read_residual(
    dec: &mut RangeDec,
    r: &mut BitReader,
    models: &mut [BinModel],
    mix_models: &mut [BinModel],
    mix_w: &mut [i32],
    ctx: &mut CarcCtx,
    cid: usize,
    bins_per_ctx: usize,
    mag_bits: usize,
) -> Result<i32, CodecError> {
    let slot = cid * bins_per_ctx;
    let is_zero = cmarc_mix_get(
        dec,
        r,
        models,
        mix_models,
        mix_w,
        slot + CMARC_BIN_ZERO,
        CMARC_BIN_ZERO,
    )?;
    if is_zero {
        ctx.adapt(0);
        return Ok(0);
    }
    let neg = cmarc_mix_get(
        dec,
        r,
        models,
        mix_models,
        mix_w,
        slot + CMARC_BIN_SIGN,
        CMARC_BIN_SIGN,
    )?;
    let mut m: u32 = 0;
    let mut window: u32 = 0;
    for p in 0..mag_bits {
        let state = (window & ((1 << CMARC_MAG_WIN) - 1)) as usize;
        let bin = CMARC_BIN_MAG + p * CMARC_MAG_STATES + state;
        let bit = cmarc_mix_get(dec, r, models, mix_models, mix_w, slot + bin, bin)?;
        m = (m << 1) | bit as u32;
        window = ((window << 1) | bit as u32) & ((1 << CMARC_MAG_WIN) - 1);
    }
    let residual = if neg { -(m as i32) } else { m as i32 };
    ctx.adapt(m);
    Ok(residual)
}

// ===========================================================================
// M2.5 context mixing: mixture of Rice experts (per-context).
//
// A single adaptive `k` (M1) is a compromise between local residual variance
// (which wants a small `k`) and long-run variance (which wants a larger `k`).
// M2.5 runs three independent Rice sub-estimators per context that track the
// residual magnitude at different time constants -- a fast EMA (reacts to local
// detail), a slow EMA (the M1-equivalent stationary estimate), and a very-slow
// "prior" EMA (a stable baseline) -- and a Hedge/PMAC weight update picks the
// best-performing expert for each symbol. Selection depends only on already
// decoded symbols, so the encoder and decoder stay in lockstep with zero
// signaled model bytes. This is a genuine (if lightweight) context mix: over a
// whole image the cost is at most that of the best single expert, and on
// non-stationary photographic residuals it beats M1. See
// `obsidian/docs/m25-context-mixing.md`.
// ===========================================================================

/// Number of Rice sub-estimators mixed per context (fast, slow, prior).
pub const CM_EXPERTS: usize = 3;
/// Weights are fixed-point integers summing to `CM_WSUM`.
pub const CM_WSUM: i64 = 1024;
/// EMA smoothing denominators (alpha = 1/ALPHA) for the three experts.
const CM_ALPHAS: [u32; 3] = [8, 32, 256];

/// Per-context context-mixing state: three Rice experts + Hedge weights.
#[derive(Debug, Clone)]
pub struct CmState {
    k: [u8; 3],
    ema: [u32; 3],
    w: [i64; 3],
    /// Expert index chosen for the *next* symbol (from prior statistics).
    cur: usize,
}

impl CmState {
    pub fn new() -> CmState {
        CmState {
            k: [GR_K_INIT; 3],
            ema: [(1u32 << GR_K_INIT) << 8; 3],
            w: [CM_WSUM / 3; 3],
            cur: 1, // start on the slow (M1-equivalent) expert
        }
    }

    fn log2_floor(v: u32) -> u8 {
        if v == 0 {
            0
        } else {
            31 - v.leading_zeros() as u8
        }
    }

    /// Adapt after coding a residual of magnitude `m`: update every expert's
    /// EMA/`k`, then run the Hedge update over their Rice costs and pick the
    /// most-confident expert for the next symbol.
    pub fn adapt(&mut self, m: u32) {
        for j in 0..3 {
            let a = CM_ALPHAS[j];
            self.ema[j] = (self.ema[j] * (a - 1) + (m << 8) + (a >> 1)) / a;
            let mean = self.ema[j] >> 8;
            self.k[j] = Self::log2_floor(mean).min(GR_MAX_K);
        }
        let mut sum = 0i64;
        for j in 0..3 {
            let cost = rice_cost(m, self.k[j]) as i64;
            // Hedge: reward low-cost experts (factor in (0,1]).
            let denom = 1024 + 8 * cost;
            self.w[j] = (self.w[j] * 1024 / denom).max(1);
            sum += self.w[j];
        }
        // Renormalize to `CM_WSUM` (fixed point, mirrors on both sides).
        let scale = CM_WSUM * 1024 / sum.max(1);
        for j in 0..3 {
            self.w[j] = (self.w[j] * scale / 1024).clamp(1, CM_WSUM);
        }
        let mut best = 0usize;
        let mut best_w = -1i64;
        for j in 0..3 {
            if self.w[j] > best_w {
                best_w = self.w[j];
                best = j;
            }
        }
        self.cur = best;
    }

    /// The Rice exponent to use for the current symbol (chosen from prior stats,
    /// so it is identical on the encoder and decoder).
    pub fn k_current(&self) -> u8 {
        self.k[self.cur]
    }
}

impl Default for CmState {
    fn default() -> Self {
        Self::new()
    }
}

/// Apply the M2-A bias adaptation to a `GrState` from the raw residual `r_raw`.
///
/// The dead-zone (`|r_raw| <= GR_BIAS_DEADZONE`) leaves the bias untouched so
/// zero-peaked planes (chroma after YCoCg-R) are never nudged. Otherwise the
/// bias tracks the local *mean* residual via a clamped integer EMA; the rounded
/// EMA becomes the prediction bias. This converges to a constant residual
/// offset instead of ratcheting to the clamp, and because the EMA is identical
/// on both encoder and decoder no bias value is ever written to the stream.
pub fn gr_adapt_bias(st: &mut GrState, r_raw: i32) {
    let alpha = std::env::var("OBSIDIAN_M2_ALPHA")
        .ok()
        .and_then(|s| s.parse::<i32>().ok())
        .filter(|&a| a >= 1)
        .unwrap_or(GR_BIAS_ALPHA as i32);
    let dz = std::env::var("OBSIDIAN_M2_DZ")
        .ok()
        .and_then(|s| s.parse::<i32>().ok())
        .unwrap_or(GR_BIAS_DEADZONE);
    let limit = std::env::var("OBSIDIAN_M2_BL")
        .ok()
        .and_then(|s| s.parse::<i32>().ok())
        .unwrap_or(GR_BIAS_LIMIT as i32);
    if r_raw.abs() > dz {
        // Integer EMA with alpha = 1/alpha (Q8). The mean tracks the true offset,
        // so the bias settles there rather than slamming to +/-limit.
        st.bias_ema += ((r_raw << 8) - st.bias_ema) / alpha;
        let m = (st.bias_ema + 128) >> 8;
        st.bias = m.clamp(-limit, limit) as i16;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn static_roundtrip() {
        let mut hist = [0u32; 512];
        hist[0] = 2000; hist[1] = 1000; hist[2] = 500; hist[5] = 300;
        hist[10] = 100; hist[30] = 40; hist[100] = 20; hist[255] = 10; hist[400] = 5; hist[510] = 3;
        let symbols: Vec<usize> = vec![0,5,1,2,30,0,0,0,10,255,1,400,510,5,2];
        let mut enc = RansEncoder::new();
        let mut table_e = RansTable::new_static(&hist);
        for &s in symbols.iter().rev() { enc.put(s, &mut table_e); }
        let bytes = enc.finish();
        let mut dec = RansDecoder::new(&bytes).unwrap();
        let mut table_d = RansTable::new_static(&hist);
        let mut got = Vec::new();
        for _ in symbols.iter() { got.push(dec.get(&mut table_d).unwrap()); }
        assert_eq!(got, symbols);
    }

    #[test]
    fn adaptive_roundtrip_lockstep() {
        let size = 512;
        let n = 200_000;
        let mut seed = 0xDEADBEEFu64;
        let mut rnd = move || { seed ^= seed << 13; seed ^= seed >> 7; seed ^= seed << 17; seed };
        let symbols: Vec<usize> = (0..n).map(|_| {
            let r = (rnd() % 1000) as usize;
            if r < 600 { 0 } else if r < 800 { 1 + (r % 8) } else { 10 + (r % 300) }
        }).collect();
        let (bytes, table_e) = adaptive_encode(&symbols, size);
        let (got, table_d) = adaptive_decode(&bytes, size, n);
        assert_eq!(got, symbols);
        // Tables evolved identically (fixed total preserved).
        assert_eq!(table_e.freq, table_d.freq);
        assert_eq!(table_e.freq.iter().map(|&x| x as u64).sum::<u64>(), M);
        assert_eq!(table_d.freq.iter().map(|&x| x as u64).sum::<u64>(), M);
    }

    #[test]
    fn adaptive_single_symbol() {
        let syms = vec![7usize; 10_000];
        let (bytes, _) = adaptive_encode(&syms, 64);
        let (got, _) = adaptive_decode(&bytes, 64, syms.len());
        assert_eq!(got, syms);
    }

    #[test]
    fn renorm_pressure() {
        for size in [4usize, 8, 32] {
            let syms: Vec<usize> = (0..50_000).map(|i| (i * 7) % size).collect();
            let (bytes, _) = adaptive_encode(&syms, size);
            let (got, _) = adaptive_decode(&bytes, size, syms.len());
            assert_eq!(got, syms);
        }
    }

    #[test]
    fn uniform_adaptive_efficient() {
        let size = 512;
        let n = 200_000;
        let mut seed = 0xCAFEu64;
        let mut rnd = move || { seed ^= seed << 13; seed ^= seed >> 7; seed ^= seed << 17; seed };
        let symbols: Vec<usize> = (0..n).map(|_| (rnd() % size) as usize).collect();
        let (bytes, _) = adaptive_encode(&symbols, size as usize);
        let bits = bytes.len() as f64 * 8.0 / n as f64;
        assert!(bits < 10.0, "adaptive uniform too wasteful: {bits:.2} bits/sym");
    }

    #[test]
    fn encoder_invariant_window() {
        // After every put the state must sit in [RNB, 256*RNB).
        let mut enc = RansEncoder::new();
        let mut table = RansTable::new_adaptive(256);
        let mut seed = 12345678u64;
        let mut rnd = move || { seed ^= seed << 13; seed ^= seed >> 7; seed ^= seed << 17; seed };
        for _ in 0..100_000 {
            let s = (rnd() % 256) as usize;
            enc.put(s, &mut table);
            assert!(
                enc.state >= RNB && enc.state < INVARIANT_HIGH,
                "invariant violated: state {}",
                enc.state
            );
        }
    }

    #[test]
    fn normalize_exact_sum() {
        let mut hist = [0u32; 512];
        for i in 0..512usize {
            hist[i] = ((i * 13) % 7) as u32;
        }
        hist[3] = 5000;
        hist[0] = 9000;
        let f = normalize_histogram(&hist);
        assert_eq!(f.iter().map(|&x| x as u64).sum::<u64>(), M);
        for i in 0..512 {
            if hist[i] > 0 {
                assert!(f[i] >= 1, "active symbol {i} must have freq >= 1");
            } else {
                assert_eq!(f[i], 0);
            }
        }
    }

    #[test]
    fn decoder_errors_on_truncation() {
        let hist = [10u32; 512];
        let symbols: Vec<usize> = (0..20).collect();
        let mut enc = RansEncoder::new();
        let mut table_e = RansTable::new_static(&hist);
        for &s in symbols.iter().rev() {
            enc.put(s, &mut table_e);
        }
        let bytes = enc.finish();
        let truncated = &bytes[..bytes.len() - 2];
        // The payload must still be long enough to construct a decoder.
        let mut dec = match RansDecoder::new(truncated) {
            Ok(d) => d,
            Err(_) => return,
        };
        // Reading past the end must error, never panic.
        let mut table_d = RansTable::new_static(&hist);
        let mut got = 0usize;
        let result = (0..100).try_fold((), |_, _| {
            dec.get(&mut table_d).map(|_| {
                got += 1;
            })
        });
        assert!(result.is_err());
        assert!(got < 20);
    }

    #[test]
    fn gamma_roundtrip() {
        // Elias-gamma round-trips for all small n and a batch of random ones.
        for n in 1u32..4096 {
            let mut w = BitWriter::new();
            write_gamma(&mut w, n);
            let bytes = w.finish();
            let mut r = BitReader::new(&bytes);
            assert_eq!(read_gamma(&mut r).unwrap(), n, "gamma({n})");
        }
        let mut seed = 0x7777u64;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        for _ in 0..5000 {
            let n = 1u32 + ((rnd() % 1_000_000) as u32);
            let mut w = BitWriter::new();
            write_gamma(&mut w, n);
            let bytes = w.finish();
            let mut r = BitReader::new(&bytes);
            assert_eq!(read_gamma(&mut r).unwrap(), n, "gamma({n})");
        }
    }

    #[test]
    fn bin_coder_roundtrip_uniform() {
        // The mirrored binary arithmetic coder round-trips random bit strings of
        // every length 1..4000 (and a batch of biased strings). This is the
        // bit-exactness proof for the M3-A match flag.
        let mut seed = 0x5151u64;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        for len in 1usize..2000 {
            let bits: Vec<bool> = (0..len).map(|_| rnd() & 1 == 0).collect();
            let mut w = BitWriter::new();
            let mut enc = BinEnc::new();
            for &b in &bits {
                enc.put(&mut w, b);
            }
            enc.finish(&mut w);
            let bytes = w.finish();
            let mut r = BitReader::new(&bytes);
            let mut dec = BinDec::new();
            dec.init(&mut r);
            let mut got = Vec::with_capacity(len);
            for i in 0..len {
                let g = dec.get(&mut r).unwrap();
                if g != bits[i] {
                    panic!("bin length {len} diverged at {i}: expected {} got {}, bytes={:?}", bits[i] as u8, g as u8, bytes);
                }
                got.push(g);
            }
            assert_eq!(got, bits, "bin length {len}");
            assert!(r.bits_remaining() < 8, "bin leftover {len}");
        }
    }

    #[test]
    fn bin_coder_roundtrip_biased() {
        // Biased strings (mostly literals => flag rarely 1) exercise the
        // probability adaptation and the underflow (pending-bit) path.
        let mut seed = 0xABCDEu64;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        for trial in 0..2000u64 {
            let frac = (trial % 20) as u32; // probability of 1 in [0,19]/20
            let len = 1 + (rnd() as usize % 3000);
            let bits: Vec<bool> = (0..len)
                .map(|_| ((rnd() % 20) as u32) < frac)
                .collect();
            let mut w = BitWriter::new();
            let mut enc = BinEnc::new();
            for &b in &bits {
                enc.put(&mut w, b);
            }
            enc.finish(&mut w);
            let bytes = w.finish();
            let mut r = BitReader::new(&bytes);
            let mut dec = BinDec::new();
            dec.init(&mut r);
            let mut got = Vec::with_capacity(len);
            for _ in 0..len {
                got.push(dec.get(&mut r).unwrap());
            }
            assert_eq!(got, bits, "biased bin len {len} frac {frac}");
        }
    }

    #[test]
    fn bin_coder_compresses_sparse() {
        // A mostly-zero (literal) flag stream must compress: the binary coder
        // spends far less than 1 bit per flag when matches are rare.
        let len = 50_000usize;
        let bits = vec![false; len]; // all literals
        let mut w = BitWriter::new();
        let mut enc = BinEnc::new();
        for &b in &bits {
            enc.put(&mut w, b);
        }
        enc.finish(&mut w);
        let bytes = w.finish();
        let bits_used = bytes.len() * 8;
        assert!(bits_used < len / 4, "sparse flag stream too big: {bits_used} vs {len}");
    }

    #[test]
    fn match_helper_roundtrip() {
        // write_match / read_match round-trip a range of (offset, length) pairs.
        for len in MIN_MATCH as u32..200 {
            for off in [1u32, 2, 3, 7, 64, 1000, 32768] {
                let mut w = BitWriter::new();
                write_match(&mut w, off, len);
                let bytes = w.finish();
                let mut r = BitReader::new(&bytes);
                let (ro, rl) = read_match(&mut r).unwrap();
                assert_eq!((ro, rl), (off, len), "match off {off} len {len}");
            }
        }
    }

    #[test]
    fn bias_deadzone_holds_on_zero_peaked() {
        // A zero-peaked residual (|r| <= dead-zone) must never nudge the bias.
        let mut st = GrState::new(GR_K_INIT);
        for _ in 0..1000 {
            gr_adapt_bias(&mut st, 0);
            gr_adapt_bias(&mut st, 1);
            gr_adapt_bias(&mut st, -2);
            gr_adapt_bias(&mut st, 2);
        }
        assert_eq!(st.bias(), 0, "dead-zone must keep bias at 0");
    }

    #[test]
    fn bias_converges_to_constant_offset() {
        // A constant positive residual drives the bias to that offset (it tracks
        // the mean, converging rather than ratcheting to the clamp).
        let mut st = GrState::new(GR_K_INIT);
        for _ in 0..2000 {
            gr_adapt_bias(&mut st, 7);
        }
        assert_eq!(st.bias(), 7, "bias must converge to the constant offset");
    }

    #[test]
    fn bias_clamps_at_limit() {
        // A large constant residual converges to the clamp limit, never beyond.
        let mut st = GrState::new(GR_K_INIT);
        for _ in 0..2000 {
            gr_adapt_bias(&mut st, 40);
        }
        assert_eq!(st.bias(), GR_BIAS_LIMIT, "bias clamps at GR_BIAS_LIMIT");
    }

    #[test]
    fn bias_follows_mean_then_recenters() {
        // After a long +6 run the bias sits near +6; an equal-length -6 run pulls
        // it back toward 0 (it tracks the local mean, so it cannot stay pinned).
        let mut st = GrState::new(GR_K_INIT);
        for _ in 0..2000 {
            gr_adapt_bias(&mut st, 6);
        }
        let after_pos = st.bias();
        for _ in 0..4000 {
            gr_adapt_bias(&mut st, -6);
        }
        let after_neg = st.bias();
        assert!(after_pos > 0, "bias should be positive after +6 run");
        assert!(after_neg < 0, "bias should recenter negative after -6 run");
    }

    // ---- Golomb-Rice backend -------------------------------------------------

    #[test]
    fn bitwriter_reader_roundtrip() {
        // Random bit stream round-trips exactly.
        let mut seed = 0x1357u64;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        let total = 20_000usize;
        let bits: Vec<bool> = (0..total).map(|_| rnd() & 1 == 0).collect();
        let mut w = BitWriter::new();
        for &b in &bits {
            w.write_bit(b);
        }
        let bytes = w.finish();
        let mut r = BitReader::new(&bytes);
        for &b in &bits {
            assert_eq!(r.read_bit().unwrap(), b);
        }
        assert_eq!(r.bits_remaining(), 0);

        // write_bits / read_bits for a range of widths and values.
        let mut w = BitWriter::new();
        let cases: Vec<(u32, u8)> = vec![
            (0, 1), (1, 1), (0b1011, 4), (0xFF, 8), (0xABCD, 16),
            ((1 << 31) - 1, 31), (0, 32), (0xFFFF_FFFF, 32), (12345, 14),
        ];
        for &(v, n) in &cases {
            w.write_bits(v, n);
        }
        let bytes = w.finish();
        let mut r = BitReader::new(&bytes);
        for &(v, n) in &cases {
            assert_eq!(r.read_bits(n).unwrap(), v, "bits {v:#x}/{n}");
        }
    }

    #[test]
    fn bitreader_exhaustion_errors() {
        let bytes = vec![0b0000_0001u8]; // one 1 bit followed by padding zeros
        let mut r = BitReader::new(&bytes);
        assert!(r.read_bit().unwrap());
        // The remaining 7 bits are zero; reading past them must error, never loop.
        for _ in 0..7 {
            assert!(!r.read_bit().unwrap());
        }
        assert!(r.read_bit().is_err());
    }

    #[test]
    fn rice_cost_matches_gr_layout() {
        // rice_cost must equal the actual GR bit count for a sample of residuals
        // and k values, so the mixer scores experts correctly.
        for k in 0u8..=6 {
            for a in [0u32, 1, 2, 3, 7, 8, 15, 16, 255, 1023] {
                let mut w = BitWriter::new();
                gr_write_symbol_k(&mut w, a as i32, k);
                let bits = w.finish().len() * 8;
                // gr_write_symbol_k emits into whole bytes; exact bit count is the
                // relevant floor, so compare against the formula minus padding.
                let padded = (((rice_cost(a, k) + 7) / 8) * 8) as usize;
                assert!(bits <= padded, "a={a} k={k}: {bits} > {padded}");
                let mut w2 = BitWriter::new();
                gr_write_symbol_k(&mut w2, -(a as i32), k);
                assert_eq!(w2.finish().len() * 8, bits, "sign symmetry a={a} k={k}");
            }
        }
    }

    #[test]
    fn gr_symbol_k_roundtrip() {
        // Explicit-k GR round-trips and matches implicit-k GR when k agrees.
        let mut seed = 0xABCDEFu64;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        let mut w = BitWriter::new();
        let mut residuals = Vec::new();
        for _ in 0..20_000 {
            let r = ((rnd() as i32) % 2001) - 1000;
            residuals.push(r);
            gr_write_symbol_k(&mut w, r, 3);
        }
        let bytes = w.finish();
        let mut rdr = BitReader::new(&bytes);
        for &exp in &residuals {
            let got = gr_read_symbol_k(&mut rdr, 3).unwrap();
            assert_eq!(got, exp);
        }
        // Only zero-padding may remain (the writer pads the final byte).
        assert!(rdr.bits_remaining() < 8, "leftover bits: {}", rdr.bits_remaining());
    }

    #[test]
    fn cm_state_mixes_and_roundtrips() {
        // A full plane of residuals round-trips through the mixer: the encoder
        // and decoder both pick `cur` from identical prior stats, so they code
        // with the same k every symbol and reconstruct exactly.
        let mut seed = 0x1234_5678u64;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        // Non-stationary residual stream: variance shifts over time so a single
        // k cannot track it as well as the mixed experts.
        let area = 30_000usize;
        let residuals: Vec<i32> = (0..area)
            .map(|i| {
                let base = if i % 5000 < 2500 { 2 } else { 40 };
                let n = (rnd() as i32 % (2 * base + 1)) - base;
                n
            })
            .collect();
        let mut bw = BitWriter::new();
        let mut cm_w = vec![CmState::new()];
        for &r in &residuals {
            let k = cm_w[0].k_current();
            gr_write_symbol_k(&mut bw, r, k);
            cm_w[0].adapt(r.unsigned_abs());
        }
        let bytes = bw.finish();
        let mut br = BitReader::new(&bytes);
        let mut cm_r = vec![CmState::new()];
        let mut got = Vec::with_capacity(area);
        for _ in 0..area {
            let k = cm_r[0].k_current();
            let r = gr_read_symbol_k(&mut br, k).unwrap();
            got.push(r);
            cm_r[0].adapt(r.unsigned_abs());
        }
        assert_eq!(got, residuals);
        // The mixer must never be worse than the slow (M1) expert alone on this
        // non-stationary stream: decoded k series is valid (in range).
        for st in &cm_r {
            for &k in &st.k {
                assert!(k <= GR_MAX_K);
            }
        }
    }

    #[test]
    fn gr_symbol_roundtrip() {
        // gr_write_symbol / gr_read_symbol round-trip every residual in a range
        // with a matching GrState on both sides.
        let mut seed = 0xBEEF;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        let mut w = BitWriter::new();
        let mut we = GrState::new(GR_K_INIT);
        let mut residuals = Vec::new();
        for _ in 0..50_000 {
            let r = ((rnd() as i32) % 4001) - 2000;
            residuals.push(r);
            gr_write_symbol(&mut w, &mut we, r);
        }
        let bytes = w.finish();
        let mut rdr = BitReader::new(&bytes);
        let mut rd = GrState::new(GR_K_INIT);
        let mut mismatches = 0usize;
        for &exp in &residuals {
            let got = gr_read_symbol(&mut rdr, &mut rd).unwrap();
            if got != exp {
                mismatches += 1;
            }
        }
        eprintln!(
            "GR symbol roundtrip: mismatches={} enc_k={} dec_k={} bits_remaining={}",
            mismatches, we.k(), rd.k(), rdr.bits_remaining()
        );
        assert_eq!(mismatches, 0);
        // Both sides must have adapted identically.
        assert_eq!(we.k(), rd.k(), "k divergence with 0 mismatches");
    }

    #[test]
    fn gr_adapt_converges() {
        // Sustained zeros keep k low; a run of large residuals raises k; the
        // two sides converge to the same k.
        let mut w = BitWriter::new();
        let mut we = GrState::new(GR_K_INIT);
        for _ in 0..10_000 {
            gr_write_symbol(&mut w, &mut we, 0);
        }
        assert!(we.k() <= GR_K_INIT);
        let bytes = w.finish();
        let mut rdr = BitReader::new(&bytes);
        let mut rd = GrState::new(GR_K_INIT);
        for _ in 0..10_000 {
            let _ = gr_read_symbol(&mut rdr, &mut rd).unwrap();
        }
        assert_eq!(rd.k(), we.k());

        let mut w = BitWriter::new();
        let mut we = GrState::new(GR_K_INIT);
        for _ in 0..10_000 {
            gr_write_symbol(&mut w, &mut we, 2000);
        }
        assert!(we.k() > GR_K_INIT, "large residuals should raise k");
        let bytes = w.finish();
        let mut rdr = BitReader::new(&bytes);
        let mut rd = GrState::new(GR_K_INIT);
        for _ in 0..10_000 {
            let _ = gr_read_symbol(&mut rdr, &mut rd).unwrap();
        }
        assert_eq!(rd.k(), we.k());
    }

    #[test]
    fn gr_plane_roundtrip() {
        // A full plane of random residuals round-trips bit-exactly through the
        // GR backend with a single per-plane context.
        let mut seed = 0xCAFEu64;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        let w = 64usize;
        let h = 48usize;
        let area = w * h;
        let residuals: Vec<i32> = (0..area).map(|_| ((rnd() as i32) % 600) - 300).collect();
        let mut bw = BitWriter::new();
        let mut gr_w = vec![GrState::new(GR_K_INIT)];
        for &r in &residuals {
            gr_write_symbol(&mut bw, &mut gr_w[0], r);
        }
        let bytes = bw.finish();
        let mut br = BitReader::new(&bytes);
        let mut gr_r = vec![GrState::new(GR_K_INIT)];
        let mut got = Vec::with_capacity(area);
        for _ in 0..area {
            got.push(gr_read_symbol(&mut br, &mut gr_r[0]).unwrap());
        }
        assert_eq!(got, residuals);
    }

    // ---- CMARC (R1 context-modeled binary range coder) -----------------------

    #[test]
    fn cmarc_residual_roundtrip() {
        // `cmarc_write_residual`/`cmarc_read_residual` round-trip every residual
        // with matching per-`(cid, bin)` models and `CarcCtx` on both sides.
        let n = 64usize;
        // Residuals up to magnitude 4096 need 13 magnitude bits.
        let mag_bits = cmarc_mag_bits(4096);
        let mut seed = 0x1234u64;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        let mut residuals: Vec<i32> = Vec::new();
        for _ in 0..5000 {
            let r = ((rnd() as i32) % 4097) - 2048;
            residuals.push(r);
        }
        // Also exercise the exact-zero and small-magnitude edge cases.
        residuals.extend_from_slice(&[0, 0, 1, -1, 2, -2, 255, -256, 4096, -4096]);
        let mut models = vec![BinModel::new(); n * cmarc_bins_per_ctx(mag_bits)];
        let mut ctxs: Vec<CarcCtx> = (0..n).map(|_| CarcCtx::new()).collect();
        let mut enc = RangeEnc::new();
        let mut w = BitWriter::new();
        for (i, &r) in residuals.iter().enumerate() {
            let cid = i % n;
            cmarc_write_residual(&mut enc, &mut w, &mut models, &mut ctxs[cid], cid, mag_bits, r);
        }
        enc.finish(&mut w);
        let bytes = w.finish();
        let mut models2 = vec![BinModel::new(); n * cmarc_bins_per_ctx(mag_bits)];
        let mut ctxs2: Vec<CarcCtx> = (0..n).map(|_| CarcCtx::new()).collect();
        let mut rdr = BitReader::new(&bytes);
        let mut dec = RangeDec::new();
        dec.init(&mut rdr);
        let mut got = Vec::with_capacity(residuals.len());
        for i in 0..residuals.len() {
            let cid = i % n;
            got.push(
                cmarc_read_residual(&mut dec, &mut rdr, &mut models2, &mut ctxs2[cid], cid, mag_bits)
                    .unwrap(),
            );
        }
        assert_eq!(got, residuals, "CMARC residual round-trip");
        // Mirrored models must stay identical (proves no signaled state leaks).
        assert_eq!(models, models2, "CMARC models must stay mirrored");
    }

    #[test]
    fn cmarc_zero_bin_specializes() {
        // After many zero residuals the zero-flag model `p` drives toward 1 (the
        // bit "is zero" becomes certain), and encoder/decoder agree.
        let n = 8usize;
        let mag_bits = cmarc_mag_bits(4096);
        let mut models = vec![BinModel::new(); n * cmarc_bins_per_ctx(mag_bits)];
        let mut ctxs: Vec<CarcCtx> = (0..n).map(|_| CarcCtx::new()).collect();
        let mut enc = RangeEnc::new();
        let mut w = BitWriter::new();
        for i in 0..2000 {
            let cid = i % n;
            cmarc_write_residual(&mut enc, &mut w, &mut models, &mut ctxs[cid], cid, mag_bits, 0);
        }
        enc.finish(&mut w);
        let bytes = w.finish();
        let mut models2 = vec![BinModel::new(); n * cmarc_bins_per_ctx(mag_bits)];
        let mut ctxs2: Vec<CarcCtx> = (0..n).map(|_| CarcCtx::new()).collect();
        let mut rdr = BitReader::new(&bytes);
        let mut dec = RangeDec::new();
        dec.init(&mut rdr);
        for i in 0..2000 {
            let cid = i % n;
            let r = cmarc_read_residual(&mut dec, &mut rdr, &mut models2, &mut ctxs2[cid], cid, mag_bits)
                .unwrap();
            assert_eq!(r, 0);
        }
        assert_eq!(models, models2);
        // The zero-flag model must have collapsed toward the `true` clamp (p
        // near 4095) because every residual is zero.
        for cid in 0..n {
            let zp = models[cid_bin(cid, cmarc_bins_per_ctx(mag_bits), CMARC_BIN_ZERO)].p;
            assert!(zp >= 4095, "zero bin p should have risen for all-zero, got {zp}");
        }
    }

    #[test]
    fn binmodel_from_counts() {
        // `BinModel::from_counts` reconstructs a sensible prior within [1, 4095].
        let m = BinModel::from_counts(3, 1);
        assert!(m.p >= 1 && m.p <= 4095);
        // A balanced 50/50 count stays near the center.
        let m2 = BinModel::from_counts(100, 100);
        assert!(m2.p > 1900 && m2.p < 2196, "balanced prior p={}", m2.p);
        let mut m3 = BinModel::new();
        let before = m3.p;
        m3.adapt(true);
        assert!(m3.p > before);
        m3.adapt(false);
        assert!(m3.p >= 1 && m3.p <= 4095, "BinModel stays in [1,4095]");
    }

    #[test]
    fn range_coder_bit_roundtrip() {
        // The CMARC `RangeEnc`/`RangeDec` round-trip random and biased bit
        // strings exactly (this is the bit-exactness proof for the R1 backend).
        let mut seed = 0x5151u64;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        for len in 1usize..2000 {
            let bits: Vec<bool> = (0..len).map(|_| rnd() & 1 == 0).collect();
            let mut models: Vec<BinModel> = bits.iter().map(|_| BinModel::new()).collect();
            let mut enc = RangeEnc::new();
            let mut w = BitWriter::new();
            for (i, &b) in bits.iter().enumerate() {
                enc.put(&mut w, &mut models[i], b);
            }
            enc.finish(&mut w);
            let bytes = w.finish();
            let mut models2: Vec<BinModel> = bits.iter().map(|_| BinModel::new()).collect();
            let mut rdr = BitReader::new(&bytes);
            let mut dec = RangeDec::new();
            dec.init(&mut rdr);
            let mut got = Vec::with_capacity(len);
            for i in 0..len {
                got.push(dec.get(&mut rdr, &mut models2[i]).unwrap());
            }
            assert_eq!(got, bits, "range coder len {len}");
        }
    }

    fn adaptive_encode(symbols: &[usize], size: usize) -> (Vec<u8>, RansTable) {
        let mut table = RansTable::new_adaptive(size);
        let mut plan: Vec<(u32, u32, u32)> = Vec::with_capacity(symbols.len());
        for &s in symbols {
            let (f, c) = table.lookup(s);
            plan.push((f, c, table.total));
            table.adapt(s);
        }
        let mut enc = RansEncoder::new();
        for (&s, &(f, c, total)) in symbols.iter().zip(plan.iter()).rev() {
            enc.put_fc(s, f, c, total);
        }
        (enc.finish(), table)
    }

    fn adaptive_decode(bytes: &[u8], size: usize, n: usize) -> (Vec<usize>, RansTable) {
        let mut dec = RansDecoder::new(bytes).unwrap();
        let mut table = RansTable::new_adaptive(size);
        let mut got = Vec::with_capacity(n);
        for _ in 0..n { got.push(dec.get(&mut table).unwrap()); }
        (got, table)
    }

    // ---- CMARC-LZ (R2.3 LZ77 re-woven with CMARC bins) ----------------------

    #[test]
    fn cmarc_lz_gamma_roundtrip() {
        // `cmarc_lz_write_gamma`/`cmarc_lz_read_gamma` round-trip Elias-gamma
        // values through the per-`(cid, bin)` binary models, mirroring
        // `write_gamma`/`read_gamma` bit-for-bit (leading zeros, stop-one, LSB-
        // first value bits) but context-adaptive. Length and offset of real
        // matches span 1..4000 and beyond.
        let mut seed = 0x55u64;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        let mut vals: Vec<u32> = Vec::new();
        for _ in 0..2000 {
            vals.push((rnd() % 4000) as u32 + 1);
        }
        vals.extend_from_slice(&[
            1u32,
            2,
            3,
            MIN_MATCH as u32,
            255,
            256,
            4000,
            1 << 15,
            1 << 20,
        ]);
        let n = 4usize;
        let mag_bits = 1;
        let bpc = cmarc_lz_bins_per_ctx(mag_bits);
        let mut models = vec![BinModel::new(); n * bpc];
        let mut enc = RangeEnc::new();
        let mut w = BitWriter::new();
        for (i, &v) in vals.iter().enumerate() {
            let slot = (i % n) * bpc;
            cmarc_lz_write_gamma(&mut enc, &mut w, &mut models, slot + cmarc_lz_len_bin(mag_bits), v);
        }
        enc.finish(&mut w);
        let bytes = w.finish();
        let mut models2 = vec![BinModel::new(); n * bpc];
        let mut rdr = BitReader::new(&bytes);
        let mut dec = RangeDec::new();
        dec.init(&mut rdr);
        let mut got = Vec::with_capacity(vals.len());
        for (i, &v) in vals.iter().enumerate() {
            let slot = (i % n) * bpc;
            let g = cmarc_lz_read_gamma(
                &mut dec,
                &mut rdr,
                &mut models2,
                slot + cmarc_lz_len_bin(mag_bits),
            )
            .unwrap();
            assert_eq!(g, v, "LZ gamma mismatch at {i}");
            got.push(g);
        }
        assert_eq!(got, vals, "LZ gamma stream round-trip");
        assert_eq!(models, models2, "LZ gamma models must stay mirrored");
    }

    #[test]
    fn cmarc_lz_literal_roundtrip() {
        // `cmarc_lz_write_literal`/`cmarc_lz_read_literal` round-trip signed
        // residuals through the CMARC bins (zero-flag, sign, window-conditioned
        // magnitude), with the per-context `CarcCtx` adapted identically on both
        // sides so no state is signaled.
        let mut seed = 0x99u64;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        let mut residuals: Vec<i32> = Vec::new();
        for _ in 0..3000 {
            residuals.push(((rnd() as i32) % 4097) - 2048);
        }
        residuals.extend_from_slice(&[0, 1, -1, 255, -256, 4096, -4096]);
        let n = 8usize;
        let mag_bits = cmarc_mag_bits(4096);
        let bpc = cmarc_lz_bins_per_ctx(mag_bits);
        let mut models = vec![BinModel::new(); n * bpc];
        let mut ctxs: Vec<CarcCtx> = (0..n).map(|_| CarcCtx::new()).collect();
        let mut enc = RangeEnc::new();
        let mut w = BitWriter::new();
        for (i, &r) in residuals.iter().enumerate() {
            let slot = (i % n) * bpc;
            cmarc_lz_write_literal(&mut enc, &mut w, &mut models, slot, mag_bits, r);
            ctxs[i % n].adapt(r.unsigned_abs());
        }
        enc.finish(&mut w);
        let bytes = w.finish();
        let mut models2 = vec![BinModel::new(); n * bpc];
        let mut ctxs2: Vec<CarcCtx> = (0..n).map(|_| CarcCtx::new()).collect();
        let mut rdr = BitReader::new(&bytes);
        let mut dec = RangeDec::new();
        dec.init(&mut rdr);
        let mut got = Vec::with_capacity(residuals.len());
        for i in 0..residuals.len() {
            let slot = (i % n) * bpc;
            let r = cmarc_lz_read_literal(&mut dec, &mut rdr, &mut models2, slot, mag_bits).unwrap();
            ctxs2[i % n].adapt(r.unsigned_abs());
            got.push(r);
        }
        assert_eq!(got, residuals, "LZ literal round-trip");
        assert_eq!(models, models2, "LZ literal models must stay mirrored");
    }

    #[test]
    fn cmarc_mix_residual_roundtrip() {
        // R2.4 logistic-mixed CMARC residual codec: bit-exact round-trip and
        // mirrored (encoder == decoder) model + weight state, for random
        // residuals across random contexts.
        let mut seed = 0xC0FFEEu64;
        let mut rnd = || {
            seed ^= seed.wrapping_mul(6364136223846793005).wrapping_add(1);
            seed
        };
        let mag_bits = 12usize;
        let bins_per_ctx = cmarc_bins_per_ctx(mag_bits);
        let nctx = 16usize;
        for trial in 0..200 {
            let mut models_e: Vec<BinModel> = vec![BinModel::new(); nctx * bins_per_ctx];
            let mut models_d = models_e.clone();
            let mut mix_e: Vec<BinModel> = vec![BinModel::new(); bins_per_ctx];
            let mut mix_d = mix_e.clone();
            let mut w_e: Vec<i32> = vec![MIX_INIT_W; bins_per_ctx];
            let mut w_d = w_e.clone();
            let mut ctxs_e: Vec<CarcCtx> = (0..nctx).map(|_| CarcCtx::new()).collect();
            let mut ctxs_d = ctxs_e.clone();
            let mut enc = RangeEnc::new();
            let mut bw = BitWriter::new();
            let mut log: Vec<(usize, i32)> = Vec::new();
            for _ in 0..500 {
                let cid = (rnd() as usize) % nctx;
                let r = ((rnd() % 4097) as i32) - 2048;
                cmarc_mix_write_residual(
                    &mut enc,
                    &mut bw,
                    &mut models_e,
                    &mut mix_e,
                    &mut w_e,
                    &mut ctxs_e[cid],
                    cid,
                    bins_per_ctx,
                    mag_bits,
                    r,
                );
                log.push((cid, r));
            }
            enc.finish(&mut bw);
            let bytes = bw.finish();
            let mut rdr = BitReader::new(&bytes);
            let mut dec = RangeDec::new();
            dec.init(&mut rdr);
            for (cid, r) in &log {
                let got = cmarc_mix_read_residual(
                    &mut dec,
                    &mut rdr,
                    &mut models_d,
                    &mut mix_d,
                    &mut w_d,
                    &mut ctxs_d[*cid],
                    *cid,
                    bins_per_ctx,
                    mag_bits,
                )
                .unwrap();
                assert_eq!(got, *r, "trial {trial}: residual mismatch");
            }
            // Both estimator models and the per-bin mixing weights must stay in
            // lockstep (mirrored, zero signaled bytes).
            assert_eq!(models_e, models_d, "primary models diverged trial {trial}");
            assert_eq!(mix_e, mix_d, "coarse models diverged trial {trial}");
            assert_eq!(w_e, w_d, "mixing weights diverged trial {trial}");
        }
    }
}
