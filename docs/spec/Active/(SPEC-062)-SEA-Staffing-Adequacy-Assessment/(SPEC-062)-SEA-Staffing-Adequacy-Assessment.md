---
title: "SEA Staffing Adequacy Assessment"
artifact: SPEC-062
track: implementable
status: Complete
author: cristos
created: 2026-03-30
last-updated: 2026-03-31
type: feature
parent-epic: EPIC-031
linked-artifacts:
  - INITIATIVE-006
depends-on-artifacts:
  - SPEC-053
  - SPEC-054
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# SEA Staffing Adequacy Assessment

## Problem Statement

The SEA bargaining unit (facilities/food/transport) faces a 14% staffing reduction (100 → 86 FTE) — the highest percentage cut of any unit. Simultaneously, reconfiguration may require route expansion. Nobody has assessed whether the post-cut workforce can cover the expanded routes. This is a contradiction: cut the transport workforce while increasing transport demand.

## Desired Outcomes

An assessment of whether 86 SEA FTEs can cover the estimated route requirements under each configuration. If the answer is "probably not," quantify the gap.

## External Behavior

**Inputs:**
- SEA staffing data from budget documents (100 FTE → 86 FTE, but these cover facilities + food + transport — need to estimate the transport-specific share)
- Current route structure (from SPEC-055 bell schedule / tier data)
- Peer district driver/route ratios (from SPEC-053)

**Outputs:**
- `docs/analysis/sea-staffing-assessment.md`
- Estimate of transport-specific FTE share (pre-cut and post-cut)
- Estimated route/driver requirements under each configuration
- Gap analysis: shortfall or surplus under each scenario

**Constraints:**
- SEA covers three functions (facilities, food, transport) and the budget documents don't break out transport-specific FTE. Estimate from peer district ratios or reasonable allocation.
- This is a workforce adequacy question, not a cost question — cost implications are captured in the configuration comparison (SPEC-065)

## Acceptance Criteria

- Given SEA staffing data, when the transport share is estimated, then the methodology and assumptions are documented
- Given three configurations, when route requirements are estimated, then each produces a driver/route FTE requirement
- Given the pre-cut and post-cut FTE, when compared to requirements, then any staffing gap is identified and quantified

## Scope & Constraints

**In scope:** Workforce adequacy assessment.
**Out of scope:** Salary/benefit cost modeling. Union contract analysis. Recommendations on staffing levels.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-031 |
| Complete | 2026-03-31 | — | Analysis implemented; see docs/analysis/ |
