# Post-Transformer Sequence Architecture: Research Specification

- **Issue:** #294 (Post-Transformer Sequence Architecture, O(T^2)-free alternative beating Transformer baseline)
- **Author role:** Researcher (Dr. Mob)
- **Origin:** Brainstorm Board #42 comment by Userfrom1995 (2026-09-07T16:35:36Z), Hephaestus acknowledgment run 34143986245
- **Target language:** Python + PyTorch (honest right tool per issue mandate; diversity rule waived)
- **Handoff target:** Architect (blueprint + milestone roadmap in progress/) then Builder (iterative implementations with head-to-head eval)

This document is the scientific blueprint. It defines the literature synthesis,
the causal Transformer baseline contract, the four-gate benchmark methodology,
the mathematical analysis of the associative recall gap, and five ranked
architectural proposals with falsifiable hypotheses and an ablation plan. It
does NOT contain production code; the Architect turns this into a module layout
and milestone roadmap, and the Builder implements it.

All matched-budget comparisons use identical parameter count, training tokens,
optimizer budget, tokenizer, and evaluation protocol. A PR may use `Closes #294`
ONLY when all four gates pass with reproducible numbers. Intermediate PRs use
`Refs #294` with committed CSVs/plots and a negative-result ledger.

---

## 1. Problem statement and success gates

Design a causal sequence model with:

(a) Training cost subquadratic in sequence length T (target O(T log T) or O(T)),
(b) Generation with O(1) state memory and O(1) latency per token (state size
independent of T, with asymptotic proof plus empirical state-bytes and
ms/token vs T curve),
(c) Reasoning and in-context learning at or above a causal Transformer
decoder baseline under matched parameter budget.

Binding targets (all must be met to merge):

1. **G1 Associative Recall and Tracking.** Match or exceed Transformer on
   multi-query associative recall (MQAR), induction heads, copying, and
   variable binding. Metric: accuracy / recall@k under matched budget.
2. **G2 Length Generalization.** Lower degradation than baseline extending
   beyond the training window (4x to 8x). Train at T_train, evaluate at 4x and
   8x; report perplexity/BPB delta vs baseline.
3. **G3 Real-World Compression.** Equal or lower Bits-Per-Byte (BPB) on
   Enwik8 (enwik8-valid BPB is the scoreboard) with identical tokenizer and
   context window.
4. **G4 Inference Footprint.** Strict O(1) state and O(1) per-token latency.
   Proof plus empirical curve.

---

## 2. Literature synthesis

### 2.1 SSM lineage: S4 through Mamba-2, discrete SSMs, TTT, Titans

**S4 (Gu et al. 2021).** Continuous system `x'(t) = A x(t) + B u(t)`,
`y(t) = C x(t) + D u(t)`, `x in R^N`. Discretized by zero-order hold (ZOH):
`Abar = exp(dt A)`, `Bbar = A^{-1}(Abar - I) B`, or bilinear equivalent.
Training as recurrence `x_k = Abar x_{k-1} + Bbar u_k` or as convolution
`y = K * u` with `K_k = C Abar^k Bbar` via Cauchy kernel plus FFT. LTI
(time-invariant): no input dependence. `A` initialized HiPPO-LegS for long
memory. Train `O(B L d (log L + N))`, inference state `O(d N)`, per-step
`O(d N)`. Strong on Long Range Arena smoothing tasks, weak on MQAR and
copying. Limitation: fixed filter cannot route by content or form induction
heads; parameter budget is spent on static dynamics, not key-value comparison.

**S4D (Gu et al. 2022).** Same system with diagonal complex
`A = diag(a_1..a_N)`, e.g. `a_n = -1/2 + i pi n`. Per-scalar ZOH,
Vandermonde convolution. Same complexities, simpler code, more stable
extrapolation via `Re(a_n) < 0` envelope. Same recall ceiling: diagonal LTI
is content-blind.

**S5 (Smith et al. 2022).** MIMO form `x_k = Abar x_{k-1} + Bbar u_k`,
`y_k = Cbar x_k + D u_k` with vector input, diagonal `Abar`, learned per-dim
`dt`, HiPPO init, parallel scan training `O(B L P H)` work and `O(log L)`
depth, inference state `O(P^2)`. Faster than S4, same expressivity class:
still LTI, no MQAR gain.

**H3 (Fu et al. 2022).** Two SSMs plus gating: `Q,K,V = proj(u)`,
`K_ssm = SSM_shift(K)`, output `O = Q * SSM_diag(K_ssm * V)`. FFT training
`O(L log L)`, inference `O(d N)`. First SSM to target recall explicitly by
emulating `QK^T V` with SSMs in place of softmax. Closes part of the S4 to
attention gap on recall and SuperGLUE, still fails multi-query MQAR because
`A,B` remain input-independent and cannot filter distractors.

