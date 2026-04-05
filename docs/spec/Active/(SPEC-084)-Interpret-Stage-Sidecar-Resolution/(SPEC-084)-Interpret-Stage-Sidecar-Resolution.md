---
title: Interpret Stage Sidecar Resolution
artifact: SPEC-084
track: implementable
status: Proposed
author: cristos
created: 2026-04-04
last-updated: 2026-04-04
priority-weight: high
type: enhancement
parent-epic: EPIC-035
parent-initiative: INITIATIVE-003
linked-artifacts:
  - SPEC-083
depends-on-artifacts:
  - SPEC-082
  - SPEC-083
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Interpret Stage Sidecar Resolution

## Problem Statement

After agents fill sidecar templates, the pipeline needs to apply completed outputs to final locations and advance pipeline state. The resolve phase must be fast, deterministic, and isolated from failures.

## Desired Outcomes

**Completed interpretations** are applied to `data/interpretation/meetings/$meeting_id/` without manual intervention.

**Failed sidecars** are reported without blocking successful ones.

**Operators** can see at a glance which interpretations are complete, pending, or failed.

## External Behavior

**Inputs:**
- Bundle directory with `.pending/PERSONA-NNN/interpret.md` files (completed sidecars)
- Stage identifier: `interpret`

**Outputs:**
- Final output files: `data/interpretation/meetings/$meeting_id/PERSONA-NNN.md`
- Resolve report: `data/resolve-log/$meeting_id-$stage-$timestamp.json`
- Cleanup: `.pending/` directories removed for completed items

**Preconditions:**
- At least one `.pending/PERSONA-NNN/interpret.md` exists

**Postconditions:**
- All valid sidecars applied to final location
- Invalid sidecars reported in resolve log with error details
- `.pending/` directories cleaned up for completed items
- Resolve report persisted

**Constraints:**
- Resolution must complete in <10 seconds per bundle
- Must not overwrite existing final outputs without `--force` flag
- Must validate YAML frontmatter and required sections before applying

## Acceptance Criteria

**AC1: Apply Completed Sidecars**
Given a bundle with 3 completed sidecars (interpret.md files)
When `resolve_interpret_sidecars(bundle)` is called
Then 3 final output files are created in `data/interpretation/meetings/$meeting_id/`
And `.pending/` directories are removed for completed items

**AC2: Report Pending Sidecars**
Given a bundle with 2 completed and 3 pending sidecars (interpret.j2 but no interpret.md)
When resolve is called
Then 2 sidecars are applied
And resolve report lists 2 applied, 3 pending, 0 failed

**AC3: Isolate Failures**
Given a bundle with 1 valid sidecar and 1 invalid sidecar (missing required sections)
When resolve is called
Then valid sidecar is applied
And invalid sidecar is reported as failed
And `.pending/` directory is NOT removed for failed item

**AC4: Prevent Overwrite**
Given a bundle with completed sidecar
And final output file already exists at `data/interpretation/meetings/$meeting_id/PERSONA-001.md`
When resolve is called (without --force)
Then sidecar is skipped
And resolve report notes "skipped (output exists, use --force)"

**AC5: Resolve Report Persistence**
Given a completed resolve
When resolve finishes
Then report is persisted to `data/resolve-log/$meeting_id-interpret-$timestamp.json`
And report contains: applied count, pending count, failed count, list of failed items with errors

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|
| AC1: Apply Completed Sidecars | | |
| AC2: Report Pending Sidecars | | |
| AC3: Isolate Failures | | |
| AC4: Prevent Overwrite | | |
| AC5: Resolve Report Persistence | | |

## Scope & Constraints

**In scope:**
- `resolve_interpret_sidecars()` function
- Validation: YAML frontmatter, required sections (Structured Points, Journey Map, Reactions)
- Final output application with cleanup
- Resolve reporting and persistence
- `--force` flag for overwriting existing outputs

**Out of scope:**
- Sidecar generation (SPEC-083)
- LLM invocation (handled by agents)
- Brief stage (SPEC-085)
- Batch gate enforcement (optional future enhancement)

## Implementation Approach

**TDD Cycle 1: Apply Completed Sidecars**
- Test: `test_resolve_applies_completed_sidecars_to_final_location()`
- Test: `test_resolve_cleans_up_pending_directories()`
- Implement: `pipeline/pending.py::resolve_interpret_sidecars()`

**TDD Cycle 2: Report Pending**
- Test: `test_resolve_reports_pending_count()`
- Implement: `resolve_interpret_sidecars()` pending reporting

**TDD Cycle 3: Isolate Failures**
- Test: `test_resolve_isolates_invalid_sidecars()`
- Test: `test_resolve_keeps_pending_for_failed_items()`
- Implement: Validation logic in `resolve_interpret_sidecars()`

**TDD Cycle 4: Overwrite Protection**
- Test: `test_resolve_skips_existing_outputs_without_force()`
- Test: `test_resolve_overwrites_with_force_flag()`
- Implement: `--force` flag handling

**TDD Cycle 5: Resolve Report**
- Test: `test_resolve_persists_report_to_log_directory()`
- Implement: JSON report generation and persistence

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-04-04 | | Initial creation |