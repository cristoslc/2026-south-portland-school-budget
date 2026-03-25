---
title: "Answer Detail Pages"
artifact: SPEC-027
type: feature
status: Active
author: cristos
created: 2026-03-25
last-updated: 2026-03-25
parent-epic: EPIC-017
parent-initiative: INITIATIVE-004
priority-weight: high
acceptance-criteria:
  - Each question has a detail page at /questions/<slug>/
  - Detail page shows the question, sourced answer with context, and evidence citations
  - Evidence citations link to the sources page or primary source URLs
  - Related questions are shown for cross-navigation
  - Back link returns to the questions index
depends-on-artifacts:
  - SPEC-025
  - SPEC-026
  - SPEC-033
addresses: []
---

# Answer Detail Pages

## Problem Statement

The questions index (SPEC-026) shows what people are asking, but the answer — with sourced evidence and context — needs its own page. This is where the site delivers its core value: a clear answer to a specific budget question, backed by citations to meeting transcripts, slides, and documents.

## External Behavior

- **Route:** `/questions/<slug>/`
- **Data source:** `dist/questions.json` (SPEC-025)
- **Layout:** Single question detail with answer, evidence, and related questions

### Page Structure

```
← Back to Questions

Which school is formally closing?
[Category badge: School Closures & Reconfiguration]

Answer context paragraph explaining what's known, with nuance
about what's confirmed vs. implied.

Sources
├── Budget Workshop 2026-03-23 — "Kaler at zero allocation"
├── Board Meeting Packet — "FY27 staffing shows no Kaler positions"
└── ...

Asked by: Concerned Parent, Tax-Conscious Resident, ...

Related Questions
├── "What grade configuration was chosen?"
└── "What happens to students at the closing school?"
```

## Acceptance Criteria

1. Given a question slug, when the page loads, then it displays the canonical question, category, answer context, and evidence citations
2. Given evidence entries, when rendered, then each links to the corresponding source on the evidence page (SPEC-033) or to the primary source URL
3. Given a question asked by multiple personas, when rendered, then persona names (not IDs) are shown as "Asked by" with links to persona pages
4. Given other questions in the same category, when rendered, then up to 3 related questions are shown with links
5. Given the page, when navigated to, then a back link returns to `/questions/`

## Scope & Constraints

- Static generation — one page per question, generated at build time
- Answer context comes from the extraction JSON (SPEC-025), not generated at page render time
- Persona names resolved from persona artifact titles
- Related questions = same category, excluding current question

## Implementation Approach

1. **Dynamic route** — `site/src/pages/questions/[slug].astro` with `getStaticPaths()` from questions JSON
2. **Answer section** — render context paragraph with proper typography
3. **Evidence citations** — list with links to evidence page sections or primary URLs
4. **Persona attribution** — "Asked by" section resolving PERSONA-NNN to display names
5. **Related questions** — filter same-category questions, show top 3 as cards
6. **Back navigation** — consistent with existing back-link pattern

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-25 | — | Created from EPIC-017 decomposition |
