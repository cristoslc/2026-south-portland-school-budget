---
title: "Building-Level Data Feasibility"
artifact: SPIKE-009
track: container
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
question: "Can we obtain or approximate building-level enrollment projections and functional capacity analysis using publicly available data?"
gate: Pre-MVP
risks-addressed:
  - Without building-level data, enrollment projections remain district-wide and cannot inform which specific buildings are overcrowded or underutilized under different configurations
evidence-pool: ""
linked-artifacts:
  - INITIATIVE-005
  - EPIC-026
  - EPIC-028
---

# Building-Level Data Feasibility

## Summary

<!-- Populated on transition to Complete -->

## Question

Can we obtain or approximate building-level enrollment projections and functional capacity analysis using publicly available data? Specifically:

1. **Building-level enrollment:** Can census block demographic data overlaid with school catchment zone boundaries produce directionally useful enrollment estimates per school?
2. **Functional capacity:** Can the building capacity numbers cited in the district's reconfiguration presentations be combined with SPED/ELL/CDS service ratios to estimate functional (not seat-count) capacity?
3. **FOAA viability:** Would a Freedom of Access Act request to the district yield building utilization or room assignment data within a useful timeframe?

## Go / No-Go Criteria

- **Go (census overlay approach):** Census block data is available at sufficient granularity to distinguish school catchment zones, AND catchment zone boundaries are publicly documented or derivable from redistricting tool data.
- **Go (district data):** FOAA request is feasible and estimated response time is under 30 days.
- **Go (presentation extraction):** District reconfiguration presentations contain room counts, stated capacity, and enough detail to derive functional capacity estimates.
- **No-Go:** Census blocks are too coarse to map to catchment zones AND no district data is obtainable within project timeline.

## Pivot Recommendation

If building-level data is not feasible, document the limitation transparently in all deliverables and constrain EPIC-028 projections to district-wide totals. Note that this limits the project's ability to evaluate whether specific receiving schools can absorb displaced Kaler students — flag this as a question the district should answer.

## Findings

_To be populated during investigation._

### Investigation threads:

1. **Census data resolution:** Check American Community Survey (ACS) block group data for South Portland — what demographic fields are available, what geographic granularity?
2. **Catchment zone boundaries:** Check the redistricting tool evidence pool for zone maps or boundary definitions.
3. **District presentation mining:** Extract room counts and capacity claims from March 2 and March 9 presentations (already in evidence pools).
4. **FOAA precedent:** Research Maine FOAA requirements, typical response times for school district requests, and what data categories are covered.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-026 under INITIATIVE-005; user-approved |