**Mamba-1 / S6 (Gu and Dao 2023).** Selective recurrence:
`dt_k = softplus(W_dt x_k + b)`, `B_k = W_B x_k`, `C_k = W_C x_k`, fixed
negative diagonal `A`. ZOH: `Abar_k = exp(dt_k A)`, `Bbar_k ~= dt_k B_k`.
`h_k = Abar_k h_{k-1} + Bbar_k x_k`, `y_k = C_k h_k + D x_k`. Here `dt_k` is a
content gate: large `dt` forgets, small `dt` retains. Train `O(B L D N)` via
hardware-aware parallel scan, inference state `O(D N)` (typical D=2048,
N=16), per-token `O(D N)`. Large Pile gains over S4/H3, 5x Transformer
throughput, extrapolation to very long copying with tuned `dt`. MQAR studies
show sharp degradation when the number of key-value pairs exceeds N
(compressive bottleneck); distractor-heavy length generalization drops. No
explicit erase beyond decay.

**Mamba-2 / SSD (Dao and Gu 2024).** Scalar-per-head form:
`h_t = a_t h_{t-1} + B_t x_t`, `y_t = C_t^T h_t`, with `h in R^{N x P}`,
`a_t = exp(-exp(w dt_t)) in (0,1)`. Duality: mixer matrix
`M_{ij} = C_i^T (prod_{k=j+1..i} a_k) B_j` for `i >= j`, so
`Y = (M hadamard C B^T) X`: a 1-semiseparable structured attention without
softmax, enabling block-chunk matmul training (2-8x faster than Mamba-1).
Larger N (64..256) materially improves MQAR; pure SSD still underperforms
Transformer++ on fuzzy recall and multi-hop at matched params. Recall
capacity scales as `O(N P)` per head (linear in params) while attention
recall scales with context `O(L)`; growing N to match attention erodes the
speed advantage.

**SD-SSM / selective-diagonal variants (incl. Gated DeltaNet precursors).**
Per-state-dim gating `h_{k,n} = a_{k,n} h_{k-1,n} + b_{k,n} x_k` with
`a_{k,n} = exp(dt_{k,n} lambda_n)`. Finer timescale diversity, small MQAR
gain; extra projections cost params without solving the compression bound.

**Discrete SSMs (LRU, DSS, RetNet-LTI core).** Native discrete recurrence
`x_k = Lambda x_{k-1} + B u_k` with `|lambda_j| < 1` enforced by
`lambda_j = exp(-exp(nu_j) + i theta_j)`. No continuous parameterization.
Same LTI ceiling; discrete init aids optimization but adds no content
awareness.

**TTT (Sun et al. 2024).** Hidden state is fast weights `W`. TTT-Linear:
loss `l_t(W) = ||W x_t - x_t||^2`, update
`W_t = W_{t-1} - eta grad l_t(W_{t-1})`, readout `z_t = W_t x^Q_t`. TTT-MLP
uses a 2-layer MLP as `W`. Chunkwise parallel training `O(L)`; inference
requires a gradient step per token `O(d^2)` with state `O(d^2)`. Capacity
`O(d^2)` beats vector SSMs; strong on long needle tasks and distribution
shift. Per-token SGD is FLOP-heavy and unstable; exact MQAR fidelity still
trails verbatim KV storage under matched FLOP budget.

**Titans (Behrouz et al. 2024).** Deep neural memory `M_t` (MLP weights),
surprise metric `s_t = ||grad L(M_{t-1}, x_t)||`, gating
`alpha_t = f(s_t)`, update
`M_t = (1 - alpha_t) M_{t-1} - eta_t grad L(M_{t-1}, x_t)` with decay
forgetting, readout `y_t = M_t(x_t)`. Variants MAC (memory as context), MAG
(gated short-attention plus long-memory branch), MAL (memory as layer).
Chunkwise `O(L)` training; inference `O(1)` per token with state `O(|M|)`.
Best SSM-lineage long-retrieval results (BABILong, 2M needle). Most complex
to train; exact token-level copying precision still trails full attention;
inner-loop gradient overhead exceeds Mamba and attention decoding.

### 2.2 Linear and subquadratic attention family

**Vanilla linear attention (Katharopoulos et al. 2020).**
`S_t = S_{t-1} + phi(K_t)^T V_t`, `z_t = z_{t-1} + phi(K_t)`,
`Y_t = phi(Q_t)^T S_t / (phi(Q_t)^T z_t)` with `phi = elu+1` or ReLU. State
`R^{d_phi x d_v}`, `O(d^2)`, `O(N d^2)` recurrent. Replaces
`exp(QK^T/sqrt(d))` by factorizable `phi(Q)^T phi(K)`. Poor MQAR: capacity
bounded by `rank(S) <= d`; fails when distinct pairs exceed d; blurred
induction heads; dilution with N.

