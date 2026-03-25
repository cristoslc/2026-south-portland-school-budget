---
title: "Question Hub"
artifact: EPIC-017
track: container
status: Active
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
parent-vision: VISION-004
parent-initiative: INITIATIVE-004
priority-weight: high
success-criteria:
  - Questions page shows categorized budget questions residents are asking
  - Each question links to a sourced answer page with evidence citations
  - Residents find answers within two clicks from landing page
  - Questions are organized by topic, not by persona
depends-on-artifacts:
  - EPIC-015
  - INITIATIVE-003
addresses: []
evidence-pool: ""
---

# Question Hub

## Goal / Objective

Build the question-first navigation layer that VISION-004 calls for — a hub where residents can browse and search the budget questions they're actually asking, with each question leading to a sourced, evidence-linked answer.

## Desired Outcomes

Residents who arrive at the site with a specific concern ("Will my kid's school close?", "How much will my taxes go up?") can find a direct answer within two clicks. The question-first approach distinguishes this site from a document dump or meeting archive.

## Scope Boundaries

**In scope:** Questions index page, individual answer pages, question categorization, evidence citations within answers, cross-links to relevant briefings and persona perspectives.

**Out of scope:** Community question submission (EPIC-018), question curation workflow, AI-generated question clustering (may be a spike).

## Child Specs

| Artifact | Title | Status |
|----------|-------|--------|
| SPEC-025 | Question Extraction | Active |
| SPEC-026 | Questions Index Page | Active |
| SPEC-027 | Answer Detail Pages | Active |

## Key Dependencies

- EPIC-015 (core pages and layout must exist)
- INITIATIVE-003 (briefings contain the "Open Questions" sections that seed the question set)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-22 | — | Agent-suggested during decomposition; operator decision needed on question sourcing |
| Active | 2026-03-22 | — | Activated by operator — approach C (auto-extract + curate) |
