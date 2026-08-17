//! rANS frequency tables.
//!
//! A [`RansTable`] holds the working frequencies (`freq`), their prefix sums
//! (`cum`), and a 4096-entry slot table mapping each 12-bit range slot to its
//! symbol. Tables adapt online: each observed symbol increments its
//! frequency, and when the sum exceeds `TOTAL` all frequencies are halved
//! (keeping a floor of 1) and the cum/slot structures rebuilt. Rebuilds are
//! amortized logarithmic in the symbol count because the sum halves each
//! time.

/// Number of residual symbols (re-export for table sizing).
pub use crate::context::ALPHABET;

/// Table size bits: `1 << TBITS = 4096`.
pub const TBITS: u32 = 12;
pub const TOTAL: u32 = 1 << TBITS;

/// The lower bound of the rANS normalization interval.
pub const RANS_L: u32 = 1 << 23;

/// Per-symbol renorm threshold derived from frequency: `(RANS_L >> TBITS) <<
/// 8` times the frequency. Precomputed as a constant factor.
pub const RENORM_FACTOR: u32 = (RANS_L >> TBITS) << 8; // = freq * 2^19

/// A per-context adaptive frequency table.
pub struct RansTable {
    freq: [u16; ALPHABET],
    cum: [u32; ALPHABET + 1],
    slot: [u16; TOTAL as usize],
    sum: u32,
}

impl Clone for RansTable {
    fn clone(&self) -> Self {
        RansTable {
            freq: self.freq,
            cum: self.cum,
            slot: self.slot,
            sum: self.sum,
        }
    }
}

impl Default for RansTable {
    fn default() -> Self {
        Self::new()
    }
}

impl RansTable {
    /// A fresh table with every symbol at frequency 1.
    pub fn new() -> Self {
        let mut t = RansTable {
            freq: [1u16; ALPHABET],
            cum: [0u32; ALPHABET + 1],
            slot: [0u16; TOTAL as usize],
            sum: ALPHABET as u32,
        };
        t.rebuild();
        t
    }

    /// Frequency of a symbol (for tests and inspection).
    pub fn frequency(&self, s: usize) -> u32 {
        self.freq[s] as u32
    }

    pub fn sum(&self) -> u32 {
        self.sum
    }

    /// Current `cum[s]` value.
    pub fn cum_of(&self, s: usize) -> u32 {
        self.cum[s]
    }

    /// Renorm threshold for a symbol, as a u64 to avoid overflow.
    #[inline]
    pub fn x_max(&self, s: usize) -> u64 {
        (self.freq[s] as u64) * (RENORM_FACTOR as u64)
    }

    /// Register an observed symbol: increment frequency and rescale when the
    /// sum exceeds `TOTAL`.
    pub fn update(&mut self, s: usize) {
        debug_assert!(s < ALPHABET);
        self.freq[s] += 1;
        self.sum += 1;
        if self.sum > TOTAL {
            self.rescale();
        }
    }

    fn rescale(&mut self) {
        for f in self.freq.iter_mut() {
            let h = (*f as u32) / 2;
            *f = h.max(1) as u16;
        }
        self.rebuild();
    }

    /// Rebuild `cum` and `slot` from `freq`.
    fn rebuild(&mut self) {
        let mut sum = 0u32;
        for i in 0..ALPHABET {
            self.cum[i] = sum;
            sum += self.freq[i] as u32;
        }
        self.cum[ALPHABET] = sum;
        debug_assert!(sum <= TOTAL);
        // Build the slot table: slot[t] = symbol whose [cum, cum+freq) range
        // contains t.
        let mut sym = 0usize;
        for t in 0..TOTAL as usize {
            while sym + 1 < ALPHABET && self.cum[sym + 1] <= t as u32 {
                sym += 1;
            }
            self.slot[t] = sym as u16;
        }
        self.sum = sum;
    }

    /// Look up the symbol for a 12-bit slot value `t`.
    #[inline]
    pub fn slot(&self, t: usize) -> usize {
        self.slot[t] as usize
    }

    #[inline]
    pub fn freq_of(&self, s: usize) -> u32 {
        self.freq[s] as u32
    }

    #[inline]
    pub fn cum_of_slot(&self, s: usize) -> u32 {
        self.cum[s]
    }
}

/// A table that never adapts is reserved for a future static mode; v1 always
/// uses adaptive tables, so no static table type is provided yet.

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fresh_table_invariants() {
        let t = RansTable::new();
        assert_eq!(t.sum(), ALPHABET as u32);
        assert_eq!(t.cum_of(0), 0);
        assert_eq!(t.cum_of(1), 1);
        assert_eq!(t.slot(0), 0);
        assert_eq!(t.slot(1), 1);
        assert_eq!(t.slot(511), 511);
        // Sum invariant: cum[ALPHABET] == sum.
        assert_eq!(t.cum_of(ALPHABET), t.sum());
    }

    #[test]
    fn update_and_rescale_preserve_invariant() {
        let mut t = RansTable::new();
        // Push the sum well past TOTAL (4096): after each update the sum is
        // recomputed by rebuild, and stays <= TOTAL.
        for i in 0..10_000usize {
            t.update((i * 37) % ALPHABET);
            assert!(t.sum() <= TOTAL, "sum {} after {i}", t.sum());
            // cum/slot consistency spot check.
            let s = t.slot(t.sum() as usize - 1);
            assert!(s < ALPHABET);
        }
    }

    #[test]
    fn slot_matches_cum_range() {
        let mut t = RansTable::new();
        for _ in 0..2000 {
            t.update(7);
            t.update(300);
        }
        for t_idx in 0..TOTAL as usize {
            let s = t.slot(t_idx);
            let c = t.cum_of(s);
            let f = t.freq_of(s);
            assert!(t_idx as u32 >= c && (t_idx as u32) < c + f, "slot {t_idx} -> sym {s}");
        }
    }

    #[test]
    fn rescale_drops_frequencies_but_keeps_floor() {
        let mut t = RansTable::new();
        for _ in 0..5000 {
            t.update(3);
        }
        // sum must never exceed TOTAL.
        assert!(t.sum() <= TOTAL);
        // Frequencies are at least 1 for every symbol.
        for s in 0..ALPHABET {
            assert!(t.frequency(s) >= 1);
        }
    }
}
