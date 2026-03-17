---
title: "Budget Lever Analysis"
artifact: INITIATIVE-001
track: container
status: Active
author: cristos
created: 2026-03-16
last-updated: 2026-03-16
parent-vision: VISION-001
success-criteria:
  - Budget levers extracted with dollar amounts and evidence links
  - Tax rate calculation model computes mil rate impact from lever combinations
  - Structured data outputs consumable by downstream presentation layers (VISION-004)
depends-on-artifacts: []
addresses:
  - JOURNEY-002.PP-03
  - JOURNEY-002.PP-05
  - JOURNEY-001.PP-03
  - JOURNEY-004.PP-01
  - JOURNEY-003.PP-01
trove: ""
linked-epics:
  - EPIC-007
linked-artifacts:
  - VISION-004
---

# Budget Lever Analysis

## Strategic Focus

Extract the discrete decision points ("levers") from the FY27 budget — staffing changes, program additions/cuts, capital projects, revenue adjustments, reconfiguration savings — and quantify each lever's impact as structured data. This is the analytical core of VISION-001: turning opaque budget documents into queryable, evidence-linked decision models that any downstream presentation layer can consume.

## Scope Boundaries

**In scope:** Lever extraction, categorization, quantification with source citations, baseline budget model, tax rate calculation, structured data output (JSON/YAML).

**Out of scope:** Interactive UI or dashboard (owned by VISION-004), advocacy for specific outcomes, multi-year forecasting.

## Child Epics

| Artifact | Title | Status |
|----------|-------|--------|
| EPIC-007 | Budget Lever Analysis | Proposed |

## Small Work (Epic-less Specs)

_None currently._

## Key Dependencies

- Evidence pools: `school-board-budget-meetings`, `fy27-budget-documents`, `city-council-meetings-2026`
- Assessed valuation and mil rate data from city tax records

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-16 | — | Created during initiative migration |
