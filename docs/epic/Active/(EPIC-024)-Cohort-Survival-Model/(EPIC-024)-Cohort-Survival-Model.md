---
title: "Cohort Survival Model & 5-Year Projections"
artifact: EPIC-024
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
  - Retention/attrition rates calculated from historical DOE enrollment data
  - Birth-to-kindergarten pipeline modeled from DHHS vital records
  - At least 3 scenario brackets produced: baseline trend continuation, LD 1829 housing density absorption, multilingual learner pipeline sensitivity
  - CDS pre-K mandate ramp incorporated as a scenario variable
  - 5-year projections (FY27-FY31) generated with explicit assumptions documented per scenario
  - Projection data structured as JSON/CSV consumable by INITIATIVE-001 lever analysis
depends-on-artifacts:
  - EPIC-022
addresses: []
evidence-pool: ""
---

# Cohort Survival Model & 5-Year Projections

## Goal / Objective

Build an independent demographic projection model that produces 5-year enrollment forecasts with scenario brackets. This is the analytical engine that replaces the missing district projections — not point estimates but ranges under explicit, testable assumptions.

## Desired Outcomes

The public has access to the enrollment projections the district never published. Anyone can inspect the assumptions, test them against incoming data each fall, and evaluate whether the closure decision was made on a defensible enrollment basis. INITIATIVE-001's lever analysis can plug in enrollment scenarios instead of treating enrollment as a static given.

## Scope Boundaries

**In scope:**
- Cohort survival methodology: grade-to-grade retention/attrition rates from 10+ years of DOE data
- Birth-to-kindergarten pipeline: DHHS birth records lagged 5-6 years to kindergarten entry
- Scenario modeling:
  - Baseline: trend continuation from historical retention rates
  - LD 1829 housing absorption: housing density impact on family in-migration
  - Multilingual learner pipeline: sensitivity to federal immigration/education policy shifts
  - CDS pre-K ramp: 80-90 four-year-olds entering the K pipeline earlier
- 5-year projection horizon (FY27-FY31)
- Structured data output (JSON/CSV) for downstream consumption
- Methodology documentation sufficient for independent reproduction

**Stretch goals (data-gated, see SPIKE-009):**
- Building-level projections using census block demographic overlay
- Functional capacity analysis (available space vs. seat count given SPED/ELL/behavioral needs)

**Out of scope:**
- Interpretation or brief writing (that's EPIC-025)
- Transportation or route modeling
- Projections beyond 5-year horizon

## Child Specs

| Artifact | Title | Status |
|----------|-------|--------|
| SPEC-044 | Cohort Survival Projection Model | Proposed |
| SPEC-045 | Scenario Brackets & Structured Data Output | Proposed |

## Key Dependencies

- **EPIC-022** — Maine DOE enrollment history and DHHS birth records must be collected before model can be built
- **INITIATIVE-001** — downstream consumer of structured projection data
- **Methodological reference** — standard cohort survival methodology (NCES, state demographer practices)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-30 | — | Decomposed from INITIATIVE-005; Track 2 |
| Active | 2026-03-30 | -- | Operator approved; child SPECs created |
