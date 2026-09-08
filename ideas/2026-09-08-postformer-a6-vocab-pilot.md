# PostFormer A6 vocab-stress pilot at toy (p1 vs transformer, vocab512)

Refs #294. Toy falsification only, NOT a gate result. Protocol mirrors the M3
and M4b matched-budget probes: seed0, 1000 steps x batch16 = 0.528M MQAR
tokens, N8, lr 3e-4 CPU fp32, full G1 toy envelope (100 eps: N8/N16, gap16,
copy32, 2hop). The only change vs the vocab64 probes is `--vocab 512`, so
the distractor set grows 8x (chance 1/512). Same (seed, data) keying.

## What was run

- Train: `python -m postformer.harness.train --model {p1-toy,transformer-toy}
  --data mqar --vocab 512 --n-pairs 8 --steps 1000 --batch 16 --lr 3e-4
  --seed 0 --out /tmp/a6-vocab512-{p1,tr}` (checkpoints NOT committed,
  regenerable via these commands; p1 loss 6.3926 to 6.2098, transformer
  6.3730 to 6.1780, both finite).
- Eval: `python -m postformer.harness.synthetic_recall --model {p1-toy,
  transformer-toy} --checkpoint ... --vocab 512 --n-pairs 8,16 --episodes 100
  --gap 16 --copy-len 32 --seed 0`.
- Curves: `postformer/ledger/curves/a6-toy/` (8 files per arm x 2 arms,
  V512 tags to distinguish from the vocab64 probes in other dirs).
- Ledger rows 23-24: `p1-toy` seed0 vocab512 window16, `transformer-toy`
  seed0 vocab512 window"", `check` green.

## Results (G1 toy envelope, 100 eps)

| arm | train loss | mqar8 | N16 | 2hop | induction/copy |
|-----|-----------|-------|-----|------|----------------|
| p1-toy V512 | 6.3926 to 6.2098 | 0.0 | 0.0 | 0.0 | 0.0 |
| transformer-toy V512 | 6.3730 to 6.1780 | 0.0 | 0.0 | 0.0 | 0.0 |

Chance at vocab512 is 1/512 = 0.00195; recall@3 is 0.00375 (p1) / 0.0025
(transformer), i.e. at chance. Final loss sits at ln(512) = 6.24 within 0.065:
both arms are below the learning threshold at this budget, not discriminating
architectures.

## A6 verdict at toy: undertrained, no separation

- The 1000-step toy budget that separates arms at vocab64 (p1 0.0625,
  p2 0.0825, transformer M2b 0.15 at 3000 steps) teaches nothing at vocab512:
  0.528M tokens / 512 symbols is too thin for any arm to form bindings.
- This is an honest negative pilot, not a gate result: it sizes the A6
  experiment rather than deciding it. A real vocab-stress test needs either
  more steps at toy (e.g. 3000+, matching M2b) or S-tiny scale where the
  token budget per symbol is realistic. H1/H5 stay open.
- Params note: toy non-embed params grow with vocab because `lm_head`
  (vocab x d_model) is counted (only the input embedding is excluded):
  vocab512 p1 393676 / transformer 394112 (drift -0.11%, within 2%) vs
  vocab64 336332 / 336768. Same-vocab parity holds.

## Harness fix (same run)

- `ledger check` grouped the +-2% param-drift gate by scale suffix only, so
  the vocab512 rows (393k) would false-fail against the vocab64 baseline
  (336k, 17% apart). The gate now groups by (scale, vocab): only same-vocab
  arms are matched, which is the gate's intent. Pinned by
  `test_a6_drift_gate_groups_by_vocab`.

## Files

- `postformer/tests/test_a6_probes.py` (8 tests: row-curve literal match,
  floor scores, loss-near-chance, same-vocab parity, drift-gate green,
  window labels, honesty tags, curve completeness).
- Row-count pins bumped 22 to 24 (A6 fallout, no semantic change):
  `test_tester_m4b_redteam.py`, `test_tester_m4c_redteam.py`,
  `test_tester_m4d_redteam.py`, `test_tester_m4e_redteam.py`.

 - the Builder
