---
source-id: "langgraph-memory"
title: "LangGraph Memory Overview"
type: web
url: "https://docs.langchain.com/oss/python/langgraph/memory"
fetched: 2026-04-05T00:00:00Z
hash: "5461ba65428623655114a44f1d46d85bc7a5e1f8b07ab9340d306dfada46b812"
---

# LangGraph Memory Overview

**Source:** LangChain documentation (docs.langchain.com)

## Core Concept

Memory in AI agents is "crucial because it lets them remember previous interactions, learn from feedback, and adapt to user preferences," particularly for agents handling complex, multi-turn tasks.

## Two Memory Categories

### Short-Term Memory (Thread-Scoped)
Maintains conversation context within a single session. The system persists state through database checkpoints, allowing threads to resume at any time. State updates occur when the graph executes or completes a step.

### Long-Term Memory (Cross-Session)
Stores user or application-level data across multiple conversational sessions. Memories exist within custom namespaces rather than single thread IDs, making them retrievable "at any time and in any thread." LangGraph provides **stores** as the mechanism for saving and retrieving these persistent memories.

## Managing Short-Term Memory

As conversations lengthen, full message histories may exceed LLM context windows. Models struggle with lengthy contexts, experiencing "distraction" from outdated content while incurring slower response times and higher costs. Recommended technique: manually remove or forget stale information.

## Long-Term Memory Types (Cognitive Taxonomy)

| Type | Content | Human Parallel | Agent Application |
|------|---------|----------------|-------------------|
| **Semantic** | Facts | School learning | Personalized user facts |
| **Episodic** | Experiences | Past events | Historical agent actions |
| **Procedural** | Instructions | Motor skills | System prompt + code |

### Semantic Memory: Two Approaches

**Profile method:** A continuously updated JSON document containing scoped, specific information. Challenges: model must regenerate entire profiles or apply patches, risking data loss or schema corruption.

**Collection method:** Multiple narrowly-scoped documents extended over time. Reduces information loss (easier for models to generate new objects than reconcile updates), but introduces complexity in deletion/updating and shifts burden to memory searching.

### Episodic Memory
Typically implemented as few-shot example prompting. Agents learn task completion patterns from prior action sequences. LLMs "learn well from examples."

### Procedural Memory
Agents rarely modify weights or rewrite code, but prompt modification is common. "Reflection" or meta-prompting: agents receive current instructions alongside recent conversations or feedback, then refine prompts accordingly.

## Memory Writing Strategies

### Hot Path (Synchronous)
- Memories created during runtime
- Immediate availability for subsequent interactions
- Increases agent complexity and latency
- Requires decision-making about what to memorize

### Background (Asynchronous)
- Separate background tasks eliminate primary application latency
- Isolates memory management from core logic
- Challenge: determining update frequency and triggers
- Common strategies: time-based scheduling, cron jobs, manual triggers

## Memory Storage Architecture

Long-term memories stored as JSON documents with hierarchical organization:
- Custom namespaces (analogous to folders) contain distinct keys (similar to filenames)
- Namespaces typically incorporate user or organization IDs
- Supports semantic search and content filtering across namespaces

```python
store.put(
    (user_id, application_context),
    "memory-key",
    {"data": "value"}
)
```

Database-backed stores recommended for production over in-memory implementations.

## Significance

LangGraph's memory model explicitly maps cognitive science categories (semantic, episodic, procedural) onto engineering constructs. The profile vs. collection distinction for semantic memory is directly relevant to the fold model's structured state objects -- profiles risk corruption on update while collections risk retrieval sprawl.
