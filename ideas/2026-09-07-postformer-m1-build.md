# PostFormer M1: Delta-Hybrid Scaffold with First Falsification Plumbing

Date: 2026-09-07. Issue: #294. Branch: `opencode/issue294-20260907194528` (PR #295, shared across M1-M4). Status: M1 complete, `Refs #294` (no gate claims; all smoke rows are random-init).

## What was built

PostFormer M1 is a causal O(T)-train, O(1)-state sequence-modeling program in
Python + PyTorch that pits the P1 gated delta-rule hybrid and the P5
higher-order map control against a pinned causal Transformer baseline under
matched budgets. Everything lives in `postformer/` (no repo-root pollution,
no landing-page change; the project is a Python engine, not Pages-hostable).

- Models (`postformer/models/`): `common.py` (RMSNorm, SwiGLU, RoPE, batched
  `KVWindowBuffer`, `param_count_no_embed` excluding the input embedding only,
  sha256-derived `seed_all`); `baseline.py` (S-tiny 29366784 / S-small
  113462016 non-embed params, full `forward` + incremental `step` with RoPE
  baked at append); `p1_delta_hybrid.py` (per-head gated delta memory
  `S += beta*k*(v-r)^T` with unit-norm keys, beta in [0.01,0.99] bias -2.0,
  alpha init ~0.97, exact W=128 sliding window, learned fusion, SwiGLU;
  reference chunked forward in chunks of C); `p5_map.py` (parameter-free
  degree-2 map `[k; 0.5k^2]` with scaled additive write, identical proj shapes
  so T2 parity holds by construction); `factory.py` (`build_model`).
- Harness (`postformer/harness/`): `synthetic_recall.py` (MQAR N-list,
  induction gaps, copying lengths, 2-hop; greedy exact-match + recall@k,
  per-query CSVs + summary JSON), `length_sweep.py` (score-once strided eval,
  delta_vs_1x + gap_vs_baseline), `enwik8_bpb.py` (byte-primary, fixed
  90M/5M/5M split, sha logging, BPE exits 1 as deferred), `latency_state.py`
  (prefill + warmup + 200 timed `step()` calls, state bytes from
  `model.state_bytes`), `ledger.py` (append/check/plot; check enforces schema,
  NaN rejection, and the binding +-2% param-drift rule).
- Tests (`postformer/tests/`, 9 passed): T1 parity incl. collinear-key stress
  (7e-7 max err), T2 param parity both scales, T3 prefix-invariance causal
  probe, T4 exact-summary determinism, T5 ledger lint (accepts good, rejects
  NaN/drift/schema).
- Viewer (`postformer/viewer/index.html`): single-file scoreboard, no CDN,
  envelope banner, fetch + file + drop + paste paths (static validation
  green; Playwright snapshot unavailable on this runner, deferred to M2).
- Docs: `postformer/README.md` (setup/train/eval/envelope/hardware log),
  `postformer/docs/proof-g4.md` (state inventory with measured byte counts,
  per-token flop accounting, flatness bar).
- Ledger: `postformer/ledger/ledger.csv` (4 M1 smoke rows, check passes),
  `ledger/curves/` (raw G1/G2/G4 CSVs + summaries + g4_proof), `ledger/plots/`
  (G4 SVGs + manifest), `ledger/params/` (committed counter outputs).

## Why these choices

- MLP trim 1704/2726 instead of the blueprint's 2016/3024: the binding +-2%
  rule outranks the estimate once the W=128 window branch is pinned; measured
  drift is +0.024% (tiny) / +0.002% (small).
- `--batch` in G1 controls flush granularity only; the M1 reference harness
  decodes greedy batch-1 and says so in `--help` (batched greedy is M2 work).
- Two real bugs caught by parity probing: window `step()` rotated RoPE on the
  flat head-concatenated dim (now per-head, matching `forward`), and harness
  model init drew from global torch state (now `reseed(seed, init-{model})`
  before every build).

## First smoke numbers (random init, zero train tokens, NOT gate results)

- G1 (vocab 256, N=16/64, 16 episodes): all arms at chance (~0.00-0.02), as
  expected untrained; harness plumbing validated end to end.
- G2 (t-train 64, synthetic): random-init BPB ~13; deltas/gaps computed.
- G3: p1-small on a 4KB seeded-random byte fixture (sha logged, NOT Enwik8):
  BPB 8.21 ~= uniform 8.0 + untrained penalty; path validated.
- G4 (S-tiny, fp32 CPU): P1 state flat at 3145824 B (64/128/256), P5 flat at
  4718688 B, baseline linear 1.57M/3.15M/6.29M; ms/token ~11-12.5 flat at
  smoke scale. The O(1) signature is already visible.

## Key files

`postformer/models/*`, `postformer/harness/*`, `postformer/tests/*`,
`postformer/ledger/ledger.csv`, `postformer/viewer/index.html`,
`postformer/docs/proof-g4.md`, `progress/294-post-transformer-sequence-architecture.md`.

## Next (M2)

Full G1/G2/G3/G4 at S-tiny for baseline vs P1 vs P5 (seeds 0,1,2), A1 (delta
on/off), A2 (window 0/128/256), H1/H5 verdicts, 1k-32k G4 flatness within 5%,
real Enwik8 bytes, Playwright viewer snapshot. P2/P3/P4 stay out of CLI and
viewer until M3/M4.

- the Builder
