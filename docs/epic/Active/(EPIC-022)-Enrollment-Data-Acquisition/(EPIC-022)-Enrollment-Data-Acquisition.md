---
title: "Enrollment Data Acquisition"
artifact: EPIC-022
track: container
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
parent-vision: VISION-001
parent-initiative: INITIATIVE-005
priority-weight: high
success-criteria:
  - Maine DOE grade-level enrollment history (10+ years, K-12) collected and normalized in a swain-search trove
  - Every enrollment claim and assumption in existing evidence pools (budget documents, board presentations) cataloged with source citations
  - DHHS municipal birth records collected for South Portland (10+ years)
  - City housing permit data collected (recent years, sufficient for LD 1829 absorption modeling)
  - School choice transfer flow data collected or gap documented with rationale
  - All acquired data structured for consumption by downstream EPICs (gap analysis, cohort survival model)
depends-on-artifacts: []
addresses:
  - JOURNEY-002.PP-03
  - JOURNEY-001.PP-03
evidence-pool: ""
---

# Enrollment Data Acquisition

## Goal / Objective

Collect, normalize, and catalog the demographic and enrollment data required for independent enrollment analysis. This is the foundation for both Track 1 (gap exposure) and Track 2 (independent projections) — no downstream EPIC can begin without this data.

## Desired Outcomes

Maria, Tom, Linda, and Priya gain access to the raw evidence base that the district has not published. Researchers and journalists can independently verify enrollment claims. The project has a structured, citable data foundation that outlasts any single analysis.

## Scope Boundaries

**In scope:**
- Maine DOE grade-level enrollment history (K-12, 10+ years) via public data portals
- District enrollment claims extraction from existing evidence pools (fy27-budget-documents, school-board-budget-meetings)
- DHHS vital records (municipal birth data for South Portland)
- City of South Portland housing permit data (for LD 1829 absorption modeling)
- School choice transfer flow data (if publicly available)
- Data normalization into structured formats (CSV/JSON) within swain-search troves
- Building-level data feasibility investigation (SPIKE)

**Out of scope:**
- Infinite Campus (district SIS) data — no access
- Analysis or interpretation of the data (that's EPIC-023 and EPIC-024)
- Data from other municipalities (South Portland only unless comparison is needed for cohort survival)

## Child Specs

| Artifact | Title | Status |
|----------|-------|--------|
| SPEC-039 | Maine DOE Enrollment Data Collection | Proposed |
| SPEC-040 | District Enrollment Claims Catalog | Proposed |
| SPEC-041 | Supplementary Demographic Data Collection | Proposed |
| SPIKE-009 | Building-Level Data Feasibility | Proposed |

## Key Dependencies

- **Evidence pools (existing):** fy27-budget-documents, school-board-budget-meetings, city-council-meetings-2026
- **Data sources (external):** Maine DOE public data portal, DHHS vital records, City of South Portland planning/permits
- **Infrastructure:** swain-search trove collection pipeline

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-30 | — | Decomposed from INITIATIVE-005 |
| Active | 2026-03-30 | -- | Operator approved; decomposing into child SPECs |
