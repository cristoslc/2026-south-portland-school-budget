---
title: "Budget Lever Analysis"
artifact: EPIC-007
status: Proposed
author: cristos
created: 2026-03-11
last-updated: 2026-03-16
parent-vision: VISION-001
parent-initiative: INITIATIVE-001
success-criteria:
  - Budget levers identified and catalogued with dollar amounts and sources
  - Each lever linked to evidence (meeting transcript, slide deck, or budget document)
  - Baseline budget model reflects the current proposed budget
  - Tax rate calculation model computes mil rate impact from lever combinations
  - At least one alternative budget scenario fully costed via lever combinations
  - Analysis outputs are structured data consumable by downstream presentation layers
depends-on: []
addresses:
  - JOURNEY-002.PP-03
  - JOURNEY-002.PP-05
  - JOURNEY-001.PP-03
  - JOURNEY-004.PP-01
  - JOURNEY-003.PP-01
evidence-pool: ""
---

# Budget Lever Analysis

## Goal / Objective

Extract the discrete decision points ("levers") from the FY27 budget evidence — staffing changes, program additions/cuts, capital projects, revenue adjustments, reconfiguration savings — and build structured data models that quantify each lever's impact on the tax rate and budget deficit/surplus.

This is the core analysis deliverable of VISION-001: turning opaque budget documents into structured, queryable data. The interactive presentation of this analysis (dashboard UI, "what-if" tools) is owned by VISION-004's static site.

## Scope Boundaries

**In scope:**

- Systematic extraction of levers from all three evidence pools (school board meetings, budget documents, city council meetings)
- Categorization of levers (expenditure vs. revenue, recurring vs. one-time, discretionary vs. mandated)
- Dollar-amount quantification of each lever with source citations
- Baseline budget model (proposed FY27 budget as-is)
- Tax rate calculation model (assessed valuation, mil rate, state revenue sharing)
- Structured data output (JSON/YAML) consumable by downstream presentation layers
- At least one pre-built "what-if" scenario (e.g., no-closure alternative)

**Out of scope:**

- Advocacy for or against specific lever combinations
- Multi-year forecasting beyond FY27
- Full municipal budget (city side) — school department only
- **Interactive dashboard UI** — presentation of lever analysis is owned by VISION-004 (static site)
- Native mobile app

## Child Specs

_To be created. Expected decomposition:_

- Lever extraction and cataloguing (research/analysis spec)
- Budget baseline model (data spec — the numbers behind the dashboard)
- Tax rate calculation engine (computation spec)

## Key Dependencies

- Evidence pools: `school-board-budget-meetings`, `fy27-budget-documents`, `city-council-meetings-2026` — all currently populated and refreshed
- Assessed valuation and mil rate data from city tax records (may need to be sourced)
- State education subsidy figures for South Portland (EPS allocation)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-11 | 0664840 | Initial creation |
