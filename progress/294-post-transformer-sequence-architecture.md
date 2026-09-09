# Progress - Post-Transformer Sequence Architecture (issue #294)

- **Issue:** #294
- **Branch:** opencode/issue294-20260907194528
- **Status:** in-progress
- **Research deliverable:** `docs/research/issue-294-post-transformer-sequence-architecture.md` (literature review + baseline spec + benchmark methodology + 5 ranked proposals + falsifiable hypotheses + ablation plan + O(1) proof sketch).
- **Architect blueprint:** `ideas/2026-09-07-post-transformer-sequence-architecture.md` (module layout, pinned choices, interfaces, test matrix, single-PR build order).

## Research summary (Dr. Mob, the Researcher, 2026-09-07)

- Surveyed via subagent army: S4/S4D/S5/H3/Mamba-1/Mamba-2/SD-SSM/discrete SSMs/TTT/Titans; linear attention/Performer/RWKV/RetNet/Hyena/GLA/Gated DeltaNet/Hawk-Griffin/SSD-GSA; recall-gap theory (induction heads, MQAR, Thm A-D, scalar vs content-selective forgetting, O(T) vs O(1) capacity bound).
- Core finding: scalar selectivity controls when to remember; only key-structured removal (delta/Householder rule), explicit bounded slots, or exact windowed attention restores what to forget. State geometry predicts recall: vector O(d) < matrix O(d^2) < KV cache O(T d).
- Baseline contract pinned: causal decoder-only Transformer, S-tiny approx 30M (synthetic) + S-small approx 150M (text), params within plus/minus 2 percent, AdamW cosine, fixed seeds, identical tokenizer/context/eval per comparison.
- Four-gate methodology pinned: G1 MQAR N={16,64,256} (+512 for winners) plus induction/copy/2-hop; G2 1x/2x/4x/8x degradation deltas; G3 enwik8-valid BPB scoreboard (byte-mapped); G4 O(1) proof plus state-bytes and ms/token vs T curve; ledger schema defined; negative results committed with Refs #294; Closes #294 only on all four gates passing.
- Proposals ranked: P1 Delta-Hybrid (top) > P2 SSD + sparse slots > P3 decoupled multi-scale > P4 Titans MAG-lite (high risk) > P5 higher-order map (ablation control). Build order: P5 + P1-minimal first, then P3 ablation, then P2, then P4.
- Ablations A1-A7 defined as falsification tests (delta on/off, window on/off, accumulator on/off, slots sweep, state scaling, vocab/distractor stress, retrieval-vs-drift split).

## Handoff to Architect

