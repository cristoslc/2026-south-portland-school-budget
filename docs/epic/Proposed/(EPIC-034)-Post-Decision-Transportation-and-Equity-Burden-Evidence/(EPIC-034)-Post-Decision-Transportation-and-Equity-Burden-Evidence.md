---
title: "Post-Decision Transportation and Equity Burden Evidence"
artifact: EPIC-034
track: container
status: Proposed
author: cristos
created: 2026-04-03
last-updated: 2026-04-03
parent-vision: VISION-001
parent-initiative: INITIATIVE-006
priority-weight: high
success-criteria:
  - The adopted reconfiguration has a documented transport burden baseline grounded in the repo's modeled walk and drive distance matrices
  - `student_blocks.json` is documented as a reusable data contract with reconciled totals, known caveats, and downstream handling rules
  - Block and neighborhood burden outputs identify where walkability loss, reassignment volume, and long-tail drive risk concentrate
  - An equity overlay shows whether modeled burden clusters in less-advantaged geographies, with limits stated clearly
  - Brief-ready tables, maps, and claims are published in forms that advocacy and site outputs can reuse without re-running the analysis manually
  - A claim-audit memo separates direct findings from inference and documents likely attacks on the methodology
depends-on-artifacts:
  - EPIC-031
  - EPIC-032
  - SPEC-065
  - SPEC-066
addresses:
  - JOURNEY-001.PP-03
  - JOURNEY-002.PP-03
evidence-pool: sopo-redistricting-tool
---

# Post-Decision Transportation and Equity Burden Evidence

## Goal / Objective

The closure vote is over. The open question is burden. This epic shows what the adopted plan does, where burden lands, and how to describe it with evidence.

The epic uses the repo's walk and drive model. It uses block weights, road distances, and current outputs to show walk loss, reassignment burden, long trips, and where harm clusters. It then adds an equity layer by place and income proxy.

## Desired Outcomes

Post-decision transport analysis becomes concrete. The project can say what the model shows, who is hit, and where burden clusters.

The output must serve three uses. It should sharpen advocacy. It should feed the site and briefs. It should mark what is modeled and what is observed.

## Progress

<!-- Auto-populated from session digests. See progress.md for full log. -->

## Scope Boundaries

**In scope:**
- Post-decision burden analysis for the adopted plan
- Documentation of `student_blocks.json` as a weighted block input contract
- Use of the repo's walk and drive matrices in downstream outputs
- Block, neighborhood, and school burden metrics
- Equity overlays using geography and public socioeconomic proxies
- Brief-ready tables, maps, and claim language
- A claim audit with findings, inference, and caveats

**Out of scope:**
- Re-running the school closure decision itself
- Recommending a new closure option
- Route-level bus scheduling or exact ride-time simulation
- Individual-level demographic inference from protected student records
- Replacing EPIC-031 or EPIC-032; this epic extends them into post-decision evidence

## Child Specs

| Artifact | Title | Status |
|----------|-------|--------|
| [SPEC-076](../../../spec/Proposed/(SPEC-076)-Student-Blocks-Contract-and-Model-Integration/(SPEC-076)-Student-Blocks-Contract-and-Model-Integration.md) | Student Blocks Contract and Model Integration | Proposed |
| [SPEC-077](../../../spec/Proposed/(SPEC-077)-Modeled-Walkability-and-Drive-Burden-Baseline/(SPEC-077)-Modeled-Walkability-and-Drive-Burden-Baseline.md) | Modeled Walkability and Drive Burden Baseline | Proposed |
| [SPEC-078](../../../spec/Proposed/(SPEC-078)-Equity-Overlay-on-Modeled-Burden/(SPEC-078)-Equity-Overlay-on-Modeled-Burden.md) | Equity Overlay on Modeled Burden | Proposed |
| [SPEC-079](../../../spec/Proposed/(SPEC-079)-Brief-Ready-Transportation-and-Equity-Evidence-Pack/(SPEC-079)-Brief-Ready-Transportation-and-Equity-Evidence-Pack.md) | Brief-Ready Transportation and Equity Evidence Pack | Proposed |
| [SPEC-080](../../../spec/Proposed/(SPEC-080)-Transportation-and-Equity-Claim-Audit/(SPEC-080)-Transportation-and-Equity-Claim-Audit.md) | Transportation and Equity Claim Audit | Proposed |

## Key Dependencies

- [EPIC-031](../../Active/(EPIC-031)-Configuration-Transport-Modeling-V1/(EPIC-031)-Configuration-Transport-Modeling-V1.md) for the modeled transport substrate and scenario outputs
- [EPIC-032](../../Active/(EPIC-032)-Fiscal-Exposure-Family-Logistics-Briefs/(EPIC-032)-Fiscal-Exposure-Family-Logistics-Briefs.md) for downstream brief framing and publication patterns
- [SPEC-065](../../../spec/Active/(SPEC-065)-Transport-Configuration-Comparison/(SPEC-065)-Transport-Configuration-Comparison.md) for the existing comparison deliverable and limits statement
- [docs/troves/sopo-redistricting-tool](/Users/cristos/Documents/projects/south-portland-school-budget-FY27/.claude/worktrees/epic-034-transport-equity-evidence/docs/troves/sopo-redistricting-tool/synthesis.md) for the ingested repo and source notes
- Publicly available equity overlays such as Census-based socioeconomic indicators and neighborhood geography

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-04-03 | — | Created to convert the repo's model into post-decision transport and equity evidence |
