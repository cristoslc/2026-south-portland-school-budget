---
title: "DHHS Birth Records Trove"
artifact: SPEC-049
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

# DHHS Birth Records Trove

## Problem Statement

The cohort survival model needs birth data by municipality to project the kindergarten entry pipeline 5 years out. Maine DHHS publishes vital statistics including births by municipality, but this data has not been collected.

## Desired Outcomes

The project has birth count data for South Portland by year, covering at least 2016-2025 (children who will enter kindergarten through FY31), enabling kindergarten cohort size projection.

## External Behavior

**Inputs:** Maine DHHS vital statistics reports (likely PDF or Excel, published annually)

**Outputs:** Trove at `docs/troves/dhhs-birth-records/` containing:
- Raw source files in `sources/`
- Normalized data (CSV with columns: year, municipality, birth_count)
- `synthesis.md` noting trends, data quality, and lag considerations (vital stats often publish 1-2 years behind)
- `trove.yaml` manifest

**Constraints:**
- Municipal-level granularity (not just county)
- If municipal data is unavailable, county-level with South Portland's share estimated from census population ratios
- Note any data lag (most recent year available may be 2023 or 2024)

## Acceptance Criteria

- Given DHHS vital statistics, when the trove is collected, then birth counts for South Portland (or Cumberland County with apportionment method documented) are available for at least 8 consecutive years
- Given the normalized data, when used to project kindergarten entry, then the pipeline shows expected K cohort sizes for FY27-FY31
- Given data lag, when the most recent available year is documented, then the gap between latest data and projection period is explicit

## Scope & Constraints

**In scope:** Birth data acquisition and normalization.
**Out of scope:** Kindergarten entry rate modeling (that's SPEC-058 — birth-to-K conversion requires assumptions about private school, homeschool, and migration).

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-026 |
