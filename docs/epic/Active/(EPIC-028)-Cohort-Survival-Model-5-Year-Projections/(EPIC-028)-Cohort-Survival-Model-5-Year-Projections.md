---
title: "Cohort Survival Model & 5-Year Projections"
artifact: EPIC-028
track: container
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
parent-vision: VISION-001
parent-initiative: INITIATIVE-005
priority-weight: high
success-criteria:
  - Cohort survival model implemented with grade-level resolution for South Portland K-12
  - Model produces 5-year projections (FY27-FY31)
  - At least 3 scenario brackets produced (baseline trend continuation, housing growth, migration shift)
  - CDS pre-K mandate ramp incorporated into projections
  - Projection data output as structured data consumable by INITIATIVE-001
  - All assumptions explicitly documented and testable
depends-on-artifacts:
  - EPIC-026
addresses: []
evidence-pool: ""
---

# Cohort Survival Model & 5-Year Projections

## Goal / Objective

Build an independent demographic projection model for South Portland school enrollment. The model uses cohort survival methodology — tracking how a grade-level cohort flows through successive grades with retention/attrition rates — layered with birth rate pipeline data (kindergarten entry), housing development absorption estimates, multilingual learner placement sensitivity to federal policy, and the CDS pre-K mandate ramp. Output is scenario brackets, not point estimates: ranges under explicit assumptions that make the district's own projections testable.

## Desired Outcomes

An independent, transparent enrollment projection exists as a public resource. Anyone can inspect the assumptions, challenge the inputs, and update the model as new data arrives each fall. The projection answers the central question: is the enrollment decline structural or cyclical, and does it justify irreversible infrastructure decisions? Within 2-3 years, the scenario brackets can be compared to actual enrollment to evaluate whether the closure was supported by demographic trends.

## Scope Boundaries

**In scope:**
- Cohort survival model with grade-level resolution (K-12)
- Input layers: historical retention/attrition rates, DHHS birth records (kindergarten pipeline), housing permit absorption, multilingual learner placement trends, CDS pre-K ramp (80-90 four-year-olds FY27, three-year-olds FY28)
- Scenario brackets: (1) baseline trend continuation, (2) LD 1829 housing density absorption, (3) multilingual learner pipeline shift (federal policy sensitivity)
- Structured data output (JSON/CSV) consumable by [INITIATIVE-001](../../../initiative/Active/(INITIATIVE-001)-Budget-Lever-Analysis/(INITIATIVE-001)-Budget-Lever-Analysis.md)
- Methodology documentation sufficient for replication

**Stretch goals (data-gated, per SPIKE-009):**
- Building-level projections using census block demographic overlay with catchment zone boundaries
- Functional capacity analysis against projected enrollment

**Out of scope:**
- Brief generation (EPIC-029)
- Student-level address data modeling

## Child Specs

_To be decomposed during implementation planning._

## Key Dependencies

- EPIC-026 (data acquisition — Maine DOE grade-level data, birth records, housing permits)
- [SPIKE-009](../../research/Active/(SPIKE-009)-Building-Level-Data-Feasibility/(SPIKE-009)-Building-Level-Data-Feasibility.md) gates stretch goals

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of INITIATIVE-005; user-approved |
