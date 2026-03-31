---
source-id: "sopo-data4good-repo"
title: "sopo-data4good — South Portland Elementary School Redistricting Model"
type: repository
url: "https://github.com/adamtishok-git/sopo-data4good"
fetched: 2026-03-31T02:22:00Z
hash: "63e360542b933593ab9af74c4aefe07883cb8f321defa64f8a7b0db00d5b6cbb"
selective: true
highlights:
  - "src/assignment.py"
  - "src/config.py"
  - "src/pipeline.py"
  - "outputs/scenario_summary.csv"
  - "webapp/src/App.jsx"
  - "webapp/src/components/ScenarioView.jsx"
---

# sopo-data4good — South Portland Elementary School Redistricting Model

**Author:** adamtishok-git (Adam Tishok)
**Created:** 2026-03-08
**Language:** Python (geospatial backend) + React/Vite (webapp frontend)
**License:** None specified
**Deployed at:** https://sopo-data4good.vercel.app/

## Overview

A reproducible geospatial model for analyzing school boundary scenarios in South Portland, Maine. Models four closure scenarios (Brown, Dyer, Small, Kaler) and optimizes remaining school zone boundaries. Skillin closure is excluded — remaining four schools (capacity 1,020) cannot absorb all 1,013 K-4 students.

## Architecture

### Python backend (`src/`)

- **config.py** — School locations, capacities, per-grade enrollment (March 2026), PreK pilot configuration, grade-center reconfiguration mappings
- **assignment.py** — Three-stage block-to-school assignment algorithm:
  1. Capacity-bounded Voronoi flood-fill from guaranteed seed blocks
  2. Hard capacity enforcement with tiered contiguity-preference moves
  3. Bussed community cohesion smoothing
- **network.py** — OSM road network loading via OSMnx for real walk/drive distance matrices
- **contiguity.py** — Zone contiguity checks (removal/addition preserves connectedness)
- **data_loader.py** — Census block loading, student estimation from population data
- **metrics.py** — Walkability, drive distance, capacity utilization calculations
- **pipeline.py** — Orchestrates all scenarios through assignment + metrics
- **visualization.py** — Folium map generation

### React webapp (`webapp/`)

- **App.jsx** — Main app with tab navigation across closure scenarios and viewing modes
- **ScenarioView.jsx** — Per-scenario map + stats panel with interactive zone editing
- **MapView.jsx** — Leaflet map with clickable census blocks for zone reassignment
- **StatsPanel.jsx** — Enrollment, walkability, drive distance stats per school
- **UploadTab.jsx** — GeoJSON upload for sharing custom zone configurations
- **AboutModal.jsx** — Methodology explanation

### Key data

- **Polygons.geojson** — 317 census blocks (2020 Census) with population counts (not ingested — 479KB)
- **outputs/scenario_summary.csv** — Ranked comparison of all scenarios
- **outputs/*_metrics.json** — Detailed per-school metrics for each scenario

## Selective ingestion

Large generated files excluded: HTML maps (~848KB each), boundary GeoJSON (~75KB each), block assignment CSVs (~19KB each), webapp data JSON (~498KB each), Polygons.geojson (479KB). All Python source, React source, metrics JSON, and scenario summary CSV are included.
