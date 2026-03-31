---
title: "School Locations & Catchment Data"
artifact: SPEC-055
track: implementable
status: Complete
author: cristos
created: 2026-03-30
last-updated: 2026-03-31
type: feature
parent-epic: EPIC-030
linked-artifacts:
  - INITIATIVE-006
  - SPIKE-009
  - SPIKE-010
depends-on-artifacts: []
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# School Locations & Catchment Data

## Problem Statement

The configuration transport modeling (EPIC-031) needs geographic data: where are the school buildings, what are the current catchment zone boundaries, and what does I-295 do to the transportation geography. This data is likely available from the district's redistricting tool evidence pool, city GIS, and public school information.

## Desired Outcomes

The project has geocoded school locations and documented catchment zone boundaries sufficient for rough route distance estimation and split-family geographic analysis.

## External Behavior

**Inputs:**
- School addresses (public information)
- Redistricting tool data from `docs/troves/sopo-redistricting-tool/`
- City of South Portland GIS data (if available)
- District website school boundary information

**Outputs:** Data files in `docs/troves/school-geography/` containing:
- `schools.json` — geocoded school locations (lat/lon, address, grades served, current enrollment)
- `catchment-zones.geojson` or narrative boundary descriptions if GIS data unavailable
- `geography-notes.md` — I-295 crossing analysis, major arterials, geographic constraints on bus routing
- Bell schedule data (current start/end times for each school, tier assignments)
- `trove.yaml` manifest

**Constraints:**
- Geocoding can use any free geocoding service or manual lookup
- Catchment zones may not be available as GIS polygons — narrative descriptions ("east of Broadway, north of Main St") are acceptable
- Bell schedule data may require extraction from district website or meeting documents

## Acceptance Criteria

- Given school addresses, when geocoded, then all 5 elementary schools + SPMS + SPHS have lat/lon coordinates
- Given catchment zone data, when documented, then the current attendance zones for all elementary schools are described with enough precision to estimate which neighborhoods feed which school
- Given bell schedule data, when documented, then current start/end times and bus tier assignments are captured
- Given I-295 geography, when analyzed, then the schools and neighborhoods separated by the interstate are identified

## Scope & Constraints

**In scope:** Location data, boundary documentation, bell schedule extraction.
**Out of scope:** Route optimization, ride time estimation, student address data.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-030 |
| Complete | 2026-03-31 | — | School locations and synthesis populated |
