---
title: "Resolution Stress-Test Gate"
artifact: SPEC-037
track: implementable
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
priority-weight: ""
type: feature
parent-epic: EPIC-021
linked-artifacts:
  - SPIKE-008
depends-on-artifacts:
  - SPEC-034
  - SPEC-035
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Resolution Stress-Test Gate

## Problem Statement

When new transcript evidence suggests that the administration has answered a question, the pipeline must verify that the answer actually satisfies every persona's version of that question. A generic response that addresses one persona's framing may leave others unanswered. SPIKE-008 demonstrated this with a synthetic transportation scenario: a cost figure resolved David's fiscal question but not Rachel's routing concern or the equity lens on multilingual families.

## Desired Outcomes

No question is marked resolved prematurely. Partial resolutions are tracked per-variant so the pipeline and briefings can report "3 of 6 perspectives answered" rather than a binary open/closed. The administration's pattern of giving partial answers becomes visible.

## External Behavior

**Inputs:**
- A QUESTION artifact with persona variants
- New transcript evidence that may contain a resolution

**Outputs:**
- Per-variant resolved/unresolved status updated in the QUESTION artifact's Persona Variants table
- Resolution Evidence section populated with transcript citations
- Stress Test Results section populated with per-persona pass/fail
- `resolution-status` frontmatter updated: `open` → `claimed` (some evidence found) → `resolved` (all variants pass)

**Constraints:**
- All persona variants must pass for the canonical question to reach `resolved`
- Partial resolution keeps the question `open` (or `claimed`) with individual variants marked
- LLM calls use `claude -p` (subscription auth)
- The stress-test prompt must present each persona's specific framing, not the canonical phrasing

## Acceptance Criteria

1. **Given** new evidence contains a transportation cost figure of $340K annually, **when** the stress-test runs against QUESTION-001's 10 persona variants, **then** PERSONA-002's variant (cost question) is marked resolved while PERSONA-008's variant (specific bus route) remains unresolved.

2. **Given** a QUESTION has 6 persona variants and evidence resolves 3 of them, **when** the stress-test completes, **then** `resolution-status` is `claimed`, 3 variants show `resolved: true`, and the Stress Test Results section shows pass/fail per persona.

3. **Given** evidence fully resolves all persona variants of a question, **when** the stress-test completes, **then** `resolution-status` transitions to `resolved` and the QUESTION artifact is eligible for lifecycle transition to Resolved phase.

4. **Given** no new evidence is relevant to a QUESTION, **when** the pipeline runs, **then** the stress-test is not triggered and the QUESTION's resolution state is unchanged.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

**In scope:** Stress-test logic, per-variant resolution tracking, resolution evidence citation, pipeline integration point for detecting potential resolutions in new transcripts.

**Out of scope:** The lifecycle transition from Active to Resolved (that's a swain-design phase transition triggered after the stress-test confirms full resolution). Question extraction (SPEC-035). Scoring (SPEC-036).

## Implementation Approach

1. After new transcripts are processed, scan QUESTION artifacts for topic overlap with the new evidence.
2. For each potential match, run the stress-test: prompt the LLM with each persona variant's specific framing and the evidence text.
3. Parse per-variant results (YES with specifics / NO with gaps).
4. Update the QUESTION artifact: Persona Variants table, Resolution Evidence section, Stress Test Results section, and `resolution-status` frontmatter.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Operator-requested |
