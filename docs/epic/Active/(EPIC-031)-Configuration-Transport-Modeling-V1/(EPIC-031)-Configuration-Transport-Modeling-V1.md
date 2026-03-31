---
title: "Configuration Transport Modeling (V1)"
artifact: EPIC-031
track: container
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
parent-vision: VISION-001
parent-initiative: INITIATIVE-006
priority-weight: high
success-criteria:
  - Split-family counts calculated for all three configurations
  - Bell schedule tier requirements estimated for each configuration
  - McKinney-Vento transport obligation exposure quantified (number of students, estimated cost range)
  - SEA staffing adequacy assessed against estimated route expansion for each configuration
  - Before/after care gap quantified for each configuration
  - Structured comparison output (JSON/CSV) produced
depends-on-artifacts:
  - EPIC-030
addresses: []
evidence-pool: ""
---

# Configuration Transport Modeling (V1)

## Goal / Objective

Model the transportation implications of three elementary reconfiguration options using publicly available data and current enrollment numbers. For each configuration, estimate the key transport metrics that the district has not analyzed: how many families are split across buildings, what bell schedule tiers are needed, what federal transport obligations are triggered, whether the post-cut SEA workforce can cover the routes, and where before/after care gaps emerge.

This is order-of-magnitude analysis, not route-level precision — disclosed as such in all outputs. The goal is to surface the relative transport burden across configurations, not to produce a routing plan.

## Desired Outcomes

The board, council, and community can compare reconfiguration options on transportation dimensions that were absent from the decision. The comparison reveals whether the administration's preferred option (Option A) has materially different transport costs and logistics burden than alternatives — information that should have been part of the decision basis.

## Scope Boundaries

**Three configurations modeled:**

| Config | Structure | Buildings |
|--------|-----------|-----------|
| **Option A** (admin recommendation) | 2 primary (Pre-K-1) + 2 intermediate (2-4) | Kaler closed |
| **Option B** (board alternative) | 4 buildings K-4, redistrict by proximity | Kaler closed |
| **Variant C** (citizen alternative) | 3 buildings Pre-K-2 + 1 building Grades 3-4 | Kaler closed |

**Metrics per configuration:**
- Split-family count: families with children in two different buildings simultaneously
- Bell schedule tier feasibility: number of tiers required, fleet coverage
- McKinney-Vento exposure: students with school-of-origin transport rights triggered by displacement
- SPED transport obligations: estimated door-to-door mandate exposure
- SEA staffing adequacy: 86 FTE (post-14% cut) against estimated route expansion
- Before/after care gap: families facing mismatched schedules across buildings

**Out of scope:**
- Route-level optimization (requires student addresses)
- Actual ride time estimation (requires routing software)
- V2 configuration space search (EPIC-033)

**Data dependency:** Uses current district enrollment numbers (soft dependency on [INITIATIVE-005](../../../initiative/Active/(INITIATIVE-005)-Independent-Enrollment-Study/(INITIATIVE-005)-Independent-Enrollment-Study.md)). Updates when independent projections become available.

## Child Specs

| Artifact | Title | Status |
|----------|-------|--------|
| SPEC-060 | Split-Family Count Model | Active |
| SPEC-061 | McKinney-Vento Exposure Analysis | Active |
| SPEC-062 | SEA Staffing Adequacy Assessment | Active |
| SPEC-063 | Bell Schedule Tier Analysis | Active |
| SPEC-064 | Before/After Care Gap Analysis | Active |
| SPEC-065 | Transport Configuration Comparison | Active |

## Key Dependencies

- EPIC-030 (transportation data acquisition — baseline data)
- Current enrollment by grade (from existing evidence pools)
- School location and catchment zone data (from EPIC-030)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of INITIATIVE-006; user-approved |
