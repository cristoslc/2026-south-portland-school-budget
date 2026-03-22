---
title: "Last Updated Indicator"
artifact: SPEC-032
type: feature
status: Proposed
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
parent-epic: EPIC-015
parent-initiative: ""
priority-weight: low
acceptance-criteria:
  - Site-level "last updated" timestamp visible on landing page
  - Individual briefings show when they were last regenerated
  - Repeat visitors can quickly see if anything changed since their last visit
depends-on-artifacts:
  - EPIC-015
addresses: []
---

# Last Updated Indicator

## Problem

Repeat visitors (especially Linda, the School Board Insider) bookmark the site and check back regularly. There's no way to see at a glance whether anything changed since their last visit. Individual briefings show a generated_date but there's no site-level freshness indicator.

## Proposed Solution

Add a "Last updated: YYYY-MM-DD" line to the landing page hero or below the research banner, derived from the most recent briefing generated_date. Optionally, highlight briefings that changed since a configurable date (via URL param or localStorage).

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-22 | — | From persona-lens design review (Linda persona) |
