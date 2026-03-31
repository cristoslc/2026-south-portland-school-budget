---
title: "Before/After Care Gap Analysis"
artifact: SPEC-064
track: implementable
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
type: feature
parent-epic: EPIC-031
linked-artifacts:
  - INITIATIVE-006
  - SPEC-060
  - SPEC-063
depends-on-artifacts:
  - SPEC-060
  - SPEC-063
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Before/After Care Gap Analysis

## Problem Statement

57% of surveyed parents cited disruption to before/after care as a concern. Split-building families under Option A or Variant C face mismatched schedules — if primary and intermediate schools have different start times, who manages extended care? The parent who testified at March 2 described this as "proposals will crush us" for working families with one car. Nobody has quantified the gap.

## Desired Outcomes

For each configuration, an estimate of how many families face a before/after care gap created by the reconfiguration, and what the cost implications are (either as district-provided extended care or as a family cost burden).

## External Behavior

**Inputs:**
- Split-family count by configuration (SPEC-060 output)
- Bell schedule tier analysis (SPEC-063 output — earliest start, latest end per building)
- Current before/after care programs (if documented in evidence pools)

**Outputs:**
- `docs/analysis/before-after-care-gap.md`
- Gap estimate: configuration, split_families_with_schedule_mismatch, estimated_minutes_of_gap, current_care_coverage (yes/no)
- Cost estimate: per-family annual before/after care cost (market rate for South Portland area) × families affected

**Constraints:**
- This analysis combines the split-family model (SPEC-060) with the bell schedule analysis (SPEC-063) — it can't be completed until both are done
- Market rate for before/after care in the Portland metro area is estimable from published data (Boys & Girls Club, YMCA, private providers)
- Document whether the district currently provides or subsidizes before/after care at elementary schools

## Acceptance Criteria

- Given split-family counts and bell schedule data, when the care gap is calculated, then the number of families facing schedule mismatches is estimated per configuration
- Given market rates for care, when the cost burden is estimated, then it's expressed as annual cost per affected family and total cost across all affected families
- Given Option B (no grade-band split), when the gap is analyzed, then it shows zero or minimal before/after care disruption (confirming the structural advantage)

## Scope & Constraints

**In scope:** Care gap quantification, cost estimation.
**Out of scope:** Recommending specific care solutions. Evaluating existing care provider capacity.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-031 |
