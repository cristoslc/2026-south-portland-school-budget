---
title: "School Integration Trove Expansion"
artifact: SPEC-089
track: implementable
status: Active
author: cristos
created: 2026-04-05
last-updated: 2026-04-05
priority-weight: ""
type: feature
parent-epic: EPIC-036
parent-initiative: ""
linked-artifacts:
  - SPEC-081
depends-on-artifacts: []
addresses: []
evidence-pool: "school-integration-policy"
source-issue: ""
swain-do: required
---

# School Integration Trove Expansion

## Problem Statement

The `school-integration-policy` trove has 2 sources: the SPSD Boundaries & Configurations web page and the TCF nine-districts report. This is not enough to tell the full story of the 2024 process. The community engagement findings, steering committee recommendations, board meeting minutes, and any consultant reports are missing. Without these primary sources, the reconfiguration context page (SPEC-090) cannot present the full narrative.

## Desired Outcomes

The trove contains enough primary source material to support a factual narrative of the 2024 Boundaries & Configurations process — what the community said, what the steering committee recommended, how the Board deliberated, and what they decided. Gaps (e.g., an unreleased consultant report) are documented in the synthesis rather than silently omitted.

## External Behavior

**Source collection targets:**
- Board meeting minutes from the 2024 Boundaries & Configurations process (steering committee formation, guiding principles adoption, May 2024 action items vote)
- Community engagement session summaries or reports (if published by the district)
- Steering committee findings or recommendations (if published)
- Consultant report on magnet programs and controlled choice (directed by January 2025; document as gap if not publicly available)
- Annual attendance zone demographic report (directed by November 30 annually; document as gap if not published)

**Collection method:** Browser automation for JS-rendered district pages; web fetch for static documents. Normalize all sources to markdown per existing trove conventions.

**Trove updates:**
- Add new sources to `manifest.yaml` with keyword triggers
- Update `synthesis.md` to incorporate findings from new sources
- Document gaps explicitly in the synthesis (e.g., "The Board directed a consultant report by January 2025. No such report has been located in public meeting documents or on the district website as of this writing.")

## Acceptance Criteria

- AC-1: Given the trove has 2 sources, when expansion is complete, then it contains at least 4 primary sources covering the 2024 process.
- AC-2: Given a source is not publicly available, when it is referenced in Board directives, then the synthesis documents the gap with the directive date and expected delivery.
- AC-3: Given new sources are added, when the manifest is updated, then each source has keyword triggers that match the content's key topics.
- AC-4: Given the synthesis is updated, when read by a non-expert, then it tells a coherent story of the 2024 process without requiring readers to cross-reference raw sources.

## Scope & Constraints

**In scope:** Source collection, normalization, manifest updates, synthesis rewrite, gap documentation.

**Out of scope:** Building site pages (SPEC-090). Briefing regeneration (SPEC-091). Creating new analysis documents from the sources — the trove collects and synthesizes, it does not produce original analytical content.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-04-05 | — | Created as EPIC-036 child spec (Phase 1) |
