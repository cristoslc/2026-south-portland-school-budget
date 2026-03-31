---
title: "Independent Transportation Analysis"
artifact: INITIATIVE-006
track: container
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
parent-vision:
  - VISION-001
priority-weight: high
success-criteria:
  - Every transportation-related claim and non-answer from the budget process cataloged with source citations
  - Three configurations compared on split-family count, McKinney-Vento exposure, SEA staffing adequacy, bell schedule feasibility, and before/after care gap
  - Fiscal exposure estimate produced for each configuration (order of magnitude, disclosed as such)
  - Per-persona briefs published to the site
  - Comparison data structured and consumable by INITIATIVE-001 and INITIATIVE-004
  - Known limitations and data gaps disclosed transparently with open invitation to district to contribute refining data
  - "V2 stretch: at least one alternative configuration identified that outperforms Options A and B on transport metrics"
depends-on-artifacts:
  - INITIATIVE-005
addresses:
  - JOURNEY-001.PP-03
  - JOURNEY-002.PP-03
evidence-pool: ""
linked-epics:
  - EPIC-030
  - EPIC-031
  - EPIC-032
  - EPIC-033
linked-artifacts:
  - INITIATIVE-001
  - INITIATIVE-003
  - INITIATIVE-004
  - INITIATIVE-005
  - SPIKE-010
---

# Independent Transportation Analysis

## Strategic Focus

Produce independent transportation impact estimates for the elementary reconfiguration options under consideration by the South Portland School Board. The district has acknowledged that transportation modeling is needed but has not published estimates in advance of the board's configuration vote. This initiative uses publicly available data to model the fiscal exposure, family logistics burden, and implementation requirements that transportation analysis would normally surface before an irreversible infrastructure decision. These estimates would benefit from district data on current routes, fleet contracts, and building capacity — contributions from the district or board are welcome and would improve the analysis.

V1 compares three specific configurations on transport metrics using current enrollment data. V2 (stretch) expands the configuration space to identify alternatives that minimize transport burden.

Soft dependency on [INITIATIVE-005](../(INITIATIVE-005)-Independent-Enrollment-Study/(INITIATIVE-005)-Independent-Enrollment-Study.md) (Independent Enrollment Study) — V1 uses current enrollment numbers, updates when independent projections become available.

## Desired Outcomes

Residents and board members can compare reconfiguration options on transportation metrics that the district has not published. Families with elementary-age children understand how each configuration affects their logistics — how many families would have children in two different buildings, what bell schedule constraints exist, where before/after care gaps emerge. The fiscal exposure of unfunded transportation obligations (McKinney-Vento rights, SPED mandates, route expansion against a 14% SEA staffing cut) is quantified at order-of-magnitude precision.

For each persona: Maria knows how many mornings she'd spend doing split-building drop-offs under each option. David has a dollar figure for the transportation costs missing from the budget. Rachel can compare what Option A means for her family's morning vs. what Variant C would mean. Linda has the implementation analysis the board should have had before voting. Tom can see the unfunded mandates buried in the closure decision.

## Scope Boundaries

