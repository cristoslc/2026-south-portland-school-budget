---
title: "Cohort Survival Projection Model"
artifact: SPEC-044
track: implementable
status: Proposed
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
priority-weight: high
type: ""
parent-epic: EPIC-024
linked-artifacts: []
depends-on-artifacts:
  - SPEC-039
  - SPEC-041
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Cohort Survival Projection Model

## Problem Statement

The district is making a permanent infrastructure decision based on enrollment decline without publishing any enrollment projections. Standard demographic methodology (cohort survival) can produce defensible projections from publicly available data — grade-to-grade retention rates, birth-to-kindergarten pipeline, and historical trends. This spec builds that model.

## Desired Outcomes

An independent, reproducible enrollment projection model that anyone can inspect, validate, and update as new data arrives. The model uses standard demographic methodology (cohort survival ratios) that school districts and state demographers routinely use, making it credible and comparable. When Fall 2026 enrollment numbers are published, the model's projections can be checked against reality.

## External Behavior

**Inputs:**
- Maine DOE grade-level enrollment data (from SPEC-039 trove): 10+ years, K-12
- DHHS birth records (from SPEC-041 trove): municipal births lagged 5-6 years for kindergarten pipeline
- Historical grade-to-grade retention rates calculated from DOE data

**Outputs:**
- Python module implementing cohort survival methodology
- Grade-level retention/attrition rate calculations from historical data
- Birth-to-kindergarten pipeline model (births → kindergarten entry with configurable lag)
- Baseline 5-year projection (FY27-FY31) using historical trend continuation
- Per-grade, per-year enrollment projections with confidence indicators
- Methodology documentation sufficient for independent reproduction
- Structured data output (JSON/CSV) for downstream consumption

**Preconditions:**
- DOE enrollment data spans at least 10 years for stable retention rate calculation
- Birth data spans at least 10 years for pipeline modeling

**Constraints:**
- Model must be deterministic and reproducible given the same inputs
- All assumptions explicit and documented — no hidden parameters
- Standard cohort survival methodology (NCES-compatible)
- Model code in Python, runnable with `uv`

## Acceptance Criteria

1. Given DOE enrollment data, when retention rates are calculated, then grade-to-grade survival ratios are produced for each year in the dataset with documentation of calculation method
2. Given the baseline model, when run for FY27, then the projection for the current year can be compared against known actual enrollment to validate the model
3. Given the model, when run for FY27-FY31, then per-grade enrollment projections are produced for each year with the assumption set documented
4. Given birth records, when the kindergarten pipeline model runs, then projected kindergarten cohort sizes for FY27-FY31 are produced with documented birth-year-to-K lag
5. Given the model outputs, when exported as JSON, then downstream consumers (INITIATIVE-001 lever analysis, site) can parse without manual transformation
6. Given the methodology documentation, when read by a demographer or policy analyst, then the approach is reproducible from the description alone

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

- Baseline model only — scenario brackets are SPEC-045's scope
- District-level projections only (building-level is a stretch goal gated by SPIKE-009)
- No Monte Carlo or probabilistic methods in v1 — deterministic cohort survival with explicit assumptions
- Model validation against known recent-year enrollment is required before producing forward projections
- Python with uv for dependency management

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-30 | — | Decomposed from EPIC-024 |
