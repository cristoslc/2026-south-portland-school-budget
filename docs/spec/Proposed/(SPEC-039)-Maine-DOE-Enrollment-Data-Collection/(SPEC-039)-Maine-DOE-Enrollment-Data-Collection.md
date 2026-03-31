---
title: "Maine DOE Enrollment Data Collection"
artifact: SPEC-039
track: implementable
status: Proposed
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
priority-weight: high
type: ""
parent-epic: EPIC-022
linked-artifacts: []
depends-on-artifacts: []
addresses:
  - JOURNEY-002.PP-03
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Maine DOE Enrollment Data Collection

## Problem Statement

The district cites declining enrollment as the primary structural driver for school closure, but no independent enrollment data has been compiled for public analysis. The Maine DOE publishes grade-level enrollment data that could establish an authoritative 10+ year baseline for South Portland, but it hasn't been collected, normalized, or made accessible for this analysis.

## Desired Outcomes

The project has a complete, structured, citable dataset of South Portland K-12 enrollment by grade level spanning at least 10 years. This data feeds both the gap analysis (EPIC-023) and the cohort survival model (EPIC-024). Anyone can trace the project's enrollment claims back to official DOE sources.

## External Behavior

**Inputs:**
- Maine DOE public enrollment data portal/files
- Target: South Portland School Department, grades K-12, at least 10 school years (2015-16 through 2025-26)

**Outputs:**
- swain-search trove containing normalized enrollment data (CSV and/or JSON)
- Per-year, per-grade enrollment counts for South Portland
- Source citation metadata (URLs, access dates, DOE report identifiers)
- Data dictionary documenting field definitions and any transformations applied

**Preconditions:**
- Maine DOE enrollment data is publicly accessible (known to be true — published annually)

**Constraints:**
- Data must be collected from official DOE sources, not third-party aggregations
- All transformations documented (no opaque data munging)

## Acceptance Criteria

1. Given the trove exists, when queried for any school year from 2015-16 through 2025-26, then grade-level enrollment counts for South Portland K-12 are returned
2. Given the trove exists, when inspected, then every data point traces to a DOE source with URL and access date
3. Given the data, when compared to district-published figures (e.g., 3,085 total in 2015-16, 2,744 current), then the DOE data either confirms or reveals discrepancies
4. Given the trove, when consumed by a downstream analysis script, then the data is parseable without manual intervention (structured CSV/JSON with documented schema)

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

- Only South Portland School Department data (not statewide)
- DOE data may have reporting lags — document the most recent year available
- If grade-level breakdowns are unavailable for some years, document the gap and collect at the finest available granularity
- School choice transfer data is a separate spec (SPEC-041) — this spec covers standard enrollment counts only

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-30 | — | Decomposed from EPIC-022 |
