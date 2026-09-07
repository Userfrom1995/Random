# PostFormer (M1: scaffold + first falsification)

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

## Train commands (M1: no training yet; random-init smoke only)

Training arrives in M2. Checkpoints are `torch.save` dicts with `state_dict`
(plus optional `config`); every harness accepts `--checkpoint`, and without
one runs seeded random init flagged `random_init:true` in outputs.

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

Tested envelope (M1 smoke): miniature configs on CPU, MQAR N<=8, lengths
<=256, synthetic streams, random init. Claims beyond this envelope require
M2+ gates. Every viewer claim carries this envelope next to it.

## Layout

- `models/`: `common.py` (RMSNorm, SwiGLU, RoPE, KVWindowBuffer, counter),
  `baseline.py` (Transformer S-tiny/S-small), `p1_delta_hybrid.py`,
  `p5_map.py`, `factory.py` (`build_model`). P2/P3/P4 stay out until M3/M4.
- `harness/`: the five CLI scripts + `ledger.py` + `util.py`.
- `ledger/`: `ledger.csv` (append-only empirical ledger) + `curves/` (raw CSVs/JSON).
- `viewer/index.html`: static scoreboard (no CDN, file:// + fetch).
- `docs/proof-g4.md`: G4 proof appendix. `tests/`: T1-T5.
