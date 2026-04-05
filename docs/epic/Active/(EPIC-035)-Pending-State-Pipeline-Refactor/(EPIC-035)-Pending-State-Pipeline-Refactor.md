---
title: Pending State Pipeline Refactor
artifact: EPIC-035
track: container
status: Active
author: cristos
created: 2026-04-04
last-updated: 2026-04-04
parent-vision: VISION-003
parent-initiative: INITIATIVE-003
priority-weight: high
success-criteria:
  - All LLM-intensive pipeline stages use pending state pattern with .pending/ directories
  - Multiple agents can fill sidecars in parallel without sequential bottleneck
  - Pipeline state visible via filesystem inspection (ls .pending/)
  - Failed sidecars recoverable without re-running completed stages
  - Runtime-agnostic: Claude, Codex, Crush, or human operators can fill sidecars
  - Batch gates prevent partial work from cascading to downstream stages
  - All existing pipeline functionality preserved (interpret, brief, fold, question extraction)
linked-artifacts:
  - SPIKE-012
  - SPIKE-013
depends-on-artifacts:
  - ADR-006
addresses: []
evidence-pool: ""
---

# Pending State Pipeline Refactor

## Goal / Objective

Refactor the LLM pipeline architecture to use the pending state pattern, decoupling agent execution from pipeline orchestration and enabling parallel, runtime-agnostic work.

## Desired Outcomes

**Operators** gain visibility into in-flight work without running scripts. Failures become recoverable without restarting from scratch. Multiple agents (human or machine) can work in parallel on independent work items.

**Personas** (end users) experience no change in output quality or latency—this is an architectural refactor with neutral user-facing impact.

**Developers** can swap runtimes (Claude, Codex, local models) without touching pipeline orchestration code.

## Progress

<!-- Auto-populated from session digests. -->

## Scope Boundaries

**In scope:**
- Pattern infrastructure: `.pending/` directory structure, generate/fill/resolve scripts
- Interpret stage refactoring: persona interpretations per meeting
- Brief stage refactoring: persona briefs per meeting
- Fold stage refactoring: cumulative synthesis per persona
- Question extraction refactoring
- Transport analysis refactoring (per-claim or per-configuration)
- Resolve scanner: unified script to apply completed work
- Runbook: operator procedures for fill/resume/retry

**Out of scope:**
- Discovery connectors (pure I/O, no LLM calls)
- Normalization (deterministic transforms, no LLM calls)
- Bundle creation (schema validation, no LLM calls)
- Site build (static generation, no LLM calls)
- MCP server or API endpoints (not required for pattern adoption)
- Task queue infrastructure (Celery, RQ, Redis)
- Database-backed state tracking

## Child Specs

- SPEC-082: Pending State Infrastructure (pattern scaffolding, directory structure, resolve scanner)
- SPEC-083: Interpret Stage Sidecar Generation
- SPEC-084: Interpret Stage Sidecar Resolution
- SPEC-085: Brief Stage Sidecar Generation and Resolution
- SPEC-086: Cumulative Fold Sidecar Generation and Resolution
- SPEC-087: Question Extraction Sidecar Generation and Resolution
- (Additional SPECs for transport analysis as needed)

## Key Dependencies

- ADR-006: Architectural decision establishing the pattern
- Existing pipeline scripts must remain functional during migration (feature flag or parallel implementation)
- No external service dependencies (filesystem is state store)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-04-04 | | Initial creation |