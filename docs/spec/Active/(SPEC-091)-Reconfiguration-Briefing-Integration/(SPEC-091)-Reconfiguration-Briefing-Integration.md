---
title: "Reconfiguration Briefing Integration"
artifact: SPEC-091
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
depends-on-artifacts:
  - SPEC-089
addresses: []
evidence-pool: "school-integration-policy"
source-issue: ""
swain-do: required
---

# Reconfiguration Briefing Integration

## Problem Statement

The 2024 Boundaries & Configurations context needs to surface in persona briefings where relevant topics arise — not as a bolted-on section, but as reference material drawn in by the keyword trigger system (SPEC-081). This requires two pipeline passes: first to verify the expanded trove's triggers inject correctly, second to regenerate briefings with the enriched context.

## Desired Outcomes

Persona briefings that discuss attendance boundaries, controlled choice, magnet programs, or integration topics naturally include historical context from the 2024 process and national research. Personas whose briefings never touch those topics get nothing added. The integration is invisible to the reader — it reads as the briefing author knowing the relevant history, not as a pasted-in reference block.

## External Behavior

**Pass 1 — Trigger verification:**
- Run the pipeline's reference context injection on the current briefing set
- Verify that keyword triggers from the expanded trove manifest (`boundaries`, `controlled choice`, `magnet`, `attendance zone`, `guiding principles`, `steering committee`, `integration`, `detracking`, etc.) match at least one persona briefing's content
- Log which personas triggered and which did not

**Pass 2 — Briefing regeneration:**
- Regenerate all persona briefings with the expanded trove context available
- The LLM draws on the injected 2024 context where a briefing paragraph matches trigger keywords
- Not every persona will trigger — a student discussing band cuts does not get integration research; a community member discussing attendance boundaries does

**Quality gate:**
- Review regenerated briefings for adversarial or editorializing language introduced by the 2024 context
- Verify that injected context is factual and grounded in trove sources
- Confirm that personas with no triggering content have unchanged briefings

## Acceptance Criteria

- AC-1: Given the expanded trove with keyword triggers, when Pass 1 runs, then at least one persona briefing triggers reference context injection for a 2024-related keyword.
- AC-2: Given a persona briefing that discusses attendance boundaries, when regenerated in Pass 2, then it includes factual context about the Board's 2024 directives on zone review or controlled choice.
- AC-3: Given a persona briefing that does not mention any trigger keywords, when regenerated in Pass 2, then its content is unchanged from the pre-integration version.
- AC-4: Given any regenerated briefing with injected 2024 context, when reviewed for tone, then no adversarial or editorializing language is present.

## Scope & Constraints

**In scope:** Two-pass pipeline execution, trigger verification, briefing regeneration, tone review.

**Out of scope:** Trove expansion (SPEC-089). Site restructure (SPEC-090). Changes to SPEC-081's keyword trigger mechanism itself. Manual editing of individual briefings.

**Constraint:** The 2024 context enters as reference material for the LLM, not as a template section. The output should read as naturally informed, not as a mechanical insertion.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-04-05 | — | Created as EPIC-036 child spec (Phase 3) |
