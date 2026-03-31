---
title: "Phase 2 Persona Briefs"
artifact: SPEC-046
track: implementable
status: Proposed
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
priority-weight: medium
type: ""
parent-epic: EPIC-025
linked-artifacts:
  - INITIATIVE-003
  - SPEC-043
depends-on-artifacts:
  - SPEC-042
  - SPEC-045
addresses:
  - JOURNEY-002.PP-03
  - JOURNEY-001.PP-03
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Phase 2 Persona Briefs

## Problem Statement

Phase 1 briefs (SPEC-043) expose what the district hasn't shown the public. Phase 2 briefs go further: here's what independent analysis actually shows. The cohort survival model and scenario brackets provide the projection data — this spec integrates those findings with the gap analysis context into per-persona briefs that include testable predictions.

## Desired Outcomes

Each persona receives a brief that synthesizes gap analysis (what's missing) with independent projections (what the data suggests). The briefs include testable predictions — explicit statements that can be checked against future enrollment data. This converts a one-time analysis into a longitudinal accountability tool: each fall, when new enrollment numbers arrive, anyone can compare them against the projections and assess which scenario was closest to reality.

## External Behavior

**Inputs:**
- Gap analysis from SPEC-042
- Scenario bracket data from SPEC-045 (JSON)
- Phase 1 briefs from SPEC-043 (for context continuity)
- Persona definitions (PERSONA-001 through PERSONA-004)
- Interpretation pipeline (INITIATIVE-003)

**Outputs:**
- Per-persona Phase 2 briefs (markdown)
- Each brief: gap context recap, independent projection findings in persona's frame, scenario range explanation, testable predictions with timeframes
- Testable predictions formatted as: "If [assumption], then [measurable outcome] by [date]"
- Known limitations section per brief
- Briefs suitable for site publication

**Constraints:**
- Must use interpretation pipeline for generation
- Every projection claim must trace to the scenario model output
- Testable predictions must be specific enough to verify against future enrollment data
- Known limitations disclosed transparently — what the model can't capture, what data gaps remain

## Acceptance Criteria

1. Given each persona, when their Phase 2 brief is generated, then it integrates both gap analysis context and projection findings
2. Given any projection claim in a brief, when traced to scenario data, then the specific scenario and parameter set is identifiable
3. Given the testable predictions, when formatted, then each follows the pattern "If [assumption], then [outcome] by [date]" with at least 2 predictions per persona
4. Given the known limitations section, when reviewed, then it acknowledges data gaps from SPEC-041 and model limitations from SPEC-044
5. Given the briefs, when compared to Phase 1, then there is clear narrative progression — Phase 2 builds on Phase 1, not restates it

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

- Four personas: Maria, Tom, Linda, Priya
- Generated through interpretation pipeline, not hand-authored
- Phase 2 builds on Phase 1 — assumes reader familiarity with gap analysis
- Not time-sensitive in the same way as Phase 1, but should follow within weeks
- No advocacy or recommendations — let the projections and their range speak

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-30 | — | Decomposed from EPIC-025 |
