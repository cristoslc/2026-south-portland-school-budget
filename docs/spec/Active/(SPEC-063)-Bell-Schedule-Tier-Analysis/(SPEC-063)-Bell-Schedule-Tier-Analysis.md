---
title: "Bell Schedule Tier Analysis"
artifact: SPEC-063
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
  - SPEC-055
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Bell Schedule Tier Analysis

## Problem Statement

South Portland uses tiered bell schedules so the same bus fleet can run multiple routes. Reconfiguration changes the number of buildings, grade bands, and potentially the number of tiers needed. Option A (2 primary + 2 intermediate) may require different tier coordination than Option B (4 K-4) or Variant C (3 Pre-K-2 + 1 Grades 3-4). The feasibility and constraints of bell schedule tiers under each configuration haven't been analyzed.

## Desired Outcomes

For each configuration, an assessment of how many bus tiers are needed, whether the current fleet can cover them, and what constraints emerge (minimum gap between tiers, impact on before/after school time for families).

## External Behavior

**Inputs:**
- Current bell schedule data (SPEC-055)
- Number of buildings per grade band under each configuration
- Standard bus turnaround time assumptions (15-30 minutes between tiers)

**Outputs:**
- `docs/analysis/bell-schedule-analysis.md`
- Tier requirement table: configuration, number_of_buildings, tiers_required, earliest_start, latest_end, tier_gap_minutes
- Feasibility assessment: can the current fleet pattern (assumed from current tier count) cover each configuration?

**Constraints:**
- This is a constraint satisfaction analysis, not an optimization
- Standard assumptions: buses need 15-30 minutes between tiers for route completion; maximum 3 tiers is typical for similar districts
- Note that the middle school bell time consolidation was deferred due to DOT traffic study requirements — reference this as context

## Acceptance Criteria

- Given three configurations and current bell schedule data, when tiers are analyzed, then each configuration's tier requirement is stated
- Given tier requirements, when compared to current fleet pattern, then the feasibility of each configuration is assessed
- Given family impact, when earliest start and latest end times are calculated, then the total school-day window for each configuration is documented

## Scope & Constraints

**In scope:** Tier feasibility analysis for 3 configurations.
**Out of scope:** Bell schedule optimization. DOT traffic study requirements. Middle school schedule (separate issue).

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-031 |
