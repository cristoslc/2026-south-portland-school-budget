---
title: "Analysis Section Site Restructure"
artifact: SPEC-090
track: implementable
status: Active
author: cristos
created: 2026-04-05
last-updated: 2026-04-05
priority-weight: ""
type: feature
parent-epic: EPIC-036
parent-initiative: ""
linked-artifacts:
  - SPEC-070
depends-on-artifacts:
  - SPEC-089
addresses: []
evidence-pool: "school-integration-policy"
source-issue: ""
swain-do: required
---

# Analysis Section Site Restructure

## Problem Statement

The site nav has a "Transportation" entry that implies only one analytical lens exists beyond budget briefings. A second analysis track — reconfiguration context — needs to sit alongside it. The nav, the landing page, and the homepage all need restructuring to present both tracks as peers.

## Desired Outcomes

Residents see "Analysis" in the nav and find two tracks: the existing transportation analysis and a new reconfiguration context page. The homepage presents both analysis tracks alongside the general briefings as entry points of equal weight. The reconfiguration context page tells the 2024 process story, bridges national research, and includes a collapsible accountability checklist.

## External Behavior

**Navigation:**
- "Transportation" nav item becomes "Analysis"
- `/analysis/` landing page indexes two tracks as cards:
  - Transportation Analysis (links to existing `/transportation-analysis/`)
  - Reconfiguration Context (links to `/analysis/reconfiguration-context/`)

**New page — `/analysis/reconfiguration-context/`:**
Three-part content flow:
1. **The 2024 process** — full narrative of the Boundaries & Configurations review sourced from the expanded trove. Who was involved, what the community said, what the steering committee recommended, how the Board deliberated, what they decided in May 2024.
2. **Research bridge** — TCF nine-districts findings on voluntary integration. Where South Portland's 2024 directives align with best practice. Where they do not yet reach. Presented as context, not judgment.
3. **Accountability checklist (collapsible)** — May 2024 Board action items with delivery status (Delivered / Not yet delivered / Unknown). Factual only. Rendered as a collapsible element.

Source attribution footer consistent with site conventions.

**Homepage:**
- Top section becomes "Briefings & Analysis" with a 4-card grid:
  - General Budget Briefing
  - Upcoming Meeting Briefing
  - Transportation Analysis
  - Reconfiguration Context
- The standalone "Transportation Analysis" section lower on the page is removed
- Budget Community Lenses and Transportation Community Lenses sections remain unchanged

**Content loading:**
- New Astro content collection or loader for reconfiguration context markdown (sourced from the trove's expanded synthesis or a dedicated `dist/` output)
- Collapsible component for the accountability checklist (HTML details/summary or equivalent)

## Acceptance Criteria

- AC-1: Given a user clicks "Analysis" in the nav, when the landing page loads, then it shows cards for both Transportation Analysis and Reconfiguration Context.
- AC-2: Given a user navigates to `/analysis/reconfiguration-context/`, when the page loads, then it displays the process narrative, research bridge, and collapsible accountability checklist.
- AC-3: Given the homepage loads, when the user sees the top card grid, then it shows 4 peer cards (2 general briefings + 2 analysis tracks).
- AC-4: Given the accountability checklist, when first rendered, then it is collapsed by default.
- AC-5: Given any text on the reconfiguration context page, when reviewed for tone, then no adversarial or editorializing language is present.
- AC-6: Given the existing transportation analysis pages, when the nav restructure is complete, then all existing `/transportation-analysis/` URLs still work and content is unchanged.

## Scope & Constraints

**In scope:** Nav rename, Analysis landing page, reconfiguration context page, homepage 4-card grid, removal of standalone Transportation Analysis homepage section.

**Out of scope:** Trove expansion (SPEC-089). Briefing regeneration (SPEC-091). New community-lens briefings for the reconfiguration track. Changes to transportation analysis content.

**Constraint:** No adversarial framing. The accountability checklist presents facts — it does not editorialize about what gaps mean.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-04-05 | — | Created as EPIC-036 child spec (Phase 2) |
