# Post-Transformer Sequence Architecture: Delta-Hybrid Blueprint (Architect)

Date: 2026-09-07. Issue: #294. Research input: `docs/research/issue-294-post-transformer-sequence-architecture.md` (binding: SSM plus linear-attention plus recall-gap synthesis, S-tiny 30M and S-small 150M baseline contract within 2 percent params, four-gate methodology G1-G4, O(1) proof sketch, proposals P1-P5 ranked, ablations A1-A7, merge discipline Refs #294 until all gates pass). This blueprint resolves every handoff item in research section 9 into solution layout, pinned choices, interfaces, build order, and acceptance gates.

## Summary

PostFormer is a causal O(T)-train, O(1)-state sequence modeling program in Python plus PyTorch that tests whether key-structured forgetting closes the associative recall gap to Transformers. The core bet (P1 Delta-Hybrid) pairs a gated delta-rule fast-weight memory (content-addressed erase plus write) with a short exact sliding window (local induction) fused per layer, followed by SwiGLU. Controls and challengers stage behind it: P5 higher-order map (ablation control), P3 decoupled accumulator branch, P2 SSD plus sparse global slots, P4 Titans MAG-lite (gated behind ledgered P1/P2 results). A reproducible harness evaluates all arms head-to-head against a pinned causal Transformer baseline under matched params, tokens, optimizer, tokenizer, and protocol across four binding gates (G1 recall, G2 length, G3 Enwik8 BPB, G4 O(1) footprint). A static viewer renders the ledger as a scoreboard. One branch and one PR carry the whole technique across continuous `continue` cycles: M1 scaffolds harness plus baseline plus P5 plus P1-minimal, M2 gates S-tiny, M3 adds P3 and P2, M4 attempts P4 and the full envelope audit. `Closes #294` only on all four gates passing with reproducible numbers.

## Deliverables (what the Builder ships across continue cycles on this PR)

- `postformer/` project root (no repo-root pollution, no landing-page change):
  - `postformer/models/baseline.py`: causal decoder-only Transformer (pre-norm RMSNorm, SwiGLU, RoPE, no bias, pinned configs S-tiny and S-small).
  - `postformer/models/p1_delta_hybrid.py`: gated delta memory plus W-window attention plus fusion plus SwiGLU (minimal first, full in M2).
  - `postformer/models/p5_map.py`: gated linear attention with degree-2 map, no delta rule (ablation control).
  - `postformer/models/p3_decoupled.py`: accumulator plus selective-decay plus window branches with gating (M3).
  - `postformer/models/p2_slots.py`: SSD backbone plus G-slot exact attention plus gating (M3).
  - `postformer/models/p4_maglite.py`: W-window short attention plus fast-weight MLP long memory plus surprise gating (M4 only).
  - `postformer/models/common.py`: RMSNorm, SwiGLU, RoPE, KV window buffer, param counter, deterministic init helpers.
  - `postformer/harness/synthetic_recall.py`, `length_sweep.py`, `enwik8_bpb.py`, `latency_state.py`, `ledger.py`: exact CLI contracts below, greedy scoring, fixed seeds.
  - `postformer/ledger/ledger.csv` plus `plots/`: append-only empirical ledger, every version one row per model per seed, negative results committed.
  - `postformer/viewer/index.html`: single-file static scoreboard (vanilla JS, inline SVG, no CDN, file plus fetch load) reading `ledger.csv` and curve CSVs.
  - `postformer/docs/proof-g4.md`: asymptotic-proof appendix skeleton (state inventory table plus per-token flop accounting, Builder fills measured shapes).
  - `postformer/tests/`: unit plus parity tests (chunked vs recurrent, param parity, determinism, window masking, ledger schema).
  - `postformer/README.md`: setup, train commands, eval commands, envelope statement, hardware and dtype log.
- `ideas/2026-09-07-post-transformer-sequence-architecture.md`: this blueprint.
- `progress/294-post-transformer-sequence-architecture.md`: milestone roadmap M1-M4, status in-progress, current step, next steps, dated agent log.
- All intermediate pushes use `Refs #294`. `Closes #294` only when G1+G2+G3+G4 all pass head-to-head with reproducible numbers inside the tested envelope.

## Why

