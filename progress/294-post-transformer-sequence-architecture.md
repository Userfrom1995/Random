# Progress - Post-Transformer Sequence Architecture (issue #294)

- **Issue:** #294
- **Branch:** opencode/issue294-20260907194528
- **Status:** research_complete. Handoff to Architect requested.
- **Research deliverable:** `docs/research/issue-294-post-transformer-sequence-architecture.md` (literature review + baseline spec + benchmark methodology + 5 ranked proposals + falsifiable hypotheses + ablation plan + O(1) proof sketch).

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

- Dr. Mob, the Researcher
