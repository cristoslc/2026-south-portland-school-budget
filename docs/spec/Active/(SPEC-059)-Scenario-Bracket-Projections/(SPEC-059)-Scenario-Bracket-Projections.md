---
title: "Scenario Bracket Projections"
artifact: SPEC-059
track: implementable
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
type: feature
parent-epic: EPIC-028
linked-artifacts:
  - INITIATIVE-005
  - SPEC-058
  - SPEC-050
  - SPEC-052
depends-on-artifacts:
  - SPEC-058
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Scenario Bracket Projections

## Problem Statement

A single baseline projection is useful but incomplete. The closure decision depends on whether the enrollment decline is structural or cyclical — and that question has multiple plausible answers depending on assumptions about housing development, federal immigration policy, and school choice dynamics. Scenario brackets make these assumptions explicit and show the range of futures the board is deciding within.

## Desired Outcomes

Three (minimum) scenario brackets that bound the plausible enrollment future, each with explicit assumptions that can be tested against reality as years pass. The community can see: "under optimistic assumptions enrollment recovers to X; under pessimistic assumptions it falls to Y; under baseline it stays at Z."

## External Behavior

**Inputs:**
- Baseline cohort survival model (SPEC-058 output)
- Housing permit data (SPEC-050 output)
- School choice data or gap documentation (SPEC-052 output)
- Existing evidence on multilingual learner trends, CDS mandate

**Outputs:**
- Extended projection script that layers scenario assumptions on the baseline model
- Scenario projection CSV: year, grade, scenario_name, projected_enrollment
- Scenario documentation in `docs/analysis/enrollment-scenarios.md`

**Minimum scenario set:**
1. **Baseline (trend continuation):** Historical retention rates continue. No major policy or demographic shifts. This is the "null hypothesis."
2. **Housing growth (LD 1829):** New residential development adds students at estimated yield rates (0.3-0.5 students per new multi-family unit). Use housing permit pipeline from SPEC-050 to estimate magnitude.
3. **Migration shift:** Multilingual learner pipeline changes — model both a slowdown (federal enforcement reducing in-migration) and continued growth. This is the most uncertain variable; bracket it wide.

**Optional additional scenarios:**
4. **CDS ramp:** Pre-K expansion adds 80-90 four-year-olds FY27, three-year-olds FY28. While these students are technically new enrollment, model whether they convert to increased K enrollment in subsequent years.
5. **School choice shift:** If closure reduces confidence in the district, model increased outflow to private/charter.

**Constraints:**
- Each scenario must state its assumptions in plain language
- Each scenario must include a testable prediction: "if this scenario is correct, enrollment in grade X should be above/below Y by FY29"
- Scenarios are not recommendations — they are "if...then" statements

## Acceptance Criteria

- Given the baseline model and scenario assumptions, when scenarios are run, then at least 3 distinct projections are produced with different enrollment trajectories
- Given each scenario, when its assumptions are read, then a non-expert can understand what would have to be true for that scenario to materialize
- Given the testable predictions, when FY28 or FY29 enrollment data becomes available, then the community can evaluate which scenario the actual data matches

## Scope & Constraints

**In scope:** Scenario definition, modeling, documentation.
**Out of scope:** Building-level scenarios (gated on SPIKE-009). Probability assignment to scenarios (we're bracketing, not forecasting).

**Decision made (flagged for review):** I scoped this as minimum 3 scenarios rather than exactly 3, leaving room to add CDS ramp and school choice shift if the data supports them without overcomplicating the deliverable.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-028 |
