---
title: "Reconfiguration Context Analysis Track"
artifact: EPIC-036
track: container
status: Active
author: cristos
created: 2026-04-05
last-updated: 2026-04-05
parent-vision: ""
parent-initiative: INITIATIVE-004
priority-weight: high
success-criteria:
  - The site has an Analysis section with Transportation and Reconfiguration Context tracks
  - The school-integration-policy trove contains at least 4 primary sources on the 2024 process
  - The reconfiguration context page tells the full 2024 story with research bridge and accountability checklist
  - Homepage presents both analysis tracks as peers alongside general briefings
  - Briefings that trigger 2024 keywords include historical context via SPEC-081
depends-on-artifacts:
  - SPEC-070
  - SPEC-081
addresses: []
evidence-pool: "school-integration-policy"
---

# Reconfiguration Context Analysis Track

## Goal / Objective

Add a second analysis track to the site that tells the story of South Portland's 2024 Boundaries and Configurations process — community engagement, steering committee work, board deliberations, and the May 2024 action items — alongside national research on what works for voluntary school integration. This gives residents the historical context missing from the current site, which presents reconfiguration as if it started in 2025.

## Desired Outcomes

Residents can trace the current reconfiguration back to the year-long process that preceded it. The 2024 community engagement findings, board directives, and national research are accessible in one place. An accountability checklist tracks delivery status of the May 2024 action items without editorializing. The pipeline surfaces this context in persona briefings where relevant topics arise — not as a bolted-on section, but as natural reference material drawn in by keyword triggers.

## Progress

<!-- Auto-populated from session digests. See progress.md for full log. -->

## Scope Boundaries

**In scope:**
- Trove expansion with 2024 process sources (board minutes, community engagement, steering committee)
- Nav restructure: "Transportation" becomes "Analysis" with two tracks
- New reconfiguration context page (process narrative, research bridge, collapsible accountability checklist)
- Homepage layout update: 4-card "Briefings & Analysis" grid
- Two-pass briefing regeneration via [SPEC-081](../../../spec/Active/(SPEC-081)-Keyword-Triggered-Reference-Context/(SPEC-081)-Keyword-Triggered-Reference-Context.md)

**Out of scope:**
- Community-lens briefings for the reconfiguration track (future work)
- Inter-district analysis (Hartford/Louisville style)
- Changes to existing transportation analysis pages or content
- Consultant report content if not publicly available (document the gap)

## Child Specs

| Spec | Title | Phase | Status |
|------|-------|-------|--------|
| SPEC-089 | School Integration Trove Expansion | Phase 1 | Active |
| SPEC-090 | Analysis Section Site Restructure | Phase 2 | Active |
| SPEC-091 | Reconfiguration Briefing Integration | Phase 3 | Active |

**Dependency:** SPEC-089 (trove expansion) must complete before SPEC-090 and SPEC-091 can begin implementation. SPEC-090 and SPEC-091 can proceed in parallel after SPEC-089.

## Key Dependencies

- [SPEC-070](../../../spec/Active/(SPEC-070)-Transportation-Analysis-Site-Pages/(SPEC-070)-Transportation-Analysis-Site-Pages.md) — established the transportation analysis site section that this epic extends into a shared Analysis nav
- [SPEC-081](../../../spec/Active/(SPEC-081)-Keyword-Triggered-Reference-Context/(SPEC-081)-Keyword-Triggered-Reference-Context.md) — provides the keyword-triggered reference context injection that SPEC-091 relies on
- `school-integration-policy` trove — the evidence base for the reconfiguration context page

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-04-05 | — | Promoted from SPEC-088; decomposed into 3 child specs |
