---
title: "Progressive Event-Scoped Fold"
artifact: EPIC-037
track: container
status: Active
author: cristos
created: 2026-04-05
last-updated: 2026-04-05
parent-vision: VISION-003
parent-initiative: INITIATIVE-003
priority-weight: high
success-criteria:
  - Fold points are event-scoped, not meeting-scoped — inter-meeting evidence triggers folds alongside meeting interpretations
  - Evidence reclassification (inter-meeting to bundled) correctly stales and re-folds affected fold points forward
  - Progressive re-folding detects the first stale fold point in a persona's event sequence and re-folds from there, skipping valid earlier folds
  - Fold history is recorded per persona x fold point with hashstamped commits and outputs for staleness detection
  - Existing meeting-scoped fold behavior is preserved as one event type within the new model
depends-on-artifacts:
  - EPIC-010
addresses: []
evidence-pool: ""
---

# Progressive Event-Scoped Fold

## Goal / Objective

Evolve the fold pipeline from meeting-scoped (one fold per meeting per persona) to event-scoped (one fold per evidence event per persona) with progressive re-folding. The current architecture treats meetings as the only fold trigger, but inter-meeting evidence (document releases, news articles, public statements) also changes what a persona knows. When that evidence later gets bundled with a meeting transcript, the prior fold is stale because the evidence is now contextualized differently. The fold pipeline needs to handle both triggers and know when to re-fold.

## Desired Outcomes

Personas get cumulative records that reflect their full information timeline, not just what they learned at meetings. The operator sees folds that are never unnecessarily re-run (progressive) but always re-run when inputs change (stale-aware). The pipeline can answer: "what does Maria know right now?" at any point in the budget season, including between meetings.

This advances INITIATIVE-003's success criterion: "Cumulative narratives maintained with temporal fold tracking position shifts and supersessions" by extending temporal tracking to cover the full evidence lifecycle.

## Scope Boundaries

**In scope:**
- Event model defining fold point types (meeting-interpretation, inter-meeting evidence, evidence reclassification)
- Staling rules per event type (what invalidates which folds, cascade semantics)
- Progressive re-fold algorithm (detect first stale point, re-fold forward, skip valid prefixes)
- Fold history recording (sidecar per persona x fold point with input hashes and commit references)
- Integration with existing pending state infrastructure (ADR-006, SPEC-086)

**Out of scope:**
- Changes to the evidence collection pipeline (INITIATIVE-002)
- Changes to brief generation (EPIC-011) — briefs consume fold output but their generation logic is unchanged
- New persona definitions
- Bundle schema changes (SPEC-016) — bundles remain meeting-scoped evidence containers

## Child Specs

| Artifact | Title | Status |
|----------|-------|--------|
| SPIKE-014 | Progressive Fold Event Model | Active |

_Implementation specs to be created after SPIKE-014 completes._

## Key Dependencies

- [EPIC-010](../../epic/Complete/(EPIC-010)-Cumulative-Narrative-Fold/(EPIC-010)-Cumulative-Narrative-Fold.md) (existing fold engine — this epic extends it)
- [SPIKE-006](../../research/Complete/(SPIKE-006)-Cumulative-Fold-Strategy/(SPIKE-006)-Cumulative-Fold-Strategy.md) (log-structured approach — foundational design decision)
- [SPEC-086](../../spec/Active/(SPEC-086)-Cumulative-Fold-Sidecar-Generation-and-Resolution/(SPEC-086)-Cumulative-Fold-Sidecar-Generation-and-Resolution.md) (sidecar pattern — progressive fold builds on this)
- ADR-006 (pending state pattern)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-04-05 | — | Created from design discussion; SPIKE-014 is first child |
