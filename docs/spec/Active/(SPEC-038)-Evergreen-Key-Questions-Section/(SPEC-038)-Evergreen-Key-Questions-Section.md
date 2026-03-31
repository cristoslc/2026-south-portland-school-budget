---
title: "Evergreen Key Questions Section"
artifact: SPEC-038
track: implementable
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
priority-weight: ""
type: feature
parent-epic: EPIC-021
linked-artifacts:
  - SPIKE-008
depends-on-artifacts:
  - SPEC-034
  - SPEC-036
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Evergreen Key Questions Section

## Problem Statement

The PERSONA-000 evergreen brief needs a "Key Questions" section that surfaces the highest-priority unanswered questions ranked by score. SPIKE-008 prototyped this as a static table. This spec makes it a pipeline-generated section that reads from QUESTION artifacts and renders a priority-ranked summary.

## Desired Outcomes

Any resident reading the evergreen brief sees, at a glance, which questions the community has been asking the longest without getting answers. The section updates automatically each pipeline run. It complements (not replaces) the existing "Open Questions" section, which tracks pending institutional decisions rather than cross-persona unresolved threads.

## External Behavior

**Inputs:**
- All Active QUESTION artifacts in `docs/question/Active/` (read frontmatter for score, canonical phrasing, persona count, resolution status)

**Outputs:**
- A "Key Questions" section in the PERSONA-000 evergreen brief, positioned between "Major Decisions Ahead" and "Open Questions"

**Constraints:**
- Table must show: priority score, canonical question (truncated if needed), open-since date, perspective count, status
- Top-N questions shown (N configurable, default all Active questions)
- Section includes a link to full question artifacts for detail
- Must not disrupt existing evergreen brief structure

## Acceptance Criteria

1. **Given** 5 Active QUESTION artifacts with scores 592, 540, 378, 66, and 0, **when** the evergreen brief is generated, **then** the Key Questions table lists them in descending score order.

2. **Given** a QUESTION transitions from Active to Resolved, **when** the next evergreen brief is generated, **then** that question no longer appears in the Key Questions table.

3. **Given** a QUESTION has `resolution-status: claimed` with 3/6 variants resolved, **when** the evergreen brief renders, **then** the status column shows "Partial (3/6)" rather than "Open."

4. **Given** the existing "Open Questions" section is present, **when** the Key Questions section is generated, **then** both sections appear with the Key Questions section above Open Questions.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

**In scope:** Evergreen brief template modification, pipeline step to render the Key Questions section from QUESTION artifact frontmatter.

**Out of scope:** Per-persona briefing integration (future — persona briefs could reference canonical questions instead of re-deriving them). Site-facing question display (EPIC-017).

## Implementation Approach

1. In the evergreen brief generation step, scan `docs/question/Active/` and read frontmatter from each QUESTION artifact.
2. Sort by `priority-score` descending.
3. Render a markdown table with the required columns.
4. Insert the section at the correct position in the evergreen brief template.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Operator-requested |
