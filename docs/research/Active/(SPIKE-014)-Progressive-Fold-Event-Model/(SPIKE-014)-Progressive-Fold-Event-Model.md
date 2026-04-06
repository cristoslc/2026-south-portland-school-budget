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

**Go.** Use two event types (meeting and intermeeting) with a per-persona fold manifest. The manifest records input hashes at each fold point. Absorption is not a third event type. It stales folds through the interpretation layer: bundle changes cause the interpretation to re-run, which changes fold input hashes. To re-fold, scan the manifest for the first hash mismatch and re-fold from there forward. Every fold after a stale point is also stale, because each fold reads all prior fold outputs. Next step: create specs under EPIC-037 for the fold manifest schema, the progressive fold algorithm, and the intermeeting fold prompt.

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

### 1. Event Taxonomy

**Two event types, not three.** Absorption is not its own event. It changes an existing event's context, which triggers a re-fold.

| Event type | Trigger | Evidence source | Current support |
|-----------|---------|----------------|-----------------|
| `meeting` | Per-meeting interpretation lands | Bundle manifest + SPEC-018 interpretation | Yes (`fold_meeting.py`) |
| `intermeeting` | Inter-meeting evidence posted | Inter-meeting manifest entry + normalized source | No (bypasses fold, only feeds briefs) |

**Absorption is not an event.** When evidence gets absorbed into a bundle, the intermeeting event stays. It still shows what the persona knew at that moment. What changes is the *next meeting's fold input*. The meeting interpretation now includes that evidence as meeting context. The meeting fold re-triggers because its interpretation changed (the bundle grew).

Example from the data:
- `im-001` (budget slides) posted 2026-03-20, between March 19 and March 23 meetings
- The slides are also source `sb-document-2026-03-23-036` in the March 23 bundle
- An intermeeting fold would say: "Maria sees the budget slides before the workshop"
- The March 23 meeting fold would say: "The workshop discussed these slides — here's what was said"
- Both folds are valid. They show different moments in Maria's timeline.

**How absorption stales things:** The meeting interpretation changes because the bundle grew. This stales the meeting fold point. Each fold depends on all prior outputs, so everything after that meeting cascades too. The intermeeting fold stays valid — it came before the meeting.

### 2. Ordering

**Sort by date. Break ties by event type.**

Each persona's fold sequence is an ordered list:
```
[event_date, event_type, event_id]
```

Ordering rules:
1. Primary sort: `event_date` ascending
2. Tie-break: `intermeeting` before `meeting` (evidence posted on a meeting day was known before the meeting started)
3. Within same type and date: `event_id` ascending (stable sort)

For meetings, `event_date` = `meeting_date` from the bundle manifest.
For intermeeting evidence, `event_date` = `date_posted` from the inter-meeting manifest.

**No cross-persona links.** Each persona's fold sequence is its own. The No-Go condition does not apply.

### 3. Staling Cascade

**Forward-total cascade from the first stale point.** Each fold reads all prior fold outputs (`build_fold_prompt()`, line 343). If fold N is stale, fold N+1 is always stale too — its input hash includes N's output.

Staling triggers:

| Trigger | What stales | Cascade |
|---------|------------|---------|
| New meeting interpretation | That meeting's fold point + all after | Forward-total |
| New intermeeting evidence | New fold point inserted + all after its date | Forward-total |
| Meeting interpretation re-generated (e.g., bundle grew) | That meeting's fold point + all after | Forward-total |
| Persona definition changed | All fold points for that persona | Full re-fold |
| Prior fold output changed (cascade) | Next fold + all after | Forward-total |

**Key insight: absorption stales through the interpretation layer, not the fold itself.** When evidence joins a bundle, the meeting interpretation re-runs with new input. That changes the fold's input hash, which starts the cascade. The fold engine does not need to know about absorption — it just sees that the interpretation changed.

### 4. Fold History Format

**Use a manifest per persona** (Option 2).

Why not the others:
- **Sidecar per fold point** (Option 1): Creates 24+ `.meta.yaml` files per persona (360+ total). Clutters the directory. Hard to scan for "first stale point" without reading all files.
- **Git-native** (Option 3): Needs `git log` parsing for hash lookup. Fragile — commits can be amended or squashed. Not usable without git.

**Recommended format: `fold-manifest.yaml` per persona**

```
data/interpretation/cumulative/PERSONA-001/
├── fold-manifest.yaml    # fold history + input hashes
├── 2025-12-01.md         # cumulative record (unchanged)
├── 2025-12-08.md
├── ...
└── summary.md
```