Attention keeps every pairwise comparison explicit so recall is retrieval, while linear recurrences compress history into a fixed sketch so recall is reconstruction under a `d = Omega(N)` bit bound. Scalar selectivity (Mamba `dt`, GLA gates, RetNet decay) learns when to remember but erases all keys at once, so interleaved bindings collide. The research finding is that only key-structured removal (delta rule `M = M + beta (v - M k) k^T`, equivalently `M = (I - beta k k^T) M + beta v k^T`), bounded exact slots, or exact windowed attention restores what to forget. P1 is ranked first because Grazzi et al. show the delta rule solves MQAR at `d = O(D_key)` where diagonal Mamba needs `Omega(N)`; the W=128 window offloads exact local induction (Based recipe) so fast weights focus on long bindings. P5 isolates how much comes from feature geometry vs erase (A1). P3 tests whether a cheap decay-free accumulator extends copying without erase. P2 tests whether G exact slots recover bindings with 10 percent of KV bytes. P4 tests whether gradient-based memory extrapolates better at 8x. The milestone order (P5 plus P1 first, then P3, then P2, then P4) spends the cheapest falsification first and gates the most complex training loop (P4) behind real P1/P2 numbers.

## How It Works

1. Train: pick scale (S-tiny synthetic or S-small text), build baseline and candidate with the param counter inside 2 percent, train with identical tokens, steps, batch, AdamW cosine schedule, and seeds. Delta and SSD arms train chunkwise (fixed C, fp32 inter-chunk state, bf16 intra-chunk with fp32 WY accumulator, checkpoint per chunk); window and slot terms add `O(T (W+G) d)`; no `O(T^2)` term appears.
2. Recall (G1): generate MQAR episodes from derived seeds (`k v` bigrams shuffled, permuted queries after separator, greedy decode, exact match plus recall at k), induction with gaps {16, 64, 256}, copy lengths {32, 128, 512}, 2-hop chains `k1 -> k2 -> v`. Same tokenizer, window, order, and scoring code for both arms. Confusion CSVs per N per seed.
3. Length (G2): train at T_train, sliding-window eval (stride T_train/2, no arm-specific truncation) at {1x, 2x, 4x, 8x} on held-out streams plus MQAR-256 to 1024/2048 retrieval split. Report `BPB(L) - BPB(T_train)` per arm and the head-to-head gap.
4. Text (G3): Enwik8 byte-level primary scoreboard (enwik8-valid BPB = loss_nats / ln2, BPE mapped back to bytes if used as secondary). Fixed 90M/5M/5M split convention pinned in harness, checksums logged, test scored only at gate time.
5. Footprint (G4): name every recurrent tensor with shapes as functions of (d_model, heads, d_k, d_v, N_state, W, G) with no factor of T, show per-token update is `O(state_size)`, then microbench steady state bytes plus median ms per token over 200 decode steps after warmup at T in {1k, 2k, 4k, 8k, 16k, 32k}, batch 1, fixed precision. Flat curve (under 5 percent growth 1k to 32k) plus proof passes.
6. Ledger and viewer: every run appends `(model, seed, gate)` rows to `postformer/ledger/ledger.csv`; `ledger.py plot` regenerates curves; `viewer/index.html` renders badges G1-G4 client side against baseline rows in the same envelope. Failed gates commit CSVs plus a dated note; issue stays open on `Refs #294`.

## Pinned choices (all research open questions resolved with justification)

- Language and stack: Python plus PyTorch (honest right tool per issue; diversity rule waived). Pure torch reference kernels first; Triton or custom CUDA only if profiled G4 bottleneck, never as silent dependency. `requirements.txt` pins torch, numpy, pyyaml.
- Tokenizer default: byte-level vocab 256 for primary Enwik8 scoreboard (no tokenizer confound); GPT-2 BPE as secondary diagnostic only. Synthetic MQAR vocab default 8192 for S-tiny; ablate {512, 8192, 32768} in A6.
- Context windows: S-tiny T_train = 512 (synthetic; cheaper seeds, covers gaps 16/64/256 plus copy 512). S-small T_train = 1024 (text; 8x = 8k fits the G4 curve without heroic hardware). Length eval at {1x, 2x, 4x, 8x} with stride T_train/2.
- Scales (non-embedding param count within plus/minus 2 percent, counting script output committed as `params_baseline.txt` and `params_candidate.txt`):
  - S-tiny approx 30M: 6 layers, d_model 512, baseline 8 heads MLP mult 4. P1: 4 delta heads with d_k 128 d_v 128 (QKV params identical to baseline), W 128, C 64, MLP hidden trimmed 2048 to 2016 for fusion headroom (beta proj d to H, alpha proj d to H, per-head scalar fusion gate).
  - S-small approx 150M: 12 layers, d_model 768, baseline 12 heads MLP mult 4. P1: 6 delta heads with d_k 128 d_v 128, W 128, C 128, MLP hidden 3072 to 3024.
  - State inventory per layer batch 1: `H*d_k*d_v` (delta S) plus `2*W*d_model` (window K plus V) plus H scalars; C never appears at inference. S-tiny bf16 total about 2.36 MB flat; S-small about 7.08 MB flat vs baseline KV growing linearly with T.
