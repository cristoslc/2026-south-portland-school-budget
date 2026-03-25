---
title: "Questions Index Page"
artifact: SPEC-026
type: feature
status: Active
author: cristos
created: 2026-03-25
last-updated: 2026-03-25
parent-epic: EPIC-017
parent-initiative: INITIATIVE-004
priority-weight: high
acceptance-criteria:
  - /questions/ page renders categorized list of budget questions
  - Questions are grouped by topic category, not by persona
  - Each question card links to its answer detail page
  - Category counts are visible
  - Page is linked from site navigation
depends-on-artifacts:
  - SPEC-025
  - EPIC-015
addresses: []
---

# Questions Index Page

## Problem Statement

Residents arriving at the site with a specific concern need a browsable index of questions organized by topic. The existing site has briefings (organized by date and persona) and evidence (organized by source), but no question-first entry point. This page is the front door of the Question Hub.

## External Behavior

- **Route:** `/questions/`
- **Data source:** `dist/questions.json` (produced by SPEC-025)
- **Layout:** Categorized card grid — one section per topic category, each containing question cards that link to answer detail pages

### Page Structure

```
Questions People Are Asking
├── School Closures & Reconfiguration (N questions)
│   ├── "Which school is formally closing?" →
│   └── "What grade configuration was chosen?" →
├── Staffing & Positions (N questions)
│   ├── "How many positions are being cut?" →
│   └── ...
├── Tax Impact (N questions)
└── ...
```

## Acceptance Criteria

1. Given `dist/questions.json` with categorized questions, when the page renders, then questions are grouped under category headings with counts
2. Given a question card, when clicked, then it navigates to `/questions/<slug>/` for the answer detail
3. Given the site navigation, when viewing any page, then "Questions" appears in the header nav between existing items
4. Given the page on mobile, when viewed, then the layout is responsive and readable
5. Given the site's design system, when the page renders, then it uses existing card grid, badge, and typography patterns from BaseLayout and other pages

## Scope & Constraints

- Static generation — questions are loaded at build time from the JSON file
- No search or filtering beyond category grouping (keep it simple for v1)
- Follows existing Astro page patterns (BaseLayout, .card-grid, .reveal)

## Implementation Approach

1. **Create page** — `site/src/pages/questions/index.astro` loading `dist/questions.json`
2. **Group by category** — render sections with category headings and question counts
3. **Question cards** — card per question showing the question text, category badge, and persona count
4. **Navigation** — add "Questions" link to BaseLayout header nav
5. **Styling** — reuse existing card-grid and badge patterns

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-25 | — | Created from EPIC-017 decomposition |
