---
title: "Configuration Space Optimization (V2)"
artifact: EPIC-033
track: container
status: Proposed
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
parent-vision: VISION-001
parent-initiative: INITIATIVE-006
priority-weight: low
success-criteria:
  - Transport burden metrics formally defined from V1 findings
  - Feasible configuration space enumerated (buildings x grade-band boundaries)
  - At least one alternative configuration identified that outperforms Options A and B on transport metrics
  - Results documented with methodology sufficient for replication
depends-on-artifacts:
  - EPIC-031
addresses: []
evidence-pool: ""
---

# Configuration Space Optimization (V2)

## Goal / Objective

Expand beyond the three hand-picked configurations modeled in V1 to systematically search the feasible configuration space. Define transport burden as a composite metric from V1's individual measures (split-family count, McKinney-Vento exposure, bell schedule complexity, SEA staffing adequacy, before/after care gap), then evaluate all plausible configurations of 3-4 buildings across reasonable grade-band boundaries.

This is a stretch goal. Scope and feasibility depend on V1 learnings — the modeling framework built in EPIC-031 determines what's tractable here.

## Desired Outcomes

The community has evidence-based alternatives beyond the options the administration presented. If a configuration exists that significantly reduces transport burden while achieving comparable savings, that finding has value for future planning — even if the board has already voted. The methodology demonstrates that citizen analysis can surface options the district didn't consider.

## Scope Boundaries

**In scope:**
- Formal definition of composite transport burden metric
- Enumeration of feasible configuration space (constrained by building count, grade-band options, capacity)
- Optimization search across configurations
- Route distance estimation using catchment geometry (if feasible)
- Equity analysis of ride time distribution by neighborhood (if data supports it)
- Results documentation

**Out of scope:**
- Route-level optimization requiring student addresses
- Implementation planning for alternative configurations
- Advocacy for any specific configuration

## Child Specs

_To be decomposed if/when this epic is activated._

## Key Dependencies

- EPIC-031 (V1 modeling — provides framework, metrics, and baseline data)
- EPIC-030 (catchment geometry and school location data)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-30 | — | V2 stretch goal; activation depends on V1 completion and learnings |
