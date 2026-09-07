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

- **Active Milestone:** M2 (in progress on PR #295; M1 complete)
- **Milestone 1 (M1: scaffold + first falsification, PR 1 target, Refs #294):** [x] `postformer/` scaffold with `requirements.txt` + README + proof appendix skeleton; [x] baseline Transformer S-tiny/S-small + param counter within 2 percent (tiny +0.024%, small +0.002%, committed `ledger/params/`); [x] harness five scripts with exact CLI contracts + seeding + ledger schema; [x] P5 map control + P1-minimal (delta + W=128 + fusion); [x] unit tests T1-T5 green (9 passed) + viewer fixture snapshot (static green; Playwright deferred, no browser on runner); [x] first S-tiny smoke rows in ledger (4 rows, check passes, G4 plots).
- **Milestone 2 (M2: S-tiny gates + erase proof, Refs #294):** [x] M2a trainer + toy scale + W=0 A2 switch + T6 (11 passed); [x] M2b toy matched-budget MQAR training (transformer vs P1 vs P5, 3 seeds, 1.584M tokens each) + G1 eval = A1; [x] M2c A2 window {0,16,32} toy sweep + G4 1k-32k flatness (toy timed + S-tiny analytic) + RoPE O(T)-per-step fix + ledger 15 rows check-green + plots; [ ] full S-tiny trained gates DEFERRED (CPU-bound, documented below).
- **Milestone 3 (M3: decoupled + slots, Refs #294):** [ ] P3 accumulator branch + A3; [ ] P2 SSD + slots G {0,4,16,64} + A4; [ ] A5 state scaling curve; [ ] H2/H3 verdicts ledgered.
- **Milestone 4 (M4: MAG-lite + envelope audit, Closes #294 only on full pass):** [ ] P4 gated behind P1/P2 ledger + H4 verdict; [ ] A6 vocab/distractor stress; [ ] A7 retrieval-vs-drift split; [ ] S-small Enwik8 + 8x audit + final scoreboard; [ ] `Closes #294` if G1+G2+G3+G4 pass else `Refs #294` with negative ledger.
- **Current step:** M2 toy falsification complete and ledgered (15 rows). Next: S-tiny training (needs GPU runner) then M3 P3/P2.
- **Next steps:** (1) full S-tiny trained gates on a GPU runner via `continue` (train.py supports tiny/small presets); (2) M3 P3/P2 implementation; (3) viewer Playwright snapshot; (4) envelope audit.

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
