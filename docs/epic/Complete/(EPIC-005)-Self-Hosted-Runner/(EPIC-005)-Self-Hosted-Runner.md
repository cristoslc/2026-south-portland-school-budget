---
title: "Self-Hosted GitHub Actions Runner"
artifact: EPIC-005
status: Complete
author: cristos
created: 2026-03-11
last-updated: 2026-03-11
parent-vision: ""
success-criteria:
  - Pipeline workflow executes on a local Docker-based self-hosted runner
  - Zero GitHub Actions quota consumed for scheduled pipeline runs
  - Hosted runner fallback triggers automatically when self-hosted is unavailable
  - Schedule reduced to 2x/day (8 AM and 8 PM ET)
depends-on: []
addresses: []
evidence-pool: ""
---

# Self-Hosted GitHub Actions Runner

## Goal / Objective

Eliminate GitHub Actions quota consumption for the evidence pipeline by running scheduled workflows on a local Docker-based self-hosted runner. The runner polls GitHub (no inbound ports required), has all Python dependencies baked in, and runs via docker-compose. The workflow falls back to hosted runners when the self-hosted runner is unavailable.

## Scope Boundaries

**In scope:**
- Dockerfile with Python 3.12, pip deps, and GitHub Actions runner agent
- docker-compose.yml for persistent runner operation
- Workflow update: self-hosted primary, hosted fallback, 2x/day schedule
- Runbook for initial setup and runner registration

**Out of scope:**
- Multi-runner scaling
- Kubernetes or cloud deployment
- Runner for other workflows (only the evidence pipeline)

## Child Specs

| ID | Title | Status |
|----|-------|--------|
| SPEC-012 | Docker Runner Setup | Implemented |

## Child Runbooks

| ID | Title | Status |
|----|-------|--------|
| RUNBOOK-001 | Standing Up the Self-Hosted Runner | Active |

## Key Dependencies

- Docker Desktop or Docker Engine on the host machine
- GitHub personal access token or runner registration token
- Existing pipeline workflow (.github/workflows/pipeline.yml)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-11 | _pending_ | Created directly in Active — straightforward infra work |
| Complete | 2026-03-11 | _pending_ | SPEC-012 implemented, RUNBOOK-001 active |
