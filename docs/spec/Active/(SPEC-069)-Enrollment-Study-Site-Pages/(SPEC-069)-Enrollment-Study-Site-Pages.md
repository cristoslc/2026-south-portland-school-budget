---
title: "Enrollment Study Site Pages"
artifact: SPEC-069
track: implementable
status: Active
author: cristos
created: 2026-03-31
last-updated: 2026-03-31
type: feature
parent-epic: EPIC-019
linked-artifacts:
  - INITIATIVE-004
  - INITIATIVE-005
depends-on-artifacts:
  - EPIC-014
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Enrollment Study Site Pages

## Problem Statement

The enrollment study deliverables (persona briefings, enrollment data) now live in `dist/enrollment-study/` with their own README and METHODOLOGY. The Astro site's `briefings` content collection still points at the old `dist/briefings/` path, and there are no dedicated pages for the enrollment study as a coherent initiative. Visitors should be able to find the enrollment study as a self-contained section with its own landing page, methodology explanation, and briefing index.

## Desired Outcomes

The site has an `/enrollment-study` section that presents [INITIATIVE-005](../../initiative/Active/(INITIATIVE-005)-Independent-Enrollment-Study/(INITIATIVE-005)-Independent-Enrollment-Study.md) deliverables as a cohesive body of work — not just individual briefings scattered in a flat list.

## External Behavior

**Content collection changes:**
- Update `site/src/content.config.ts` to load enrollment briefings from `../dist/enrollment-study/briefings/` instead of the old `../dist/briefings/` path
- Add schema fields for any new frontmatter in enrollment briefings (if needed)

**New pages:**
- `/enrollment-study` — Landing page rendering `dist/enrollment-study/README.md` content. Links to methodology, individual briefings, and data sources.
- `/enrollment-study/methodology` — Renders `dist/enrollment-study/METHODOLOGY.md`
- `/enrollment-study/briefings` — Index of all enrollment study persona briefings with persona name, audience description, and link
- `/enrollment-study/briefings/[slug]` — Individual briefing pages (reuse existing briefing layout)

**Navigation:**
- Add "Enrollment Study" to the site's main navigation
- Cross-link from persona pages to their enrollment study briefing
- Cross-link from the main briefings index (if retained) to the initiative-specific section

**Data files:**
- Make `nces-enrollment-by-grade.csv` and `.json` available as downloadable files or rendered as a table on the landing page

## Acceptance Criteria

- Given the updated content collection config, when the site builds, then enrollment briefings load from `dist/enrollment-study/briefings/`
- Given the `/enrollment-study` landing page, when a visitor arrives, then they see the initiative overview, key findings, and links to all deliverables
- Given the methodology page, when a visitor reads it, then all assumptions and data sources are documented
- Given the briefing index, when a visitor browses, then each persona's enrollment briefing is listed and linked
- Given the old `dist/briefings/` path no longer exists, when the site builds, then there are no broken collection references

## Scope & Constraints

**In scope:** Content collection update, new pages, navigation integration.
**Out of scope:** Generating new briefings (INITIATIVE-005 handles that). Visual design beyond existing site patterns. New Astro components (reuse existing layouts).

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-31 | — | User-requested; site integration for INITIATIVE-005 deliverables |
