---
title: "Site Visual Design"
artifact: EPIC-016
track: container
status: Active
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
parent-vision: VISION-004
parent-initiative: INITIATIVE-004
priority-weight: medium
success-criteria:
  - WCAG AA contrast ratios across all color pairings in both themes
  - Dark mode visually distinct and fully functional
  - Interaction delight (hover states, animations) present but not distracting
  - Mobile responsive down to 320px width
  - Research project banner visible on all pages
  - Base font size >= 18px for senior readability
depends-on-artifacts:
  - EPIC-015
  - DESIGN-001
addresses: []
evidence-pool: ""
---

# Site Visual Design

## Goal / Objective

Polish the site's visual presentation, accessibility, and interaction design to be production-quality for a civic audience including senior citizens.

## Desired Outcomes

The site feels trustworthy and professional — not flashy, not generic. Senior residents can read it comfortably. Dark mode users see a fully functional, visually distinct experience. The research banner is unmissable.

## Scope Boundaries

**In scope:** CSS system, color variables, dark mode, typography scale, responsive breakpoints, micro-animations, theme toggle, research banner, card hover states.

**Out of scope:** Content changes, new page types, question hub UI.

## Child Specs

| Artifact | Title | Status |
|----------|-------|--------|
| SPEC-025 | Dark mode color system | _to be created_ |
| SPEC-026 | Interaction delight pass | _to be created_ |
| — | 18px base font + responsive scaling | Complete (commit c2103e0) |
| — | Research project banner | Complete (commit 7293ca7) |
| — | Card hover fix (link cascade) | Complete (commit c2103e0) |

## Key Dependencies

- DESIGN-001 (accessibility standards)
- EPIC-015 (pages must exist to style)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | 248620e | Core visual work done; refinements ongoing |
