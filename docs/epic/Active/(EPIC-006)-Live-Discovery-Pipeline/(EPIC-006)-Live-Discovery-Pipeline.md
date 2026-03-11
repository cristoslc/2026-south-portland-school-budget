---
title: "Live Discovery Pipeline"
artifact: EPIC-006
status: Active
author: cristos
created: 2026-03-11
last-updated: 2026-03-11
parent-vision: ""
success-criteria:
  - Connectors enumerate sources live on every run (no static config files)
  - Discovery history JSONL tracks all seen URLs with backoff for failures
  - Pipeline completes successfully with partial connector failures (resolves BUG-001)
  - YAML config files (vimeo-sources.yaml, budget-page-sources.yaml) removed
  - Pipeline can run hourly without excessive API load or log noise
depends-on: []
addresses: []
evidence-pool: ""
---

# Live Discovery Pipeline

## Goal / Objective

Refactor the evidence pipeline connectors from a config-driven model (discover once, download from static YAML list) to a live discovery model (enumerate every run, diff against repo, download missing). This eliminates stale config failures (BUG-001), simplifies the connector architecture, and supports hourly scheduling with backoff for persistent failures.

## Scope Boundaries

**In scope:**
- Shared live discovery connector model with history JSONL and backoff
- Vimeo connector refactor (remove vimeo-sources.yaml dependency)
- Budget page connector refactor (remove budget-page-sources.yaml dependency)
- Pipeline runner exit code fix (tolerate partial failures)

**Out of scope:**
- Diligent connector (already stateless — no config file)
- Normalizers (unchanged)
- New source types
- Pipeline scheduling changes (already handled by EPIC-005)

## Child Specs

| ID | Title | Status |
|----|-------|--------|
| SPEC-013 | Live Discovery Connector Model | Draft |
| SPEC-014 | Vimeo Live Discovery | Draft |
| SPEC-015 | Budget Page Live Discovery | Draft |

## Related Artifacts

| Artifact | Relationship |
|----------|-------------|
| ADR-001 | Architectural decision driving this epic |
| BUG-001 | Triggering defect — resolved by this work |
| EPIC-004 | Predecessor — its approach is superseded |
| SPEC-009 | Superseded by SPEC-014 |
| SPEC-010 | Superseded by SPEC-015 |

## Key Dependencies

- ADR-001 (Adopted — decision is made)
- Existing connector download logic (SPEC-001, SPEC-003) — reused, not rewritten

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-11 | _pending_ | Created directly in Active — design decided via ADR-001 |
