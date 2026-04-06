---
source-id: "sleepgate-paper"
title: "Learning to Forget: Sleep-Inspired Memory Consolidation for LLMs (SleepGate)"
type: web
url: "https://arxiv.org/html/2603.14517v1"
fetched: 2026-04-05T00:00:00Z
hash: "88e56769df5964319346b88c4384623d099f741ea1392812be0efdcc5701cce1"
---

# Learning to Forget: Sleep-Inspired Memory Consolidation for LLMs

## Core Problem

Large language models suffer from **proactive interference (PI)**: outdated information in the context window disrupts retrieval of current, relevant data. Accuracy degrades log-linearly as stale associations accumulate -- a fundamental working memory bottleneck that persists regardless of context length and resists prompt-engineering fixes.

## Proposed Solution: SleepGate

SleepGate augments transformer-based LLMs with a learned sleep cycle operating over the key-value cache, inspired by biological sleep-dependent memory consolidation. The framework comprises three coordinated mechanisms:

### Three Core Modules

1. **Conflict-Aware Temporal Tagger**: Detects when new entries supersede old ones using semantic signatures and marks superseded entries with binary flags.

2. **Forgetting Gate (G_theta)**: A lightweight neural network assigning retention scores to each cache entry. Uses soft attention biasing to downweight stale entries without hard deletion: "an entry with r_i=0.01 receives a bias of b_i of approximately -23, effectively zeroing its attention weight."

3. **Consolidation Module**: Merges related entries marked for compression into compact summary representations, analogous to hippocampal replay transferring episodic memories into semantic knowledge.

### Adaptive Sleep Scheduling

Sleep micro-cycles trigger based on two signals:

- **Attention Entropy**: When distributions become uniform (model uncertainty)
- **Conflict Density**: When fraction of superseded entries exceeds threshold

## Theoretical Results

**Theorem 1** demonstrates that SleepGate reduces the interference horizon from O(n) to O(log n) under the assumption that "the forgetting gate identifies superseded entries with probability p_c >= 1 - epsilon for epsilon < 1."

The retrieval probability becomes "1/(1+O(N)) -- a constant independent of the number of updates n, eliminating the log-linear degradation."

## Experimental Validation

**Setup**: 4-layer transformer (793K parameters) on synthetic PI-LLM benchmark with seven interference depths (n in {1,2,5,10,15,20,30}).

**Key Results**:

- SleepGate: 99.5% accuracy at depth 5; 97.0% at depth 10
- All five baselines: <18% across all depths
- 5.5x improvement over best baseline (StreamingLLM) at n=2
- 10x improvement at n=5

**Baseline Analysis**:

- H2O performs worst (0-7.5% accuracy) because cumulative attention scores are anti-correlated with freshness under PI
- StreamingLLM (best baseline) reaches only 17.5% at n=1
- Decay-only ablation (<=12.5%) confirms learned gating is essential

## Identified Limitations

**Depth Saturation** (n>=15): Accuracy drops from 97.0% (n=10) to 16.5% (n=30). Stale retrieval rate reaches 62% at n=30, indicating semantic signatures lack capacity to disambiguate many similar entries. The soft bias mechanism also saturates when multiple entries contribute residual attention mass.

## Training Approach

Four-stage curriculum:

1. Base model warm-start (22% budget)
2. Gate pre-training on ground truth labels (11%)
3. Joint end-to-end training with soft biasing (67%)
4. Optional threshold calibration

## Broader Significance

The work demonstrates that "cognitive science can inform the design of LLM architectures," offering an architectural solution where prompt engineering fails. SleepGate provides a direct mechanism for selective inhibition through soft attention biasing -- a capability absent in standard transformers where all KV entries participate equally in attention computation.
