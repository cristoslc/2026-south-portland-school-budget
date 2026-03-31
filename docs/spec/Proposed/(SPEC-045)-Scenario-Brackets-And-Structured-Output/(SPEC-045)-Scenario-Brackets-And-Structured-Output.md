---
title: "Scenario Brackets & Structured Data Output"
artifact: SPEC-045
track: implementable
status: Proposed
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
priority-weight: high
type: ""
parent-epic: EPIC-024
linked-artifacts:
  - INITIATIVE-001
depends-on-artifacts:
  - SPEC-044
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Scenario Brackets & Structured Data Output

## Problem Statement

The baseline cohort survival model (SPEC-044) answers "what happens if current trends continue?" But the closure decision depends on factors the baseline doesn't capture: LD 1829 housing density changes, multilingual learner pipeline sensitivity to federal policy, and CDS pre-K mandate ramp. Scenario brackets let decision-makers see the range of plausible futures rather than a single line.

## Desired Outcomes

Decision-makers can compare enrollment futures under different assumptions. Instead of "enrollment will be X," they see "under baseline trends X, under housing growth Y, under multilingual learner pipeline shifts Z." INITIATIVE-001's lever analysis can test whether closure savings hold up across the scenario range, not just one assumption.

## External Behavior

**Inputs:**
- Baseline cohort survival model from SPEC-044
- Housing permit data from SPEC-041 (for LD 1829 absorption scenario)
- Multilingual learner enrollment trends from DOE data (SPEC-039)
- CDS pre-K enrollment plans (from existing evidence pools)

**Outputs:**
- At least 3 scenario brackets:
  1. **Baseline**: historical trend continuation (from SPEC-044)
  2. **LD 1829 Housing Absorption**: models increased family in-migration from housing density changes
  3. **Multilingual Learner Pipeline Shift**: models sensitivity to federal immigration/education policy
  4. *(Optional)* **CDS Pre-K Ramp**: models 80-90 four-year-olds entering the K pipeline earlier
- Per-scenario: documented assumptions, parameter values, and rationale
- Scenario comparison data (JSON/CSV): per-year, per-grade projections for each scenario
- Scenario comparison visualization data (structured for charting)
- Structured data API/export consumable by INITIATIVE-001 and the site (INITIATIVE-004)

**Constraints:**
- Each scenario must have explicitly documented assumptions and parameter choices
- Scenarios represent plausible futures, not worst/best case extremes
- Parameter sensitivity: document which assumptions have the largest impact on projections
- All scenario data in the same structured format as baseline for easy comparison

## Acceptance Criteria

1. Given the scenario suite, when inspected, then at least 3 distinct scenarios exist with documented assumptions differing from baseline
2. Given the LD 1829 scenario, when inspected, then housing permit data is incorporated and the assumption connecting permits to student enrollment is explicitly documented
3. Given the multilingual learner scenario, when run with different federal policy sensitivity parameters, then enrollment projections shift meaningfully (>2% total enrollment difference from baseline over 5 years)
4. Given all scenarios, when exported as JSON, then each contains per-grade, per-year projections in the same schema as baseline
5. Given the scenario comparison, when visualized, then the bracket range is clear — not overlapping indistinguishably from baseline
6. Given INITIATIVE-001 lever analysis, when it consumes scenario data, then it can test whether closure savings hold under each scenario independently

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

- Scenarios are deterministic variations on the baseline model, not probabilistic distributions
- District-level only (building-level scenarios gated by SPIKE-009)
- CDS pre-K scenario is optional — include if existing evidence pool data is sufficient to parameterize it
- Parameter sensitivity analysis is required — document which assumptions matter most
- This spec produces the data; visualization/presentation is SPEC-047's scope

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-30 | — | Decomposed from EPIC-024 |