**Performer / FAVOR+ (Choromanski et al. 2020).** Same recurrence with random
feature map approximating `exp(x^T y)` in expectation via orthogonal random
features. Better scores than elu kernel but stochastic variance blurs sharp
retrieval; MQAR still fails at scale.

**RWKV-4 (Peng et al. 2023).** Per-channel time-mix:
`wkv_t = (sum_{i<t} exp(-(t-i)w+k_i) v_i + exp(u+k_t) v_t) /
(sum_{i<t} exp(-(t-i)w+k_i) + exp(u+k_t))`, output gated by receptance
`sigma(R_t)`, plus token-shift. Vector state `O(d)`, `O(N d)`. No QK pairwise
dot; channel-wise exponential moving average. Very weak MQAR and induction;
good extrapolation but distant info forgotten.

**RWKV-5 Eagle / RWKV-6 Finch.** Multi-head matrix state
`S^h_t = diag(w^h) S^h_{t-1} + K^{hT}_t V^h_t`, v6 adds data-dependent decay
`w_t = f(x_t)`. State per head `R^{D_h x D_h}`, total `O(D^2/h)`. Improved
over v4, modest MQAR for few keys; still diagonal forget with no removal of
colliding bindings; lags GLA and DeltaNet on MQAR at matched state.

**RetNet (Sun et al. 2023).** Parallel
`Y = ((QK^T) hadamard D) V` with `D_{n,m} = gamma^{n-m}` for `n >= m`;
recurrent `S_n = gamma S_{n-1} + K_n^T V_n`, `Y_n = Q_n S_n`; per-head
`gamma`, GroupNorm plus swish gate. State `O(d^2)`, recurrent `O(N d^2)`.
Fixed geometric decay forgets old pairs regardless of importance; poor long
MQAR; stable chunkwise inference but strictly dominated by data-dependent
gating at matched budget.

**Hyena / Hyena-2 (Poli et al. 2023).** Order-2:
`q,k,v = P(x)`, `y = P(q hadamard H*(k hadamard v))` where `H` is an implicit
long filter `h_t = MLP(pos_emb(t))` via FFT conv, `P` short depthwise conv
plus linear. `O(N log N d)`. Replaces pairwise routing by gated long
convolution; data control is elementwise gating, not content addressing.
Fails MQAR and induction requiring arbitrary lookup; good for dense
long-range smoothing, not retrieval.

**GLA - Gated Linear Attention (Yang et al. 2023).**
`S_t = G_t hadamard S_{t-1} + K_t^T V_t`, `O_t = Q_t S_t`,
`G_t = alpha_t^T beta_t` (rank-1 outer-product forget from sigmoids).
Chunkwise parallel. State `O(d^2)`, `O(N d^2)` recurrent. Selective forget
helps ignore distractors; decent MQAR for small key counts; fuzzy induction
heads observed. Additive rank-1 write causes collisions; capacity about
`d^2` floats; exact multi-key recall below softmax Transformer at matched
width.

**Gated DeltaNet / Delta Rule (Schlag et al. 2021; Yang et al. 2024; Grazzi
et al. 2024).** One gradient step on `||v - S k||^2`:
`S_t = S_{t-1} + beta_t (V_t - S_{t-1} K_t) K_t^T`, gated form
`S_t = alpha_t S_{t-1} (I - beta_t K_t K_t^T) + beta_t K_t V_t^T` with
`beta, alpha(x_t)`. Parallelized via WY representation for Householder-like
chunks. State `O(d^2)`, `O(N d^2)` with chunk overhead. Fast-weight
associative memory with retrieve-then-overwrite; removes the old value bound
to the same or similar key before writing. Best in the linear family:
near-Transformer MQAR at moderate length, exact overwrite enables induction
heads and multi-hop tracking; overwrite prevents saturation, giving the best
length scaling among linear variants. Limit: one rank-1 correction per step
bottlenecks distinct-pair throughput; higher chunkwise cost; still below
softmax at large key counts or high interference at matched width.

**Hawk / Griffin (De et al. 2024).** Hawk RG-LRU is a diagonal input-gated
RNN with gated MLP output (vector state `O(d)`); Griffin adds local sliding
MQA plus residual. Hawk alone has near-zero long MQAR; Griffin is good
within window W via local attention and fails beyond it. Excellent
extrapolation; long associative recall fundamentally capped at matched
budget unless d or W scales linearly.

**SSD / GSA synthesis.** `S_t = alpha_t(x_t) S_{t-1} + K_t^T V_t`,
`Y_t = Q_t S_t`, scalar or vector `alpha`; SSD duality
`Y = (L hadamard QK^T) V` with 1-semiseparable
`L_{n,m} = prod_{k=m+1..n} alpha_k`. Selectivity helps ignore distractors
but provides no sharp max and no explicit unbinding; induction stays fuzzy;
memory interference persists.

