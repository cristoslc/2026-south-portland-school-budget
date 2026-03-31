---
title: "Maine DOE Enrollment Data Trove"
artifact: SPEC-048
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

# Maine DOE Enrollment Data Trove

## Problem Statement

The cohort survival model (EPIC-028) requires grade-level enrollment data for South Portland going back 10+ years. This data is published by the Maine Department of Education but has not been collected into the project's trove system.

## Desired Outcomes

The project has a normalized, structured trove of historical enrollment data at grade-level granularity for South Portland, enabling cohort retention/attrition rate calculation and trend analysis.

## External Behavior

**Inputs:** Maine DOE public enrollment data portal (likely CSV/Excel downloads by district, by grade, by year)

**Outputs:** Trove at `docs/troves/maine-doe-enrollment/` containing:
- Raw source files in `sources/`
- Normalized data in structured format (CSV with columns: year, district, grade, enrollment_count)
- `synthesis.md` summarizing key trends, anomalies, and data quality notes
- `trove.yaml` manifest

**Preconditions:** swain-search trove infrastructure exists and is functional

**Constraints:**
- Data must cover at least 2015-16 through 2025-26 (10 school years)
- Grade-level resolution (K through 12, not just district totals)
- If per-school data is available from DOE, collect that too (feeds SPIKE-009 stretch goals)

## Acceptance Criteria

- Given the Maine DOE enrollment portal, when the trove is collected, then grade-level enrollment for South Portland is available for at least 10 consecutive school years
- Given the normalized data, when loaded into a spreadsheet or script, then each row represents one grade-year combination with a numeric enrollment count
- Given the synthesis document, when read, then key enrollment trends (overall decline, elementary collapse, grade-level patterns) are summarized with year-over-year deltas

## Scope & Constraints

**In scope:** Data acquisition, normalization, synthesis for South Portland. Peer district data if easily available from the same source.
**Out of scope:** Modeling, analysis, projection. That's SPEC-058.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-026 |
