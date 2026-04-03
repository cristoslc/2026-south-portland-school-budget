---
title: "Equity Overlay on Modeled Burden"
artifact: SPEC-078
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
  - EPIC-034
  - SPEC-077
depends-on-artifacts:
  - SPEC-076
  - SPEC-077
addresses:
evidence-pool: sopo-redistricting-tool
source-issue: ""
swain-do: required
---

# Equity Overlay on Modeled Burden

## Problem Statement

Transport burden alone is not enough. The project needs to know whether modeled harm lands evenly or clusters in less-advantaged places. It needs a clear way to join burden outputs to equity geography and to state what those joins prove.

## Desired Outcomes

The project can make careful equity claims about place-based disparity. It can say whether modeled burden falls harder on some places, while avoiding claims about individual student traits.

## External Behavior

**Inputs:**
- Burden outputs from SPEC-077
- Neighborhood geography and public income overlays
- Any school or area proxy data that can be defended publicly

**Outputs:**
- An equity overlay dataset joining burden metrics to geography
- Summary tables showing burden concentration by neighborhood or proxy group
- A short methods note defining what the equity lens measures and what it cannot measure

**Constraints:**
- Must not infer individual protected traits from aggregate geography
- Must distinguish direct measures from proxy-based inference
- Must document the unit used for each disparity claim

## Acceptance Criteria

- Given the burden outputs, when the equity overlay runs, then each analysis geography has both burden metrics and the chosen proxy indicators attached
- Given the summary tables, when a reader reviews them, then they can see whether burden concentrates in less-advantaged areas
- Given the methods note, when a skeptical reader reviews it, then the difference between place disparity and student-level evidence is clear
- Given the final outputs, when a later brief cites them, then the brief can quote both the finding and the caveat from the same source

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

In scope: geographic and socioeconomic disparity analysis.
Out of scope: student-level protected-class inference, legal discrimination findings, or claims beyond the available proxies.

## Implementation Approach

Use burden outputs as the left side of the join. Add only public overlays you can defend. Keep the methods note with the data so later claims stay disciplined.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-04-03 | — | Initial creation |
