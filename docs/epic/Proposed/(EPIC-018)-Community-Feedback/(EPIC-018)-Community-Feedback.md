---
title: "Community Feedback"
artifact: EPIC-018
track: container
status: Proposed
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
parent-vision: VISION-004
parent-initiative: INITIATIVE-004
priority-weight: medium
success-criteria:
  - Residents can flag inaccurate claims on any answer or briefing page
  - Residents can suggest new questions
  - Flags and suggestions are collected in a reviewable format
  - No backend required (static site constraint)
depends-on-artifacts:
  - EPIC-015
  - EPIC-017
addresses: []
evidence-pool: ""
---

# Community Feedback

## Goal / Objective

Create a feedback loop so residents can flag inaccuracies and suggest questions, making the analysis self-correcting and community-driven — all within the constraints of a static site.

## Desired Outcomes

Community members who spot an error or have an unanswered question have a low-friction way to report it. The project maintainer can triage these without building a backend.

## Scope Boundaries

**In scope:** Inline flag buttons on briefing/answer pages, question suggestion form, feedback collection mechanism.

**Out of scope:** Real-time moderation, user accounts, comment threads, backend services.

## Child Specs

| Artifact | Title | Status |
|----------|-------|--------|
| SPEC-030 | Inline accuracy flag | _to be created_ |
| SPEC-031 | Question suggestion form | _to be created_ |

## Key Dependencies

- EPIC-015 (pages must exist to add feedback UI)
- EPIC-017 (answer pages are the primary flagging surface)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-22 | — | Agent-suggested; operator decision needed on feedback mechanism |
