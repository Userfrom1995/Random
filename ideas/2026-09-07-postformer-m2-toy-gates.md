# PostFormer M2: Toy Falsification with Matched Budgets (plus a Real G4 Win)

Date: 2026-09-07. Issue: #294. Branch: `opencode/issue294-20260907194528` (PR #295, shared across M1-M4). Status: M2-toy complete, `Refs #294` (S-tiny trained gates deferred to a GPU runner; H1/H5 unresolved at toy envelope).

## What was built (M2 on top of M1)

- `postformer/harness/train.py`: matched-budget trainer (AdamW 0.9/0.95, wd 0.1, clip 1.0, cosine + warmup, MQAR/Markov data mirroring the G1 generator, checkpoint + `train_curve.csv` + `train_summary.json` outputs). Full CLI contract in `postformer/README.md`.
- Toy scale pinned in `models/baseline.py` + `models/factory.py`: `transformer-toy` (2L d128 4h mlp256, 336768 non-embed) vs `p1/p5-toy` (2L d128, 2 delta/map heads dk32/dv32, W16, C16, win 2x16, mlp296, 336332, -0.13%). T2 param test extended to toy/tiny/small.
- A2 switch: `SlidingWindowAttn` with `window<=0` returns zeros (fusion learns to ignore it); `state_size` excludes the rings. Param count is W-invariant (336332 at W=0/16/32), so A2 varies only the mechanism.
- T6 `postformer/tests/test_stability.py`: beta in [0.01,0.99], alpha in (0,1), beta*||k||^2 worst 0.99 (< 2.0 required), collinear outputs finite. Suite now 11 passed (T1-T6).
- `harness/ledger.py plot` recurses milestone subdirs and relabels analytic series, so M1 smoke + M2 toy curves share one scoreboard.

## Measured numbers (matched budget: vocab64/N8, 3000 steps x batch16 = 1.584M tokens/arm/seed, lr 3e-4, CPU fp32, seeds 0/1/2; G1 toy envelope 200 eps)

- MQAR N8 (train N): P5 0.300 / P1 0.287 / Transformer 0.146 (chance 0.016). Recurrent arms learn the binding task ~2x better than attention at matched toy budget.
- A1 (delta vs additive = P1 vs P5): NO delta advantage at toy N8 (P5 leads by 1.3pts, within noise across seeds). The erase hypothesis H1 is NOT confirmed here - but N=8 with d_v=32 is far below the bound regime (H1 predicts separation at N=256). Honest verdict: unresolved, needs S-tiny.
- N16 extrapolation: all collapse (P1 0.039, P5 0.000, T 0.091). Nobody extrapolates 2x past train N at toy scale - consistent with the O(d) capacity bound, and a useful negative result.
- 2-hop: P5 0.53 / P1 0.46 / T 0.12. Recurrent memories compose chained bindings far better than the toy transformer.
- Induction/copy: chance (MQAR-only training does not transfer - expected, documented).
- A2 W{0,16,32} seed0: N8 0.275/0.287/0.251 - no collapse at W0, so the window is not doing the binding work at N8. A real A2 test needs S-tiny N64+.
- H5 (degree-2 map): P5 beats transformer at N8 (+15pts) but trails-vs-leads P1 by only ~1pt, not the predicted >=15pt P1 lead. Unresolved at toy envelope.
- G4 (the real win): the 1k-32k curve exposed an O(T)-per-step RoPE table rebuild (`cos_sin(pos+1)` per step) in ALL step paths - 16.3ms at 32k pre-fix. Fixed with `RotaryEmbedding.row()` (identical values, O(d)); T1 parity still green. Post-fix: P1 1.06ms flat (<1% growth 1k-32k, bytes flat 24592), P5 1.05ms flat (bytes 40976), control 2.07/6.49/15.96ms at 1k/2k/4k with linear bytes. S-tiny analytic: baseline 25M-805M linear vs P1 flat 3.15M (256x less at 32k).
- G2 OOD probe (NOT a gate measurement - ledger cells left empty): MQAR-trained arms on uniform streams all explode; P1 degrades least (8x +6.0 vs T +10.8). Real G2 needs LM-trained arms.

## Ledger and reproducibility

- `postformer/ledger/ledger.csv`: 15 rows (4 M1 + 9 toy + 2 A2 as `p1-W0/W32-toy`), `check` green, N8 headline in `notes` (schema pins 16/64/256; toy N16 fills `g1_mqar_16` as a harsh extrapolation point).
- 99 curve files under `postformer/ledger/curves/m2-toy/` (train curves/summaries, G1 summaries + per-query CSVs, G2 OOD probe, G4 timed + S-tiny analytic).
- Checkpoints (11 x ~1.4MB) NOT committed; regenerate bit-identically on CPU via the README command + seed (fix `OMP_NUM_THREADS`; thread scheduling is the only nondeterminism outside `seed_all`).

## Why these choices

- Toy-first instead of S-tiny: ~25M-param x 3 arms x 3 seeds training is hours on CPU and would have blown the run budget with zero results; the toy matrix (2 min/arm) buys real falsification signal plus the G4 bug catch now, while `train.py` already supports tiny/small presets for a GPU `continue`.
- G2/G3 gate cells left EMPTY rather than filled with OOD/fixture numbers: the ledger lint cannot distinguish, so discipline has to live in the Builder. Negative space in the ledger is a result too.
- Single-PR discipline kept: everything on PR #295 as `Refs #294`; `Closes #294` only when G1+G2+G3+G4 pass at gate scale.

## Next (M2-S-tiny on GPU, then M3)

`continue` on PR #295: (1) train S-tiny 3 arms x 3 seeds on GPU, run full G1 (N16/64/256) + G2 text + A1/A2 at gate scale, ledger H1/H5 verdicts; (2) M3 P3/P2; (3) Playwright viewer snapshot; (4) M4 envelope audit.

- the Builder
