---
title: "Maine DOE Transport Expenditure Trove"
artifact: SPEC-053
track: implementable
status: Complete
author: cristos
created: 2026-03-30
last-updated: 2026-03-31
type: feature
parent-epic: EPIC-030
linked-artifacts:
  - INITIATIVE-006
depends-on-artifacts: []
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Maine DOE Transport Expenditure Trove

## Problem Statement

The fiscal exposure analysis needs per-pupil transportation cost data for South Portland and peer districts. Maine DOE publishes financial data by district that includes transportation expenditures. This enables benchmarking: is South Portland spending more or less than comparable districts, and what does that imply about the cost headroom for route expansion?

## Desired Outcomes

The project has transportation expenditure data for South Portland and 5-8 peer districts, enabling per-pupil cost comparison and order-of-magnitude cost estimation for route changes.

## External Behavior

**Inputs:** Maine DOE financial reports (ED279 or equivalent annual financial data by district)

**Outputs:** Trove at `docs/troves/maine-doe-transport-expenditure/` containing:
- Raw source files in `sources/`
- Normalized data (CSV with columns: year, district, total_transport_expenditure, enrollment, per_pupil_transport_cost)
- `synthesis.md` with peer comparison analysis, cost trends, and notes on what's included/excluded in the transport line item
- `trove.yaml` manifest

**Constraints:**
- Peer districts should be comparable in size, geography, and demographics. Candidates: Scarborough, Cape Elizabeth, Gorham, Westbrook, Portland (note: South Portland has a bus service agreement with Portland — document this).
- At least 3 years of data for trend analysis
- Document what the DOE transport expenditure line includes (regular routes, SPED transport, field trips, athletics) — the composition matters for cost comparison

## Acceptance Criteria

- Given Maine DOE financial data, when collected, then per-pupil transport cost is calculable for South Portland and at least 5 peer districts for 3+ years
- Given the peer comparison, when synthesized, then South Portland's transport spending is contextualized (above/below/at peer average, trend direction)
- Given the Portland bus agreement reference in the evidence pools, when documented, then the cost structure implications are noted

## Scope & Constraints

**In scope:** DOE financial data acquisition, peer benchmarking.
**Out of scope:** Route-level cost modeling, contract analysis (would require district data).

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-030 |
| Complete | 2026-03-31 | — | Trove populated with sources, CSV, and synthesis |
