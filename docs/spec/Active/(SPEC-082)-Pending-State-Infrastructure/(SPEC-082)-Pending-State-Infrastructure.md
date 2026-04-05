---
title: Pending State Infrastructure
artifact: SPEC-082
track: implementable
status: In Progress
author: cristos
created: 2026-04-04
last-updated: 2026-04-04
priority-weight: high
type: enhancement
parent-epic: EPIC-035
parent-initiative: INITIATIVE-003
linked-artifacts:
  - ADR-006
  - SPIKE-012
  - SPIKE-013
depends-on-artifacts: []
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Pending State Infrastructure

## Problem Statement

The pipeline currently couples LLM invocation directly into Python scripts, creating a sequential bottleneck and runtime lock-in. Infrastructure is needed to support the pending state pattern: directory structure conventions, sidecar generation utilities, and a resolve scanner that applies completed work.

## Desired Outcomes

**Developers** have a reusable pattern for LLM-intensive work that can be adopted by any pipeline stage without custom state management.

**Operators** can inspect `.pending/` directories to see work queue status without running scripts.

**Agents** (any runtime) can fill sidecars in parallel without coordination overhead.

## External Behavior

**Inputs:**
- Bundle directory containing source material (meeting, trove, data)
- Persona list, configuration, or work item specification
- Stage identifier (interpret, brief, fold, extract, analyze)

**Outputs:**
- `.pending/` directory structure with sidecar templates
- Resolve report: applied count, pending count, failed count
- Final output files in target location

**Preconditions:**
- Bundle directory exists and has valid manifest
- Python 3.9+ environment
- No other resolve process running on same bundle (advisory lock)

**Postconditions:**
- All completed sidecars applied to final outputs
- `.pending/` directories cleaned up after successful application
- Resolve report persisted to `data/resolve-log/`

**Constraints:**
- Sidecar generation must complete in <5 seconds per bundle (no LLM calls)
- Resolve must complete in <10 seconds per bundle (no LLM calls)
- Must not modify source files (only create new outputs)

## Acceptance Criteria

**AC1: Sidecar Generation**
Given a bundle directory and persona list
When `generate_sidecars(bundle, stage="interpret", personas)` is called
Then `.pending/PERSONA-NNN/interpret.j2` files are created for each persona
And generation completes in <5 seconds for 15 personas

**AC2: Stage Detection**
Given a bundle directory
When `get_stage(bundle, persona_id)` is called
Then return one of: `pending-interpret`, `ready-to-resolve`, `done`, or `unknown`
And detection completes in <1 second

**AC3: Resolve Scanner**
Given a bundle directory with 12 completed and 3 pending sidecars
When `resolve_bundle(bundle)` is called
Then 12 outputs are applied to final location
And resolve report lists 12 applied, 3 pending, 0 failed
And `.pending/` directories for completed items are removed

**AC4: Streaming Resolve**
Given a bundle directory with partial completion
When `resolve_bundle(bundle, streaming=True)` is called
Then completed sidecars are applied immediately
And pending sidecars remain untouched in `.pending/`

**AC5: Error Isolation**
Given a bundle with one corrupted sidecar (invalid markdown)
When resolve runs
Then corrupted sidecar is reported as failed
And other sidecars are still applied
And resolve report lists applied count, pending count, and failed count

**AC6: Visibility**
Given a bundle directory with pending work
When operator runs `find bundle -name "*.j2" | wc -l`
Then output shows count of pending work items
And operator can inspect individual `.pending/PERSONA-NNN/` directories

## Verification

<!-- Populated when entering Testing phase. -->

| Criterion | Evidence | Result |
|-----------|----------|--------|
| AC1: Sidecar Generation | | |
| AC2: Stage Detection | | |
| AC3: Resolve Scanner | | |
| AC4: Streaming Resolve | | |
| AC5: Error Isolation | | |
| AC6: Visibility | | |

## Scope & Constraints

**In scope:**
- Directory structure convention (`entity/.pending/NNN/task.j2`, `entity/.pending/NNN/task.md`)
- `generate_sidecars()` function with stage-specific prompt templates
- `get_stage()` function for state detection
- `resolve_bundle()` function for applying completed work
- Resolve report persistence (`data/resolve-log/`)
- Advisory lock implementation (file-based, no external dependencies)

**Out of scope:**
- LLM invocation (handled by fill scripts or agents)
- UI or dashboard (filesystem is the interface)
- Database state tracking
- MCP server or API endpoints

**Token budget:** Sidecar templates should stay <100 KB each for interpret stage.

## Implementation Approach

**TDD Cycle 1: Sidecar Generation**
- Test: `test_generate_sidecars_creates_pending_directories()`
- Test: `test_sidecar_template_includes_context_and_prompt()`
- Implement: `pipeline/pending.py::generate_sidecars()`

**TDD Cycle 2: Stage Detection**
- Test: `test_get_stage_returns_pending_when_template_exists()`
- Test: `test_get_stage_returns_ready_when_output_exists()`
- Test: `test_get_stage_returns_done_when_no_pending()`
- Implement: `pipeline/pending.py::get_stage()`

**TDD Cycle 3: Resolve Scanner**
- Test: `test_resolve_applies_completed_outputs()`
- Test: `test_resolve_cleans_up_pending_directories()`
- Test: `test_resolve_reports_pending_count()`
- Test: `test_resolve_isolates_failures()`
- Implement: `pipeline/pending.py::resolve_bundle()`

**TDD Cycle 4: Streaming Resolve**
- Test: `test_streaming_resolve_applies_partial_completion()`
- Implement: `resolve_bundle(bundle, streaming=True)`

**TDD Cycle 5: Integration**
- Test: `test_full_cycle_generate_fill_resolve()`
- Test: `test_visibility_commands()`
- Implement: `scripts/resolve.py` CLI wrapper

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-04-04 | | Initial creation |