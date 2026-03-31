---
title: "Enrollment Claims Catalog"
artifact: SPEC-051
track: implementable
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
type: feature
parent-epic: EPIC-026
linked-artifacts:
  - INITIATIVE-005
  - EPIC-027
depends-on-artifacts: []
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Enrollment Claims Catalog

## Problem Statement

The gap analysis (EPIC-027) needs a systematic inventory of every enrollment-related claim and assumption the district has made during the FY27 budget process. These claims are scattered across meeting transcripts, presentations, and budget documents in the existing evidence pools. They need to be extracted, cataloged, and tagged for gap analysis.

## Desired Outcomes

Every enrollment claim embedded in the closure recommendation is identified and structured, ready for SPEC-056 (gap analysis) to assess each as supported, unsupported, or unpublished. The catalog itself becomes a reference document — a timestamped record of what was claimed, when, by whom, and in what context.

## External Behavior

**Inputs:** Existing evidence pools:
- `docs/troves/fy27-budget-documents/` (12 sources)
- `docs/troves/school-board-budget-meetings/` (4 transcripts)
- `docs/troves/city-council-meetings-2026/` (7 transcripts)

**Outputs:** Structured catalog at `docs/troves/enrollment-claims/` containing:
- `claims.yaml` or `claims.json` — structured data with fields: claim_id, claim_text, source_file, source_line, speaker (if identifiable), date, category (enrollment_total | grade_level | demographic | projection | staffing_ratio | capacity), evidence_status (pending assessment)
- `synthesis.md` — narrative summary of claim patterns, contradictions, and evolution over time
- `trove.yaml` manifest

**Constraints:**
- Every claim must have a source citation (file + line number or timestamp)
- Claims should capture the exact language used, not paraphrases
- Include non-claims: questions raised in public comment that received no answer (these are gaps by definition)

## Acceptance Criteria

- Given the three evidence pools, when the catalog is complete, then at least every enrollment figure cited in the December 2025 workshop, February presentations, and March board meetings is captured
- Given the catalog, when filtered by category, then enrollment totals, demographic shifts, and staffing ratios are separately addressable
- Given public comment questions, when cataloged, then unanswered enrollment questions are tagged as such with the meeting date and approximate timestamp

## Scope & Constraints

**In scope:** Claim extraction and structuring from existing evidence pools.
**Out of scope:** Assessing claims as supported/unsupported (that's SPEC-056). Acquiring new data (that's SPEC-048/049/050).

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-026 |