State-geometry rule of thumb: vector SSM `O(d)` is weaker than matrix memory
`O(d^2)`, which is weaker than KV cache `O(T d)`. Data dependence and delta
overwrite close much of the gap but do not match causal softmax under
matched budget for exact recall.

### 2.3 Why Transformers win at recall: induction heads and capacity bounds

**Induction heads (Elhage et al. 2021; Olsson et al.).** Two-head composition
completing `[A][B]...[A] -> [B]`. Head 1 (previous-token) attends to `i-1`
and writes "previous token was X". Head 2 (induction) matches the current
`A` query against the earlier `A` key via its QK circuit and copies `B`
forward via its OV circuit. Formal sketch: with token embedding plus head-1
output encoding `x_{i-1}`, there exist `W_Q,W_K,W_V,W_O` such that
`q_T^T k_j` is maximized iff `x_j == x_T` and the output approximates
`e_{next(j)}`. This is a 2-layer, 1-head-per-layer construction implementing
on-the-fly variable binding: `A` is a variable, `B` its bound value, created
by contiguity rather than by weights. Copying generalizes this to L distinct
bindings; fuzzy copying generalizes equality to similarity. Induction heads
explain much of the in-context learning phase change.

**MQAR (Arora et al., Zoology 2023).** Sample N disjoint pairs
`(k_1,v_1)..(k_N,v_N)`, present as a sequence, then query a subset (or all)
keys in permuted order; the model must emit matching values. A 2-layer
Transformer solves arbitrary N up to context with O(1) heads (layer 1 marks
pairs, layer 2 retrieves). Linear recurrences with fixed state `d << N` must
compress pairs into one sketch and suffer interference. Reported pattern:
attention, Based, and Hyena with enough heads solve MQAR at N=64-256 while
H3, RWKV, Hyena-small, and Mamba-1 fail or need state scaling with N.

**Theorem sketches.**

- Thm A (Copying lower bound, Jelassi et al. 2024, informal): a causal linear
  SSM `h_t = A h_{t-1} + B x_t`, `y_t = C h_t` with state dim d over finite
  precision needs `d = Omega(L)` to exactly copy an arbitrary string of
  length L over an alphabet of size at least 2. Proof idea: copying is the
  identity on `|Sigma|^L` distinct inputs; a d-dim bottleneck has at most
  `exp(O(d))` distinguishable states at fixed precision; pigeonhole forces
  collision unless d grows linearly. Transformers copy with `O(log L)`
  depth/width by attending back positionwise.
- Thm B (Merrill et al. 2024, log-precision SSM): a log-precision linear RNN
  with `poly(n)` steps and `o(n)` state cannot recognize unbounded copying
  `w#w` or general associative recall with a growing key universe, while a
  constant-size Transformer can with direct attention. SSMs simulate small
  finite-state machines well but not content-addressable retrieval over large
  alphabets.
- Thm C (Arora et al. MQAR separation): some MQAR instance with N pairs is
  solvable by 1-layer attention with `O(N)` sequence cache, but any
  time-invariant linear recurrence needs `d >= N * log|V|` bits for exact
  recall, because the same compression applies to every pair before queries
  arrive.
- Thm D (Grazzi et al. 2024, DeltaNet vs Mamba): diagonal selective SSMs
  `h_t = alpha_t h_{t-1} + beta_t outer(k_t, v_t)` with scalar `alpha_t`
  cannot delete a single key without decaying all keys, so interleaved
  repeats require growing norm or dimension. The delta rule
  `M_t = M_{t-1} + beta_t (v_t - M_{t-1} k_t) k_t^T`
  (equivalently `M_t = (I - beta_t k_t k_t^T) M_{t-1} + beta_t v_t k_t^T`)
  implements content-addressed overwrite and solves MQAR with
  `d = O(D_key)` independent of N up to capacity `O(d)`, where diagonal
  Mamba needs `Omega(N)`. Gated DeltaNet reaches 100 percent MQAR where
  Mamba-1/2 plateau at matched state size.

**Fixed vs data-dependent decay.** Fixed decay (S4, S5, H3, Hyena) is a
low-pass filter: good for denoising, bad for selective keep/forget. Old keys
persist as noise and new keys overwrite weakly. Data-dependent decay (Mamba
`delta_t, B_t, C_t`; GLA; RWKV-6) implements an input-controlled latch:
remember pairs until queried, ignore filler; strictly better on MQAR and
enables small-N induction-like copying. Limit: scalar `alpha_t` is global;
suppressing stale key A also suppresses live key B when they share state
dimensions. Selectivity in time is not selectivity in content.
Content-selective forgetting needs matrix-valued forget
(`I - beta k k^T`), not scalar `alpha`.

