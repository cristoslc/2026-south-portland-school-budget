# South Portland Elementary School Redistricting Model

A reproducible geospatial model for analyzing school boundary scenarios in South Portland, Maine.

## What This Does

Models four closure scenarios (close Brown / Dyer / Small / Kaler) and optimizes the remaining school zone boundaries to:
1. **Respect hard capacity constraints** — no school exceeds its enrollment cap
2. **Maximize community continuity** — contiguous zones; bussed neighbors go together
3. **Minimize travel distance** — walkability and drive time factored into assignments

## How It Works

**Three-stage assignment algorithm:**
- **Stage 1** — Capacity-bounded Voronoi flood-fill from guaranteed seed blocks
- **Stage 2** — Hard capacity enforcement with tiered contiguity-preference moves
- **Stage 3** — Bussed community cohesion smoothing (keeps non-walkable neighbors together)

Uses OSM road networks (via OSMnx) for real walk/drive distance matrices.

## Schools

| School | Capacity | Coordinates |
|--------|----------|-------------|
| Brown  | 260 | 43.6347, -70.2489 |
| Dyer   | 240 | 43.6219, -70.2749 |
| Small  | 280 | 43.6413, -70.2339 |
| Skillin | 380 | 43.6260, -70.3054 |
| Kaler  | 240 | 43.6287, -70.2688 |

*Note: Closing Skillin is excluded — remaining four schools (capacity 1,020) cannot absorb all 1,074 students.*

## Quick Start

```bash
pip install geopandas osmnx folium networkx shapely pandas numpy
python3 run.py
```

Outputs saved to `outputs/`:
- `*_map.html` — Interactive folium maps (open in browser)
- `*_boundaries.geojson` — Zone boundary polygons
- `*_block_assignments.csv` — Per-block assignments with walk/drive distances
- `*_metrics.json` — School utilization, walkability %, avg drive times
- `scenario_summary.csv` — Ranked comparison of all scenarios

## Results Summary

| Scenario | Capacity OK | Walkable Students | Avg Drive |
|----------|:-----------:|:-----------------:|:---------:|
| **Kaler Closed** | ✓ | 692 | 0.87 mi |
| **Brown Closed** | ✓ | 567 | 1.03 mi |
| Dyer Closed | ~1 student over | 653 | 0.91 mi |
| Small Closed | ~0.1 over | 561 | 1.20 mi |

## Data

`Polygons.geojson` — 317 census blocks (2020 Census, South Portland, ME) with population counts used to estimate student distribution.
