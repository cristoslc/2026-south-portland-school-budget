---
title: "Question Extraction Pipeline"
artifact: SPEC-035
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
  - ADR-004
depends-on-artifacts:
  - SPEC-034
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Question Extraction Pipeline

## Problem Statement

Per-persona briefings contain questions that residents and stakeholders are asking about the budget. These questions recur across personas and meetings but are currently isolated within individual briefs. The pipeline needs to extract these questions, cluster variants into canonical questions, and create or update QUESTION-NNN artifacts.

## Desired Outcomes

After each pipeline run, the set of QUESTION artifacts reflects the current state of unresolved questions across all persona briefings. New questions are detected and created. Existing questions gain new persona variants when additional personas raise the same concern. The extraction is automatic — no manual curation step.

## External Behavior

**Inputs:**
- All persona briefings in `data/interpretation/briefs/`
- Existing QUESTION artifacts in `docs/question/`

**Outputs:**
- New QUESTION-NNN artifacts for newly detected canonical questions
- Updated persona variant tables in existing QUESTION artifacts when new variants are found

**Preconditions:**
- SPEC-034 complete (QUESTION artifact type exists with template and definition)
- At least one set of persona briefings exists

**Constraints:**
- Clustering must produce zero false merges (distinct questions collapsed into one)
- Clustering must detect when a new persona variant belongs to an existing canonical question
- LLM calls use `claude -p` (subscription auth, per AGENTS.md LLM usage policy)

## Acceptance Criteria

1. **Given** a new set of persona briefings is generated, **when** the extraction pipeline runs, **then** it identifies questions that are not yet tracked in any QUESTION artifact and creates new QUESTION-NNN files for each.

2. **Given** PERSONA-008 raises a question about transportation in the 03-30 briefing that maps to an existing QUESTION-001, **when** the extraction pipeline runs, **then** it adds PERSONA-008's variant to QUESTION-001's persona variants table without duplicating the canonical question.

3. **Given** the extraction runs on the full corpus (03-19, 03-23, 03-30 briefings), **when** compared to the SPIKE-008 manual extraction, **then** it produces the same 5 canonical question clusters with the same persona groupings (allowing minor framing differences).

4. **Given** clustering must avoid false merges, **when** two questions are thematically related but operationally distinct (e.g., "transportation cost" vs. "September timeline"), **then** they remain separate canonical questions.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

**In scope:** Extraction logic, clustering logic, QUESTION artifact creation/update, integration with the existing interpretation pipeline.

**Out of scope:** Scoring (SPEC-036), resolution detection (SPEC-037), evergreen brief integration (SPEC-038).

## Implementation Approach

1. Add an extraction step to the interpretation pipeline that runs after persona briefs are generated.
2. For each brief, use the LLM to extract questions/concerns as structured output (persona, framing, date).
3. Compare extracted questions against existing QUESTION artifacts using semantic similarity (LLM-assisted clustering).
4. For new clusters: create QUESTION-NNN artifact from template.
5. For existing matches: append the new persona variant to the artifact's Persona Variants table.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Operator-requested |
