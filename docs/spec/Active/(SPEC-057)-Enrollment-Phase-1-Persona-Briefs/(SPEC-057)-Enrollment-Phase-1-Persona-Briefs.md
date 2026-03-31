---
title: "Enrollment Phase 1 Persona Briefs"
artifact: SPEC-057
track: implementable
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
type: feature
parent-epic: EPIC-027
linked-artifacts:
  - INITIATIVE-005
  - SPEC-056
depends-on-artifacts:
  - SPEC-056
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Enrollment Phase 1 Persona Briefs

## Problem Statement

The gap analysis findings need to reach each persona in their own frame. A single analytical document doesn't serve Maria (worried about her kid's school), Tom (worried about taxes), or Dana (looking for a story) equally. The interpretation pipeline exists to translate evidence into persona-specific communication.

## Desired Outcomes

15 persona-specific enrollment gap briefs that surface what's missing from the decision basis. Interventionist tone — "here's what you need to know before this decision gets made, and here's what nobody has shown you yet." Each persona gets the same underlying analysis, presented in the frame that matters to them.

## External Behavior

**Inputs:**
- Gap analysis document (SPEC-056 output)
- Existing persona definitions (PERSONA-001 through PERSONA-015)
- Interpretation pipeline infrastructure (INITIATIVE-003)

**Outputs:**
- 15 persona-specific enrollment gap briefs in `dist/briefings/enrollment/`
- 1 general enrollment gap brief for non-persona audiences
- Published to site via INITIATIVE-004

**Constraints:**
- Must use the existing interpretation pipeline, not a custom generation process
- Tone is interventionist but factual — blazing red arrows around the gaps, but the arrows point at evidence, not opinions
- Each brief must include: what the persona should know, what questions they should ask, and what to watch for
- Briefs must be publishable before City Council budget adoption (time-sensitive)

## Acceptance Criteria

- Given the gap analysis and 15 personas, when briefs are generated, then each persona receives a brief tailored to their frame
- Given the briefs, when read, then the enrollment gaps are surfaced with specific claims, missing evidence, and suggested questions
- Given the general brief, when read by someone unfamiliar with the personas, then the core gap analysis is accessible
- Given publication, when deployed to the site, then briefs are accessible alongside existing persona briefings

## Scope & Constraints

**In scope:** Brief generation, publication.
**Out of scope:** Gap analysis itself (SPEC-056). Independent projections (Phase 2).

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-027 |