**Pairwise comparison vs compressed state.** Attention keeps `QK^T`
explicit: T queries each compare against T keys with no bottleneck; memory
`O(T^2)` compute and `O(T)` KV cache; recall is retrieval, not
reconstruction. Linear recurrence keeps
`S_t = sum_i c_{i,t} outer(phi(k_i), v_i)` with scalar weights from decay
products; query `q_t` sees only the sketch `S_t phi(q_t)`. Similar keys
collide; recovery needs near-orthogonal codes, limiting slots to `O(d)`.
Information-theoretic form: exact recall of N arbitrary b-bit pairs needs
`N*b` bits until query time; a d-float state at p bits holds `d*p` bits, so
`d*p >= N*b`, i.e. `d = Omega(N)`; attention stores `O(T*d)` bits in its KV
cache and satisfies this with constant d as T grows. The `O(T)` cache vs
`O(1)` recurrence gap is therefore a necessity for exact recall, not an
implementation detail. Approximate or structured recall (small universe, Zipf
keys, short distance) evades the bound, which is why SSMs look competitive
on natural text but fail adversarial MQAR.

---

## 3. Baseline specification (binding contract)

Every candidate is evaluated head-to-head against a causal Transformer
decoder-only baseline under identical parameter count, training tokens,
optimizer budget, tokenizer, and evaluation protocol.

### 3.1 Architecture

- Decoder-only, causal mask, pre-norm (RMSNorm), SwiGLU MLP, RoPE positions,
  no bias terms, tied or untied embeddings (fix one choice per scale and
  document it).
- Two mandated scales:
  - **S-tiny (synthetic track):** approx 30M non-embedding params, 6 layers,
    d_model 512, 8 heads, MLP mult 4. For MQAR, induction, copying, variable
    binding ablations where many seeds are cheap.
  - **S-small (text track):** approx 150M non-embedding params, 12 layers,
    d_model 768, 12 heads, MLP mult 4. For Enwik8 BPB and length sweeps.
- Parameter matching rule: count non-embedding params; candidate total must
  be within plus or minus 2 percent of baseline at the same scale. Publish
  the counting script output (`params_baseline.txt`, `params_candidate.txt`).
  State memory (KV cache vs recurrent state) is NOT counted as params but is
  reported separately under G4.

### 3.2 Data and tokenizer

- Synthetic tasks generate from fixed seeds (Section 4). Text track uses
  Enwik8 with byte-level vocabulary (256 symbols) OR GPT-2 BPE; the choice
  must be identical for baseline and candidate within a comparison. Default
  recommendation: byte-level for the primary Enwik8 scoreboard (no tokenizer
  confound), BPE as a secondary diagnostic.
- Context windows: S-tiny synthetic T_train in {256, 512}; S-small text
  T_train in {1024, 2048} (Architect fixes exact values per milestone and
  documents them). Length generalization evaluates at 4x and 8x T_train.

### 3.3 Training budget

- Optimizer: AdamW (beta1 0.9, beta2 0.95, weight decay 0.1, grad clip 1.0),
  cosine schedule with warmup (values fixed per scale and shared across arms).
- Matched FLOPs: same training tokens and same steps for baseline and
  candidate. Document tokens, steps, batch size, and measured GPU-hours in
  every ledger row. One seed is never a result: minimum 3 seeds for synthetic
  gates, minimum 1 full seed plus 2 short-seed repeats for Enwik8 (Architect
  may raise this).
- Fixed-seed reproducibility: all data generation, init, and shuffling seeded;
  seeds published; nondeterministic kernels either disabled or explicitly
  flagged with measured variance.

### 3.4 Evaluation protocol parity

- Same eval harness, same prompts/orderings, same context window, same
  scoring code for both arms. No candidate-specific prompt tuning. Any
  inference hyperparameter (temperature is 0 for scoring; top-k disabled)
  applies equally.

---

## 4. Benchmark methodology (four gates)

Harness layout (Architect finalizes paths; Builder implements):

```
harness/
  synthetic_recall.py    # G1: MQAR + induction + copying + variable binding
  length_sweep.py        # G2: T_train, 4x, 8x perplexity/BPB deltas
  enwik8_bpb.py          # G3: enwik8-valid BPB scoreboard
  latency_state.py       # G4: state bytes + ms/token vs T curve + proof notes
  ledger.py              # aggregates runs into CSV + plots
```

### 4.1 G1: Associative recall and tracking

- **MQAR core.** Vocab V (default 8192 for S-tiny; ablate 512/8192/32768),
  N_pairs in {16, 64, 256} (extend to 512 for winners), pair format
  `k v` bigrams shuffled, queries permuted after a separator, greedy decode,
  exact-match accuracy per query plus recall@k where k in {1, 3}. Report mean
  and std over at least 3 seeds x 1000 episodes. Passing bar: candidate mean
  accuracy >= baseline mean minus one pooled std (i.e. statistical tie or
  win) at every N_pairs level, with no level below baseline by more than 1
  point absolute.
