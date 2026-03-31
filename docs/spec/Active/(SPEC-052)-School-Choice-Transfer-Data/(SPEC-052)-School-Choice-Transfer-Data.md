---
title: "School Choice Transfer Data"
artifact: SPEC-052
track: implementable
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
type: feature
parent-epic: EPIC-026
linked-artifacts:
  - INITIATIVE-005
depends-on-artifacts: []
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# School Choice Transfer Data

## Problem Statement

School choice transfers (students opting out to private/charter/neighboring districts, and students opting in) are a significant enrollment driver that the cohort survival model needs to account for. Maine DOE may publish transfer data, or it may require a separate data request. This spec acquires whatever is publicly available and documents the gap if it's not.

## Desired Outcomes

The project either has school choice transfer flow data for South Portland or has documented that the data is unavailable and estimated the magnitude from other indicators (e.g., difference between census-age population and actual enrollment).

## External Behavior

**Inputs:** Maine DOE school choice reporting, district annual reports, or FOAA request

**Outputs:** Either:
- Trove at `docs/troves/school-choice-transfers/` with transfer counts by year and direction (in/out), OR
- Gap documentation in `docs/troves/enrollment-claims/synthesis.md` noting that transfer data is unavailable, with an estimate of net transfer magnitude from indirect indicators

**Constraints:**
- Maine's school choice law (LD 1817 / Title 20-A §5205) requires districts to report transfers. Check whether DOE publishes aggregate data.
- If district-level transfer data isn't publicly available, document what would be needed (FOAA request scope) for future acquisition

## Acceptance Criteria

- Given a search of Maine DOE data portals, when school choice transfer data is found, then it is collected into a trove with year-over-year trends
- Given transfer data is not publicly available, when the gap is documented, then the documentation includes: what was searched, what would need to be requested, and an indirect estimate of net transfer magnitude
- Given either outcome, when the cohort survival model (SPEC-058) is built, then school choice is either modeled from data or handled as an explicit assumption with stated uncertainty

## Scope & Constraints

**In scope:** Data search, acquisition if available, gap documentation if not.
**Out of scope:** Modeling the behavioral dynamics of school choice (that's SPEC-059 scenario brackets).

**Decision made (flagged for review):** This spec is Active rather than gated behind a spike because the search itself is quick — either the data exists publicly or it doesn't. If it doesn't, the deliverable is documentation, not a failed spec.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-026 |
