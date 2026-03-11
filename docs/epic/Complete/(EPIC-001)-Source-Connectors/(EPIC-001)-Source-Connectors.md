---
title: "Source Connectors"
artifact: EPIC-001
status: Complete
author: cristos
created: 2026-03-10
last-updated: 2026-03-10
parent-vision: VISION-002
success-criteria:
  - Each connector can discover new content published since its last run
  - Each connector downloads new content to the correct data/ subdirectory
  - Connectors are idempotent -- re-running produces no duplicate downloads
depends-on: []
addresses: []
evidence-pool: ""
---

# Source Connectors

## Goal / Objective

Build individual connectors for each source type that can discover and download new meeting materials. Each connector knows one source site, can detect what's new since the last check, and fetches it to the local `data/` tree.

Three connectors are needed:

1. **Vimeo / SPC-TV** -- Use `yt-dlp` to download auto-generated VTT captions for new SPC-TV videos. No API token needed (SPIKE-001).
2. **Diligent Community** -- Fetch city council agendas via the portal's public REST API. No scraping needed (SPIKE-002).
3. **spsdme.org budget page** -- Poll the budget page for new PDF links (packets, presentations, spreadsheets) and download them.

## Scope Boundaries

**In scope:**
- Source discovery (what's new since last run)
- Download to `data/` in the existing directory structure
- De-duplication (skip already-downloaded content)
- Connector-level error handling and logging

**Out of scope:**
- Content normalization (EPIC-002)
- Scheduling and orchestration (EPIC-003)
- BoardDocs connector (platform retired March 2026; historical data already collected)

## Child Specs

- SPEC-001: Vimeo VTT Connector (yt-dlp wrapper)
- SPEC-002: Diligent Community Agenda Connector (REST API client)
- SPEC-003: Budget Page PDF Connector (HTML polling + download)

## Key Dependencies

- SPIKE-001 (Complete) -- confirmed yt-dlp approach for Vimeo
- SPIKE-002 (Complete) -- confirmed public REST API for Diligent Community

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-10 | _pending_ | Initial creation |
| Active | 2026-03-10 | 19807c6 | All gating spikes complete; decomposing into specs |
| Complete | 2026-03-10 | 4e32287 | All 3 child specs implemented and verified |
