---
title: "Modeled Walkability and Drive Burden Baseline"
artifact: SPEC-077
track: implementable
status: Proposed
author: cristos
created: 2026-04-03
last-updated: 2026-04-03
priority-weight: high
type: feature
parent-epic: EPIC-034
parent-initiative: ""
linked-artifacts:
  - INITIATIVE-006
  - EPIC-031
  - SPEC-076
depends-on-artifacts:
  - SPEC-076
  - SPEC-065
addresses:
evidence-pool: sopo-redistricting-tool
source-issue: ""
swain-do: required
---

# Modeled Walkability and Drive Burden Baseline

## Problem Statement

The repo already computes walk and drive distances from the road network. The project still lacks a post-decision burden baseline that uses those distances to show walk loss, reassignment clusters, and long-drive risk.

## Desired Outcomes

The transport case moves from vague claims to concrete burden. Readers can see the block and neighborhood pattern of harm behind the adopted plan.

## External Behavior

**Inputs:**
- Validated block weights from SPEC-076
- Repo travel matrices and scenario outputs
- Block geometry and school geometry from the ingested repo

**Outputs:**
- Block-level burden table for the adopted plan
- Neighborhood or aggregation-level burden summaries
- Metrics for walkability loss, drive burden, reassignment volume, and tail risk
- A methods note stating which metrics come from the model and which are recomputed for advocacy use

**Constraints:**
- Must reuse the repo's road-network walk and drive model
- Must distinguish centroid-based travel from observed travel
- Must state whether averages use student weights, population weights, or both

## Acceptance Criteria

- Given the repo's walk and drive matrices, when the burden baseline runs, then each block receives walkability and drive-burden fields grounded in the modeled distances
- Given the adopted plan output, when burden metrics are computed, then the analysis identifies blocks and geographies with the largest walk loss and longest drive burden
- Given the final tables, when a reader inspects them, then they can tell which metrics come from the repo and which were recomputed here
- Given the methods note, when a skeptical reader reviews it, then centroid and weighting caveats are explicit

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

In scope: modeled burden baseline for the adopted plan.
Out of scope: route planning, bus timing simulation, or alternative closure advocacy.

## Implementation Approach

Start from the repo's `walk_df`, `drive_df`, and assignment outputs. Build a burden layer for blocks and neighborhoods. Expose raw and summary outputs for later specs.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-04-03 | — | Initial creation |
