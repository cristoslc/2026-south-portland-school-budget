---
title: "Key Questions Tracking"
artifact: EPIC-021
track: container
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
parent-vision: VISION-003
parent-initiative: INITIATIVE-003
priority-weight: high
success-criteria:
  - Canonical questions extracted and clustered from per-persona briefings into a scored QUESTIONS artifact
  - Priority score computed as age (days since first raised) x breadth (persona count), recalculated each pipeline run
  - Resolution stress-test gate requires every persona variant to pass before a question moves to resolved
  - Top-N unresolved questions surface in PERSONA-000 evergreen brief "Key Questions" section
  - Pipeline produces the QUESTIONS artifact automatically — no manual curation required
depends-on-artifacts:
  - EPIC-009
  - EPIC-017
addresses: []
evidence-pool: ""
---

# Key Questions Tracking

## Goal / Objective

Build a pipeline-level feature that extracts unresolved questions from persona briefings, clusters them into canonical questions, scores them by age and breadth, and surfaces the highest-priority unanswered questions in the PERSONA-000 evergreen brief. Resolution requires stress-testing against every persona's specific framing of the question — a generic administration response does not close a canonical question unless it satisfies all persona variants.

## Desired Outcomes

Residents and meeting attendees see, at a glance, which questions have been outstanding the longest and across the most perspectives. The administration's pattern of acknowledging questions without answering them becomes visible and trackable. Persona briefings can reference the canonical question rather than re-deriving it each cycle, reducing redundancy and increasing coherence across briefs.

## Scope Boundaries

**In scope:**
- New QUESTIONS artifact type: YAML objects in `data/interpretation/questions/` with id, canonical phrasing, first-raised date, persona variants, status, resolution evidence, stress-test results, and computed priority score
- Pipeline step: extract questions from per-persona briefs, cluster into canonical questions, score, and write QUESTIONS artifact
- Pipeline step: on new evidence, detect potential resolutions and run stress-test gate against all persona variants
- PERSONA-000 integration: "Key Questions" section ranked by priority score
- Partial resolution handling: when some persona variants are answered but others remain open, the canonical question stays open with the resolved variants marked

**Out of scope:**
- Site-facing question display (handled by [EPIC-017](../../Active/(EPIC-017)-Question-Hub/(EPIC-017)-Question-Hub.md))
- Community-submitted questions ([EPIC-018](../../Proposed/(EPIC-018)-Community-Feedback/(EPIC-018)-Community-Feedback.md))
- Manual question curation UI
- Historical backfill beyond the current evidence corpus

## Child Specs

| Artifact | Title | Status |
|----------|-------|--------|
| SPIKE-008 | Question Scoring Prototype | Active |

_Specs to be created after SPIKE-008 findings._

## Key Dependencies

- [EPIC-009](../../Complete/(EPIC-009)-Per-Meeting-Interpretation-Engine/(EPIC-009)-Per-Meeting-Interpretation-Engine.md) (interpretation engine produces the per-persona briefs that contain extractable questions)
- [EPIC-017](../../Active/(EPIC-017)-Question-Hub/(EPIC-017)-Question-Hub.md) (question extraction pipeline from SPEC-025 provides the raw material; this epic adds clustering, scoring, and resolution tracking)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created directly as Active — operator-requested |
