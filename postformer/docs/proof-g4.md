# G4 Asymptotic Proof Appendix (M1 skeleton; Builder fills measured shapes)

Claim: every M1 arm (Transformer baseline, P1 Delta-Hybrid, P5 map control)
trains subquadratically and, except for the baseline KV cache by design,
generates with O(1) state and O(1) latency per token.

## M1 state inventory (per layer, batch B, bytes-per-element e)

| Arm | Tensor | Shape | Bytes |
|-----|--------|-------|-------|
| P1 | delta S (per layer) | (B, H, d_k, d_v) | B*H*d_k*d_v*e |
| P1 | window K ring + V ring | 2 x (B, W, H*hd_w) | 2*B*W*H*hd_w*e |
| P1 | fusion scalars | (B, H) | B*H*e |
| P5 | map S (per layer) | (B, H, 2*d_k, d_v) | 2*B*H*d_k*d_v*e |
| P5 | window K ring + V ring | same as P1 | same as P1 |
| Base | KV cache (control) | 2 x (B, H, T, hd), grows with T | 2*B*T*d_model*e |

S-tiny P1 (H=4, d_k=d_v=128, W=128, win 4x64, e=4 fp32, B=1):
delta 4*128*128*4 = 262144 B; window 2*128*256*4 = 262144 B; total/layer
524304 B; x6 layers = 3146256 B (~3.0 MB, flat in T).
S-small P1: 6*128*128*4 + 2*128*256*4 = 655360 B/layer; x12 = 7864320 B (~7.5 MB).
S-tiny baseline KV at T: 2*T*512*4*6 = 24576*T bytes (linear in T by design).

Chunk size C (64 tiny / 128 small) appears only in training chunking;
it never appears in the inference state.

## Per-token flop accounting (all constant in T)

- P1 delta step: one rank-1 retrieve/erase/write, O(H*d_k*d_v).
- P5 map step: one scaled additive outer product, O(H*2*d_k*d_v).
- Window/slot step: exact softmax over at most W keys, O(W*d_win).
- Fusion + SwiGLU: O(d_model) + O(d_model*mlp_hid).
- No scan over history appears in any update path.

## Empirical bar (latency_state.py)

Flat = under 5% growth in state bytes AND median ms/token from T=1k to
T=32k, batch 1, fixed precision, 200 decode steps after warmup. Hardware,
dtype, torch/cuda versions are logged per row. M1 records smoke points at
small T on reference configs; the full 1k-32k curve is M2 work.
