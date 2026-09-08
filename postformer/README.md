# PostFormer (M4h: toy envelope audited, 118 tests green; S-tiny trained gates deferred)

O(T)-train, O(1)-state sequence modeling vs a causal Transformer baseline
under matched budgets. Issue #294. All intermediate results use `Refs #294`;
`Closes #294` only when G1+G2+G3+G4 all pass head-to-head (G4 in Pareto
tiers: (a) full O(1) flat within 5% 1k-32k, or (b) sublinear dominating the
baseline at every T with G1+G2+G3 green - 2026-09-07 amendment).

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
Pinned S-tiny baseline = 29366784; P1/P5/P2-tiny = 29373756/29373756/29364522
(+0.024%/+0.024%/-0.008%); P3-tiny = 29376858 (+0.034%);
P4-tiny = 29367660 (+0.003%).
Pinned S-small baseline = 113462016; all five candidates within +-0.05%
(see `tests/test_params.py`, which enforces the 2% rule at all three scales for
p1/p2/p3/p4/p5). To fit the binding +-2% budget with the W=128 window branch
pinned, MLP hid is trimmed per family (tiny 1704, P3-tiny 1532, P4-tiny 1702;
small 2726, P3-small 2468, P4-small 2724) instead of the blueprint's 2016/3024 estimate.

## Train commands (M2: matched-budget MQAR trainer)

```bash
# Toy proxy (CPU minutes): vocab64/N8, 3000 steps x batch16 = 1.584M tokens
python -m postformer.harness.train --model p1-toy --data mqar \
  --vocab 64 --n-pairs 8 --steps 3000 --batch 16 --lr 3e-4 --seed 0 \
  --out postformer/ledger/checkpoints/p1-toy-s0
# A2 window override (0/16/32 at identical toy params 336332)
python -m postformer.harness.train --model p1-toy --window 0 ... (same rest)
# A4 slots sweep (P2: 0/4/16/64; slots=0 is the pure-SSD control)
python -m postformer.harness.train --model p2-toy --slots 0 ... (same rest)
# A3 accumulator control (P3 dynamics removed, params unchanged)
python -m postformer.harness.train --model p3-toy --no-accumulator ... (same rest)
# P4 MAG-lite smoke (CPU): --model p4-toy ... (same rest; 100-step smoke
# verified finite loss + checkpoint + G1 eval; NOT a gate result)
# Full S-tiny (needs GPU runner): --model {transformer,p1,p2,p3,p4,p5}-tiny --vocab 8192
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

## M2 toy results (matched budget, 3 seeds, `ledger/ledger.csv` data rows 5-13)

- MQAR N8 (train N): P5 0.300 / P1 0.2875 / Transformer 0.146 (chance 0.016).
  A1: INVALID (P5 cells pre unit-norm fix, ledger rows 8-10; control math
  changed after measurement, no delta conclusion until P5 re-run; H1/H5
  unresolved - N=256 untested). N16 extrapolation collapses for all arms
  (P1 0.039, P5 0.000, T 0.091). 2-hop: P5 0.532 / P1 0.46 / T 0.118.
- A2 W{0,16,32}: N8 0.275/0.287/0.251 - HOWEVER the pre-fix G1 harness had
  no `--window` passthrough, so all three evals ran window 16 (see the
  `config.window=16` in `g1_summary_p1-toy-W0/W32-s0.json`); the A2
  conclusion is INVALID pending re-eval with the fixed harness. Ledger rows
  now carry the true train-window in the `window` column with this disclaimer
  in `notes`.
- G4 1k-32k: P1 1.06ms flat (<1%) with bytes flat 24576; P5 1.05ms flat
  (bytes 40960); control 2.07/6.49/15.96ms at 1k/2k/4k with linear bytes.
  S-tiny analytic bytes: baseline 25M-805M linear vs P1 flat 3.15M.
  (The curve caught a real O(T)-per-step RoPE table rebuild; fixed with
  `RotaryEmbedding.row()`, parity still green.)
- G2/G3 trained-gate cells are EMPTY for toy rows (OOD probe + fixture only,
  documented in `ledger/curves/m2-toy/`). PR stays `Refs #294`.

## M3/M4b/A4/A6 toy probes (matched 0.528M-token protocol, 100 eps)

- M3: p2-G16 0.0825 / p3 0.0600 vs matched p1-W16-1000 ref 0.0625; A3
  p3-noacc 0.06125 vs p3 0.0600 (H3 unresolved at toy).
- M4b: p4 0.035, BELOW the matched p1 ref (H4 NEGATIVE at toy, open at scale).
- A4: G0 0.04625 < G4 0.0825 = G16 = G64 behaviorally identical at score
  level (slot count untested:
  toy T=33/stride 8 admits at most 5 writes; H2 open).
- A6: p1 + transformer both at the 0.0 floor at vocab512 (budget below
  threshold; H1/H5 open). N16 sits at chance for every 0.528M-token toy probe
  (M2b 1.584M-budget arms retain 0.039-0.091, still far below train-N accuracy).
- Consolidated scoreboard: `docs/envelope-audit.md` (M4e).

## Layout

- `models/`: `common.py` (RMSNorm, SwiGLU, RoPE incl. O(1) `row()` for the
  step path, KVWindowBuffer, counter),
  `baseline.py` (Transformer toy/tiny/small), `p1_delta_hybrid.py`,
  `p5_map.py`, `p3_decoupled.py` (accumulator + selective + window, A3),
  `p2_slots.py` (SSD-lite + G exact stride slots, A4),
  `p4_maglite.py` (surprise-gated delta + window, M4/H4), `factory.py`
  (`build_model`).
- `harness/`: the five CLI scripts + `train.py` (matched-budget trainer,
  `--window`/`--slots`/`--no-accumulator` ablation flags) + `ledger.py` + `util.py`.
- `ledger/`: `ledger.csv` (append-only empirical ledger, 25 rows: 4 smoke +
  20 trained toy + 1 params-only drift-baseline pin) + `curves/` (raw CSVs/JSON).
- `viewer/index.html`: static scoreboard (no CDN, file:// + fetch).
 - `docs/proof-g4.md`: G4 proof appendix (Pareto tiers (a)/(b) + P2/P3/P4
   inventory). `docs/envelope-audit.md`: consolidated toy scoreboard (M4e).
   `tests/`: T1-T6 over all six families + `test_m3.py`
   (A3/A4 controls, slot contract, G4 flatness) + `test_p4.py`
   (surprise grads, P4 causality, P4/P1 state equality) + A4/A6 probe pins
    + tester red-team suites - 118 passed.
