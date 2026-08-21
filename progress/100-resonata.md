# Progress - Resonata (real-time WASM synthesizer)

- **Issue:** #100
- **Branch:** opencode/issue100-20260821065856
- **Status:** in-progress (Architect blueprint delivered 2026-08-21; handed to Builder via `build`)
- **Research:** Dr. Mob's DSP spec at `docs/resonata-research-spec.md` (PR #101, closes #100).

## Checklist

- [x] Research phase: algorithmic/DSP spec (oscillators + PolyBLEP, wavetable mipmapping, exponential ADSR, RBJ biquad TDF2, voice-stealing polyphony, versioned JSON patch, WASM/C ABI, complexity bounds, native-testable core).
- [x] Architect blueprint: `ideas/2026-08-21-resonata.md` (module boundaries `core/` `wasm/` `ui/` `test/`, the exact `resonata_*` ABI + `ResonataParam` enum, data-structure contracts, `make test`/`make wasm` pipeline from one `core/`, UI wiring, Pages layout at `/resonata/index.html`, 7-item test matrix).
- [ ] 1. Scaffolding: `resonata/` tree, `Makefile`, `core/resonata.h` public ABI, default patch (`ui/default-patch.json`).
- [ ] 2. Oscillator (`core/osc.c`): phase accumulator, naive sine/saw/square/triangle, PolyBLEP anti-aliasing for saw/square, `osc_step(Oscillator*, f, fs) -> double`.
- [ ] 3. Wavetable (`core/wavetable.c`): generate `M=10` x `L=2048` mipmapped band-limited tables at `f0=20`, interpolated read with octave select + optional crossfade.
- [ ] 4. ADSR (`core/adsr.c`): exponential segment state machine, cached lambdas, fast-release guard, `adsr_step(ADSR*) -> double`.
- [ ] 5. Biquad (`core/biquad.c`): RBJ cookbook coefficient builder for all 8 filter types, transposed Direct Form II step with denormal protection + `|a2|<1` debug assert.
- [ ] 6. Voice (`core/voice.c`): osc pair -> mixer -> filter -> VCA, `voice_render(Voice*, f, fs) -> double`.
- [ ] 7. Patch + JSON (`core/patch.c`, `core/json.c`): `Patch` struct, minimal recursive-descent JSON reader/serializer, clamping, tolerant parse, `resonata_set_patch` returns error without crashing.
- [ ] 8. Engine (`core/engine.c`): `resonata_create/destroy/note_on/note_off/set_param/render`; fixed voice pool `V=16`, steal quietest+oldest, `tanh` master soft-clip, block size `N=128`, no hot-path allocation.
- [ ] 9. WASM (`wasm/exports.c` + `make wasm`): `STANDALONE_WASM=1` build exporting the 7 functions + `malloc`/`free`; `ui/resonata.wasm` instantiable directly inside the worklet.
- [ ] 10. UI (`ui/`): `index.html` at `/resonata/`, `resonata.js` glue, `worklet.js` AudioWorkletProcessor owning the wasm engine and rendering per block, `main.js` controls + piano + scope, `styles.css`, patch load/save.
- [ ] 11. Tests (`test/`): `fft.c` + `test_harness.h` + `test_osc/wavetable/adsr/biquad/poly/patch/e2e.c` covering the 7 matrix items; `make test` green at `fs=48000`.
- [ ] 12. Docs: `resonata/README.md` quick-start + ABI contract; verify `/resonata/` serves on Pages with correct `application/wasm` MIME.
- [ ] 13. Tester verification: load page, key press produces tone, scope animates, filter/ADSR sliders audibly change timbre, saved patch reloads byte-for-byte.

## Current step

Blueprint complete. Builder to scaffold the `resonata/` tree and implement the core
DSP library (`core/`), then the native test suite, then the WASM build and UI.

- the Architect
