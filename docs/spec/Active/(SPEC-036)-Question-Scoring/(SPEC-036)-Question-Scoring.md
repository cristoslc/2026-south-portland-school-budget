---
title: "Question Scoring"
artifact: SPEC-036
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

# Question Scoring

## Problem Statement

QUESTION artifacts need a priority score that increases as a function of age and breadth, so the most important unanswered questions surface first. SPIKE-008 validated `age_days x persona_count` as the formula. This spec implements the scoring pipeline step that computes and writes scores to QUESTION frontmatter.

## Desired Outcomes

Every QUESTION artifact carries a current priority score in its frontmatter. The pipeline recomputes scores on each run. Consumers (PERSONA-000 brief, site question hub) can sort questions by score without running their own calculations.

## External Behavior

**Inputs:**
- All QUESTION artifacts in `docs/question/Active/`
- Current date (for age calculation)

**Outputs:**
- Updated `priority-score`, `scored-at`, and `persona-count` fields in each QUESTION artifact's frontmatter

**Constraints:**
- Formula: `priority_score = (current_date - first_raised).days * persona_count`
- Score must be recomputed on every pipeline run (not cached from prior runs)
- Only Active questions are scored (Resolved/Retired questions retain their last score but are not recomputed)

## Acceptance Criteria

1. **Given** QUESTION-001 has `first-raised: 2026-02-04` and 10 persona variants, **when** scoring runs on 2026-03-30, **then** `priority-score` is set to 540 (54 days x 10 personas).

2. **Given** a new persona variant is added to QUESTION-003 by the extraction pipeline, **when** scoring runs, **then** the `persona-count` increments and the score reflects the new count.

3. **Given** QUESTION-005 was created today with 1 persona variant, **when** scoring runs, **then** `priority-score` is 0 and `scored-at` is today's date.

4. **Given** a QUESTION has been transitioned to Resolved, **when** scoring runs, **then** it is skipped (retains its last score unchanged).

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

**In scope:** Score computation, frontmatter update, pipeline integration.

**Out of scope:** The scoring formula itself is decided (SPIKE-008 validated it). Alternative formulas are not in scope unless the operator revisits.

## Implementation Approach

1. Scan `docs/question/Active/` for all QUESTION artifacts.
2. Parse `first-raised` and count entries in the Persona Variants table.
3. Compute `age_days * persona_count`.
4. Write `priority-score`, `scored-at`, and `persona-count` to frontmatter.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Operator-requested |
