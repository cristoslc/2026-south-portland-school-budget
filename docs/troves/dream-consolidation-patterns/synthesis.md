---
trove: dream-consolidation-patterns
synthesized: 2026-04-05
sources: 6
referenced-by:
  - SPIKE-014
  - EPIC-037
---

# Dream/Consolidation Patterns -- Thematic Synthesis

## 1. Anchored Iterative Summarization vs Full Re-summarization

The strongest consensus across sources is that **incremental summary extension beats full reconstruction**. The Zylos survey (`zylos-context-compression`) reports that Factory's anchored iterative approach scored 4.04 on accuracy versus 3.43-3.74 for full-reconstruction competitors across 36,000 real messages. The mechanism: when a compression trigger fires, only the newly-evicted span gets summarized, then merged into a persistent anchor containing intent, changes, decisions, and next steps.

Full re-summarization introduces two failure modes: accumulated detail drift across compression cycles, and high per-compression cost. Active Context Compression (`active-context-compression`) takes this further by making the agent itself decide what to compress, using importance evaluation rather than age-based eviction.

Context-Folding (`context-folding-sun-2025`) offers a structural variant: rather than summarizing a flat history, the agent branches into subtask trajectories and collapses them on completion. This achieves 10x context reduction while matching ReAct baselines -- the fold/unfold boundary naturally defines what gets summarized.

**Implication for SPIKE-014:** A fold event's consolidation step should extend the existing world-model summary rather than regenerate it. The fold boundary (event completion) is a natural compression trigger.

## 2. Sleep-Inspired Consolidation: Key Decay, Forgetting Gates, Consolidation Modules

SleepGate (`sleepgate-paper`) provides the most direct biological analogy. Its three modules map to distinct consolidation concerns:

- **Conflict-Aware Temporal Tagger** -- detects when new information supersedes old, marking stale entries. This is the "what changed" signal.
- **Forgetting Gate** -- assigns retention scores via soft attention biasing, downweighting stale entries without hard deletion. Reduces interference horizon from O(n) to O(log n).
- **Consolidation Module** -- merges related entries into compact summaries, analogous to hippocampal replay converting episodic to semantic memory.

The adaptive sleep scheduling triggers on attention entropy (model confusion) and conflict density (staleness ratio) rather than fixed intervals.

**Limitation:** SleepGate accuracy drops sharply at interference depth >= 15. For long event histories with many similar updates, semantic signatures alone cannot disambiguate. This is directly relevant to fold events that accumulate many structurally similar budget-line updates.

## 3. Focus Loop / Autonomous Compression Triggers

Multiple sources converge on trigger-based rather than scheduled compression:

- **Budget-based:** Zylos recommends triggering at 70% context utilization (`zylos-context-compression`).
- **Entropy-based:** SleepGate triggers when attention distributions become uniform (`sleepgate-paper`).
- **Failure-driven:** ACON optimizes compression guidelines by analyzing cases where compressed context caused task failure, then updating the compression prompt to preserve that information class (`zylos-context-compression`). This achieves 26-54% token reduction while keeping 95%+ accuracy.
- **Structural:** Context-Folding triggers on subtask boundaries -- the agent learns when to open and close folds via reinforcement learning (`context-folding-sun-2025`).

**Implication for SPIKE-014:** The fold event model should support multiple trigger types. Budget pressure is the baseline, but structural triggers (phase completion, decision points) and quality triggers (drift detection) add robustness.

## 4. Multi-Resolution Summary Layers

The enterprise memory stack (`enterprise-memory-stack-2026`) formalizes four layers with distinct retention periods and access patterns:

| Layer | Content | Retention | Analogy |
|---|---|---|---|
| Working | Active context, recent turns | Minutes/hours | Context window |
| Episodic | Task-grouped interactions with metadata | Months | Session logs |
| Semantic | Distilled facts, entities, relationships | Years | World model |
| Governance | Prompts, actions, outputs, audit trail | Policy-set | Decision log |

Access follows read-then-write: query semantic facts, retrieve relevant episodes, compose working context, execute, then append events and update summaries. This layered model maps naturally to fold event consolidation: each fold completion writes to episodic (what happened), updates semantic (what changed in the world model), and logs to governance (what was decided and why).

## 5. Context Window Optimization Techniques

The Zylos survey catalogs six approaches with production guidance:

| Technique | Compression Ratio | Best For |
|---|---|---|
| Sliding window | N/A (truncation) | Short, stateless sessions |
| Full re-summarization | 3:1 to 5:1 | Infrequent compression |
| Anchored iterative | 3:1 to 5:1 | Long sessions with continuity needs |
| ACON (failure-driven) | 26-54% reduction | Domain-specific optimization |
| Provider-native compaction | Automatic | API-integrated agents |
| Embedding-based | 80-90% reduction | Large archives with retrieval |

Tool outputs compress most aggressively (10:1 to 20:1). Recent messages (last 5-7 turns) and system prompts should never be compressed.

Context drift -- not exhaustion -- is the primary failure mode. 65% of enterprise agent failures in 2025 stemmed from degraded reasoning due to memory loss during multi-step work. Symptoms: redoing completed work, shifting goal language, forgetting instructions.

## 6. Gaps Relevant to Our Use Case

The collected sources reveal several gaps that matter for SPIKE-014's progressive fold event model:

**DAG-structured event history.** All sources assume linear conversation history. Our fold events form a DAG where multiple branches may share context and converge. None of the surveyed compression techniques address merging summaries from parallel branches or preserving shared-context references across folds.

**Temporal fidelity preservation.** SleepGate's forgetting gate and anchored summarization both optimize for "what's current" at the expense of temporal ordering. For budget analysis, the sequence of changes matters -- knowing that staffing was cut before transportation was expanded tells a different story than the reverse. No source addresses order-preserving compression.

**Shared world model across folds.** The enterprise memory stack's semantic layer is closest, but it assumes a single agent updating a single knowledge store. Our model needs multiple fold events to read from and write to a shared world model without conflicts. Concurrent update semantics are unaddressed.

**Governance-aware compression.** The enterprise stack identifies governance as a layer, but no source addresses how compression interacts with auditability. If a fold event compresses intermediate reasoning, can we still trace why a conclusion was reached? This matters for public-accountability analysis.

**Structural similarity disambiguation.** SleepGate's accuracy collapse at depth >= 15 is directly relevant. Budget line items are structurally similar (same schema, similar magnitudes). Compression techniques need domain-specific signals beyond semantic similarity to distinguish between them.
