# Resonata: Algorithmic & DSP Research Specification

**Project:** Resonata - a real-time audio synthesizer in C compiled to WebAssembly
**Issue:** #100 (picked from Brainstorm Board #42)
**Author:** Dr. Mob, the Researcher
**Date:** 2026-08-21
**Audience:** The Architect (blueprints) and The Builder (implementation)
**Status:** Research complete. Hands off to `architect`.

This document defines the scientific and algorithmic foundation for Resonata.
It is deliberately language-agnostic in places and C-specific where the
numeric core is concerned. It contains the mathematics, the data structures,
the complexity bounds, and a testable definition of correctness. It does NOT
contain build tooling or UI code; those are the Architect's and Builder's
domain.

---

## 1. Scope and the core principle

Resonata's value is *legibility*: every stage of the signal path must be
readable, tweakable code that you can hear instantly. That imposes one hard
constraint on the design below:

> The DSP core must be a set of **pure, deterministic functions** over an
> explicit state struct, with no hidden global state and no heap allocation on
> the audio hot path.

This is what makes the core "testable" (the issue's explicit requirement) and
what makes it hostable in WASM, where a clean state-in / state-out boundary
maps trivially onto an exported C ABI.

The signal path per voice is:

```
oscillator(s) --> mixer --> biquad filter --> ADSR-scaled VCA --> voice sum
```

plus a global master gain and a soft-clip limiter before the output buffer.

---

## 2. Sampling model and block processing

- Let `fs` be the sample rate in Hz. The reference rate is `fs = 48000`; the
  core must accept any `fs >= 8000` and recompute coefficients from it.
- The Nyquist frequency is `fn = fs / 2`.
- The signal is a discrete sequence `x[n]`, `n` in `Z`, representing a sample
  value in `[-1, 1]` (float). Internal oscillator/filter state uses `double`;
  only the final output buffer is `float32` to keep the WASM memory footprint
  small and the AudioWorklet copy cheap.

**Block processing.** The renderer is invoked once per audio callback with a
block of `N` frames (the Builder should default `N = 128`, a common
AudioWorklet quantum; must be a multiple of the platform quantum). All voices
are advanced `N` samples per call. Block processing amortizes per-call overhead
and lets the UI update parameters once per block rather than per sample.

**Time accounting.** A per-voice sample counter `n_v` and a global `n_global`
index samples. Envelope and LFO timing are expressed in seconds and converted
to sample counts via `samples = round(t_seconds * fs)`.

---

## 3. Oscillator algorithms

### 3.1 Phase accumulator

Each oscillator keeps a normalized phase `phi` in `[0, 1)`. Per sample:

```
dp = f / fs                 // phase increment per sample
phi += dp
if phi >= 1.0: phi -= 1.0   // (and record that a wrap occurred)
```

where `f` is the oscillator frequency in Hz. Integer `dp` accumulation drift is
avoided by keeping `phi` as `double` and only wrapping modulo 1.0. For very low
frequencies this is exact enough; if sub-Hz precision matters the Builder can
promote `phi` to a 64-bit fixed point, but `double` is sufficient for `fs <= 192000`.

### 3.2 Naive waveforms and why they alias

| Waveform | Naive formula over `phi in [0,1)` |
|---|---|
| Sine | `sin(2*pi*phi)` |
| Sawtooth | `2*phi - 1` |
| Square | `phi < 0.5 ? 1.0 : -1.0` |
| Triangle | `4*abs(phi - 0.5) - 1` |

The saw, square, and triangle are *discontinuous* (step/slope jumps) and have
harmonics that decay as `1/k`, `1/k`, `1/k^2` respectively. Above the Nyquist
frequency those harmonics fold back into the audible band as inharmonic
distortion. The sine is already band-limited and needs no repair.

The fix is **band-limited synthesis** via BLEP (band-limited step) / BLAMP
(band-limited ramp), or equivalently wavetable mipmapping (section 4). For the
subtractive core we use PolyBLEP; for richer timbres we use wavetables.

### 3.3 PolyBLEP anti-aliasing

PolyBLEP replaces each discontinuity with a smooth polynomial transition of
width `w` (in samples). With oversampling factor `O` (default `O = 1`, i.e. no
oversampling; `O = 2` is a cheap quality bump), the transition width is
`w = 1 / O` samples and the residual is evaluated at the fractional distance to
the discontinuity.

**Residual function** `P(d)` for a unit step as a function of signed distance
`d` measured in transition-widths, `d in [-1, 1]`:

```
P(d) = 0,                              |d| >= 1
P(d) = d*d*(3 - 2*d),                  d  >= 0     (smoothstep rising)
P(d) = d*d*(3 + 2*d),                  d  <  0     (mirror, rising)
```

This is the integral of a 3rd-order polynomial, hence "poly"-BLEP; it cancels
the leading aliasing term of a step. (For ramps, use BLAMP = integral of P, or
equivalently apply P to the slope.)

**Sawtooth with PolyBLEP.** Let `p0` be the previous phase and `p1` the current
phase. A downward discontinuity of magnitude 2 occurs when `p1 < p0` (wrap).

```
y = 2*p1 - 1                              // naive saw, range [-1,1]
t = p1 / (dp)                             // distance (in samples) past the wrap, normalized
y -= 2 * P(t)                             // subtract the band-limited step
```

The subtraction removes the aliasing lobe. The Builder must compute `t` from the
exact wrap location (`t = (p1) / dp`, since the jump is at `p1 == 0`).

**Square with PolyBLEP.** Two discontinuities per cycle (at `phi = 0.5` and
`phi = 0.0`). Apply `+P` at the rising edge and `-P` at the falling edge,
scaled by the jump magnitude (2.0).

**Triangle.** Triangle is the integral of a square, so it has no step
discontinuity, only slope discontinuities. Apply BLAMP (integral of P) at the
peaks, or simply generate it as the cumulative sum of a PolyBLEP square; for the
reference core we recommend generating triangle via `2*abs(saw)-1` of a
PolyBLEP saw, which inherits the saw's band-limiting well enough for a first
shippable demo. Document this approximation in code.

**Frequency accuracy test.** For a sine or band-limited saw at frequency `f`, a
2048-point FFT of one second of output must peak at bin `round(f / (fs/NFFT))`
within +/- 1 bin, and the energy above `fn` must be below the signal energy by
at least 40 dB for the PolyBLEP saw at `f <= fn/4` (the alias-suppression
specification).

---

## 4. Wavetable synthesis

Wavetable synthesis precomputes single-cycle waveforms at several "octave"
bandwidths so that, for any fundamental, the table used never contains a
harmonic above `fn`. This is the **mipmap** idea from graphics, applied to
frequency.

### 4.1 Table generation

- Choose `M` tables; `M = 10` covers 10 octaves (C0..C10) which is more than
  enough. Each table has `L = 2048` samples (power of two for cheap indexing).
- Table `m` represents frequencies in the band `[f0*2^m, f0*2^(m+1))` where
  `f0` is the lowest fundamental (e.g. `f0 = 20` Hz). The highest harmonic
  permitted in table `m` is `floor(fn / (f0*2^m))`; above that we zero-fill, so
  the stored waveform is intrinsically band limited for that band.
- Generation: build the harmonic series `sum_k a_k sin(2*pi*k*phi + ph_k)` but
  only for `k <= H_m`, where `H_m = floor(fn / f_low_m)`. For a classic
  "sawtooth" wavetable use `a_k = 1/k`; for pulse width `d`, `a_k = (2/(k*pi))*sin(pi*k*d)`.
- Tables are generated at init time in C (or baked into a generated header for
  zero runtime cost) and stored as `float` arrays of length `L`.

### 4.2 Reading / interpolation

For fundamental `f`:
1. Select table `m = floor(log2(f / f0))`, clamped to `[0, M-1]`.
2. Index `i = phi * L` (fractional). Linear interpolation between `table[m][floor(i)]`
   and `table[m][ceil(i)]`. Optionally cubic Hermite for lower distortion.
3. To avoid zipper noise when crossing octave boundaries, crossfade between
   `table[m]` and `table[m+1]` over a small frequency region (recommended but
   optional for the first demo).

**Complexity:** `O(1)` per sample (a couple of multiplies). Memory `O(M*L)`
(`10*2048*4 bytes ~= 80 KB`, trivially WASM-friendly).

**Test:** wavetable output at a mid-band frequency must match the analytic
band-limited harmonic sum within 1e-3 RMS, and cross-table switching must not
produce discontinuities larger than 1e-2.

---

## 5. ADSR envelope generator

The envelope is a gain multiplier `g[n]` in `[0, 1]` driving a voltage-controlled
amplifier (VCA). We use **exponential segments** (natural-sounding) with a
time-constant parameterization.

### 5.1 Segment math

Each segment approaches a target with leakage factor `lambda = exp(-1/(fs*tau))`,
where `tau` is the segment time constant. The per-sample update for a segment
moving from `g` toward `target` is:

```
g_next = target + (g - target) * lambda
```

- **Attack** (`gate on`): target = 1.0, `tau_a = attack_time / 4.605170`
  (so `g` reaches ~99% of 1.0 in `attack_time` seconds).
- **Decay**: target = `sustain` (level in `[0,1]`), `tau_d = decay_time / 4.605170`.
- **Sustain**: constant `g = sustain` while gate held.
- **Release** (`gate off`): target = 0.0, `tau_r = release_time / 4.605170`.

The constant `4.605170 = ln(100)` gives 99% settling; the Builder may expose a
"exponential vs linear" toggle, defaulting to exponential.

### 5.2 State machine

```
states: IDLE, ATTACK, DECAY, SUSTAIN, RELEASE
on note-on:  state = ATTACK; g = 0 (or 0 if retrigger)
on note-off: state = RELEASE
ATTACK:   g->1 via tau_a; when g >= 0.999 -> DECAY
DECAY:    g->sustain via tau_d; when g <= sustain -> SUSTAIN
SUSTAIN:  g = sustain (until gate off)
RELEASE:  g->0 via tau_r; when g <= 0.0001 -> IDLE (voice free)
```

**Fast-release guard.** If a note-off arrives during ATTACK/DECAY, jump
straight to RELEASE from the current `g`; do not snap to 1.0 first.

**Complexity:** `O(1)` per sample, one exponential base computed once per
parameter change (cache `lambda_a, lambda_d, lambda_r`). Memory `O(1)` per voice.

**Test:** render attack with `attack_time = 0.1 s` at `fs = 48000`; `g` must
exceed 0.99 within 4800 +/- 50 samples. Decay to `sustain = 0.5` must converge
to within 1e-3 of 0.5. Release to below 1e-3 within the specified time +/- 5%.

---

## 6. Biquad filter (RBJ Cookbook)

A biquad is a second-order IIR filter. Transfer function:

```
        b0 + b1 z^-1 + b2 z^-2
H(z) =  -----------------------
        1  + a1 z^-1 + a2 z^-2
```

All filters below share the same coefficient computation built from:

```
w0   = 2*pi*f0/fs
cosw = cos(w0)
sinw = sin(w0)
alpha = sinw / (2*Q)
```

`f0` is the corner/center frequency, `Q` the quality factor, `fs` the sample
rate. After computing the raw `b0,b1,b2,a0,a1,a2`, **normalize** by dividing
all `b` and `a` coefficients by `a0` (so the stored form uses `a0 = 1`).

### 6.1 Coefficient formulas

**Lowpass:**

```
b0 = (1 - cosw)/2
b1 =  1 - cosw
b2 = (1 - cosw)/2
a0 =  1 + alpha
a1 = -2*cosw
a2 =  1 - alpha
```

**Highpass:**

```
b0 =  (1 + cosw)/2
b1 = -(1 + cosw)
b2 =  (1 + cosw)/2
a0 =   1 + alpha
a1 =  -2*cosw
a2 =   1 - alpha
```

**Bandpass (constant 0 dB peak gain):**

```
b0 =  alpha
b1 =  0
b2 = -alpha
a0 =  1 + alpha
a1 = -2*cosw
a2 =  1 - alpha
```

**Bandpass (constant skirt gain):**

```
b0 =  sinw/2  ( = Q*alpha )
b1 =  0
b2 = -sinw/2
a0 =  1 + alpha
a1 = -2*cosw
a2 =  1 - alpha
```

**Notch:**

```
b0 =  1
b1 = -2*cosw
b2 =  1
a0 =  1 + alpha
a1 = -2*cosw
a2 =  1 - alpha
```

**Peaking EQ (gain `A = 10^(dBgain/40)`):**

```
b0 =  1 + alpha*A
b1 = -2*cosw
b2 =  1 - alpha*A
a0 =  1 + alpha/A
a1 = -2*cosw
a2 =  1 - alpha/A
```

**Low shelf (`A = 10^(dBgain/40)`):**

```
b0 =  A*( (A+1) - (A-1)*cosw + 2*sqrt(A)*alpha )
b1 =  2*A*( (A-1) - (A+1)*cosw )
b2 =  A*( (A+1) - (A-1)*cosw - 2*sqrt(A)*alpha )
a0 =     (A+1) + (A-1)*cosw + 2*sqrt(A)*alpha
a1 = -2*( (A-1) + (A+1)*cosw )
a2 =     (A+1) + (A-1)*cosw - 2*sqrt(A)*alpha
```

**High shelf (`A = 10^(dBgain/40)`):**

```
b0 =  A*( (A+1) + (A-1)*cosw + 2*sqrt(A)*alpha )
b1 = -2*A*( (A-1) + (A+1)*cosw )
b2 =  A*( (A+1) + (A-1)*cosw - 2*sqrt(A)*alpha )
a0 =     (A+1) - (A-1)*cosw + 2*sqrt(A)*alpha
a1 =  2*( (A-1) - (A+1)*cosw )
a2 =     (A+1) - (A-1)*cosw - 2*sqrt(A)*alpha
```

### 6.2 Topology: Transposed Direct Form II

Use the **transposed Direct Form II** realization for numerical stability and
minimal state (two delay registers `s1, s2`):

```
y   = b0*x + s1
s1  = b1*x - a1*y + s2
s2  = b2*x - a2*y
```

(Here `a1, a2` are the *normalized* coefficients, i.e. divided by `a0`.) TDF2 is
preferred over Direct Form I in floating point because the intermediate sums are
kept smaller, reducing round-off growth, and it has the best transient behavior
when coefficients change per block (no "zipper" spikes).

**Denormal protection.** Multiply `s1, s2` by `1 + 1e-20` (or flush subnormals)
each sample, or add a tiny DC offset, to prevent denormal-operand stalls on x86
inside WASM.

**Stability.** For `Q > 0` all RBJ filters above have poles strictly inside the
unit circle, so the filter is unconditionally stable. The Builder must still
assert `|a2| < 1` in a debug build and clamp `f0` to `(20, fn-20)` and `Q` to
`(0.0001, 100)` to avoid degenerate inputs.

**Complexity:** `O(1)` per sample, 5 multiplies + 4 adds. Memory `O(1)` per
voice (two state registers + 5 coefficients).

**Test:** for a lowpass at `f0 = fn/4`, `Q = 0.7071`, the magnitude response at
`f0` must be within 0.5 dB of -3 dB, and at `0.5*f0` within 0.5 dB of 0 dB, and
at `2*f0` must be <= -12 dB. Render 1e6 samples of an impulse; the output must
remain finite (`|y| < 1e3`).

---

## 7. Polyphony and voice management

### 7.1 Voice pool

Pre-allocate a fixed pool of `V` voices (`V = 16` is a comfortable, cheap
default; `V = 32` for a richer demo). Each voice holds:

```
struct Voice {
  int active;          // 0 = free, 1 = playing
  int note;            // MIDI note number (for note-off matching)
  double age_samples;  // for stealing
  Oscillator osc[OSC_PER_VOICE];   // OSC_PER_VOICE = 2 (detune pair)
  ADSR env;
  Biquad filter;
  double gain;         // per-voice level
}
```

### 7.2 Note on / note off

- **note-on(midi, velocity):** compute `f = 440 * 2^((midi-69)/12)`. If a free
  voice exists, allocate it; else **steal** the best candidate (see 7.3).
  Initialize oscillators (reset phase), set envelope to ATTACK with peak =
  `velocity/127`, store `note`.
- **note-off(midi):** find the active voice with matching `note`, set its
  envelope to RELEASE. (Mono/last-note priority is a later option; default is
  per-note polyphony.)

### 7.3 Voice stealing policy

When no free voice is available, steal according to a priority score. The
recommended default: **steal the voice with the smallest envelope gain**
(quietest is least audible) and, as a tiebreak, the oldest. This minimizes
audible artifacts. The policy is a single pluggable comparator; document it.

### 7.4 Mixing and master stage

Per sample, the output is:

```
mix = sum_{v active} voice_render(v)      // each voice already VCA-scaled
out = tanh(master_gain * mix)             // soft clip to keep within [-1,1]
```

`tanh` soft-clipping is cheap (one transcendental) and prevents wrap-around
distortion when many voices stack. If `V*peak` never exceeds 1, the `tanh` is
near-linear and inaudible; it only engages on overload.

**Complexity:** `O(V)` per sample, `O(N*V)` per block. With `V=16` and
`N=128` at `fs=48000` this is ~768k voice-samples/sec of trivial arithmetic:
comfortably real-time even interpreted in WASM. Memory `O(V)`.

---

## 8. Patch serialization format

A *patch* is the full set of synthesis parameters (oscillator types/waveforms,
detune, mix levels, filter type/cutoff/Q/gain, ADSR times/levels, polyphony
count, master gain). It must be (a) human-readable on Pages and (b) round-trippable.

### 8.1 Schema (JSON, versioned)

```json
{
  "schema": "resonata-patch",
  "version": 1,
  "master": { "gain": 0.8 },
  "polyphony": 16,
  "voices": [
    {
      "oscillators": [
        { "kind": "saw|square|sine|triangle|wavetable",
          "detuneCents": -7, "level": 0.6, "wavetable": "saw2048" },
        { "kind": "saw", "detuneCents": 7, "level": 0.6 }
      ],
      "filter": { "type": "lowpass", "cutoffHz": 8000, "q": 0.7, "gainDb": 0 },
      "adsr": { "attack": 0.01, "decay": 0.2, "sustain": 0.7, "release": 0.3 }
    }
  ]
}
```

The C side mirrors this with a `Patch` struct parsed by a minimal JSON reader
(the Builder may vendor a tiny parser; the spec forbids pulling a large
dependency into the WASM binary). A compact **binary** patch format (tagged
float32 fields) is optional for preset banks but JSON is the canonical,
Pages-readable form.

### 8.2 Parsing rules

- Unknown keys are ignored (forward compatibility).
- Missing keys fall back to documented defaults.
- `cutoffHz` is clamped to `(20, fn-20)`; `q` to `(0.0001, 100)`; gains to
  `[0, 2]`; ADSR times to `[0, 60]` seconds.
- On parse failure the engine keeps the previous valid patch and returns an
  error code (never a crash).

**Test:** serialize a default patch, parse it back, and assert byte-for-byte (or
field-for-field) equality of the re-serialized form; apply a patch and assert the
live coefficients (e.g. filter `b0`) changed accordingly.

---

## 9. WASM / C ABI boundary

Resonata compiles the C core with Emscripten to a `.wasm` plus a thin JS glue.
The exported surface should be minimal and state-explicit:

```
resonata_create(sample_rate)   -> handle (opaque pointer in wasm memory)
resonata_note_on(handle, midi, velocity)
resonata_note_off(handle, midi)
resonata_set_patch(handle, json_ptr, json_len)  -> status code
resonata_set_param(handle, id, value)           // live tweak, per block
resonata_render(handle, out_ptr, frames)        // fills float32 buffer
resonata_destroy(handle)
```

- `out_ptr` points into WASM linear memory; JS copies `frames` float32 samples
  into an `AudioWorklet` `Float32Array` (or a SharedArrayBuffer ring for
  lower latency). Recommend `AudioWorklet` over `ScriptProcessorNode` (deprecated).
- **No malloc on the render path.** The voice pool and all state are allocated
  once in `resonata_create`. `render` only reads/writes pre-allocated structs.
- Parameters changed by the UI are written into the engine state between
  `render` calls (per block), not per sample, to keep the hot loop tight.
- Everything deterministic and free of `clock()`/`rand()` on the hot path so the
  core is reproducible in tests (the C tests run the same functions natively,
  no browser needed).

---

## 10. Numerical precision and the testable core

The entire point of "core first" is a C library that is exercised by a native
test harness (Unity, or a hand-rolled `assert`-based runner) **before** any
WASM/UI work. Define the core as pure functions:

```
osc_step(Oscillator*, double freq, double fs) -> double
adsr_step(ADSR*) -> double
biquad_step(Biquad*, double x) -> double
voice_render(Voice*, double freq, double fs) -> double
```

Tests (the Builder's checklist, derived from this spec):

1. **Oscillator** - FFT peak location within +/-1 bin; PolyBLEP saw alias
   rejection >= 40 dB below `fn` at `f <= fn/4`.
2. **Wavetable** - matches analytic band-limited sum within 1e-3 RMS; no
   cross-table pop > 1e-2.
3. **ADSR** - attack 99% within `attack_time +/- 5%`; decay converges to
   `sustain` within 1e-3; release to <1e-3 within `release_time +/- 5%`.
4. **Biquad** - magnitude at `f0` within 0.5 dB of target for each filter type;
   impulse response finite over 1e6 samples; `|a2| < 1` asserted.
5. **Polyphony** - note-on allocates a voice, note-off frees it after release;
   stealing picks the quietest active voice.
6. **Patch** - JSON round-trip field equality; clamping enforced; bad JSON does
   not crash (returns error, keeps prior patch).
7. **End-to-end** - render a 0.5 s note and assert the RMS envelope follows the
   ADSR shape (rising, sustaining, falling) within tolerance.

Reference test sample rate: `fs = 48000`.

---

## 11. Complexity summary

| Component | Time / sample | Space / voice |
|---|---|---|
| Oscillator (phase + PolyBLEP) | O(1), ~10 flops | O(1) state |
| Wavetable read | O(1), ~3 flops | O(1) (tables shared) |
| ADSR | O(1), 1 mul + 1 add | O(1) state |
| Biquad (TDF2) | O(1), 5 mul + 4 add | 2 regs + 5 coeffs |
| Voice sum + master | O(V) | O(V) pool |
| Patch parse | O(tokens) one-off | O(patch) |

Per block of `N` frames: `O(N*V)` arithmetic, no allocation. Real-time budget at
`fs=48000`, `V=16`, `N=128`: roughly 6.1M voice-samples/sec of trivial ops,
well within a single core even under WASM's baseline JIT.

---

## 12. Stretch goal notes (WebUSB MIDI, non-blocking)

The core above is the shippable demo. WebUSB MIDI keyboard input is explicitly a
stretch goal and must NOT block the core. Design for it by keeping the
note-on/note-off API (`resonata_note_on/off`) transport-agnostic: a MIDI
handler in JS simply translates `0x90/0x80` messages into those calls. No
changes to the DSP core are required, which is the proof that the core boundary
was drawn correctly.

---

## 13. Handoff to the Architect

The algorithmic surface is now fixed. The Architect should produce:

- Module boundaries: `core/` (osc, adsr, biquad, wavetable, voice, patch,
  engine) as a standalone C library with a native test target; `wasm/` glue via
  Emscripten; `ui/` (the browser front end at `/resonata/index.html`).
- A build that compiles the core to a native test binary AND to WASM from the
  same sources.
- The exact `resonata_*` ABI in section 9.
- The static-hosting layout required by lab docs: entrypoint `/resonata/index.html`,
  fully client-side, no backend.

The Researcher's work is complete; the next action is `architect`.

- Dr. Mob, the Researcher
