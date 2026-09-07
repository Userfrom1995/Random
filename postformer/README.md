# PostFormer (M2: toy falsification ledgered; S-tiny trained gates deferred)

O(T)-train, O(1)-state sequence modeling vs a causal Transformer baseline
under matched budgets. Issue #294. All intermediate results use `Refs #294`;
`Closes #294` only when G1+G2+G3+G4 all pass head-to-head.

## Setup

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r postformer/requirements.txt
export PYTHONPATH=.   # run from the repo root
```

Hardware/dtype log for this run: CPU reference, fp32 scoring, torch 2.14.0+cpu.
Every harness JSON records hardware, dtype, torch/cuda versions per row.

## Param convention

`param_count_no_embed` excludes the input token embedding only (the output
lm_head counts; applied identically to both arms, so parity is fair).
Pinned S-tiny baseline = 29366784; P1/P5-tiny = 29373756 (+0.024%).
Pinned S-small baseline = 113462016; P1/P5-small = 113463720 (+0.002%).
To fit the binding +-2% budget with the W=128 window branch pinned, the P1/P5
MLP hid is trimmed to 1704 (tiny) / 2726 (small) instead of the blueprint's
2016/3024 estimate. `tests/test_params.py` enforces the 2% rule at both scales.

## Train commands (M2: matched-budget MQAR trainer)

```bash
# Toy proxy (CPU minutes): vocab64/N8, 3000 steps x batch16 = 1.584M tokens
python -m postformer.harness.train --model p1-toy --data mqar \
  --vocab 64 --n-pairs 8 --steps 3000 --batch 16 --lr 3e-4 --seed 0 \
  --out postformer/ledger/checkpoints/p1-toy-s0
# A2 window override (0/16/32 at identical toy params 336332)
python -m postformer.harness.train --model p1-toy --window 0 ... (same rest)
# Full S-tiny (needs GPU runner): --model {transformer,p1,p5}-tiny --vocab 8192
```

Checkpoints are `torch.save` dicts with `state_dict` (plus `config`); every
harness accepts `--checkpoint`, and without one runs seeded random init
flagged `random_init:true` in outputs. Toy checkpoints are NOT committed
(1.4MB each x 11); they regenerate bit-identically on CPU from the command
above plus seed (keep `OMP_NUM_THREADS` fixed; thread scheduling is the only
nondeterminism source outside `seed_all`). Train curves + summaries for all
11 M2 runs live in `postformer/ledger/curves/m2-toy/`.

## Eval commands

```bash
# G1 recall (smoke: 8 episodes, N=8; full gates use --episodes 1000 --n-pairs 16,64,256)
python -m postformer.harness.synthetic_recall --model p1-tiny --task mqar \
  --vocab 64 --n-pairs 8 --episodes 8 --seed 0 --out postformer/ledger/curves
# G2 length sweep (smoke lengths; full: --t-train 512 default 1x/2x/4x/8x)
python -m postformer.harness.length_sweep --model p1-tiny --t-train 64 \
  --lengths 64,128,256 --split synthetic --seed 0 --out postformer/ledger/curves
# G3 Enwik8 BPB (needs Hutter Prize Enwik8 file at --data-root/enwik8)
python -m postformer.harness.enwik8_bpb --model p1-small --split valid \
  --context 1024 --tokenizer byte --data-root /data --out postformer/ledger/curves
# G4 footprint (smoke lengths; full: 1k..32k flatness bar)
python -m postformer.harness.latency_state --model p1-tiny --lengths 64,128,256 \
  --decode-steps 20 --report-proof --out postformer/ledger/curves
# Ledger
python -m postformer.harness.ledger append --run-json run.json --ledger postformer/ledger/ledger.csv
python -m postformer.harness.ledger check --ledger postformer/ledger/ledger.csv
python -m postformer.harness.ledger plot --ledger postformer/ledger/ledger.csv \
  --out-dir postformer/ledger/plots
```

## Envelope statement

Tested envelope (M2 toy): 2L-d128 toy arms, MQAR vocab64/N8, 1.584M train
tokens/arm/seed, G1 at 200 episodes (N8/N16, gap16, copy32, 2-hop), G4 timed
1k-32k on CPU fp32. S-tiny/S-small TRAINED gates (G1 N=64/256, G2 text, G3
Enwik8) are NOT yet measured - they need a GPU runner. Claims beyond the toy
envelope require M2-S-tiny/M4 gates. Every viewer claim carries this envelope
next to it.

## M2 toy results (matched budget, 3 seeds, `ledger/ledger.csv` rows 5-15)

- MQAR N8 (train N): P5 0.300 / P1 0.287 / Transformer 0.146 (chance 0.016).
  A1: delta shows no advantage over the additive map at toy N8 (H1/H5
  unresolved - N=256 untested). N16 extrapolation collapses for all arms
  (P1 0.039, P5 0.000, T 0.091). 2-hop: P5 0.53 / P1 0.46 / T 0.12.
- A2 W{0,16,32}: N8 0.275/0.287/0.251 - window contributes little at N8.
- G4 1k-32k: P1 1.06ms flat (<1%) with bytes flat 24592; P5 1.05ms flat
  (bytes 40976); control 2.07/6.49/15.96ms at 1k/2k/4k with linear bytes.
  S-tiny analytic bytes: baseline 25M-805M linear vs P1 flat 3.15M.
  (The curve caught a real O(T)-per-step RoPE table rebuild; fixed with
  `RotaryEmbedding.row()`, parity still green.)
- G2/G3 trained-gate cells are EMPTY for toy rows (OOD probe + fixture only,
  documented in `ledger/curves/m2-toy/`). PR stays `Refs #294`.

## Layout

- `models/`: `common.py` (RMSNorm, SwiGLU, RoPE incl. O(1) `row()` for the
  step path, KVWindowBuffer, counter),
  `baseline.py` (Transformer toy/tiny/small), `p1_delta_hybrid.py`,
  `p5_map.py`, `factory.py` (`build_model`). P2/P3/P4 stay out until M3/M4.
- `harness/`: the five CLI scripts + `train.py` (M2 matched-budget trainer) + `ledger.py` + `util.py`.
- `ledger/`: `ledger.csv` (append-only empirical ledger) + `curves/` (raw CSVs/JSON).
- `viewer/index.html`: static scoreboard (no CDN, file:// + fetch).
 - `docs/proof-g4.md`: G4 proof appendix. `tests/`: T1-T6 (11 passed).
