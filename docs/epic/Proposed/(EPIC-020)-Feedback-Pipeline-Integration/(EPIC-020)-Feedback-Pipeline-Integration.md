---
title: "Feedback Pipeline Integration"
artifact: EPIC-020
track: container
status: Proposed
author: cristos
created: 2026-03-21
last-updated: 2026-03-23
parent-vision: VISION-003
parent-initiative: INITIATIVE-003
priority-weight: ""
success-criteria:
  - Operator editorial context (tone, emphasis, corrections, framing guidance) flows into interpretation and fold stages as structured input
  - Community feedback (e.g., GitHub issues, reader corrections) is captured and routed to the relevant persona's interpretive context
  - Editorial review pass produces actionable annotations on generated interpretations before they enter the fold
  - Existing pipeline stages (interpret, fold, brief) consume editorial context without breaking when none is provided
depends-on-artifacts:
  - EPIC-009
  - EPIC-010
addresses: []
trove: ""
linked-epics:
  - EPIC-009
  - EPIC-010
  - EPIC-011
  - EPIC-013
linked-specs: []
linked-research: []
---

# Feedback Pipeline Integration

## Goal / Objective

Add an editorial input channel to the interpretation pipeline so that operator judgment and community feedback shape the generated interpretations. Today the pipeline is one-directional: evidence flows in, interpretations flow out, and the operator's only recourse is to re-run or manually edit outputs. This epic closes the loop — editorial context (tone guidance, factual corrections, emphasis shifts, framing notes) and external feedback (community corrections, reader questions) become first-class pipeline inputs that influence interpretation, fold, and brief stages.

The result is interpretations that reflect not just what the LLM infers from evidence and personas, but what the operator knows from domain expertise and what the community has surfaced through engagement.

## Scope Boundaries

**In scope:**
- Editorial policy file format and loader — structured operator guidance that persists across pipeline runs
- Editorial review pass — a new pipeline stage that annotates generated interpretations with editorial feedback before they enter the fold
- Editorial context integration into interpret and fold stages — passing editorial guidance as additional context to LLM calls
- Community feedback ingestion — routing GitHub issues, reader corrections, and other external input into persona-specific editorial context
- Graceful degradation — all stages must work identically when no editorial context exists

**Out of scope:**
- Per-meeting interpretation generation logic (EPIC-009 — this epic adds inputs, not new generation logic)
- Cumulative fold mechanics (EPIC-010 — this epic feeds context into the fold, not changing how folding works)
- Brief generation formatting (EPIC-011)
- Pipeline automation and scheduling (EPIC-013)
- Automated quality scoring or acceptance/rejection of interpretations — editorial input is advisory, not gatekeeping
- Public-facing feedback collection UI (INITIATIVE-004 / VISION-004)

## Child Specs

_To be decomposed. Anticipated specs:_

1. Editorial policy file format and loader — define the schema for operator editorial guidance (per-persona overrides, global tone, factual corrections) and the loader that makes it available to pipeline stages
2. Editorial review pass — new pipeline stage between interpret and fold that applies editorial annotations to generated interpretations
3. Community feedback ingestion — normalize external feedback (GitHub issues, corrections) into the editorial context format
4. Editorial context integration — modify interpret and fold stages to accept and use editorial context when available

## Key Dependencies

- EPIC-009 (per-meeting interpretations — the outputs this epic annotates)
- EPIC-010 (cumulative fold — the stage that consumes editorial-annotated interpretations)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-23 | — | Recreated from claude/feedback-pipeline-integration branch as EPIC-020 (EPIC-014 ID was already taken) |
