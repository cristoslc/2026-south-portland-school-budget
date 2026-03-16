---
title: "Public Budget Site"
artifact: INITIATIVE-004
track: container
status: Active
author: cristos
created: 2026-03-16
last-updated: 2026-03-16
parent-vision: VISION-004
success-criteria:
  - Residents find answers within two clicks from landing page
  - Site rebuilds automatically from pipeline outputs
  - Community feedback loop operational (flags, question suggestions)
  - At least one answer or briefing shared in a public forum
depends-on-artifacts:
  - INITIATIVE-003
addresses: []
evidence-pool: ""
---

# Public Budget Site

## Strategic Focus

Build and deploy a question-first static site (Astro, GitHub Pages) that gives South Portland residents access to AI-analyzed budget interpretations, persona-tailored briefings, and evidence-linked answers. The site is the public face of the entire analysis project — it makes the work of VISION-001/002/003 accessible to non-technical residents.

## Scope Boundaries

**In scope:** Astro site scaffolding, content collection schemas, site data assembly (pipeline → Astro), question hub, answer pages, persona pages, meeting timeline, evidence browser, inline flagging system, community question submission, visual design, GitHub Pages deployment, continuous deploy workflow.

**Out of scope:** Evidence collection (INITIATIVE-002), interpretation and analysis (INITIATIVE-003), budget lever calculation engine (INITIATIVE-001 — though results are presented here).

## Child Epics

| Artifact | Title | Status |
|----------|-------|--------|
| EPIC-013 | Site Scaffolding | _to be created_ |
| EPIC-014 | Site Data Assembly | _to be created_ |
| EPIC-015 | Core Pages | _to be created_ |
| EPIC-016 | Feedback System | _to be created_ |
| EPIC-017 | Visual Design | _to be created_ |
| EPIC-018 | Continuous Deploy | _to be created_ |

## Small Work (Epic-less Specs)

_None currently._

## Key Dependencies

- INITIATIVE-003 (interpretation outputs and question clustering)
- INITIATIVE-001 (budget lever data, when available)
- EPIC-012 / SPIKE-007 (pipeline automation for continuous deploy)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-16 | — | Created during initiative migration; child epics not yet created |
