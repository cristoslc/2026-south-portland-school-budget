---
title: "Transport Configuration Comparison"
artifact: SPEC-065
track: implementable
status: Complete
author: cristos
created: 2026-03-30
last-updated: 2026-03-31
type: feature
parent-epic: EPIC-031
linked-artifacts:
  - INITIATIVE-006
  - INITIATIVE-001
depends-on-artifacts:
  - SPEC-060
  - SPEC-061
  - SPEC-062
  - SPEC-063
  - SPEC-064
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Transport Configuration Comparison

## Problem Statement

The individual transport metrics (split families, McKinney-Vento, SEA staffing, bell schedules, care gaps) need to be assembled into a structured comparison that allows side-by-side evaluation of the three configurations. This is the capstone deliverable of EPIC-031 — the thing the persona briefs (EPIC-032) will translate into stakeholder-specific communication.

## Desired Outcomes

A single, structured comparison document and dataset that makes the transport tradeoffs between configurations visible and concrete. This is the "missing analysis" that the initiative set out to produce.

## External Behavior

**Inputs:** All EPIC-031 spec outputs (SPEC-060 through SPEC-064)

**Outputs:**
- `docs/analysis/transport-configuration-comparison.md` — narrative comparison with tables
- `data/transport-comparison.json` — structured data for site consumption (INITIATIVE-004)
- Summary comparison table:

| Metric | Option A | Option B | Variant C |
|--------|----------|----------|-----------|
| Split families | X | 0 | Y |
| McKinney-Vento exposure | $X-Y | $X-Y | $X-Y |
| SEA staffing gap | +/- N FTE | +/- N FTE | +/- N FTE |
| Bus tiers required | N | N | N |
| Before/after care gap (families) | N | 0 | N |
| Total fiscal exposure | $X-Y | $X-Y | $X-Y |

**Constraints:**
- All numbers presented as ranges, not point estimates
- Every number traced to its source spec
- Limitations section: what this comparison can and cannot tell you
- Open invitation to district to provide data that would refine these estimates

## Acceptance Criteria

- Given all five metric specs, when assembled, then the comparison table is complete for all three configurations
- Given the structured data output, when consumed by the site, then the comparison is renderable as a web page
- Given the limitations section, when read, then a skeptical reader understands what was estimated vs. measured and where the analysis could be wrong
- Given the fiscal exposure total, when compared to the $1.5-2.2M claimed savings from closure, then the net savings after transport costs is estimable

## Scope & Constraints

**In scope:** Assembly, comparison, structured output.
**Out of scope:** Recommendations. V2 optimization (EPIC-033). New analysis beyond what the input specs provide.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-031 |
| Complete | 2026-03-31 | — | Analysis implemented; see docs/analysis/ |
