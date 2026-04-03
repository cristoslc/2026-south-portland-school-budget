---
source-id: "sopo-data4good-repo"
title: "sopo-data4good — South Portland Elementary School Redistricting Model"
type: repository
url: "https://github.com/adamtishok-git/sopo-data4good"
fetched: 2026-03-31T02:22:00Z
hash: "755fea2bf7ffc15ee2f815c653fe1a09503ca4b9c9f7ef5f86a63c4c475a6ad3"
selective: true
highlights:
  - "src/assignment.py"
  - "src/config.py"
  - "src/pipeline.py"
  - "data/student_blocks.json"
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

A map model for South Portland school zones. It covers four closure cases: Brown, Dyer, Small, and Kaler. Skillin stays open. The other four schools have 1,020 seats for 1,013 K-4 students.

## Architecture

### Python backend (`src/`)

- **config.py** — Schools, seats, grades, PreK, and zone maps
- **assignment.py** — Three-step block assignment:
  1. Start at seed blocks
  2. Fill seats
  3. Keep nearby blocks together
- **network.py** — Road data from OSMnx
- **contiguity.py** — Checks that zones stay connected
- **data_loader.py** — Census blocks and student estimates
- **metrics.py** — Walk, drive, and seat stats
- **pipeline.py** — Runs all cases
- **visualization.py** — Map output

### React webapp (`webapp/`)

- **App.jsx** — Main app with tabs
- **ScenarioView.jsx** — Map and stats with live edits
- **MapView.jsx** — Clickable census blocks
- **StatsPanel.jsx** — School stats
- **UploadTab.jsx** — GeoJSON upload
- **AboutModal.jsx** — Method note

### Key data

- **Polygons.geojson** — 317 census blocks (2020 Census) with population counts (not ingested — 479KB)
- **data/student_blocks.json** — raw block-level enrollment JSON pulled from the GitHub fork and included in the source tree
- **outputs/scenario_summary.csv** — Ranked comparison of all scenarios
- **outputs/*_metrics.json** — Detailed per-school metrics for each scenario

## Selective ingestion

Large generated files are out. HTML maps, boundary GeoJSON, block assignment CSVs, webapp data JSON, and `Polygons.geojson` are not included. The raw block-level JSON is included as `data/student_blocks.json`. The Python code, React code, metrics, and scenario summary are included.
