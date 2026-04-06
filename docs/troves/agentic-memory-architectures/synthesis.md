# Agentic Memory Architectures: Thematic Synthesis

Trove: `agentic-memory-architectures`
Referenced by: SPIKE-014 (Progressive Fold Event Model), EPIC-037

---

## 1. Tiered Memory Architectures

Every system in this trove organizes memory into tiers. Two naming conventions dominate:

**Architecture-focused (Letta/MemGPT lineage):**
- Main context / message buffer (RAM-like, token-limited)
- Core memory (persistent structured blocks, always in context)
- Recall storage (searchable conversation history)
- Archival storage (vector-indexed long-term knowledge)

Sources: `memgpt-paper`, `letta-memory-management`, `monigatti-memory-in-agents`

**Cognitive-science-focused (LangGraph/LangMem lineage):**
- Working memory (current context window)
- Semantic memory (facts, preferences -- decontextualized)
- Episodic memory (timestamped experiences)
- Procedural memory (learned skills, instructions)

Sources: `langgraph-memory`, `langmem-sdk`, `agent-memory-survey-2026`

The survey (`agent-memory-survey-2026`) unifies both under a three-axis taxonomy: temporal scope, representational substrate, and control policy. The key unsolved problem across all systems is **transition policy** -- when does an episodic record graduate to semantic status, and when does a semantic fact get evicted?

**Relevance to SPIKE-014:** The fold model's tiering (hot context vs. accumulated state vs. archival evidence) maps onto this pattern. The question is whether fold events are episodic (timestamped, specific) or semantic (abstracted into the world model), and when the transition happens.

## 2. Structured State Objects and Entity Graphs

Two approaches to structuring long-term memory appear:

**Profile method** (`langgraph-memory`): A single JSON document continuously updated with scoped facts. Risk: models must regenerate or patch the entire profile, causing data loss or schema corruption on updates.

**Collection method** (`langgraph-memory`): Many narrowly-scoped documents extended over time. Reduces information loss but shifts burden to search and retrieval.

**Graph-based memory** (`mem0-paper`, `mem0-state-of-memory-2026`): Mem0g captures relational structures among entities. Graph queries enable multi-hop reasoning that vector similarity alone cannot resolve. Production results show a modest accuracy gain (68.4% vs. 66.9%) but qualitative improvement on relationship-heavy queries.

The survey identifies four representational substrates: context-resident text, vector-indexed stores, structured stores (SQL/knowledge graphs), and executable repositories. No system effectively combines all four.

**Relevance to SPIKE-014:** The fold world model is closest to the profile method -- a structured state object that evolves over time. The graph approach matters for tracking entity relationships (e.g., which budget line items connect to which programs). The profile corruption risk is directly relevant: fold events must apply cleanly without losing prior state.

## 3. Conflict Detection and Supersession

The literature identifies four memory management operations (`monigatti-memory-in-agents`):
- **ADD:** Store new information
- **UPDATE/MERGE:** Modify existing data
- **DELETE/INVALIDATE:** Remove obsolete information
- **NOOP/SKIP:** Decide no action needed

The survey (`agent-memory-survey-2026`) adds detail on staleness and contradiction handling:
- **Temporal versioning:** Track when facts were true
- **Source attribution:** Know where each fact came from
- **Contradiction detection:** Flag when new information conflicts with stored state
- **Periodic consolidation:** Merge and deduplicate during idle periods

Mem0's extract-consolidate-retrieve loop (`mem0-paper`) is the most production-tested conflict resolution pipeline. The survey warns of **self-reinforcing error** in reflective systems -- agents that incorrectly conclude something and never revisit the conclusion.

**Relevance to SPIKE-014:** The fold model's add/merge/invalidate/skip operations map directly onto these four operations. The temporal versioning and source attribution patterns are essential -- fold events need provenance (which evidence source, which session) and timestamp ordering to resolve conflicts correctly. The self-reinforcing error risk applies to persona interpretations that calcify across sessions.

## 4. Memory Compression and Retrieval Strategies

**Compression risks** (`agent-memory-survey-2026`):
- Summarization drift: each compression pass silently discards low-frequency details
- Attentional dilution: information in the middle of long contexts is recalled less reliably

**Retrieval strategies:**
- Two-stage retrieval (broad then precise)
- Retrieval-or-not gating (skip retrieval for straightforward requests)
- Token budgeting (allocate retrieval tokens based on query complexity)
- Multi-granularity indexing (select resolution adaptively)

Sources: `agent-memory-survey-2026`, `mem0-state-of-memory-2026`

**Write path engineering** (`agent-memory-survey-2026`): Well-designed write paths include filtering, canonicalization, deduplication, priority scoring, and metadata tagging. Async writes eliminate user-facing latency (`mem0-state-of-memory-2026`).

**Hot path vs. background** (`langgraph-memory`, `monigatti-memory-in-agents`): Synchronous memory writes give immediacy but add latency and complexity. Background writes decouple memory from the main loop but risk stale reads.

**Relevance to SPIKE-014:** Summarization drift is the core risk for progressive folds -- each fold pass could lose minority-viewpoint details or edge-case evidence. The fold model should preserve raw evidence alongside compressed state, matching the survey's recommendation that "context-resident memory should be supplemented with external stores preserving raw records."

## 5. Gaps in the Literature Relevant to Our Use Case

### Shared world model across personas
No system in this trove addresses multiple agents (or personas) maintaining a shared, evolving world model where each agent contributes partial observations from a different viewpoint. Multi-agent memory (`agent-memory-survey-2026`) is discussed only in terms of access control and leakage prevention, not collaborative world-building. The fold model's requirement -- multiple personas contributing to a single evolving state object -- has no direct prior art.

### DAG-structured event history
All systems use flat or two-tier temporal ordering (recent vs. old). None model event history as a directed acyclic graph where events can branch, merge, and have causal dependencies. The survey calls for "causally grounded retrieval" but notes it is "largely unexplored." The fold model's need for DAG-structured event chains (where a fold event depends on specific prior events, not just recency) sits in this gap.

### Conflict resolution with domain semantics
Existing conflict detection is generic (newer supersedes older, or flag for human review). The fold model needs domain-aware conflict resolution -- e.g., a budget figure from an official document supersedes a figure from a news article, regardless of timestamp. No system provides pluggable conflict resolution policies.

### Forgetting with accountability
The survey notes forgetting is underexplored. For the budget analysis use case, forgetting must be auditable -- if a fold event invalidates prior state, the invalidation itself is evidence that must be preserved. Current systems treat deletion as permanent removal, not as a tracked state transition.

### Evaluation of progressive memory
MemoryArena (`agent-memory-survey-2026`) is the closest benchmark, testing inter-session dependencies. But no benchmark evaluates progressive state accumulation where correctness depends on the full history of updates, not just the current snapshot.

---

*8 sources collected. Letta docs returned partial content (landing page redirect). All other sources fetched successfully.*