- **Induction heads.** Two settings: natural (repeated random bigram strings,
  score next-token accuracy on second occurrence) and planted (insert
  `[A][B]...[A]` trigger with distractor gap in {16, 64, 256} tokens).
- **Copying.** Exact string copy: present random string length L in
  {32, 128, 512}, separator, prefix, model completes; exact-match rate.
- **Variable binding / multi-hop.** 2-hop retrieval: `k1 -> k2, k2 -> v`
  chains; query `k1`, expect `v`. Accuracy over 1000 episodes x 3 seeds.
- Controls: same tokenizer and context window; distractor density fixed;
  key/value position counterbalanced. Log full confusion CSVs
  (`g1_mqar_N{n}_seed{s}.csv`).

### 4.2 G2: Length generalization

- Train at T_train. Evaluate perplexity and BPB on held-out streams at
  lengths {T_train, 2x, 4x, 8x} by sliding-window eval with stride T_train/2
  (no truncation tricks that differ across arms).
- Metric: degradation delta `BPB(L) - BPB(T_train)` per arm, plus head-to-head
  gap `delta_candidate(L) - delta_baseline(L)`; passing bar is gap <= 0 at
  both 4x and 8x (candidate degrades no more than baseline).
- Synthetic companion: MQAR-trained-at-256 evaluated at 1024/2048 to isolate
  retrieval extrapolation from language-model drift.
- Publish the length-degradation curve (CSV plus plot) for every version.

### 4.3 G3: Real-world compression (Enwik8 scoreboard)

- Primary metric: **enwik8-valid BPB** (bits per byte = loss_nats / ln 2,
  computed at byte level; if BPE is used, map back to bytes before scoring so
  BPB stays comparable). Identical tokenizer and context window across arms.
- Secondary: enwik8-test BPB (report only; valid is the gate), plus
  per-position loss curves to diagnose early-vs-late degradation.
- Passing bar: candidate valid BPB <= baseline valid BPB (statistical tie
  allowed within one pooled std, estimated from seeds/splits; Architect sets
  the exact tie rule and documents it).
- Data provenance: Hutter Prize Enwik8, fixed split (first 90M train, next 5M
  valid, last 5M test, or the standard 100M/valid/test convention the harness
  pins); checksums logged; no test leakage (test evaluated only at gate
  time).

### 4.4 G4: Inference footprint (O(1) proof plus microbench)

- Asymptotic proof obligation (in the Architect blueprint and code comments):
  name the recurrent state tensors, give their shapes as functions of
  (d_model, n_heads, d_state, window, slots) with NO factor of T, and show
  the per-token update is `O(state_size)` flops with no scan over history.
  Counter: the baseline KV cache is `O(T)`; any candidate component whose
  state grows with T (full attention, unbounded kNN index) must be explicitly
  bounded (fixed window W, fixed slot count G) to qualify.
- Empirical microbench `latency_state.py`: for T in
  {1k, 2k, 4k, 8k, 16k, 32k} (extend while hardware allows), measure steady
  state bytes (allocated recurrent state, excluding weights) and median
  ms/token over 200 decode steps after warmup, batch size 1, fixed precision.
  Plot both vs T; passing bar is flat (slope statistically zero; Architect
  sets the tolerance, e.g. < 5 percent growth from 1k to 32k).
- Report hardware, dtype, and framework versions alongside.

### 4.5 Empirical ledger schema

Every version appends one row per (model, seed, gate) to
`ledger/ledger.csv` with at least: model, params, train_tokens, seed,
g1_mqar_{16,64,256}, g1_induction, g1_copy, g1_2hop, g2_bpb_{1x,4x,8x},
g2_delta_{4x,8x}, g3_valid_bpb, g3_test_bpb, g4_state_bytes,
g4_ms_per_token, gpu_hours. Plots regenerate from CSV. Negative results are
committed, never discarded.

---

## 5. Architectural proposals (ranked by promise)

Ranking criterion: expected MQAR scaling evidence plus theoretical
justification for content-selective forgetting under O(1) state. All
proposals keep a causal, subquadratic-training, O(1)-inference envelope;
any exact-attention component is windowed or slot-bounded (see G4).

### P1. Gated DeltaNet + sliding-window hybrid (Delta-Hybrid). Highest promise.

**Design.** Each layer combines (i) a gated delta-rule fast-weight memory
`S_t = alpha_t S_{t-1} (I - beta_t K_t K_t^T) + beta_t K_t V_t^T` with
`alpha_t, beta_t = f(x_t)` per head (key dim 128 default), and (ii) a short
exact sliding-window attention (W = 128 or 256) whose output is fused by a
learned gate with the delta branch, followed by SwiGLU. Optionally add one
decay-free accumulator head per layer (Section P3).

