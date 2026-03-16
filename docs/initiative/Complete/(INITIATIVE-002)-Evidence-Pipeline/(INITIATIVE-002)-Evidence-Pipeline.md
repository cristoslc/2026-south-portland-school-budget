---
title: "Evidence Pipeline"
artifact: INITIATIVE-002
track: container
status: Complete
author: cristos
created: 2026-03-16
last-updated: 2026-03-16
parent-vision: VISION-002
success-criteria:
  - Evidence from all configured sources discovered and normalized automatically
  - Evidence pools updated within 24 hours of new content publication
  - Pipeline runs on self-hosted GitHub Actions runner without manual intervention
depends-on-artifacts: []
addresses: []
evidence-pool: ""
---

# Evidence Pipeline

## Strategic Focus

Build and operate the automated evidence collection infrastructure — source connectors, content normalization, pipeline orchestration, auto-discovery, and the self-hosted runner that keeps it all running. This initiative delivers the data foundation that VISION-003 (interpretation) and VISION-004 (public site) depend on.

## Scope Boundaries

**In scope:** Vimeo transcript download, Diligent/BoardDocs scraping, content normalization (VTT, PDF, HTML, XLSX), evidence pool assembly, auto-discovery polling, pipeline orchestration, self-hosted runner operation.

**Out of scope:** Interpretation of evidence (VISION-003), presentation of evidence (VISION-004).

## Child Epics

| Artifact | Title | Status |
|----------|-------|--------|
| EPIC-001 | Source Connectors | Complete |
| EPIC-002 | Content Normalization | Complete |
| EPIC-003 | Pipeline Orchestration | Complete |
| EPIC-004 | Source Auto-Discovery | Complete |
| EPIC-005 | Self-Hosted GitHub Actions Runner | Complete |
| EPIC-006 | Live Discovery Pipeline | Complete |

## Small Work (Epic-less Specs)

_None currently._

## Key Dependencies

- External: Vimeo API access, Diligent Community site availability, spsdme.org content structure

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-16 | — | Created during initiative migration; all child epics already complete |
| Complete | 2026-03-16 | — | All 6 child epics complete; evidence pipeline fully operational |
