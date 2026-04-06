---
title: "Interpretation Pipeline"
artifact: INITIATIVE-003
track: container
status: Active
author: cristos
created: 2026-03-16
last-updated: 2026-03-16
parent-vision: VISION-003
success-criteria:
  - Every budget-relevant meeting interpreted through all 14 personas
  - Cumulative narratives maintained with temporal fold tracking position shifts and supersessions
  - Briefs generated for upcoming meetings
  - Pipeline automation runs interpretation chain after evidence updates
depends-on-artifacts:
  - INITIATIVE-002
addresses: []
trove: ""
linked-epics:
  - EPIC-008
  - EPIC-009
  - EPIC-010
  - EPIC-011
  - EPIC-013
  - EPIC-037
linked-artifacts:
  - INITIATIVE-004
  - INITIATIVE-004
linked-research: []
---

# Interpretation Pipeline

## Strategic Focus

Systematically interpret every meeting through 14 persona lenses, fold interpretations into cumulative narratives that track how each stakeholder's understanding evolves, generate forward-looking briefs, and automate the entire chain so it runs after evidence updates land. This initiative delivers the analytical layer between raw evidence (INITIATIVE-002) and public presentation (INITIATIVE-004).

## Scope Boundaries

**In scope:** Meeting bundling, per-meeting persona interpretation, cumulative fold with temporal tracking, brief generation, pipeline automation via two-track architecture (deterministic runner + local LLM polling), question clustering for downstream consumption.

**Out of scope:** Evidence collection (INITIATIVE-002), public-facing presentation (INITIATIVE-004).

## Child Epics

| Artifact | Title | Status |
|----------|-------|--------|
| EPIC-008 | Meeting Bundler | Complete |
| EPIC-009 | Per-Meeting Interpretation Engine | Complete |
| EPIC-010 | Cumulative Narrative Fold | Complete |
| EPIC-011 | Upcoming Event Brief Generation | Complete |
| EPIC-012 | Interpretation Pipeline Automation | Abandoned (superseded by EPIC-013) |
| EPIC-013 | Polling Interpretation Pipeline | Proposed |
| EPIC-037 | Progressive Event-Scoped Fold | Active |

## Small Work (Epic-less Specs)

_None currently._

## Key Dependencies

- INITIATIVE-002 (evidence pipeline must produce bundles)
- ADR-002 (Polling LLM Pipeline Over Runner-Based LLM) gates EPIC-013

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-16 | — | Created during initiative migration; 4/5 child epics complete |
