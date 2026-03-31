# Synthesis: South Portland Redistricting Tool

## Key Findings

The Data4Good redistricting tool (by Adam Tishok, a South Portland parent) models four elementary school closure scenarios, each removing one school (Brown, Dyer, Kaler, or Small) and redistributing students across the remaining buildings. Skillin (capacity 380) cannot be closed because the other four schools lack combined capacity — total K-4 enrollment is 1,013 vs. remaining capacity of 1,020.

### Algorithm design (from source repo)

The zone assignment uses a **three-stage algorithm** (`src/assignment.py`):

1. **Capacity-bounded Voronoi flood-fill** — each school gets a seed block (nearest uncontested centroid), then grows outward by drive distance priority, stopping at proportional capacity targets.
2. **Hard capacity enforcement** — over-capacity schools shed marginal blocks (farthest first) to under-capacity neighbors, preferring contiguity-preserving moves.
3. **Bussed community cohesion smoothing** — keeps non-walkable neighbors together in the same zone.

Real road network distances come from OSMnx (OpenStreetMap), not straight-line calculations. The 0.75-mile walkability threshold accounts for actual sidewalk/road paths — highways and rail lines correctly block walking routes.

### Scenario rankings (from `scenario_summary.csv`)

| Rank | Scenario | Capacity OK | % Walkable | Avg Drive | Max Drive |
|------|----------|:-----------:|:----------:|:---------:|:---------:|
| 1 (tied) | Close Dyer | Yes | 44.2% | 1.08 mi | 4.96 mi |
| 1 (tied) | Close Kaler | Yes | 44.4% | 1.08 mi | 4.96 mi |
| 3 | Close Brown | Yes | 40.9% | 1.13 mi | 2.98 mi |
| 4 | Close Small | Yes | 39.5% | 1.18 mi | 3.15 mi |

The composite ranking uses drive distance, walkability, and capacity overflow. **Close Dyer and Close Kaler tie at #1** by composite score, though the webapp shows different "% change schools" figures (34% vs 27%) because the webapp applies PreK overhead differently than the raw model.

### Enrollment data (from `src/config.py`)

Per-grade enrollment as of March 2026:

| School | PreK | K | 1 | 2 | 3 | 4 | Total K-4 |
|--------|------|---|---|---|---|---|-----------|
| Brown | 0 | 29 | 44 | 46 | 38 | 37 | 194 |
| Dyer | 29 | 35 | 28 | 39 | 25 | 39 | 166 |
| Kaler | 29 | 26 | 33 | 30 | 26 | 20 | 135 |
| Small | 0 | 33 | 39 | 39 | 42 | 46 | 199 |
| Skillin | 0 | 68 | 56 | 64 | 58 | 73 | 319 |
| **Total** | **58** | **191** | **200** | **218** | **189** | **215** | **1,013** |

PreK is a pilot at Dyer and Kaler only (29 each). The model treats PreK as pre-assigned capacity overhead, not subject to geographic zone optimization.

### Grade center configurations

The repo also models grade-center reconfigurations (`RECONFIG_SCENARIOS` in config.py):

| Closure | PreK-1 Centers | Grades 2-4 Centers |
|---------|----------------|-------------------|
| Brown closed | Dyer, Kaler | Small, Skillin |
| Kaler closed | Dyer, Small | Brown, Skillin |
| Dyer closed | Kaler, Small | Brown, Skillin |
| Small closed | Dyer, Kaler | Brown, Skillin |

### Webapp features

The React/Vite webapp allows interactive zone editing — click any census block to reassign it, with enrollment stats updating live. Users can export modified zones as GeoJSON and upload others' zone files for comparison.

## Points of Agreement (across sources)

- Skillin cannot be a closure candidate — remaining capacity (1,020) barely covers enrollment (1,013)
- Census 2020 population data is the enrollment basis (317 blocks), not actual enrollment rolls by address
- 0.75 miles is the walkability threshold, using real road network distances
- Zone boundaries are algorithmically generated via flood-fill, not hand-drawn
- PreK pilot sites (Dyer and Kaler at 29 students each) affect capacity math
- All four scenarios are capacity-feasible, but none produce fully contiguous zones

## Points of Disagreement (webapp vs raw model)

- The webapp shows "27% change schools" for Close Kaler vs "34% change schools" for Close Dyer, but the raw model's composite ranking ties them — the difference comes from how PreK overhead and the interactive display layer handle reassignment counts
- The webapp's per-school enrollment figures (e.g., "347/380 enrolled" for Skillin) differ slightly from the model's computed assignments (374 students) due to PreK overhead allocation

## Gaps

- **No contiguous zones** — all scenarios produce non-contiguous zones (`all_zones_contiguous: false`), meaning some blocks are geographic islands within another school's zone
- No modeling of Full PreK expansion captured in detail (current pilot only in the data we extracted)
- No cost analysis (operating costs, transportation costs, facility maintenance)
- No demographic or equity analysis (income, race, special needs distribution)
- No timeline or phasing information for any closure scenario
- Census 2020 basis is now 6 years old — population shifts since then are unaccounted for
- No comparison against the school department's own 9 reconfiguration options presented at the March 2026 budget workshop
