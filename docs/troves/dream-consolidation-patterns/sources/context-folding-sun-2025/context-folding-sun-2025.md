---
source-id: "context-folding-sun-2025"
title: "Scaling Long-Horizon LLM Agent via Context-Folding"
type: web
url: "https://arxiv.org/abs/2510.11967"
fetched: 2026-04-05T00:00:00Z
hash: "91d09cc828e0c70393f5119856171dcf77198d68121ffbf0bcb82dd6cb57a689"
---

# Scaling Long-Horizon LLM Agent via Context-Folding

**Authors:** Weiwei Sun, Miao Lu, Zhan Ling, Kang Liu, Xuesong Yao, Yiming Yang, Jiecao Chen
**Submitted:** October 13, 2025
**Categories:** Computation and Language (cs.CL); Machine Learning (cs.LG)
**DOI:** 10.48550/arXiv.2510.11967

## Overview

This paper introduces Context-Folding, a framework enabling LLM agents to manage working context on extended tasks by decomposing complex problems into manageable subtasks.

## Key Innovation

The core mechanism allows agents to "branch into a sub-trajectory to handle a subtask and then fold it upon completion, collapsing the intermediate steps while retaining a concise summary." This is structurally analogous to function call/return semantics applied to agent reasoning traces.

## Technical Approach

- **Framework**: FoldGRPO -- an end-to-end reinforcement learning system with process rewards
- **Mechanism**: The agent learns when to open a fold (branch into subtask), how to execute within the fold, and when to close (collapse intermediate steps into summary)
- **Training**: Reinforcement learning encourages effective task decomposition and context management

## Performance Results

On complex benchmarks (Deep Research and SWE):

- Matches or outperforms ReAct baselines
- Uses active context approximately **10x smaller**
- Significantly exceeds summarization-based context management approaches

## Relevance to Consolidation Patterns

Context-Folding demonstrates that hierarchical decomposition with summary-on-close can achieve dramatic context reduction without sacrificing task performance. The fold/unfold metaphor maps naturally to consolidation: completed work streams collapse into summaries while active work retains full detail.
