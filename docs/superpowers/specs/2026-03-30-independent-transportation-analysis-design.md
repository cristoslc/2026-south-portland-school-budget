# Independent Transportation Analysis — Initiative Design

## Context

The South Portland School Board is choosing between elementary reconfiguration options (Option A: primary/intermediate grade-band split; Option B: full K-4 redistricting) following the proposed closure of Kaler Elementary. The district has acknowledged that transportation modeling is needed — a transportation consultant was budgeted — but no estimates have been published. The Director of Operations confirmed on the record that no modeling exists and none will be done before the board votes. Meanwhile, the SEA bargaining unit (which covers transportation workers) faces a 14% staffing reduction — the highest percentage cut of any unit — concurrent with a reconfiguration that may require route expansion.

Community testimony documents 45-minute bus rides under the current configuration, parents with one car facing impossible split-building logistics, 90% of surveyed parents worried about busing complications, and 57% citing disruption to before/after care. McKinney-Vento eligible students (1% → 10% of the student body) have federal transportation rights that reconfiguration could trigger. None of this has been modeled.

## Intent

This initiative produces independent transportation impact estimates using publicly available data. It fills the analysis gap the district has not filled and costs the risks nobody is quantifying. The tone is rigorous and factual — let the numbers speak. Contributions from the district or board that would improve the analysis are welcome.

Phase 1 (V1): Compare three specific configurations on transport metrics.
Phase 2 (V2, stretch): Open the configuration space to optimization search.

## Position in Architecture

Soft dependency on INITIATIVE-005 (Independent Enrollment Study) — V1 uses current enrollment numbers, updates when independent projections become available.

Downstream of INITIATIVE-005, upstream of:
- INITIATIVE-001 (Budget Lever Analysis) — transport costs are an uncosted lever
- INITIATIVE-004 (Public Budget Site) — comparison data published to site

## Scope

**In scope:**
- Transport metric modeling for three configurations: Option A (2 primary Pre-K-1 / 2 intermediate 2-4), Option B (4 K-4 redistrict by proximity), Variant C (3 Pre-K-2 / 1 Grades 3-4) — all with Kaler closed
- Fiscal exposure: McKinney-Vento transport obligations, SPED door-to-door mandate costs, SEA staffing adequacy, before/after care cost gap, per-pupil transport cost benchmarking
- Family logistics: split-family counts per configuration, bell schedule feasibility and tier constraints, before/after care gap quantification
- Walk zone policy audit: current policy vs. state minimums vs. actual pedestrian infrastructure
- Per-persona briefs through interpretation pipeline
- Structured comparison data for downstream consumption

**Stretch goals (V2):**
- Configuration space optimization: search across feasible configurations for minimum transport burden
- Route distance estimation using catchment geometry
- Equity analysis of ride time distribution by neighborhood

**Out of scope:**
- Route-level optimization requiring student address data (FERPA)
- Actual ride time modeling (requires routing software + district data)
- Advocacy for or against any configuration

## Epic Decomposition

**EPIC A: Transportation Data Acquisition & Baseline** — Trove collection. Maine DOE per-pupil transport expenditure, peer district benchmarks, SEA contract/staffing data, walk zone policies, school locations and catchment boundaries, bell schedule data. Catalog every transportation-related claim, question, and non-answer from existing evidence pools.

**EPIC B: Configuration Transport Modeling (V1)** — (Depends on A) For each configuration: split-family counts, bell schedule tier requirements, McKinney-Vento exposure, SEA staffing adequacy, before/after care gap. Structured comparison output.

**EPIC C: Fiscal Exposure & Family Logistics Briefs** — (Depends on B) Per-persona briefs. Lead with fiscal exposure, ground in family logistics, frame with governance context. Factual tone.

**EPIC D (stretch): Configuration Space Optimization (V2)** — (Depends on B) Define transport burden metrics from V1, search feasible configurations for minimizers.

**SPIKE (under EPIC A): Walk Zone & Pedestrian Infrastructure Audit** — Time-boxed. Walk zone policy vs. state minimums vs. actual conditions (I-295, arterials, winter). Walker/rider reclassification under reconfiguration.

## Success Criteria

1. Every transportation-related claim and non-answer from the budget process cataloged with source citations
2. Three configurations compared on split-family count, McKinney-Vento exposure, SEA staffing adequacy, bell schedule feasibility, and before/after care gap
3. Fiscal exposure estimate produced for each configuration (order of magnitude, disclosed as such)
4. Per-persona briefs published to the site
5. Comparison data structured and consumable by INITIATIVE-001 and INITIATIVE-004
6. Known limitations and data gaps disclosed transparently; open invitation to the district to contribute refining data
7. V2 stretch: at least one alternative configuration identified that outperforms Options A and B on transport metrics
