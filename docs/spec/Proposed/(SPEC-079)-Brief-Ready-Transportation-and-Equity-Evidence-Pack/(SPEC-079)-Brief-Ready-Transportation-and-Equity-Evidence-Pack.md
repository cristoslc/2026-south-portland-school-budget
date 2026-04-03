---
title: "Brief-Ready Transportation and Equity Evidence Pack"
artifact: SPEC-079
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
  - EPIC-032
  - SPEC-066
depends-on-artifacts:
  - SPEC-077
  - SPEC-078
addresses:
evidence-pool: sopo-redistricting-tool
source-issue: ""
swain-do: required
---

# Brief-Ready Transportation and Equity Evidence Pack

## Problem Statement

Even good analysis fails if each brief must reinterpret it from scratch. The project needs a reusable pack with tables, maps, short claims, and source notes that later outputs can use directly.

## Desired Outcomes

The evidence becomes portable. Advocacy, rebuttal, parent explainers, and site pages all pull from the same pack.

## External Behavior

**Inputs:**
- Burden baseline outputs from SPEC-077
- Equity outputs from SPEC-078
- Existing persona and site publication patterns from EPIC-032 and SPEC-070

**Outputs:**
- Brief-ready tables and maps
- A short set of reusable claims with citations and caveats
- Publication-friendly markdown or JSON outputs that later briefs and pages can consume

**Constraints:**
- Must optimize for reuse, not for one-off polish
- Must keep every claim attached to a sourceable metric and caveat
- Must be usable by both human-written and generated brief workflows

## Acceptance Criteria

- Given the post-decision outputs, when the evidence pack is produced, then it contains reusable tables, maps, and claim snippets for transport and equity findings
- Given a downstream briefing workflow, when it consumes the pack, then it can reuse the outputs without manual recomputation
- Given each reusable claim, when a reader follows its citation, then they can find the metric source and its caveat
- Given the pack, when site-oriented content consumes it, then the outputs are shaped for direct publication or light transformation

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

In scope: packaging, reusable claims, publication-ready evidence artifacts.
Out of scope: persona-specific narrative writing or site component implementation.

## Implementation Approach

Start with the smallest set of reusable artifacts that answer the core post-decision questions. Prefer a stable pack format. Keep claim language short and sourceable.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-04-03 | — | Initial creation |
