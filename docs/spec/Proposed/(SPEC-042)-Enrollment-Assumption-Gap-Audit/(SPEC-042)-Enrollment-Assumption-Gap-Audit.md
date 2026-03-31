---
title: "Enrollment Assumption Gap Audit"
artifact: SPEC-042
track: implementable
status: Proposed
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
priority-weight: high
type: ""
parent-epic: EPIC-023
linked-artifacts:
  - SPEC-040
depends-on-artifacts:
  - SPEC-039
  - SPEC-040
addresses:
  - JOURNEY-002.PP-03
  - JOURNEY-001.PP-03
evidence-pool: "fy27-budget-documents, school-board-budget-meetings"
source-issue: ""
swain-do: required
---

# Enrollment Assumption Gap Audit

## Problem Statement

The district is making a permanent closure decision based on enrollment assumptions that have never been systematically audited. The claims catalog (SPEC-040) identifies what the district has said; the DOE data (SPEC-039) provides the independent baseline. This spec bridges them: for each district enrollment claim, assess whether it is supported by evidence, contradicted by evidence, or rests on unpublished analysis that the public has never seen.

## Desired Outcomes

A structured gap analysis that makes the enrollment decision basis transparent and assessable. Each assumption gets a verdict with rationale. The gaps aren't just identified — they're contextualized: why does this gap matter for the closure decision? What would a responsible decision-maker need to see here? This becomes the analytical backbone for Phase 1 persona briefs.

## External Behavior

**Inputs:**
- Claims catalog from SPEC-040 (structured JSON/CSV)
- DOE enrollment data from SPEC-039 (structured trove)
- Existing evidence pool documents (budget presentations, board materials)

**Outputs:**
- Gap analysis document (markdown) with structured assessment per claim
- Per-claim fields: claim text, source, assessment (supported/unsupported/unpublished), evidence citation, gap significance (why this matters for the closure decision), what a responsible process would require
- Summary: count of supported/unsupported/unpublished claims, most significant gaps
- Structured data export (JSON) for consumption by persona brief generation

**Constraints:**
- Assessments must be evidence-based — "unsupported" means evidence contradicts the claim, "unpublished" means no evidence exists either way
- The audit is analytical, not advocacy — let the gaps speak for themselves
- Scope limited to enrollment assumptions, not all budget assumptions

## Acceptance Criteria

1. Given the gap analysis, when filtered for "unpublished" assessments, then the absence of district enrollment projections is documented as the most significant gap
2. Given each claim in the catalog, when looked up in the gap analysis, then it has a non-empty assessment, evidence citation, and significance statement
3. Given the gap analysis, when the district's headline decline figure (3,085 → 2,744) is assessed, then the DOE data either confirms or reveals discrepancy with specific year-by-year comparison
4. Given the gap analysis JSON export, when consumed by the brief generation pipeline, then per-persona gap summaries can be generated without manual intervention
5. Given the analysis, when reviewed, then no claim is assessed as "unsupported" without specific contradicting evidence cited

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

- Only enrollment-related assumptions (budget lever assumptions are INITIATIVE-001's domain)
- Assessment is binary + unpublished — not a confidence score
- This spec produces the analytical foundation; persona framing is SPEC-043's scope
- Must be completable with publicly available data — no reliance on district cooperation

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-30 | — | Decomposed from EPIC-023 |
