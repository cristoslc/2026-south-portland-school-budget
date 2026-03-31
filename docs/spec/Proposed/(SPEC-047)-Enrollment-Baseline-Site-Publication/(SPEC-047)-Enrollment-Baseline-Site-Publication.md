---
title: "Enrollment Baseline Site Publication"
artifact: SPEC-047
track: implementable
status: Proposed
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
priority-weight: medium
type: ""
parent-epic: EPIC-025
linked-artifacts:
  - INITIATIVE-004
depends-on-artifacts:
  - SPEC-045
  - SPEC-046
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Enrollment Baseline Site Publication

## Problem Statement

The independent enrollment projections and persona briefs need a permanent, publicly accessible home. The project site (INITIATIVE-004) is the natural venue, but enrollment data requires specialized presentation: interactive scenario comparison, methodology transparency, and downloadable data for researchers and journalists.

## Desired Outcomes

The site becomes the canonical location for independent South Portland enrollment data. Residents can explore scenario projections interactively. Researchers and journalists can download structured data. The methodology is transparent and inspectable. As new enrollment data arrives each fall, the baseline remains available for comparison.

## External Behavior

**Inputs:**
- Scenario bracket data from SPEC-045 (JSON/CSV)
- Phase 2 persona briefs from SPEC-046
- Methodology documentation from SPEC-044
- Site infrastructure from INITIATIVE-004

**Outputs:**
- Enrollment projections page on the site with:
  - Interactive scenario comparison (chart showing baseline + brackets over 5-year horizon)
  - Scenario assumption descriptions (what each scenario assumes and why)
  - Grade-level detail view (drill into per-grade projections)
- Methodology page explaining the cohort survival approach, data sources, and limitations
- Data download section: CSV/JSON exports of all projection data
- Phase 2 persona briefs integrated into existing persona pages
- Known limitations prominently displayed

**Constraints:**
- Must integrate with existing Astro site architecture (INITIATIVE-004)
- Charts must work without JavaScript frameworks beyond what the site already uses
- Data downloads must be structured identically to the model outputs (no lossy transformation)
- Methodology page must be understandable by an informed non-specialist

## Acceptance Criteria

1. Given the enrollment page, when a user visits, then they see a scenario comparison chart with at least 3 scenarios over 5 years
2. Given the scenario chart, when a user selects a scenario, then the assumptions behind it are displayed
3. Given the methodology page, when read by a non-specialist, then the cohort survival approach is explained with data sources and limitations
4. Given the data download section, when a researcher downloads CSV, then it matches the model's structured output schema exactly
5. Given the persona pages, when visited, then Phase 2 briefs appear alongside existing content
6. Given the known limitations, when displayed, then they are prominent (not buried in footnotes)

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

- Builds on existing Astro site — no new framework or architecture
- Interactive charts should be lightweight (Chart.js or similar, not D3 unless already in use)
- Enrollment page is a new section, not a replacement for existing content
- Mobile-responsive required
- Accessibility: charts must have tabular data alternatives

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-30 | — | Decomposed from EPIC-025 |
