---
title: "McKinney-Vento Exposure Analysis"
artifact: SPEC-061
track: implementable
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
type: feature
parent-epic: EPIC-031
linked-artifacts:
  - INITIATIVE-006
depends-on-artifacts:
  - SPEC-048
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# McKinney-Vento Exposure Analysis

## Problem Statement

McKinney-Vento eligible students (1% → 10% of the student body) have a federal right to transportation to their school of origin, even after redistricting. Closing Kaler and redistricting those students triggers school-of-origin transport obligations that could persist for years. This is an unfunded mandate baked into the closure decision that doesn't appear in the $1.5-2.2M savings estimate.

## Desired Outcomes

An order-of-magnitude estimate of the McKinney-Vento transportation cost exposure created by the closure, broken down by configuration. This surfaces a cost category nobody has publicly quantified.

## External Behavior

**Inputs:**
- McKinney-Vento percentage from evidence pools (10% of 2,744 = ~274 students district-wide)
- Elementary enrollment (~1,080 students; ~108 McKinney-Vento eligible at elementary level)
- Kaler enrollment (estimated from available data)
- Per-pupil transport cost from SPEC-053

**Outputs:**
- `docs/analysis/mckinney-vento-exposure.md` — analysis and cost estimate
- Comparison table: configuration, displaced_mv_students, estimated_transport_obligation_years, annual_cost_range

**Analysis approach:**
1. Estimate McKinney-Vento eligible students at Kaler (proportional to district rate or higher if Kaler serves higher-need population)
2. Under federal law, these students can remain at their school of origin with district-provided transportation. With Kaler closing, "school of origin" becomes the receiving school — but the transition itself may trigger obligations for students already displaced from other schools attending Kaler.
3. Estimate incremental transport cost per student (difference between current route and new school-of-origin route)
4. Estimate duration of obligation (typically until the student completes the terminal grade of the school)
5. Produce annual cost range for each configuration

**Constraints:**
- McKinney-Vento law is federal; reference 42 U.S.C. § 11432
- The cost estimate is order-of-magnitude — present as a range
- Note that the 10% district rate may undercount (McKinney-Vento eligibility is self-reported and often undercounted)

## Acceptance Criteria

- Given district McKinney-Vento data and elementary enrollment, when the exposure is calculated, then the number of affected students is estimated
- Given the cost model, when applied to each configuration, then the incremental transport obligation is estimated as an annual cost range
- Given the analysis, when compared to the $1.5-2.2M claimed savings, then the McKinney-Vento obligation is expressed as a percentage of those savings

## Scope & Constraints

**In scope:** McKinney-Vento exposure estimation.
**Out of scope:** SPED transport obligations (related but separate — could be a future spec). Legal analysis of specific obligations (this is a cost estimation, not legal advice).

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-031 |
