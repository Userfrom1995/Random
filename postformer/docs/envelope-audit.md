# PostFormer toy envelope audit (M4e, 2026-09-08)

Consolidated first-read scoreboard over every CPU-feasible toy probe on PR #295
(`postformer/ledger/ledger.csv`, 25 rows: 4 smoke + 20 trained toy + 1
params-only transformer-small drift-baseline pin, `check` green). All probes share one
protocol unless noted: vocab64/N8 MQAR, seed0, 1000 steps x batch16 = 0.528M
tokens (M2b uses 3000 steps = 1.584M tokens x 3 seeds), G1 envelope 100 eps
(M2b 200 eps), lr 3e-4 fp32 (M2/M3/M4b/A6 CPU; A4 train + G1 eval on CUDA
cu130 per `a4-toy` summaries). Toy rows are NOT gate results; `Refs #294`
is kept and `Closes #294` waits on S-tiny/S-small G1+G2+G3+G4 head-to-head.

## Scoreboard (G1 mqar8, train N; N16 cells are extrapolation, chance 1/64)

| Arm (ledger row) | mqar8 | N16 | 2hop | Budget | Read |
|---|---|---|---|---|---|
| transformer-toy mean, 3 seeds (rows 11-13) | 0.146 | 0.091 | 0.118 | 1.584M | M2b baseline ref |
| p1-toy mean, 3 seeds (rows 5-7) | 0.2875 | 0.039 | 0.46 | 1.584M | M2b A1: no delta edge |
| p5-toy mean, 3 seeds (rows 8-10) | 0.300 | 0.000 | 0.532 | 1.584M | M2b A1 control |
| p1-toy W0, seed0 (row 17) | 0.275 | 0.110 | 0.42 | 1.584M | A2 INVALID (see below) |
| p1-toy W32, seed0 (row 18) | 0.251 | 0.053 | 0.43 | 1.584M | A2 INVALID (see below) |
| p1-W16-1000 ref, seed0 (curves/m3-toy, note only) | 0.0625 | - | 0.01 | 0.528M | M3 matched ref |
| p2-toy G16, seed0 (row 14) | 0.0825 | - | 0.03 | 0.528M | M3 P2 above p1 ref |
| p3-toy, seed0 (row 15) | 0.0600 | - | 0.01 | 0.528M | M3 P3 at p1 ref |
| p3-toy noacc, seed0 (row 16) | 0.06125 | - | 0.02 | 0.528M | M3 A3: unresolved |
| p4-toy, seed0 (row 19) | 0.035 | 0.0156 | 0.01 | 0.528M | M4b H4 NEGATIVE at toy |
| p2-toy slots0, seed0 (row 20) | 0.04625 | 0.0056 | 0.01 | 0.528M | A4 pure-SSD control |
| p2-toy slots4, seed0 (row 21) | 0.0825 | 0.0013 | 0.03 | 0.528M | A4 slots help |
| p2-toy slots64, seed0 (row 22) | 0.0825 | 0.0013 | 0.03 | 0.528M | A4 count untested |
| p1-toy V512, seed0 (row 23) | 0.0 | 0.0 | 0.0 | 0.528M | A6 floor (both arms) |
| transformer-toy V512, seed0 (row 24) | 0.0 | 0.0 | 0.0 | 0.528M | A6 floor (both arms) |
| transformer-small pin (row 25) | - | - | - | 0 | params-only drift baseline, gates empty |

## Ablation verdicts at toy (all open at scale)

- A1 (delta on/off): P1 0.2875 vs P5 0.300 at N8 (3 seeds). INVALID
  (P5 cells pre unit-norm fix; control math changed after measurement, see
  ledger rows 8-10 notes). No delta conclusion until P5 re-run;
  H1/H5 unresolved (N=256 untested). Caveat: P5 now unit-norms q+k while P1
  leaves q raw, so the control differs by query scale as well as the write rule.
- A2 (window on/off): rows 17/18 evals ran window 16 pre-fix, so the
  W0/W16/W32 comparison is INVALID as an A2 result; the A2-re seed0 probe
  (W0 0.0875 / W16-ref 0.0625 / W32 0.05125) shows no window advantage at toy N8.
- A3 (accumulator on/off): p3-noacc 0.06125 vs p3 0.0600. Unresolved at toy.
- A4 (slots sweep): G0 0.04625 < G4 0.0825 = G64 summary-cell
  equal (identical params 336074 and identical
  train loss 3.942723035812378; per-episode N16 CSVs differ as
  disclosed: 7 pred flips, acc/recall unchanged; G4 evicts at T=33,
  so count scaling untested; the M3 G16 match at 0.0825 is cross-env
  corroboration only, CPU torch 2.14.0+cpu vs CUDA torch 2.14.0+cu130).
  N16 sits far below chance (1/64) for all measured A4-sweep arms
  (G0/G4/G64: 0.005625/0.00125/0.00125 vs chance 0.015625; M3 G16 N16
  unmeasured, ledger row 14 cell empty), so that column is noise floor,
  not signal.
  Slots beat pure-SSD, but toy episodes (T=33, stride 8) admit at most 5 slot
  writes, so only G >= 5 holds full history; G4 holds 4/5 and evicts
  position 0, so slot COUNT stays untested
  until S-tiny N64+ (T_train 512). H2 open.
- A6 (vocab stress): both arms at the 0.0 floor at vocab512 under the 1000-step
  toy budget (final loss within 0.065 of ln512); budget below threshold, no
  separation. Sizes the real A6 (3000+ steps or S-tiny).
- A7 (retrieval-vs-drift): every toy arm shows mqar8 > 2hop > untrained
  transfer 0.0 (induction/copy at chance after MQAR-only training, as expected).

## Hypothesis first reads (all open pending S-tiny N64+)

H1/H5 unresolved; H2 open (A4 count untested); H3 unresolved (A3 at toy);
H4 NEGATIVE at toy (p4 0.035 below matched p1 ref 0.0625 and p2 0.0825).

## Gate status

G1/G2/G3 trained gates: NOT measured (GPU-blocked; p1-tiny is ~1s/step at
batch2/seq33 on CPU, so the binding gate is ~50+h/arm). G4: analytic + toy
timed flatness holds (P1/P5 timed flat 1k-32k: P1 1.06ms flat <1%;
P2/P3/P4 flat analytically by shared step-path construction, not timed;
proof-g4.md is source of
truth for byte inventories). G2/G3 trained cells are EMPTY by design.
