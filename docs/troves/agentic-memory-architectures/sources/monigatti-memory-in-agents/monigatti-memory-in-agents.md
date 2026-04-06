---
source-id: "monigatti-memory-in-agents"
title: "Making Sense of Memory in AI Agents"
type: web
url: "https://www.leoniemonigatti.com/blog/memory-in-ai-agents.html"
fetched: 2026-04-05T00:00:00Z
hash: "b06826da24276d474c5c1c1d5aabb47a84f5e441684a6b6c4854bd80ad7e1a9e"
---

# Making Sense of Memory in AI Agents

**Author:** Leonie Monigatti
**Source:** leoniemonigatti.com

## Core Concept

LLMs lack built-in memory; they process each interaction as a fresh start. "Memory in AI agents is the ability to remember and recall important information across multiple user interactions." To enable recall, developers must provide agents access to historical conversation data.

## Memory Architecture: Two Categories

**In-Context Memory (Short-term):** Information within the LLM's context window, including current and retrieved past conversations.

**Out-of-Context Memory (Long-term):** Information stored externally in databases or vector stores.

## Two Taxonomies

### CoALA-inspired (Cognitive Science)
- Working memory
- Semantic memory (facts)
- Episodic memory (experiences)
- Procedural memory (instructions)

### Letta's Architecture-Focused Approach
- Message buffer
- Core memory
- Recall memory
- Archival memory

## Memory Management Operations

Four operations for managing external storage:

| Operation | Description |
|-----------|-------------|
| **ADD** | Store new information |
| **UPDATE** | Modify existing data |
| **DELETE** | Remove obsolete information |
| **NOOP** | Decide no database action needed |

## Information Transfer Strategies

### Explicit Memory (Hot Path)
Agents autonomously recognize important information and consciously store it via tool calls.

### Implicit Memory (Background)
Programmatic memory management at defined intervals -- after sessions, periodically during long conversations, or after each turn.

## Storage Implementation

- **Lists** for conversation history
- **Text/Markdown files** for instructions
- **Databases** for semantic information requiring specific retrieval methods

## Key Challenges

1. **Latency:** Continuous memory retrieval/offloading operations slow response times
2. **Forgetting:** Automating what to permanently delete remains difficult, with memory bloat and quality degradation as risks

## Available Frameworks

- **Dedicated memory:** mem0, Letta, Cognee, Zep
- **Orchestration frameworks with memory:** LangChain, LlamaIndex, CrewAI, Google ADK
- **Built-in provider memory:** Anthropic's Claude memory tools

## Significance

This article provides the clearest practitioner-oriented synthesis of the two competing taxonomies (cognitive-science vs. architecture-focused) and the four CRUD-like memory operations. The ADD/UPDATE/DELETE/NOOP framework maps directly to the fold model's conflict resolution operations (add/merge/invalidate/skip).