```yaml
schema_version: "1.0"
persona_id: PERSONA-001
persona_hash: "sha256:a1b2c3..."   # hash of persona definition file

events:
  - event_id: "2025-12-01-city-council"
    event_type: meeting
    event_date: "2025-12-01"
    input_hash: "sha256:d4e5f6..."   # hash of (persona_def + prior_outputs + interpretation)
    output_hash: "sha256:g7h8i9..."  # hash of the cumulative record produced
    fold_date: "2026-03-17"
    commit: "a31869a"

  - event_id: "im-001"
    event_type: intermeeting
    event_date: "2026-03-20"
    input_hash: "sha256:j0k1l2..."
    output_hash: "sha256:m3n4o5..."
    fold_date: "2026-04-05"
    commit: "e26b9aa"

  - event_id: "2026-03-23-school-board"
    event_type: meeting
    event_date: "2026-03-23"
    input_hash: "sha256:p6q7r8..."
    output_hash: "sha256:s9t0u1..."
    fold_date: "2026-04-05"
    commit: "e26b9aa"

summary_hash: "sha256:v2w3x4..."     # hash of all output_hashes concatenated
summary_date: "2026-04-05"
```

**Why this works:**
- One file read gives the full fold sequence for a persona
- Linear scan finds the first stale point: compute input hash per event, compare to stored hash, stop at first mismatch
- `persona_hash` at the top catches persona definition changes (stales everything)
- `summary_hash` tells you when the summary needs a rebuild
- `commit` keeps git provenance without needing git for staleness checks
- Reuses `sha256_bytes()` from `pipeline/pool_utils.py`

### 5. Progressive Algorithm

```
for each persona P:
    load fold-manifest.yaml
    
    # Check persona definition staleness
    current_persona_hash = sha256_file(persona_definition_path)
    if current_persona_hash != manifest.persona_hash:
        stale_from = 0  # full re-fold
    else:
        # Build current event sequence from meeting + intermeeting sources
        current_events = sorted(
            meeting_events + intermeeting_events,
            key=(event_date, type_priority, event_id)
        )
        
        # Compare against manifest event sequence
        stale_from = None
        for i, (current, recorded) in enumerate(zip_longest(current_events, manifest.events)):
            if current != recorded:  # event added, removed, or changed
                stale_from = i
                break
            current_input_hash = compute_input_hash(P, current, prior_outputs[:i])
            if current_input_hash != recorded.input_hash:
                stale_from = i
                break
        
        if stale_from is None:
            skip P entirely  # nothing changed
    
    # Re-fold from stale_from forward
    for event in current_events[stale_from:]:
        fold(P, event)  # produces cumulative record, updates manifest entry
    
    regenerate_summary(P)
```

**LLM call savings:** In the common case (new meeting, no changes to prior ones), only 1 fold per persona instead of N. When a mid-sequence interpretation changes, folds before the change are skipped. Typical re-runs save 90%+ of calls, well above the 50% Go threshold.

### 6. Integration with Existing Infrastructure

**`fold_meeting.py` changes:**
- Swap `record_exists()` for manifest-based staleness check
- Add `intermeeting` event type to `build_fold_prompt()` (new prompt for non-meeting evidence)
- Read/write `fold-manifest.yaml` around the fold loop
- `--force` skips the hash check (same intent, new path)

**`pipeline/pending.py` (SPEC-086):**
- Extend sidecar generation to intermeeting events: `.pending/fold/{event_id}/PERSONA-NNN/fold.j2`
- `get_stage()` works as-is — it does not care about event type
- Resolution writes the record and updates the fold manifest

**`pipeline/pool_utils.py`:**
- Reuse `sha256_file()` for persona hashing
- Reuse `sha256_bytes()` for input hash (concat persona_hash + prior outputs + evidence)

**`pipeline/inter_meeting_schema.py`:**
- No changes. It already has `entry_id`, `date_posted`, and source paths.

**New code:**
- `pipeline/fold_manifest.py` — read/write/validate fold-manifest.yaml (same pattern as `bundle_schema.py`)
- `compute_input_hash()` — hash of fold inputs
- Intermeeting fold prompt in `fold_meeting.py`

### Go / No-Go Assessment

| Criterion | Result |
|-----------|--------|
| Handles all three scenarios without special-casing | **Go** — two event types + deterministic staling; absorption handled through interpretation re-generation |
| Progressive re-fold avoids 50%+ LLM calls | **Go** — common case (append new meeting) saves ~95% of calls |
| Staling rules are deterministic function of input hashes | **Go** — `sha256_bytes(persona_hash + prior_outputs + evidence)` is fully deterministic |
| No cross-persona coordination needed | **Go** — each persona's fold sequence is independent |

**Verdict: Go.** Proceed to implementation specs under EPIC-037.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-04-05 | — | Created from design discussion with operator |
