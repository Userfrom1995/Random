# PostFormer M3: Decoupled (P3) + SSD-Slots (P2), First Falsification (Builder)

Date: 2026-09-08. Issue: #294. PR #295 (single-PR discipline, `Refs #294`).
Continues M2-toy (Reviewer-approved at 2017b885, Tester 27 passed at e16ae8b4).

## What was built

- `postformer/models/p3_decoupled.py` (new): shared-QKV dual-state memory.
  Accumulator branch (decay-free `A += beta*k v^T`, alpha fixed 1.0, F-norm
  rescale-hook with ledgered fire counter) + selective branch (GLA-lite
  scalar decay) + reused exact W-window, fused 3-way, SwiGLU close.
  `use_accumulator=False` freezes A at zeros (A3 control: same params,
  dynamics removed). `step_split` returns (recurrent, selective) in one
  pass; the accumulator contribution `r - s` is exact (states evolve
  independently, reads are linear). No shadow double-pass.
- `postformer/models/p2_slots.py` (new): SSD-lite branch (`S = a*S + k v^T`,
  no erase term) + global exact slots (capacity G, fixed-stride writer,
  oldest evict, exact softmax read over stored slots = top-G by q-k match
  with zero router params, hence no router-collapse mode; deviation from
  the blueprint's learned top-k is deliberate and documented) + reused
  W-window, 3-way fusion, SwiGLU. `slots=0` is the pure-SSD A4 control.
  Training forward uses prefix-stacked exact reads (fresh tensors, full
  slot-path grads); `step()` uses the incremental ring buffer (eval-only).
  A first version read from the mutable buffer in forward and broke
  autograd (in-place version bump, caught by the new train test, fixed).
- `postformer/models/factory.py`: `_trunk_cfg` shared dims + `_MLP_HID`
  parity pins for p1/p2/p3/p5 x toy/tiny/small. Measured (non-embed):
  toy base 336768 vs p2 336074 (-0.21%) / p3 336594 (-0.05%);
  tiny base 29366784 vs p2 29364522 (-0.01%) / p3 29376858 (+0.03%);
  small base 113462016 vs p2 113417580 (-0.04%) / p3 113473020 (+0.01%).
  P2 shares P1's hid (stride router is parameter-free); P3 pays one hid
  step for its second output proj. `tie_embeddings` guard extended.
- Harness: `train.py` gains `--slots` (A4) and `--no-accumulator` (A3);
  `synthetic_recall.py` `--window` gate extended to p2/p3; `util.load_model`
  now inherits non-param ablation keys (window/slots/use_accumulator/
  slot_stride) from the checkpoint config and fails loudly on --config
  mismatch (see bug below). `ledger.py` window docstring covers p2/p3.
- `postformer/docs/proof-g4.md`: P2/P3 state inventory + measured S-tiny
  footprints (P2 3932256 B / P3 4718784 B flat, tier (a) by construction)
  + the binding 2026-09-07 Pareto-tier amendment (a: O(1) flat <5%;
  b: sublinear dominating baseline at every T with G1+G2+G3 green).
  Viewer banner + README updated to match (envelope, tiers, P2/P3 layout,
  A3/A4 commands, corrected parity pins).

## Real bug caught (same class as M2-A2, fixed centrally)

The p3-noacc probe first evaluated with the accumulator ON: `load_model`
built factory defaults and loaded the state_dict (identical shapes, so
`strict=False` stayed silent), ignoring the checkpoint's
`use_accumulator=False` - the exact analogue of the M2 window bug, now for
non-param keys. Fix: `load_model` inherits (window, slots,
use_accumulator, slot_stride) from the checkpoint config unless explicitly
overridden, and rejects --config disagreement with SystemExit. Regression
test `test_load_model_inherits_ablation_config` covers inherit + slots=0 +
loud mismatch. p3-noacc G1 re-ran after the fix (below). All harnesses
(length/enwik8/latency) inherit the fix via the shared loader.

## Measurements (CPU fp32, honestly reduced budget - NOT gate results)

Matched toy probes, seed0, 1000 steps x batch16 = 0.528M tokens/arm,
vocab64/N8, G1 100 episodes (`postformer/ledger/curves/m3-toy/`, 12 summaries):

- A2-re (fixed loader, eval window == train window): W0 0.0875 / W16
  0.0625 / W32 0.0512 (2-hop 0.01 all). No window advantage at toy N8;
  W0 numerically best. A2 gate verdict still needs S-tiny N64+.
- M3 first falsification: p2 (G16/s8) mqar8 0.0825 / 2hop 0.03 - above the
  matched p1-W16 ref (0.0625), below M2b 3000-step arms (different budget,
  not comparable). p3 mqar8 0.0600 / 2hop 0.01 - matches p1 ref within
  noise. p3-noacc (corrected) mqar8 0.0612 / 2hop 0.02 - accumulator shows
  NO advantage at toy N8 (A3/H3 unresolved, needs S-tiny copy tasks).
- Ledger: 18 rows, `check` green. 5 upserts/appends only where keys were
  novel (p2/p3/p3-noacc-toy); the M2 A2 rows kept their 3000-step cells
  with a re-eval pointer appended to notes (no history rewrite). The
  matched W16-1000 ref lives in curves + notes (key collides with the M2b
  row; upsert would have destroyed it).
- S-tiny pipeline smoke: all five families forward-finite at tiny/vocab8192
  (0.2-0.4s/64tok CPU); p1-tiny trains ~1s/step at batch2/seq33, so the
  binding gate (3000 steps x batch16 x N64+) is ~50+ h/arm on CPU - GPU
  runner required, documented. Gate-vocab (8192) eval path verified on
  random init (chance, as expected); vocab-mismatched checkpoints fail
  loudly (size-mismatch SystemExit, verified).

## Tests

34 passed (27 pre-existing + 7 new): `test_m3.py` (A3 zero-branch + param
equality, A4 slots=0 + SlotBuffer contract + stride/evict/read, G4
flatness p2/p3 vs growing control, ablation flags, loader inheritance) +
`test_gate_invariants_p2_p3` (T6: SSD decay in (0,1), P3 betas/alpha,
rescale counter) with T1/T2/T3 automatically extended over p2/p3 via
conftest FAMILIES. Two genuine implementation bugs (P2 forward zeros-shape,
slot-buffer autograd) were caught by the new tests before commit.

## Next

Full S-tiny trained gates on a GPU runner (3 arms... now 5 arms x 3 seeds,
N64/256) via `continue`; then A3/A4/A5 sweeps at S-tiny, viewer Playwright
snapshot, M4 (P4 MAG-lite gated behind P1/P2 ledger, A6/A7, S-small
Enwik8 + 8x audit). `Closes #294` only on G1+G2+G3+G4-tier-a/b passing
head-to-head.

- the Builder
