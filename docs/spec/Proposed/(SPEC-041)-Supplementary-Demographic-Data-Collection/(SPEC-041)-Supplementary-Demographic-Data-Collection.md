---
title: "Supplementary Demographic Data Collection"
artifact: SPEC-041
track: implementable
status: Proposed
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
priority-weight: medium
type: ""
parent-epic: EPIC-022
linked-artifacts:
  - EPIC-024
depends-on-artifacts:
  - SPEC-039
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Supplementary Demographic Data Collection

## Problem Statement

The cohort survival model (EPIC-024) requires demographic inputs beyond enrollment history: municipal birth records (to project the kindergarten pipeline), housing permit data (to model LD 1829 density absorption), and school choice transfer flows (to calibrate inter-district movement). These datasets are scattered across state and municipal agencies with varying accessibility.

## Desired Outcomes

The project has the supplementary demographic datasets needed to power scenario brackets in the cohort survival model. Each dataset is documented with its source, limitations, and coverage gaps. Where data is unavailable, the gap is documented with rationale so the model can explicitly flag which scenarios rest on weaker foundations.

## External Behavior

**Inputs:**
- DHHS vital records portal (municipal birth data)
- City of South Portland planning/permitting records
- Maine DOE or district-level school choice transfer data (if publicly available)

**Outputs:**
- swain-search trove: DHHS birth records for South Portland (10+ years, annual births by municipality)
- swain-search trove: city housing permit data (recent years, residential units permitted)
- swain-search trove or documented gap: school choice transfer flows (in/out by grade level if available)
- Source citation metadata for each dataset
- Data gap report: for each target dataset, what was available, what wasn't, and implications for modeling

**Constraints:**
- All data from official government sources
- Document access method (public portal, FOAA request, etc.)
- If a dataset requires FOAA and turnaround exceeds the project timeline, document the gap and model without it

## Acceptance Criteria

1. Given the birth records trove, when queried for South Portland births by year, then at least 10 years of annual birth counts are available
2. Given the housing permit trove, when queried, then residential unit permit counts for recent years are available with source citations
3. Given the school choice data, when investigated, then either transfer flow data is collected OR a documented gap explains why it's unavailable and how the model compensates
4. Given all troves, when consumed by the cohort survival model (EPIC-024), then each dataset is parseable as structured data
5. Given the data gap report, when reviewed, then every target dataset has an entry documenting availability, source, and limitations

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

- South Portland municipality only for birth and housing data
- School choice data scope: South Portland as sending or receiving district
- This spec collects and structures data — it does not analyze or model it (that's EPIC-024)
- FOAA-dependent data sources may not be available within project timeline — document gaps, don't block
- Priority order: birth records (essential for kindergarten pipeline) > housing permits (essential for LD 1829 scenario) > school choice (calibration, not gating)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-30 | — | Decomposed from EPIC-022 |
