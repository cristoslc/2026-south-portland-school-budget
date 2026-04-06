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

## Question

What event model and staling rules enable progressive, event-scoped folds that avoid redundant re-computation while correctly propagating evidence reclassification?

Sub-questions:
1. **Event taxonomy**: What are the distinct fold-triggering event types? Meetings and inter-meeting evidence are clear. Is evidence absorption (standalone -> bundled) a third event type, or is it a mutation of an existing event that triggers re-folding?
2. **Ordering**: How are events ordered within a persona's fold sequence? Strict chronological by evidence date? What happens when two events share the same date?
3. **Staling cascade**: When an event changes (e.g., inter-meeting evidence gets absorbed into a bundle), how far forward does staleness propagate? Every subsequent fold? Only the next fold?
4. **Fold history format**: What does the per-persona x fold-point sidecar look like? Input hashes + commit refs? A manifest per persona? One file per fold point?
5. **Progressive algorithm**: Given a persona's event sequence with some stale points, what's the re-fold algorithm? Linear scan from first stale point? Can you skip non-dependent folds?
6. **Integration with existing infrastructure**: How does this compose with SPEC-086's sidecar generation, ADR-006's pending state, and the existing `fold_meeting.py` engine?

## Go / No-Go Criteria

- **Go**: The event model handles all three scenarios (meeting fold, inter-meeting fold, absorption reclassification) without special-casing, and progressive re-fold avoids at least 50% of LLM calls in the "re-run after evidence update" scenario
- **Go**: Staling rules are expressible as a deterministic function of input hashes — no heuristics needed
- **No-Go**: If the event ordering problem requires global coordination across personas (one persona's fold depending on another's), the model is too complex — fall back to meeting-scoped with per-meeting caching only

## Pivot Recommendation

If the full event-scoped model proves too complex, fall back to a simpler two-tier approach: (1) meeting-scoped folds with input hashing for skip detection, and (2) inter-meeting evidence injected into the next meeting's fold context rather than folded independently. This loses the "Maria knows about the slides before the meeting" capability but preserves progressive re-folding for the common case.

## Findings

### Event Taxonomy (to investigate)

Candidate event types:
- `meeting-interpretation` — a meeting was interpreted for this persona (current fold trigger)
- `intermeeting-evidence` — evidence arrived between meetings; persona should fold it in
- `absorption` — previously inter-meeting evidence is now part of a meeting bundle; the inter-meeting fold point's context changed

Open question: is absorption a *new* event or a *mutation* of the `intermeeting-evidence` event that triggers re-fold of everything from that point forward?

### Staling Rules (to investigate)

Candidate rules:
- New `meeting-interpretation` event → append to sequence, fold it (no staling of prior folds)
- New `intermeeting-evidence` event → insert in chronological position, fold it, stale everything after it
- `absorption` of an inter-meeting event → the absorbed event changes (or is removed?), stale everything from that point forward
- Persona definition change → stale everything (rare, treat as full re-fold)

### Fold History Format (to investigate)

Options:
1. **Sidecar per fold point**: `cumulative/PERSONA-NNN/YYYY-MM-DD.meta.yaml` with input hashes
2. **Manifest per persona**: `cumulative/PERSONA-NNN/fold-history.yaml` listing all fold points with hashes
3. **Git-native**: hashstamped commits only — detect staleness by comparing current input hashes against the commit that produced each fold output

Option 3 is appealing because git already tracks what changed and when, but it requires parsing git log for hash comparison. Options 1-2 are more explicit but add files.

### Progressive Algorithm (to investigate)

Candidate: linear scan from earliest event to latest. For each fold point, compute input hash (persona def + prior fold outputs + event evidence). Compare to recorded hash. First mismatch = re-fold from here forward. Everything before the mismatch is valid.

Question: can folds after the first stale point ever be *valid*? If fold N is stale, is fold N+1 always stale? (Probably yes, because each fold's input includes the output of all prior folds.)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-04-05 | — | Created from design discussion with operator |
