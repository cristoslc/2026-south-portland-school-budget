---
title: "Persona Routing Selector"
artifact: SPEC-029
type: feature
status: Proposed
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
parent-epic: EPIC-015
parent-initiative: ""
priority-weight: medium
acceptance-criteria:
  - Landing page has an "I am a..." interactive selector
  - Selecting a role routes directly to the matching briefing
  - Works without JavaScript (graceful degradation to briefings index)
  - Mobile-friendly tap targets
depends-on-artifacts:
  - EPIC-015
addresses: []
---

# Persona Routing Selector

## Problem

First-time visitors don't know which of the 15 persona briefings matches them. They must scan a grid of cards and infer from titles like "Concerned Elementary Parent" vs "Pragmatic Elementary Parent." A parent of a third-grader worried about school closure shouldn't have to parse persona taxonomy.

## Proposed Solution

Add an "I am a..." selector to the landing page — a simple set of role buttons (Parent, Teacher/Staff, Taxpayer, Board Member, Journalist, Student) that routes to the most relevant briefing or shows a filtered view. Not a quiz — just role-based routing with one click.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-22 | — | From persona-lens design review |
