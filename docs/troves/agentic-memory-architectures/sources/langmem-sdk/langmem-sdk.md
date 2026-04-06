---
source-id: "langmem-sdk"
title: "LangMem SDK for Agent Long-Term Memory"
type: web
url: "https://blog.langchain.com/langmem-sdk-launch/"
fetched: 2026-04-05T00:00:00Z
hash: "e90d9a24d556d44b3bc6d147b914ec0ae82e935dcbecc94b92670aa4629c32b0"
---

# LangMem SDK for Agent Long-Term Memory

**Source:** LangChain blog
**Published:** 2025

## Overview

LangMem SDK enables AI agents to "learn and improve through long-term memory." The toolkit provides capabilities for extracting conversational information, refining agent behavior via prompt modifications, and maintaining persistent memory. Works with any storage backend and agent framework, with native support for LangGraph's persistent memory layer.

Installation: `pip install -U langmem`

## Three Memory Categories

### Semantic Memory
Stores factual knowledge and relationships -- user preferences, domain-specific information. Unlike traditional RAG, semantic memory learns through interaction rather than offline data loading.

**Example:** "Alice manages the ML team and mentors Bob" gets captured. When roles change, the memory updates.

### Procedural Memory
Captures learned behaviors and patterns that evolve through feedback. Encodes learned procedures as updated system instructions rather than modifying model weights.

**Optimization algorithms:**
- `metaprompt`: Reflection-based optimization
- `gradient`: Separated critique/proposal steps
- `prompt_memory`: Unified approach

### Episodic Memory
Records specific past interactions and successful problem-solving approaches, typically distilled into few-shot examples. The documentation notes this category lacks opinionated utilities currently.

## Design Considerations

Before implementation, developers should evaluate:

- Which agent behaviors should adapt vs. remain constant
- What knowledge requires persistent tracking
- Which conditions should trigger memory recall
- Privacy requirements through namespace scoping (often user-specific to prevent data leakage)

## Key Distinction

LangMem distinguishes itself from conversation checkpointing by supporting recall across separate interactions -- "long-term" rather than working memory needs. This positions it as the cross-session complement to LangGraph's thread-scoped checkpointing.

## Significance

LangMem operationalizes the three-category memory model (semantic, procedural, episodic) with concrete algorithms for each. The procedural memory optimization algorithms (metaprompt, gradient, prompt_memory) are notable -- they enable agents to refine their own instructions based on feedback, a form of self-improvement that most memory systems do not address.
