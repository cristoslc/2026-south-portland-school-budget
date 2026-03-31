---
title: "District Enrollment Claims Catalog"
artifact: SPEC-040
track: implementable
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
priority-weight: high
type: ""
parent-epic: EPIC-022
linked-artifacts:
  - EPIC-023
depends-on-artifacts: []
addresses:
  - JOURNEY-002.PP-03
  - JOURNEY-001.PP-03
evidence-pool: "fy27-budget-documents, school-board-budget-meetings"
source-issue: ""
swain-do: required
---

# District Enrollment Claims Catalog

## Problem Statement

The district's closure recommendation rests on enrollment assumptions scattered across budget documents, board presentations, and public testimony. No systematic inventory exists of what enrollment claims the district has made, what evidence supports each claim, and what questions remain unanswered. Without this catalog, the gap analysis (EPIC-023) lacks a structured foundation.

## Desired Outcomes

Every enrollment-related claim and assumption in the district's published materials is extracted, cataloged, and mapped to source evidence. The gap analysis team (EPIC-023) has a structured input that identifies exactly which assumptions need scrutiny. The public can see — in one place — what the district has claimed about enrollment and where each claim comes from.

## External Behavior

**Inputs:**
- Existing evidence pools: fy27-budget-documents, school-board-budget-meetings, city-council-meetings-2026
- Interpretation pipeline outputs (existing persona briefs and meeting summaries)

**Outputs:**
- Structured claims catalog (JSON/CSV) with fields: claim text, source document, source page/timestamp, claim category (enrollment level, trend, projection, capacity), evidence status (supported/unsupported/unpublished/unexamined)
- Each claim linked to its source with sufficient precision for independent verification
- Summary statistics: total claims identified, breakdown by category and evidence status

**Constraints:**
- Claims must be extracted verbatim or with minimal paraphrase — preserve the district's own language
- Evidence status assessment at this stage is preliminary (supported/unsupported based on what's in existing evidence pools); deep analysis is EPIC-023's scope
- Focus on enrollment-related claims only — budget, staffing, and other claims are out of scope

## Acceptance Criteria

1. Given the catalog exists, when filtered for "enrollment level" claims, then the district's headline figures (3,085 → 2,744 total; 1,401 → 1,080 elementary) are present with source citations
2. Given the catalog, when inspected, then every claim has a non-empty source document and location field
3. Given the catalog, when filtered by evidence status, then at least one claim is marked "unpublished" (enrollment projections are known to be absent)
4. Given the catalog, when consumed by the gap analysis pipeline, then it is parseable as structured data without manual transformation
5. Given the catalog, when reviewed by a human, then claim extraction is faithful to source language (no editorializing in the claim text field)

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

- Enrollment-related claims only (not all budget claims)
- Sources limited to existing evidence pools — no new data acquisition
- Preliminary evidence status, not deep analysis (that's EPIC-023)
- Claims from public testimony are in scope if captured in meeting transcripts

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-30 | — | Decomposed from EPIC-022 |
| Active | 2026-03-30 | -- | Operator approved; ready for implementation |