- Window W: 128 first (covers local induction gaps per Based recipe, keeps state constant small); ablate W in {0, 128, 256} in A2 with freed params reallocated to state dim and documented.
- Slots G (P2, M3): schedule {0, 4, 16, 64} at matched state bytes; G=0 must reproduce pure-SSD failure (A4). Router top-k by query-key match, load-balance loss logged, same selection budget for any baseline augmentation.
- SSD dims (P2/P3): N_state in {64, 128} default 64 first; A5 sweeps state at {0.5x, 1x, 2x} with params held fixed (trade depth or width vs state).
- Gates init and stability: k RMSNormed per head with norm fixed to 1.0; beta = sigmoid clamped to [0.01, 0.99] with bias init -2.0 (start retentive); alpha = exp(-exp(v)) init to about 0.95 to 0.99; gate projs at 0.5x lr; grad clip 1.0; cosine schedule with warmup 500 to 2000 steps; fp32 inter-chunk S; chunked-vs-recurrent forward parity test to 1e-4 relative including C boundaries.
- Optimizer shared across arms: AdamW beta1 0.9 beta2 0.95 weight decay 0.1 grad clip 1.0 cosine with warmup; tokens, steps, batch fixed per scale and documented per ledger row with GPU hours.
- Seeds: master {0, 1, 2} synthetic minimum 3 seeds x 1000 episodes; Enwik8 1 full seed plus 2 short repeats (Builder may raise). Derive subseeds via sha256 of `master/purpose` for data_gen, init, shuffle, per-episode; `random`, `numpy`, `torch`, `cuda` seeded; `cudnn.benchmark=False`, `cudnn.deterministic=True`; TF32 disabled for scoring or explicitly flagged with variance.
- Tie tolerances (documented in README and viewer): G1 candidate mean accuracy at or above baseline mean minus one pooled std at every N in {16, 64, 256} with no level below baseline by more than 1 point absolute; G2 gap `delta_candidate - delta_baseline` at or below 0 at both 4x and 8x; G3 candidate valid BPB at or below baseline valid BPB within one pooled std; G4 under 5 percent growth in state bytes and median ms per token from 1k to 32k with slope statistically zero.
- P4 gating: P4 earns M4 implementation only after P1/P2 S-tiny rows are ledgered; if P4 trails P1 on MQAR N=256 by more than 10 points, the gradient-compression fidelity hypothesis is recorded as rejected for this budget and P4 stays Refs.
- Hardware and dtype: every ledger row logs hardware, dtype, torch and cuda versions; default train bf16 with fp32 state, scoring greedy temp 0 top-k disabled; Builder pins the exact GPU string on first M1 push.

## Module Breakdown (domain decoupled from presentation)

Domain (`postformer/models/`, torch only, no viewer or HTML imports, deterministic):