**In scope:**
- Transport metric modeling for three configurations:
  - **Option A** (administration's recommendation): 2 primary (Pre-K-1) + 2 intermediate (2-4), Kaler closed
  - **Option B**: 4 buildings K-4, Kaler closed, redistrict by proximity
  - **Variant C**: 3 buildings Pre-K-2 + 1 building Grades 3-4, Kaler closed
- Fiscal exposure analysis: McKinney-Vento transport obligations triggered by displacement (10% of student body eligible), SPED door-to-door mandate costs, SEA staffing adequacy (14% cut concurrent with route expansion), before/after care cost gap, per-pupil transport cost benchmarking against peer districts
- Family logistics modeling: split-family counts per configuration, bell schedule feasibility and tier constraints, before/after care gap quantification
- Walk zone policy audit: current policy vs. state minimums vs. actual pedestrian infrastructure (I-295, arterials, winter conditions)
- Per-persona briefs through interpretation pipeline (interventionist framing — fiscal exposure leads, family logistics grounds it, governance context frames it)
- Structured comparison data consumable by [INITIATIVE-001](../(INITIATIVE-001)-Budget-Lever-Analysis/(INITIATIVE-001)-Budget-Lever-Analysis.md) and the site

**Stretch goals (V2):**
- Configuration space optimization: define transport burden metrics from V1, search across feasible configurations for minimizers
- Route distance estimation using catchment geometry and school locations (no student addresses)
- Equity analysis of ride time distribution by neighborhood

**Out of scope:**
- Route-level optimization requiring student address data (FERPA-protected)
- Actual ride time modeling (requires routing software + district data)
- Advocacy for or against any configuration — the deliverable is the missing analysis, not a recommendation

## Tracks

**Track 1 — V1 Comparison (3 configurations):** Data acquisition + transport modeling + persona briefs. Time-sensitive — most valuable before City Council budget adoption.

**Track 2 — V2 Optimization (stretch):** Configuration space search. Depends on V1 framework and findings. Scope TBD based on V1 learnings.

## Child Epics

| Artifact | Title | Status | Track |
|----------|-------|--------|-------|
| [EPIC-030](../../epic/Active/(EPIC-030)-Transportation-Data-Acquisition-Baseline/(EPIC-030)-Transportation-Data-Acquisition-Baseline.md) | Transportation Data Acquisition & Baseline | Active | Both |
| [EPIC-031](../../epic/Active/(EPIC-031)-Configuration-Transport-Modeling-V1/(EPIC-031)-Configuration-Transport-Modeling-V1.md) | Configuration Transport Modeling (V1) | Active | Track 1 |
| [EPIC-032](../../epic/Active/(EPIC-032)-Fiscal-Exposure-Family-Logistics-Briefs/(EPIC-032)-Fiscal-Exposure-Family-Logistics-Briefs.md) | Fiscal Exposure & Family Logistics Briefs | Active | Track 1 |
| [EPIC-033](../../epic/Proposed/(EPIC-033)-Configuration-Space-Optimization-V2/(EPIC-033)-Configuration-Space-Optimization-V2.md) | Configuration Space Optimization (V2) | Proposed | Track 2 |

## Small Work (Epic-less Specs)

_None currently._

## Research Spikes

| Artifact | Title | Status | Parent |
|----------|-------|--------|--------|
| [SPIKE-010](../../research/Active/(SPIKE-010)-Walk-Zone-Pedestrian-Infrastructure-Audit/(SPIKE-010)-Walk-Zone-Pedestrian-Infrastructure-Audit.md) | Walk Zone & Pedestrian Infrastructure Audit | Active | EPIC-030 |

## Key Dependencies

- **Evidence pools (existing):** fy27-budget-documents, school-board-budget-meetings, city-council-meetings-2026 — transportation claims and gaps already documented in synthesis
- **Data acquisition (needed):** Maine DOE per-pupil transport expenditure, peer district benchmarks, catchment zone boundaries, bell schedule data
- **Soft dependency:** [INITIATIVE-005](../(INITIATIVE-005)-Independent-Enrollment-Study/(INITIATIVE-005)-Independent-Enrollment-Study.md) (enrollment projections) — V1 uses current numbers, updates later
- **Infrastructure:** [INITIATIVE-003](../(INITIATIVE-003)-Interpretation-Pipeline/(INITIATIVE-003)-Interpretation-Pipeline.md) (interpretation pipeline) for persona briefs; [INITIATIVE-004](../(INITIATIVE-004)-Public-Budget-Site/(INITIATIVE-004)-Public-Budget-Site.md) (site) for publication
- **Downstream consumers:** [INITIATIVE-001](../(INITIATIVE-001)-Budget-Lever-Analysis/(INITIATIVE-001)-Budget-Lever-Analysis.md) (lever analysis — transport costs are an uncosted lever)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created from brainstorming session; user-requested |
