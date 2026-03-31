---
title: "Phase 1 Persona Briefs"
artifact: SPEC-043
track: implementable
status: Proposed
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
priority-weight: high
type: ""
parent-epic: EPIC-023
linked-artifacts:
  - INITIATIVE-003
depends-on-artifacts:
  - SPEC-042
addresses:
  - JOURNEY-002.PP-03
  - JOURNEY-001.PP-03
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Phase 1 Persona Briefs

## Problem Statement

The gap analysis (SPEC-042) produces a structured assessment of the district's enrollment assumptions. But raw analysis doesn't reach people — each persona needs the findings framed in their own context, language, and decision-making frame. Phase 1 briefs are interventionist: not "here are some gaps" but "here's what you need to know before this decision gets made, and here's what nobody has shown you yet."

## Desired Outcomes

Each persona receives a brief that translates enrollment gaps into their specific frame of concern. Maria understands what enrollment trends mean for her kids' school. Tom can challenge the savings math when the enrollment assumptions underneath don't hold. Linda has specific, sourced gaps she can raise in governance proceedings. Priya can see whether the analysis even accounts for the populations she advocates for. The briefs land before City Council budget adoption — timing matters as much as content.

## External Behavior

**Inputs:**
- Gap analysis structured output from SPEC-042 (JSON)
- Existing persona definitions (PERSONA-001 through PERSONA-004)
- Interpretation pipeline (INITIATIVE-003) for brief generation

**Outputs:**
- Per-persona Phase 1 briefs (markdown, one per persona)
- Each brief: persona-specific framing of the most significant gaps, what it means for their concerns, what questions they should be asking, what the district hasn't shown them
- Briefs suitable for publication on the site (INITIATIVE-004) and distribution
- Interventionist tone throughout — not neutral gap reporting

**Constraints:**
- Must use the interpretation pipeline (INITIATIVE-003) for generation — not hand-written
- Persona names must not match real people (standing project rule)
- Tone is interventionist but evidence-based — every claim in the brief must trace back to the gap analysis
- Must be published before City Council budget adoption (time-sensitive)

## Acceptance Criteria

1. Given each persona (Maria, Tom, Linda, Priya), when their Phase 1 brief is generated, then it addresses at least 3 enrollment gaps specific to their concern frame
2. Given any claim in a brief, when traced to the gap analysis, then the underlying evidence is found and correctly characterized
3. Given the briefs, when read by a non-expert, then the interventionist framing is clear — not neutral academic tone but "here's what you need to know"
4. Given the interpretation pipeline, when invoked with gap analysis data and persona context, then briefs are generated without manual content authoring
5. Given the briefs, when published to the site, then each persona's page shows the Phase 1 enrollment brief alongside existing content

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

- Phase 1 only — briefs cover gap exposure, not independent projections (that's Phase 2 / SPEC-046)
- Four personas: Maria, Tom, Linda, Priya
- Briefs generated through interpretation pipeline, not hand-authored
- Time-sensitive delivery — must land before City Council budget adoption
- Known limitation: briefs can only reference publicly available evidence

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-30 | — | Decomposed from EPIC-023; Track 1 time-sensitive |
