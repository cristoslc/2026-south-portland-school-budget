# School Geography — Synthesis

**Trove:** school-geography
**Date:** 2026-03-31
**Linked spec:** SPEC-055

---

## Key Findings

### School Locations and Enrollment

South Portland operates 5 elementary schools, 1 middle school, and 1 high school. Elementary enrollment by building (2025-26, from redistricting tool data):

| School | Address | K-4 Enrollment | Capacity | Notes |
|--------|---------|:--------------:|:--------:|-------|
| Brown | 37 Highland Ave | 194 | — | No PreK |
| Dyer | 52 Alfred St | 166 (+29 PreK) | — | PreK pilot; roof $535K |
| Kaler | 165 S Kelsey St | 135 (+29 PreK) | — | PreK pilot; proposed closure; roof $302K |
| Small | 87 Thompson St | 199 | — | No PreK |
| Skillin | 180 Wescott Rd | 319 | 380 | Largest; most diverse; HVAC needs |
| **Total** | | **1,013** (+58 PreK) | | |

### Geographic Constraints

**I-295:** Bisects South Portland, creating a hard transportation boundary. West-side students are 100% bused. Some existing routes reach 45+ minutes.

**Walkability:** The Data4Good redistricting tool uses OpenStreetMap road network data with a 0.75-mile walkability threshold. Under any 4-school configuration, approximately 44% of students are within walking distance. This means ~56% require bus service.

### Redistricting Tool Findings

The citizen-built redistricting tool (Data4Good / Adam Tishok) models all closure scenarios using capacity-bounded Voronoi flood-fill with real road network distances. Key findings:

- **Skillin cannot be closed** — remaining 4 schools lack capacity to absorb (total K-4 enrollment 1,013 vs. remaining capacity 1,020, with no headroom)
- **Close Dyer and Close Kaler tie** on composite ranking (drive distance + walkability + capacity overflow)
- Average drive distance: ~1.08 miles for Dyer/Kaler closure scenarios
- Maximum drive distance: 4.96 miles (both scenarios)

### Bell Schedule Data

**Current elementary:** Not documented in evidence pools at school level. General knowledge: staggered start times to enable tiered bus service.

**Middle school:** Two staggered start times (7:55 and 8:45). Consolidation deferred to fall 2027 pending $25K DOT traffic study and 6-12 month permitting.

**High school:** Not documented in available sources.

**Gap:** School-level bell schedules (start time, end time, tier assignment) are needed for the bell schedule tier analysis (SPEC-063). These may be on the district website or in parent handbooks.

### Capacity Data Gap

Only Skillin's capacity (380) is documented. Building capacities for Brown, Dyer, Kaler, and Small are referenced in the reconfiguration presentations but not captured as specific numbers in the evidence pools. The redistricting tool uses capacity figures in its model (`src/config.py`) — these should be extracted.

## Data Sources

- School addresses: NCES CCD, district website
- Enrollment by grade: Data4Good redistricting tool (`src/config.py`), cross-validated against NCES CCD
- Walkability/drive distance: Data4Good redistricting tool (OSMnx road network analysis)
- Capital needs: FY27 budget documents evidence pool
- Bell schedules: School board meeting transcripts (partial)

## Gaps Requiring Additional Data

1. **Building capacities** for Brown, Dyer, Kaler, Small (extract from redistricting tool config)
2. **Bell schedules** by school (start time, end time, bus tier assignment)
3. **Catchment zone boundary definitions** (the redistricting tool generates zones algorithmically — current attendance zone boundaries may differ)
4. **I-295 crossing points** and safe pedestrian routes
5. **Geocoded coordinates** for each school (available via geocoding services)
