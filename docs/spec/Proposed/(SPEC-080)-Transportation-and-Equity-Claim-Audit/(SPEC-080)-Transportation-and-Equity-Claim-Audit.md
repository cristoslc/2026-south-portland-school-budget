---
title: "Transportation and Equity Claim Audit"
artifact: SPEC-080
track: implementable
status: Proposed
author: cristos
created: 2026-04-03
last-updated: 2026-04-03
priority-weight: high
type: feature
parent-epic: EPIC-034
parent-initiative: ""
linked-artifacts:
  - INITIATIVE-006
  - EPIC-034
depends-on-artifacts:
  - SPEC-077
  - SPEC-078
  - SPEC-079
addresses:
evidence-pool: sopo-redistricting-tool
source-issue: ""
swain-do: required
---

# Transportation and Equity Claim Audit

## Problem Statement

Post-decision transport and equity work will draw scrutiny. The project needs an audit that separates direct findings from inference, marks weak points in the method, and gives later briefs language they can defend.

## Desired Outcomes

The project can say what the model shows, what it only suggests, and where critics have a fair point. That makes public analysis harder to dismiss and less likely to overreach.

## External Behavior

**Inputs:**
- Burden outputs from SPEC-077
- Equity outputs from SPEC-078
- Evidence pack outputs from SPEC-079

**Outputs:**
- A claim audit memo
- Claim tiers such as direct finding, model-based inference, and unsupported or too-weak claim
- A counterargument section listing likely critiques and the right project response

**Constraints:**
- Must not collapse caveats into fine print
- Must preserve useful claims instead of sanding everything down to generic uncertainty
- Must be written for reuse in briefs, interviews, and rebuttal documents

## Acceptance Criteria

- Given the evidence pack, when the audit is complete, then each major public-facing claim is labeled by strength and method type
- Given likely critiques, when the counterargument section is read, then the project response is concrete and direct
- Given a claim that is too weak, when the audit runs, then that claim is either downgraded or removed from the reusable set
- Given downstream brief authors, when they use the audit, then they can tell what to lead with and what to hedge

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

In scope: claim strength, caveats, attack surfaces, rebuttal framing.
Out of scope: producing new transport or equity metrics.

## Implementation Approach

Treat the audit as part of the evidence product. Build a short, reusable structure that later deliverables can quote when challenged on method or certainty.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-04-03 | — | Initial creation |
