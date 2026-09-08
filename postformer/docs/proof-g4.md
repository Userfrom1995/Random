# G4 Asymptotic Proof Appendix (M1 skeleton; Builder fills measured shapes)

Claim: every M1 arm (Transformer baseline, P1 Delta-Hybrid, P5 map control)
trains subquadratically and, except for the baseline KV cache by design,
generates with O(1) state and O(1) latency per token.

## M1 state inventory (per layer, batch B, bytes-per-element e)

| Arm | Tensor | Shape | Bytes |
|-----|--------|-------|-------|
| P1 | delta S (per layer) | (B, H, d_k, d_v) | B*H*d_k*d_v*e |
| P1 | window K ring + V ring | 2 x (B, W, H*hd_w) | 2*B*W*H*hd_w*e |
| P5 | map S (per layer) | (B, H, 2*d_k, d_v) | 2*B*H*d_k*d_v*e |
| P5 | window K ring + V ring | same as P1 | same as P1 |
| P2 | SSD S (per layer) | (B, H, d_k, d_v) | B*H*d_k*d_v*e |
| P2 | global slots K+V (capped at G) | G x (B, H, d_k) + G x (B, H, d_v) | G*B*H*(d_k+d_v)*e |
| P2 | window K ring + V ring | same as P1 | same as P1 |
| P3 | accumulator A + selective S | 2 x (B, H, d_k, d_v) | 2*B*H*d_k*d_v*e |
| P3 | window K ring + V ring | same as P1 | same as P1 |
| P4 | surprise-gated M (per layer) | (B, H, d_k, d_v) | B*H*d_k*d_v*e |
| P4 | window K ring + V ring | same as P1 | same as P1 |
| Base | KV cache (control) | 2 x (B, H, T, hd), grows with T | 2*B*T*d_model*e |

S-tiny P1 (H=4, d_k=d_v=128, W=128, win 4x64, e=4 fp32, B=1):
delta 4*128*128*4 = 262144 B; window 2*128*256*4 = 262144 B;
total/layer 524288 B; x6 layers = 3145728 B (~3.0 MB, flat in T).
S-small P1: 6*128*128*4 + 2*128*256*4 = 655360 B/layer;
x12 = 7864320 B (~7.5 MB).
Note: pre-2026-09-08 curves recorded 3145824 (tiny) / 7864608 (small)
including a 16 B/layer (tiny) / 24 B/layer (small) fusion-scalar
reservation with no backing tensor; the inventory above drops it and
state_size() matches exactly.
S-tiny baseline KV at T: 2*T*512*4*6 = 24576*T bytes (linear in T by design).

Chunk size C (64 tiny / 128 small) appears only in training chunking;
it never appears in the inference state.

## Per-token flop accounting (all constant in T)

- P1 delta step: one rank-1 retrieve/erase/write, O(H*d_k*d_v).
- P5 map step: one scaled additive outer product, O(H*2*d_k*d_v).
- Window/slot step: exact softmax over at most W keys, O(W*d_win).
- Fusion + SwiGLU: O(d_model) + O(d_model*mlp_hid).
- No scan over history appears in any update path.

## Empirical bar (latency_state.py, Pareto tiers per 2026-09-07 amendment)

Gate 4 passes in one of two tiers (binding amendment 2026-09-07, recorded
by the Maintainer on #294; strict-O(1)-only is superseded):

- Tier (a) full O(1): under 5% growth in state bytes AND median ms/token
  from T=1k to T=32k, batch 1, fixed precision, 200 decode steps after
  warmup, slope statistically zero.
- Tier (b) Pareto-dominance: state/latency sublinear (strictly
  subquadratic) AND dominating the baseline at every measured T, with
  G1+G2+G3 all green. Tier (b) is keep-worthy, not a rejection.

Hardware, dtype, torch/cuda versions are logged per row. M1 records smoke
points at small T on reference configs; the full 1k-32k curve is M2 work.

## M2 measured flatness (2026-09-07, CPU fp32, torch 2.14.0+cpu)

- p1-toy, timed `step()` path, decode-steps 50, warmup 10:
  T=1024/2048/4096/8192/16384/32768 -> ms 1.062/1.065/1.059/1.056/1.058/1.066
  (growth 0.4%, bar is <5%: PASS), bytes flat 24576 (PASS).
- p5-toy: T=1024 -> 1.051ms / 40960 B; T=32768 -> 1.053ms / 40960 B (PASS).
- transformer-toy control: T=1024/2048/4096 -> ms 2.067/6.491/15.96
  (superlinear, O(T) attention per step as designed), bytes 2M/4M/8M linear.
  8k+ points skipped on CPU (quadratic prefill); linearity is analytic.
- S-tiny analytic bytes (`state_bytes()` formula, no timing claim):
  baseline 25M/50M/101M/201M/403M/805M linear vs P1 flat 3145728 vs P5 flat
  4718592 at every T (P1 uses 256x less state than the baseline at 32k).
- Real bug caught by the gate: every `step()` path rebuilt the full RoPE
  table via `cos_sin(pos+1)` - O(T) work per token (p1-toy showed 16.3ms at
  32k pre-fix). Fixed with `RotaryEmbedding.row()` (byte-identical values,
  O(d)); T1 parity still green (11/11). Curves: `ledger/curves/m2-toy/
  g4_curve_{p1,transformer,p5}-toy_seed0.csv` + S-tiny `*_analytic.csv`.

## M3 state footprints (analytic `state_bytes()`, fp32, batch 1)

- S-tiny P2 (G=16): SSD 262144 + slots 16*4*256*4 = 65536 + window
  262144 = 589824 B/layer flat; x6 = 3538944 B (~3.37 MB, O(1)
  in T, byte-flat by construction, tier (a) PENDING timed ms/token curve).
- S-tiny P3: 2*262144 (A+S) + window 262144 = 786432 B/layer;
  x6 = 4718592 B (~4.5 MB) flat, byte-flat by construction,
  tier (a) PENDING timed ms/token curve.
- S-tiny P1/P5 reference: flat 3145728 / 4718592 B (see above).
- S-tiny P4 (H=4, d_k=d_v=128, W=128, win 4x64, e=4): fast weights
  262144 + window 262144 = 524288 B/layer; x6 = 3145728 B
  (~3.0 MB) flat, identical inventory to P1 by construction (the
  surprise proj and error gain are parameters, not state).
  Byte-flat by construction, tier (a) PENDING timed ms/token curve.
