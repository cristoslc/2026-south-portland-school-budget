---
title: Question Extraction Sidecar Generation and Resolution
artifact: SPEC-087
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
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Question Extraction Sidecar Generation and Resolution

## Problem Statement

The question extraction pipeline (`extract_questions.py`) is NOT LLM-intensive—it uses pattern matching and heuristics. However, the pending state pattern can still provide value for visibility and error isolation. This spec applies the pattern for consistency across all pipeline stages.

## Desired Outcomes

**Question extraction sidecars** follow the same pending state convention as LLM-intensive stages.

**Visibility** into extraction progress without running scripts.

**Error isolation** allows partial extraction without blocking downstream stages.

## External Behavior

**Inputs:**
- Bundle directory (meeting or inter-meeting context)
- Stage identifier: `questions`

**Outputs:**
- `.pending/questions/bundle/questions.j2` (template with extraction hints)
- `.pending/questions/bundle/questions.yaml` (extracted question candidates)
- Final: `data/interpretation/questions/questions.yaml`

**Preconditions:**
- Bundle has source material (transcripts, documents, inter-meeting context)

**Postconditions:**
- Question candidates written to YAML
- `.pending/` directory cleaned up
- Resolve report persisted

**Constraints:**
- Extraction uses heuristics, not LLM (fast, deterministic)
- Sidecars serve visibility and error isolation, not parallelism need

## Acceptance Criteria

**AC1: Question Sidecar Generation**
Given a bundle directory
When `generate_question_sidecars(bundle)` is called
Then `.pending/questions/bundle/questions.j2` is created
And template contains extraction hints and pattern guidance

**AC2: Fill as Heuristic Pass**
Given a question sidecar template
When "fill" is called (heuristic extraction, not LLM)
Then extraction runs deterministically
And `.pending/questions/bundle/questions.yaml` is produced

**AC3: Question Sidecar Resolution**
Given completed question YAML
When `resolve_question_sidecars(bundle)` is called
Then questions are written to `data/interpretation/questions/questions.yaml`
And `.pending/` directory is cleaned up

**AC4: Error Isolation**
Given a bundle with extraction errors (malformed content)
When extraction runs
Then errors are logged
And resolve report lists failed items with error details

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|
| AC1: Question Sidecar Generation | | |
| AC2: Fill as Heuristic Pass | | |
| AC3: Question Sidecar Resolution | | |
| AC4: Error Isolation | | |

## Scope & Constraints

**In scope:**
- Question sidecar generation (deterministic, no LLM)
- Heuristic extraction "fill" pass
- Resolution with YAML validation
- Visibility and error isolation

**Out of scope:**
- LLM-based question extraction (future enhancement, not this spec)
- Interpret stage (SPEC-083, SPEC-084)
- Brief stage (SPEC-085)

## Implementation Approach

**Note:** This spec is lower priority than the LLM-intensive stages. The pending state pattern provides less value here (no LLM bottleneck to decouple). Implementation can be deferred or simplified.

**TDD Cycle 1: Question Sidecar Generation**
- Test: `test_generate_question_sidecars_creates_template()`
- Implement: `pipeline/pending.py::generate_question_sidecars()`

**TDD Cycle 2: Heuristic Fill**
- Test: `test_question_fill_runs_deterministically()`
- Implement: `pipeline/question_extraction.py::extract_with_heuristics()`

**TDD Cycle 3: Resolution**
- Test: `test_resolve_question_sidecars_writes_yaml()`
- Implement: `pipeline/pending.py::resolve_question_sidecars()`

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-04-04 | | Initial creation |