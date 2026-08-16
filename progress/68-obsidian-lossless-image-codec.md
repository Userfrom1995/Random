# Progress - Obsidian (lossless image codec)

- **Issue:** #68
- **Branch:** opencode/issue68-20260816082105
- **Status:** in-progress
- **Updated:** 2026-08-16T08:25:00Z

## Checklist
- [x] Research phase: literature review, SOTA survey, algorithmic spec, benchmark methodology
- [x] obsidian/docs/ (research.md, algorithmic-spec.md, benchmark-methodology.md)
- [x] ideas/ entry for the project
- [x] Architect: software architecture from the spec (docs/architecture.md)
- [ ] 1. Scaffolding: Cargo workspace (core/cli/web), PPM P6 I/O, container header + CRC, CLI skeleton
- [ ] 2. Color transforms: YCoCg-R + palette, bijection unit tests
- [ ] 3. Predictor bank (8 predictors) + border handling + per-context predictor map (analysis pass)
- [ ] 4. Context model: gradient quantization, sign symmetry, activity class, border contexts, zigzag map
- [ ] 5. rANS: adaptive (12-bit) + static tables, renorm guard, stream finalization, property tests
- [ ] 6. Effort levels 0-7 wiring, decode path complete, effort 0 end-to-end first
- [ ] 7. Fidelity gates: bit-exact round trips (Kodak + fuzz) at every effort
- [ ] 8. Benchmark harness: run_kodak.sh, fuzz_gate.sh, aggregate.py, toolchain.md + reference baseline
- [ ] 9. M1: beat WebP lossless + optipng PNG on Kodak
- [ ] 10. M2: self-correcting weighted predictor (v1.5), within 10% of JPEG XL
- [ ] 11. M3: squeeze/interlacing or improved context model, ~3% of or above JPEG XL
- [ ] 12. Web specimen page + wasm bindings + Playwright verification
- [ ] 13. Docs: README, architecture reference, benchmark tables

## Current step
Architecture phase complete. The blueprint in `obsidian/docs/architecture.md`
defines the Cargo workspace (obsidian-core std-only library, obsidian-cli,
obsidian-web + specimen page), module responsibilities, public API, data
structures (12-bit freq/cum/slot rANS tables, <= 256 active contexts/plane),
effort-level pipeline, test matrix, and the Builder milestone mapping. Ready
for the Builder to scaffold and implement effort 0 end-to-end.

## Next steps
- Builder: scaffold the Cargo workspace, PPM I/O, container header + CRC, and
  the CLI skeleton; implement color transforms and the predictor/context/rANS
  stack bottom-up (effort 0 first); run the fidelity gates; compute the
  reference baseline and the first Obsidian Kodak row.
- Reviewer / Tester: quality gate, dynamic round-trip + benchmark + specimen
  page verification.

## Agent log
- 2026-08-16T08:25:00Z (Researcher) - Literature review and SOTA survey on
  Kodak lossless rates (PNG, JPEG-LS, WebP, FLIF, JPEG XL, MRP). Authored the
  v1 algorithmic spec (reversible color transform, predictor bank with
  per-context selection, gradient+activity contexts, adaptive rANS, effort
  levels, complexity, fidelity gate) and the benchmark methodology. Committed
  `obsidian/docs/*`, `ideas/2026-08-16-obsidian-lossless-image-codec.md`,
  progress file; wrote the architect decision.
- 2026-08-16T09:05:00Z (Architect) - Designed the v1 architecture from the
  spec: Cargo workspace (obsidian-core std-only codec library, obsidian-cli,
  obsidian-web + interactive specimen page), module breakdown with interface
  contracts, data structures and memory budget, effort-level pipeline, test
  matrix, and the Builder milestone mapping. Committed
  `obsidian/docs/architecture.md`, ideas entry architecture section, progress
  file update, README status update; wrote the build decision.

- Dr. Ada, the Researcher
- the Architect