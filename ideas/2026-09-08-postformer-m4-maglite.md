# PostFormer M4a: P4 MAG-lite (surprise-gated fast weights)

Date: 2026-09-08. Issue: #294. PR #295 (`opencode/issue294-20260907194528`).
Status: code + tests green on CPU; toy smoke only; NOT a gate result.

## What was built

- `postformer/models/p4_maglite.py`: per-block surprise-gated delta memory
  (`M = alpha*(M + beta*sigmoid(w_s(x)+g*||e||)*k*e^T)`, `e = v - M^T k`)
  plus the exact W-window branch reused from P1, 2-way fusion, SwiGLU.
  `P4LM` exposes the binding interface (`forward`/`step`/`init_state`/
  `state_bytes`/`state_size`); state inventory equals P1
  (`H*d_k*d_v + 2*W*d_win + H`, proof-g4.md updated).
- Factory: `p4-toy/tiny/small` with hid pins toy 294 / tiny 1702 /
  small 2724 (one extra surprise proj `d x H` plus per-head error gain
  over P1, compensated by trimming 2 hid units). Measured parity:
  toy -0.43%, tiny +0.003%, small +0.002% (all inside 2%).
- `tests/test_p4.py` (4 tests): surprise gate bounds, error-gain/trunk
  grads present after backward, step-vs-forward equivalence (1e-4) plus
  prefix invariance (1e-6), P4/P1 `state_bytes` equality and T-flatness.
  `test_params.py` now covers p4; conftest FAMILIES includes p4 so the
  shared T1/T2/T3 suites auto-extend.
- Docs: README parity pins + P4 smoke command + layout; proof-g4.md P4
  inventory row + S-tiny footprint (524304 B/layer, 3145824 B total).

## Verification (torch 2.14 CPU, this run)

- `pytest postformer/tests/ -q`: 48 passed (44 prior + 4 new P4).
- Parity re-measured at all three scales (above), all inside 2%.
- Smoke: `train --model p4-toy --steps 100` finishes (loss 4.32 to 4.30,
  finite), checkpoint loads, `synthetic_recall` eval writes a summary
  (N8 acc 0.025 at 100 steps, chance-level as expected for a smoke).

## Why this design

The blueprint gates P4 (most complex loop) behind P1/P2 numbers and
defines H4 as tie-P1-on-recall plus beat-P1-on-drift. A full Titans
inner-loop optimizer would break the G4 latency budget and the CPU
test budget, so M4a ships an honest single-step MAG-lite: the write is
a delta-rule gradient step whose size is modulated by the live
reconstruction error (surprise). Same shapes as P1, one extra proj,
identical state - so A-comparisons vary one mechanism at a time.

## Next (M4b, still on this PR)

- Toy falsification: matched-budget P4 vs P1 probes (seed0 1000-step
  MQAR, fixed loader) + H4 first read; A6 vocab sweep + A7 split at toy.
- S-tiny full gates for all six families (GPU runner required).
- Viewer Playwright snapshot; envelope audit; `Closes #294` only when
  G1+G2+G3+G4-tier-a/b pass head-to-head.

Refs #294.

- the Builder
