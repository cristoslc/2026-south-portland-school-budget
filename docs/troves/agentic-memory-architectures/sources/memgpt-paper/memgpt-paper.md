---
source-id: "memgpt-paper"
title: "MemGPT: Towards LLMs as Operating Systems"
type: web
url: "https://arxiv.org/abs/2310.08560"
fetched: 2026-04-05T00:00:00Z
hash: "aff9a65b5e7810e95573e2f096fd11579671099e39542aed7d6a65d6b28fb378"
---

# MemGPT: Towards LLMs as Operating Systems

**Authors:** Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez (UC Berkeley)
**Published:** October 2023, revised February 2024

## Core Problem

Modern LLMs struggle with tasks requiring extended context, such as analyzing large documents or maintaining long-term conversations. Their limited context windows significantly restrict their practical utility.

## Key Innovation: Virtual Context Management

MemGPT proposes virtual context management, inspired by hierarchical memory systems in traditional operating systems. The technique creates an illusion of expanded memory by intelligently moving data between fast and slow memory tiers, analogous to how operating systems handle virtual memory through paging.

## System Architecture

MemGPT implements an OS-inspired design with:

- **Main context (RAM):** Active window with recent, relevant records
- **Recall storage (disk):** Searchable database of past messages
- **Archival storage (cold):** Vector-indexed long-term knowledge
- **Interrupt mechanisms:** Handle control flow between the system and users
- **Intelligent paging:** Data movement strategies borrowed from operating system principles

The system's key challenge is orchestration -- paging wrong content wastes tokens, while archiving too aggressively creates memory blindness.

## Evaluated Applications

The system was tested in two domains where context limitations are particularly problematic:

1. **Document Analysis:** MemGPT successfully processes documents exceeding the underlying model's context window
2. **Multi-Session Chat:** Creates conversational agents capable of remembering, reflecting, and evolving through extended user interactions

## Significance for Agent Memory

MemGPT established the tiered memory paradigm that subsequent systems (Letta, Mem0, LangMem) have built upon. Its OS analogy (main context as RAM, archival as disk) became the dominant mental model for agent memory architecture. The survey paper (agent-memory-survey-2026) identifies MemGPT's orchestration challenge -- deciding what to page in and out -- as the central unsolved problem in hierarchical memory management.