- `common.py`: `RMSNorm(d)`, `SwiGLU(d_in, d_hid)`, `RotaryEmbedding(dim, base)`, `param_count_no_embed(model)` (binding counter), `seed_all(master, purpose)`, `KVWindowBuffer(W, d)` ring buffer with causal mask helper. Complexity targets: norm and MLP `O(d)` per token, RoPE `O(d)` per token.
- `baseline.py`: `TransformerBlock(d, heads, mlp_hid)` with `forward(x, kv_cache)` causal plus `step(x_t, cache_t)` for `O(1)`-per-step audit parity; `DecoderLM(config)` with tied or untied embeddings (one choice per scale, documented). State: KV cache `O(T d)` (the control that must grow).
- `p1_delta_hybrid.py`: `GatedDeltaHead(d, d_k, d_v)` with `forward_chunk(K, V, beta, alpha, S_prev)` via WY Householder chunking (C fixed global) plus `step(k_t, v_t, S)` as `S = alpha_t * (S - beta_t * (S k_t) k_t^T) + beta_t * k_t v_t^T` in `O(d_k d_v)`; `SlidingWindowAttn(d, heads, W)` exact causal over last W keys in `O((W) d)` per step; `FusionGate(d, heads)` learned per-head scalar gate blending delta and window outputs; `P1Block` = parallel branches plus residual plus SwiGLU. State per layer: `H*d_k*d_v + 2*W*d + H` floats, no T factor.
- `p5_map.py`: `PolyMap(d_k)` degree-2 feature map plus `GatedLinearHead` with `S = alpha S + K^T V` additive write (A1 counterpart to P1 erase). Same window interface with W forced to the matched value so A1 varies only the write rule.
- `p3_decoupled.py` (M3): `AccumulatorHead` with alpha fixed 1.0 plus norm-guard rescale hook, `SelectiveHead` (SSD or GLA style), `LocalWindow` reuse; `DecoupledFusion` input-dependent gate over three branches.
- `p2_slots.py` (M3): `SSDBranch(d, N_state)` with `h = a h + B x`, `SlotRouter(d, G)` top-k selector, `SlotAttn` exact over at most G keys `O(G d)` per step; slot KV capped at G positions globally.
- `p4_maglite.py` (M4): `ShortWindow` W=256 plus `FastMLP` fixed-size per-segment weights updated by one associative-reconstruction gradient step with surprise gate `alpha = f(grad_norm)` and decay; `MAGFusion` scalar gate. Per-token cost `O(|M| + W d)` constant in T; gradient overhead metered in G4 and must stay flat.

Harness (`postformer/harness/`, CLI only, no model logic beyond loading checkpoints):

- `synthetic_recall.py`: flags `--model --checkpoint --task {mqar,induction,copying,bind2hop,all} --vocab --n-pairs --episodes --gap --copy-len --batch --seed --device --dtype --out --config`; writes `g1_mqar_N{n}_seed{s}.csv` (`episode,query_idx,key,value,pred,correct,rank`) plus `g1_summary_seed{s}.json` (acc, recall at 1 and 3, mean, std, n).
- `length_sweep.py`: flags `--baseline-ckpt --candidate-ckpt --t-train --lengths --stride --split --tokenizer`; writes `g2_curve_seed{s}.csv` (`model,length,bpb,ppl,delta_vs_1x,gap_vs_baseline`).
- `enwik8_bpb.py`: flags `--checkpoint --split {valid,test} --context --stride --tokenizer {byte,bpe} --data-root --checksum`; writes `g3_bpb_seed{s}.csv` (`model,split,context,stride,tokenizer,loss_nats,bpb,n_bytes,sha256_data`); BPB = loss_nats / ln2 mapped to bytes.
- `latency_state.py`: flags `--checkpoint --lengths 1k..32k --decode-steps 200 --warmup 20 --batch-size 1 --report-proof`; writes `g4_curve_seed{s}.csv` (`model,T,state_bytes,ms_per_token_median,ms_p90,hardware,dtype,torch,cuda`) plus `g4_proof.json` skeleton.
- `ledger.py`: subcommands `append --run-json --ledger`, `check` (schema plus gate lint plus 2 percent param drift fail), `plot --ledger --out-dir` regenerating degradation and latency curves from CSV only.

Presentation (`postformer/viewer/index.html`, only place HTML or JS appears):

- Single file, vanilla JS plus inline SVG, no CDN, works over Pages preview and `file://` (fetch `../ledger/ledger.csv` with drag-drop plus paste fallback).
- Views: sortable scoreboard table (one row per version and model, filter by model); gate badges G1-G4 computed client side with the pinned tie rules; curve panels rendering selected `g2_curve` and `g4_curve` CSVs as SVG lines; header banner stating the tested envelope (`N<=512, 8x, Enwik8 valid`) next to every claim per research section 8.
- All fetches same-origin or local file; no backend calls; no build step; Builder adds a Playwright snapshot of the viewer with a fixture ledger in M1.

Public interface sketch (binding shapes; Builder expands in torch):

