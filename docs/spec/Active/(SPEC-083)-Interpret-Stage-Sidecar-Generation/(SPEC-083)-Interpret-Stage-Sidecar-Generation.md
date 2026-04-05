---
title: Interpret Stage Sidecar Generation
artifact: SPEC-083
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
  - SPEC-082
  - SPIKE-013
depends-on-artifacts:
  - SPEC-082
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Interpret Stage Sidecar Generation

## Problem Statement

The interpretation pipeline (`interpret_meeting.py`) couples LLM invocation directly into the script, forcing sequential execution and Claude lock-in. Sidecar generation is needed to decouple prompt assembly from LLM execution.

## Desired Outcomes

**Pipeline operators** can generate interpretation prompts without calling LLMs (fast, deterministic).

**Agents** receive structured templates with full context, filling them at their own pace.

**Runtime flexibility** allows Claude, Codex, Crush, or human operators to fill sidecars.

## External Behavior

**Inputs:**
- Bundle directory path (contains manifest.yaml and source material)
- Persona list (from `docs/persona/Active/`)
- Stage identifier: `interpret`

**Outputs:**
- `.pending/PERSONA-NNN/interpret.j2` for each persona (template with context)
- `.pending/PERSONA-NNN/intake.lock` marker file (optional, for locking)

**Preconditions:**
- Bundle directory exists and has valid manifest
- Persona definitions exist in `docs/persona/Active/`

**Postconditions:**
- All persona sidecar templates created
- Templates include: persona definition, task instructions, output format, meeting context
- Reference context block (from SPEC-081) injected when keyword triggers match

**Constraints:**
- Generation must complete in <5 seconds for 15 personas
- Templates must stay under 100 KB each
- No LLM calls during generation

## Acceptance Criteria

**AC1: Template Generation**
Given a bundle directory and persona list
When `generate_interpret_sidecars(bundle, personas)` is called
Then `.pending/PERSONA-NNN/interpret.j2` files are created for each persona
And each template contains: persona definition, task, output format schema, meeting context

**AC2: Performance**
Given a bundle with 15 personas
When sidecars are generated
Then generation completes in <5 seconds
And no network calls are made (no LLM, no API)

**AC3: Reference Context Injection**
Given a bundle with meeting context containing keyword triggers (from SPEC-081)
When templates are generated
Then reference context block is injected into templates for matching personas

**AC4: Persona Extraction**
Given persona definitions in `docs/persona/Active/`
When templates are generated
Then persona body is extracted from markdown (stripped of frontmatter and lifecycle table)
And persona name is extracted from H1 heading
And reaction audience is populated from REACTION_AUDIENCES mapping

**AC5: Backward Compatibility**
Given existing `interpret_meeting.py --dry-run` output
When sidecars are generated for the same bundle
Then template content matches the prompt that `--dry-run` would generate

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|
| AC1: Template Generation | | |
| AC2: Performance | | |
| AC3: Reference Context Injection | | |
| AC4: Persona Extraction | | |
| AC5: Backward Compatibility | | |

## Scope & Constraints

**In scope:**
- Refactor `interpret_meeting.py` to separate prompt assembly from LLM call
- `generate_interpret_sidecars()` function
- Template formatting (Jinja2-style placeholders)
- Persona extraction and formatting
- Reference context block injection (integrates SPEC-081)

**Out of scope:**
- LLM invocation (handled by agents)
- Resolve phase (SPEC-084)
- Brief stage (SPEC-085)
- Fold stage (SPEC-086)

## Implementation Approach

**TDD Cycle 1: Prompt Assembly Extraction**
- Test: `test_build_prompt_produces_same_output_as_dry_run()`
- Test: `test_persona_body_excludes_frontmatter_and_lifecycle()`
- Implement: Extract `build_prompt()` from `interpret_meeting.py` to `pipeline/prompt_assembly.py`

**TDD Cycle 2: Sidecar Generation**
- Test: `test_generate_sidecars_creates_pending_directories()`
- Test: `test_sidecar_includes_all_sections()`
- Implement: `pipeline/pending.py::generate_interpret_sidecars()`

**TDD Cycle 3: Reference Context Integration**
- Test: `test_reference_context_injected_when_triggers_match()`
- Implement: Integrate `pipeline/reference_context.py` into prompt assembly

**TDD Cycle 4: Performance Validation**
- Test: `test_generation_under_five_seconds_for_fifteen_personas()`
- Implement: Optimize prompt assembly for speed (cache persona definitions)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-04-04 | | Initial creation |