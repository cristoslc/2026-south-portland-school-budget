---
title: "Site Data Assembly"
artifact: EPIC-019
track: container
status: Proposed
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
parent-vision: VISION-004
parent-initiative: INITIATIVE-004
priority-weight: medium
success-criteria:
  - Site content collections cover all data sources (briefings, personas, evidence syntheses, questions)
  - Content schemas validate at build time
  - Pipeline-to-site data flow documented
  - Build fails on schema violations (no silent data loss)
depends-on-artifacts:
  - EPIC-014
  - INITIATIVE-003
addresses: []
evidence-pool: ""
---

# Site Data Assembly

## Goal / Objective

Extend the site's content collection layer to cover all data sources needed by the question hub, evidence browser, and any future pages — beyond the initial briefings and personas.

## Desired Outcomes

Every piece of structured data the site needs is loaded through Astro content collections with Zod schema validation. Schema errors caught at build time, not at runtime. New data types (questions, evidence syntheses, meeting timelines) can be added without changing the build pipeline.

## Scope Boundaries

**In scope:** Content collection definitions for questions, evidence syntheses, meeting bundles, journey maps. Schema definitions. Build-time validation.

**Out of scope:** Content generation (that's INITIATIVE-003), page templates (EPIC-015/017), visual design (EPIC-016).

## Child Specs

| Artifact | Title | Status |
|----------|-------|--------|
| SPEC-032 | Evidence synthesis content collection | _to be created_ |
| SPEC-033 | Meeting timeline data collection | _to be created_ |
| SPEC-034 | Question data schema and collection | _to be created_ |

## Key Dependencies

- EPIC-014 (Astro scaffolding)
- INITIATIVE-003 (produces the data that feeds these collections)
- EPIC-017 (question hub defines what question data looks like)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-22 | — | Agent-suggested; scope depends on EPIC-017 decisions |
