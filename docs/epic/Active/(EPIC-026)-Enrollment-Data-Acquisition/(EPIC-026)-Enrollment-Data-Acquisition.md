---
title: "Enrollment Data Acquisition"
artifact: EPIC-026
track: container
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
parent-vision: VISION-001
parent-initiative: INITIATIVE-005
priority-weight: high
success-criteria:
  - Maine DOE grade-level enrollment data for South Portland acquired (10+ years)
  - DHHS municipal birth records for South Portland acquired
  - City housing permit data acquired
  - School choice transfer flow data acquired or gap documented
  - Every enrollment claim and assumption from existing evidence pools extracted and cataloged with source citations
depends-on-artifacts: []
addresses: []
evidence-pool: ""
---

# Enrollment Data Acquisition

## Goal / Objective

Acquire and normalize the external data sources required for independent enrollment analysis, and systematically extract every enrollment-related claim and assumption from the project's existing evidence pools. This epic produces the dataset that EPIC-027 (gap analysis), EPIC-028 (cohort survival model), and EPIC-029 (Phase 2 briefs) all consume.

## Desired Outcomes

The project has a complete, structured enrollment dataset drawn from authoritative public sources — not dependent on district cooperation. Every enrollment assumption embedded in the administration's closure recommendation is identified and cataloged, ready for gap analysis. Data acquisition uses the established swain-search → trove → synthesis pipeline.

## Scope Boundaries

**In scope:**
- Trove collection via swain-search: Maine DOE grade-level enrollment by district (10+ year history), DHHS vital statistics (births by municipality), city of South Portland housing permits, school choice transfer data (Maine DOE or district-published)
- Extraction and cataloging of enrollment claims from existing evidence pools (fy27-budget-documents, school-board-budget-meetings, city-council-meetings-2026)
- Normalization to structured data formats consumable by downstream epics
- [SPIKE-009](../../research/Active/(SPIKE-009)-Building-Level-Data-Feasibility/(SPIKE-009)-Building-Level-Data-Feasibility.md): feasibility assessment for building-level data

**Out of scope:**
- Modeling or analysis (EPIC-028)
- Brief generation (EPIC-027, EPIC-029)
- Data requiring FERPA-protected access

## Child Specs

_To be decomposed during implementation planning._

## Key Dependencies

- Existing evidence pools (already collected)
- Maine DOE public data portal
- Maine DHHS vital statistics
- City of South Portland planning office

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of INITIATIVE-005; user-approved |
