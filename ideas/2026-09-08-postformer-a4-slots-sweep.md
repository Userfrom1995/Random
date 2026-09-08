# PostFormer A4 slots sweep at toy (P2 G0/G4/G64)

Refs #294. Toy falsification only, NOT a gate result. Protocol mirrors the M3
and M4b matched-budget probes: seed0, 1000 steps x batch16 = 0.528M MQAR
tokens, vocab64/N8, lr 3e-4 fp32 (train + G1 eval on CUDA cu130 per the
`a4-toy` summaries, not CPU). Same (seed, data) keying, so the episode
stream is identical to the M3 p2-G16 probe and the M4b p4 probe; init is keyed
per (seed, model, data) with model string `p2-toy` for all three arms, so G0
differs from G4/G64 by slot count alone.

## What was run

- Train: `python -m postformer.harness.train --model p2-toy --data mqar
  --vocab 64 --n-pairs 8 --steps 1000 --batch 16 --lr 3e-4 --seed 0
  --slots {0,4,64} --out /tmp/a4-G{0,4,64}` (checkpoints NOT committed,
  regenerable via these commands).
- Eval: `python -m postformer.harness.synthetic_recall --model p2-toy
  --checkpoint /tmp/a4-G{G}/checkpoint.pt --vocab 64 --n-pairs 8,16
  --episodes 100 --gap 16 --copy-len 32 --seed 0` (eval loader inherits slots
  from the checkpoint config; no override flags needed).
- Curves: `postformer/ledger/curves/a4-toy/` (8 files per arm x 3 arms).
- Ledger rows 20-22: `p2-toy` slots 0/4/64 (seed0, 0.528M tokens each),
  `check` green. Ledger model names are valid `--model` values; replay via
  `train --model p2-toy --slots {0,4,64}` (slots column disambiguates).

## Results (G1 toy envelope, 100 eps)

| arm | train loss | mqar8 | N16 | 2hop | induction/copy |
|-----|-----------|-------|-----|------|----------------|
| p2-G0 (pure SSD) | 4.0436 | 0.04625 | 0.005625 | 0.01 | 0.0 |
| p2-G4 | 3.9427 | 0.0825 | 0.00125 | 0.03 | 0.0 |
| p2-G64 | 3.9427 | 0.0825 | 0.00125 | 0.03 | 0.0 |
| M3 p2-G16 ref | - | 0.0825 | - | 0.03 | - |
| matched p1-W16-1000 ref | - | 0.0625 | - | - | - |

## A4 verdict at toy: slots help, slot COUNT untested

- Slots help over pure SSD: G4 beats G0 by +3.6pts mqar8 (0.0825 vs
  0.04625) and 3x on 2-hop (0.03 vs 0.01) at identical params (336074,
  zero router params by construction) and identical data. G0 also sits below
  the matched P1 ref (0.0625).
- Slot-count ceiling: G4 and G64 collapse to bit-identical scores
  (A4-internal train loss equal to 16 digits, all G1 cells equal). Mechanism: toy MQAR
  episodes are T=33 tokens with slot stride 8, so at most 5 slot writes ever
  occur; any G >= 5 holds the full write history and behaves identically.
  Slot COUNT therefore stays untested until S-tiny N64+ (T_train 512), where
  write counts exceed small-G capacity and eviction actually fires.
- H2 stays open pending S-tiny scale. A4 at toy is a partial pass: existence
  of slot benefit confirmed, capacity scaling not yet probed.

## Files

- `postformer/tests/test_a4_probes.py` (7 tests: row-curve literal match,
  expected scores, G4/G64 identity, param identity across G0/G4/G16/G64,
  train/eval slots agreement, honesty tags, curve completeness).
- `postformer/tests/test_tester_m4b_redteam.py`: row-count pin 19 -> 22
  (A4 fallout, no semantic change).

 - the Builder
