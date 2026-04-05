---
title: Cumulative Fold Sidecar Generation and Resolution
artifact: SPEC-086
track: implementable
status: Proposed
author: cristos
created: 2026-04-04
last-updated: 2026-04-04
priority-weight: medium
type: enhancement
parent-epic: EPIC-035
parent-initiative: INITIATIVE-003
linked-artifacts:
  - SPEC-082
depends-on-artifacts:
  - SPEC-082
  - SPEC-085
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Cumulative Fold Sidecar Generation and Resolution

## Problem Statement

The cumulative fold pipeline (`fold_meeting.py`) synthesizes persona-specific narratives across multiple meetings. It currently runs sequentially and blocks on LLM calls. Applying the pending state pattern enables parallel synthesis and incremental updates.

## Desired Outcomes

**Fold sidecars** can be generated for multiple personas simultaneously.

**Incremental updates** resume from failures without re-folding completed personas.

**Cumulative records** are updated atomically after successful resolution.

## External Behavior

**Inputs:**
- Meeting ID (new meeting being added to cumulative narrative)
- Persona list
- Prior cumulative records (`data/interpretation/cumulative/PERSONA-NNN/`)
- Stage identifier: `fold`

**Outputs:**
- `.pending/fold/$meeting_id/PERSONA-NNN/fold.j2` (template)
- `.pending/fold/$meeting_id/PERSONA-NNN/fold.md` (synthesis)
- Final: `data/interpretation/cumulative/PERSONA-NNN/$meeting_id.md` (incremental)
- Final: `data/interpretation/cumulative/PERSONA-NNN/summary.md` (full narrative)

**Preconditions:**
- Brief outputs exist for this meeting (from SPEC-085)
- Prior cumulative records exist

**Postconditions:**
- Incremental fold appended to cumulative record
- Summary synthesis regenerated (or marked for deferred synthesis)
- `.pending/` directories cleaned up

**Constraints:**
- Fold synthesis must reference all prior cumulative content
- Summary synthesis may be deferred (batch synthesis at end of run)

## Acceptance Criteria

**AC1: Fold Sidecar Generation**
Given a new meeting ID and persona with prior cumulative records
When `generate_fold_sidecars(meeting_id, personas)` is called
Then `.pending/fold/$meeting_id/PERSONA-NNN/fold.j2` files are created
And templates include: prior cumulative content, new brief content, synthesis prompt

**AC2: Incremental Fold Resolution**
Given completed fold sidecars
When `resolve_fold_sidecars(meeting_id)` is called
Then incremental synthesis is appended to `cumulative/PERSONA-NNN/$meeting_id.md`
And summary synthesis is queued (or deferred)

**AC3: Summary Synthesis**
Given all incremental folds for a persona are complete
When summary synthesis is triggered
Then `cumulative/PERSONA-NNN/summary.md` is regenerated with full narrative

**AC4: Parallel Execution**
Given fold sidecars for 15 personas
When multiple agents fill sidecars simultaneously
Then resolution applies all completed sidecars correctly
And no race conditions or conflicts in cumulative records

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|
| AC1: Fold Sidecar Generation | | |
| AC2: Incremental Fold Resolution | | |
| AC3: Summary Synthesis | | |
| AC4: Parallel Execution | | |

## Scope & Constraints

**In scope:**
- Fold sidecar generation with cumulative context assembly
- Incremental fold resolution
- Summary synthesis (immediate or deferred)
- File locking or advisory locks for parallel execution

**Out of scope:**
- Brief stage (SPEC-085)
- Interpret stage (SPEC-083, SPEC-084)
- Batch gate enforcement across personas

## Implementation Approach

**TDD Cycle 1: Fold Sidecar Generation**
- Test: `test_generate_fold_sidecars_assembles_cumulative_context()`
- Implement: `pipeline/pending.py::generate_fold_sidecars()`

**TDD Cycle 2: Cumulative Context Assembly**
- Test: `test_assemble_cumulative_context_from_prior_records()`
- Implement: `pipeline/cumulative.py::assemble_fold_context()`

**TDD Cycle 3: Incremental Fold Resolution**
- Test: `test_resolve_fold_appends_to_cumulative_record()`
- Implement: `pipeline/pending.py::resolve_fold_sidecars()`

**TDD Cycle 4: Summary Synthesis**
- Test: `test_summary_synthesis_regenerates_full_narrative()`
- Implement: `pipeline/cumulative.py::synthesize_summary()`

**TDD Cycle 5: Parallel Execution Safety**
- Test: `test_parallel_fill_does_not_conflict()`
- Implement: Advisory file locks (`fcntl.flock` or `.lock` files)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-04-04 | | Initial creation |