**Why it should win.** The delta update is the only linear mechanism with
proven key-wise removal: it erases the old value at the same key before
writing, giving `O(d)` orthogonal slots with content-addressed overwrite
(Grazzi et al.), while scalar-decay models (Mamba, GLA, RetNet) erase
everything at once. The sliding window handles exact local induction pairs
(Based recipe) so the fast weights focus on long-range bindings. This
directly targets the Thm D separation and the Based synthesis.

**Falsifiable hypothesis H1.** At S-tiny with matched params, P1 reaches
>= 95 percent MQAR accuracy at N=256 and vocab 8192 where a matched Mamba-2
arm plateaus below 60 percent, and matches baseline induction accuracy
within 1 point.

**Risks.** Chunkwise WY training cost; stability of `beta_t`; window adds a
`W*d` state constant (still O(1) in T but must be budgeted).

### P2. Retrieval-routed SSD + sparse global slots. High promise, moderate risk.

**Design.** Mamba-2 SSD backbone (`h_t = a_t h_{t-1} + B_t x_t`,
`y_t = C_t^T h_t`, N=64..128) plus a learned router selecting up to G=8..16
global tokens per segment for exact attention (top-k by router score or by
query-key match), with the SSD output and slot-attention output gated. Slots
are fixed-count (O(1) state); training stays subquadratic via block-chunk
SSD plus sparse slot attention.

**Why it should win.** Explicit slots restore exact pairwise comparison for
the small subset that matters (2 percent of tokens carrying bindings),
recovering full-attention MQAR while cutting KV cache by an order of
magnitude (NSA / Mixture-of-Depths precedent). SSD handles smoothing and
filtering; slots handle retrieval.

**Falsifiable hypothesis H2.** With G=16 slots, P2 recovers baseline MQAR at
N=512 within 2 points while using at most 10 percent of baseline KV bytes at
T=8k, and degrades less at 8x length than the pure SSD ablation.

**Risks.** Router training (collapse, top-k nondifferentiability); load
balancing; slot-selection leakage across arms must be controlled (same
selection budget for any baseline augmentation).

### P3. Multi-scale decoupled memory (accumulator + filter + local window).

**Design.** Per layer, three parallel branches: (a) one decay-free head
(`alpha = 1`, pure accumulation, no normalization) for verbatim storage;
(b) selective-decay heads (Mamba-2/GLA style) for filtering; (c) sliding
local attention (W=128). Branches fused by input-dependent gating. Rationale:
separate storage from filtering instead of forcing one decay to do both
(Hyena-MR / Griffin lessons).

**Falsifiable hypothesis H3.** Adding one decay-free head per layer extends
noise-interleaved copying length from `O(d)` to at least 4x at fixed d, and
ablating it drops MQAR N=64 accuracy by at least 10 points.

**Risks.** Unbounded accumulator norm; needs normalization or periodic
rescaling; still no key-wise erase, so large-N MQAR likely trails P1.

### P4. Test-time fast-weight MLP memory, MAG-lite (Titans-inspired). High risk, high reward.

**Design.** Long-memory branch as a small per-segment MLP updated by one
gradient step on an associative reconstruction loss with surprise gating,
fused MAG-style: `y = g * Attn_short + (1-g) * Mem_long`, where `Attn_short`
is a W=256 sliding window and `Mem_long` is the fast-weight readout. Mini-batch
chunkwise training; inference keeps one MLP state (O(1)).

**Falsifiable hypothesis H4.** P4 beats P1 on 8x length extrapolation
(BABILong-style needle and Enwik8 8x delta) by at least 0.02 BPB while tying
on MQAR N=64; if it trails P1 on MQAR N=256 by more than 10 points, the
gradient-compression fidelity hypothesis is rejected for this budget.

**Risks.** Highest training complexity (lr, surprise threshold, decay
schedule); per-token gradient overhead threatens the G4 latency bar; exact
copying fidelity is lossy by construction.

### P5. Higher-order feature-map baseline (ablation control, not a contender).

**Design.** Gated linear attention with degree-2 polynomial or learned spiky
map (Based / ReBased / Hedgehog recipe) and no delta rule. Included as the
ablation that quantifies how much H1 gains come from feature geometry vs
from key-wise removal.

**Falsifiable hypothesis H5.** Degree-2 maps double MQAR N at fixed d
relative to elu/ReLU maps but still fail linear scaling past `d^2` slots,
underperforming P1 by at least 15 points at N=256.

### Ranking summary

| Rank | Proposal | Expected edge | Main risk |
|------|----------|---------------|-----------|
| P1 | Delta-Hybrid | key-wise erase, proven MQAR scaling | training cost/stability |
| P2 | SSD + sparse slots | exact retrieval for bindings | router complexity |
| P3 | Decoupled multi-scale | cheap copying extension | no key-wise erase |
| P4 | Titans MAG-lite | best extrapolation | overhead, fidelity |
| P5 | Higher-order map | ablation control | capped scaling |

