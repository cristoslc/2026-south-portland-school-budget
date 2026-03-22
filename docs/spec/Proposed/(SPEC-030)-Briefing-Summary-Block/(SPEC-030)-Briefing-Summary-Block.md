---
title: "Briefing Summary Block"
artifact: SPEC-030
type: feature
status: Proposed
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
parent-epic: EPIC-015
parent-initiative: ""
priority-weight: medium
acceptance-criteria:
  - Each briefing page starts with a 2-3 sentence TL;DR summary
  - Summary is visually distinct (callout box or highlighted block)
  - Summary is copy-paste friendly for sharing in group chats
  - Generated automatically by the brief generation pipeline
depends-on-artifacts:
  - EPIC-015
addresses: []
---

# Briefing Summary Block

## Problem

The Group Chat Relay persona (Meg) needs a shareable snippet she can paste into a text thread. Current briefings are long and well-structured but lack a quick-grab summary. She has to read the whole thing to find the key takeaway.

## Proposed Solution

Add a summary block at the top of each briefing — 2-3 sentences, visually distinct, optimized for copy-paste. The pipeline's brief generation step should produce this as a frontmatter field or structured section.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-22 | — | From persona-lens design review (Meg persona) |
