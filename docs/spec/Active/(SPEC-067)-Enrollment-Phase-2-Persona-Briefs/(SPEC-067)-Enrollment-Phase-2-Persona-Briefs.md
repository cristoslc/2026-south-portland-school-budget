---
title: "Enrollment Phase 2 Persona Briefs"
artifact: SPEC-067
track: implementable
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
type: feature
parent-epic: EPIC-029
linked-artifacts:
  - INITIATIVE-005
  - SPEC-058
  - SPEC-059
depends-on-artifacts:
  - SPEC-057
  - SPEC-058
  - SPEC-059
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Enrollment Phase 2 Persona Briefs

## Problem Statement

Phase 1 briefs (SPEC-057) surface the gaps. Phase 2 briefs fill them — integrating the independent cohort survival projections and scenario brackets into persona-specific communication. These briefs go from "here's what's missing" to "here's what the data shows."

## Desired Outcomes

Each persona receives an updated enrollment brief that includes the independent projection, scenario brackets, and testable predictions. The community has a concrete, persona-framed answer to "is the decline structural or cyclical?"

## External Behavior

**Inputs:**
- Phase 1 briefs (SPEC-057 output) — gap framing to build on
- Cohort survival model output (SPEC-058)
- Scenario bracket projections (SPEC-059)
- Existing persona definitions

**Outputs:**
- 15 persona-specific Phase 2 enrollment briefs in `dist/briefings/enrollment-phase2/`
- 1 general Phase 2 brief
- Published to site

**Constraints:**
- Build on Phase 1 framing — don't replace it, extend it ("we showed you the gaps; now here's what independent analysis reveals")
- Each brief must include at least one testable prediction relevant to that persona
- Scenario brackets presented as ranges, not predictions — "if X assumption holds, enrollment will be between Y and Z"

## Acceptance Criteria

- Given Phase 1 briefs and projection data, when Phase 2 briefs are generated, then each extends the Phase 1 narrative with projection findings
- Given testable predictions, when included in briefs, then each persona has at least one "you'll know by FY29 whether..." statement
- Given scenario brackets, when presented, then the range of plausible futures is clear without false precision

## Scope & Constraints

**In scope:** Brief generation integrating projection findings.
**Out of scope:** New modeling. Building-level projections (unless SPIKE-009 succeeds).

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-029 |
