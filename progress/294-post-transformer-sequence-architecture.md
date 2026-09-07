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

- **Active Milestone:** M1
- **Milestone 1 (M1: scaffold + first falsification, PR 1 target, Refs #294):** [x] `postformer/` scaffold with `requirements.txt` + README + proof appendix skeleton; [x] baseline Transformer S-tiny/S-small + param counter within 2 percent (tiny +0.024%, small +0.002%, committed `ledger/params/`); [x] harness five scripts with exact CLI contracts + seeding + ledger schema; [x] P5 map control + P1-minimal (delta + W=128 + fusion); [x] unit tests T1-T5 green (9 passed) + viewer fixture snapshot; [ ] first S-tiny smoke rows in ledger.
- **Milestone 2 (M2: S-tiny gates + erase proof, Refs #294):** [ ] full G1/G2/G3/G4 at S-tiny for baseline vs P1 vs P5; [ ] A1 delta on/off; [ ] A2 window {0,128,256}; [ ] H1/H5 verdicts ledgered; [ ] G4 curve flat within 5 percent.
- **Milestone 3 (M3: decoupled + slots, Refs #294):** [ ] P3 accumulator branch + A3; [ ] P2 SSD + slots G {0,4,16,64} + A4; [ ] A5 state scaling curve; [ ] H2/H3 verdicts ledgered.
- **Milestone 4 (M4: MAG-lite + envelope audit, Closes #294 only on full pass):** [ ] P4 gated behind P1/P2 ledger + H4 verdict; [ ] A6 vocab/distractor stress; [ ] A7 retrieval-vs-drift split; [ ] S-small Enwik8 + 8x audit + final scoreboard; [ ] `Closes #294` if G1+G2+G3+G4 pass else `Refs #294` with negative ledger.
- **Current step:** M1 code complete (models + harness + T1-T5 green); S-tiny smoke rows next.
- **Next steps:** Builder to run S-tiny smoke (G1/G2/G4 small-T + G3 byte fixture + ledger append/check/plot), then yield `continue` for M2 full gates.

## Builder log (the Builder, 2026-09-07, M1)

- Installed torch CPU 2.14.0 + numpy/pytest on the runner; pinned in `postformer/requirements.txt`.
- Implemented `models/common.py` (RMSNorm, SwiGLU, RoPE, batched KVWindowBuffer, `param_count_no_embed` excluding input embedding only, sha256-derived `seed_all`).
- Implemented `models/baseline.py` (pre-norm causal Transformer, full `forward` + incremental `step` with RoPE baked at append), `models/p1_delta_hybrid.py` (gated delta memory + W=128 sliding window + fusion + SwiGLU; reference chunked forward), `models/p5_map.py` (degree-2 map + scaled additive write, identical proj shapes so T2 holds by construction), `models/factory.py`.
- Parity tuning: to hold the binding +-2% rule with the window branch pinned, P1/P5 MLP hid is 1704 (tiny) / 2726 (small), not the blueprint's 2016/3024 estimate. Measured: tiny +0.024%, small +0.002%.
- Fixed two real bugs found by parity probing: window `step()` applied RoPE on the flat head-concatenated dim (now per-head, matching `forward`), and harness model init was seeded from global torch state (now `reseed(seed, init-{model})` before every build).
- Harness: all five CLIs with blueprint contracts; G2 uses score-once strided eval; G3 byte-primary (BPE exits non-zero as deferred); G4 benches the recurrent `step()` path with prefill + warmup.
- T1-T5 green (9 passed): parity incl. collinear stress, param parity both scales, prefix-invariance causal probe, exact-summary determinism, ledger lint (NaN/drift/schema rejection).

- Dr. Mob, the Researcher
- the Architect
