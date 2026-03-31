---
title: "Enrollment Gap Analysis Document"
artifact: SPEC-056
track: implementable
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
type: feature
parent-epic: EPIC-027
linked-artifacts:
  - INITIATIVE-005
  - SPEC-051
depends-on-artifacts:
  - SPEC-048
  - SPEC-051
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Enrollment Gap Analysis Document

## Problem Statement

The district is making a permanent school closure decision based on enrollment assumptions that have not been independently verified. The claims catalog (SPEC-051) identifies what was claimed; this spec assesses each claim against the independently acquired data (SPEC-048/049/050) and documents the gaps.

## Desired Outcomes

A rigorous, source-cited gap analysis that any resident can read and understand: what the district claimed, whether the evidence supports it, and what questions remain unanswered. This document is the analytical foundation for the Phase 1 persona briefs (SPEC-057).

## External Behavior

**Inputs:**
- Enrollment claims catalog (SPEC-051 output)
- Maine DOE enrollment data (SPEC-048 output)
- DHHS birth records (SPEC-049 output)
- Housing permit data (SPEC-050 output)

**Outputs:** Gap analysis document at `docs/analysis/enrollment-gap-analysis.md` containing:
- For each claim category: claim text, source citation, assessment (supported | partially supported | unsupported | unpublished), evidence basis, severity (critical | important | informational)
- Summary of critical gaps — assumptions that are load-bearing for the closure decision but lack evidence
- Summary of contradictions — claims that conflict with independently acquired data
- Unanswered questions — public comment questions that received no response, mapped to what data would answer them

**Constraints:**
- Assessments must be factual and evidence-based, not editorial
- "Unsupported" means no public evidence was found, not that the claim is false
- "Unpublished" means the district may have internal data but hasn't shared it

## Acceptance Criteria

- Given the claims catalog and independent data, when the gap analysis is complete, then every claim has an assessment with cited evidence
- Given the assessments, when filtered to "critical" severity, then the load-bearing assumptions for the closure decision are identified
- Given the gap analysis, when read by a non-expert, then the distinction between "unsupported" and "false" is clear

## Scope & Constraints

**In scope:** Assessment of claims against data. Gap identification.
**Out of scope:** Independent projection (that's SPEC-058). Policy recommendations.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-027 |
