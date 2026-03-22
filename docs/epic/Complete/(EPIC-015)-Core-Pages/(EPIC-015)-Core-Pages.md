---
title: "Core Pages"
artifact: EPIC-015
track: container
status: Complete
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
parent-vision: VISION-004
parent-initiative: INITIATIVE-004
priority-weight: high
success-criteria:
  - Landing page with budget stats, briefing cards, persona cards, and timeline
  - Individual briefing pages rendering full markdown content
  - Persona profile pages with cross-links to briefings
  - Evidence page with budget tables and pipeline explanation
  - Timeline page with full budget season calendar
  - About page with methodology, limitations, and verification links
depends-on-artifacts:
  - EPIC-014
addresses: []
evidence-pool: ""
---

# Core Pages

## Goal / Objective

Build the six core page types that present the budget analysis to residents: landing, briefings (index + individual), personas (index + individual), evidence, timeline, and about.

## Desired Outcomes

Residents can navigate from the landing page to any briefing, persona, or evidence summary within two clicks. Each briefing renders its full content with proper formatting. Persona profiles link to their corresponding briefings.

## Scope Boundaries

**In scope:** All page layouts and templates, card grids, navigation, footer, content rendering via Astro's `render()` API.

**Out of scope:** Question hub (EPIC-017), feedback system (EPIC-018), visual polish beyond functional layout (EPIC-016).

## Child Specs

Work was done directly — 36 pages total across 6 templates.

| Artifact | Title | Status |
|----------|-------|--------|
| — | Landing page (hero, stats, cards, timeline preview) | Complete (commit cd1f1a4) |
| — | Briefings index + 16 individual briefing pages | Complete (commit cd1f1a4) |
| — | Personas index + 14 individual persona pages | Complete (commit cd1f1a4) |
| — | Evidence page with budget tables | Complete (commit cd1f1a4) |
| — | Timeline page | Complete (commit cd1f1a4) |
| — | About page (methodology, limitations) | Complete (commit cd1f1a4) |
| — | Persona title display (description over first name) | Complete (commit 5da585e) |

## Key Dependencies

- EPIC-014 (scaffolding must exist first)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | cd1f1a4 | Created and shipped in single session |
| Complete | 2026-03-22 | 5da585e | All 36 pages building, persona titles fixed |
