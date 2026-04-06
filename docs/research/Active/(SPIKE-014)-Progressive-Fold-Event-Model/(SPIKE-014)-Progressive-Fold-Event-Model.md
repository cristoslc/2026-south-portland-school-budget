---
title: "Progressive Fold Event Model"
artifact: SPIKE-014
track: container
status: Active
author: cristos
created: 2026-04-05
last-updated: 2026-04-05
question: "What event model and staling rules enable progressive, event-scoped folds that avoid redundant re-computation while correctly propagating evidence reclassification?"
gate: Pre-Implementation
parent-epic: EPIC-037
risks-addressed:
  - Full fold re-runs waste LLM calls on unchanged inputs
  - Inter-meeting evidence bypasses cumulative understanding entirely
  - Evidence reclassification (standalone to bundled) silently stales downstream folds
  - No mechanism to detect which fold points need re-computation
evidence-pool: ""
---

# Progressive Fold Event Model

## Summary

<!-- Populated at completion. -->

## Question

What event model and staling rules let folds skip work that hasn't changed, while still catching evidence that moved from standalone to bundled?

Sub-questions:
1. **Event taxonomy**: What event types trigger a fold? Is absorption a third type, or does it stale existing events?
2. **Ordering**: How do events sort within a persona's fold sequence? What breaks ties on the same date?
3. **Staling cascade**: When an event changes, how far forward does staleness spread? Every later fold? Just the next one?
4. **Fold history format**: What does the record look like? Input hashes plus commit refs? A manifest per persona? One file per fold point?
5. **Progressive algorithm**: How does the engine find the first stale fold and re-fold from there?
6. **Integration**: How does this fit with SPEC-086 sidecars, ADR-006 pending state, and `fold_meeting.py`?

## Go / No-Go Criteria

- **Go**: The model handles all three cases (meeting fold, intermeeting fold, absorption) without special-casing. Progressive re-fold skips at least 50% of LLM calls on re-runs.
- **Go**: Staling rules use input hashes only — no heuristics.
- **No-Go**: If event ordering needs cross-persona coordination (one persona's fold depends on another's), the model is too complex. Fall back to meeting-scoped caching only.

## Pivot Recommendation

If the full model is too complex, fall back to two tiers: (1) meeting-scoped folds with input hashing to skip unchanged folds, and (2) inter-meeting evidence injected into the next meeting's fold context instead of folded on its own. This loses the ability to show "Maria saw the slides before the meeting" but keeps progressive re-folding for the common case.

## Findings

### Working notes

**Two event types confirmed:** `meeting` and `intermeeting`. Absorption is not a third type — it stales folds through the interpretation layer (bundle changes cause re-interpretation, which changes input hashes).

**Key open question: branching.** The fold graph is a DAG, not a linear chain. Between two meetings, multiple pieces of intermeeting evidence arrive independently. They all branch from the last meeting's fold output and don't depend on each other. The next meeting is a merge point that reads all branch outputs.

```
M1 (meeting, Dec 1)
├── im-001 (evidence, Dec 5)   ← branches from M1
├── im-002 (evidence, Dec 7)   ← branches from M1, NOT from im-001
M2 (meeting, Dec 8)            ← merges M1 + im-001 + im-002
├── im-003 (evidence, Dec 15)  ← branches from M2
M3 (meeting, Dec 22)           ← merges M2 + im-003
```

This changes three things from the naive linear model:

1. **Fold inputs differ by position in the DAG.** An intermeeting fold reads: persona def + parent meeting output + the evidence. A meeting fold reads: persona def + all branch outputs since last meeting + the interpretation. These are different input shapes.

2. **Staling is narrower.** If `im-001` changes, `im-002` is unaffected (sibling branches share the same parent, not each other). Only the next meeting fold (the merge point) and everything after it cascades.

3. **Intermeeting folds are parallelizable.** All branches from the same meeting can run at once — they share the same parent output and don't read each other.

**Implications for manifest format:** Events need a `parent` field (or `parents` for merge points) instead of assuming the prior entry is the parent. The flat event list from the linear model doesn't capture the graph.

**Implications for progressive algorithm:** "Linear scan for first mismatch" doesn't work for a DAG. Need a topological walk that checks each node's input hash against its specific parents, not against a global sequence position.

**Still to resolve:**
- Manifest schema that encodes the DAG (parent refs per event)
- Input hash computation for merge points (meeting folds that read N branch outputs)
- Whether the summary reads all leaf outputs or all outputs
- How `--force` works on a DAG (re-fold one branch? one subtree? everything?)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-04-05 | — | Created from design discussion with operator |
