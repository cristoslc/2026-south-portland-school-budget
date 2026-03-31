---
title: "Cohort Survival Model"
artifact: SPEC-058
track: implementable
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
type: feature
parent-epic: EPIC-028
linked-artifacts:
  - INITIATIVE-005
  - SPEC-048
  - SPEC-049
depends-on-artifacts:
  - SPEC-048
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Cohort Survival Model

## Problem Statement

No independent enrollment projection exists for South Portland. The district is making permanent infrastructure decisions based on current-year enrollment without publishing forward projections. A cohort survival model is the standard methodology for school enrollment projection — track how each grade cohort flows through successive grades, apply retention/attrition rates, and project forward.

## Desired Outcomes

A transparent, reproducible cohort survival model that any data-literate citizen can inspect, challenge, and update. The model answers: given historical patterns, what is the baseline enrollment trajectory for the next 5 years?

## External Behavior

**Inputs:**
- Maine DOE grade-level enrollment (SPEC-048 output): 10+ years of K-12 enrollment by grade
- DHHS birth records (SPEC-049 output): kindergarten entry pipeline

**Outputs:**
- Python script or Jupyter notebook implementing the model at `pipeline/enrollment/cohort_survival.py`
- Baseline projection CSV: year, grade, projected_enrollment (FY27-FY31)
- Model parameters CSV: grade_transition, retention_rate, attrition_rate, confidence_interval
- Methodology document: `docs/analysis/cohort-survival-methodology.md`

**Model mechanics:**
1. Calculate grade-to-grade retention rates from historical data (e.g., Grade 1 in year N → Grade 2 in year N+1)
2. Use 3-year and 5-year rolling averages for rate stability
3. Project kindergarten entry from birth data with a birth-to-K conversion rate (historical average)
4. Apply retention rates forward to produce baseline projection
5. Include confidence intervals based on historical rate variance

**Constraints:**
- Must use `uv` for any Python dependencies (per project policy)
- Must run via `claude -p` if any LLM processing is needed (per LLM usage policy)
- Model must be deterministic (same inputs → same outputs)
- All assumptions documented in methodology document

## Acceptance Criteria

- Given 10 years of grade-level enrollment data, when the model runs, then it produces grade-by-grade projections for FY27-FY31
- Given birth data, when the kindergarten pipeline is calculated, then projected K cohort sizes are consistent with recent birth-to-K conversion rates
- Given the methodology document, when read by someone with basic statistics knowledge, then every assumption and calculation is reproducible
- Given the baseline projection, when compared to the district's current enrollment (2,744), then the 5-year trend direction and magnitude are stated

## Scope & Constraints

**In scope:** Baseline cohort survival model with single set of assumptions (historical trend continuation).
**Out of scope:** Scenario brackets (that's SPEC-059). Building-level breakdown (gated on SPIKE-009). Policy recommendations.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-028 |
