---
title: Brief Stage Sidecar Generation and Resolution
artifact: SPEC-085
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
  - SPEC-083
  - SPEC-084
depends-on-artifacts:
  - SPEC-082
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Brief Stage Sidecar Generation and Resolution

## Problem Statement

The brief generation pipeline (`generate_briefs.py`) also couples LLM invocation directly into the script. Similar to the interpret stage, it needs sidecar generation and resolution to enable parallel execution and runtime flexibility.

## Desired Outcomes

**Brief sidecars** can be generated and resolved independently of the interpretation pipeline.

**Cumulative context** from interpretation outputs is available during brief generation.

**Parallel execution** enables multiple personas to be briefed simultaneously by different agents.

## External Behavior

**Inputs:**
- Meeting ID (references interpretation outputs in `data/interpretation/meetings/$meeting_id/`)
- Persona list (same as interpret stage)
- Cumulative context (from prior meetings for this persona)
- Stage identifier: `brief`

**Outputs:**
- `.pending/briefs/$meeting_id/PERSONA-NNN/brief.j2` (template)
- `.pending/briefs/$meeting_id/PERSONA-NNN/brief.md` (filled output)
- Final: `data/interpretation/briefs/$meeting_id/PERSONA-NNN.md`

**Preconditions:**
- Interpretation outputs exist for this meeting
- Persona definitions exist

**Postconditions:**
- Brief outputs applied to final location
- `.pending/` directories cleaned up

**Constraints:**
- Brief generation must include cumulative context (previous briefs for this persona)
- Resolution validates brief schema (evergreen context, upcoming events, persona-specific sections)

## Acceptance Criteria

**AC1: Brief Sidecar Generation**
Given a meeting ID and persona list
When `generate_brief_sidecars(meeting_id, personas)` is called
Then `.pending/briefs/$meeting_id/PERSONA-NNN/brief.j2` files are created
And templates include: cumulative context, meeting interpretations, output format

**AC2: Cumulative Context Injection**
Given a persona with prior briefs in `data/interpretation/cumulative/PERSONA-NNN/`
When brief sidecars are generated
Then cumulative context is assembled from prior briefs
And cumulative context is injected into template

**AC3: Brief Sidecar Resolution**
Given completed brief sidecars
When `resolve_brief_sidecars(meeting_id)` is called
Then briefs are applied to `data/interpretation/briefs/$meeting_id/`
And `data/interpretation/cumulative/PERSONA-NNN/$meeting_id.md` is updated

**AC4: Brief Schema Validation**
Given a brief sidecar missing required sections
When resolve is called
Then sidecar is reported as failed
And error message identifies missing sections

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|
| AC1: Brief Sidecar Generation | | |
| AC2: Cumulative Context Injection | | |
| AC3: Brief Sidecar Resolution | | |
| AC4: Brief Schema Validation | | |

## Scope & Constraints

**In scope:**
- Brief sidecar generation (similar pattern to interpret stage)
- Cumulative context assembly from `data/interpretation/cumulative/`
- Brief sidecar resolution with validation
- Update cumulative records after resolution

**Out of scope:**
- Interpret stage (SPEC-083, SPEC-084)
- Fold stage (SPEC-086)
- Question extraction (SPEC-087)

## Implementation Approach

**TDD Cycle 1: Brief Sidecar Generation**
- Test: `test_generate_brief_sidecars_includes_cumulative_context()`
- Implement: `pipeline/pending.py::generate_brief_sidecars()`

**TDD Cycle 2: Cumulative Context Assembly**
- Test: `test_assemble_cumulative_context_from_prior_meetings()`
- Implement: `pipeline/cumulative.py::assemble_cumulative_context()`

**TDD Cycle 3: Brief Resolution**
- Test: `test_resolve_brief_sidecars_applies_to_final_location()`
- Test: `test_resolve_updates_cumulative_records()`
- Implement: `pipeline/pending.py::resolve_brief_sidecars()`

**TDD Cycle 4: Schema Validation**
- Test: `test_brief_schema_validation_catches_missing_sections()`
- Implement: Validation in `resolve_brief_sidecars()`

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-04-04 | | Initial creation |