---
title: "Building-Level Data Feasibility"
artifact: SPIKE-009
track: container
status: Complete
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
question: "Can we obtain building-level enrollment, capacity, and demographic data sufficient for per-school projections and functional capacity analysis?"
gate: "Pre-stretch-goal"
risks-addressed:
  - "Stretch goals (building-level projections, capacity analysis) may be infeasible due to data unavailability"
evidence-pool: ""
---

# Building-Level Data Feasibility

## Summary

**Conditional Go.** Building-level enrollment projections are feasible using publicly available data: NCES CCD provides 12+ years of school-level enrollment, and the sopo-data4good redistricting tool demonstrates a working census block → school zone overlay with 317 blocks. Rated building capacity is available (Brown 260, Dyer 240, Small 280, Skillin 380, Kaler 240 = 1,400 total). Full functional capacity analysis (accounting for SPED/ELL/behavioral space needs) requires a FOAA request to the district, viable within 3-4 weeks. Recommended next step: proceed with building-level projections using public data; file FOAA in parallel for functional capacity detail.

## Question

Can we obtain building-level enrollment, capacity, and demographic data sufficient for per-school projections and functional capacity analysis? Specifically:

1. Does Maine DOE publish enrollment data at the school level (not just district level)?
2. Can building functional capacity be determined from public sources (room counts, room types, space allocations for SPED/ELL/behavioral programs)?
3. Are census block demographic overlays with school catchment zone boundaries feasible using public data?
4. Would a FOAA request to the district for building-level data be viable within the project timeline?

## Go / No-Go Criteria

**Go (building-level projections feasible):**
- School-level enrollment data available from DOE for 5+ years
- At least one method for determining building functional capacity identified (public source OR viable FOAA)
- Census block overlay approach validated with available geographic boundary data

**Conditional (partial feasibility):**
- School-level enrollment available but capacity data requires FOAA with uncertain timeline
- Census block data available but catchment boundaries are not publicly documented

**No-Go (defer stretch goals):**
- School-level enrollment not available from public sources
- No viable path to capacity data within project timeline
- Geographic boundary data insufficient for census block overlay

## Pivot Recommendation

If No-Go: focus EPIC-024 exclusively on district-level projections. Document the building-level gap as a known limitation and recommend it as a follow-up initiative contingent on FOAA response or future data releases.

If Conditional: proceed with the feasible components (e.g., school-level enrollment projections without capacity analysis). Scope the stretch goals to match available data.

## Findings

### Q1: School-level enrollment from DOE/NCES

**Available.** NCES Common Core of Data provides school-level enrollment via the ELSI Table Generator. Confirmed 7 South Portland schools with current enrollment:

| School | NCES ID | Grades | 2024-25 Enrollment |
|--------|---------|--------|--------------------|
| Dora L Small Elementary | 231233000575 | KG-4 | 193 |
| Dyer Elementary | 231233000578 | PK-4 | 194 |
| Frank I Brown Elementary | 231233000586 | KG-4 | 213 |
| James Otis Kaler Elementary | 231233000716 | PK-4 | 179 |
| South Portland High School | 231233000585 | 9-12 | 928 |
| South Portland Middle School | 231233023206 | 5-8 | 807 |
| Waldo T Skillin Elementary | 231233000033 | KG-4 | 302 |

Multi-year school-level data is available through ELSI going back to 2013-14 or earlier. **This exceeds the 5+ year threshold.**

### Q2: Building functional capacity

**Partially available from public sources.** The sopo-data4good redistricting tool (`docs/troves/sopo-redistricting-tool`) contains capacity estimates used for modeling:

| School | Capacity (seats) |
|--------|-----------------|
| Brown | 260 |
| Dyer | 240 |
| Small | 280 |
| Skillin | 380 |
| Kaler | 240 |
| **Total** | **1,400** |

Source: `sopo-data4good/src/config.py` — capacity values appear to be derived from district presentations (March 2026 board workshop). These are *rated capacity* figures, not *functional capacity* (which accounts for rooms used for SPED, ELL, behavioral programs, offices, etc.).

The district presented class size data at the March 2 workshop showing room-by-room class sections per school (claim EC-035 in the enrollment catalog), which provides indirect capacity evidence. However, true functional capacity analysis (room counts, room type allocations, sq ft per student) is **not publicly available** and would require FOAA.

### Q3: Census block demographic overlay

**Feasible with existing data.** Three data sources converge:

1. **Census block population data**: US Census 2020 provides block-level population by age group. The sopo-data4good tool already uses this — its `Polygons.geojson` contains 317 census blocks with population counts, and `convert_addresses.py` estimates per-block student counts.

2. **School catchment boundaries**: ZipDataMaps publishes South Portland elementary attendance zones. The sopo-data4good tool has implemented catchment zone assignment algorithms with the geographic data already assembled.

3. **Maine GIS data**: Maine Office of GIS provides School Administrative District shapefiles through Maine GeoLibrary.

The sopo-data4good tool demonstrates that census block → school zone overlay is not just feasible but already implemented as working software. The main limitation is that census population data is from 2020 and student counts are estimates (not actual enrollment by address).

### Q4: FOAA viability

**Viable within project timeline.** Maine FOAA requires:
- 5 working day acknowledgment
- "Reasonable time" for production (typically 10-30 days for straightforward requests)
- Charges may apply at $25/hour after first 2 hours

A targeted request for building capacity reports, facility assessments, and room-use inventories would likely be fulfilled within 3-4 weeks. The 1-3 month project timeline accommodates this.

### Assessment Against Go/No-Go Criteria

| Criterion | Status | Evidence |
|-----------|--------|----------|
| School-level enrollment for 5+ years | **Met** | NCES CCD via ELSI, 12+ years available |
| Building capacity method identified | **Partially met** | Rated capacity available via redistricting tool; functional capacity requires FOAA |
| Census block overlay validated | **Met** | sopo-data4good tool demonstrates working implementation with 317 census blocks |

**Verdict: CONDITIONAL** — building-level enrollment projections are feasible with publicly available data. Full functional capacity analysis (accounting for SPED/ELL/behavioral space needs) requires FOAA. Recommend proceeding with the publicly available data while filing a targeted FOAA request in parallel.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-30 | — | Gates EPIC-024 stretch goals; decomposed from EPIC-022 |
| Active | 2026-03-30 | -- | Operator approved |
| Complete | 2026-03-31 | -- | Conditional Go — building-level projections feasible with public data; FOAA needed for functional capacity |
