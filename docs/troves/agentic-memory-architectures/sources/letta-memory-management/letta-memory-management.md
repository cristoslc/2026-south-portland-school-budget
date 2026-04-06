---
source-id: "letta-memory-management"
title: "Letta Memory Management Documentation"
type: web
url: "https://docs.letta.com/advanced/memory-management/"
fetched: 2026-04-05T00:00:00Z
hash: "4eb30c613682f39f31039755b22a204541bd12231e5e514b3e3b4973660f600d"
note: "Partial fetch -- docs URL redirects to landing page. Content reconstructed from landing page and cross-references in other trove sources."
---

# Letta Memory Management

**Source:** Letta platform documentation (docs.letta.com)

## Platform Overview

Letta (formerly MemGPT) is a platform for building stateful AI agents with memory and learning capabilities. It evolved from the MemGPT research paper into a production system.

## Products

- **Letta Code:** A "memory-first coding agent in your terminal" (npm install -g @letta-ai/letta-code, requires Node.js 18+)
- **Letta Code SDK:** Build apps on top of stateful computer use agents
- **Letta API:** Lower-level API for managing agent memory and context

## Memory Architecture (from cross-references)

Letta implements the MemGPT tiered architecture in production form:

- **Message buffer:** Recent conversation messages held in the active context window
- **Core memory blocks:** Persistent knowledge the agent maintains, viewable and editable through the State Visualization panel. Structured as named blocks (e.g., "human" and "persona" blocks for conversational agents)
- **Recall memory:** Searchable database of past conversation messages (analogous to MemGPT's recall storage)
- **Archival memory:** External out-of-context memory store, searchable via semantic queries (analogous to MemGPT's archival storage)

## State Management

The Agent Development Environment (ADE) provides:

- **State Visualization:** View and edit core memory blocks
- **Archival Memory Browser:** Monitor and search archival memory
- **Context Window Viewer:** Examine what information the agent currently processes
- **State Control:** Direct read/write access to persistent memory without recreating agents

## Significance

Letta operationalized the MemGPT research into a deployable system, demonstrating that the three-tier memory model (core/recall/archival) works in production. The architecture-focused naming (message buffer, core memory, recall, archival) became an alternative taxonomy to the cognitive-science-inspired naming (working, semantic, episodic, procedural) used by LangGraph and others.
