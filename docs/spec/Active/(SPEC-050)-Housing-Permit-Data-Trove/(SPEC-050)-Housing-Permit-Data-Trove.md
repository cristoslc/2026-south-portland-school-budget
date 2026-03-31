---
title: "Housing Permit Data Trove"
artifact: SPEC-050
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

# Housing Permit Data Trove

## Problem Statement

LD 1829 housing density development is a key enrollment uncertainty — the PERSONA-007 brief explicitly asks whether the administration has modeled what happens if residential density development adds 50-100 elementary students within three years. Housing permit data from the city would ground this scenario bracket.

## Desired Outcomes

The project has housing permit data for South Portland showing recent and planned residential development, enabling an estimate of potential enrollment increase from new housing absorption.

## External Behavior

**Inputs:** City of South Portland planning office data — building permits, approved developments, planning board records. Likely available via city website, FOAA request, or Census Building Permits Survey.

**Outputs:** Trove at `docs/troves/housing-permits/` containing:
- Raw source files in `sources/`
- Normalized data (CSV with columns: year, permit_type, units, location/neighborhood, status)
- `synthesis.md` summarizing development trends, LD 1829 impact, and estimated unit counts by area
- `trove.yaml` manifest

**Constraints:**
- Focus on residential permits (single-family, multi-family, mixed-use with residential)
- If city data portal exists, prefer that. If not, Census Building Permits Survey provides municipal-level annual totals.
- Geographic detail (which part of town) is valuable for building-level stretch goals but not required for district-wide projection

## Acceptance Criteria

- Given housing permit sources, when the trove is collected, then residential permit/unit counts for South Portland are available for at least 5 years (2021-2025)
- Given LD 1829 context, when planned/approved developments are documented, then the pipeline of future units expected in the next 3-5 years is estimated
- Given the synthesis, when read, then the estimated student yield (students per new housing unit, typically 0.3-0.5 for multi-family) is noted with methodology reference

## Scope & Constraints

**In scope:** Permit data acquisition, development pipeline documentation.
**Out of scope:** Student yield modeling (that's SPEC-059 scenario brackets). Geographic mapping to catchment zones (that's SPIKE-009).

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-026 |