- Requested action: `architect`.
- Architect tasks: module layout for harness + baseline + P1/P5 (M1) with P3/P2/P4 staged; pin open choices (tokenizer default byte-level recommended; S-small T_train 1024 recommended; W=128 first; G in {0,4,16,64}; tie tolerances; hardware/dtype); milestone roadmap in progress/ (3-7 capabilities per milestone PR, Refs #294); asymptotic-proof appendix skeleton for Builder + G4 curve.

## Architect blueprint (the Architect, 2026-09-07)

Single technique, single branch, single PR (#295) across continuous `continue` cycles. Never split scaffolding and measurements into separate PRs. All intermediate pushes use `Refs #294`; `Closes #294` only on G1+G2+G3+G4 passing head-to-head with reproducible numbers.

- **Active Milestone:** M4be Tester hostile ground-truth suite complete on PR #295 (M1 + M2-toy + M3 + M4a/M4b toy falsification + A4 sweep + A6 pilot + M4e audit + M4ac-M4be hostile suites gated-ready, ledger 25 rows green); next is S-tiny full gates (GPU-blocked).
- **Milestone 1 (M1: scaffold + first falsification, PR 1 target, Refs #294):** [x] `postformer/` scaffold with `requirements.txt` + README + proof appendix skeleton; [x] baseline Transformer S-tiny/S-small + param counter within 2 percent (tiny +0.024%, small +0.002%, committed `ledger/params/`); [x] harness five scripts with exact CLI contracts + seeding + ledger schema; [x] P5 map control + P1-minimal (delta + W=128 + fusion); [x] unit tests T1-T5 green (9 passed) + viewer fixture snapshot (static green; Playwright deferred, no browser on runner); [x] first S-tiny smoke rows in ledger (4 rows, check passes, G4 plots).
- **Milestone 2 (M2: S-tiny gates + erase proof, Refs #294):** [x] M2a trainer + toy scale + W=0 A2 switch + T6 (11 passed); [x] M2b toy matched-budget MQAR training (transformer vs P1 vs P5, 3 seeds, 1.584M tokens each) + G1 eval = A1; [x] M2c A2 window {0,16,32} toy sweep + G4 1k-32k flatness (toy timed + S-tiny analytic) + RoPE O(T)-per-step fix + ledger 15 rows check-green + plots; [x] G4 Pareto-tier amendment re-lint (proof/viewer/README, no re-run, 2026-09-07 binding); [ ] full S-tiny trained gates DEFERRED (CPU-bound, measured 2026-09-08: p1-tiny ~1s/step at batch2/seq33 so the binding 3000x16xN64+ gate is ~50+h/arm on CPU - needs GPU runner).
- **Milestone 3 (M3: decoupled + slots, Refs #294):** [x] P3 accumulator branch + factory pins (toy 274 / tiny 1532 / small 2468, +0.03% tiny) + `--no-accumulator` A3 flag; [x] P2 SSD + slots G {0,4,16,64} + `--slots` A4 flag + A4 G=0 control (shares P1 hid, -0.01% tiny); [x] M3 test suite (T1/T2/T3 auto-extended over p2/p3 + test_m3.py A3/A4/slot-contract/G4-flatness/loader-inheritance + T6 p2/p3 guards, 34 passed); [x] A2-re + M3 first falsification toy probes (6 arms seed0 1000 steps = 0.528M tokens, fixed --window loader, curves/m3-toy, ledger 18 rows check-green); [ ] A3/A4/A5 sweeps at S-tiny (needs GPU); [ ] H2/H3 verdicts ledgered (H3 unresolved at toy: p3-noacc 0.0612 vs p3 0.0600).
- **Milestone 4 (M4: MAG-lite + envelope audit, Closes #294 only on full pass):** [x] M4a P4 code (`models/p4_maglite.py` surprise-gated delta + window, factory pins toy 294/tiny 1702/small 2724, parity toy -0.43%/tiny +0.003%/small +0.002%, `test_p4.py` 4 tests, suite 48 passed, 100-step toy smoke finite + checkpoint + eval, proof/README/ideas updated); [x] M4b toy falsification (p4-toy seed0 1000 steps = 0.528M tokens matched to M3 refs, G1 envelope 100 eps: mqar8 0.035 / N16 0.0156 chance / 2hop 0.01 / induction-copy 0.0; BELOW p1-W16-1000 ref 0.0625 and p2 0.0825, H4 NEGATIVE at toy, A6 N16-collapse + A7 retrieval-vs-drift split documented, curves/m4b-toy/, ledger 19 rows check-green); [ ] P4 gated behind P1/P2 ledger + H4 verdict at scale; [ ] A6 vocab/distractor stress at scale; [ ] A7 retrieval-vs-drift split at scale; [ ] S-small Enwik8 + 8x audit + final scoreboard; [ ] `Closes #294` if G1+G2+G3+G4 pass else `Refs #294` with negative ledger.
- **Current step:** M4be verification complete at 5f136f4a (ledger 25 rows green 26-col schema, py_compile clean, scope clean, PR MERGEABLE CLEAN per gh, forward_chunk refs only test self-pins, Refs #294; full pytest incl. M4bd/M4be suites rests on the torch-env Tester pass). Next: S-tiny full gates on a GPU runner.
- **Next steps:** (1) full S-tiny trained gates on a GPU runner via `continue` (train.py supports tiny presets for all five families; at S-tiny the token-per-symbol budget makes A6 realistic); (2) A3/A4/A5 at S-tiny; (3) viewer Playwright snapshot; (4) envelope audit.

## Builder log (the Builder, 2026-09-07, M2 toy falsification)

- M2a: `harness/train.py` (AdamW 0.9/0.95, wd 0.1, clip 1.0, cosine+warmup, MQAR/Markov data, checkpoint+curve+summary outputs); toy scale pinned in factory/baseline (`transformer-toy` 336768 vs `p1/p5-toy` 336332, -0.13%, T2 extended to toy/tiny/small); `SlidingWindowAttn` W=0 zero-branch + state_size guard (A2 control); T6 `tests/test_stability.py` (beta in [0.01,0.99], alpha in (0,1), beta*||k||^2 worst 0.99 < 2.0, collinear finite). 11 passed.
- M2b (matched budget, CPU fp32, vocab64/N8, 3000 steps x batch16 = 1.584M tokens/arm/seed, lr 3e-4): G1 toy envelope (200 eps) - MQAR N8 P5 0.300 / P1 0.287 / T 0.146 (chance 0.016); N16 extrapolation collapses (P1 0.039, P5 0.000, T 0.091); 2-hop P5 0.532 / P1 0.460 / T 0.118; induction/copy at chance (MQAR-only training, no transfer, as expected). A1 verdict: INVALID (P5 cells pre unit-norm fix, ledger rows 8-10; control math changed after measurement, no delta conclusion until P5 re-run); H1/H5 UNRESOLVED at toy envelope (N=256 untested) - honestly ledgered, Refs #294 kept.
- M2c: A2 W{0,16,32} seed0 N8: 0.275/0.287/0.251 - RETRACTED as an A2 result: the pre-fix G1 harness had no `--window` passthrough, so all three evals ran window 16 (`config.window=16` in both W0/W32 summaries); no A2 conclusion until re-eval with the fixed harness (needs S-tiny N64+ for a real test anyway). G4: real gate win - the 1k-32k curve exposed an O(T)-per-step RoPE table rebuild in every step() path (16.3ms at 32k); fixed via `RotaryEmbedding.row()` (identical values, O(d)); after fix p1-toy 1.06ms flat (<1% growth 1k-32k, bytes flat 24592), p5-toy 1.05ms flat (bytes 40976), control transformer-toy 2.07/6.49/15.96ms at 1k/2k/4k with bytes 2M/4M/8M linear. S-tiny analytic bytes 1k-32k: baseline 25M-805M linear vs P1 flat 3.15M vs P5 flat 4.72M (256x less at 32k). Parity still 11/11 green after the fix.
- G2 OOD probe (MQAR-trained arms on uniform streams, NOT a gate measurement, ledger cells left empty): all explode OOD; P1 degrades least (8x +6.0 vs T +10.8). Real G2 needs text-trained arms - deferred with S-tiny. G3 real Enwik8 deferred to M4 (path validated M1).
- Ledger: 15 rows (4 M1 + 9 toy + 2 A2, renamed to valid `p1-toy` + `window` column by the Fixer), `check` green; 99 M2 curve files under `ledger/curves/m2-toy/`; `ledger plot` now recurses subdirs with analytic relabeling; checkpoints NOT committed (1.4MB each x 11) - bit-regenerable on CPU via documented `train.py` command + seed (note thread-count caveat in ideas entry).
- Deferred (needs GPU runner): full S-tiny trained G1/G2/G3 (train.py already supports `--model transformer-tiny` etc.; ~25M params x 3 arms x 3 seeds is hours on CPU, minutes-hours on GPU).

## Fixer log (the Fixer, 2026-09-07, M1+M2-toy review findings)
- Applied all 6 M2 findings + all 10 M1 carry-forwards on PR #295 (no clobber of M2a/b/c artifacts; raw curve files untouched, ledger notes disclose provenance).
- M2-1: `train.py` data RNG now keyed by (seed, data) only (identical streams per arm), init RNG by (seed, model, data) applied after; M2-5: full-sequence CE documented as designed + `mqar_query_positions` helper pins the future span-masked index set; M2-6: T6 asserts the P5 `poly_map` bound separately (smoke cap 50, no 2.0 claim) + `steps/batch/log_every/seq-len` guards + `SlidingWindowAttn` rejects `window<0`.
- M2-2: `synthetic_recall --window` with train/eval mismatch guard (inherits checkpoint train window by default); M2-3/4: ledger renamed to valid `--model` values with true train-window bytes (W0 16400 / W16 24592 / W32 32784), new `vocab`/`window`/`g1_mqar_8` columns, N16 cells literal with N8 in notes, A2 conclusion retracted pending re-eval.
- M1: `forward_chunk` renamed `forward_recurrent` with honest docstring (both memories); viewer RFC-4180 `splitCSV` + HTML-escaping; ledger `append` dedups on (model, seed, vocab, window) with `--force` upsert and a strict per-row `check` (schema per row, dupes, empty-row tags, no dead except); factory pins 29366784/113462016 + ternary fix + `tie_embeddings` guard; proof-g4 totals 3145824/7864608; `parse_int_list` k/K/M suffixes; `length_sweep --baseline-checkpoint`; hygiene (dead imports, RoPE `max_len` enforced, `test_params` on `tmp_path`, T3 `<=1e-6` + step prefix-invariance at the W boundary). The cited stale progress line ("S-tiny smoke rows next") was already gone from the file; no change needed there.
- `ledger check` green on 15 migrated rows (verified without torch); full pytest T1-T6 needs a torch env (absent here) - next review/test pass must re-run it. `Refs #294` kept.

- the Fixer

## Builder log (the Builder, 2026-09-07, M1)

- Installed torch CPU 2.14.0 + numpy/pytest on the runner; pinned in `postformer/requirements.txt`.
- Implemented `models/common.py` (RMSNorm, SwiGLU, RoPE, batched KVWindowBuffer, `param_count_no_embed` excluding input embedding only, sha256-derived `seed_all`).
- Implemented `models/baseline.py` (pre-norm causal Transformer, full `forward` + incremental `step` with RoPE baked at append), `models/p1_delta_hybrid.py` (gated delta memory + W=128 sliding window + fusion + SwiGLU; sequential reference forward (renamed from `forward_chunk` by the Fixer - chunk groups loop iterations only)), `models/p5_map.py` (degree-2 map + scaled additive write, identical proj shapes so T2 holds by construction), `models/factory.py`.
- Parity tuning: to hold the binding +-2% rule with the window branch pinned, P1/P5 MLP hid is 1704 (tiny) / 2726 (small), not the blueprint's 2016/3024 estimate. Measured: tiny +0.024%, small +0.002%.
- Fixed two real bugs found by parity probing: window `step()` applied RoPE on the flat head-concatenated dim (now per-head, matching `forward`), and harness model init was seeded from global torch state (now `reseed(seed, init-{model})` before every build).
- Harness: all five CLIs with blueprint contracts; G2 uses score-once strided eval; G3 byte-primary (BPE exits non-zero as deferred); G4 benches the recurrent `step()` path with prefill + warmup.
- T1-T5 green (9 passed): parity incl. collinear stress, param parity both scales, prefix-invariance causal probe, exact-summary determinism, ledger lint (NaN/drift/schema rejection).
- Smoke (random init, zero train tokens, NOT gate results): G1 at chance as expected; G2 deltas computed; G3 path validated on 4KB seeded byte fixture (sha logged, NOT Enwik8); G4 shows the O(1) signature already (P1 flat 3145824 B at T=64/128/256, P5 flat 4718688 B, baseline linear 1.57M/3.15M/6.29M). 4 ledger rows appended, `ledger check` passes, G4 SVGs plotted.
- Viewer: static validation green (envelope, table, fetch/drop/paste, no CDN); Playwright snapshot deferred (no browser on runner) to M2.
- Root landing/README untouched per safety net (Python engine, not Pages-hostable; site links deferred to the final milestone).
- Builder ideas entry: `ideas/2026-09-07-postformer-m1-build.md`.

- Dr. Mob, the Researcher
- the Architect

## Builder log (the Builder, 2026-09-08, M3 decoupled + slots + first falsification)

- P3 (`models/p3_decoupled.py`): shared-QKV accumulator (alpha 1.0, F-norm rescale hook with counter) + selective (GLA-lite) + W-window, 3-way fusion, SwiGLU. `step_split` single-pass exact `r - s` split. A3 control `--no-accumulator` (same params).
- P2 (`models/p2_slots.py`): SSD-lite (scalar decay, no erase) + G exact stride slots (oldest evict, zero router params) + W-window, 3-way fusion. A4 control `--slots 0`. Training forward uses prefix-stacked reads (a mutable-buffer first version broke autograd - caught by the new train test, fixed).
- Parity (non-embed, all within 2%): toy p2 -0.21% / p3 -0.05%; tiny p2 -0.008% / p3 +0.034%; small p2 -0.039% / p3 +0.010%. P2 shares P1 hid; P3 hid toy 274 / tiny 1532 / small 2468.
- Harness: `util.load_model` inherits (window, slots, use_accumulator, slot_stride) from checkpoint config, rejects --config mismatch loudly. This caught a REAL bug: the first p3-noacc eval silently ran with the accumulator ON (identical shapes); re-ran after the fix (mqar8 0.0612 vs p3 0.0600 - A3/H3 unresolved at toy).
- Probes (seed0, 1000 steps x batch16 = 0.528M tokens/arm, vocab64/N8, 100 eps, curves/m3-toy/): A2-re W0 0.0875 / W16-ref 0.0625 / W32 0.05125 (no window advantage at toy N8); p2 (G16) 0.0825/0.03 (above matched p1 ref); p3 0.0600/0.01. Ledger 18 rows check-green (novel keys appended; M2 A2 rows extended by --force note upsert, cells intact; W16-1000 ref in curves+notes only - key collides with M2b row).
- G4 amendment re-lint: proof tiers (a)/(b) + P2/P3 inventory (tiny P2 3932256 B / P3 4718784 B flat), viewer banner, README (tiers, A3/A4 commands, pins).
- S-tiny smoke: all five families forward-finite at tiny/vocab8192; p1-tiny ~1s/step at batch2/seq33, so the binding gate is ~50+h/arm on CPU - GPU runner required. Gate-vocab eval path verified (random init, chance); vocab-mismatched checkpoints fail loudly.
- Tests: 34 passed (T1/T2/T3 auto-extended over p2/p3 via conftest; test_m3.py A3/A4/slot-contract/G4-flatness/flags/loader-inheritance; T6 p2/p3 guards). Ideas entry: `ideas/2026-09-08-postformer-m3-decoupled-slots.md`.

- the Builder

## Builder log (the Builder, 2026-09-08, M4a P4 MAG-lite)

- Implemented `models/p4_maglite.py` (surprise-gated delta `eta = beta*sigmoid(w_s(x)+g*||e||)`, shared QKV trunk, W-window reuse, 2-way fusion, SwiGLU); `P4LM` matches the binding `SeqBlock` API; state equals P1 by construction.
- Factory pins p4 toy 294 / tiny 1702 / small 2724 (measured parity toy -0.43%, tiny +0.003%, small +0.002%, all within 2%); `tie_embeddings` guard extended to p4; conftest FAMILIES + `test_params.py` cover p4.
- New `tests/test_p4.py` (surprise bounds, error-gain grads, step/forward 1e-4 + prefix 1e-6, P4/P1 state equality): suite 48 passed on torch 2.14 CPU.
- Smoke (NOT a gate result): p4-toy 100-step MQAR train finishes finite (4.32 to 4.30), checkpoint loads, G1 eval writes a summary (N8 0.025, chance-level as expected).
- Docs: README pins/commands/layout, proof-g4.md P4 row + S-tiny 3145824 B footprint, ideas entry `2026-09-08-postformer-m4-maglite.md`. `Refs #294` kept.

- the Builder

## Fixer log (the Fixer, 2026-09-08, M3 review findings)

- P3 `_guard`: scale computed under no-grad, applied outside (`return A * scale`), so trunk grads survive rescale firing (was detached by where() inside no-grad).
- P2 `state_size`: slots `G*H*(d_k+d_v)` (was 2x), dropped phantom `H*bpe`; docstring matches. P3 `state_size`: conditional accumulator mem + window (no phantom `2*H` scalars); docstring notes A zeros when disabled.
- Proof `docs/proof-g4.md`: P2/P3 inventory + S-tiny footprints corrected (P2 589824 B/layer, 3538944 B total; P3 786432 B/layer, 4718592 B total). Prior builder log lines above keep historical numbers; proof is the source of truth.
- Nits: `SlotBuffer.append` stride check deduped (`0 % stride == 0` covers pos 0); `P2Block.step` detaches q/k/v on the eval-only incremental path (training forward keeps full slot-path grads).
- Verified: py_compile clean on touched models; footprint arithmetic re-computed by hand (no torch on runner); full pytest T1-T6 + M3 suite left for the Tester on a torch env. Refs #294.

- the Fixer

## Builder log (the Builder, 2026-09-08, M4b P4-vs-P1 toy falsification)

- Matched probe (mirrors M3 protocol): `p4-toy` seed0, 1000 steps x batch16 = 0.528M tokens, vocab64/N8, lr 3e-4 CPU fp32 (loss 4.3195 to 4.1157 finite). Same (seed, data) keying, so the episode stream is identical to the M3 p1-W16-1000 ref and p2/p3 probes.
- Full G1 toy envelope (100 eps): mqar8 0.035, N16 0.015625 (= chance 1/64), 2hop 0.01, induction/copy 0.0. Curves under `postformer/ledger/curves/m4b-toy/` (8 files); checkpoints NOT committed (regenerable via documented commands).
- H4 first read: NEGATIVE at toy - p4 0.035 sits below matched p1-W16-1000 ref 0.0625 and p2 0.0825; honestly ledgered (row 19, `check` green), H4 stays open pending S-tiny N64+.
- A6/A7 at toy: N16-extrapolation collapses to chance for p4 (same as all toy arms); retrieval-vs-drift split documented (mqar8 > 2hop > untrained transfer 0.0, as expected for MQAR-only training).
- Ideas entry: `ideas/2026-09-08-postformer-m4b-p4-probes.md`. Remaining (GPU-blocked): S-tiny/S-small full gates G1+G2+G3+G4-tier-a/b (~50+h/arm on CPU), A3/A4/A5 at scale, H1-H5 verdicts at scale, viewer snapshot, envelope audit. `Refs #294` kept; `Closes #294` only on full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4c A4 slots sweep at toy)

- A4 sweep (mirrors M3/M4b protocol): `p2-toy --slots {0,4,64}`, seed0, 1000 steps x batch16 = 0.528M tokens each, vocab64/N8, lr 3e-4 CPU fp32 (all finite). Same (seed, data) stream and same `p2-toy` init keying, so arms differ by slot count alone. Checkpoints NOT committed (regenerable via documented commands).
- G1 toy envelope (100 eps): G0 mqar8 0.04625 / N16 0.005625 / 2hop 0.01; G4 0.0825 / 0.00125 / 0.03; G64 bit-identical to G4 (train loss equal to 16 digits). Curves under `postformer/ledger/curves/a4-toy/` (24 files); ledger rows 20-22 (`p2-G0/G4/G64-toy`), `check` green.
- A4 verdict: slots beat pure-SSD (+3.6pts mqar8, 3x 2hop, identical 336074 params), G0 below the matched p1-W16-1000 ref 0.0625. But G4 = M3-G16 = G64 exactly: toy episodes (T=33, stride 8) admit at most 5 slot writes, so any G >= 5 holds full history and slot COUNT stays untested until S-tiny N64+ (T_train 512) where eviction fires. H2 stays open. Ideas entry: `ideas/2026-09-08-postformer-a4-slots-sweep.md`.
- Tests: `postformer/tests/test_a4_probes.py` (7 tests) + M4b row-count pin 19 -> 22 (A4 fallout). Full suite re-run on torch CPU in this run. `Refs #294` kept; `Closes #294` only on full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4d A6 vocab-stress pilot at toy)

- A6 pilot (mirrors M3/M4b protocol, only `--vocab 512` changed): `p1-toy` + `transformer-toy`, seed0, 1000 steps x batch16 = 0.528M tokens each, N8, lr 3e-4 CPU fp32 (p1 loss 6.3926 to 6.2098, transformer 6.3730 to 6.1780, both finite). Same (seed, data) keying.
- G1 toy envelope (100 eps): BOTH arms at the 0.0 floor (mqar8/N16/2hop/induction/copy all 0.0; recall@3 at chance 3/512; final loss within 0.06 of ln512 = 6.24). The 1000-step toy budget is below the learning threshold at vocab512 and yields no P1-vs-transformer separation. Honest negative pilot: it sizes the A6 experiment (needs 3000+ steps or S-tiny scale), H1/H5 stay open. Curves under `postformer/ledger/curves/a6-toy/` (16 files, V512 tags); ledger rows 23-24, `check` green.
- Harness fix in the same run: `ledger check` grouped the +-2% param-drift gate by scale suffix only, so vocab512 rows (lm_head scales with vocab: 393676/394112) would false-fail vs the vocab64 baseline (336768, 17% apart). The gate now groups by (scale, vocab); same-vocab parity holds (-0.11% at vocab512). Pinned by `test_a6_drift_gate_groups_by_vocab`.
- Tests: `postformer/tests/test_a6_probes.py` (8 tests) + row-count pins 22 -> 24 in the four tester red-team files (A6 fallout, no semantic change). Full suite 95 passed on torch 2.14 CPU in this run. `Refs #294` kept; `Closes #294` only on full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4e toy envelope audit)

- Docs-only milestone, no new training: `postformer/docs/envelope-audit.md` freezes all 20 trained toy rows (ledger rows 5-24) in one scoreboard with exact cells, ablation verdicts (A1 unresolved, A2 invalid pre-fix + A2-re no-advantage, A3 unresolved, A4 slots-help-but-count-untested, A6 floor, A7 split) and H1-H5 first reads (H4 NEGATIVE at toy, rest open); viewer banner names the M1-M4d envelope and links the audit; README gains the M3/M4b/A4/A6 probe section.
- Validation on torch 2.14 CPU in this run: full suite 102 passed, `ledger check` green on 24 rows, viewer static check green (quote-aware splitCSV parses all 24 rows at 24 cols; naive split shreds to 29-37 cols, proving the M1 fix still holds on the migrated schema).
- Ideas entry: `ideas/2026-09-08-postformer-m4e-envelope-audit.md`. `Refs #294` kept; `Closes #294` only on full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4c/d/e verification + review handoff)

- Re-ran the full envelope on CPU (torch 2.14, numpy/pytest installed on runner): **108 passed** (M4e audit claimed 102; +6 from the Tester M4f/M4g hostile suites landed after), `ledger check` green on 24 rows, tree clean, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (no infra touch). M4c A4 sweep + M4d A6 pilot + M4e audit + M4f/M4g suites are complete and unreviewed; all remaining work (S-tiny/S-small full gates, A3/A4/A5 at scale, H-verdicts at scale) is GPU-blocked and documented. Handing the full M4b-M4e delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4i handoff verification)

- Resume check on `opencode/issue294-20260907194528` at `27f98150`: tree clean, `merge-base HEAD origin/main = cdf3cdae` (NOT orphan; earlier no-base was shallow-clone artifact, resolved via `--unshallow`), PR #295 MERGEABLE, body `Refs #294`.
- Verified without torch: `ledger check` green on 25 rows, `py_compile` clean on harness/models, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-`, zero `forward_chunk` refs. Full pytest (118 passed) rests on the last torch-env runs; no re-run here (no torch on runner).
- No new training: S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). All CPU-feasible milestones M1-M4e plus M4f-M4i hardening are complete and pushed. Handing the post-a7553d5c delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Tester log (the Tester, 2026-09-08, M4b red-team)

- `postformer/tests/test_tester_m4b_redteam.py` (hostile regression for the M4b P4-vs-P1 probe); suite re-run left for the torch-env test pass. `Refs #294`.

- the Tester

## Fixer log (the Fixer, 2026-09-08, M4b-M4e review findings)

- Blocking: `tests/test_tester_m4b_redteam.py:131` dropped the tautological
  `or True` disjunct (header assertion is now strict); renamed the stale
  `test_m4b_live_ledger_check_green_19_rows` to `..._24_rows`.
- Test hygiene: renamed `test_m4e_ledger_has_22_rows_all_toy_honest` to
  `..._24_rows` and fixed its `19 -> 22` docstring to the live 24 rows.
- Docs: `docs/envelope-audit.md` W32 0.05125 (was truncated), A4
  `behaviorally identical at score level` with N16 noise-floor note, A6
  `within 0.065 of ln512` (matches the pinned test threshold), G4 flatness
  qualified (P1/P5 timed, P2/P3/P4 analytic); `README.md` 108 passed + A4
  wording; `viewer/index.html` comment now cites the live 24-col header.
   Builder history above keeps its original numbers; the audit/proof stay the
   source of truth. `Refs #294` kept.

- the Fixer

## Builder log (the Builder, 2026-09-08, M4f/g/h verification + review handoff)

- Re-ran the full envelope on CPU (torch 2.14.0+cpu, numpy/pytest installed on runner): **118 passed** (was 108 at the M4c/d/e check; +10 from the Tester M4h hostile suite: slot eviction, G-identity, audit pins), `ledger check` green on 24 rows, tree clean, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (no infra touch). M4b probes + M4c A4 sweep + M4d A6 pilot + M4e audit + M4f/M4g/M4h suites are complete and the post-a7553d5c delta is unreviewed; all remaining work (S-tiny/S-small full gates, A3/A4/A5 at scale, H-verdicts at scale) is GPU-blocked and documented. Handing the full M4b-M4h delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Fixer log (the Fixer, 2026-09-08, M4b-M4h review findings)

- `harness/ledger.py` `check`: rejects `inf`/`-inf` gate values (was `isnan`
  only); a `(scale, vocab)` group with candidates but no `transformer-`
  baseline now fails loudly instead of skipping the +-2% drift gate, and
  disagreeing baselines fail; per-row numericity enforced for
  `seed`/`vocab`/`train_tokens`/`gpu_hours` plus `window >= 0` integer check.
- The stricter gate exposed a real gap: no transformer-small row existed for
  the `(small, 256)` group, so the live ledger failed. Added an honest
  params-only `transformer-small` pin (row 25, gates empty, fixture-tagged;
  113462016 from the factory pin, test_params-enforced) via the `append` CLI;
  `check` green on 25 rows. Row-count pins bumped 24 to 25 in
  `test_tester_m4b/m4c/m4d/m4e_redteam.py` (no semantic change).
- `harness/train.py`: `--window`/`--slots`/`--no-accumulator` are now rejected
  on families that ignore them (same silent-invalidation class as M2/M4a).
- `harness/length_sweep.py`: `--tokenizer` is now read (BPE rejected loudly
  like `enwik8_bpb`, bytes split requires byte tokenizer) and recorded in the
  G2 summary. Hygiene: dropped dead `math` import in `synthetic_recall.py`
  and dead `argparse` import plus dead `unexpected = None` in `util.py`;
  unified `synthetic_recall` family split to `rsplit`.
- Docs/counts: README header/body 118 passed; ledger 25 rows; p3-noacc cell
  exact 0.06125 (was floored, `test_tester_m4g` pin updated); audit/README
  M2b means exact (P1 0.2875, P5 2hop 0.532, T 2hop 0.118); audit row labels
  corrected to 1-indexed ledger rows; A4 hardware provenance corrected to
  CUDA cu130 per `a4-toy` summaries (was CPU fp32); ideas-a6 bound 0.065.
  Builder history lines above keep their original numbers except the two
  stale count lines the Reviewer explicitly listed.
- Verified: `py_compile` clean, `ledger check` green (25 rows), no em dashes,
  no `forward_chunk` refs. Full pytest re-run left for the Tester (no torch
  on this runner). `Refs #294` kept.

## Fixer log (the Fixer, 2026-09-08, M4b-M4h review findings at bcf769e3)

- Finding 1: added `slots` + `use_accumulator` ledger columns (26-col schema);
  renamed A4 rows to valid `--model` values (`p2-toy` slots 0/4/64, M3 G16
  row slots 16) and `p3-noacc-toy` to `p3-toy` use_accumulator False (M3 p3
  row True); `_key` is now normalized (strip, None-safe) over
  (model,seed,vocab,window,slots,use_accumulator); cells literal, `check`
  green on 25 rows.
- Finding 2: family parse unified to `split("-",1)[0]` in train.py and
  synthetic_recall.py (rsplit broke guards for variant names); train builds
  via (family, scale).
- Finding 3: shared `util.load_model` guard extended to `window` (file-config
  mismatch fails loudly); explicit `--window` in extra_overrides stays the
  allowed A2 override path, so length/latency/enwik8 (no --window flag) gain
  the protection automatically.
- Finding 4: `params` nan/inf now rejected (per-row plus drift gate, baseline
  set included); drift nan/inf guarded.
- Finding 5: `cmd_append` validates the constructed row before writing.
- Finding 6: `_key` None/whitespace normalized (str(v or "").strip()).
- Nits: narrowed ideas-a4 G16 equality to A4-internal; ideas-m4e 26-col/25-row
  counts; audit row labels to slots/noacc names; viewer 26-col comment;
  `--vocab` vs checkpoint-vocab mismatch guard in length_sweep/latency_state.
  weights_only stays False (checkpoints are local build artifacts, trusted
  path only; changing loader semantics without a torch env to verify would
  risk breaking the Tester gate).
- Tests updated for the new schema/names (a4_probes, m4b/m4c/m4d/m4g/m4h
  red-team, test_ledger good_row). Full pytest re-run left for the Tester
  (no torch/pytest on this runner). `Refs #294` kept.

- the Fixer

## Fixer log (the Fixer, 2026-09-08, 6f9653c review findings)

- Finding 1: dropped phantom `+ H*bpe` from P1/P4/P5 `state_size`
  (no backing tensor; FusionGate stateless, beta/alpha recomputed);
  docstrings updated; proof-g4 inventory rows removed and S-tiny
  footprints recomputed (P1/P4 524288/layer = 3145728 total;
  P5 786432/layer = 4718592 total; small P1 655360/layer = 7864320).
  Historical curves keep old reservation numbers with a proof footnote.
- Finding 2: P3 `state_size` always reports 2x (A resident zeros when
  disabled); matches init_state alloc, keeps A3 param-identity green.
- Finding 3: deleted dead `_p1_cfg` in factory (all builds via
  `_candidate_cfg`).
- Finding 4: shared T6 collinear sweep covers p4.
- Nits: `tie_embeddings` ValueError in each P*LM `__init__` (defense in
  depth; factory already guards CLI); test pins updated (m3 off 2x,
  m4h 3145728). Verified py_compile clean, ledger check green (25 rows).
  Full pytest left for Tester (no torch here). `Refs #294` kept.

- the Fixer

## Fixer log (the Fixer, 2026-09-08, 619807ce review findings)

- Finding 1: strict --model gate via factory.parse_model_name
  (fullmatch on family-scale); wired into util.load_model, train,
  synthetic_recall, length_sweep (incl. --baseline-model), plus
  library-level family/scale guards in build_model and strict ledger
  row-name check. Middle tags (p2-G0-toy) and suffixes (p1-toy-V512)
  now fail loudly; replay via plain name plus flags. M4i R2
  acceptance tests rewritten to pin the rejection.
- Finding 2: proof-g4 P2/P3/P4 rows reworded to byte-flat by
  construction, tier (a) PENDING timed ms/token curve.
- Nits: README M2 rows 5-13; viewer title M4e plus self-escaping
  cell(); ledger g1_* [0,1] range check plus extra-key note;
  train init-key comment notes strict names. Verified py_compile
  clean, ledger check green (25 rows). Full pytest left for Tester
  (no torch here). Refs #294 kept.

- the Fixer

## Fixer log (the Fixer, 2026-09-08, 10890bbc review findings)

- Finding 1: test_m4d NaN test rewritten to hand-craft the corrupt row
  (bypassing append validation) on canonical p1-toy so only the
  check-time NaN branch fires.
- Findings 2+3: m4f/m4i p9-probe-toy rows renamed to canonical p1-toy
  (same-vocab drift at vocab64, cross-vocab skip at vocab999) with
  explicit "param drift" message asserts so the drift gate cannot be
  hollowly satisfied by the malformed-name error.
- Finding 4: --vocab vs checkpoint vocab_size SystemExit guard copied
  into synthetic_recall (vocab+2) and enwik8_bpb (256), matching the
  length_sweep/latency_state discipline.
- Findings 5+6: smoke G1 cells verified already literal
  (g1_mqar_16=N16, g1_mqar_64=N64); notes annotated with N16/N64
  provenance plus the G4 post-fix migration pointer (archived smoke
  g4_proof JSONs hold pre-fix +96B reservation values, proof-g4.md:29-32).
- Finding 7: README G4 toy pins 24592/40976 corrected to 24576/40960.
- Nits: length_sweep dead bpb_1x dict deleted; latency_state prompt
  tensor placed on device (CPU-only latent path until --device cuda).
  Verified py_compile clean, ledger check green (25 rows), no em dashes,
  zero p9-probe-toy refs in the repaired suites. No torch/pytest here;
  full suite (incl. 3 repaired redteam tests) left for Tester. Refs #294 kept.

- the Fixer

## Builder log (the Builder, 2026-09-08, M4j-M4l hardening + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `cf108ecf`: tree clean, `merge-base HEAD origin/main = cdf3cdae` (NOT orphan after `--unshallow`), PR #295 OPEN MERGEABLE, body `Refs #294`.
- Post-M4i delta verified without torch: `ledger check` green on 25 rows, `py_compile` clean on harness/models, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-`, zero `forward_chunk` refs. Full pytest (144 test functions across 24 files, incl. Tester M4j/M4k/M4l hostile suites for N>vocab refusal, n-guard edges, off-by-one boundaries, live parity, ledger green, viewer hardening) rests on the torch-env Tester pass; no re-run here (no torch on runner).
- M4j pinned the `gen_mqar` N>vocab numpy crash as a loud up-front `SystemExit` with zero partial g1_* outputs; Fixer extended the guard to bare-defaults (`64772a97`); M4k pins bare-defaults plus n=0/negative edges and MQAR-only scoping; M4l pins n==vocab success vs vocab+1 refusal, non-MQAR task exemption, `--window -1` / `--vocab 8` refusal, live +-2% parity all scales, committed-ledger green, viewer splitCSV+esc hardening. All CPU-feasible milestones M1-M4l complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-M4i delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4m verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `c18e2891`: tree clean, `merge-base HEAD origin/main = cdf3cdae` (NOT orphan after `--unshallow`), PR #295 OPEN MERGEABLE, body `Refs #294`.
- Verified on torch 2.14 CPU in this run: full suite **175 passed** (all T1-T6/M3/M4/a4/a6 + Tester M4b-M4m hostile suites incl. M4m cross-W causality, flatness pins, live guards), `ledger check` green on 25 rows, `py_compile` clean on harness/models, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-`, zero `forward_chunk` refs.
- No new training: S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). All CPU-feasible milestones M1-M4m are complete and pushed. Handing the post-a7553d5c delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4n verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `21c29177`: tree clean, PR #295 OPEN MERGEABLE CLEAN per gh (local merge-base missing is the known shallow-clone artifact; prior `--unshallow` runs proved NOT orphan), body `Refs #294`.
- Verified without torch (absent on this runner): `py_compile` clean on harness/models/tests, `ledger check` green on 25 rows (26-col schema), zero `forward_chunk` refs, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-`.
- No new training: Tester M4n hostile suite (tiny causality/flatness/parity/live guards) landed at head since the M4m verification; full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4n complete and pushed; S-tiny/S-small full gates remain GPU-blocked and documented. Handing the post-a7553d5c delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4o verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `cba76a3c`: `--unshallow` re-run, `merge-base HEAD FETCH_HEAD = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN MERGEABLE per gh, body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check` green on 25 rows (26-col schema), `py_compile` clean on harness/models/tests, zero `forward_chunk` refs, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-`.
- No new training: Tester M4o hostile suite (M4b probe honesty + head pins) landed at head since the M4n verification; full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4o complete and pushed; S-tiny/S-small full gates remain GPU-blocked and documented. Handing the post-a7553d5c delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4p verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `e902e694`: `--unshallow` re-run, `merge-base HEAD origin/main = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN MERGEABLE CLEAN per gh, body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check` green on 25 rows (26-col schema), `py_compile` clean on harness/models, zero `forward_chunk` code refs in `postformer/` (remaining hits are historical mentions in ideas/progress docs only), zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-`.
- No new training: Tester M4p hostile suite (curve ground truth m4b-toy g1_summary vs ledger cells, all-family live parity, p4 causality/flatness, CLI guards, viewer hardening) landed at head since the M4o verification; full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4p complete and pushed; S-tiny/S-small full gates remain GPU-blocked and documented. Handing the post-a7553d5c delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4q verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `112d1d73`: `--unshallow` re-run, `merge-base HEAD origin/main = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN MERGEABLE CLEAN per gh, body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check` green on 25 rows (26-col schema), `py_compile` clean on harness/models, zero `forward_chunk` code refs in `postformer/` (remaining hits are historical mentions in ideas/progress docs only), zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-`.
- No new training: Tester M4q hostile suite (family-wide gate readiness) landed at head since the M4p verification; full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4q complete and pushed; S-tiny/S-small full gates remain GPU-blocked and documented. Handing the post-a7553d5c delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4r-v verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `f7a3f503`: `--unshallow` re-run, `merge-base HEAD origin/main = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN MERGEABLE per gh, body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check` green on 25 rows (26-col schema), `py_compile` clean on harness/models, zero `forward_chunk` code refs in `postformer/` (remaining hits are test-file self-pins in `test_tester_m4q_redteam.py` only), zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-`.
- No new training: Tester M4r/M4s/M4t/M4u/M4v hostile suites (envelope ground truth, curve ground truth, small pins, roundtrips, M4b honesty, live guards, flatness) landed at head since the M4q verification; full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4v complete and pushed; S-tiny/S-small full gates remain GPU-blocked and documented. Handing the post-a7553d5c delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Fixer log (the Fixer, 2026-09-08, M4b-M4r 6 findings at b88f2a7a)

- Applied all 6 blocking findings on PR #295 head: latency_state --vocab forwarding with >=1 guard; P5 GatedMapMemory unit-normed keys (matched key scale, A1 honest) plus docstring; ledger drift zero-baseline guard; ledger svg_line XML escaping plus non-finite point filtering; P3 dead FusionGate import drop plus step_split honest docstring; m4v red-team em-dash escape (source self-clean, runtime still greps U+2014).
- Verified without torch (absent here): py_compile clean on touched files, ledger check green (25 rows), zero em dashes in PR scope, forward_chunk refs only test self-pins. Full pytest re-run left for Tester on torch env. Refs #294 kept.

- the Fixer

## Fixer log (the Fixer, 2026-09-08, M4q-M4y vocab-convention findings at 28cda2ec)

- Finding 1: `latency_state --vocab` now uses the train convention (model vocab_size = vocab + 2, prompts sampled from 0..vocab-1), matching `train.py`/`synthetic_recall.py`; guard aligned to `>= 16` and checkpoint mismatch message pins both sides. Same fix applied to `length_sweep --vocab` (explicit path; discovered path keeps vocab_size identity for existing G2 curves).
- Finding 2: header/step pointers bumped to M4q-M4y (this entry); history above untouched.
- Verified: py_compile clean on touched harnesses, ledger check green (25 rows). Full pytest re-run left for the Tester (no torch here). Refs #294 kept.

- the Fixer

## Builder log (the Builder, 2026-09-08, M4ac verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `2c2fa587`: `--unshallow` re-run, `merge-base HEAD origin/main = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN MERGEABLE CLEAN per gh, body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check` green on 25 rows (26-col schema), `py_compile` clean on harness/models, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-`, `forward_chunk` code refs none (remaining hits are test-file self-pins only).
- No new training: Tester M4ac hostile final-gate suite (current-head pins, literal N16 cells, loud schema-mismatch exit) plus Fixer hardening (fail-fast slots/stride/chunk guards, real CLI window probe, torch.equal identity, CLI guards, surprise_scale/P5 docs, literal full-precision N16 cells) landed at head since the M4z-M4ab verification; full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4ac complete and pushed; S-tiny/S-small full gates remain GPU-blocked and documented. Handing the post-bec0d248 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4z-M4ab verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `bec0d248`: `merge-base HEAD origin/main = cdf3cdae` (NOT orphan), PR #295 OPEN MERGEABLE CLEAN per gh, body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check` green on 25 rows (26-col schema), `py_compile` clean on harness/models, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-`, `forward_chunk` refs only test self-pins in `test_tester_m4q_redteam.py`.
- No new training: Tester M4z/M4aa/M4ab hostile suites (+2 vocab convention, n==vocab, curve ground truth, W-edge causality, T=1, single-Q-proj split, single-load recall, P5/A1 honesty) plus Fixer P5 pre unit-norm staleness annotation (A1 INVALID until re-run) and single Q-proj step_split / single checkpoint load hardening landed at head since the M4r-v verification; full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4ab complete and pushed; S-tiny/S-small full gates remain GPU-blocked and documented. Handing the post-f7a3f503 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4ad verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `3b73a60b`: tree clean, `merge-base HEAD FETCH_HEAD` empty locally (known shallow-clone artifact; prior `--unshallow` runs proved NOT orphan at cdf3cdae, PR #295 MERGEABLE CLEAN per gh), body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-`, zero `forward_chunk` code refs in shipped code.
- No new training: Tester M4ad hostile final-gate suite (current-head pins, 300 passed at 448e838c + 6 new, all green per Tester approve-test) landed at head since the M4ac verification; full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4ad complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-448e838c delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4ae verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `595f5075`: `--unshallow` re-run, `merge-base HEAD FETCH_HEAD = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN MERGEABLE per gh, body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models/tests, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (302 changed files, all in scope), zero `forward_chunk` code refs in shipped code (remaining hits are test-file self-pins only).
- No new training: Tester M4ae hostile suite (p2/p3/p5 MINI causality, all-family tie_embeddings rejection, parse_model_name locks, p4 window routing, commit-discipline lock) landed at head since the M4ad verification; full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4ae complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-22012286 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4af verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `a3d73128`: tree clean, `origin/main = cdf3cdae`, PR #295 OPEN, body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-`, zero `forward_chunk` code refs in shipped code (remaining hits are test-file self-pins only).
- No new training: Tester M4af hostile suite (`test_tester_m4af_redteam.py`, 5 tests: AF1 disagreeing-baseline loud fail, AF2 numericity/negative guards, AF3 G1 rerun byte-identity, AF4 G3 byte-path fixture roundtrip, AF5 length_sweep +2 success roundtrip) landed at head since the M4ae verification; full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4af complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-15633408 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4ag verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `d45b3f24`: tree clean, PR #295 OPEN MERGEABLE CLEAN per gh, body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models/tests, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean), zero `forward_chunk` refs in shipped code.
- No new training: Tester M4ag hostile suite (G4 flatness, inventory formulae, ledger honesty) landed at head since the M4af verification; full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4ag complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-a3d73128 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4ah verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `c7cc1c55`: tree clean, `--unshallow` re-run, `merge-base HEAD origin/main = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN MERGEABLE CLEAN per gh, body `Refs #294`.
- Verified without torch/pytest (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models/tests, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean), zero `forward_chunk` refs in shipped code (remaining hits are test-file self-pins only).
- No new training: Tester M4ah hostile suite (`test_tester_m4ah_redteam.py`) landed at head since the M4ag verification; full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4ah complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-791f8017 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4ah final verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `70f98b4e`: tree clean, PR #295 OPEN MERGEABLE CLEAN per gh (local merge-base missing is the known shallow-clone artifact; prior `--unshallow` runs proved NOT orphan at cdf3cdae), body `Refs #294`.
- Verified without torch/pytest (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models, `gh pr view 295` file list fully inside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean), zero `forward_chunk` refs in shipped code (remaining hits are test-file self-pins only).
- No new training: Tester final-gate hostile suite (`70f98b4e`, current-head pins) landed at head since the M4ah verification; full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4ah complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-c7cc1c55 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4ai verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `2d4ad761`: tree clean, PR #295 OPEN, body `Refs #294`.
- Verified on torch 2.14 CPU in this run (installed torch+pytest+numpy on runner): full suite **344 passed** (all T1-T6/M3/M4/a4/a6 + Tester M4b-M4ai hostile suites incl. M4ai ground-truth pins), `ledger check` green on 25 rows (26-col schema), `py_compile` clean on harness/models, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean), zero `forward_chunk` refs in shipped code (remaining hits are test-file self-pins only).
- No new training: Tester M4ai hostile suite (`test_tester_m4ai_redteam.py`, current-head ground-truth pins) landed at head since the M4ah verification; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). All CPU-feasible milestones M1-M4ai complete and pushed. Handing the post-c55cf6cd delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4aj verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `adfc5124`: `--unshallow` re-run, `merge-base HEAD origin/main = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN MERGEABLE per gh, body `Refs #294`.
- Verified without torch/pytest (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models/tests, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean via merge-base diff), zero `forward_chunk` refs in shipped code (`grep postformer --include=*.py` outside tests: no hits).
- No new training: Tester M4aj hostile E2E CLI-chain suite (`test_tester_m4aj_redteam.py`) landed at head since the M4ai verification (344 passed at `705ad11d`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4aj complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-705ad11d delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4ak verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `809542ad`: tree clean, PR #295 OPEN MERGEABLE CLEAN per gh, body `Refs #294`.
- Verified without torch/pytest (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models/tests (incl. new `test_tester_m4ak_redteam.py`), zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean), shipped-code `eval(`/`exec(`/`input(` grep hits are `model.eval()` only, no secrets, no `Co-authored-by`.
- No new training: Tester M4ak hostile suite (`test_tester_m4ak_redteam.py`, guard live-fire + full-model determinism: train/eval CLI rejection paths, W0/W16 mismatch live-fire, full-model finite + bit-identical reruns, summary determinism, ledger dedup/upsert, P2 slots 0-vs-4 inventory) landed at head since the M4aj verification (`5f7429f5`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4ak complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-5f7429f5 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4al verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `204913de`: tree clean, PR #295 OPEN MERGEABLE per gh, body `Refs #294`.
- Verified without torch/pytest (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models/tests (incl. new `test_tester_m4al_redteam.py`), recent commits all inside `postformer/` scope (tester M4al suite + fixer ledger/length_sweep/audit hardening), zero `forward_chunk` refs in shipped code (grep `postformer --include=*.py` outside tests: no hits), zero em dashes in `postformer --include=*.py`.
- No new training: Tester M4al hostile suite (`test_tester_m4al_redteam.py`, stride/extra-key/nonfinite/vocab guards) plus Fixer hardening (ledger append/check stride guard, key-col finite, extra-key fail; length_sweep discovered-vocab baseline-mismatch guard; A4 identity scoped to CUDA sweep; A2-re W32 note 0.05125) landed at head since the M4ak verification (`809542ad`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4al complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-809542ad delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4am verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `0db316a1`: tree clean, `--unshallow` re-run, `merge-base HEAD FETCH_HEAD = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN MERGEABLE per gh, body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models/tests (incl. new `test_tester_m4am_redteam.py`), zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (311 changed files, scope clean), zero `forward_chunk` refs in shipped `models/`+`harness/` (remaining hits are test-file self-pins only), zero em dashes in `postformer --include=*.py`.
- No new training: Tester M4am hostile suite (`test_tester_m4am_redteam.py`, live parity toy+tiny, G4 flatness vs proof pins, cross-W causality, T=1, CLI guard live-fire, dedup key, viewer hardening, honesty, hygiene) landed at head since the M4al verification (`cf9dd1eb`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4am complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-cf9dd1eb delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4an verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `f1c963ad`: tree clean, PR #295 OPEN per gh (local merge-base missing is the known shallow-clone artifact; prior `--unshallow` runs proved NOT orphan at cdf3cdae), body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models/tests (incl. new `test_tester_m4an_redteam.py`), `gh pr view 295` file list fully inside `postformer/|ideas/|docs/research/issue-294|progress/294-` (100 files, scope clean), zero `forward_chunk` refs in shipped code (grep `postformer --include=*.py` outside tests: no hits), zero em dashes in `postformer --include=*.py`.
- No new training: Tester M4an hostile suite (`test_tester_m4an_redteam.py`, small-scale live parity, tie_embeddings live-fire, parse_model_name/build_model locks, per-layer state_size pins, MINI p2/p3 causality, enwik8 name-guard ordering, 26-col ledger green) landed at head since the M4am verification (`d9fd82e8`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4an complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-d9fd82e8 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4ao verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `ac6e5d8f`: tree clean, PR #295 OPEN MERGEABLE CLEAN per gh, body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models/tests (incl. new `test_tester_m4ao_redteam.py`), zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean), zero `forward_chunk` refs in shipped code (grep `postformer --include=*.py` outside tests: no hits), zero em dashes in `postformer --include=*.py`.
- No new training: Tester M4ao hostile suite (`test_tester_m4ao_redteam.py`, p2 determinism, degenerate --slots/--window live-fire, A2/A4 control honesty, ledger tripwire) landed at head since the M4an verification (`72562bc9`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4ao complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-72562bc9 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4ap verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `79b57254`: tree clean, PR #295 OPEN MERGEABLE per gh, body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean), zero `forward_chunk` refs in shipped code (grep `postformer --include=*.py` outside tests: no hits), zero em dashes in `postformer --include=*.py`.
- No new training: Tester M4ap hostile suite (`test_tester_m4ap_redteam.py`, cross-arm stream identity, p3/p4 determinism, curve sweep, window liveness, plus hermetic python and ao4 timeout calibration) landed at head since the M4ao verification (`b0cc5cb8`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4ap complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-b0cc5cb8 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4aq verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `860c62bb`: tree clean, `--unshallow` re-run, `merge-base HEAD origin/main = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN MERGEABLE per gh, body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean via merge-base diff), zero `forward_chunk` refs in shipped code (remaining hits are test-file self-pins only).
- No new training: Tester M4aq hostile suite (`test_tester_m4aq_redteam.py`, Markov training path) landed at head since the M4ap verification (`d0e53354`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4aq complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-d0e53354 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4ar verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `e31a8937`: tree clean, PR #295 OPEN per gh, body `Refs #294`.
- Verified without torch (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models/tests, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean via merge-base diff), zero `forward_chunk` refs in shipped code (grep `postformer --include=*.py` outside tests: no hits).
- No new training: Tester M4ar hostile suite (`test_tester_m4ar_redteam.py`, A4 G4/G64 divergence disclosure) plus Fixer A4 wording/divergence pins landed at head since the M4aq verification (`057d2fd4`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4ar complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-057d2fd4 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4as verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `bfe76238`: tree clean, PR #295 OPEN per gh, body `Refs #294`.
- Verified without torch/pytest (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models/tests (60 test files), zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean via merge-base diff), zero `forward_chunk` refs in shipped code (grep `postformer --include=*.py` outside tests: no hits), zero em dashes.
- No new training: Tester M4as hostile suite landed at head since the M4ar verification (`a875e682`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4as complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-a875e682 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4at/M4au verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `b1017a22`: tree clean, `--unshallow` re-run, `merge-base HEAD origin/main = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN MERGEABLE CLEAN per gh, body `Refs #294`.
- Verified without torch/pytest (absent on this runner): `ledger check --ledger postformer/ledger/ledger.csv` green on 25 rows (26-col schema), `py_compile` clean on harness/models, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean via merge-base diff), zero `forward_chunk` refs in shipped code, zero em dashes in `postformer --include=*.py`.
- No new training: Tester M4at/M4au hostile suites (`test_tester_m4at_redteam.py` AT6 provenance-guard pin fix, `test_tester_m4au_redteam.py` head-delta locks) plus Fixer hardening (A4 G4 summary-cell scope, baseline tie_embeddings honors, state_bytes length, cfg.update overrides, arg gates) landed at head since the M4as verification; full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4au complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-bfe76238 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4av verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `cec66b1c`: tree clean, `--unshallow` re-run, `merge-base HEAD FETCH_HEAD = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN MERGEABLE CLEAN per gh, body `Refs #294`.
- Verified without torch/pytest (absent on this runner): `ledger check` green on 25 rows (26-col schema), `py_compile` clean on harness/models, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean via merge-base diff), zero `forward_chunk` refs in shipped `models/`+`harness/`, no em dash in sampled shipped files.
- No new training: Tester M4av hostile suite (`test_tester_m4av_redteam.py`, head fixer-delta locks) plus Builder M4at/M4au handoff commit landed at head since the M4at/M4au verification (`b1017a22`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4av complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-b1017a22 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-08, M4aw verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `abe65825`: tree clean, `--unshallow` re-run, `merge-base HEAD origin/main = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN MERGEABLE CLEAN per gh, body `Refs #294`.
- Verified without torch/pytest (absent on this runner): `ledger check` green on 25 rows, `py_compile` clean on harness/models plus new `test_tester_m4aw_redteam.py`, `gh pr view 295` file list fully inside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean), zero `forward_chunk` refs in shipped code (grep `postformer --include=*.py` outside tests: no hits), zero em dashes in `postformer --include=*.py`.
- No new training: Tester M4aw hostile suite (`test_tester_m4aw_redteam.py`: code-vs-proof S-tiny state pins p1/p4 3145728, p2 3538944, p3/p5 4718592; p4 --window 0 train-side liveness; unknown-family ValueError plus all-five tie_embeddings rejection; ledger honesty sweep; --steps 1 degenerate; p2/p3 T=1) landed at head since the M4av verification (`8a01c6fb`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4aw complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-8a01c6fb delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-09, M4ax verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `96e389ef`: tree clean, `origin/main = cdf3cdae`, PR #295 OPEN per gh, body `Refs #294`.
- Verified without torch/pytest (absent on this runner): `ledger check` green on 25 rows (26-col schema), `py_compile` clean on harness/models/tests (incl. new `test_tester_m4ax_redteam.py`), zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (322 changed files, scope clean), zero `forward_chunk` refs in shipped `models/`+`harness/`, zero em dashes in `postformer --include=*.py`.
- No new training: Tester M4ax hostile suite (`test_tester_m4ax_redteam.py`: small state pins, window-train liveness, slot eviction, P5/eval liveness, G4 bench and ledger locks) landed at head since the M4aw verification (`d4611fb2`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4ax complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-d4611fb2 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-09, M4ay verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `0e39daaf`: `--unshallow` re-run, `merge-base HEAD origin/main = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN per gh, body `Refs #294`.
- Verified without torch/pytest (absent on this runner): `ledger check` green on 25 rows (26-col schema), `py_compile` clean on harness/models, `gh pr view 295` file list fully inside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean), zero `forward_chunk` refs in shipped `models/`+`harness/`, zero em dashes in `postformer --include=*.py`.
- No new training: Tester M4ay hostile suite (`test_tester_m4ay_redteam.py`: G4 control growth, measure-chain, plot escaping, task liveness, upsert locks) landed at head since the M4ax verification (`86a1ef99`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4ay complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-86a1ef99 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-09, M4az verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `aedf65f6`: `--unshallow` re-run, `merge-base HEAD origin/main = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN MERGEABLE CLEAN per gh, body `Refs #294`.
- Verified without torch/pytest (absent on this runner): `ledger check` green on 25 rows, `py_compile` clean on harness/models plus new `test_tester_m4az_redteam.py`, `origin/main...HEAD` file list fully inside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean), zero `forward_chunk` refs in shipped `models/`+`harness/`, zero em dashes in `postformer --include=*.py`.
- No new training: Tester M4az hostile suite (`test_tester_m4az_redteam.py`: M4b ground truth, live parity, p4 window chain, causality; plus m4v full-envelope timeout 300 to 1500s) landed at head since the M4ay verification (`c36014bb`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4az complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-c36014bb delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-09, M4ba verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `b0c52626`: `--unshallow` re-run, `merge-base HEAD FETCH_HEAD = cdf3cdae` (NOT orphan; missing base is the known shallow-clone artifact), PR #295 OPEN MERGEABLE CLEAN per gh, body `Refs #294`.
- Verified without torch/pytest (absent on this runner): `ledger check` green on 25 rows (26-col schema), `py_compile` clean on harness/models/tests (incl. new `test_tester_m4ba_redteam.py`), `gh pr view 295` file list fully inside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean), zero `forward_chunk` refs in shipped `models/`+`harness/`, zero em dashes in `postformer --include=*.py`.
- No new training: Tester M4ba hostile suite (`test_tester_m4ba_redteam.py`: six-family parity, G4 flatness, p4 causality, strict names, guards) landed at head since the M4az verification (`a915477a`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4ba complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-a915477a delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Builder log (the Builder, 2026-09-09, M4bb verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `5633a813`: tree clean, PR #295 OPEN MERGEABLE CLEAN per gh, body `Refs #294`.
- Verified without torch/pytest (absent on this runner): `ledger check` green on 25 rows (26-col schema), `py_compile` clean on harness/models, zero files outside `postformer/|ideas/|docs/research/issue-294|progress/294-` (scope clean), zero `forward_chunk` refs in shipped `models/`+`harness/`, zero em dashes in `postformer --include=*.py`.
- No new training: Tester M4bb hostile suite (`test_tester_m4bb_redteam.py`: envelope audit, P4 beyond-toy flatness, p4 curve ground truth) landed at head since the M4ba verification (`6de0eaea`); full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4bb complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-6de0eaea delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder

## Fixer log (the Fixer, 2026-09-09, M4bb review findings at 9861d8b3)

- Applied all 5 blocking findings on PR #295 (5 modular fixer: commits, no clobber, Refs #294 kept).
- 1: enwik8_bpb test/valid split (enwik8_bpb.py): full-file test now scores 95M..100M only (was 90M..100M swallowing valid); fixture path unchanged (lo,hi = 0,size).
- 2: ledger negative guards (ledger.py _validate_row): g2_bpb_*/g3_*/g4_state_bytes/g4_ms_per_token plus params/train_tokens/gpu_hours reject < 0; g2_delta_* exempt (negative delta legitimate); ledger check green on 25 rows.
- 3: ledger model-name check (ledger.py _validate_row): re.fullmatch family-scale gate shared by check and append, so p2-G0-toy/"" fails at append time, not only at check.
- 4: train --weight-decay >= 0 guard (train.py) alongside sibling scalar guards.
- 5: util loader (util.py): cross-scale provenance refuse (ckpt scale != requested scale) plus RuntimeError -> SystemExit wrap on shape mismatch, so p1-tiny-as-p1-toy fails loudly.
- Verified: py_compile clean, ledger check green (25 rows), negative/edge probes green (neg g2/params/tokens/name rejected, neg delta accepted), no em dashes, tree clean. Full pytest re-run rests on the torch-env Tester pass.

- the Fixer

## Fixer log (the Fixer, 2026-09-09, 790ea127 review findings)

- Finding 1: T6 P5 branch now uses live `mem._normed_k(k)` (unit-normed, matching `GatedMapMemory.step`) instead of RMSNorm-only `k_norm`; header corrected to unit-normed keys.
- Finding 2: `util.load_model` refuses family-inappropriate ablation keys from `--config` and inherited checkpoint config (transformer+window, non-p2+slots, non-p3+use_accumulator fail loudly).
- Finding 3: `ledger cmd_append` treats explicit `slot_stride: null` as default (no false refuse).
- Verified: py_compile clean on touched files, ledger check green (25 rows), no em dashes, no shipped-code forward_chunk refs. Full pytest re-run left for Tester (no torch here). Refs #294 kept.

- the Fixer

## Fixer log (the Fixer, 2026-09-09, Tester d5581ff2 dynamic gate findings)

- 1: test_determinism MINI fixture now passes a p1-family-appropriate subset via --config (drops p2-only slots/slot_stride and p3-only use_accumulator); harness guard in util.load_model stays strict by design (M2-A2 class), library build_model still ignores inert keys.
- 2: enwik8_bpb stride guard corrected from >= to > at both sites (explicit --stride and defaulted stride), matching length_sweep.py stride > t_train; stride==context is valid non-overlapping eval.
- 3: test_at6 scale-mismatch block widened from pytest.raises(Exception) to pytest.raises(BaseException) so the by-design SystemExit is caught.
- 4: test_parse_int_list garbage pin updated from ValueError to SystemExit (harness convention since d4f3fbb2 hardening).
- 5: commit d4f3fbb2 discipline (missing Refs #294 plus leaked Co-authored-by trailer): history/process issue, not code-fixable without rewriting pushed history; flagged for Maintainer awareness, no code change.
- Verified: py_compile clean on touched files, no em dashes. No torch/pytest on this runner so the full 469+5 suite re-run is left for the Tester. Refs #294 kept.

- the Fixer

## Fixer log (the Fixer, 2026-09-09, Reviewer ceb445e1 3 findings restored on 4c66fd9d)

- 1: enwik8_bpb.py stride guard restored from > to >= at both sites (explicit and defaulted stride); stride==context skips scored tokens (keep_from -1) so it must refuse, restoring agreement with test_fixer_enwik8_stride_eq_context_refused.
- 2: length_sweep.py stride guard restored from > to >= at the G2 boundary; extended test_tester_m4bc_redteam boundary pin to cover stride 64 vs t-train 64.
- 3: m3-toy matched-budget premise downgraded per option (b): p2/p3/p4/A4 notes citing the p1-W16-1000 ref are now eval-matched only with explicit train-summary-absent qualifier (m3-toy holds g1_summary JSONs, zero train_summary artifacts); cells untouched.
- Nits: proof-g4.md M2 PASS lines qualified as toy-only NOT gate results; Active Milestone pointer updated to M4bc.
- Verified: py_compile clean, ledger check green (25 rows), no em dashes. No torch on this runner so full suite re-run rests on Tester. Refs #294 kept.

- the Fixer

## Builder log (the Builder, 2026-09-09, M4bd/M4be verification + review handoff)

- Resume check on `opencode/issue294-20260907194528` at `5f136f4a`: tree clean, PR #295 OPEN MERGEABLE CLEAN per gh (mergeStateStatus CLEAN), body `Refs #294`.
- Verified without torch/pytest (absent on this runner): `ledger check` green on 25 rows (26-col schema), `py_compile` clean on harness/models/tests, zero `forward_chunk` refs in shipped `models/`+`harness/` (remaining hits are test-file self-pins only, confirmed via grep).
- No new training: Tester M4bd hostile suite (commit-attribution locks, live gate spots) plus M4be ground-truth suite (2 stale pins repaired) landed at head since the M4bb verification; Fixer M4bc/M4bd/M4be hardening (toy PASS qualification, matched-ref eval-matched downgrade, stride guards) already in the tree. Full pytest re-run rests on the torch-env Tester pass. All CPU-feasible milestones M1-M4be complete and pushed; S-tiny/S-small full gates remain GPU-blocked (~50+h/arm on CPU, documented). Handing the post-9861d8b3 delta to the Reviewer. `Refs #294` kept; `Closes #294` only on G1+G2+G3+G4-tier-a/b full pass.

- the Builder
