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

- **Active Milestone:** M4e toy envelope audit complete on PR #295 (M1 + M2-toy + M3 + M4a/M4b toy falsification + A4 sweep + A6 pilot + audit gated-ready); next is S-tiny full gates (GPU-blocked).
- **Milestone 1 (M1: scaffold + first falsification, PR 1 target, Refs #294):** [x] `postformer/` scaffold with `requirements.txt` + README + proof appendix skeleton; [x] baseline Transformer S-tiny/S-small + param counter within 2 percent (tiny +0.024%, small +0.002%, committed `ledger/params/`); [x] harness five scripts with exact CLI contracts + seeding + ledger schema; [x] P5 map control + P1-minimal (delta + W=128 + fusion); [x] unit tests T1-T5 green (9 passed) + viewer fixture snapshot (static green; Playwright deferred, no browser on runner); [x] first S-tiny smoke rows in ledger (4 rows, check passes, G4 plots).
- **Milestone 2 (M2: S-tiny gates + erase proof, Refs #294):** [x] M2a trainer + toy scale + W=0 A2 switch + T6 (11 passed); [x] M2b toy matched-budget MQAR training (transformer vs P1 vs P5, 3 seeds, 1.584M tokens each) + G1 eval = A1; [x] M2c A2 window {0,16,32} toy sweep + G4 1k-32k flatness (toy timed + S-tiny analytic) + RoPE O(T)-per-step fix + ledger 15 rows check-green + plots; [x] G4 Pareto-tier amendment re-lint (proof/viewer/README, no re-run, 2026-09-07 binding); [ ] full S-tiny trained gates DEFERRED (CPU-bound, measured 2026-09-08: p1-tiny ~1s/step at batch2/seq33 so the binding 3000x16xN64+ gate is ~50+h/arm on CPU - needs GPU runner).
- **Milestone 3 (M3: decoupled + slots, Refs #294):** [x] P3 accumulator branch + factory pins (toy 274 / tiny 1532 / small 2468, +0.03% tiny) + `--no-accumulator` A3 flag; [x] P2 SSD + slots G {0,4,16,64} + `--slots` A4 flag + A4 G=0 control (shares P1 hid, -0.01% tiny); [x] M3 test suite (T1/T2/T3 auto-extended over p2/p3 + test_m3.py A3/A4/slot-contract/G4-flatness/loader-inheritance + T6 p2/p3 guards, 34 passed); [x] A2-re + M3 first falsification toy probes (6 arms seed0 1000 steps = 0.528M tokens, fixed --window loader, curves/m3-toy, ledger 18 rows check-green); [ ] A3/A4/A5 sweeps at S-tiny (needs GPU); [ ] H2/H3 verdicts ledgered (H3 unresolved at toy: p3-noacc 0.0612 vs p3 0.0600).
- **Milestone 4 (M4: MAG-lite + envelope audit, Closes #294 only on full pass):** [x] M4a P4 code (`models/p4_maglite.py` surprise-gated delta + window, factory pins toy 294/tiny 1702/small 2724, parity toy -0.43%/tiny +0.003%/small +0.002%, `test_p4.py` 4 tests, suite 48 passed, 100-step toy smoke finite + checkpoint + eval, proof/README/ideas updated); [x] M4b toy falsification (p4-toy seed0 1000 steps = 0.528M tokens matched to M3 refs, G1 envelope 100 eps: mqar8 0.035 / N16 0.0156 chance / 2hop 0.01 / induction-copy 0.0; BELOW p1-W16-1000 ref 0.0625 and p2 0.0825, H4 NEGATIVE at toy, A6 N16-collapse + A7 retrieval-vs-drift split documented, curves/m4b-toy/, ledger 19 rows check-green); [ ] P4 gated behind P1/P2 ledger + H4 verdict at scale; [ ] A6 vocab/distractor stress at scale; [ ] A7 retrieval-vs-drift split at scale; [ ] S-small Enwik8 + 8x audit + final scoreboard; [ ] `Closes #294` if G1+G2+G3+G4 pass else `Refs #294` with negative ledger.
- **Current step:** M4i verification complete on CPU-less runner (ledger 25 rows green, py_compile clean, scope clean, merge-base cdf3cdae NOT orphan after --unshallow, zero forward_chunk refs, Refs #294). Next: S-tiny full gates on a GPU runner.
- **Next steps:** (1) full S-tiny trained gates on a GPU runner via `continue` (train.py supports tiny presets for all five families; at S-tiny the token-per-symbol budget makes A6 realistic); (2) A3/A4/A5 at S-tiny; (3) viewer Playwright snapshot; (4) envelope audit.

## Builder log (the Builder, 2026-09-07, M2 toy falsification)

- M2a: `harness/train.py` (AdamW 0.9/0.95, wd 0.1, clip 1.0, cosine+warmup, MQAR/Markov data, checkpoint+curve+summary outputs); toy scale pinned in factory/baseline (`transformer-toy` 336768 vs `p1/p5-toy` 336332, -0.13%, T2 extended to toy/tiny/small); `SlidingWindowAttn` W=0 zero-branch + state_size guard (A2 control); T6 `tests/test_stability.py` (beta in [0.01,0.99], alpha in (0,1), beta*||k||^2 worst 0.99 < 2.0, collinear finite). 11 passed.
- M2b (matched budget, CPU fp32, vocab64/N8, 3000 steps x batch16 = 1.584M tokens/arm/seed, lr 3e-4): G1 toy envelope (200 eps) - MQAR N8 P5 0.300 / P1 0.287 / T 0.146 (chance 0.016); N16 extrapolation collapses (P1 0.039, P5 0.000, T 0.091); 2-hop P5 0.532 / P1 0.460 / T 0.118; induction/copy at chance (MQAR-only training, no transfer, as expected). A1 verdict: delta shows NO advantage over additive map at toy N8 (P5 +1.3pts); H1/H5 UNRESOLVED at toy envelope (N=256 untested) - honestly ledgered, Refs #294 kept.
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
- Probes (seed0, 1000 steps x batch16 = 0.528M tokens/arm, vocab64/N8, 100 eps, curves/m3-toy/): A2-re W0 0.0875 / W16-ref 0.0625 / W32 0.0512 (no window advantage at toy N8); p2 (G16) 0.0825/0.03 (above matched p1 ref); p3 0.0600/0.01. Ledger 18 rows check-green (novel keys appended; M2 A2 rows extended by --force note upsert, cells intact; W16-1000 ref in curves+notes only - key collides with M2b row).
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
