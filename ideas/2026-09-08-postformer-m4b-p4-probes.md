# PostFormer M4b: P4-vs-P1 toy falsification + A6/A7 at toy (2026-09-08)

## Protocol (matched, mirrors M3)

- One arm: `p4-toy`, seed0, 1000 steps x batch16 = 0.528M tokens, vocab64/N8,
  lr 3e-4, CPU fp32. Data RNG keyed by (seed, data), so the episode stream is
  identical to the M3 p1-W16-1000 ref and the p2/p3 probes at the same seed.
- Train command:
  `train --model p4-toy --data mqar --vocab 64 --n-pairs 8 --steps 1000
  --batch 16 --lr 3e-4 --seed 0 --out /tmp/m4b-p4`
  (loss 4.3195 to 4.1157, finite; checkpoint NOT committed, regenerable).
- Eval (full G1 toy envelope, 100 eps):
  `synthetic_recall --model p4-toy --checkpoint ... --vocab 64
  --n-pairs "8,16" --episodes 100 --gap 16 --copy-len 32 --seed 0`
- Curves: `postformer/ledger/curves/m4b-toy/` (train summary+curve, G1 summary,
  N8/N16/induction/copy/2hop CSVs). Ledger: 19 rows, `check` green.

## Results (H4 first read: NEGATIVE at toy)

- p4-toy: mqar8 **0.035**, N16 0.015625 (= chance 1/64), 2hop 0.01,
  induction gap16 0.0, copy L32 0.0.
- Matched refs (same budget/seed): p1-W16-1000 **0.0625**, p2-G16 0.0825,
  p3 0.0600. So surprise gating underperforms plain delta (-2.75 pts vs P1)
  and slots (+4.75 pts gap to P2) at toy N8.
- H4 verdict: NEGATIVE at the toy envelope (single seed, N8, 0.528M tokens).
  Not a rejection of MAG-lite at scale: toy N8 with 1000 steps is a weak
  discriminator (all arms < 0.09), and the surprise gate's error-gain path may
  need longer training or larger N to separate from the delta baseline.
  Recorded honestly; H4 stays open pending S-tiny N64+ (GPU).
- A6 (vocab/distractor stress at toy): N16 extrapolation collapses to chance
  for p4 (0.0156), same as every other toy arm (P1 0.039/P5 0.000/T 0.091 at
  M2b 3000-step; M3 refs unmeasured at N16). No arm generalizes N8-trained recall to N16
  distractors at toy scale.
- A7 (retrieval-vs-drift split): trained retrieval (mqar8 0.035) >
  compositional retrieval (2hop 0.01) > untrained transfer (induction/copy 0.0).
  MQAR-only training does not transfer, as expected; the split is documented
  for the S-tiny text-trained gate where drift (G2/G3) becomes measurable.

## What remains (GPU-blocked)

- S-tiny/S-small full gates G1+G2+G3+G4-tier-a/b (3 arms x 3 seeds, ~50+h/arm
  on CPU per 2026-09-08 smoke); A3/A4/A5 at S-tiny; H1-H5 verdicts at scale;
  viewer Playwright snapshot; envelope audit; `Closes #294` only on full pass.

- the Builder