```python
class SeqBlock(torch.nn.Module):
    def forward(self, x: Tensor, state) -> tuple[Tensor, object]: ...
    def step(self, x_t: Tensor, state) -> tuple[Tensor, object]: ...
    def state_size(self, batch: int, bpe: int) -> int: ...

def param_count_no_embed(model) -> int: ...
def build_model(name: str, scale: str, config: dict) -> torch.nn.Module: ...
```

## Test Matrix (headless self-checks plus dynamic verification)

- Unit (pytest, CPU, fixed seeds, must be green before any eval claim):
  - T1 chunked vs recurrent parity for P1/P5/P2/P3 (relative err at or under 1e-4 including C boundaries, collinear-key stress).
  - T2 param parity: candidate within 2 percent of baseline at both scales (counter script output committed).
  - T3 causal masking: window and slot branches never attend past t (future-mask probe with planted trigger).
  - T4 determinism: same master seed reproduces `g1_summary` exactly on CPU; nondeterministic kernels flagged with variance.
  - T5 ledger schema: `ledger.py check` rejects missing cols, NaN gates, param drift.
  - T6 norm guards: beta times squared key norm under 2.0 invariant logged; accumulator rescale hook fires before overflow (P3).
- Gate (matched-budget, seeds {0,1,2} synthetic):
  - G1 MQAR N {16, 64, 256} (512 for winners) vocab 8192 plus A6 vocab and distractor sweep; induction gaps {16, 64, 256}; copy {32, 128, 512}; 2-hop 1000 episodes; pass per pinned G1 tie rule.
  - G2 curves at {1x, 2x, 4x, 8x} plus MQAR-256 to 1024/2048 split (A7); pass per pinned G2 rule with CSV plus plot.
  - G3 enwik8-valid BPB primary, test report only; pass per pinned G3 rule with checksums and provenance.
  - G4 proof plus microbench T {1k..32k} flat within 5 percent; hardware, dtype, versions logged.
- Ablations as falsification (each committed even on failure):
  - A1 delta vs additive (P1 with plain write; predicts MQAR N=256 collapse at or over 15 points or H1 is wrong).
  - A2 window {0, 128, 256} at matched params.
  - A3 accumulator on/off (predicts copying extension per H3, MQAR N=64 drop at or over 10 points without it).
  - A4 slots G {0, 4, 16, 64}; G=0 reproduces pure-SSD failure.
  - A5 state scaling {0.5x, 1x, 2x} at fixed params (recall-vs-state curve testing the bound).
  - A6 vocab {512, 8192, 32768} and distractor {0, 0.5, 0.9}.
  - A7 retrieval extrapolation vs language drift split.
- Viewer: Playwright snapshot with fixture ledger (badges plus curves render, envelope banner visible); `file://` smoke via drag-drop path.
- Hypotheses ledger: H1 (P1 at or over 95 percent MQAR N=256 where Mamba-2 arm under 60, induction within 1 point), H2 (G=16 within 2 points at N=512 with at or under 10 percent KV bytes at T=8k), H3 (decay-free head 4x copy extension), H4 (P4 beats P1 on 8x delta by at or over 0.02 BPB while tying N=64 or fidelity hypothesis rejected), H5 (degree-2 doubles MQAR N vs elu but trails P1 by at or over 15 points at N=256).

## Risks and merge discipline

- Core risk: the `d = Omega(N)` bound means exact unbounded recall with strictly O(1) state is impossible; victory is matching the baseline inside the tested envelope (N to 512, 8x, Enwik8 BPB), stated next to every claim.
- Secondary: delta instability (bounded by k-norm plus beta clamp plus fp32 state), router collapse (load-balance loss plus G=0 control), accumulator blowup (rescale hook), P4 overhead breaking G4 (metered, gated behind P1/P2).
- Every failed gate commits config plus CSV plus dated note under `postformer/ledger/`; tracking issue stays open on `Refs #294`; `Closes #294` only on G1+G2+G3+G4 passing head-to-head with reproducible numbers.

## Build order (single branch, single PR #295 across continue cycles)

- M1: harness plus baseline plus P5 plus P1-minimal (see progress file). M2: S-tiny full gates plus A1/A2. M3: P3 plus P2 plus A3/A4/A5. M4: P4 plus A6/A7 plus envelope audit. Builder never splits scaffolding and measurements into separate PRs; never adds stub buttons, no-op flags, or placeholder dialogs; unimplemented proposals stay out of CLI and viewer until their milestone.

- the Architect