Recommended build order: P5 (cheap control) plus P1 core in Milestone 1
(harness + baseline + P5 + P1-minimal), P3 accumulator ablation in
Milestone 2, P2 slots in Milestone 3, P4 only after P1/P2 results are
ledgered.

---

## 6. Ablation plan (each ablation is a falsification test)

1. **A1 feature map vs delta.** P1 with delta update replaced by plain
   additive write (`S_t = alpha_t S_{t-1} + K_t^T V_t`). Predicts MQAR N=256
   collapse (>= 15 point drop); if not, H1 is wrong about the erase
   mechanism.
2. **A2 window on/off.** P1 with W=0 vs W=128/256 at matched params (freed
   params reallocated to state dim). Predicts local induction gap closes with
   window but long MQAR persists without delta.
3. **A3 decay-free head.** P3 accumulator head on/off. Predicts copying
   extension per H3.
4. **A4 slots count.** P2 with G in {0, 4, 16, 64} at matched state bytes.
   Predicts monotonic MQAR gain with diminishing returns; G=0 must reproduce
   pure-SSD failure.
5. **A5 state scaling.** Each contender at state dims {0.5x, 1x, 2x} with
   params held fixed (trade depth/width vs state). Plots recall-vs-state to
   test the `d = Omega(N)` bound empirically.
6. **A6 vocab and distractor stress.** MQAR at vocab {512, 8192, 32768} and
   distractor ratios {0, 0.5, 0.9}. Scalar-decay models should degrade faster
   than delta/slot models.
7. **A7 length-stress split.** Separate retrieval extrapolation (MQAR-256 to
   2048) from language drift (Enwik8 8x) to attribute G2 failures correctly.

---

## 7. Complexity and O(1) inference argument (proof sketch for G4)

Claim: every proposal P1-P5 has per-token generation cost and state
independent of T.

State inventory (per layer, batch 1): delta memory `S in R^{d_k x d_v}` per
head (P1, P5); SSD state `R^{N x P}` per head (P2, P3); sliding window KV of
at most W positions (P1-P4); slot KV of at most G positions (P2); fast-weight
MLP of fixed size (P4). Total state
`S_total = L_layers * (H * d_k * d_v + W * d + G * d + const)` with no factor
of T. Update per token: one rank-1 delta correction `O(d_k d_v)`, one SSD
scalar-gated outer product `O(N P)`, window/slot attention over at most
`W+G` keys `O((W+G) d)`, MLP step `O(|M|)`. All terms are constant in T.
Hence memory `O(1)` and latency `O(1)` per token. The harness verifies the
constants empirically (state bytes and ms/token flat vs T). Any unbounded
kNN index or full-context attention would violate this and is therefore
excluded; G and W are fixed globals, not functions of T.

Training stays subquadratic: delta/SSD/GLA via chunkwise parallel scans and
WY Householder chunking (`O(T)` work, `O(log T)` depth, plus a bounded
`C^2` intra-chunk term with fixed chunk size C); window/slot attention adds
`O(T (W+G) d)`; long convolutions (if any) via FFT `O(T log T)`. No
`O(T^2)` term appears.

---

## 8. Risks, negative-result ledger, and merge discipline

- Core risk: the `d = Omega(N)` bound (Section 2.3) means exact recall of
  unbounded pairs with strictly O(1) state is information-theoretically
  impossible; victory is defined as matching the baseline within the tested
  envelope (N up to 512, 8x length, Enwik8 BPB), not as unbounded exact
  recall. Ledger must state the tested envelope next to every claim.
- Secondary risks: delta-rule training instability, router collapse (P2),
  accumulator norm blowup (P3), TTT-style overhead breaking G4 (P4).
- Every failed gate is committed to `ledger/` with config, CSV, and a dated
  note; the tracking issue stays open on negative results (`Refs #294`).
  `Closes #294` is used ONLY when G1+G2+G3+G4 all pass head-to-head with
  reproducible numbers.

---

## 9. Handoff to the Architect

The Architect is asked to produce: (1) module layout for the harness plus
baseline plus P1/P5 (Milestone 1), with P3/P2/P4 staged behind it; (2) exact
pinned choices left open here (T_train per scale, tokenizer default,
W/G/N/dims, tie tolerances, hardware/dtype); (3) milestone roadmap in
`progress/` scoping 3 to 7 capabilities per milestone PR referencing
`Refs #294`; (4) the asymptotic-proof appendix skeleton that the Builder
fills with measured shapes and the G4 curve.

Open questions for the Architect (with Researcher recommendations in
parentheses): Enwik8 tokenizer default (recommend byte-level primary);
S-small T_train 1024 vs 2048 (recommend 1024 for cheaper 8x=8k eval);
window W 128 vs 256 (recommend 128 first, ablate); slot count G schedule
(recommend {0,4,16,64}); whether P4 earns a milestone before P1/P2 ledger
(recommend no).

- Dr. Mob, the Researcher
