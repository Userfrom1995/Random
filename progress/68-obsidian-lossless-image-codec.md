# Progress - Obsidian (lossless image codec)

- **Issue:** #68
- **Branch:** opencode/issue68-20260816082105
- **Status:** in-progress
- **Updated:** 2026-08-16T08:25:00Z

## Checklist
- [x] Research phase: literature review, SOTA survey, algorithmic spec, benchmark methodology
- [x] obsidian/docs/ (research.md, algorithmic-spec.md, benchmark-methodology.md)
- [x] ideas/ entry for the project
- [ ] Architect: software architecture from the spec
- [ ] Builder: v1 encoder/decoder + benchmark harness
- [ ] Baseline benchmark table on Kodak (pinned toolchain)
- [ ] Fidelity gate: bit-exact round trips (Kodak + fuzz)
- [ ] M1: beat WebP lossless + optipng PNG on Kodak
- [ ] M2: within 10% of JPEG XL lossless (effort 7)
- [ ] M3: within ~3% of or above JPEG XL lossless

## Current step
Research phase complete. Handing the algorithmic specification to the
Architect (`/oc architect`). The spec defines: container layout, YCoCg-R
reversible color transform, predictor bank with per-context predictor map,
gradient + activity context model, adaptive rANS (12-bit tables), effort
levels, O(n) complexity, and fidelity guarantees. The benchmark protocol
pins the toolchain and the Kodak procedure.

## Next steps
- Architect: read `obsidian/docs/algorithmic-spec.md` and `research.md`,
  design the module layout (encoder/decoder/benchmark CLI), branch/PR.
- Builder: implement v1, run the fidelity gate, compute the reference
  baseline and the first Obsidian Kodak row.
- Reviewer / Tester: quality gate, dynamic round-trip + benchmark verification.

## Agent log
- 2026-08-16T08:25:00Z (Researcher) - Literature review and SOTA survey on
  Kodak lossless rates (PNG, JPEG-LS, WebP, FLIF, JPEG XL, MRP). Authored the
  v1 algorithmic spec (reversible color transform, predictor bank with
  per-context selection, gradient+activity contexts, adaptive rANS, effort
  levels, complexity, fidelity gate) and the benchmark methodology. Committed
  `obsidian/docs/*`, `ideas/2026-08-16-obsidian-lossless-image-codec.md`,
  progress file; wrote the architect decision.

- Dr. Ada, the Researcher