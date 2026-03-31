---
title: "Enrollment Baseline Site Page"
artifact: SPEC-068
track: implementable
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
type: feature
parent-epic: EPIC-029
linked-artifacts:
  - INITIATIVE-005
  - INITIATIVE-004
  - SPEC-058
  - SPEC-059
depends-on-artifacts:
  - SPEC-058
  - SPEC-059
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Enrollment Baseline Site Page

## Problem Statement

The independent enrollment projection needs a permanent home on the site — not just embedded in persona briefs, but as a standalone reference page that anyone can access, inspect, and return to as new enrollment data arrives each fall.

## Desired Outcomes

A public, permanent enrollment baseline page on the site that presents the independent projection, scenario brackets, methodology, assumptions, and testable predictions. Designed for longitudinal use — visitors can return each October when new enrollment data is published and compare actual vs. projected.

## External Behavior

**Inputs:**
- Cohort survival model output (SPEC-058)
- Scenario bracket projections (SPEC-059)
- Methodology document from SPEC-058

**Outputs:**
- Astro page at `site/src/pages/enrollment/index.astro` (or similar)
- Content sections: historical enrollment chart, 5-year projection with scenario brackets, methodology summary, assumptions table, testable predictions, data sources, limitations
- Structured data for charts (the site already uses Astro; chart rendering approach TBD — could be static SVG, Mermaid, or a lightweight JS chart library)

**Constraints:**
- Must follow existing site design system (DESIGN-001: 18px base font, WCAG AA contrast, dark mode support, research banner)
- Must include the project's standard disclaimer (independent analysis, not affiliated with district)
- Must be maintainable — when FY28 enrollment data arrives, updating the page should be straightforward
- Must include a "last updated" date and link to the methodology document

## Acceptance Criteria

- Given the projection data, when the page is deployed, then historical enrollment and 5-year projections are visible with scenario brackets
- Given the methodology section, when read, then assumptions are stated clearly enough for a non-expert to evaluate
- Given testable predictions, when displayed, then each prediction has a concrete threshold and target date
- Given the existing site design, when the page is rendered, then it follows DESIGN-001 standards

## Scope & Constraints

**In scope:** Site page creation, data visualization, methodology presentation.
**Out of scope:** Interactive tools (scenario sliders, etc.). Transportation comparison page (separate spec under INITIATIVE-006 if needed).

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-029 |
