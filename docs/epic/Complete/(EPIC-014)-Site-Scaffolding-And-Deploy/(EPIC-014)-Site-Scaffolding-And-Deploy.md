---
title: "Site Scaffolding and Deploy"
artifact: EPIC-014
track: container
status: Complete
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
parent-vision: VISION-004
parent-initiative: INITIATIVE-004
priority-weight: high
success-criteria:
  - Astro project scaffolded with content collections pointing at existing content
  - GitHub Pages deployment working on push
  - Site accessible at cristoslc.github.io/south-portland-school-budget-FY27
depends-on-artifacts:
  - ADR-003
addresses: []
evidence-pool: ""
---

# Site Scaffolding and Deploy

## Goal / Objective

Stand up the Astro static site generator with content collections that read directly from the existing `dist/briefings/` and `docs/persona/Active/` directories, deploy to GitHub Pages, and establish the build/deploy pipeline.

## Desired Outcomes

Residents can access the site at a public URL. Content authors (the interpretation pipeline) don't need to do anything special — new briefings appear automatically on rebuild. The deploy workflow runs on push without manual intervention.

## Scope Boundaries

**In scope:** Astro project setup, content collection config with glob loaders, GitHub Pages workflow, base URL config, favicon, package.json.

**Out of scope:** Page design (EPIC-015), visual polish (EPIC-016), content beyond what the collections provide.

## Child Specs

Work was done directly without formal specs — the scaffolding was a single-session build.

| Artifact | Title | Status |
|----------|-------|--------|
| — | Astro project init with content collections | Complete (commit cd1f1a4) |
| — | GitHub Pages deployment workflow | Complete (commit cd1f1a4) |
| — | GitHub Pages API enablement | Complete (gh api call, same session) |

## Key Dependencies

- ADR-003 (Astro content collections decision)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | cd1f1a4 | Created and shipped in single session |
| Complete | 2026-03-22 | cd1f1a4 | All success criteria met |
